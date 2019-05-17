# coding: utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from huaxin_restful_service.restful_cms_service.main_restful_cms_entity import MainResfulCmsEntity
from _tools.mysql_xjb_tools import MysqlXjbTools


class RestfulCmsTools(object):
    def __init__(self):
        self.entity = MainResfulCmsEntity()
        self.mysql = MysqlXjbTools()

    # 登录
    def login(self):
        try:
            self.entity.login()
        except Exception, e:
            print e
            pass

    # CMS优惠券发放
    def issue_coupon(self, code, mobile, quantity, env='CI'):
        try:
            cust_no = self.mysql.get_cust_info(columns='cust_no', match='=', mobile=mobile)[0]['cust_no']
            trade_acco = self.mysql.get_trade_acco_info(cust_no=cust_no)[0]['trade_acco']
            if env is 'CI':
                self.entity.login()
            else:
                # UAT
                self.entity.login(username='zuodongxiang', password='39385da1627e73a537dc26111b7530c5')
            self.entity.add_coupon_record(code=code, tradeAcco=trade_acco, custNo=cust_no, qty=quantity)
            latest_coupon_record = self.mysql.get_coupon_import_record(cust_no=cust_no, trade_acco=trade_acco)[0]
            entity = self.entity.issue_coupon_record(id=str(latest_coupon_record['id']))
            message = entity.message

            print message

        except Exception, e:
            print e
            pass


if __name__ == '__main__':
    m = RestfulCmsTools()
    m.issue_coupon(code='FULL_OFF_10000_10_0171', mobile='18019281762', quantity='1', env='UAT')
