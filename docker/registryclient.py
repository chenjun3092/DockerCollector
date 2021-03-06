# -*- coding: utf-8 -*-
#!/usr/bin/env python
# Copyright (c) 20016-2016 The Cloudsoar.
# See LICENSE for details.
'''
Created on 2016-3-8

@author: Jack
'''

import json
import re

from common.util import Result
from frame.Logger import Log, PrintStack
from frame.curlclient import CURLClient
from frame.errcode import FAIL
from mongoimpl.docker.layerdbimpl import LayerDBImpl
from mongoimpl.docker.repositorydbimpl import RepositoryDBImpl
from mongoimpl.docker.tagdbimpl import TagDBImpl


class RegistryClient(CURLClient):
    '''
    # 实现 Dockers registry的接口
    '''

    def __init__(self):
        '''
        Constructor
        '''
        username = 'registry_username'
        pwd = 'registry_password'
        #domain = GetSysConfig('registry_domain') or '192.168.2.55:5000'
        domain = '192.168.2.55:5000'
        CURLClient.__init__(self, username, pwd, domain)
        

    def load_registry_data(self):
        rlt = self.listing_repositories(100)
        if not rlt.success:
            return rlt
        
        data = rlt.content
        RepositoryDBImpl.instance().upsert_repository(data['repositories'])
        
        for repo in data['repositories']:
            rlt = self.listing_image_tags(repo)
            if rlt.success:
                TagDBImpl.instance().upsert_tags(repo, rlt.content['tags'])
                self.load_tag_data(repo, rlt.content['tags'])
            else:
                Log(1, 'load_registry_data.listing_image_tags fail,as[no tags], repository[%s]'%(repo))
                
                
    def load_tag_data(self, repository_name, tags):
        for tag in tags:
            rlt = self.read_tag_detail(repository_name, tag)
            if rlt.success:
                if not TagDBImpl.instance().is_tag_exist(repository_name, tag, rlt.content['digest']):
                    TagDBImpl.instance().update_tag_info(repository_name, tag, rlt.content['digest'])
                    LayerDBImpl.instance().save_layer_info(rlt.content)
    
    def listing_repositories( self, num, last=0 ):
        url = "http://" + self.domain + '/v2/_catalog?n=%d&last=%d'%(num, last)
        response = self.do_get(url)
        if response.fail:
            response.log('listing_repositories')
            return Result(response.body, FAIL, response.message)
            
        try:
            return Result(json.loads(response.body))
        except Exception:
            PrintStack()
            Log(1,"listing_repositories format to json fail,body[%s]"%(response.body))
            return Result('', FAIL, 'json.loads fail')

        
    def listing_image_tags(self, repository_name):
        url = "http://" + self.domain + '/v2/%s/tags/list'%(repository_name)
        response = self.do_get(url)
        if response.fail:
            response.log('listing_image_tags')
            return Result(response.body, FAIL, response.message)
        
        try:
            return Result(json.loads(response.body))
        except Exception:
            PrintStack()
            Log(1,"listing_image_tags format to json fail,body[%s]"%(response.body))
            return Result('', FAIL, 'json.loads fail')
    
    
    def read_tag_detail(self, repository_name, tag='latest'):
        """
        # 读取指定tag的信息
        """
        url = "http://" + self.domain + '/v2/%s/manifests/%s'%(repository_name,tag)
        response = self.do_get(url)
        if response.fail:
            response.log('repository_detail')
            return Result(response.body, FAIL, response.message)
        
        info = {}
        try:
            data = json.loads(response.body)
            info['fsLayers'] = data.get('fsLayers',[])
        except Exception:
            PrintStack()
            Log(1,"repository_detail format to json fail,body[%s]"%(response.body))

            
        m = re.search(r"Docker-Content-Digest: ([^\s]+)*", response.respond_headers)
        if m:
            info['digest'] = m.group(1)
        else:
            Log(1,"repository_detail get Docker-Content-Digest fail,header[%s]"%(response.respond_headers))
            
        if info:
            return Result(info)
        else:
            return Result('', FAIL, 'Fail Get data from registry.')
        
    
        
    def read_tag_detail2(self, url):
        url = url.replace('localhost:5000',self.domain)
        response = self.do_get(url)
        if response.fail:
            response.log('repository_detail')
            return Result(response.body, FAIL, response.message)
        
        info = {}
        try:
            data = json.loads(response.body)
            info['fsLayers'] = data.get('layers',[])
        except Exception:
            PrintStack()
            Log(1,"repository_detail format to json fail,body[%s]"%(response.body))

            
        m = re.search(r"Docker-Content-Digest: ([^\s]+)", response.respond_headers)
        if m:
            info['digest'] = m.group(1)
        else:
            Log(1,"repository_detail get Docker-Content-Digest fail,header[%s]"%(response.respond_headers))
            
        if info:
            return Result(info)
        else:
            return Result('', FAIL, 'Fail Get data from registry.')
    
        
    def delete_image(self, repository_name, digest):
        url = "http://" + self.domain + '/v2/%s/manifests/%s'%(repository_name, digest)
        response = self.do_delete(url)
        if response.fail:
            response.log('delete_image')
        response.log('delete_image')
        
        

        
        

        
        
            
        
        
        
        