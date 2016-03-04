# -*- coding: utf-8 -*-
# Copyright (c) 20016-2016 The Cloudsoar.
# See LICENSE for details.

"""
"""

COLLECTOR = 10000

SUCCESS = 0
FAIL = COLLECTOR
MAX_ERROR_CODE = COLLECTOR +10000


UNCAUGHT_EXCEPTION_ERR = COLLECTOR + 1


AUTHEN_ERROR = COLLECTOR + 100
INVALID_TOKEN_ERR      = AUTHEN_ERROR + 1                # 无效的token
ERR_LOGIN_TIMEOUT      = AUTHEN_ERROR + 2                # 登录超时
USER_UN_LOGIN_ERR      = AUTHEN_ERROR + 3                # 用户未登录
ERR_ACCESS_IDNOTEXIST  = AUTHEN_ERROR + 4                # access_uuid不存在
ERR_NO_TOKEN_PARAM     = AUTHEN_ERROR + 5                # 缺少token
ERR_TIME_MISMATCH      = AUTHEN_ERROR + 6                # 时间偏移超过限制范围

ERR_TIMESTAMP_REPEAT   = AUTHEN_ERROR + 7                # 时间戳重复，调用太频繁或非法调用 

PERMISSION_DENIED_ERR  = AUTHEN_ERROR + 8                # 用户权限不够
ERR_UNDEFINED_RING     = AUTHEN_ERROR + 9                # 未定义的ring
NO_SUCH_GROUP_ERR      = AUTHEN_ERROR + 10               # 分组不存在
NO_SUCH_USER_ERR       = AUTHEN_ERROR + 11               # 用户不存在
INVALID_PASSWORD_ERR   = AUTHEN_ERROR + 12               # 密码错误
ERR_ACCESS_AUTHENFAIL  = AUTHEN_ERROR + 13               # 密钥未通过验证




COMMON_ERR = COLLECTOR + 200
FILE_OPERATE_ERR = COMMON_ERR + 1
CALL_REMOTE_METHOD_ERR = COMMON_ERR + 2
REMOTE_SERVICE_ABNORMAL_ERR = COMMON_ERR + 3
SERVER_IS_DISCONNECT_ERR = COMMON_ERR + 4     # 服务器连接断开

ERR_SERVICE_INACTIVE = COMMON_ERR + 5
INTERNAL_OPERATE_ERR = COMMON_ERR + 6
INTERNAL_EXCEPT_ERR = COMMON_ERR + 7
PERMISSION_DENIED_ERR = COMMON_ERR + 8
ERR_METHOD_CONFLICT = COMMON_ERR + 10
RESULT_FORMAT_INVALID = COMMON_ERR + 11
INVALID_PARAM_ERR = COMMON_ERR + 12
INVALID_RESULT_DATA_ERR = COMMON_ERR + 13


CONFIG_OUT_OF_LIMIT_ERR = COMMON_ERR + 50                # 用户输入超出配置限制
DATE_FAMAT_IS_INVALID = COMMON_ERR + 51                  # 日期格式不合法
PARAME_IS_INVALID_ERR = COMMON_ERR + 52                  # 参数不合法



DB_ERROR               = COLLECTOR + 500
DATABASE_EXCEPT_ERR    = DB_ERROR + 1                    # 数据库异常
NO_SUCH_RECORD_ERR     = DB_ERROR + 3                    # 记录不存在
IDENTITY_KEY_NOT_EXIST_ERR = DB_ERROR + 9                # 记录信息中没有ID
FILTER_IS_INVALID_ERR = DB_ERROR + 10                    # 过滤条件不合法


CONSOLE_ERROR = COLLECTOR + 1000

INVALID_PARAMETERS_ERR = CONSOLE_ERROR + 1               # 
NO_IMPLEMENT_INTERFACE_ERR = CONSOLE_ERROR + 2           # 没有实现对应的接口





