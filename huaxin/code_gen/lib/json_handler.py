# -*- coding:utf-8 -*-
"""
Created on Jun 20, 2013

@author: Chester.Qian
"""
import json


def getCleanJsonView(data):
    return json.dumps(data, indent=2)


def getJsonData(data):
    json_data = json.loads(data.readline())
    return json_data


def get_stop_polling_flag(mode, values):
    return (mode == 'set' and not values) and True or False


def try_json_loads(data):
    try:
        return json.loads(data)
    except ValueError:
        return False


def handle_item_in_json(candidate, node,
                        key=None, container=None,
                        values=[], mode='get', deep_search=False):
    # value for mode:get,set,pop_key,replace_key_with_value
    # deep_search is False for same keys on the same level
    # deep_search is True for same keys on all level(same&different)
    def handle_get_data(data, _key=None):
        if _key:
            if _key in data:
                data = data[_key]
            else:
                return
        container.append(data)

    def handle_set_data(data, _key):
        if _key in data:
            value = values.pop(0)
            data[_key] = value
        else:
            pass

    def handle_pop_key(data, _key):
        if _key in data:
            data.pop(_key)

    def handle_replace_key_with_value(data, _key):
        if _key in data:
            value = data.pop(_key)

            if values:
                value = values.pop(0)

            if isinstance(value, dict):
                # only supportted when data[_key] is type of dict
                data.update(value)
            else:
                raise Exception('only support dict value')

    def handle(source):
        source_value = source[node]

        if key:

            def _handle_source_value():
                if isinstance(source_value, list):
                        for i in source_value:
                            handle_function(i, key)
                elif isinstance(source_value, dict):
                    handle_function(source_value, key)

            try:
                if isinstance(source_value, list) or isinstance(source_value, dict):
                    _handle_source_value()
                else:
                    # for the sake of capatibilty with form data
                    source_value = try_json_loads(source_value)
                    if source_value:
                        _handle_source_value()
                        source[node] = json.JSONEncoder().encode((source_value))
            except KeyError:
                pass
        else:
            args = ((values,) and (source, node)) or (source_value,)
            handle_function(*args)

    mode_map_function = {
        'get': handle_get_data,
        'set': handle_set_data,
        'pop_key': handle_pop_key,
        'replace_key_with_value': handle_replace_key_with_value
    }

    if container and values:
        msg = 'container and values are mutual exclusive,one of those should be None!'
        raise TypeError(msg)

    if not isinstance(values, list):
        values = [values]

    handle_function = mode_map_function[mode]

    if isinstance(candidate, dict):
        def looping():
            for k in candidate:
                if get_stop_polling_flag(mode, values):
                    break
                handle_item_in_json(candidate[k], node,
                                    key, container, values, mode, deep_search)

        if node in candidate:
            handle(candidate)

            if deep_search:
                looping()
        else:
            looping()
    elif isinstance(candidate, list):
        for i in candidate:
            if get_stop_polling_flag(mode, values):
                break
            if not key:
                try:
                    handle(i)
                except (KeyError, TypeError):
                    pass
                continue

            handle_item_in_json(i, node,
                                key, container, values, mode, deep_search)


if __name__ == '__main__':
    results = []
    results2 = []


    def get_id(candidate):
        # test content get
        # handle_item_in_json(candidate, 'courseStep_id', None, results2)
        # handle_item_in_json(candidate, 'activityContent', "id", results2)
        # handle_item_in_json(candidate, 'pics', "_id", results2)
        # handle_item_in_json(candidate, 'image', "url", results2)
        # handle_item_in_json(candidate, 'id', None, results2)
        # handle_item_in_json(candidate, "node2", "key2", results2)
        # handle_item_in_json(candidate, 'errors', None, results2)
        # handle_item_in_json(candidate, 'content', 'apiReturn', results2)
        # handle_item_in_json(candidate, 'id', None, results2)
        # test content2 get
        # handle_item_in_json(candidate, 'files', "id", results2)
        # handle_item_in_json(candidate, 'type', None, results2)
        # test content3 get
        # handle_item_in_json(candidate, 'loanApp', "id", results2)
        # test content4 get
        # handle_item_in_json(candidate, 'schema', None, results2)
        # handle_item_in_json(candidate, 'issusdInfos', 'productStatus', results2)
        # test content set
        # handle_item_in_json(candidate, 'courseStep_id', None, values=["test1"], mode='set')
        # handle_item_in_json(candidate, 'activityContent', "id", values=["test"], mode='set')
        # handle_item_in_json(candidate, 'pics', "_id", values=["test1", "test2", "test3", "test4"], mode='set')
        # handle_item_in_json(candidate, 'image', "url", values=["test16768", "test2213"], mode='set')
        # handle_item_in_json(candidate, 'id', None, values=["test16768", "test2213"], mode='set')
        # handle_item_in_json(candidate, "node2", "key2", values=["test"], mode='set')
        # handle_item_in_json(candidate, 'errors', None, values="test", mode='set')
        # handle_item_in_json(candidate, 'content', 'apiReturn', values=["test"], mode='set')
        # handle_item_in_json(candidate, 'id', None, values=["test1", "test2"], mode='set')
        # test content2 set
        # handle_item_in_json(candidate, 'files', "id", values=["test1", "test2", "test3"], mode='set')
        # handle_item_in_json(candidate, 'type', None, values=["test"], mode='set')
        # test content3 set
        # handle_item_in_json(candidate, 'loanApp', "id", values=["test1", "test2"], mode='set')
        # print results
        # print len(results2)
        # test content5 set
        handle_item_in_json(candidate, 'issusdInfos', 'productStatus', values=["test"], mode='set')
        # print results2
        print getCleanJsonView(content5)
        assert 0
        return results2


    content = [
        {
            "courseStep_id": 38074,  # result 1 (M1:correct)
            # "activityNo": 3,
            "activityContent":
                {
                    "collapsed": 'true',
                    "id": "activity_content!140921",  # result 2 (M1:correct)
                    "node1":
                        {
                            "key1":
                                {
                                    "node2":
                                        {
                                            "key2": "value"
                                        }
                                }
                        }
                },
            "id": "activity!114944"  # result 5
        },
        {
            "content": {
                "pics": [
                    {
                        "_id": "p_1",  # result 3 (M1:correct)
                        "image": {
                            "url": "I'm the first url.",  # result 4 (M1:correct)
                            "id": "media!129951"
                        }
                    },
                    {
                        "_id": "p_2",  # result 3
                        "image": {
                            "url": "I'm the 2nd url.",  # result 4
                            "id": "media!129950"
                        }
                    }

                ],
                "audios": [
                    {
                        "_id": "a_1",
                        "audio": {
                            "url": "http://schooluat-ak.englishtown.com/Juno/12/98/09/v/129809/GE_9.1.2.2.4_1_v2.mp3",
                            "maxAge": 3600,
                            "collapsed": 'false',
                            "id": "media!129809"}
                    },
                    {
                        "_id": "a_2",
                        "audio": {
                            "url": "http://schooluat-ak.englishtown.com/Juno/12/98/10/v/129810/GE_9.1.2.2.4_2_v2.mp3",
                            "maxAge": 3600,
                            "collapsed": 'false',
                            "id": "media!129810"}
                    }
                ]
            },
            "scoring": {
                "pics": [
                    {
                        "_id": "p_3"  # result 3
                    },
                    {
                        "_id": "p_4"  # result 3
                    }
                ],
                "audios": [
                    {
                        "_id": "a_1",
                        "pic": {
                            "_id": "p_3"
                        }
                    },
                    {
                        "_id": "a_2",
                        "pic": {
                            "_id": "p_4"
                        }
                    }
                ]
            },
            "templateCode": "MatPicToAud",
            "id": "activity_content!140921"  # result 5 (M1: can't find this value)
        },
        {
            "content": {
                "apiReturn": {
                }
            },
            "errors": ["\u5bf9\u4e0d\u8d77\uff0c\u8bf7\u8f93\u5165\u6b63\u786e\u7684\u7528\u6237\u540d"],
            "messages": [],
            "result": "error"
        }
    ]

    content2 = [{"id": 407007, "files": [
        {"id": 920411, "fileName": "LS-831 (2).jpg", "contentType": "JPEG", "date": "2015-07-29 14:15:10"}],
                 "status": "REQUESTED", "optional": "false", "type": "IDENTITY_CARD", "group": "GENERAL"},
                {"files": [], "status": "REQUESTED", "optional": "true", "type": "PBOC_CREDIT_REPORT",
                 "group": "GENERAL"}, {"id": 407008, "files": [
            {"id": 920408, "fileName": "LS-831.jpg", "contentType": "JPEG", "date": "2015-07-29 11:28:19"}],
                                       "status": "REQUESTED", "optional": "false", "type": "RESIDENCE_REGISTRATION",
                                       "group": "GENERAL"},
                {"id": 407201, "files": [], "status": "REQUESTED", "optional": "false", "type": "BANK_CARD",
                 "group": "GENERAL"}, {"id": 407401, "files": [
            {"id": 918806, "fileName": "LS-833 (3).jpg", "contentType": "JPEG", "date": "2015-07-28 10:10:22"}],
                                       "status": "REQUESTED", "optional": "false", "type": "BANK_STATEMENT",
                                       "group": "GENERAL"},
                {"files": [], "status": "REQUESTED", "optional": "true", "type": "PROOF_OF_SALARY",
                 "group": "PERSONAL"},
                {"files": [], "status": "REQUESTED", "optional": "true", "type": "PROPERTY_TITLE_CERTIFICATE",
                 "group": "GENERAL"},
                {"files": [], "status": "REQUESTED", "optional": "true", "type": "LAST_YEAR_TAX_RETURNS",
                 "group": "PERSONAL"},
                {"files": [], "status": "REQUESTED", "optional": "true", "type": "LOAN_PURPOSE_SUPPORT",
                 "group": "GENERAL"},
                {"files": [], "status": "REQUESTED", "optional": "true", "type": "MARRIAGE_CERTIFICATE",
                 "group": "GENERAL"},
                {"files": [], "status": "REQUESTED", "optional": "true", "type": "PROOF_OF_OTHER_LIQUID_ASSETS",
                 "group": "GENERAL"},
                {"files": [], "status": "REQUESTED", "optional": "false", "type": "BORROWER_SALES_APP_PHOTO",
                 "group": "PERSONAL"},
                {"files": [], "status": "REQUESTED", "optional": "true", "type": "OTHER_DOCUMENTS",
                 "group": "PERSONAL"},
                {"id": 407801, "files": [], "status": "REQUESTED", "optional": "false", "type": "APPLICATION_FORM",
                 "group": "GENERAL"}]
    content3 = {"loans": [{
        "loanApp": {
            "id": "1460710999",
            "loanAmount": "50000",
            "loanPurpose": "fund_flow",
            "paymentMethod": "AMORTIZATION",
            "loanMaturity": "Year1"
        },
        "personalInfo": {
            "fullName": "李四",
            "idCard": "441501196805133032",
            "residenceAddress": "成都",
            "mobilePhone": "13334536029",
            "yearlyIncome": "50000",
            "residenceCity": "成都"
        },
        "employmentInfo": {
            "empCity": "成都",
            "companyName": "肯的鸡",
            "companyPhone": "028-6981222",
            "empStreetAddress": "成都",
            "industryCode": "I010",
            "companySize": "MORE_THAN_1000",
            "occupationCode": "O001",
            "jobTenureYears": "2"
        },
        "bankInfo": {
            "accountNumber": "4782573818720",
            "accountName": "李四",
            "financialInstitution": "招商银行",
            "province": "四川",
            "accountBranch": "支行2"
        },
        "contactInfo": [
            {
                "type": "FAMILIES",
                "relation": "BROTHER_AND_SISTER",
                "name": "李四爸",
                "phone": "15982143099",
                "occupationCode": "O005",
                "companyName": "拉拉",
                "address": "成都"
            }
        ]
    }, {
        "loanApp": {
            "id": "2921421998",
            "loanAmount": "50000",
            "loanPurpose": "fund_flow",
            "paymentMethod": "AMORTIZATION",
            "loanMaturity": "Year1"
        },
        "personalInfo": {
            "fullName": "李四",
            "idCard": "441202200510227217",
            "residenceAddress": "成都",
            "mobilePhone": "18019715579",
            "yearlyIncome": "50000",
            "residenceCity": "成都"
        },
        "employmentInfo": {
            "empCity": "成都",
            "companyName": "肯的鸡",
            "companyPhone": "028-6981222",
            "empStreetAddress": "成都",
            "industryCode": "I010",
            "companySize": "MORE_THAN_1000",
            "occupationCode": "O001",
            "jobTenureYears": "2"
        },
        "bankInfo": {
            "accountNumber": "4295195011307737",
            "accountName": "李四",
            "financialInstitution": "招商银行",
            "province": "四川",
            "accountBranch": "支行2"
        },
        "contactInfo": [
            {
                "type": "FAMILIES",
                "relation": "BROTHER_AND_SISTER",
                "name": "李四爸",
                "phone": "15982143099",
                "occupationCode": "O005",
                "companyName": "拉拉",
                "address": "成都"
            }
        ]
    }], "transactionNo": "1460710999"}

    content4 = {u'responses': {u'201': {u'description': u'Created'},
                               u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ApiResult'}},
                               u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                               u'401': {u'description': u'Unauthorized'}}, u'parameters': [
        {u'schema': {u'$ref': u'#/definitions/BorrowerLoanInfoVo'}, u'description': u'req', u'required': True,
         u'name': u'req', u'in': u'body'},
        {u'description': u'appId', u'format': u'int64', u'required': True, u'in': u'path', u'type': u'integer',
         u'name': u'appId'}], u'produces': [u'*/*'], u'tags': [u'borrower-controller'],
                u'summary': u'\u66f4\u65b0\u8d37\u6b3e\u7684\u57fa\u672c\u4fe1\u606f',
                u'consumes': [u'application/json'], u'operationId': u'updateLoanInfoUsingPOST'}
    content4 = {u'responses': {u'201': {u'description': u'Created'},
                               u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/PersonalAttrDto'}},
                               u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                               u'401': {u'description': u'Unauthorized'}}, u'parameters': [
        {u'description': u'aid', u'format': u'int64', u'required': True, u'in': u'path', u'type': u'integer',
         u'name': u'aid'},
        {u'description': u'source', u'required': True, u'type': u'string', u'name': u'source', u'in': u'path'},
        {u'schema': {u'$ref': u'#/definitions/PersonalAttrDto'}, u'description': u'personalAttrDto', u'required': True,
         u'name': u'personalAttrDto', u'in': u'body'}], u'produces': [u'*/*'], u'tags': [u'borrower-info-controller'],
                u'summary': u'\u63d0\u4ea4\u4e2a\u4eba\u7533\u8bf7\u8d44\u6599', u'consumes': [u'application/json'],
                u'operationId': u'submitPersonalApplicationUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ApiResult'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'description': u'id', u'format': u'int64', u'required': True, u'in': u'path', u'type': u'integer',
             u'name': u'id'},
            {u'schema': {u'additionalProperties': {u'type': u'string'}, u'type': u'object'}, u'description': u'map',
             u'required': False, u'name': u'map', u'in': u'body'}], u'produces': [u'*/*'],
                   u'tags': [u'channel-product-config-controller'], u'summary': u'updateQuotaStatus',
                   u'consumes': [u'application/json'], u'operationId': u'updateQuotaStatusUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ModelAndView'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'schema': {u'$ref': u'#/definitions/ModelAndView'}, u'description': u'mav', u'required': False,
             u'name': u'mav', u'in': u'body'}], u'produces': [u'*/*'], u'deprecated': True,
                   u'tags': [u'act-manager-controller'], u'summary': u'showIndex', u'consumes': [u'application/json'],
                   u'operationId': u'showIndexUsingPOST'}, {u'responses': {u'201': {u'description': u'Created'},
                                                                           u'200': {u'description': u'OK', u'schema': {
                                                                               u'$ref': u'#/definitions/ApiResult'}},
                                                                           u'404': {u'description': u'Not Found'},
                                                                           u'403': {u'description': u'Forbidden'},
                                                                           u'401': {u'description': u'Unauthorized'}},
                                                            u'parameters': [
                                                                {u'description': u'appId', u'format': u'int64',
                                                                 u'required': True, u'in': u'path', u'type': u'integer',
                                                                 u'name': u'appId'},
                                                                {u'schema': {u'$ref': u'#/definitions/BankAccountDto'},
                                                                 u'description': u'bankAccountDto', u'required': True,
                                                                 u'name': u'bankAccountDto', u'in': u'body'}],
                                                            u'produces': [u'*/*'],
                                                            u'tags': [u'bank-account-controller'],
                                                            u'summary': u'\u66f4\u65b0\u94f6\u884c\u8d26\u6237\u4fe1\u606f',
                                                            u'consumes': [u'application/json'],
                                                            u'operationId': u'updateBankAccountInfoUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ApiResult'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'description': u'msg', u'required': True, u'type': u'string', u'name': u'msg', u'in': u'formData'}],
                   u'produces': [u'application/json'], u'tags': [u'mq-controller'], u'summary': u'sendMq',
                   u'consumes': [u'application/x-www-form-urlencoded'], u'operationId': u'sendMqUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ApiResult'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'description': u'appId', u'format': u'int64', u'required': True, u'in': u'path', u'type': u'integer',
             u'name': u'appId'}], u'produces': [u'*/*'], u'tags': [u'borrower-controller'],
                   u'summary': u'\u5ba1\u6279\u9000\u56de\u8d37\u6b3e\u7533\u8bf7', u'consumes': [u'application/json'],
                   u'operationId': u'returnBorrowerLoanUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ApiResult'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'schema': {u'$ref': u'#/definitions/BorrowerPermanentDto'}, u'description': u'req', u'required': True,
             u'name': u'req', u'in': u'body'},
            {u'description': u'aid', u'format': u'int64', u'required': True, u'in': u'path', u'type': u'integer',
             u'name': u'aid'}], u'produces': [u'*/*'], u'tags': [u'borrower-controller'],
                   u'summary': u'\u66f4\u65b0\u8d37\u6b3e\u4fe1\u606f\u4e2d\u7684\u8d37\u6b3e\u4eba\u6237\u7c4d\u4fe1\u606f',
                   u'consumes': [u'application/json'], u'operationId': u'updateIdentityCardInfoUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ApiResult'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'description': u'aid', u'required': True, u'type': u'string', u'name': u'aid', u'in': u'path'},
            {u'description': u'uploadedFiles', u'items': {u'type': u'file'}, u'required': True,
             u'collectionFormat': u'multi', u'in': u'query', u'type': u'array', u'name': u'uploadedFiles'},
            {u'description': u'appId', u'format': u'int64', u'required': False, u'in': u'query', u'type': u'integer',
             u'name': u'appId'}], u'produces': [u'*/*'], u'tags': [u'borrower-controller'],
                   u'summary': u'\u4e0a\u4f20\u8d37\u6b3e\u4fe1\u606f\u4e2d\u6240\u9700\u7684\u6587\u4ef6',
                   u'consumes': [u'application/json'], u'operationId': u'uploadDocumentUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ApiResult'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'description': u'aid', u'format': u'int64', u'required': True, u'in': u'path', u'type': u'integer',
             u'name': u'aid'}], u'produces': [u'*/*'], u'tags': [u'borrower-controller'],
                   u'summary': u'\u63d0\u4ea4\u4e00\u7b14\u8d37\u6b3e\u5230crm', u'consumes': [u'application/json'],
                   u'operationId': u'borrowerSubmitLoanAppUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ApiResult'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'description': u'file', u'required': False, u'type': u'file', u'name': u'file', u'in': u'formData'},
            {u'schema': {u'$ref': u'#/definitions/DocumentDto'}, u'description': u'docDto', u'required': False,
             u'name': u'docDto', u'in': u'body'}, {
                u'enum': [u'NONE', u'DIANRONG', u'GENGMEI', u'MIME', u'LIYUN', u'QUARK', u'ALADING', u'ELEME',
                          u'TRADELOAN', u'FANGSILING', u'QFANG', u'DAFY'], u'description': u'userSourcce',
                u'required': False, u'in': u'query', u'type': u'string', u'name': u'userSourcce'}],
                   u'produces': [u'*/*'], u'tags': [u'document-controller'],
                   u'summary': u'\u6839\u636e\u7c7b\u578b(\u5982\u8eab\u4efd\u8bc1)\u4e0a\u4f20\u6587\u4ef6',
                   u'consumes': [u'multipart/form-data'], u'operationId': u'uploadDocumentsInfoByTypeUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ApiResult'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'description': u'appId', u'format': u'int64', u'required': True, u'in': u'path', u'type': u'integer',
             u'name': u'appId'}], u'produces': [u'*/*'], u'tags': [u'borrower-controller'],
                   u'summary': u'\u7528\u4e8ecrm\u63d0\u4ea4\u8d37\u6b3e\u5230crc\u5ba1\u6838',
                   u'consumes': [u'application/json'], u'operationId': u'submitLoanToCrcUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ApiResult'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'description': u'aid', u'required': True, u'type': u'string', u'name': u'aid', u'in': u'path'},
            {u'enum': [u'SHAPING', u'DENTIST', u'ONLINE_EDU'], u'description': u'category', u'required': True,
             u'in': u'query', u'type': u'string', u'name': u'category'},
            {u'schema': {u'$ref': u'#/definitions/LoanAppBundleDto'}, u'description': u'bundle', u'required': True,
             u'name': u'bundle', u'in': u'body'}], u'produces': [u'*/*'], u'tags': [u'geng-mei-controller'],
                   u'summary': u'\u6839\u636eaid\u548ccategory\u7b49\u66f4\u65b0loanapp\u4fe1\u606f',
                   u'consumes': [u'application/json'], u'operationId': u'submitAssociatedLoanAppInfoUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ApiResult'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'description': u'aid', u'format': u'int64', u'required': True, u'in': u'path', u'type': u'integer',
             u'name': u'aid'},
            {u'schema': {u'$ref': u'#/definitions/PersonalBasicInfoDto'}, u'description': u'req', u'required': True,
             u'name': u'req', u'in': u'body'}], u'produces': [u'*/*'], u'tags': [u'borrower-controller'],
                   u'summary': u'\u65b0\u589e\u6216\u66f4\u65b0\u8d37\u6b3e\u4fe1\u606f\u4e2d\u7684\u4e2a\u4eba\u57fa\u672c\u4fe1\u606f',
                   u'consumes': [u'application/json'],
                   u'operationId': u'updateBorrowerAppPersonalBasicInfoUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ApiResult'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'description': u'appId', u'format': u'int64', u'required': True, u'in': u'path', u'type': u'integer',
             u'name': u'appId'},
            {u'schema': {u'$ref': u'#/definitions/LoanAppDto'}, u'description': u'loanInfoDTO', u'required': True,
             u'name': u'loanInfoDTO', u'in': u'body'}], u'produces': [u'*/*'], u'tags': [u'loan-app-controller'],
                   u'summary': u'\u66f4\u65b0\u501f\u6b3e\u4fe1\u606f', u'consumes': [u'application/json'],
                   u'operationId': u'updateLoanInfoUsingPOST_1'}, {u'responses': {u'201': {u'description': u'Created'},
                                                                                  u'200': {u'description': u'OK',
                                                                                           u'schema': {
                                                                                               u'$ref': u'#/definitions/ApiResult'}},
                                                                                  u'404': {
                                                                                      u'description': u'Not Found'},
                                                                                  u'403': {
                                                                                      u'description': u'Forbidden'},
                                                                                  u'401': {
                                                                                      u'description': u'Unauthorized'}},
                                                                   u'parameters': [
                                                                       {u'description': u'appId', u'format': u'int64',
                                                                        u'required': True, u'in': u'path',
                                                                        u'type': u'integer', u'name': u'appId'},
                                                                       {u'description': u'rejectCode',
                                                                        u'required': True, u'type': u'string',
                                                                        u'name': u'rejectCode', u'in': u'query'}],
                                                                   u'produces': [u'*/*'],
                                                                   u'tags': [u'borrower-controller'],
                                                                   u'summary': u'\u5ba1\u6279\u62d2\u7edd\u8d37\u6b3e\u7533\u8bf7',
                                                                   u'consumes': [u'application/json'],
                                                                   u'operationId': u'updateBorrowerLoanStatusByRejectedActionUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ModelAndView'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'schema': {u'$ref': u'#/definitions/ModelAndView'}, u'description': u'mav', u'required': False,
             u'name': u'mav', u'in': u'body'}], u'produces': [u'*/*'], u'deprecated': True,
                   u'tags': [u'act-manager-controller'], u'summary': u'setAllRetriesAs20',
                   u'consumes': [u'application/json'], u'operationId': u'setAllRetriesAs20UsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ApiResult'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'description': u'appId', u'format': u'int64', u'required': True, u'in': u'path', u'type': u'integer',
             u'name': u'appId'},
            {u'description': u'gpId', u'format': u'int64', u'required': True, u'in': u'path', u'type': u'integer',
             u'name': u'gpId'},
            {u'schema': {u'$ref': u'#/definitions/GuarantorPersonalDto'}, u'description': u'dto', u'required': True,
             u'name': u'dto', u'in': u'body'}], u'produces': [u'*/*'], u'tags': [u'guarantor-controller'],
                   u'summary': u'\u66f4\u65b0\u4e2a\u4eba\u62c5\u4fdd\u4fe1\u606f, owner:jie.xu',
                   u'consumes': [u'application/json'], u'operationId': u'updateGuarantorPersonalUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ApiResult'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'schema': {u'$ref': u'#/definitions/BorrowerLoanInfoVo'}, u'description': u'req', u'required': True,
             u'name': u'req', u'in': u'body'},
            {u'description': u'appId', u'format': u'int64', u'required': True, u'in': u'path', u'type': u'integer',
             u'name': u'appId'}], u'produces': [u'*/*'], u'tags': [u'borrower-controller'],
                   u'summary': u'\u66f4\u65b0\u8d37\u6b3e\u7684\u57fa\u672c\u4fe1\u606f',
                   u'consumes': [u'application/json'], u'operationId': u'updateLoanInfoUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ApiResult'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'description': u'appId', u'format': u'int64', u'required': True, u'in': u'path', u'type': u'integer',
             u'name': u'appId'},
            {u'schema': {u'$ref': u'#/definitions/LoanWithdrawalInfoDto'}, u'description': u'req', u'required': True,
             u'name': u'req', u'in': u'body'}], u'produces': [u'*/*'], u'tags': [u'borrower-controller'],
                   u'summary': u'\u5ba2\u6237\u53d6\u6d88\u8d37\u6b3e\u7533\u8bf7', u'consumes': [u'application/json'],
                   u'operationId': u'withdrawalBorrowerLoanUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ApiResult'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'description': u'appId', u'format': u'int64', u'required': True, u'in': u'path', u'type': u'integer',
             u'name': u'appId'},
            {u'schema': {u'$ref': u'#/definitions/HouseInfoDto'}, u'description': u'houseInfoDto', u'required': True,
             u'name': u'houseInfoDto', u'in': u'body'}], u'produces': [u'*/*'], u'tags': [u'house-controller'],
                   u'summary': u'\u521b\u5efa\u6216\u66f4\u65b0\u8d2d\u623f\u4fe1\u606f',
                   u'consumes': [u'application/json'], u'operationId': u'updateHouseInfoUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'}, u'200': {u'description': u'OK', u'schema': {
                       u'$ref': u'#/definitions/ConsumerLoanAppDto'}}, u'404': {u'description': u'Not Found'},
                                  u'403': {u'description': u'Forbidden'}, u'401': {u'description': u'Unauthorized'}},
                   u'parameters': [{u'description': u'aid', u'format': u'int64', u'required': True, u'in': u'path',
                                    u'type': u'integer', u'name': u'aid'},
                                   {u'description': u'source', u'required': True, u'type': u'string',
                                    u'name': u'source', u'in': u'path'},
                                   {u'schema': {u'$ref': u'#/definitions/ConsumerLoanAppDto'},
                                    u'description': u'loanAppDto', u'required': True, u'name': u'loanAppDto',
                                    u'in': u'body'}], u'produces': [u'*/*'], u'tags': [u'borrower-loan-app-controller'],
                   u'summary': u'\u521b\u5efa\u501f\u6b3e\u7533\u8bf7', u'consumes': [u'application/json'],
                   u'operationId': u'submitLoanAppUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'}, u'200': {u'description': u'OK'},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'schema': {u'type': u'string'}, u'description': u'procDefId', u'required': False, u'name': u'procDefId',
             u'in': u'body'},
            {u'schema': {u'type': u'string'}, u'description': u'procInstId', u'required': False, u'name': u'procInstId',
             u'in': u'body'}], u'produces': [u'*/*'], u'deprecated': True, u'tags': [u'act-manager-controller'],
                   u'summary': u'graphics', u'consumes': [u'application/json'], u'operationId': u'graphicsUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ApiResult'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'description': u'aid', u'format': u'int64', u'required': True, u'in': u'path', u'type': u'integer',
             u'name': u'aid'},
            {u'schema': {u'$ref': u'#/definitions/BorrowerBankAccountDto'}, u'description': u'bankAccountDto',
             u'required': True, u'name': u'bankAccountDto', u'in': u'body'}], u'produces': [u'*/*'],
                   u'tags': [u'borrower-controller'],
                   u'summary': u'\u65b0\u589e\u6216\u66f4\u65b0\u8d37\u6b3e\u4fe1\u606f\u4e2d\u7684\u94f6\u884c\u5361\u8d26\u6237\u4fe1\u606f',
                   u'consumes': [u'application/json'], u'operationId': u'updateBankAccountUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ApiResult'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'description': u'appId', u'format': u'int64', u'required': True, u'in': u'path', u'type': u'integer',
             u'name': u'appId'},
            {u'schema': {u'$ref': u'#/definitions/CorporateGuarantorDto'}, u'description': u'guarantorDto',
             u'required': True, u'name': u'guarantorDto', u'in': u'body'}], u'produces': [u'*/*'],
                   u'tags': [u'guarantor-controller'],
                   u'summary': u'\u521b\u5efa\u4e00\u6761\u62c5\u4fdd\u4fe1\u606f\u8bb0\u5f55',
                   u'consumes': [u'application/json'], u'operationId': u'addCorporateGuarantorUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ApiResult'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'description': u'appId', u'format': u'int64', u'required': True, u'in': u'path', u'type': u'integer',
             u'name': u'appId'},
            {u'description': u'updateIfExists', u'required': False, u'type': u'boolean', u'name': u'updateIfExists',
             u'in': u'query'},
            {u'schema': {u'$ref': u'#/definitions/ContactInfoDto'}, u'description': u'contactInfoDto',
             u'required': True, u'name': u'contactInfoDto', u'in': u'body'}], u'produces': [u'*/*'],
                   u'tags': [u'contacts-controller'], u'summary': u'\u6dfb\u52a0\u4e00\u4e2a\u8054\u7cfb\u4eba',
                   u'consumes': [u'application/json'], u'operationId': u'addContactsUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'}, u'200': {u'description': u'OK', u'schema': {
                       u'$ref': u'#/definitions/PersonalBasicInfoDto'}}, u'404': {u'description': u'Not Found'},
                                  u'403': {u'description': u'Forbidden'}, u'401': {u'description': u'Unauthorized'}},
                   u'parameters': [{u'description': u'aid', u'format': u'int64', u'required': True, u'in': u'path',
                                    u'type': u'integer', u'name': u'aid'},
                                   {u'description': u'source', u'required': True, u'type': u'string',
                                    u'name': u'source', u'in': u'path'},
                                   {u'schema': {u'$ref': u'#/definitions/PersonalBasicInfoDto'},
                                    u'description': u'personalBasicInfoDto', u'required': True,
                                    u'name': u'personalBasicInfoDto', u'in': u'body'}], u'produces': [u'*/*'],
                   u'tags': [u'borrower-info-controller'],
                   u'summary': u'\u586b\u5199\u4e2a\u4eba\u57fa\u672c\u4fe1\u606f', u'consumes': [u'application/json'],
                   u'operationId': u'submitPersonalBasicInfoUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ApiResult'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'description': u'appId', u'format': u'int64', u'required': True, u'in': u'path', u'type': u'integer',
             u'name': u'appId'},
            {u'schema': {u'$ref': u'#/definitions/GuarantorPersonalDto'}, u'description': u'dto', u'required': True,
             u'name': u'dto', u'in': u'body'}], u'produces': [u'*/*'], u'tags': [u'guarantor-controller'],
                   u'summary': u'\u65b0\u589e\u4e2a\u4eba\u62c5\u4fdd\u4fe1\u606f, owner:jie.xu',
                   u'consumes': [u'application/json'], u'operationId': u'addGuarantorPersonalUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ApiResult'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'description': u'appId', u'format': u'int64', u'required': True, u'in': u'path', u'type': u'integer',
             u'name': u'appId'},
            {u'schema': {u'$ref': u'#/definitions/PersonalInfoDto'}, u'description': u'personalInfoDto',
             u'required': True, u'name': u'personalInfoDto', u'in': u'body'}], u'produces': [u'*/*'],
                   u'tags': [u'personal-info-controller'],
                   u'summary': u'\u65b0\u589e\u6216\u66f4\u65b0\u8d37\u6b3e\u7533\u8bf7\u7684\u4e2a\u4eba\u4fe1\u606f',
                   u'consumes': [u'application/json'], u'operationId': u'upsertPersonalInfoUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ApiResult'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'description': u'aid', u'format': u'int64', u'required': True, u'in': u'path', u'type': u'integer',
             u'name': u'aid'},
            {u'schema': {u'$ref': u'#/definitions/PersonalDebtInfoDto'}, u'description': u'req', u'required': True,
             u'name': u'req', u'in': u'body'}], u'produces': [u'*/*'], u'tags': [u'borrower-controller'],
                   u'summary': u'\u66f4\u65b0\u8d37\u6b3e\u4fe1\u606f\u4e2d\u7684\u4e2a\u4eba\u8d1f\u503a\u4fe1\u606f\uff08debt\u7684\u6570\u91cf\uff09',
                   u'consumes': [u'application/json'], u'operationId': u'updateBorrowerAppPersonalDebtInfoUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ApiResult'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'description': u'appId', u'format': u'int64', u'required': True, u'in': u'path', u'type': u'integer',
             u'name': u'appId'},
            {u'schema': {u'$ref': u'#/definitions/JobInfoDto'}, u'description': u'jobInfoDto', u'required': True,
             u'name': u'jobInfoDto', u'in': u'body'}], u'produces': [u'*/*'], u'tags': [u'job-controller'],
                   u'summary': u'\u66f4\u65b0\u804c\u4e1a\u4fe1\u606f', u'consumes': [u'application/json'],
                   u'operationId': u'updateJobInfoUsingPOST'}, {u'responses': {u'201': {u'description': u'Created'},
                                                                               u'200': {u'description': u'OK',
                                                                                        u'schema': {
                                                                                            u'$ref': u'#/definitions/ApiResult'}},
                                                                               u'404': {u'description': u'Not Found'},
                                                                               u'403': {u'description': u'Forbidden'},
                                                                               u'401': {
                                                                                   u'description': u'Unauthorized'}},
                                                                u'parameters': [
                                                                    {u'description': u'aid', u'format': u'int64',
                                                                     u'required': True, u'in': u'path',
                                                                     u'type': u'integer', u'name': u'aid'}, {
                                                                        u'schema': {
                                                                            u'$ref': u'#/definitions/BorrowerEmploymentDto'},
                                                                        u'description': u'borrowerEmploymentDto',
                                                                        u'required': True,
                                                                        u'name': u'borrowerEmploymentDto',
                                                                        u'in': u'body'}], u'produces': [u'*/*'],
                                                                u'tags': [u'borrower-controller'],
                                                                u'summary': u'\u65b0\u589e\u6216\u4fee\u6539\u8d37\u6b3e\u4fe1\u606f\u4e2d\u7684\u4e2a\u4eba\u5de5\u4f5c\u4fe1\u606f',
                                                                u'consumes': [u'application/json'],
                                                                u'operationId': u'updateBorrowerAppEmploymentInfoUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ApiResult'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'schema': {u'type': u'integer', u'format': u'int64'}, u'description': u'userId', u'required': False,
             u'name': u'userId', u'in': u'body'},
            {u'description': u'loanAppId', u'format': u'int64', u'required': True, u'in': u'path', u'type': u'integer',
             u'name': u'loanAppId'}, {u'schema': {u'type': u'integer', u'format': u'int32'},
                                      u'description': u'\u501f\u6b3e\u7c7b\u578b(\u5982:\u53cc\u91d1\u8d37)',
                                      u'required': False, u'name': u'loanType', u'in': u'body'},
            {u'schema': {u'type': u'string'}, u'description': u'authType', u'required': False, u'name': u'authType',
             u'in': u'body'},
            {u'schema': {u'type': u'string'}, u'description': u'\u6388\u6743\u72b6\u6001(fail,success,pending)',
             u'required': False, u'name': u'status', u'in': u'body'}], u'produces': [u'*/*'],
                   u'tags': [u'third-party-auth-controller'],
                   u'summary': u'\u589e\u52a0\u3001\u66f4\u65b0\u4e00\u6761\u7b2c\u4e09\u65b9\u6388\u6743\u4fe1\u606f\u8bb0\u5f55, owner:jie.xu',
                   u'consumes': [u'application/json'], u'operationId': u'updateThirdPartyAuthV2UsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ModelAndView'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'schema': {u'$ref': u'#/definitions/ModelAndView'}, u'description': u'mav', u'required': False,
             u'name': u'mav', u'in': u'body'}], u'produces': [u'*/*'], u'deprecated': True,
                   u'tags': [u'act-manager-controller'], u'summary': u'deleteAll', u'consumes': [u'application/json'],
                   u'operationId': u'deleteAllUsingPOST'}, {u'responses': {u'201': {u'description': u'Created'},
                                                                           u'200': {u'description': u'OK', u'schema': {
                                                                               u'$ref': u'#/definitions/ApiResult'}},
                                                                           u'404': {u'description': u'Not Found'},
                                                                           u'403': {u'description': u'Forbidden'},
                                                                           u'401': {u'description': u'Unauthorized'}},
                                                            u'parameters': [{u'description': u'aid', u'required': True,
                                                                             u'type': u'string', u'name': u'aid',
                                                                             u'in': u'path'}, {u'schema': {
                                                                u'$ref': u'#/definitions/LoanAppBundleDto'},
                                                                                u'description': u'bundle',
                                                                                u'required': True,
                                                                                u'name': u'bundle',
                                                                                u'in': u'body'}],
                                                            u'produces': [u'*/*'], u'tags': [u'geng-mei-controller'],
                                                            u'summary': u'\u7533\u8bf7\u66f4\u7f8e\u501f\u6b3e\u4fe1\u606f',
                                                            u'consumes': [u'application/json'],
                                                            u'operationId': u'addGMLoanAppUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ApiResult'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'description': u'actorId', u'required': True, u'type': u'string', u'name': u'actorId', u'in': u'path'},
            {u'schema': {u'$ref': u'#/definitions/CreditDto'}, u'description': u'dto', u'required': True,
             u'name': u'dto', u'in': u'body'}], u'produces': [u'*/*'], u'tags': [u'credit-controller'],
                   u'summary': u'\u6dfb\u52a0\u7528\u6237\u6388\u4fe1\u989d\u5ea6', u'consumes': [u'application/json'],
                   u'operationId': u'addCreditUsingPOST'}, {u'responses': {u'201': {u'description': u'Created'},
                                                                           u'200': {u'description': u'OK', u'schema': {
                                                                               u'$ref': u'#/definitions/ApiResult'}},
                                                                           u'404': {u'description': u'Not Found'},
                                                                           u'403': {u'description': u'Forbidden'},
                                                                           u'401': {u'description': u'Unauthorized'}},
                                                            u'parameters': [
                                                                {u'description': u'appId', u'format': u'int64',
                                                                 u'required': True, u'in': u'path', u'type': u'integer',
                                                                 u'name': u'appId'}], u'produces': [u'*/*'],
                                                            u'tags': [u'mortgage-controller'],
                                                            u'summary': u'\u65b0\u589e\u4e00\u6761\u62b5\u62bc\u8bb0\u5f55',
                                                            u'consumes': [u'application/json'],
                                                            u'operationId': u'addMortgageUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ApiResult'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'description': u'loanAppId', u'format': u'int64', u'required': True, u'in': u'path', u'type': u'integer',
             u'name': u'loanAppId'},
            {u'description': u'matrixPolicyEnum', u'required': True, u'type': u'string', u'name': u'matrixPolicyEnum',
             u'in': u'path'},
            {u'schema': {u'$ref': u'#/definitions/MatrixCallbackResponse'}, u'description': u'matrixResponse',
             u'required': True, u'name': u'matrixResponse', u'in': u'body'}], u'produces': [u'*/*'],
                   u'tags': [u'matrix-controller'], u'summary': u'matrixPolicyCallBack',
                   u'consumes': [u'application/json'], u'operationId': u'matrixPolicyCallBackUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ModelAndView'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'schema': {u'$ref': u'#/definitions/ModelAndView'}, u'description': u'mav', u'required': False,
             u'name': u'mav', u'in': u'body'}], u'produces': [u'*/*'], u'deprecated': True,
                   u'tags': [u'act-manager-controller'], u'summary': u'suspendAll', u'consumes': [u'application/json'],
                   u'operationId': u'suspendAllUsingPOST'}, {u'responses': {u'201': {u'description': u'Created'},
                                                                            u'200': {u'description': u'OK', u'schema': {
                                                                                u'$ref': u'#/definitions/JsonResult'}},
                                                                            u'404': {u'description': u'Not Found'},
                                                                            u'403': {u'description': u'Forbidden'},
                                                                            u'401': {u'description': u'Unauthorized'}},
                                                             u'parameters': [
                                                                 {u'schema': {u'type': u'integer', u'format': u'int64'},
                                                                  u'description': u'userId', u'required': False,
                                                                  u'name': u'userId', u'in': u'body'},
                                                                 {u'description': u'loanAppId', u'format': u'int64',
                                                                  u'required': True, u'in': u'path',
                                                                  u'type': u'integer', u'name': u'loanAppId'},
                                                                 {u'schema': {u'type': u'integer', u'format': u'int32'},
                                                                  u'description': u'\u501f\u6b3e\u7c7b\u578b(\u5982:\u53cc\u91d1\u8d37)',
                                                                  u'required': False, u'name': u'loanType',
                                                                  u'in': u'body'}, {u'schema': {u'type': u'string'},
                                                                                    u'description': u'authType',
                                                                                    u'required': False,
                                                                                    u'name': u'authType',
                                                                                    u'in': u'body'},
                                                                 {u'schema': {u'type': u'string'},
                                                                  u'description': u'\u6388\u6743\u72b6\u6001(fail,success,pending)',
                                                                  u'required': False, u'name': u'status',
                                                                  u'in': u'body'}], u'produces': [u'*/*'],
                                                             u'tags': [u'third-party-auth-controller'],
                                                             u'summary': u'\u589e\u52a0\u3001\u66f4\u65b0\u4e00\u6761\u7b2c\u4e09\u65b9\u6388\u6743\u4fe1\u606f\u8bb0\u5f55, owner:jie.xu',
                                                             u'consumes': [u'application/json'],
                                                             u'operationId': u'updateThirdPartyAuthUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ApiResult'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'description': u'source', u'required': True, u'type': u'string', u'name': u'source', u'in': u'path'},
            {u'description': u'extId', u'required': True, u'type': u'string', u'name': u'extId', u'in': u'path'}],
                   u'produces': [u'*/*'], u'tags': [u'loan-app-controller'],
                   u'summary': u'\u53d6\u6d88\u501f\u6b3e\u72b6\u6001', u'consumes': [u'application/json'],
                   u'operationId': u'updateStatusUsingPOST_1'}, {u'responses': {u'201': {u'description': u'Created'},
                                                                                u'200': {u'description': u'OK',
                                                                                         u'schema': {
                                                                                             u'$ref': u'#/definitions/ApiResult'}},
                                                                                u'404': {u'description': u'Not Found'},
                                                                                u'403': {u'description': u'Forbidden'},
                                                                                u'401': {
                                                                                    u'description': u'Unauthorized'}},
                                                                 u'parameters': [
                                                                     {u'description': u'aid', u'format': u'int64',
                                                                      u'required': True, u'in': u'path',
                                                                      u'type': u'integer', u'name': u'aid'}, {
                                                                         u'schema': {
                                                                             u'$ref': u'#/definitions/PersonalAssetInfoDto'},
                                                                         u'description': u'req', u'required': True,
                                                                         u'name': u'req', u'in': u'body'}],
                                                                 u'produces': [u'*/*'],
                                                                 u'tags': [u'borrower-controller'],
                                                                 u'summary': u'\u65b0\u589e\u6216\u66f4\u65b0\u8d37\u6b3e\u4fe1\u606f\u4e2d\u7684\u4e2a\u4eba\u8d44\u4ea7\u4fe1\u606f\uff08\u4e2a\u4eba\u623f\u4ea7\u6570\u91cf\uff09',
                                                                 u'consumes': [u'application/json'],
                                                                 u'operationId': u'updateBorrowerAppPersonalAssetInfoUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ApiResult'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'description': u'aid', u'format': u'int64', u'required': True, u'in': u'path', u'type': u'integer',
             u'name': u'aid'},
            {u'schema': {u'items': {u'$ref': u'#/definitions/BorrowerContactsVo'}, u'type': u'array'},
             u'description': u'contactInfo', u'required': True, u'name': u'contactInfo', u'in': u'body'}],
                   u'produces': [u'*/*'], u'tags': [u'borrower-controller'],
                   u'summary': u'\u65b0\u589e\u6216\u4fee\u6539\u8d37\u6b3e\u4fe1\u606f\u4e2d\u7684\u8054\u7cfb\u4eba\u4fe1\u606f',
                   u'consumes': [u'application/json'], u'operationId': u'updateBorrowerAppContactInfoUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ModelAndView'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'schema': {u'$ref': u'#/definitions/ModelAndView'}, u'description': u'mav', u'required': False,
             u'name': u'mav', u'in': u'body'}], u'produces': [u'*/*'], u'deprecated': True,
                   u'tags': [u'act-manager-controller'], u'summary': u'login', u'consumes': [u'application/json'],
                   u'operationId': u'loginUsingPOST'}, {u'responses': {u'201': {u'description': u'Created'},
                                                                       u'200': {u'description': u'OK', u'schema': {
                                                                           u'$ref': u'#/definitions/ApiResult'}},
                                                                       u'404': {u'description': u'Not Found'},
                                                                       u'403': {u'description': u'Forbidden'},
                                                                       u'401': {u'description': u'Unauthorized'}},
                                                        u'parameters': [{u'description': u'appId', u'format': u'int64',
                                                                         u'required': True, u'in': u'path',
                                                                         u'type': u'integer', u'name': u'appId'},
                                                                        {u'description': u'cgId', u'format': u'int64',
                                                                         u'required': True, u'in': u'path',
                                                                         u'type': u'integer', u'name': u'cgId'}, {
                                                                            u'schema': {
                                                                                u'$ref': u'#/definitions/CorporateGuarantorDto'},
                                                                            u'description': u'guarantorDto',
                                                                            u'required': True, u'name': u'guarantorDto',
                                                                            u'in': u'body'}], u'produces': [u'*/*'],
                                                        u'tags': [u'guarantor-controller'],
                                                        u'summary': u'\u66f4\u65b0\u4e00\u6761\u4f01\u4e1a\u62c5\u4fdd\u8bb0\u5f55',
                                                        u'consumes': [u'application/json'],
                                                        u'operationId': u'updateCorporateGuarantorUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ApiResult'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'description': u'appId', u'format': u'int64', u'required': True, u'in': u'path', u'type': u'integer',
             u'name': u'appId'},
            {u'description': u'mortgageId', u'format': u'int64', u'required': True, u'in': u'path', u'type': u'integer',
             u'name': u'mortgageId'}], u'produces': [u'*/*'], u'tags': [u'mortgage-controller'],
                   u'summary': u'\u66f4\u65b0\u4e00\u6761\u62b5\u62bc\u4fe1\u606f\u8bb0\u5f55',
                   u'consumes': [u'application/json'], u'operationId': u'updateMortgageUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ApiResult'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'enum': [u'PERMIT', u'BLACKLIST', u'DEBT', u'CREDIT'], u'description': u'policyEnum', u'required': True,
             u'in': u'path', u'type': u'string', u'name': u'policyEnum'}], u'produces': [u'*/*'],
                   u'tags': [u'activiti-controller'], u'summary': u'isMatrixEnabled',
                   u'consumes': [u'application/json'], u'operationId': u'isMatrixEnabledUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ApiResult'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'description': u'aid', u'required': True, u'type': u'string', u'name': u'aid', u'in': u'path'},
            {u'schema': {u'$ref': u'#/definitions/LoanAppDto'}, u'description': u'loanInfoDto', u'required': True,
             u'name': u'loanInfoDto', u'in': u'body'}], u'produces': [u'*/*'], u'tags': [u'loan-app-controller'],
                   u'summary': u'\u65b0\u589e\u501f\u6b3e\u4fe1\u606f', u'consumes': [u'application/json'],
                   u'operationId': u'addLoanInfoUsingPOST'}, {u'responses': {u'201': {u'description': u'Created'},
                                                                             u'200': {u'description': u'OK',
                                                                                      u'schema': {
                                                                                          u'$ref': u'#/definitions/ApiResult'}},
                                                                             u'404': {u'description': u'Not Found'},
                                                                             u'403': {u'description': u'Forbidden'},
                                                                             u'401': {u'description': u'Unauthorized'}},
                                                              u'parameters': [
                                                                  {u'description': u'appId', u'format': u'int64',
                                                                   u'required': True, u'in': u'path',
                                                                   u'type': u'integer', u'name': u'appId'}],
                                                              u'produces': [u'*/*'], u'tags': [u'loan-app-controller'],
                                                              u'summary': u'\u53d6\u6d88\u501f\u6b3e\u72b6\u6001',
                                                              u'consumes': [u'application/json'],
                                                              u'operationId': u'updateStatusUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ApiResult'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'description': u'aid', u'required': True, u'type': u'string', u'name': u'aid', u'in': u'path'},
            {u'schema': {u'$ref': u'#/definitions/LoanAppDto'}, u'description': u'loanApp', u'required': True,
             u'name': u'loanApp', u'in': u'body'}], u'produces': [u'*/*'], u'tags': [u'geng-mei-controller'],
                   u'summary': u'\u521b\u5efa\u66f4\u7f8e\u501f\u6b3e', u'consumes': [u'application/json'],
                   u'operationId': u'createByCreditUsingPOST'}, {u'responses': {u'201': {u'description': u'Created'},
                                                                                u'200': {u'description': u'OK',
                                                                                         u'schema': {
                                                                                             u'$ref': u'#/definitions/ModelAndView'}},
                                                                                u'404': {u'description': u'Not Found'},
                                                                                u'403': {u'description': u'Forbidden'},
                                                                                u'401': {
                                                                                    u'description': u'Unauthorized'}},
                                                                 u'parameters': [{u'schema': {
                                                                     u'$ref': u'#/definitions/ModelAndView'},
                                                                     u'description': u'mav',
                                                                     u'required': False, u'name': u'mav',
                                                                     u'in': u'body'}],
                                                                 u'produces': [u'*/*'], u'deprecated': True,
                                                                 u'tags': [u'act-manager-controller'],
                                                                 u'summary': u'reset',
                                                                 u'consumes': [u'application/json'],
                                                                 u'operationId': u'resetUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/LoanAppVo'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'schema': {u'$ref': u'#/definitions/BorrowerLoanAppDto'}, u'description': u'borrowerApp',
             u'required': True, u'name': u'borrowerApp', u'in': u'body'},
            {u'description': u'aid', u'format': u'int64', u'required': True, u'in': u'path', u'type': u'integer',
             u'name': u'aid'}], u'produces': [u'*/*'], u'tags': [u'borrower-controller'],
                   u'summary': u'\u65b0\u589e\u4e00\u7b14\u8d37\u6b3e\u57fa\u672c\u4fe1\u606f',
                   u'consumes': [u'application/json'], u'operationId': u'addLoanAppUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ApiResult'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'description': u'source', u'required': True, u'type': u'string', u'name': u'source', u'in': u'path'},
            {u'description': u'extId', u'required': True, u'type': u'string', u'name': u'extId', u'in': u'path'}],
                   u'produces': [u'*/*'], u'tags': [u'loan-app-controller'],
                   u'summary': u'\u8fbe\u6210\u501f\u6b3e\u534f\u8bae', u'consumes': [u'application/json'],
                   u'operationId': u'loanAgreementUsingPOST_1'}, {u'responses': {u'201': {u'description': u'Created'},
                                                                                 u'200': {u'description': u'OK',
                                                                                          u'schema': {
                                                                                              u'$ref': u'#/definitions/ModelAndView'}},
                                                                                 u'404': {u'description': u'Not Found'},
                                                                                 u'403': {u'description': u'Forbidden'},
                                                                                 u'401': {
                                                                                     u'description': u'Unauthorized'}},
                                                                  u'parameters': [{u'schema': {
                                                                      u'$ref': u'#/definitions/ModelAndView'},
                                                                      u'description': u'mav',
                                                                      u'required': False, u'name': u'mav',
                                                                      u'in': u'body'}],
                                                                  u'produces': [u'*/*'], u'deprecated': True,
                                                                  u'tags': [u'act-manager-controller'],
                                                                  u'summary': u'jobManagement',
                                                                  u'consumes': [u'application/json'],
                                                                  u'operationId': u'jobManagementUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ApiResult'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'description': u'aid', u'format': u'int64', u'required': True, u'in': u'path', u'type': u'integer',
             u'name': u'aid'},
            {u'schema': {u'$ref': u'#/definitions/PersonalIncomeInfoDto'}, u'description': u'req', u'required': True,
             u'name': u'req', u'in': u'body'}], u'produces': [u'*/*'], u'tags': [u'borrower-controller'],
                   u'summary': u'\u66f4\u65b0\u8d37\u6b3e\u4fe1\u606f\u4e2d\u7684\u4e2a\u4eba\u6536\u5165\u4fe1\u606f\uff08\u5e74\u6536\u5165\u7684\u91d1\u989d\uff09',
                   u'consumes': [u'application/json'],
                   u'operationId': u'updateBorrowerAppPersonalIncomeInfoUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ApiResult'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'schema': {u'additionalProperties': {u'type': u'string'}, u'type': u'object'}, u'description': u'map',
             u'required': True, u'name': u'map', u'in': u'body'}], u'produces': [u'*/*'],
                   u'tags': [u'geng-mei-controller'],
                   u'summary': u'\u67e5\u8be2\u66f4\u7f8e\u805a\u4fe1\u529b\u6821\u9a8c\u7ed3\u679c',
                   u'consumes': [u'application/json'], u'operationId': u'juXinLiCheckResultUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ApiResult'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'description': u'appId', u'format': u'int64', u'required': True, u'in': u'path', u'type': u'integer',
             u'name': u'appId'},
            {u'description': u'personalId', u'format': u'int64', u'required': True, u'in': u'path', u'type': u'integer',
             u'name': u'personalId'},
            {u'schema': {u'$ref': u'#/definitions/PersonalInfoDto'}, u'description': u'personalInfoDTO',
             u'required': True, u'name': u'personalInfoDTO', u'in': u'body'}], u'produces': [u'*/*'],
                   u'tags': [u'personal-info-controller'],
                   u'summary': u'\u6839\u636ePersonalId\u66f4\u65b0\u8d37\u6b3e\u7533\u8bf7\u4e2d\u7684\u4e2a\u4eba\u4fe1\u606f',
                   u'consumes': [u'application/json'], u'operationId': u'updatePersonalInfoUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ApiResult'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'description': u'appId', u'format': u'int64', u'required': True, u'in': u'path', u'type': u'integer',
             u'name': u'appId'},
            {u'description': u'contactId', u'format': u'int64', u'required': True, u'in': u'path', u'type': u'integer',
             u'name': u'contactId'},
            {u'schema': {u'$ref': u'#/definitions/ContactInfoDto'}, u'description': u'contactInfoDto',
             u'required': True, u'name': u'contactInfoDto', u'in': u'body'}], u'produces': [u'*/*'],
                   u'tags': [u'contacts-controller'],
                   u'summary': u'\u6839\u636e\u8054\u7cfb\u4ebaId\u66f4\u65b0\u8054\u7cfb\u4eba\u4fe1\u606f',
                   u'consumes': [u'application/json'], u'operationId': u'updateContactByIdUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ModelAndView'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'schema': {u'$ref': u'#/definitions/ModelAndView'}, u'description': u'mav', u'required': False,
             u'name': u'mav', u'in': u'body'}], u'produces': [u'*/*'], u'deprecated': True,
                   u'tags': [u'act-manager-controller'], u'summary': u'activateAll', u'consumes': [u'application/json'],
                   u'operationId': u'activateAllUsingPOST'}, {u'responses': {u'201': {u'description': u'Created'},
                                                                             u'200': {u'description': u'OK',
                                                                                      u'schema': {
                                                                                          u'$ref': u'#/definitions/ApiResult'}},
                                                                             u'404': {u'description': u'Not Found'},
                                                                             u'403': {u'description': u'Forbidden'},
                                                                             u'401': {u'description': u'Unauthorized'}},
                                                              u'parameters': [
                                                                  {u'description': u'appId', u'format': u'int64',
                                                                   u'required': True, u'in': u'path',
                                                                   u'type': u'integer', u'name': u'appId'}],
                                                              u'produces': [u'*/*'], u'tags': [u'loan-app-controller'],
                                                              u'summary': u'\u8fbe\u6210\u501f\u6b3e\u534f\u8bae',
                                                              u'consumes': [u'application/json'],
                                                              u'operationId': u'loanAgreementUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ModelAndView'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'schema': {u'$ref': u'#/definitions/ModelAndView'}, u'description': u'mav', u'required': False,
             u'name': u'mav', u'in': u'body'}], u'produces': [u'*/*'], u'deprecated': True,
                   u'tags': [u'act-manager-controller'], u'summary': u'running', u'consumes': [u'application/json'],
                   u'operationId': u'runningUsingPOST'}, {u'responses': {u'201': {u'description': u'Created'},
                                                                         u'200': {u'description': u'OK', u'schema': {
                                                                             u'$ref': u'#/definitions/ApiResult'}},
                                                                         u'404': {u'description': u'Not Found'},
                                                                         u'403': {u'description': u'Forbidden'},
                                                                         u'401': {u'description': u'Unauthorized'}},
                                                          u'parameters': [{u'description': u'loanIds',
                                                                           u'items': {u'type': u'integer',
                                                                                      u'format': u'int64'},
                                                                           u'required': True,
                                                                           u'collectionFormat': u'multi',
                                                                           u'in': u'query', u'type': u'array',
                                                                           u'name': u'loanIds'},
                                                                          {u'description': u'from',
                                                                           u'format': u'date-time', u'required': True,
                                                                           u'in': u'query', u'type': u'string',
                                                                           u'name': u'from'}, {u'description': u'to',
                                                                                               u'format': u'date-time',
                                                                                               u'required': True,
                                                                                               u'in': u'query',
                                                                                               u'type': u'string',
                                                                                               u'name': u'to'}],
                                                          u'produces': [u'*/*'], u'tags': [u'transaction-controller'],
                                                          u'summary': u'getTransactionHistoryRecord',
                                                          u'consumes': [u'application/json'],
                                                          u'operationId': u'getTransactionHistoryRecordUsingPOST'}, {
                   u'responses': {u'201': {u'description': u'Created'},
                                  u'200': {u'description': u'OK', u'schema': {u'$ref': u'#/definitions/ApiResult'}},
                                  u'404': {u'description': u'Not Found'}, u'403': {u'description': u'Forbidden'},
                                  u'401': {u'description': u'Unauthorized'}}, u'parameters': [
            {u'enum': [u'PERMIT', u'BLACKLIST', u'DEBT', u'CREDIT'], u'description': u'policyEnum', u'required': True,
             u'in': u'path', u'type': u'string', u'name': u'policyEnum'},
            {u'description': u'enable', u'required': True, u'type': u'boolean', u'name': u'enable', u'in': u'path'},
            {u'schema': {u'type': u'boolean'}, u'description': u'expectedRes', u'required': False,
             u'name': u'expectedRes', u'in': u'body'}], u'produces': [u'*/*'], u'tags': [u'activiti-controller'],
                   u'summary': u'enableMatrix', u'consumes': [u'application/json'],
                   u'operationId': u'enableMatrixUsingPOST'}, {u'responses': {u'201': {u'description': u'Created'},
                                                                              u'200': {u'description': u'OK',
                                                                                       u'schema': {
                                                                                           u'$ref': u'#/definitions/ModelAndView'}},
                                                                              u'404': {u'description': u'Not Found'},
                                                                              u'403': {u'description': u'Forbidden'},
                                                                              u'401': {
                                                                                  u'description': u'Unauthorized'}},
                                                               u'parameters': [
                                                                   {u'schema': {u'$ref': u'#/definitions/ModelAndView'},
                                                                    u'description': u'mav', u'required': False,
                                                                    u'name': u'mav', u'in': u'body'}],
                                                               u'produces': [u'*/*'], u'deprecated': True,
                                                               u'tags': [u'act-manager-controller'],
                                                               u'summary': u'setAllRetriesAs0',
                                                               u'consumes': [u'application/json'],
                                                               u'operationId': u'setAllRetriesAs0UsingPOST'}

    content5 = {
                "productid":"H9#H99914",
                "productNo":"H99914",
                "institutionProductCategoryCode":"H901",
                "taNo":"H9",
                "issueFacevalue":"1",
                "shareClass":"",
                "displayFundType":"",
                "ackBuyDay":"",
                "transferDays": "",
                "productFullName":"批量生成014",
                "taName":"华信资管ta",
                "currencyType":"156",
                "productRisklevel": "",
                "navFracnum": "",
                "ackRedeemDay": "",
                "deliveryDay": "",
                "productShortName":"批量生成014",
                "productType":"3",
                "shareType":"*",
                "fundType": "0",
                "navFracmode": "",
                "buyDay": "",
                "dividendDay": "",
                "minSubscribeAmount":"100",
                "minBuyAmount":"10",
                "minRspAmount":"",
                "minAddAmount":"100",
                "maxSubscribeAmount":"10000",
                "maxBuyAmount":"5000",
                "minHoldAmount":"",
                "rangeAmount":"100",
                "minRedeemAmount":"100",
                "minConvertAmount": "",
                "minAddSubscribe":"100",
                "issusdInfos":'''[{"acceptMode":"","issueTime":"20161010094800","dssubEndtime":"20161110094800","bidTime":"20161210094800","productExpiredtime":"20170410094800","liquidationTime":"20170411094800","productStatus":"4","reservationEndTime":""}]''',
                "allowChangeDividendWay":"",
                "dividendSettlementDay": "",
                "fundManagerCode": "",
                "ackSubscribeDate": "",
                "highWealthType":"0",
                "pageNo":"1",
                "pageSize":"100",
                }

    print getCleanJsonView(content5)

    f = get_id(content5)
    print f
    print len(f)
