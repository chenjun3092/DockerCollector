# -*- coding: utf-8 -*-
# Copyright (c) 20016-2016 The Cloudsoar.
# See LICENSE for details.
import json
import re


from common.util import Result
from docker.registryclient import RegistryClient
from frame.Logger import Log
from frame.authen import ring8
from frame.errcode import FAIL
from mongodb.dbconst import MAIN_DB_NAME
from mongoimpl.docker.layerdbimpl import LayerDBImpl
from mongoimpl.docker.notifydbimpl import NotifyDBImpl
from mongoimpl.docker.tagdbimpl import TagDBImpl


_ALL = "All"

class NotifyMgr(object):
    db = MAIN_DB_NAME
    
    def __init__(self):
        pass

    @ring8
    def Save(self, post_data, *args):
        data = json.loads(post_data)
        if isinstance(data, dict) and 'events' in data:
            for event in data['events']:
                self.save_event(event)
        else:
            Log(1, 'invalid data[%s]'%(post_data))
            return Result('', FAIL, 'invalid data')
    
    def save_event(self, event):
        rlt = NotifyDBImpl.instance().create(event)
        if not rlt.success:
            Log(1, 'save_event[%s]fail,as[%s]'%(str(event), rlt.content))
        
        action = event.get('action','')
        if action == 'pull':
            # HEAD 请求用于检测manifest是否存在
            if event['request']['method'] == 'HEAD':
                return rlt
            return self.parse_pull_action(event.get('target',None))
        elif action == 'push':
            return self.parse_push_action(event.get('target',None))
        else:
            Log(1, 'unknow action[%s]'%(action))
            return Result('', FAIL, 'unknow action')
   
        
    def parse_pull_action(self, event):
        if self.is_manifest(event['repository'], event['url']):
            return TagDBImpl.instance().add_tag_pull_num(event['digest'])
        else:
            return LayerDBImpl.instance().add_layer_pull_num(event['digest'])

        
    def parse_push_action(self, event):
        if not self.is_manifest(event['repository'], event['url']):
            Log(3,'this is a layer')
            
        #if not RepositoryDBImpl.instance().is_repository_exsit(event['repository']):
        client = RegistryClient()
        rlt = client.read_tag_detail2(event['url'])
        if not rlt.success:
            Log(1, 'parse_push_action.read_tag_detail2 fail,as[%s]'%(rlt.message))
            return rlt
        
        if not TagDBImpl.instance().is_tag_exist(event['repository'], '', rlt.content['digest']):
            TagDBImpl.instance().update_tag_info(event['repository'], '', rlt.content['digest'])
            LayerDBImpl.instance().save_layer_info(rlt.content)
            
                
        

    def is_manifest(self, repository, url):
        repository = repository.replace('/', '\/')
        m = re.search(r"\/%s\/manifests\/"%(repository), url)
        if m:
            return True
        return False

    