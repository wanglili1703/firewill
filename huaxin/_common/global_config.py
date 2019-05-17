# coding: utf-8

import inspect
import os
import re
import sys

import time


def get_resource_root_path():
    string_separator = 'huaxin'
    current_module_path = inspect.getmodule(get_resource_root_path).__file__
    init_path = re.split(string_separator, current_module_path)[0]
    resource_path = os.path.normpath(os.path.join(init_path, string_separator))
    return resource_path


sys.path.append(get_resource_root_path())

import MySQLdb.cursors
import MySQLdb

ASSERT_LIST = []
ASSERT_DICT = {}
ASSERT_DICT_ = {}


class GlobalConfig:
    PREFIX = '+-+'
    RESOURCE_ROOT_PATH = get_resource_root_path()
    SESSION = {"current_domain_name": ""}
    COOKIES = {"cookies": None}

    class PageTimeControl:
        WebDriverWait_TimeOut = 15
        SwipePage_Time = 1000
        Scroll_Time = 1000
        SwipePage_TryTime = 15

    class HuaXinMySql:
        DBC_UAT = {'host': '10.199.105.111',
                   'user': 'dbexecute',
                   'passwd': "cfcs123",
                   'db': "",
                   'port': 3306,
                   'charset': 'utf8',
                   'cursorclass': MySQLdb.cursors.DictCursor,
                   }

        DBC_CI = {'host': '10.199.111.1',
                  'user': 'superqa',
                  'passwd': "superqa",
                  'db': "",
                  'port': 3306,
                  'charset': 'utf8',
                  'cursorclass': MySQLdb.cursors.DictCursor,
                  }
        DBC_BEIDOU = {
            'host': '10.199.101.18',
            'user': 'beidou',
            'passwd': 'beidou',
            'db': "",
            'port': 3308,
            'charset': 'utf8',
            'cursorclass': MySQLdb.cursors.DictCursor,
        }
        DBC_HSJY = {
            'host': '10.199.103.160',
            'user': 'hsjy',
            'passwd': 'hsjy',
            'db': "",
            'port': 3308,
            'charset': 'utf8',
            'cursorclass': MySQLdb.cursors.DictCursor,
        }

    class HuaXinRedis:
        REDIS_CI = {
            'host': '10.199.111.4',
            'port': '6379',
            'auth': 'askme',
        }

    class DbQueryTimeControl:
        DbQuery_TimeSpan = 3
        DbQuery_TryTime = 15

    class PathControl:
        SCREEN_SHOT = get_resource_root_path() + '/'

    class HeaderContentType:
        FORM = "application/x-www-form-urlencoded; charset=UTF-8"
        JSON = "application/json; charset=utf-8"

    class RestfulEnvironment:
        HUAXIN_XJB_UAT = '10.199.105.121:8080'
        # HUAXIN_XJB_CI = '10.199.111.2'
        HUAXIN_XJB_CI = '10.199.111.2'
        HUAXIN_CMS_UAT = '10.199.105.127:8088'
        HUAXIN_CMS_CI = '10.199.111.24:8080'

    class XjbApp:
        Xjb_App_1_8_UAT = get_resource_root_path() + '/apps/android_xjb_1_8/hxxjb-uat-latest.apk'
        Xjb_App_2_0_UAT = get_resource_root_path() + '/apps/android_xjb_2_0/hxxjb-uat-latest.apk'
        Xjb_App_2_0_CI = get_resource_root_path() + '/apps/android_xjb_2_0/hxxjb-ptest-latest.apk'
        Xjb_App_3_0_CI = get_resource_root_path() + '/apps/android_xjb_3_0/hxxjb-ptest-latest.apk'
        Xjb_App_3_0_UAT = get_resource_root_path() + '/apps/android_xjb_3_0/hxxjb-uat-latest.apk'
        Xjb_App_1_8_IOS_UAT = get_resource_root_path() + '/apps/ios_xjb_1_8/hxxjb-ios-uat-latest.app'
        Xjb_App_2_0_IOS_UAT = get_resource_root_path() + '/apps/ios_xjb_2_0/HXXjb.app'

    class XjbAccountInfo:
        # huawei eva al00
        XJB_CI_USER_1 = {
            'u1': {
                'user_name': '13328553876',
                'login_password': 'a0000000',
                'trade_password': '142536',
                'high_end_product': u'自动化专用',
                'high_end_product_for_points': u'UI自动化高端积分测试',
                'high_end_product_amount': '10.00',
                'high_end_product_for_fast_redeem': u'restful测试',
                'dqb_product': u'UI自动化定期产品测试',
                'dqb_product_2': u'UI自动化定期产品赎回测试',
                'dqb_product_3': u'UI自动化积分测试--定期',
                'dqb_product_for_coupon': u'UI自动化优惠券测试--定期',
                'dqb_product_code_3': 'SP9206',
                'dqb_product_amount': '10.00',
                'search_with_full_name': u'RPC测试专用',
                'search_with_short_name': 'R',
                'credit_card_no': '6259198855364125',
                # 'credit_card_no': '62591988536415',
                'last_card_no': '4125',
                'last_card_no_for_repay': '6685',
                # 'last_card_no': '6415',
                # 'repay_credit_card_no': '5309854552866685',   # 13328553876
                'repay_credit_card_no': '6227615438852695',
                'fund_product_name': u'博时医疗保健行业混合A',
                'fund_product_name_2': u'雷克萨斯',
                'fund_product_name_3': u'RESTFUL基金001099',
                # 'fund_product_name_for_select': u'雷克萨斯A',
                'fund_product_name_for_redeem': u'博时医疗保健行业混合A(050026)',
                'fund_product_name_for_fast_redeem': u'基金极速卖出-UI自动化测试',
                'fund_product_name_for_fund_selected': u'基金极速卖出',
                'fund_product_name_for_newly_raised_fund': u'restful基金认购测试',
                'fund_product_code': '050026',
                'fund_product_code_2': 'A09201',
                'fund_product_amount': '10.00',
                'fund_fast_convert_from': u'restful基金极速转换A',
                'fund_fast_convert_to': u'restful基金极速转换B',
                'fund_normal_convert_from': u'restful基金普通转换1',
                'fund_normal_convert_to': u'restful基金普通转换2',
                'dqb_product_amount_2': '1.00',
                'credit_card_repay_amount': '10.00',
                'credit_card_reserved_pay_amount': '1',
                'reservation_code_buy_quota': '0.00',
                'reservation_code_buy_count': '0',
                'reservation_code_reserve_quota': '1.00',
                'reservation_code_reserve_count': '1',
                'product_id_for_reservation_code': '899#SP9205',
                'reserve_code': '83809736',
                'csi_index': '中证500',
                'fund_company': u'博时基金管理有限公司',
                'pledge_amount': '100',
                'pledge_repay_amount': '100',
                'amount_min': '0',
                'amount_max': '50001000000',
                'amount_xjb_max': '100000000000',
                'recharge_amount': '1000',
                'fund_product_amount_for_coupon': '10.00',
                'pay_card_last_no': '1360',
                'pay_card_last_no_for_modification': '1136',
                'financing_amount': '1.00',
                'repay_loan_amount': '1.00',
                'cash_management_product': 'restful作为支付手段',
                'cash_management_product_for_excess': 'UI作为支付手段异常测试',
                'superposed_coupon_code': 'FULL_OFF_3_1_0053',
                'nonsuperposed_coupon_code': 'FULL_OFF_3_1_0055',
                'credit_card_repay_coupon_code': 'FULL_OFF_3_1_0070',
                'credit_card_reserved_repay_coupon_code': 'FULL_OFF_3_1_0071',
                'superposed_coupon_quantity': '2',
                'nonsuperposed_coupon_quantity': '1',
                'user_name_for_add_credit_card_without_binding_bank_card': '13400001239',
                'user_name_for_over_seventy_years_old': '13400001238',
                'bank_card_no_for_certificated_user_binding_card': '6222022222333344',
                'user_name_for_certificated_user_binding_card': '13271175772',
                'user_name_for_bank_card_resign': '13400001243',
                'user_name_for_modify_login_mode': '13400001242',
                'user_name_for_modify_mobile_without_sms': '13466466497',
                'user_name_for_reevaluating': '13983532931',
                'user_name_for_recharge_use_new_card': '13984863493',
                'bank_card_no_for_resign': '6210306555555855',
                'radical_user': '13400001235',
                'conservative_user': '13400001236',
                'cautious_user': '13400001237',
                'unevaluated_user': '13400001240',
                'name': '黄*',
                'risk_type': '稳健型',
                'financial_fund_product_name': 'UI理财型基金',
                'financial_fund_product_code': '53#530034',
                'high_end_quotation_product_code': 'H9#H90034',
                'mail': 'abc@163.com',
                'address': u'南京西路399号',
                'fund_product_for_hot_topic': '大成新锐产业混合',

            },
            'u2': {
                'user_name': '13079141536',
                'login_password': 'a0000000',
                'trade_password': '135790',
                'csi_index': '中证500',
                'fund_product_name': u'博时医疗保健行业混合A',
                'fund_product_code': '050026',
                'fund_product_code_2': 'A09201',
                'fund_product_name_2': u'雷克萨斯',
                'fund_company': u'博时基金管理有限公司',
                'dqb_product_3': u'UI自动化积分测试--定期',
                'dqb_product_code_3': 'SP9206',
                'high_end_product_for_points': u'UI自动化高端积分测试',
                'dqb_product_for_coupon': u'UI自动化优惠券测试--定期',
                'reservation_code_buy_quota': '0.00',
                'reservation_code_buy_count': '0',
                'reservation_code_reserve_quota': '1.00',
                'reservation_code_reserve_count': '1',
                'product_id_for_reservation_code': '899#SP9205',
                'reserve_code': '83809736',
                'amount_min': '0',
                'amount_max': '50000100',
                'amount_xjb_max': '100000000000',
            },
            'u3': {
                'user_name': '15005243789',
                'login_password': 'a0000000',
                'trade_password': '135790',
                'csi_index': '中证500',
                'fund_product_name': u'博时医疗保健行业混合A',
                'fund_product_code': '050026',
                'fund_product_code_2': 'A09201',
                'fund_product_name_2': u'雷克萨斯',
                'fund_company': u'博时基金管理有限公司',
                'dqb_product_3': u'UI自动化积分测试--定期',
                'dqb_product_code_3': 'SP9206',
                'high_end_product_for_points': u'UI自动化高端积分测试',
                'dqb_product_for_coupon': u'UI自动化优惠券测试--定期',
            },
        }

        # vivo x7
        XJB_CI_USER_2 = {
            'u1': {
                'user_name': '15011243991',
                'login_password': 'a0000000',
                'trade_password': '135790',
                'high_end_product': u'自动化专用',
                'high_end_product_amount': '10.00',
                'high_end_product_for_fast_redeem': u'restful测试',
                'high_end_product_for_points': u'UI自动化高端积分测试',
                'dqb_product': u'UI自动化定期产品测试',
                'dqb_product_amount': '10.00',
                'dqb_product_2': u'UI自动化定期产品赎回测试',
                'dqb_product_3': u'UI自动化积分测试--定期',
                'dqb_product_for_coupon': u'UI自动化优惠券测试--定期',
                'dqb_product_code_3': 'SP9206',
                'search_with_full_name': u'RPC测试专用',
                'search_with_short_name': 'R',
                'credit_card_no': '6259198855364126',
                'last_card_no': '4126',
                'repay_credit_card_no': '6227615438852696',
                'fund_product_name': u'博时医疗保健行业混合A',
                'fund_product_name_2': u'雷克萨斯',
                'fund_product_name_for_redeem': u'博时医疗保健行业混合A(050026)',
                'fund_product_name_for_fast_redeem': u'基金极速卖出-UI自动化测试',
                'fund_product_name_for_newly_raised_fund': u'restful基金认购测试',
                'fund_product_code': '050026',
                'fund_product_code_2': 'A09201',
                'fund_product_amount': '10.00',
                'fund_fast_convert_from': u'restful基金极速转换A',
                'fund_fast_convert_to': u'restful基金极速转换B',
                'dqb_product_amount_2': '1.00',
                'credit_card_repay_amount': '10.00',
                'credit_card_reserved_pay_amount': '10',
                'csi_index': '中证500',
                'reservation_code_buy_quota': '0.00',
                'reservation_code_buy_count': '0',
                'reservation_code_reserve_quota': '1.00',
                'reservation_code_reserve_count': '1',
                'product_id_for_reservation_code': '899#SP9205',
                'reserve_code': '83809736',
                'fund_company': u'博时基金管理有限公司',
                'pledge_amount': '100',
                'pledge_repay_amount': '100',
                'amount_min': '0',
                'amount_max': '1000000',
                'amount_xjb_max': '100000000000',
                'pay_card_last_no': '1360',
                'pay_card_last_no_for_modification': '1136',
                'financing_amount': '1.00',
                'repay_loan_amount': '1.00',
                'cash_management_product': 'restful作为支付手段',
                'user_name_for_add_credit_card_without_binding_bank_card': '13400001239',
                'user_name_for_bank_card_resign': '13400001243',
                'user_name_for_modify_login_mode': '13400001242',
                'user_name_for_modify_mobile_without_sms': '13466466497',
                'user_name_for_recharge_use_new_card': '13984863493',
                'user_name_for_reevaluating': '13983532931',
                'bank_card_no_for_resign': '6210306555555855',
                'superposed_coupon_code': 'FULL_OFF_3_1_0053',
                'nonsuperposed_coupon_code': 'FULL_OFF_3_1_0055',
                'credit_card_repay_coupon_code': 'FULL_OFF_3_1_0070',
                'superposed_coupon_quantity': '2',
                'nonsuperposed_coupon_quantity': '1',
                'name': 'A******6',
                'risk_type': '激进型',
                'conservative_user': '13400001236',
                'financial_fund_product_name': 'UI理财型基金',
                'financial_fund_product_code': '53#530034',
                'mail': 'abc@163.com',
                'address': u'南京西路399号',
                'fund_product_for_hot_topic': '大成新锐产业混合',
                'high_end_quotation_product_code': 'H9#H90034',
                'unevaluated_user': '13400001240',
                'cautious_user': '13400001237',

            },
            'u2': {
                'user_name': '13079141536',
                'login_password': 'a0000000',
                'trade_password': '135790',
                'csi_index': '中证500',
                'fund_product_name': u'博时医疗保健行业混合A',
                'fund_product_code': '050026',
                'fund_product_code_2': 'A09201',
                'fund_product_name_2': u'雷克萨斯',
                'fund_company': u'博时基金管理有限公司',
                'dqb_product_3': u'UI自动化积分测试--定期',
                'dqb_product_code_3': 'SP9206',
                'high_end_product_for_points': u'UI自动化高端积分测试',
                'dqb_product_for_coupon': u'UI自动化优惠券测试--定期',
                'reservation_code_buy_quota': '0.00',
                'reservation_code_buy_count': '0',
                'reservation_code_reserve_quota': '1.00',
                'reservation_code_reserve_count': '1',
                'product_id_for_reservation_code': '899#SP9205',
                'reserve_code': '83809736',
            },
        }

        XJB_UAT_USER_1 = {
            'u1': {
                'user_name': '18019281762',
                'login_password': 'qq123456',
                'trade_password': '258036',
                'user_credit_card_id': '185',
                'high_end_product': u'自动化专用简称',
                'best_recommend_high_end_product': u'认购测试',
                'high_end_product_amount': '10000',
                'high_end_amount_for_superposed_coupon': '10000',
                'high_end_product_for_fast_redeem': u'现金管理8号',
                'high_end_product_for_income_calculator': u'现金管理3号',
                'high_end_product_for_points_offset': u'自动化专用简称',
                'dqb_product': u'金玉满堂1月期117号',
                # 'dqb_product': u'金玉满堂1月期366号',
                # 'dqb_product': u'嫦娥二号',
                'dqb_product_amount': '500',
                'dqb_product_amount_for_superposed_coupon': '500',
                'search_with_full_name': u'博时裕诚纯债债券型证券投资基金',
                'search_with_short_name': u'博时裕诚',
                'credit_card_no': '5309820097638155',
                'cash_management_product': '现金管理8号',
                'last_card_no_for_repay': '9049',
                # 'repay_credit_card_no': '5309801454069049',   # 18019281762
                'fund_product_name': u'广发聚丰混合',
                'non_money_fund_product_code': u'270005',
                'fund_product_name_2': u'华安科技',
                'fund_product_code': '004286',
                'fund_product_code_2': '040002',
                'fund_product_name_for_redeem': u'华夏现金增利货币A(003003)',
                'fund_product_name_for_fast_redeem': u'华夏复兴混合(000031)',
                'fund_product_name_for_fast_convert': u'泓鑫混合(003475)',
                'fund_product_amount': '20',
                'fund_product_amount_for_nonsuperposed_coupon': '200',
                'last_card_no': '8155',
                'user_for_redeem_dqb': '18019281769',
                'dqb_product_2': u'组合一号',
                'dqb_product_amount_2': '1',
                'credit_card_repay_amount': '10',
                'credit_card_reserved_pay_amount': '10',
                'csi_index': '中证500',
                'reservation_code_buy_quota': '0.00',
                'reservation_code_buy_count': '0',
                'reservation_code_reserve_quota': '500.00',
                'reservation_code_reserve_count': '1',
                'product_id_for_reservation_code': '899#CS0117',
                'reserve_code': '88052891',
                'fund_company': u'博时基金管理有限公司',
                'user_name_for_reservation_code': '15011243711',
                'login_password_for_reservation_code': 'a0000000',
                'trade_password_for_reservation_code': '147258',
                'pledge_amount': '100',
                'pledge_repay_amount': '100',
                'product_name_for_vipproduct_pledge': 'pc端收益测试简称',
                'pay_card_last_no': '3555',
                'pay_card_last_no_for_modification': '8026',
                'financing_amount': '1.00',
                'repay_loan_amount': '1.01',
                'superposed_coupon_code': 'FULL_OFF_10_1_0082',
                'non_superposed_coupon_code': 'FULL_OFF_10_1_0094',
                'superposed_coupon_quantity': '2',
                'non_superposed_coupon_quantity': '1',
                'fund_product_name_for_newly_raised_fund': '泰康股票',
                'high_end_quotation_product_code': 'H9#H9011F',
                'high_end_quotation_product_name': '财富报价式2天期',
                'user_name_for_modify_mobile_without_sms': '13623835401',
            },

            'u2': {
                'user_name': '13994963565',
                'login_password': 'a1111111',
                'trade_password': '147258',
            },

            # 未绑卡未实名的用户
            'u3': {
                'user_name': '18678533361',
                'login_password': 'a0000000',
                'trade_password': '135790',
            }

        }

        XJB_UAT_USER_2 = {
            'u1': {
                'user_name': '15000203054',
                'user_name_for_dqb_redeem': '18019281764',
                'login_password_for_dqb_redeem': 'qq789123',
                # 'user_name': '18682133427',
                'login_password': 'a0000000',
                # 'login_password': 'a0000000',
                'trade_password': '121212',
                # 'trade_password': '135790',
                'high_end_product': u'现金管理1号',
                # 'high_end_product': u'自动化专用简称',
                'high_end_product_amount': '10000',
                'high_end_product_amount_for_redeem': '10',
                'high_end_amount_for_superposed_coupon': '10000',
                'high_end_product_for_fast_redeem': u'现金管理8号',
                'high_end_product_for_points_offset': u'现金管理1号',
                'dqb_product': u'金玉满堂1月期366号',
                # 'dqb_product': u'嫦娥二号',
                'dqb_product_amount': '10000',
                'dqb_product_amount_for_superposed_coupon': '5000',
                'search_with_full_name': u'千岛湖一号',
                'search_with_short_name': u'千',
                'credit_card_no': '5309820097638156',
                # 'repay_credit_card_no': '5309801454069049',   # 18019281762
                'fund_product_name': u'广发聚丰混合',
                'fund_product_name_2': u'华安科技',
                'fund_product_code': '270005',
                'fund_product_code_2': '040002',
                # 'fund_product_name_for_redeem': u'华夏复兴(000031)',
                'fund_product_name_for_redeem': u'新华股票(430001)',
                # 'fund_product_name_for_redeem': u'华夏现金(003003)',
                'fund_product_name_for_fast_redeem': u'新华股票(430001)',
                # 'fund_product_name_for_fast_redeem': u'华夏复兴(000031)',
                'fund_product_amount': '20',
                'fund_product_amount_for_nonsuperposed_coupon': '2000',
                'last_card_no': '8157',
                'dqb_product_2': u'长期交易测试产品专用简称',
                'dqb_product_amount_2': '1',
                'credit_card_repay_amount': '10',
                'credit_card_reserved_pay_amount': '10',
                'csi_index': '中证500',
                'reservation_code_buy_quota': '0.00',
                'reservation_code_buy_count': '0',
                'reservation_code_reserve_quota': '50000.00',
                'reservation_code_reserve_count': '1',
                'product_id_for_reservation_code': '899#S40066',
                'reserve_code': '85903661',
                'fund_company': u'博时基金管理有限公司',
                'user_name_for_reservation_code': '15011243711',
                'login_password_for_reservation_code': 'a0000000',
                'trade_password_for_reservation_code': '147258',
                'pledge_amount': '100',
                'pledge_repay_amount': '100',
                'product_name_for_vipproduct_pledge': '现金管理1号',
                'user_name_for_associator_level_1': '13836124723',
                'user_name_for_associator_level_2': '15802145314',
                'user_name_for_associator_level_3': '18734625874',
                'user_name_for_associator_level_4': '13043180965',
                'amount_min': '0',
                'amount_max': '5000100',
                'amount_xjb_max': '100000000000',
                'recharge_amount': '1000'
            },

            'u2': {
                'user_name': '15666666669',
                'login_password': 'a0000000',
                'trade_password': '135790',
                'reservation_code_buy_quota': '0.00',
                'reservation_code_buy_count': '0',
                'reservation_code_reserve_quota': '50000.00',
                'reservation_code_reserve_count': '1',
                'product_id_for_reservation_code': '899#S40066',
                'reserve_code': '85903661',
            }

        }
