# coding: utf-8
from _common.global_controller import GlobalController
from _tools.mysql_xjb_tools import MysqlXjbTools
from code_gen.lib.service_entity_factory import EntityFactory
from huaxin_restful_service.restful_cms_service.coupon_add_entity import CouponAddEntity
from huaxin_restful_service.restful_cms_service.coupon_issuecoupon_entity import CouponIssuecouponEntity
from huaxin_restful_service.restful_cms_service.user_login_entity import UserLoginEntity


class MainResfulCmsEntity(object):
    def __init__(self):
        self._entity_factory = EntityFactory(status=True, concurrent_mode=False)
        self._mysql = MysqlXjbTools()
        self._domain_name = GlobalController.RESTFUL_CMS

        self._common_headers = None
        self._h5_headers = None
        # self._current_device_id = None

        self.current_entity = None
        self.current_login_token = None

    # @property
    # def common_headers(self, client_version='a-3.1.0'):
    #     if not self._common_headers:
    #         self._common_headers = {'clientVersion': client_version}
    #         device_id = self.current_device_id
    #
    #         if device_id:
    #             self._common_headers.update({'deviceId': device_id})
    #         else:
    #             raise Exception('device id is not generated!')
    #
    #     return self._common_headers

    @property
    def h5_headers(self):
        # if not self._h5_headers:
        #     self._h5_headers = {'clientVersion': client_version, 'channel': channel}
        #     device_id = self.current_device_id
        #     if device_id:
        #         self._h5_headers.update({'deviceId': device_id})
        #     else:
        #         raise Exception('device id is not generated!')

        return self._h5_headers

    # @property
    # def current_device_id(self):
    #     if not self._current_device_id:
    #         device_info = u"{\"uuid\":\"AD982D9C-1992-367A-B6E6-54086C1040B5\",\"buildNo\":\"1607\",\"idfa\":\"0CF7678B-BE2B-4DC4-9079-78D9D831F197\",\"osVersion\":\"7.0\",\"appId\":\"com.shhxzq.xjbEnt\",\"locale\":\"zh\",\"os\":\"android\",\"isJailBroken\":\"0\",\"density\":\"3.0\",\"appVersion\":\"3.0.0\",\"model\":\"ZUK Z2131\",\"carrier\":\"-\",\"resolution\":\"640x1136\"}"
    #         last_12_random = Utility().GetData().GenAlphanumeric(12).upper()
    #         device_info = device_info.replace('78D9D831F197', last_12_random)
    #
    #         self._current_device_id = self.get_device_id(deviceInfo=device_info)
    #
    #     return self._current_device_id

    # def get_device_id(self, **kwargs):
    #     entity = self._entity_factory.get_entity(
    #         V1ServicesCommonAcquiredeviceidEntity, self._domain_name,
    #         **{'request_headers': self.common_headers})
    #
    #     self.current_entity = entity
    #     entity.send_request(**kwargs)
    #
    #     return entity.deviceId

    def login(self, **kwargs):
        entity = self._entity_factory.get_entity(
            UserLoginEntity, self._domain_name,
            **{'request_headers': self.h5_headers})

        self.current_entity = entity
        entity.send_request(**kwargs)

        self.current_login_token = entity.body_token

        return entity

    def add_coupon_record(self, **kwargs):
        entity = self._entity_factory.get_entity(
            CouponAddEntity, self._domain_name,
            **{'request_headers': self.h5_headers})

        self.current_entity = entity
        entity.send_request(**kwargs)

        return entity

    def issue_coupon_record(self, **kwargs):
        entity = self._entity_factory.get_entity(
            CouponIssuecouponEntity, self._domain_name,
            **{'request_headers': self.h5_headers})

        self.current_entity = entity
        entity.send_request(**kwargs)

        return entity


if __name__ == '__main__':
    m = MainResfulCmsEntity()
