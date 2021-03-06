# -*- coding: utf-8 -*-
# Copyright (c) 20016-2016 The Cloudsoar.
# See LICENSE for details.
"""
Implement Order data manage
"""

import threading

from common.guard import LockGuard
from common.util import NowMilli, Result
from frame.Logger import Log
from mongodb.dbbase import DBBase
from mongodb.dbconst import MAIN_DB_NAME, REPOSITORY_TABLE, ID


class RepositoryDBImpl(DBBase):
    db = MAIN_DB_NAME
    collection = REPOSITORY_TABLE
    __lock = threading.Lock()
    
    @classmethod
    def instance(cls):
        '''
        Limits application to single instance
        '''
        with LockGuard(cls.__lock):
            if not hasattr(cls, "_instance"):
                cls._instance = cls()
        return cls._instance
    
    
    def __init__(self):
        DBBase.__init__(self, self.db, self.collection)
        
    def is_repository_exsit(self, repository):
        rlt = self.count({ID: repository})
        if rlt.success and rlt.content>0:
            return True
        return False
        
    def upsert_repository(self, repositories):
        rlt = self.read_record_list(fields=[])
        if not rlt.success:
            Log(1, 'upsert_repository.read_record_list fail,as[%s]'%(rlt.message))
            return rlt
        
        local_repos = []
        new_repos = []
        lost_repos = []
        for repo in rlt.content:
            local_repos.append(repo[ID])
            if repo[ID] not in repositories:
                lost_repos.append(repo[ID])
        
        for repo in repositories:
            if repo not in local_repos:
                new_repos.append({ID:repo, 'push_time':NowMilli(), 'is_public':True, 'delete':0, 'desc':''})

        if len(new_repos) > 0:
            rlt = self.batch_insert(new_repos)
            if rlt.success:
                Log(3, 'upsert_repository insert [%d] new record'%(rlt.content) )
            else:
                Log(1, 'upsert_repository insert record fail,as[%s]'%(rlt.message) )
        
        if len(lost_repos) > 0:
            rlt = self.updates({ID:{'$in':lost_repos}}, {'delete':NowMilli()})
            if rlt.success:
                Log(3, 'upsert_repository update [%d] old record'%(rlt.content) )
            else:
                Log(1, 'upsert_repository update record fail,as[%s]'%(rlt.message) )
                
        return Result(len(new_repos) + len(lost_repos))
        
        
            
            
            
            
            
            
            
            
            
            
            
        