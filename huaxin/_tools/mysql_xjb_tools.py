# coding: utf-8
import calendar
import decimal
import random
import time
import re
import datetime

from _common.data_base import DataBase
from _common.global_config import GlobalConfig
from _common.global_controller import GlobalController
from _common.utility import Utility
from dateutil.relativedelta import relativedelta
import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')
DBC = GlobalController.DB_CONNECT
DBC_TAG = 'uat' if DBC['host'] == '10.199.105.111' else 'ci'


class MysqlXjbTools(object):
    def __init__(self):
        self._db = DataBase.MySql(DBC)
        self._sql_query_result = None
        self._sql_query_time_span = GlobalConfig.DbQueryTimeControl.DbQuery_TimeSpan
        self._sql_query_try_time = GlobalConfig.DbQueryTimeControl.DbQuery_TryTime

        time.sleep(self._sql_query_time_span)

    def get_cust_info(self, columns, match, mobile):
        try:
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "select %s from %s.cif_cust_base where mobile %s '%s'"
            results = self._db.sql_run(sql_query, columns, db_name, match, mobile)
            return results
        except:
            pass

    # 获取trade account info
    def get_trade_acco_info(self, cust_no):
        try:
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "select * from %s.cif_trade_account_info where cust_no = '%s'"
            results = self._db.sql_run(sql_query, db_name, cust_no)
            return results
        except:
            pass

    def get_sms_verify_code(self, mobile, template_id):
        try:
            try_time = self._sql_query_try_time

            db_name = 'supergw_uat' if DBC_TAG == 'uat' else 'spw'
            sql_query = "select * from %s.sgw_sms where sgw_sms_mobile = '%s' and template_id = '%s' order by id desc limit 1"
            results = self._db.sql_run(sql_query, db_name, mobile, template_id)

            while try_time > 0:

                for result in results:
                    if result['template_id'] == 'cif_register' or result['template_id'] == 'cif_login':
                        self._sql_query_result = re.findall(r'\d+', result['sgw_sms_content'])[
                            0]  # 把字符串里所有的数字拿出来,然后取第几个
                        if not self._sql_query_result is None:
                            return self._sql_query_result

                    if result['template_id'] == 'cif_bindBankCard':
                        self._sql_query_result = re.findall(r'\d+', result['sgw_sms_content'])[1]
                        if not self._sql_query_result is None:
                            return self._sql_query_result

                    if result['template_id'] == 'credit_bind_card':
                        self._sql_query_result = re.findall(r'\d+', result['sgw_sms_content'])[1]
                        if not self._sql_query_result is None:
                            return self._sql_query_result

                    if result['template_id'] == 'cif_changeMobile':
                        self._sql_query_result = re.findall(r'\d+', result['sgw_sms_content'])[0]
                        if not self._sql_query_result is None:
                            return self._sql_query_result

                    if result['template_id'] == 'as_risk_level' or result['template_id'] == 'as_risk_not_match':
                        self._sql_query_result = re.findall(r'\d+', result['sgw_sms_content'])[0]
                        if not self._sql_query_result is None:
                            return self._sql_query_result

                    if result['template_id'] == 'credit_apply_brand_citicb' or result[
                        'template_id'] == 'credit_activate_citicb':
                        self._sql_query_result = re.findall(r'\d+', result['sgw_sms_content'])[0]
                        if not self._sql_query_result is None:
                            return self._sql_query_result

                    if result['template_id'] == 'as_risk_match':
                        self._sql_query_result = re.findall(r'\d+', result['sgw_sms_content'])[0]
                        if not self._sql_query_result is None:
                            return self._sql_query_result

                time.sleep(self._sql_query_time_span)

                try_time -= 1

        except:
            pass

        if self._sql_query_result is None:
            # raise Exception('get_sms_verify_code: no result find within timeout !!!')
            print 'get_sms_verify_code: no result find within timeout !!!'
            return '123456'

    # 当天用户剩余快取次数
    def user_num_of_fast_withdraw(self, mobile):

        try:
            created_at = time.strftime("%Y-%m-%d", time.localtime()) + '%'

            # 用户已成功的快取次数
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query, db_name, mobile)[0]['cust_no']

            db_name = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            sql_query = "SELECT * FROM %s.CTS_TRADE_ORDER where ORDER_APKIND ='003' and cust_no = '%s' and created_at like '%s' and status = 'Y'"
            results = self._db.sql_run(sql_query, db_name, cust_no, created_at)

            user_fast_withdraw_counts = results.__len__()

            # 配置的所有用户的单日快取次数
            db_name = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            sql_query = "SELECT PM_V1 FROM %s.CTS_PARAMETER where PM_NAME = '单日可快取次数' and PM_KEY = 'FASTWITHDRAWLIMIT'"
            fast_withdraw_counts = int(self._db.sql_run(sql_query, db_name)[0]['PM_V1'])

            # 用户还剩余的单日快取次数
            user_fast_withdraw = fast_withdraw_counts - user_fast_withdraw_counts

            return user_fast_withdraw
        except:

            pass

    # 返回单日快取次数不为0的用户
    def user_fast_withdraw_true(self):

        try:
            created_at = time.strftime("%Y-%m-%d", time.localtime()) + '%'

            # 配置的所有用户的单日快取次数
            db_name = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            sql_query = "SELECT PM_V1 FROM %s.CTS_PARAMETER where PM_NAME = '单日可快取次数' and PM_KEY = 'FASTWITHDRAWLIMIT'"
            fast_withdraw_counts = int(self._db.sql_run(sql_query, db_name)[0]['PM_V1'])

            # 返回单日快取次数 < 配置的所有用户的单日快取次数 的用户
            db_name = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            sql_query = "SELECT count(cust_no), cust_no FROM %s.CTS_TRADE_ORDER where ORDER_APKIND ='003' and created_at like '%s' and status = 'Y' group by cust_no"
            results = self._db.sql_run(sql_query, db_name, created_at)

            for i in results:
                if i['count(cust_no)'] < fast_withdraw_counts:
                    cust_no = i['cust_no']

            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT mobile FROM %s.cif_cust_base where cust_no = '%s'"
            mobile = self._db.sql_run(sql_query, db_name, cust_no)[0]['mobile']

            return mobile
        except:

            pass

    def redeem_vipproduct_info(self, cust_no, product_type):

        try:
            db_name = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            sql_query = "select AP_AMT from  %s.CTS_TRADE_ORDER where cust_no = '%s' and FROM_PROD_TYPE = '%s' order by id desc"
            balance = self._db.sql_run(sql_query, db_name, cust_no, product_type)[0]['AP_AMT']

            return balance
        except:

            pass

    # 首页收益信息
    def trade_asset_total_home_page(self, mobile):

        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            pdc_db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'

            sql_query = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query, db_name, mobile)[0]['cust_no']

            # step2-根据cust_no去查首页收益信息
            db_name = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            num = int(cust_no) % 8
            table_name = 'CTS_VACCO_PAYMENT_DETAIL' + '_' + str(num)
            sql1 = "SELECT ifnull(sum(SUB_AMT), 0) as BALANCE from %s." + table_name + " WHERE CUST_NO = '%s';"

            # 现金宝总资产计算
            xjb_balance = self._db.sql_run(sql1, db_name, cust_no)
            vacco_asset = xjb_balance[0]['BALANCE']

            # 定期宝总资产计算
            # 查找在途入资金
            sql3 = "select IFNULL(sum(t.BALANCE),0) BALANCE from %s.CTS_ASSET_IN_TRANSIT t " \
                   "where 1=1 and t.CUST_NO = '%s' and t.PROD_TYPE = '1' and t.BALANCE >= 0;"
            sql3_1 = "select IFNULL(sum(t.BALANCE),0) BALANCE from %s.CTS_ASSET_IN_TRANSIT t " \
                     "where 1=1 and t.CUST_NO = '%s' and t.PROD_TYPE = '1' and t.BALANCE < 0;"
            asset_in_transit = self._db.sql_run(sql3, db_name, cust_no)
            # 赎回的金额为负数
            redeem_asset_in_transit = self._db.sql_run(sql3_1, db_name, cust_no)
            # 查找静态份额
            sql4 = "SELECT ifnull(sum(BALANCE-ABNM_FROZEN), 0) BALANCE from %s.CTS_PROD_QUTY WHERE CUST_NO='%s' and PROD_TYPE = '1';"
            capitalInTransit = self._db.sql_run(sql4, db_name, cust_no)
            # 赎回的金额为负数
            dqb_asset = asset_in_transit[0]['BALANCE'] + capitalInTransit[0]['BALANCE'] + redeem_asset_in_transit[0][
                'BALANCE']

            # 高端总资产计算
            # 查找在途入资金
            sql5 = "select IFNULL(sum(t.BALANCE),0) BALANCE from %s.CTS_ASSET_IN_TRANSIT t " \
                   "where 1=1 and t.CUST_NO = '%s' and t.PROD_TYPE = '3' and t.BALANCE >= 0;"
            vip_asset_in_transit = self._db.sql_run(sql5, db_name, cust_no)
            # 查找静态份额
            sql6 = "SELECT ifnull(sum(BALANCE-ABNM_FROZEN), 0) BALANCE from %s.CTS_PROD_QUTY WHERE CUST_NO='%s' and PROD_TYPE = '3';"
            vip_capitalInTransit = self._db.sql_run(sql6, db_name, cust_no)
            vip_asset = vip_asset_in_transit[0]['BALANCE'] + vip_capitalInTransit[0]['BALANCE']

            # 基金总资产计算
            # 查找在途资产表
            sql7 = "select IFNULL(sum(t.BALANCE),0) BALANCE from %s.CTS_ASSET_IN_TRANSIT t " \
                   "where 1=1 and t.CUST_NO = '%s' and t.PROD_TYPE = '2' and t.BALANCE >= 0;"
            fund_asset_in_transit = self._db.sql_run(sql7, db_name, cust_no)

            # 查找基金份额和净值
            sql8 = "SELECT PROD_ID, ifnull(BALANCE-ABNM_FROZEN, 0) as BALANCE from %s.CTS_PROD_QUTY WHERE CUST_NO='%s' and PROD_TYPE = '2';"
            fund_asset = 0
            fund_quty = self._db.sql_run(sql8, db_name, cust_no)
            for i in range(0, len(fund_quty)):
                balance = fund_quty[i]['BALANCE']
                product_id = fund_quty[i]['PROD_ID']
                sql9 = "SELECT IFNULL(nav, 1) as nav FROM %s.pdc_nav WHERE fundid = '%s' order by nav_date desc limit 1;"
                nav = self._db.sql_run(sql9, pdc_db_name, str(product_id).split('#')[1])
                asset = balance * nav[0]['nav']
                fund_asset = fund_asset + asset

            fund_asset = fund_asset_in_transit[0]['BALANCE'] + fund_asset

            return vacco_asset, dqb_asset, vip_asset, fund_asset
        except:
            pass

    def fund_sizer_info_verify(self, rise_min, rise_max, rate_org_id, rate_star, rise_section, company_id, fund_type):

        try:
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'

            ta_no = None
            # the query to get the total count from db
            fund_rate_query = None
            data_from_db_query = None
            # get the total count for fund sizer
            result_count = None
            data_from_db = None

            if str(company_id) is not '':
                query_ta_no = "SELECT ta_no from %s.pdc_product_ta where ta_no_hsjy = '%s'";
                ta_no = self._db.sql_run(query_ta_no, db_name, company_id)[0]["ta_no"]
                if str(fund_type) is not '':
                    if rise_section == 0:
                        fund_rate_query = "SELECT count(1) as count from (SELECT DISTINCT a.productid from %s.pdc_productinfo a, %s.pdc_fund_rate b WHERE a.ta_no = '%s' and a.weekly_return >= '%s' and b.rate_star = '%s' and a.fund_type = '%s' and a.weekly_return <= '%s' and b.rate_agency_code = '%s' and a.productid = b.productid) tmp"
                        data_from_db_query = "SELECT DISTINCT a.productid, a.weekly_return, a.fund_type, a.latest_nav from %s.pdc_productinfo a, %s.pdc_fund_rate b WHERE a.ta_no = '%s' and a.weekly_return >= %s and b.rate_star = %s and a.fund_type = '%s' and a.weekly_return <= '%s' and b.rate_agency_code = '%s' and a.productid = b.productid"
                    elif rise_section == 1:
                        fund_rate_query = "SELECT count(1) as count from (SELECT DISTINCT a.productid from %s.pdc_productinfo a, %s.pdc_fund_rate b WHERE a.ta_no = '%s' and a.monthly_return >= '%s' and b.rate_star = '%s' and a.fund_type = '%s' and a.monthly_return <= '%s' and b.rate_agency_code = '%s' and a.productid = b.productid) tmp"
                        data_from_db_query = "SELECT DISTINCT a.productid, a.monthly_return, a.fund_type, a.latest_nav from %s.pdc_productinfo a, %s.pdc_fund_rate b WHERE a.ta_no = '%s' and a.monthly_return >= %s and b.rate_star = %s and a.fund_type = '%s' and a.monthly_return <= '%s' and b.rate_agency_code = '%s' and a.productid = b.productid"
                    elif rise_section == 2:
                        fund_rate_query = "SELECT count(1) as count from (SELECT DISTINCT a.productid from %s.pdc_productinfo a, %s.pdc_fund_rate b WHERE a.ta_no = '%s' and a.quarter_return >= '%s' and b.rate_star = '%s' and a.fund_type = '%s' and a.quarter_return <= '%s' and b.rate_agency_code = '%s' and a.productid = b.productid) tmp"
                        data_from_db_query = "SELECT DISTINCT a.productid, a.quarter_return, a.fund_type, a.latest_nav from %s.pdc_productinfo a, %s.pdc_fund_rate b WHERE a.ta_no = '%s' and a.quarter_return >= %s and b.rate_star = %s and a.fund_type = '%s' and a.quarter_return <= '%s' and b.rate_agency_code = '%s' and a.productid = b.productid"
                    elif rise_section == 3:
                        fund_rate_query = "SELECT count(1) as count from (SELECT DISTINCT a.productid from %s.pdc_productinfo a, %s.pdc_fund_rate b WHERE a.ta_no = '%s' and a.halfyear_return >= '%s' and b.rate_star = '%s' and a.fund_type = '%s' and a.halfyear_return <= '%s' and b.rate_agency_code = '%s' and a.productid = b.productid) tmp"
                        data_from_db_query = "SELECT DISTINCT a.productid, a.halfyear_return, a.fund_type, a.latest_nav from %s.pdc_productinfo a, %s.pdc_fund_rate b WHERE a.ta_no = '%s' and a.halfyear_return >= %s and b.rate_star = %s and a.fund_type = '%s' and a.halfyear_return <= '%s' and b.rate_agency_code = '%s' and a.productid = b.productid"
                    elif rise_section == 4:
                        fund_rate_query = "SELECT count(1) as count from (SELECT DISTINCT a.productid from %s.pdc_productinfo a, %s.pdc_fund_rate b WHERE a.ta_no = '%s' and a.year_return >= '%s' and b.rate_star = '%s' and a.fund_type = '%s' and a.year_return <= '%s' and b.rate_agency_code = '%s' and a.productid = b.productid) tmp"
                        data_from_db_query = "SELECT DISTINCT a.productid, a.year_return, a.fund_type, a.latest_nav from %s.pdc_productinfo a, %s.pdc_fund_rate b WHERE a.ta_no = '%s' and a.year_return >= %s and b.rate_star = %s and a.fund_type = '%s' and a.year_return <= '%s' and b.rate_agency_code = '%s' and a.productid = b.productid"
                    elif rise_section == 5:
                        fund_rate_query = "SELECT count(1) as count from (SELECT DISTINCT a.productid from %s.pdc_productinfo a, %s.pdc_fund_rate b WHERE a.ta_no = '%s' and a.threeyear_return >= '%s' and b.rate_star = '%s' and a.fund_type = '%s' and a.threeyear_return <= '%s' and b.rate_agency_code = '%s' and a.productid = b.productid) tmp"
                        data_from_db_query = "SELECT DISTINCT a.productid, a.threeyear_return, a.fund_type, a.latest_nav from %s.pdc_productinfo a, %s.pdc_fund_rate b WHERE a.ta_no = '%s' and a.threeyear_return >= %s and b.rate_star = %s and a.fund_type = '%s' and a.threeyear_return <= '%s' and b.rate_agency_code = '%s' and a.productid = b.productid"

                    result_count = self._db.sql_run(fund_rate_query, db_name, db_name, ta_no, rise_min, rate_star,
                                                    fund_type, rise_max,
                                                    rate_org_id)

                    if (len(result_count) != 0):
                        total_count = result_count[0]['count']
                    else:
                        total_count = 0
                    data_from_db = self._db.sql_run(data_from_db_query, db_name, db_name, ta_no, rise_min, rate_star,
                                                    fund_type, rise_max, rate_org_id)
                    print "--- result count is ----", total_count
                    print "-----", data_from_db_query

                else:
                    if rise_section == 0:
                        fund_rate_query = "SELECT count(1) as count from (SELECT DISTINCT a.productid from %s.pdc_productinfo a, %s.pdc_fund_rate b WHERE a.ta_no = '%s' and a.weekly_return >= '%s' and b.rate_star = '%s' and a.weekly_return <= '%s' and b.rate_agency_code = '%s' and a.productid = b.productid) tmp"
                        data_from_db_query = "SELECT DISTINCT a.productid, a.weekly_return, a.fund_type, a.latest_nav from %s.pdc_productinfo a, %s.pdc_fund_rate b WHERE a.ta_no = '%s' and a.weekly_return >= %s and b.rate_star = %s and a.weekly_return <= '%s' and b.rate_agency_code = '%s' and a.productid = b.productid"
                    elif rise_section == 1:
                        fund_rate_query = "SELECT count(1) as count from (SELECT DISTINCT a.productid from %s.pdc_productinfo a, %s.pdc_fund_rate b WHERE a.ta_no = '%s' and a.monthly_return >= '%s' and b.rate_star = '%s' and a.monthly_return <= '%s' and b.rate_agency_code = '%s' and a.productid = b.productid) tmp"
                        data_from_db_query = "SELECT DISTINCT a.productid, a.monthly_return, a.fund_type, a.latest_nav from %s.pdc_productinfo a, %s.pdc_fund_rate b WHERE a.ta_no = '%s' and a.monthly_return >= %s and b.rate_star = %s and a.monthly_return <= '%s' and b.rate_agency_code = '%s' and a.productid = b.productid"
                    elif rise_section == 2:
                        fund_rate_query = "SELECT count(1) as count from (SELECT DISTINCT a.productid from %s.pdc_productinfo a, %s.pdc_fund_rate b WHERE a.ta_no = '%s' and a.quarter_return >= '%s' and b.rate_star = '%s' and a.quarter_return <= '%s' and b.rate_agency_code = '%s' and a.productid = b.productid) tmp"
                        data_from_db_query = "SELECT DISTINCT a.productid, a.quarter_return, a.fund_type, a.latest_nav from %s.pdc_productinfo a, %s.pdc_fund_rate b WHERE a.ta_no = '%s' and a.quarter_return >= %s and b.rate_star = %s and a.quarter_return <= '%s' and b.rate_agency_code = '%s' and a.productid = b.productid"
                    elif rise_section == 3:
                        fund_rate_query = "SELECT count(1) as count from (SELECT DISTINCT a.productid from %s.pdc_productinfo a, %s.pdc_fund_rate b WHERE a.ta_no = '%s' and a.halfyear_return >= '%s' and b.rate_star = '%s' and a.halfyear_return <= '%s' and b.rate_agency_code = '%s' and a.productid = b.productid) tmp"
                        data_from_db_query = "SELECT DISTINCT a.productid, a.halfyear_return, a.fund_type, a.latest_nav from %s.pdc_productinfo a, %s.pdc_fund_rate b WHERE a.ta_no = '%s' and a.halfyear_return >= %s and b.rate_star = %s and a.halfyear_return <= '%s' and b.rate_agency_code = '%s' and a.productid = b.productid"
                    elif rise_section == 4:
                        fund_rate_query = "SELECT count(1) as count from (SELECT DISTINCT a.productid from %s.pdc_productinfo a, %s.pdc_fund_rate b WHERE a.ta_no = '%s' and a.year_return >= '%s' and b.rate_star = '%s' and a.year_return <= '%s' and b.rate_agency_code = '%s' and a.productid = b.productid) tmp"
                        data_from_db_query = "SELECT DISTINCT a.productid, a.year_return, a.fund_type, a.latest_nav from %s.pdc_productinfo a, %s.pdc_fund_rate b WHERE a.ta_no = '%s' and a.year_return >= %s and b.rate_star = %s and a.year_return <= '%s' and b.rate_agency_code = '%s' and a.productid = b.productid"
                    elif rise_section == 5:
                        fund_rate_query = "SELECT count(1) as count from (SELECT DISTINCT a.productid from %s.pdc_productinfo a, %s.pdc_fund_rate b WHERE a.ta_no = '%s' and a.threeyear_return >= '%s' and b.rate_star = '%s' and a.threeyear_return <= '%s' and b.rate_agency_code = '%s' and a.productid = b.productid) tmp"
                        data_from_db_query = "SELECT DISTINCT a.productid, a.threeyear_return, a.fund_type, a.latest_nav from %s.pdc_productinfo a, %s.pdc_fund_rate b WHERE a.ta_no = '%s' and a.threeyear_return >= %s and b.rate_star = %s and a.threeyear_return <= '%s' and b.rate_agency_code = '%s' and a.productid = b.productid"

                    result_count = self._db.sql_run(fund_rate_query, db_name, db_name, ta_no, rise_min, rate_star,
                                                    rise_max,
                                                    rate_org_id)
                    if (len(result_count) != 0):
                        total_count = result_count[0]['count']
                    else:
                        total_count = 0
                    data_from_db = self._db.sql_run(data_from_db_query, db_name, db_name, ta_no, rise_min, rate_star,
                                                    rise_max, rate_org_id)

                    print "--- result count is ----", total_count
                    print "-----", data_from_db_query
            else:
                if int(rise_section) == 0:
                    fund_rate_query = "SELECT count(1) as count from (SELECT DISTINCT a.productid from %s.pdc_productinfo a, %s.pdc_fund_rate b WHERE a.weekly_return >= '%s' and b.rate_star = '%s' and a.weekly_return <= '%s' and b.rate_agency_code = '%s' and a.productid = b.productid) tmp"
                    data_from_db_query = "SELECT DISTINCT a.productid, a.weekly_return, a.fund_type, a.latest_nav from %s.pdc_productinfo a, %s.pdc_fund_rate b WHERE a.weekly_return >= %s and b.rate_star = %s and a.weekly_return <= '%s' and b.rate_agency_code = '%s' and a.productid = b.productid"
                elif int(rise_section) == 1:
                    fund_rate_query = "SELECT count(1) as count from (SELECT DISTINCT a.productid from %s.pdc_productinfo a, %s.pdc_fund_rate b WHERE a.monthly_return >= '%s' and b.rate_star = '%s' and a.monthly_return <= '%s' and b.rate_agency_code = '%s' and a.productid = b.productid) tmp"
                    data_from_db_query = "SELECT DISTINCT a.productid, a.weekly_return, a.fund_type, a.latest_nav from %s.pdc_productinfo a, %s.pdc_fund_rate b WHERE a.monthly_return >= %s and b.rate_star = %s and a.monthly_return <= '%s' and b.rate_agency_code = '%s' and a.productid = b.productid"
                elif int(rise_section) == 2:
                    fund_rate_query = "SELECT count(1) as count as count from (SELECT DISTINCT a.productid from %s.pdc_productinfo a, %s.pdc_fund_rate b WHERE a.quarter_return >= '%s' and b.rate_star = '%s' and a.quarter_return <= '%s' and b.rate_agency_code = '%s' and a.productid = b.productid) tmp"
                    data_from_db_query = "SELECT DISTINCT a.productid, a.monthly_return, a.fund_type, a.latest_nav from %s.pdc_productinfo a, %s.pdc_fund_rate b WHERE a.quarter_return >= %s and b.rate_star = %s and a.quarter_return <= '%s' and b.rate_agency_code = '%s' and a.productid = b.productid"
                elif int(rise_section) == 3:
                    fund_rate_query = "SELECT count(1) as count from (SELECT DISTINCT a.productid from %s.pdc_productinfo a, %s.pdc_fund_rate b WHERE a.halfyear_return >= '%s' and b.rate_star = '%s' and a.halfyear_return <= '%s' and b.rate_agency_code = '%s' and a.productid = b.productid) tmp"
                    data_from_db_query = "SELECT DISTINCT a.productid, a.halfyear_return, a.fund_type, a.latest_nav from %s.pdc_productinfo a, %s.pdc_fund_rate b WHERE a.halfyear_return >= %s and b.rate_star = %s and a.halfyear_return <= '%s' and b.rate_agency_code = '%s' and a.productid = b.productid"
                elif int(rise_section) == 4:
                    fund_rate_query = "SELECT count(*) as count from (select a.productid from %s.pdc_productinfo a left join %s.pdc_fund_rate b on a.productid=b.productid join (select p.fundid, p.fund_income_unit, p.fund_income_unit_flag from %s.pdc_nav p join (select fundid ,max(nav_date)m from %s.pdc_nav GROUP BY fundid) t on p.fundid=t.fundid and p.nav_date=t.m) d on a.product_no=d.fundid JOIN (SELECT g.productid, g.onsale_status FROM %s.pdc_product_marketing g WHERE g.onsale_flag = 1 and g.accept_mode = 'M' and g.is_sale = '1') m ON a.productid = m.productid LEFT JOIN %s.pdc_issued_info q ON a.productid = q.productid LEFT JOIN %s.pdc_product_detail k ON a.productid = k.productid where a.year_return >= %s and b.rate_star = %s and  a.year_return <= %s and b.rate_agency_code='%s' and a.product_type=2) temp"
                    # "SELECT count(1) as count from (SELECT DISTINCT a.productid from %s.pdc_productinfo a, %s.pdc_fund_rate b WHERE a.year_return >= '%s' and b.rate_star = '%s' and a.year_return <= '%s' and b.rate_agency_code = '%s' and a.productid = b.productid) tmp"
                    data_from_db_query = "select DISTINCT a.productid, a.year_return, a.fund_type, a.latest_nav from %s.pdc_productinfo a left join %s.pdc_fund_rate b on a.productid=b.productid join (select p.fundid, p.fund_income_unit, p.fund_income_unit_flag from %s.pdc_nav p join (select fundid ,max(nav_date)m from %s.pdc_nav GROUP BY fundid) t on p.fundid=t.fundid and p.nav_date=t.m) d on a.product_no=d.fundid JOIN (SELECT g.productid, g.onsale_status FROM %s.pdc_product_marketing g WHERE g.onsale_flag = 1 and g.accept_mode = 'M' and g.is_sale = '1') m ON a.productid = m.productid LEFT JOIN %s.pdc_issued_info q ON a.productid = q.productid LEFT JOIN %s.pdc_product_detail k ON a.productid = k.productid where a.year_return >= %s and b.rate_star = %s and  a.year_return <= %s and b.rate_agency_code='%s' and a.product_type=2;"
                elif int(rise_section) == 5:
                    fund_rate_query = "SELECT count(1) as count from (SELECT DISTINCT a.productid from %s.pdc_productinfo a, %s.pdc_fund_rate b WHERE a.threeyear_return >= '%s' and b.rate_star = '%s' and a.threeyear_return <= '%s' and b.rate_agency_code = '%s' and a.productid = b.productid) tmp"
                    data_from_db_query = "SELECT DISTINCT a.productid, a.threeyear_return, a.fund_type, a.latest_nav from %s.pdc_productinfo a, %s.pdc_fund_rate b WHERE a.threeyear_return >= %s and b.rate_star = %s and a.threeyear_return <= '%s' and b.rate_agency_code = '%s' and a.productid = b.productid"

                print "-----", db_name
                result_count = self._db.sql_run(fund_rate_query, db_name, db_name, db_name, db_name, db_name, db_name,
                                                db_name, rise_min, rate_star, rise_max,
                                                rate_org_id)
                if (len(result_count) != 0):
                    total_count = result_count[0]['count']
                else:
                    total_count = 0

                print "--- result count is ----", total_count
                print "-----", data_from_db_query
                data_from_db = self._db.sql_run(data_from_db_query, db_name, db_name, db_name, db_name, db_name,
                                                db_name,
                                                db_name, rise_min, rate_star,
                                                rise_max, rate_org_id)

            return total_count, data_from_db

        except:

            pass

    # 我的积分
    def my_points(self, mobile):

        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query, db_name, mobile)[0]['cust_no']

            # step2-根据cust_no去查我的资产界面的我的积分
            db_name = 'points_uat' if DBC_TAG == 'uat' else 'points'
            sql_query = "select amount-frozen_amount surplus_amount from %s.POINTS_ACCOUNT where CUST_NO='%s'"
            surplus_amount = self._db.sql_run(sql_query, db_name, cust_no)[0]['surplus_amount']

            return surplus_amount
        except:

            pass

    # 使用积分定投基金积分定时扣款额度验证
    def fund_used_points_investment(self, mobile, purchase_payment_type, apkind):

        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query, db_name, mobile)[0]['cust_no']

            # step2-根据cust_no去查我的资产界面的我的积分
            db_name = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            sql_query = "select points_quantity from %s.CTS_TRADE_REQUEST where cust_no='%s' and purchase_payment_type = '%s' and APKIND = '%s' order by id desc limit 1"
            points_quantity = self._db.sql_run(sql_query, db_name, cust_no, purchase_payment_type, apkind)[0][
                'points_quantity']

            return points_quantity
        except:

            pass

    # 当绑信用卡时，会报信息检验不符，需要去表里改值。valid_result = Y才可以绑定成功
    def change_bankcard_valid_result(self, card_no):
        try:
            db_name = 'supergw_uat' if DBC_TAG == 'uat' else 'spw'
            sql_query = "update %s.supergw_bankcard_valid_log set valid_result = 'Y' where bank_acco = '%s';COMMIT;"

            self._db.sql_run(sql_query, db_name, card_no)
        except:
            pass

    def get_register_mobile(self):

        try:
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "select mobile from %s.cif_cust_base where mobile is not NULL order by id desc"
            results = self._db.sql_run(sql_query, db_name)

            return random.choice(results)['mobile']
        except:

            pass

    def get_new_fund_list(self):

        try:
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            sql_query = "SELECT DISTINCT a.productid FROM %s.pdc_productinfo a JOIN %s.pdc_product_marketing b on a.productid = b.productid where a.product_type = 2 and b.accept_mode = 'M' and b.onsale_flag = 1 and b.is_new_issue = 1 and b.is_sale = 1;"

            fund_ids = self._db.sql_run(sql_query, db_name, db_name)

            return fund_ids
        except:

            pass

    # 获取用户信用卡
    def get_cust_credit_card(self, mobile, sort):
        try:
            db_name = 'lifeapp_uat' if DBC_TAG == 'uat' else 'la'
            sql_query = "SELECT * from %s.la_credit_user_card where mobile = '%s' order by id %s"
            credit_cards = self._db.sql_run(sql_query, db_name, mobile, sort)
            return credit_cards
        except:

            pass

    # 删除用户下的信用卡
    def del_cust_credit_card(self, mobile):
        try:
            db_name = 'lifeapp_uat' if DBC_TAG == 'uat' else 'la'
            sql_query = "DELETE FROM %s.la_credit_user_card where mobile='%s';"
            del_credit_cards = self._db.sql_run(sql_query, db_name, mobile)
            return del_credit_cards
        except:
            pass

    def get_cust_credit_card_by_card_no(self, card_no):
        try:
            db_name = 'lifeapp_uat' if DBC_TAG == 'uat' else 'la'
            sql_query = "SELECT * from %s.la_credit_user_card where card_no = '%s'"
            credit_cards = self._db.sql_run(sql_query, db_name, card_no)

            return credit_cards
        except:

            pass

    # 修改信用卡还款提醒状态
    def modify_credit_card_reminder_status(self, status, card_no):
        try:
            db_name = 'lifeapp_uat' if DBC_TAG == 'uat' else 'la'
            sql_query = "update %s.la_credit_user_card set is_warn='%s' where card_no = '%s';"
            self._db.sql_run(sql_query, db_name, status, card_no)

            return
        except:

            pass

    # 信用卡状态更新 (删除->正常,正常->删除)
    def update_deleted_cust_credit_card_to_normal(self, card_id, state=None):

        try:
            db_name = 'lifeapp_uat' if DBC_TAG == 'uat' else 'la'
            if state is None:
                sql_query = "update %s.la_credit_user_card set state = 'N' where id = %s;COMMIT;"
                credit_cards = self._db.sql_run(sql_query, db_name, card_id)
            else:
                sql_query = "update %s.la_credit_user_card set state = '%s' where id = %s;COMMIT;"
                credit_cards = self._db.sql_run(sql_query, db_name, state, card_id)

            return credit_cards
        except:
            pass

    # 获取基金组合百分比
    def get_fund_percent(self, mobile, object_id):

        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query, db_name, mobile)[0]['cust_no']
            # step2-查基金百分比
            db_name = 'as_uat' if DBC_TAG == 'uat' else 'as'
            sql_query = "SELECT object_id, fund_set_percent FROM %s.as_cust_favorite where cust_no = '%s' and object_id = '%s' ORDER BY id DESC"
            fund_set_percents = self._db.sql_run(sql_query, db_name, cust_no, object_id)

            return fund_set_percents

        except:

            pass

    # 还款记录
    def get_creditcard_repay_requests(self, mobile):
        try:
            db_name = 'lifeapp_uat' if DBC_TAG == 'uat' else 'la'
            sql_query = "select * from %s.la_credit_repay_request where mobile = '%s' and tran_st='Y' order by id desc"
            time.sleep(self._sql_query_time_span)
            reqs = self._db.sql_run(sql_query, db_name, mobile)
            return reqs
        except:

            pass

    # 预约还款
    def get_creditcard_repay_order(self, card_id):
        try:
            db_name = 'lifeapp_uat' if DBC_TAG == 'uat' else 'la'
            sql_query = "select * from %s.la_credit_repay_order where user_card_id = '%s' order by id desc limit 1"
            time.sleep(self._sql_query_time_span)
            reqs = self._db.sql_run(sql_query, db_name, card_id)
            return reqs
        except:
            pass

    # 查询客户是否存在预约还款状态为'N'的数据
    def check_creditcard_reserve_repay_normal_order(self, mobile, state):
        try:
            cust_no = self.get_cust_info(columns='cust_no', match='=', mobile=mobile)[0]['cust_no']

            db_name = 'lifeapp_uat' if DBC_TAG == 'uat' else 'la'
            sql_query = "select count(*) count from %s.la_credit_repay_order where cust_no = '%s' and state='%s' "
            count = self._db.sql_run(sql_query, db_name, cust_no, state)[0]['count']
            return count
        except:
            pass

    # 预约还款订单状态更改
    def update_creditcard_order_state(self, update_state, orign_state=None, card_id=None):

        try:
            db_name = 'lifeapp_uat' if DBC_TAG == 'uat' else 'la'
            if orign_state is not None:
                sql_query = "update %s.la_credit_repay_order set state = '%s' where user_card_id = %s and " \
                            "state = '%s' ORDER BY id desc LIMIT 1;COMMIT ;"
                self._db.sql_run(sql_query, db_name, update_state, card_id, orign_state)
            else:
                sql_query = "update %s.la_credit_repay_order set state = '%s' where user_card_id = %s ORDER BY id desc LIMIT 1;COMMIT ;"
                self._db.sql_run(sql_query, db_name, update_state, card_id)
        except:

            pass

    def get_work_day_after_the_day_after_tomorrow(self):
        try:
            # 获取当前自然日
            today = Utility.DateUtil().getToday()
            # 获取下一个自然日
            tomorrow = today + datetime.timedelta(days=1)
            year = datetime.datetime.now().year
            month = datetime.datetime.now().month
            if year:
                year = int(year)
            else:
                year = datetime.date.today().year

            if month:
                month = int(month)
            else:
                month = datetime.datetime.now().month
            # 获取下一个自然日所属工作日T
            tomorrow_work_date = self.judge_is_work_date(day=str(tomorrow).replace('-', ''))[0]['WORK_DATE']
            # 获取工作日T的下一个工作日
            start_date = self.get_next_work_date(pre_work_date=str(tomorrow_work_date))[0]['WORK_DATE']
            # 获取起始日期所属月
            month_start = time.strptime(start_date, '%Y%m%d').tm_mon
            # 获取下个月的最后一天
            if month_start > 11:
                month_start_add_1 = month_start + 1 - 12
                year = year + 1
            else:
                month_start_add_1 = month_start + 1
                year = year
            monthRange = calendar.monthrange(year, month_start_add_1)[1]
            nxt_month_last_date = datetime.date(year=year, month=month_start_add_1, day=monthRange)
            nxt_month_last_date = str(nxt_month_last_date).replace('-', '')
            return nxt_month_last_date, start_date
        except:
            pass

    # 获取用户绑定的储蓄卡
    def get_cust_debit_card(self, bank_mobile):

        try:
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "select * from %s.cif_bank_card_info where bank_mobile = '%s' order by id desc limit 1;"
            cust_bank_cards = self._db.sql_run(sql_query, db_name, bank_mobile)

            return cust_bank_cards
        except:

            pass

    # 获取交易请求, 交易订单
    def get_trade_request(self, mobile):
        try:
            db_name = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            cust_no = self.get_cust_info(columns='cust_no', match='=', mobile=mobile)[0]['cust_no']

            sql_query = "SELECT * from %s.CTS_TRADE_REQUEST where CUST_NO = '%s' ORDER BY id DESC LIMIT 1;"
            trade_request = self._db.sql_run(sql_query, db_name, cust_no)
            sql_query1 = "SELECT * from %s.CTS_TRADE_ORDER where CUST_NO = '%s' ORDER BY id DESC LIMIT 1;"
            trade_order = self._db.sql_run(sql_query1, db_name, cust_no)

            return trade_request, trade_order
        except:
            pass

    # 查询一键随心取父订单
    def get_parent_trade_order(self, mobile):
        try:
            db_name = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            cust_no = self.get_cust_info(columns='cust_no', match='=', mobile=mobile)[0]['cust_no']
            to_prod = 'ZX05#000730'

            sql_query = "SELECT * from %s.CTS_TRADE_ORDER where CUST_NO = '%s' and ORDER_APKIND ='018' and ORDER_SUB_APKIND ='018100' ORDER BY id DESC LIMIT 1;"
            parent_trade_order = self._db.sql_run(sql_query, db_name, cust_no)
            return parent_trade_order
        except:
            pass

    # 获取交易请求, 交易订单 仅限一键随心取/超级支付
    def get_trade_request_order(self, mobile, product_id, parent_order_no):
        try:
            db_name = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            cust_no = self.get_cust_info(columns='cust_no', match='=', mobile=mobile)[0]['cust_no']

            if str(product_id).__contains__(','):
                user_trade_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
                near_work_date = self.judge_is_work_date(day=str(user_trade_time)[0:8])[0]['WORK_DATE']
                if str(user_trade_time)[0:8] == str(near_work_date):  # 交易当天为工作日
                    if '090000' < str(user_trade_time)[8:14] < '150000':  # 交易为9:00-15：00之间
                        sql_query = "SELECT * from %s.CTS_TRADE_REQUEST where CUST_NO = '%s' and PARENT_ORDER_NO = '%s' ORDER BY id DESC LIMIT 4;"
                        trade_request = self._db.sql_run(sql_query, db_name, cust_no, parent_order_no)
                    else:
                        sql_query = "SELECT * from %s.CTS_TRADE_REQUEST where CUST_NO = '%s' and PARENT_ORDER_NO = '%s' ORDER BY id DESC LIMIT 2;"
                        trade_request = self._db.sql_run(sql_query, db_name, cust_no, parent_order_no)
                else:
                    sql_query = "SELECT * from %s.CTS_TRADE_REQUEST where CUST_NO = '%s' and PARENT_ORDER_NO = '%s' ORDER BY id DESC LIMIT 2;"
                    trade_request = self._db.sql_run(sql_query, db_name, cust_no, parent_order_no)
                sql_query1 = "SELECT * from %s.CTS_TRADE_ORDER where CUST_NO = '%s' and PARENT_ORDER_NO = '%s' and FROM_PROD in ('%s', '%s') ORDER BY id DESC LIMIT 2;"
                trade_order_redeem = self._db.sql_run(sql_query1, db_name, cust_no, parent_order_no, str(product_id).split(',')[0], str(product_id).split(',')[1])
                sql_query2 = "SELECT * from %s.CTS_TRADE_ORDER where CUST_NO = '%s' and PARENT_ORDER_NO = '%s' and TO_PROD = 'ZX05#000730' ORDER BY id DESC LIMIT 1;"
                trade_order_recharge = self._db.sql_run(sql_query2, db_name, cust_no, parent_order_no)


            else:
                sql_query = "SELECT * from %s.CTS_TRADE_REQUEST where CUST_NO = '%s' ORDER BY id DESC LIMIT 2;"
                trade_request = self._db.sql_run(sql_query, db_name, cust_no)
                sql_query1 = "SELECT * from %s.CTS_TRADE_ORDER where CUST_NO = '%s' and PARENT_ORDER_NO = '%s' and FROM_PROD in ('%s') ORDER BY id DESC LIMIT 2;"
                trade_order_redeem = self._db.sql_run(sql_query1, db_name, cust_no, parent_order_no, product_id)
                sql_query2 = "SELECT * from %s.CTS_TRADE_ORDER where CUST_NO = '%s' and PARENT_ORDER_NO = '%s' and TO_PROD = 'ZX05#000730' ORDER BY id DESC LIMIT 2;"
                trade_order_recharge = self._db.sql_run(sql_query2, db_name, cust_no, parent_order_no, product_id)
            return trade_request, trade_order_redeem, trade_order_recharge
        except:
            pass

    # 高端极速赎回，获取交易请求, 交易订单
    def get_trade_request_vip_product(self, mobile, product_id):
        try:
            db_name = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            cust_no = self.get_cust_info(columns='cust_no', match='=', mobile=mobile)[0]['cust_no']

            sql_query = "SELECT * from %s.CTS_TRADE_REQUEST where CUST_NO = '%s' and PROD_ID='%s' ORDER BY id DESC LIMIT 1;"
            trade_request = self._db.sql_run(sql_query, db_name, cust_no, product_id)
            sql_query1 = "SELECT * from %s.CTS_TRADE_ORDER where CUST_NO = '%s' ORDER BY id DESC LIMIT 1;"
            trade_order = self._db.sql_run(sql_query1, db_name, cust_no)

            return trade_request, trade_order
        except:

            pass

    # 获取交易请求, 交易订单,目标产品信息
    def get_trade_info(self, order_no):

        try:
            db_name = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            db_name_pdc = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            sql_query = "SELECT * from %s.CTS_TRADE_REQUEST where ORDER_NO = '%s';"
            trade_request = self._db.sql_run(sql_query, db_name, order_no)
            sql_query1 = "SELECT * from %s.CTS_TRADE_ORDER where ORDER_NO = '%s';"
            trade_order = self._db.sql_run(sql_query1, db_name, order_no)
            sql_query2 = "select * from %s.pdc_productinfo where productid = '%s';"
            product_to_info = self._db.sql_run(sql_query2, db_name_pdc, trade_order[0]['TO_PROD'])
            product_from_info = self._db.sql_run(sql_query2, db_name_pdc, trade_order[0]['FROM_PROD'])

            return trade_request, trade_order, product_from_info, product_to_info
        except:

            pass

    # 获取费率
    def get_product_fee(self, product_id, purchase_amt=None):
        try:
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'

            sql_query = "select a.id, a.productid, a.accept_mode, a.product_status, a.issue_time, a.dssub_endtime,a.bid_time,a.product_expiredtime, a.liquidation_time, a.create_at, a.update_at, a.reservation_end_time,b.support_invest_regularly, p.start_date_per_day, p.end_date_per_day, p.large_amount_per_day " \
                        "from %s.pdc_issued_info a left join %s.pdc_product_marketing b on a.productid = b.productid " \
                        "join %s.pdc_productinfo p on a.productid=p.productid where a.productid = '%s' and b.accept_mode= 'M'"

            product_info = self._db.sql_run(sql_query, db_name, db_name, db_name, product_id)
            if product_info[0]['product_status'] == 4:
                # 日常申购费前端
                charge_rate_type = '11010'
            elif product_info[0]['product_status'] == 1:
                # 认购费前端
                charge_rate_type = '10010'
            # elif product_info[0]['product_status']  == 4:
            # # 日常赎回费
            #     charge_rate_type = '12000'

            sql_query1 = "SELECT * from %s.pdc_base_rate WHERE productid='%s' and charge_rate_type='%s' and if_excuted = 1 ORDER BY charge_rate_unit asc"
            product_fee = self._db.sql_run(sql_query1, db_name, product_id, '11010')

            flag = False
            index = 0
            if purchase_amt is not None:
                for i in range(0, len(product_fee)):
                    if product_fee[i]['end_div_stand'] is not None:
                        if purchase_amt < (product_fee[i]['end_div_stand'] * 10000) and (
                                    purchase_amt >= product_fee[i]['start_div_stand'] * 1000):
                            flag = True
                            index = i
                            break
                    else:
                        if purchase_amt >= (product_fee[i]['start_div_stand'] * 10000):
                            flag = True
                            index = i
                            break
            if flag is True:
                print 'find the fund fee'
            return product_fee[index], product_fee
        except:
            pass

    # 获取折扣费率
    def get_fund_discount_rate(self, product_id):
        try:
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'

            sql1 = "SELECT * from %s.pdc_discount_rate WHERE is_base_discount = 0 and productid='%s'"
            product_discount_rate = self._db.sql_run(sql1, db_name, product_id)

            if len(product_discount_rate) == 0:
                sql1 = "SELECT * from %s.pdc_discount_rate WHERE is_base_discount = 1"

            product_discount_rate = self._db.sql_run(sql1, db_name)
            return product_discount_rate
        except:
            pass

    # 获取赎回费率
    def get_pdc_product_marketing(self, product_id):
        try:
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'

            sql1 = "SELECT * from %s.pdc_product_marketing WHERE productid='%s' and accept_mode='M'"
            pdc_product_marketing = self._db.sql_run(sql1, db_name, product_id)
            return pdc_product_marketing

        except:
            pass

    # 基金制定定投计划
    def get_fund_make_invest_plan_validate(self, mobile):

        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query, db_name, mobile)[0]['cust_no']

            # step2-根据cust_no去查定投计划
            db_name = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            sql_query2 = "select * from %s.CTS_FUND_INVEST_PLAN where cust_no='%s' order by id desc"
            fund_invest_plan = self._db.sql_run(sql_query2, db_name, cust_no)

            return fund_invest_plan
        except:

            pass

    # 更新基金定投计划状态
    def update_fund_invest_plan_status(self, status, mobile=None, id=None, bank_account=None, amount=None, period=None,
                                       day=None, is_delete=None, bank_serial_no=None):
        try:
            db_name = 'cts_uat' if DBC_TAG == 'uat' else 'cts'

            if is_delete is None:
                if id is None:
                    protocol_no = self.get_fund_make_invest_plan_validate(mobile=mobile)[0]['PROTOCOL_NO']

                    # step2-根据cust_no去查定投计划
                    sql_query2 = "update %s.CTS_FUND_INVEST_PLAN set status='%s' where PROTOCOL_NO='%s'"
                    self._db.sql_run(sql_query2, db_name, status, protocol_no)

                    return protocol_no
                elif bank_account is not None:
                    sql_query2 = "update %s.CTS_FUND_INVEST_PLAN set status='%s',bank_acco='%s', " \
                                 "BANK_SERIAL_ID='%s', ap_amt='%s' where id='%s'"
                    self._db.sql_run(sql_query2, db_name, status, bank_account, bank_serial_no, amount, id)

                    return
                elif period is not None:
                    sql_query2 = "update %s.CTS_FUND_INVEST_PLAN set status='%s', period='%s', `day`='%s', ap_amt='%s' where id='%s';COMMIT;"
                    self._db.sql_run(sql_query2, db_name, status, period, day, amount, id)
                else:
                    sql_query2 = "update %s.CTS_FUND_INVEST_PLAN set status='%s' where id='%s'"
                    self._db.sql_run(sql_query2, db_name, status, id)

                    return
            else:
                if id is None:
                    protocol_no = self.get_fund_make_invest_plan_validate(mobile=mobile)[0]['PROTOCOL_NO']

                    # step2-根据cust_no去查定投计划
                    sql_query2 = "update %s.CTS_FUND_INVEST_PLAN set status='%s', is_delete='%s' where PROTOCOL_NO='%s'"
                    self._db.sql_run(sql_query2, db_name, status, is_delete, protocol_no)

                    return protocol_no
                elif bank_account is not None:
                    sql_query2 = "update %s.CTS_FUND_INVEST_PLAN set status='%s',bank_acco='%s',ap_amt='%s', is_delete='%s' where id='%s'"
                    self._db.sql_run(sql_query2, db_name, status, bank_account, amount, is_delete, id)

                    return
                elif period is not None:
                    sql_query2 = "update %s.CTS_FUND_INVEST_PLAN set status='%s', period='%s', `day`='%s', ap_amt='%s', is_delete='%s' where id='%s';COMMIT;"
                    self._db.sql_run(sql_query2, db_name, status, period, day, amount, is_delete, id)
                else:
                    sql_query2 = "update %s.CTS_FUND_INVEST_PLAN set status='%s', is_delete='%s' where id='%s'"
                    self._db.sql_run(sql_query2, db_name, status, is_delete, id)

        except Exception, e:
            print e
            pass

    # 删除基金定投/理财计划
    def delete_fund_invest_plan(self, mobile):
        try:
            db_name = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            id = self.get_fund_invest_plan_detail_db(validate_phone=mobile)[0]['ID']

            # step2-根据id删除计划
            sql_query1 = "select * from %s.CTS_FUND_INVEST_PLAN where id='%s'"
            protocol_no = self._db.sql_run(sql_query1, db_name, id)[0]['PROTOCOL_NO']
            sql_query2 = "delete from %s.CTS_FUND_INVEST_PLAN where id='%s'"
            self._db.sql_run(sql_query2, db_name, id)
            return protocol_no
        except Exception, e:

            pass

    # 获取用户所有非终止状态的基金定投计划列表
    def fund_invest_plan_list(self, mobile):

        try:
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query, db_name, mobile)[0]['cust_no']

            db_name = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            sql_query2 = "select * from %s.CTS_FUND_INVEST_PLAN where cust_no='%s' and status!='E' order by id desc"
            fund_plans = self._db.sql_run(sql_query2, db_name, cust_no)

            return fund_plans
        except Exception, e:

            pass

    # 插入联名卡待激活的卡
    def insert_joint_card_activate_card(self, card_no, mobile):

        try:
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            cust_info = self.get_cust_info(columns='cert_no', match='=', mobile=mobile)
            outer_order_no = random.randrange(1000000, 9999999)
            today = Utility.DateUtil().getToday().strftime('%Y%m%d')
            middle = random.randrange(1000, 9999)
            trans_no = today + '#' + str(middle) + '#' + str(outer_order_no)
            serial_id = Utility.GetData().GenAlphanumeric(17)
            sql = "INSERT INTO %s.cif_joint_card (system_code, trans_no, trans_type, bank_trans_type, outer_order_no, serial_id, cust_no, name, cert_type, std_cert_type, cert_no, bank, card_type, card_no, bank_mobile, status, status_date, status_reason, branch_code, branch_name, ap_date, ap_time, set_date, oper_no, open_date, open_time, card_valid_date, operator, reviewer, cust_detail, extend_info, match_flag, cms_operator, created_at, updated_at) VALUES ('NY', '%s', '1', '101022', '%s', '%s', null, '测试者', '1', '0', '%s', 'A46', '41', '%s', '%s', 'I', null, null, '9600', '广州分行营业部', '%s', '103000', '%s', '16', '%s', '', '20251231', '009146', '000830', '{\"address\":\"上海\",\"certSignOrg\":\"1000_北京市\",\"certValidDate\":\"20250925\",\"email\":\"\",\"homeTel\":\"\",\"occupation\":\"1011\",\"officeTel\":\"\",\"zipcode\":\"888888\"}', '', null, null, '2017-06-19 16:10:57', '2017-06-19 16:10:57');COMMIT ;"
            self._db.sql_run(sql, db_name, trans_no, outer_order_no, serial_id, cust_info[0]['cert_no'], card_no,
                             mobile,
                             today, today, today)

        except Exception, e:

            print repr(e)
            pass

    # 查找联名卡
    def get_joint_card(self, mobile, card_no=None):

        try:
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'

            if card_no is not None:
                sql = "SELECT * FROM %s.cif_joint_card WHERE card_no = '%s' and bank_mobile = '%s' ORDER BY id DESC"
                cards = self._db.sql_run(sql, db_name, card_no, mobile)
            else:
                sql = "SELECT * FROM %s.cif_joint_card WHERE bank_mobile = '%s' ORDER BY id DESC"
                cards = self._db.sql_run(sql, db_name, mobile)

            return cards

        except Exception, e:

            print repr(e)
            pass

    # 查找限额
    def get_cts_parameter(self, query_condition):

        try:
            db_name = 'cts_uat' if DBC_TAG == 'uat' else 'cts'

            sql = "SELECT * FROM %s.CTS_PARAMETER WHERE %s"
            limit = self._db.sql_run(sql, db_name, query_condition)

            return limit
        except:

            pass

    # 查找南粤CTS_NANYUE_REDEEM_LIMIT
    def get_nanyue_limit(self, card_no):

        try:
            db_name = 'cts_uat' if DBC_TAG == 'uat' else 'cts'

            sql = "SELECT * FROM %s.CTS_NANYUE_REDEEM_LIMIT WHERE card_no = '%s'"
            limit = self._db.sql_run(sql, db_name, card_no)

            return limit
        except:

            pass

    # 修改预约码状态,便于程序循环执行
    def reservation_code_status_modify(self, buy_quota, buy_count, reserve_quota, reserve_count, mobile, reserve_code,
                                       product_id):

        try:
            # 更新预约码未使用额度和未使用人数
            db_name = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            sql_query = "update %s.CTS_PROD_QUOTA_CONTROL set BUY_QUOTA = '%s', BUY_COUNT = '%s', RESERVE_QUOTA = '%s', RESERVE_COUNT = '%s' where PROD_ID = '%s'"
            self._db.sql_run(sql_query, db_name, buy_quota, buy_count, reserve_quota, reserve_count, product_id)

            # 更新预约码使用状态
            db_name = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            sql_query = "update %s.CTS_PROD_RESERVE set STATUS = '2', IS_DELETE = 0 where MOBILE_NO='%s' and RESERVE_CODE = '%s'"
            self._db.sql_run(sql_query, db_name, mobile, reserve_code)

            return
        except:

            pass

    # 更新删除状态
    def update_bank_card_delete_status(self, card_no, is_delete='N'):

        try:
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query1 = "update %s.cif_bank_card_info set is_delete = '%s' where card_no ='%s' ;COMMIT;"
            self._db.sql_run(sql_query1, db_name, is_delete, card_no)

        except:

            pass

    # 删除银行卡
    def delete_bank_card(self, card_no=None, mobile=None):

        try:
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            if mobile is None:
                sql_query1 = "delete from  %s.cif_bank_card_info  where card_no ='%s' ;COMMIT;"
                self._db.sql_run(sql_query1, db_name, card_no)
            else:
                cust_no = self.get_cust_info(columns='cust_no', match='=', mobile=mobile)[0]['cust_no']
                # sql_query1 = "delete from %s.cif_bank_card_info where cust_no = '%s' order by created_at desc limit 1;"
                sql_query1 = "select * from %s.cif_bank_card_info where cust_no = '%s' order by created_at desc limit 1;"
                card_no = self._db.sql_run(sql_query1, db_name, cust_no)[0]['card_no']
                sql_query2 = "delete from %s.cif_bank_card_info where card_no = '%s' ;"
                self._db.sql_run(sql_query2, db_name, card_no)

        except:

            pass

    # 现金宝累计收益
    def xjb_last_profit(self, mobile, apkind):

        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query, db_name, mobile)[0]['cust_no']

            # step2-根据cust_no去查首页收益信息
            db_name = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            num = int(cust_no) % 8
            table_name = 'CTS_VACCO_PAYMENT_DETAIL' + '_' + str(num)
            sql_query = "select ifnull(sum(a.total_profit),0) total_profit from %s." + table_name + " a where  1=1 " \
                                                                                                    "and a.apkind ='%s' and  a.CUST_NO = '%s'"
            total_profit = self._db.sql_run(sql_query, db_name, apkind, cust_no)[0]['total_profit']

            return total_profit

        except:

            pass

    # 根据银行卡号查绑卡记录
    def get_bank_card_by_card_no(self, mobile, card_no):

        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query1 = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query1, db_name, mobile)[0]['cust_no']

            # step2-根据cust_no去查卡是否已删除的状态值信息
            sql_query2 = "select * from %s.cif_bank_card_info a where a.cust_no ='%s' and a.card_no = '%s' order by a.id DESC"
            cards = self._db.sql_run(sql_query2, db_name, cust_no, card_no)

            return cards

        except:

            pass

    # 获取预约码
    def get_reserve_code(self, mobile, reserve_code):

        try:
            db_name = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            sql_query = "SELECT * FROM %s.CTS_PROD_RESERVE where MOBILE_NO= '%s' or RESERVE_CODE= '%s'"
            reserve_code = self._db.sql_run(sql_query, db_name, mobile, reserve_code)

            return reserve_code
        except:

            pass

    # 查找验证码，部分银行发送验证码是银行发的，并不是华信发的
    def get_mobile_code_send_by_bank(self, mobile):

        try:
            db_name = 'be_uat' if DBC_TAG == 'uat' else 'be'
            sql_query = "SELECT auth_code FROM %s.be_sms_auth_code WHERE mobile_no = '%s' order by id desc LIMIT 1;"
            mobile_code = self._db.sql_run(sql_query, db_name, mobile)[0]['auth_code']

            return mobile_code
        except:

            pass

    # 查出最高优先级的充值通道, bank_name请保持这个名字跟be_bank_group表里面的group_name一样，否则会取不到
    def get_highest_prio_bank_channel(self, bank_name):

        try:
            db_name = 'be_uat' if DBC_TAG == 'uat' else 'be'
            sql = "SELECT DISTINCT * from %s.be_channel_conf c LEFT JOIN %s.be_bank_group g on c.bank_group_id = g.group_id WHERE c.app_recharge='01' and c.recharge_priority is not NULL and g.group_name = '%s' ORDER BY c.recharge_priority asc LIMIT 1;"
            bank_conf = self._db.sql_run(sql, db_name, db_name, bank_name)

            return bank_conf[0]['bank_no']
        except:

            pass

    # 交易密码验证
    def trade_password_validate(self, mobile):

        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query1 = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query1, db_name, mobile)[0]['cust_no']

            # step2-根据cust_no去查交易密码
            sql_query2 = "select * from %s.cif_cust_pay_pwd where cust_no ='%s'"
            trade_password = self._db.sql_run(sql_query2, db_name, cust_no)

            return trade_password

        except:

            pass

    # 绑卡-查询所有通道信息
    def check_all_bank_channel_list(self):

        try:
            db_name = 'be_uat' if DBC_TAG == 'uat' else 'be'
            sql_query = "select distinct g.group_id, g.group_name from %s.be_channel_conf b, %s.be_bank_group g where " \
                        "g.group_id = b.bank_group_id and b.m_add_card = '01' order by bank_group_id DESC"
            group_id = self._db.sql_run(sql_query, db_name, db_name)

            return group_id
        except:

            pass

    # 根据bank_no查出银行绑卡记录
    def get_binding_card_by_bank_no(self, mobile, bank_no):
        try:
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql = "SELECT * FROM %s.cif_bank_card_info WHERE bank_no = '%s' and cust_no=(select cust_no from %s.cif_cust_base WHERE mobile='%s')"
            cards = self._db.sql_run(sql, db_name, bank_no, db_name, mobile)
            return cards
        except:

            pass

    # 删除最高优先级的绑卡记录
    def delete_bind_card_with_highest_priority(self, mobile, bank_no):

        try:
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            cards = self.get_binding_card_by_bank_no(mobile=mobile, bank_no=bank_no)

            if len(cards) == 1:
                id = cards[0]['id']
                del_sql = "delete from %s.cif_bank_card_info where id = %s;COMMIT ;"
                self._db.sql_run(del_sql, db_name, id)
            else:
                print 'no binding record with highest priority exists.'

        except Exception, e:

            pass

    # 设置自选基金
    def get_fav_fund(self, mobile, object_id):
        try:
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query, db_name, mobile)[0]['cust_no']

            db_name1 = 'as_uat' if DBC_TAG == 'uat' else 'as'
            sql_query1 = "select * from %s.as_cust_favorite where cust_no='%s' and is_delete='0' order by id desc LIMIT 1;"
            add_fav_fund = self._db.sql_run(sql_query1, db_name1, cust_no)
            sql_query2 = "select * from %s.as_cust_favorite where object_id='%s' order by id desc LIMIT 1;"
            add_fav = self._db.sql_run(sql_query2, db_name1, object_id)
            return add_fav_fund, add_fav
        except:
            pass

    # 获取优惠券数量信息
    def get_coupon_info(self, mobile, prod_type_scope_val, prod_id):
        try:
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "select cust_no from %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query, db_name, mobile)[0]['cust_no']

            db_name1 = 'points_uat' if DBC_TAG == 'uat' else 'points'
            sql_query1 = "select * from %s.COUPON_ISSUE a,%s.COUPON_ECARD b,%s.COUPON_ACCOUNT c " \
                         "where a.ECARD_NO=b.ECARD_NO and a.cust_no = c.cust_no and a.cust_no='%s' and b.status='ISSUE' and b.start_at<SYSDATE() and b.end_at>SYSDATE()" \
                         "and COUPON_BATCH_ID in" \
                         "(SELECT DISTINCT COUPON_BATCH_ID from %s.COUPON_BATCH_SCOPE WHERE SCOPE_VAL in (%s) or SCOPE_VAL='%s') ORDER BY AMOUNT DESC, COUPON_ACCOUNT_HIS_ID ASC"

            coupon_available_qty = self._db.sql_run(sql_query1, db_name1, db_name1, db_name1, cust_no,
                                                    db_name1, prod_type_scope_val, prod_id)
            return coupon_available_qty

        except:
            pass

    # 查找客户的可使用优惠券
    # prod_type_scope_val 是指支持的产品类型
    def get_coupon_count(self, mobile, amount, prod_type_scope_val, prod_id):

        try:
            cust_no = self.get_cust_info(columns='cust_no', match='=', mobile=mobile)[0]['cust_no']
            points_db_name = 'points_uat' if DBC_TAG == 'uat' else 'points'
            sql_coupon_account = "select * from %s.COUPON_ISSUE i,%s.COUPON_ECARD c where i.ECARD_NO=c.ECARD_NO and i.CUST_NO='%s' and c.status='ISSUE' and c.start_at<SYSDATE() and c.end_at>SYSDATE() and COUPON_BATCH_ID in (SELECT DISTINCT COUPON_BATCH_ID from %s.COUPON_BATCH_SCOPE WHERE SCOPE_VAL in (%s) or SCOPE_VAL='%s' and STATUS='Y') ORDER BY AMOUNT DESC, COUPON_ACCOUNT_HIS_ID ASC"
            coupon_count = self._db.sql_run(sql_coupon_account, points_db_name, points_db_name, cust_no, points_db_name,
                                            prod_type_scope_val, prod_id)

            sql_coupon_available = "select * from %s.COUPON_ISSUE i,%s.COUPON_ECARD c where i.ECARD_NO=c.ECARD_NO and i.CUST_NO='%s' and c.status='ISSUE' and c.start_at<SYSDATE() and c.end_at>SYSDATE() and COUPON_AMOUNT <= %s and COUPON_BATCH_ID in (SELECT DISTINCT COUPON_BATCH_ID from %s.COUPON_BATCH_SCOPE WHERE SCOPE_VAL in (%s) or SCOPE_VAL='%s' and STATUS='Y') ORDER BY AMOUNT DESC, COUPON_ACCOUNT_HIS_ID ASC"
            coupon_available = self._db.sql_run(sql_coupon_available, points_db_name, points_db_name, cust_no, amount,
                                                points_db_name, prod_type_scope_val, prod_id)

            sql_coupon_not_used = "select * from %s.COUPON_ISSUE i,%s.COUPON_ECARD c where i.ECARD_NO=c.ECARD_NO and i.CUST_NO='%s' and c.status='ISSUE' and c.start_at<SYSDATE() and c.end_at>SYSDATE() and (COUPON_AMOUNT > %s and COUPON_BATCH_ID in (SELECT DISTINCT COUPON_BATCH_ID from %s.COUPON_BATCH_SCOPE WHERE SCOPE_VAL in (%s) or SCOPE_VAL='%s' and STATUS='Y')) ORDER BY AMOUNT DESC, COUPON_ACCOUNT_HIS_ID ASC"
            coupon_not_used = self._db.sql_run(sql_coupon_not_used, points_db_name, points_db_name, cust_no, amount,
                                               points_db_name, prod_type_scope_val, prod_id)

            return coupon_count, coupon_available, coupon_not_used
        except:
            pass

    # 根据CARD NO查找优惠券的信息
    def get_coupon_no(self, ecard_no):

        try:
            points_db_name = 'points_uat' if DBC_TAG == 'uat' else 'points'
            sql_batch = "select * from %s.COUPON_ECARD where ECARD_NO = %s"
            coupon_ecard = self._db.sql_run(sql_batch, points_db_name, ecard_no)

            return coupon_ecard

        except:

            pass

    # 查看最新的现金宝收支明细
    def get_vacco_payment_details(self, mobile):

        try:
            db_name = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            cust_no = self.get_cust_info(columns='cust_no', match='=', mobile=mobile)[0]['cust_no']
            num = int(cust_no) % 8
            table_name = 'CTS_VACCO_PAYMENT_DETAIL' + '_' + str(num)
            sql_batch = "select * from %s." + table_name + " where cust_no = '%s' order by id DESC"
            detail = self._db.sql_run(sql_batch, db_name, cust_no)

            return detail

        except:

            pass

    # 查看在途资产
    def get_asset_in_transit(self, mobile):

        try:
            db_name = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            cust_no = self.get_cust_info(columns='cust_no', match='=', mobile=mobile)[0]['cust_no']
            sql_batch = "SELECT * from %s.CTS_ASSET_IN_TRANSIT where CUST_NO = '%s' ORDER BY id DESC;"
            asset_in_transit = self._db.sql_run(sql_batch, db_name, cust_no)

            return asset_in_transit
        except:
            pass

    # 查看份额变动流水表
    def get_trade_quty_chg(self, mobile):
        try:
            db_name = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            cust_no = self.get_cust_info(columns='cust_no', match='=', mobile=mobile)[0]['cust_no']
            sql_batch = "SELECT * from %s.CTS_TRADE_QUTY_CHG where CUST_NO = '%s' ORDER BY id DESC"
            trade_quty_chg = self._db.sql_run(sql_batch, db_name, cust_no)

            return trade_quty_chg
        except:
            pass

    # 查看用户消费的券
    def get_cust_consume_coupon(self, mobile, ecard_no):

        try:
            db_name = 'points_uat' if DBC_TAG == 'uat' else 'points'
            cust_no = self.get_cust_info(columns='cust_no', match='=', mobile=mobile)[0]['cust_no']
            sql_batch = "SELECT * from %s.COUPON_CONSUME where ECARD_NO = '%s' and CUST_NO= '%s' ORDER BY id DESC"
            consume_coupon = self._db.sql_run(sql_batch, db_name, ecard_no, cust_no)

            return consume_coupon
        except:

            pass

    # 获取用户产品总收益
    def get_cust_total_profit(self, mobile, prod_type):

        try:
            db_name = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            cust_no = self.get_cust_info(columns='cust_no', match='=', mobile=mobile)[0]['cust_no']
            sql = "SELECT ifnull(sum(TOTAL_PROFIT), 0) as total_profit FROM %s.CTS_DAILY_PROFIT WHERE CUST_NO='%s' and PROD_TYPE='%s';"
            total_profit = self._db.sql_run(sql, db_name, cust_no, prod_type)
            return total_profit[0]['total_profit']

        except:

            pass

    # 获取最新的预约单
    def get_cust_latest_trade_reserve(self, mobile):
        try:
            db_name = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            cust_no = self.get_cust_info(columns='cust_no', match='=', mobile=mobile)[0]['cust_no']

            sql = "SELECT * from %s.CTS_TRADE_RESERVE where CUST_NO = '%s' ORDER BY id DESC limit 1;"
            trade_reserve = self._db.sql_run(sql, db_name, cust_no)
            return trade_reserve
        except:
            pass

    # # 获取最新的预约单/限一键随心取使用
    # def get_cust_latest_trade_reserve(self, mobile):
    #     try:
    #         db_name = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
    #         cust_no = self.get_cust_info(columns='cust_no', match='=', mobile=mobile)[0]['cust_no']
    #
    #         sql = "SELECT * from %s.CTS_TRADE_RESERVE where CUST_NO = '%s' ORDER BY id DESC limit 1;"
    #         trade_reserve = self._db.sql_run(sql, db_name, cust_no)
    #         return trade_reserve
    #     except:
    #         pass

    # 获取优惠券最新冻结和解冻
    def get_cust_latest_coupon_frozen_his(self, ecard_no):

        try:
            db_name = 'points_uat' if DBC_TAG == 'uat' else 'points'

            sql = "SELECT * from %s.COUPON_FROZEN_HIS where ECARD_NO = '%s' ORDER BY id DESC limit 1;"
            trade_reserve = self._db.sql_run(sql, db_name, ecard_no)

            return trade_reserve

        except:

            pass

    # 获取APP热门产品
    def get_hot_on_sale_product_list(self, product_type):

        try:
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            sql = "SELECT DISTINCT * FROM %s.pdc_product_marketing m left JOIN %s.pdc_productinfo p on m.productid = p.productid WHERE hot = '1' and p.product_type = '%s' and m.accept_mode = 'M' and m.onsale_flag = '1';"
            hot_product_list = self._db.sql_run(sql, db_name, db_name, product_type)

            return hot_product_list
        except:

            pass

    # 获取APP上架定期产品
    def get_on_sale_product_list(self, product_type, accept_mode, is_archive):
        try:
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            sql = "SELECT DISTINCT * FROM %s.pdc_product_marketing m left JOIN %s.pdc_productinfo p on m.productid = p.productid WHERE p.product_type = '%s' and m.accept_mode = '%s' and m.onsale_flag = '1' and m.is_archive='%s' ORDER BY m.create_at DESC;"
            product_list = self._db.sql_run(sql, db_name, db_name, product_type, accept_mode, is_archive)

            return product_list
        except:
            pass

    # 查看资金在途CTS_CAPITAL_IN_TRANSIT
    def get_capital_in_transit(self, mobile):

        try:
            db_name = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            cust_no = self.get_cust_info(columns='cust_no', match='=', mobile=mobile)[0]['cust_no']

            sql_batch = "SELECT * from %s.CTS_CAPITAL_IN_TRANSIT where CUST_NO = '%s' ORDER BY id DESC;"
            capital_in_transit = self._db.sql_run(sql_batch, db_name, cust_no)

            return capital_in_transit
        except:

            pass

    # 高端，定期宝持仓资产
    def my_hold_dqb_vip_list(self, mobile, product_type):

        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query1 = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query1, db_name, mobile)[0]['cust_no']

            # step2：根据cust_no去查持仓份额
            db_name1 = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            sql_query2 = "select * from %s.CTS_ASSET_IN_TRANSIT where cust_no ='%s' and apkind in ('020','022','039') and " \
                         "PROD_TYPE = '%s' and BALANCE >= 0 order by CREATED_AT DESC "

            sql_query2_1 = "select IFNULL(sum(BALANCE),0) BALANCE from %s.CTS_ASSET_IN_TRANSIT where cust_no ='%s' and apkind in ('024') and " \
                           "PROD_TYPE = '%s' and BALANCE < 0 order by CREATED_AT DESC "
            hold_shares_transit = self._db.sql_run(sql_query2, db_name1, cust_no, product_type)
            reedeem_hold_shares_transit = self._db.sql_run(sql_query2_1, db_name1, cust_no, product_type)

            sql_query3 = "select * from %s.CTS_PROD_QUTY where cust_no ='%s' and PROD_TYPE = '%s' ORDER BY PROD_TYPE, PROD_ID ASC "
            hold_shares_quty = self._db.sql_run(sql_query3, db_name1, cust_no, product_type)

            return hold_shares_quty, reedeem_hold_shares_transit, hold_shares_transit

        except:

            pass

    # 获取产品净值
    def get_fund_nav(self, fund_id):
        try:
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            sql_query = "SELECT * from %s.pdc_nav where fundid ='%s' order by nav_date desc;"
            fund_value = self._db.sql_run(sql_query, db_name, str(fund_id).split('#')[1])

            sql_query1 = "SELECT count(*) nav_count from %s.pdc_nav where fundid ='%s';"
            count_fund_nav = self._db.sql_run(sql_query1, db_name, str(fund_id).split('#')[1])
            if len(fund_value) == 0:
                return 1
            else:
                # if fund_value[0]['nav'] is None or fund_value[0]['nav'] == '':
                #     return 1
                # else:
                return fund_value, count_fund_nav
        except:
            pass

    # 更新自选基金
    def update_fav_fund(self, mobile, fund_id=None, id=None):
        try:
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query, db_name, mobile)[0]['cust_no']

            db_name1 = 'as_uat' if DBC_TAG == 'uat' else 'as'

            if fund_id is None:
                if id is None:
                    sql_query1 = "update %s.as_cust_favorite set is_delete=1 where cust_no='%s' and is_delete=0 and type=0;"
                    self._db.sql_run(sql_query1, db_name1, cust_no)
                else:
                    sql_query1 = "update %s.as_cust_favorite set is_delete=0 where id=%s;"
                    self._db.sql_run(sql_query1, db_name1, id)
            else:
                sql_query1 = "select * from %s.as_cust_favorite where cust_no='%s' and is_delete=0 and object_id='%s' order by id desc LIMIT 1;"
                add_fav_fund = self._db.sql_run(sql_query1, db_name1, cust_no, fund_id)
                id = add_fav_fund[0]['id']

                sql_query2 = "update %s.as_cust_favorite set is_delete=1 where id=%s;COMMIT ;"
                self._db.sql_run(sql_query2, db_name1, id)
        except:
            pass

    # 获取产品信息
    def get_product_info(self, product_id=None, product_name=None):
        try:
            print product_id
            print product_name
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            if product_name is None:
                sql = "SELECT * FROM %s.pdc_productinfo WHERE productid = '%s';"
                product_info = self._db.sql_run(sql, db_name, product_id)
            else:
                sql = "SELECT * FROM %s.pdc_productinfo WHERE product_short_name = '%s';"
                product_info = self._db.sql_run(sql, db_name, product_name)
            return product_info
        except:
            pass

    # 搜索所有产品（定期和高端）
    def search_all_fin_product(self, keyword):
        try:
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            # step-1 根据产品名和类型查出已上架的产品详情，product_type=1为定期，product_type=3为高端
            dqb_sql = "SELECT DISTINCT a.* FROM %s.pdc_productinfo a, %s.pdc_product_marketing b WHERE a.productid=b.productid and a.product_short_name like '%%%s%%' and a.product_type ='1' and b.onsale_flag='1';"
            dqb_product_info = self._db.sql_run(dqb_sql, db_name, db_name, keyword)
            dqb1_sql = "SELECT DISTINCT a.* FROM %s.pdc_productinfo a, %s.pdc_product_marketing b WHERE a.productid=b.productid and a.product_short_name like '%%%s%%' and a.product_type ='1' and b.onsale_flag='1';"
            dqb1_product_info = self._db.sql_run(dqb1_sql, db_name, db_name, keyword)
            vip_sql = "SELECT DISTINCT a.* FROM %s.pdc_productinfo a, %s.pdc_product_marketing b WHERE a.productid=b.productid and a.product_short_name like '%%%s%%' and a.product_type ='3' and b.onsale_flag='1';"
            vip_product_info = self._db.sql_run(vip_sql, db_name, db_name, keyword)
            vip1_sql = "SELECT DISTINCT a.* FROM %s.pdc_productinfo a, %s.pdc_product_marketing b WHERE a.productid=b.productid and a.product_short_name like '%%%s%%' and a.product_type ='3' and b.onsale_flag='1' ORDER BY id DESC;"
            vip1_product_info = self._db.sql_run(vip1_sql, db_name, db_name, keyword)
            fund_sql = "SELECT DISTINCT a.* FROM %s.pdc_productinfo a, %s.pdc_product_marketing b WHERE a.productid=b.productid and a.product_short_name like '%%%s%%' and a.product_type ='2' and b.onsale_flag='1';"
            fund_product_info = self._db.sql_run(fund_sql, db_name, db_name, keyword)
            fund1_sql = "SELECT DISTINCT a.* FROM %s.pdc_productinfo a, %s.pdc_product_marketing b WHERE a.productid=b.productid and a.product_short_name like '%%%s%%' and a.product_type ='2' and b.onsale_flag='1' ORDER BY id DESC;"
            fund1_product_info = self._db.sql_run(fund1_sql, db_name, db_name, keyword)

            return dqb_product_info, dqb1_product_info, vip_product_info, vip1_product_info, fund_product_info, fund1_product_info
        except:
            pass

    # 获取客户积分消费
    def get_points_consume(self, mobile):
        try:
            db_name = 'points_uat' if DBC_TAG == 'uat' else 'points'
            cust_no = self.get_cust_info(columns='cust_no', match='=', mobile=mobile)[0]['cust_no']
            sql = "SELECT * FROM %s.POINTS_CONSUME WHERE CUST_NO = '%s' ORDER BY id desc LIMIT 1"
            points_consume = self._db.sql_run(sql, db_name, cust_no)

            return points_consume
        except:
            pass

    # 获取客户积分总数
    def get_cust_total_points_amount(self, mobile):

        try:
            db_name = 'points_uat' if DBC_TAG == 'uat' else 'points'
            cust_no = self.get_cust_info(columns='cust_no', match='=', mobile=mobile)[0]['cust_no']
            sql = "SELECT * FROM %s.POINTS_ACCOUNT WHERE CUST_NO = '%s' ORDER BY id desc LIMIT 1;"
            points = self._db.sql_run(sql, db_name, cust_no)
            return points
        except:
            pass

    # 获取客户积分冻结
    def get_points_frozen(self, mobile):
        try:
            db_name = 'points_uat' if DBC_TAG == 'uat' else 'points'
            cust_no = self.get_cust_info(columns='cust_no', match='=', mobile=mobile)[0]['cust_no']
            sql = "SELECT * FROM %s.POINTS_FROZEN_HIS WHERE CUST_NO = '%s' ORDER BY id desc LIMIT 1"
            points_frozen = self._db.sql_run(sql, db_name, cust_no)

            return points_frozen
        except:
            pass

    # 查看用户具体产品的持仓情况
    def get_cust_prod_quty_by_product_id(self, mobile, product_id=None):
        try:
            db_name = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            cust_no = self.get_cust_info(columns='cust_no', match='=', mobile=mobile)[0]['cust_no']
            if product_id is not None:
                sql = "select * from %s.CTS_PROD_QUTY where cust_no ='%s' and PROD_ID = '%s'"
                prod_quty = self._db.sql_run(sql, db_name, cust_no, product_id)
            else:
                sql = "select * from %s.CTS_PROD_QUTY where cust_no ='%s'"
                prod_quty = self._db.sql_run(sql, db_name, cust_no)

            return prod_quty
        except:

            pass

    # 查看用户未还款的借款情况
    def get_cust_pledge_loan(self, mobile, product_id, is_history):

        try:
            db_name = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            cust_no = self.get_cust_info(columns='cust_no', match='=', mobile=mobile)[0]['cust_no']

            if is_history == '0':
                sql = "SELECT * FROM %s.CTS_PLEDGE_LOAN WHERE CUST_NO = '%s' and PROD_ID='%s' and STATUS != 'PAID' order by id desc"
            else:
                sql = "SELECT * FROM %s.CTS_PLEDGE_LOAN WHERE CUST_NO = '%s' and PROD_ID='%s' and STATUS = 'PAID' order by id desc"
            pledge_loan = self._db.sql_run(sql, db_name, cust_no, product_id)

            return pledge_loan
        except:
            pass

    # 查看产品质押情况
    def get_product_pledge_info(self, product_id):
        try:
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            sql = "SELECT * FROM %s.pdc_pledge WHERE productid = '%s';"
            pledge_product = self._db.sql_run(sql, db_name, product_id)

            return pledge_product
        except:

            pass

    # 查看产品质押情况
    def get_pledge_repay_record(self, product_id):
        try:
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            sql = "SELECT * FROM %s.pdc_pledge WHERE productid='%s' order by id asc"
            pledge_product = self._db.sql_run(sql, db_name, product_id)
            return pledge_product
        except:
            pass

    # 高端赎回费率
    def vip_redeem_rate(self, product_id):
        try:
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            sql = "SELECT * FROM %s.pdc_base_rate where productid = '%s' and if_excuted='1' and charge_rate_type='12000' ORDER BY id desc LIMIT 1"
            product_rate = self._db.sql_run(sql, db_name, product_id)
            return product_rate
        except:
            pass

    # 高端申购费率
    def vip_purchase_rate(self, product_id):

        try:
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            sql = "SELECT * FROM %s.pdc_base_rate where productid = '%s' and if_excuted='1' and charge_rate_type='11010' ORDER BY id desc LIMIT 1"
            product_rate = self._db.sql_run(sql, db_name, product_id)

            return product_rate

        except:
            pass

    # 基金赎回费用估算
    def fund_redeem_cost_calt_value(self, mobile, product_id):
        # 
        try:
            db_name1 = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query1 = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query1, db_name1, mobile)[0]['cust_no']

            # 基金赎回金额
            db_name2 = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            sql_query2 = "select * from %s.CTS_ASSET_IN_TRANSIT where CUST_NO = '%s' and PROD_ID ='%s' and PROD_TYPE = '2' order by id DESC"
            redeem_balance = self._db.sql_run(sql_query2, db_name2, cust_no, product_id)

            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            # 查基金费率
            sql = "SELECT * FROM %s.pdc_base_rate where productid = '%s' and if_excuted='1' and charge_rate_type_des='日常赎回费' " \
                  "ORDER BY id desc LIMIT 1"
            product_rate = self._db.sql_run(sql, db_name, product_id)

            # 查基金单位净值
            sql1 = "SELECT * FROM %s.pdc_nav where fundid = '%s' order by nav_date desc LIMIT 1"
            fund_nav = self._db.sql_run(sql1, db_name, str(product_id).split('#')[1])

            # 查PDC产品营销渠道配置中配置的产品费率预估范围
            sql2 = "SELECT * FROM %s.pdc_product_marketing where productid='%s'"
            product_nav_value = self._db.sql_run(sql2, db_name, product_id)

            # 查PDC产品"允许赎回日"配置
            sql3 = "SELECT * from %s.pdc_productinfo where productid='%s'"
            set_value = self._db.sql_run(sql3, db_name, product_id)

            # 预计到账金额 ＝ 单位净值＊赎回金额＊(1-最大费率)*(1+费率预估范围)，备注费率预估范围是PDC产品营销渠道配置的最小值和最大值
            pay_back_money_min = decimal.Decimal(fund_nav[0]['nav'] * (-redeem_balance[0]['BALANCE']) * (
                1 - product_rate[0]['max_charge_rate'] / 100) * (
                                                     1 + product_nav_value[0]['amplitude_from'] / 100)).quantize(
                decimal.Decimal('0.00'))
            pay_back_money_max = decimal.Decimal(fund_nav[0]['nav'] * (-redeem_balance[0]['BALANCE']) * (
                1 - product_rate[0]['max_charge_rate'] / 100) * (
                                                     1 + product_nav_value[0]['amplitude_to'] / 100)).quantize(
                decimal.Decimal('0.00'))

            #  
            return redeem_balance, product_rate, fund_nav, product_nav_value, pay_back_money_min, pay_back_money_max, set_value

        except:
            #  
            pass

    # 根据order_no获取交易请求, 交易订单
    def get_trade_request_by_order_no(self, order_no):

        try:
            db_name = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            sql_query = "SELECT * from %s.CTS_TRADE_REQUEST where ORDER_NO = '%s' ORDER BY id ASC"
            trade_request = self._db.sql_run(sql_query, db_name, order_no)

            return trade_request
        except:

            pass

    # 按绑定的先后顺序，获取用户绑定的普通卡卡号
    def get_cust_all_bank_cards(self, bank_mobile):

        try:
            # step1 获取用户绑定所有银行卡的卡号
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "select distinct card_no from %s.cif_bank_card_info where bank_mobile = '%s' order by id asc"
            cust_bank_cards = self._db.sql_run(sql_query, db_name, bank_mobile)

            return cust_bank_cards
        except Exception, e:

            pass

    # 获取用户优先级最高的绑卡通道的绑卡记录
    def get_bank_card_with_high_priority_bank_channel(self, bank_mobile):

        try:
            cardList = self.get_cust_all_bank_cards(bank_mobile=bank_mobile)
            # 查询每张银行银行卡通道优先级最高的那条记录
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            bank_no = {}
            for i in range(0, len(cardList)):
                sql_qury1 = "select * from %s.cif_bank_card_info where card_no = '%s' order by id asc limit 1"
                bank_no[i] = self._db.sql_run(sql_qury1, db_name, cardList[i]['card_no'])

            return bank_no
        except Exception, e:

            pass

    # 根据卡流水号查找绑卡记录
    def get_bank_card_by_serial_id(self, serial_id):

        try:
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_qury1 = "select * from %s.cif_bank_card_info where serial_id = '%s'"
            bank_card = self._db.sql_run(sql_qury1, db_name, serial_id)

            return bank_card
        except Exception, e:

            pass

    # 工资代发-确认协议
    def get_employee_info(self, employee_id):

        try:
            db_name = 'qydf_uat' if DBC_TAG == 'uat' else 'qydf'
            sql_query1 = "SELECT * FROM %s.qy_df_employee_info WHERE id='%s' "
            employee_info = self._db.sql_run(sql_query1, db_name, employee_id)

            return employee_info
        except:

            pass

    # 会员等级-查询特定用户的会员等级
    def get_my_member_role(self, mobile):

        try:
            # step1
            db_name1 = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query1 = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query1, db_name1, mobile)[0]['cust_no']

            # step2
            db_name = 'points_uat' if DBC_TAG == 'uat' else 'points'
            sql_query1 = "select MEMBER_LEVEL from %s.MEMBER_ACCOUNT where CUST_NO = '%s'"
            my_member_level = self._db.sql_run(sql_query1, db_name, cust_no)

            return my_member_level
        except Exception, e:

            pass

    # 会员等级-查询会员等级
    def get_member_role(self, ):

        try:
            # stp1
            db_name = 'points_uat' if DBC_TAG == 'uat' else 'points'
            sql_query1 = "select CODE from %s.MEMBER_LEVEL order by id asc"
            member_level = self._db.sql_run(sql_query1, db_name)

            return member_level
        except Exception, e:

            pass

    # 会员等级-查询指定等级权益
    def get_member_level_right_list_db(self):
        try:
            # step1 所有等级列表
            member_level = self.get_member_role()

            # step2 获取等级id列表
            level_id = {}
            for i in range(0, len(member_level)):
                db_name = 'points_uat' if DBC_TAG == 'uat' else 'points'
                sql_query2 = "select * from %s.MEMBER_LEVEL where CODE = '%s'"
                level_id[i] = self._db.sql_run(sql_query2, db_name, member_level[i]['CODE'])[0]['id']

            # step3 获取每个等级id对应的权益id
            interest_id_list = {}
            interests_list = {}
            for i in range(0, len(level_id)):
                db_name = 'points_uat' if DBC_TAG == 'uat' else 'points'
                sql_query3 = "select INTERESTS_ID from %s.MEMBER_LEVEL_INTERESTS where LEVEL_ID = '%s' and STATUS ='Y' order by id asc"
                interest_id_list[i] = self._db.sql_run(sql_query3, db_name, level_id[i])
                interest = {}
                for j in range(0, len(interest_id_list[i])):
                    sql_query4 = "select * from %s.MEMBER_INTERESTS where id = '%s'"
                    interest[j] = self._db.sql_run(sql_query4, db_name, interest_id_list[i][j]['INTERESTS_ID'])
                interests_list[i] = interest

            return interests_list
        except Exception, e:

            pass

    # 会员等级-查询指定权益详情
    def get_member_level_right_detail_db(self, code):

        try:
            db_name = 'points_uat' if DBC_TAG == 'uat' else 'points'
            sql_query1 = "select * from %s.MEMBER_INTERESTS where CODE='%s'"
            member_interests = self._db.sql_run(sql_query1, db_name, code)

            return member_interests
        except Exception, e:

            pass

    # 会员等级-查询特殊业务种类
    def get_member_level_category_list_db(self):

        try:
            db_name1 = 'points_uat' if DBC_TAG == 'uat' else 'points'
            sql_query2 = "select * from %s.MEMBER_TYPE order by id asc"
            member_type = self._db.sql_run(sql_query2, db_name1)

            return member_type
        except Exception, e:

            pass

    # 会员等级-查询特殊权益
    def get_member_level_right_category_list_db(self):
        try:
            # step1 获取2种特殊的业务：员工理财，中心联名卡
            db_name1 = 'points_uat' if DBC_TAG == 'uat' else 'points'
            sql_query1 = "select id from %s.MEMBER_TYPE order by id asc"
            type_id = self._db.sql_run(sql_query1, db_name1)

            # step2 获取每种特业务对应的权益ID
            db_name2 = 'points_uat' if DBC_TAG == 'uat' else 'points'
            member_type_interest_list = {}
            for i in range(0, len(type_id)):
                sql_query2 = "select a.INTERESTS_ID from %s.MEMBER_TYPE_INTERESTS a " \
                             "left join %s.MEMBER_INTERESTS b " \
                             "on a.INTERESTS_ID = b.id " \
                             "where a.TYPE_ID='%s' " \
                             "ORDER BY b.ORDER_BY, b.id ASC;"
                member_type_interest_list[i] = self._db.sql_run(sql_query2, db_name2, db_name2, type_id[i]['id'])

            # step3 根据特殊业务的权益ID查询具体权益信息
            db_name3 = 'points_uat' if DBC_TAG == 'uat' else 'points'
            interests_list = {}
            for h in range(0, len(member_type_interest_list)):
                interest = {}
                for j in range(0, len(member_type_interest_list[i])):
                    sql_query4 = "select * from %s.MEMBER_INTERESTS where id = '%s' order by ORDER_BY asc"
                    interest[j] = self._db.sql_run(sql_query4, db_name3,
                                                   member_type_interest_list[h][j]['INTERESTS_ID'])
                interests_list[h] = interest

            return interests_list
        except Exception, e:
            pass

    # 用户-行为记录（提醒我）
    def get_sava_behavior_db(self, mobile):
        # 
        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query1 = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query1, db_name, mobile)[0]['cust_no']

            db_name1 = 'as_uat' if DBC_TAG == 'uat' else 'as'
            sql_query2 = "SELECT * FROM %s.as_cust_behavior where cust_no = '%s' ORDER BY created_at DESC limit 1"
            cust_behavior = self._db.sql_run(sql_query2, db_name1, cust_no)

            return cust_behavior
        except Exception, e:

            pass

    # 工资代发-更新协议状态
    # protocol_status =0（初始状态），1（确认协议），3（终止协议）
    def update_employee_protocol_status(self, protocol_status=None, employee_id=None, mobile=None):
        try:
            db_name = 'qydf_uat' if DBC_TAG == 'uat' else 'qydf'
            # sql_update = "UPDATE %s.qy_df_employee_info set protocol_status ='1' WHERE id=%s;"
            if employee_id is None:
                sql_update = "UPDATE %s.qy_df_employee_info set protocol_status ='%s' WHERE mobile=%s;"
                protocol_status = self._db.sql_run(sql_update, db_name, protocol_status, mobile)
            else:
                sql_update = "UPDATE %s.qy_df_employee_info set protocol_status =%s WHERE id=%s;"
                protocol_status = self._db.sql_run(sql_update, db_name, protocol_status, employee_id)
            return protocol_status
        except:
            pass

    # 获取功能
    def get_function_list(self, function_type):
        try:
            db_name = 'as_uat' if DBC_TAG == 'uat' else 'as'
            sql_query = "SELECT * FROM %s.as_function where function_type='%s' AND is_delete='0' and display_rule='0' and putaway_start_time < sysdate() and putaway_end_time > sysdate() ORDER BY display_order;"
            if function_type == '43':
                sql_query = "SELECT * FROM %s.as_function WHERE function_type = '%s' AND is_delete = '0' AND cust_group is null AND putaway_start_time < sysdate() AND putaway_end_time > sysdate() ORDER BY display_order;"
            function_list = self._db.sql_run(sql_query, db_name, function_type)
            return function_list
        except:
            pass

    # 工资代发-匹配工资卡信息，获取工资卡数量
    def get_match_salary_card(self, employee_id, cert_no):
        try:
            db_name = 'qydf_uat' if DBC_TAG == 'uat' else 'qydf'
            sql_query1 = "SELECT count(1) count FROM %s.qy_df_employee_info WHERE id ='%s' and cert_no ='%s'; "
            employee_count = self._db.sql_run(sql_query1, db_name, employee_id, cert_no)
            return employee_count
        except:
            pass

    # 基金-基金定投详情
    def get_fund_invest_plan_detail_db(self, invest_plan_id=None, validate_phone=None):
        try:
            db_name = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            if validate_phone is None:
                sql_query = "SELECT * FROM %s.CTS_FUND_INVEST_PLAN where PROTOCOL_NO = '%s' ORDER BY created_at DESC limit 1;"
                invest_plan_detail = self._db.sql_run(sql_query, db_name, invest_plan_id)
            else:
                sql_query = "SELECT * FROM %s.CTS_FUND_INVEST_PLAN where VALIDATE_PHONE = '%s' ORDER BY created_at DESC limit 1;"
                invest_plan_detail = self._db.sql_run(sql_query, db_name, validate_phone)
            return invest_plan_detail
        except:
            pass

    # 基金-查询定投基金的基本信息
    def get_fund_detail_db(self, invest_plan_id):
        try:
            product_id = self.get_fund_invest_plan_detail_db(invest_plan_id)[0]['PROD_ID']
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            sql_query = "SELECT * FROM %s.pdc_productinfo where productid = '%s';"
            fund_proinfo = self._db.sql_run(sql_query, db_name, product_id)
            return fund_proinfo
        except:
            pass

    # 账户-查询电子签名约定书信息
    def get_signature_agreement_info_db(self, mobile):
        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query, db_name, mobile)[0]['cust_no']
            db_name1 = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_qury1 = "SELECT * from %s.cif_cust_base where cust_no = '%s';"
            user_signature = self._db.sql_run(sql_qury1, db_name1, cust_no)
            return user_signature
        except:
            pass

    # 获取推荐产品
    def get_recomment_product_list(self, product_type, accept_mode):
        try:
            # step1-先查用户cust_no
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            sql_query = "SELECT p.productid, m.recommended, m.display_order, m.is_archive, m.is_support_points, m.hot, m.accept_mode, i.issue_time, i.dssub_endtime, i.liquidation_time, i.product_expiredtime from %s.pdc_productinfo p, %s.pdc_product_marketing m, %s.pdc_issued_info i WHERE p.productid = m.productid and i.productid = p.productid and m.recommended=1 and m.onsale_flag = 1 and m.is_archive = '0' and p.product_type = '%s' and m.accept_mode = '%s' ORDER BY dssub_endtime DESC ;"
            product_list = self._db.sql_run(sql_query, db_name, db_name, db_name, product_type, accept_mode)

            return product_list
        except:
            pass

    # 获取高端理财频道产品列表
    def get_vip_product_list(self, product_type, accept_mode, is_archive, series_type):
        try:
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            sql_query = "SELECT DISTINCT * from %s.pdc_productinfo p, %s.pdc_product_marketing m where p.productid = m.productid and m.onsale_flag = '1' and m.is_archive = '%s' and m.accept_mode='%s' and p.product_type='%s' and p.series_type='%s';"
            product_list = self._db.sql_run(sql_query, db_name, db_name, is_archive, accept_mode, product_type,
                                            series_type)

            return product_list
        except:
            pass

    # 获取用户极速赎回限额设置
    def get_cust_quota_limit(self, mobile):
        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query, db_name, mobile)[0]['cust_no']

            # step2-查用户的单次/单日/单月限额
            db_name1 = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            sql_query1 = "select * from %s.CTS_CUST_QUOTA_LIMIT where CUST_NO = '%s'"
            quota_limit = self._db.sql_run(sql_query1, db_name1, cust_no)

            return quota_limit
        except:
            pass

    # 获取产品营销信息中除权日极速赎回收费方式
    def get_product_marketing(self, product_id):
        try:
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            sql_query = "select * from %s.pdc_product_marketing where productid = '%s' and accept_mode= 'M';"
            pro_marketing = self._db.sql_run(sql_query, db_name, product_id)
            return pro_marketing
        except:
            pass

    # 查询分红信息
    def get_melon_type_info(self, cust_no, prod_id):
        try:
            db_name = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            sql_query1 = "SELECT * FROM %s.CTS_TRADE_REQUEST WHERE cust_no ='%s' AND apkind = '029' AND prod_id = '%s' ORDER by updated_at DESC limit 1;"
            cts_trade_request = self._db.sql_run(sql_query1, db_name, cust_no, prod_id)
            sql_query2 = "SELECT * FROM %s.CTS_PROD_QUTY WHERE cust_no='%s' AND prod_id = '%s';"
            cts_prod_quty = self._db.sql_run(sql_query2, db_name, cust_no, prod_id)
            return cts_trade_request, cts_prod_quty
        except:
            pass

    # 还贷-还房贷计划创建/修改
    def get_make_plan(self, mobile, repay_plan_id=None):
        try:
            db_name = 'lifeapp_uat' if DBC_TAG == 'uat' else 'la'
            if repay_plan_id is None:
                sql_query1 = "SELECT * FROM %s.la_debit_repay_plan WHERE mobile ='%s' ORDER BY id DESC limit 1;"
                repay_plan_info = self._db.sql_run(sql_query1, db_name, mobile)
            else:
                sql_query1 = "SELECT * FROM %s.la_debit_repay_plan WHERE mobile ='%s' and id ='%s' ORDER BY id DESC limit 1;"
                repay_plan_info = self._db.sql_run(sql_query1, db_name, mobile, repay_plan_id)
            return repay_plan_info
        except:
            pass

    # 还贷-还房贷计划启用/暂停/删除
    def update_plan_status(self, mobile=None, status=None, repay_plan_id=None, repay_type=None, repay_purpose=None,
                           bank_acco=None):
        try:
            db_name = 'lifeapp_uat' if DBC_TAG == 'uat' else 'la'
            if repay_plan_id is None:
                sql_query1 = "SELECT * FROM %s.la_debit_repay_plan WHERE mobile ='%s' ORDER BY id DESC limit 1;"
                repay_plan_id = self._db.sql_run(sql_query1, db_name, mobile)[0]['id']

            if status is not None:
                if repay_type is not None:
                    if repay_purpose is not None:
                        sql_query1 = "UPDATE %s.la_debit_repay_plan SET status='%s',repay_type='%s',repay_purpose='%s' where id =%s;"
                        update_plan = self._db.sql_run(sql_query1, db_name, status, repay_type, repay_purpose,
                                                       repay_plan_id)
                    else:
                        sql_query1 = "UPDATE %s.la_debit_repay_plan SET status='%s',repay_type='%s' where id =%s;"
                        update_plan = self._db.sql_run(sql_query1, db_name, status, repay_type, repay_plan_id)

                    if bank_acco is not None:
                        sql_query1 = "UPDATE %s.la_debit_repay_plan SET status='%s',repay_type='%s', card_no='%s' where id =%s;"
                        update_plan = self._db.sql_run(sql_query1, db_name, status, repay_type, bank_acco,
                                                       repay_plan_id)
                else:
                    sql_query1 = "UPDATE %s.la_debit_repay_plan SET status='%s' where id=%s;"
                    update_plan = self._db.sql_run(sql_query1, db_name, status, repay_plan_id)
            else:
                sql_query1 = "UPDATE %s.la_debit_repay_plan SET status='P' where id =%s;"
                update_plan = self._db.sql_run(sql_query1, db_name, repay_plan_id)

            return update_plan
        except:
            pass

    # 删除所有不必要的还贷计划
    def delete_all_unnecessary_plans(self, id):
        try:
            db_name = 'lifeapp_uat' if DBC_TAG == 'uat' else 'la'
            sql_query1 = "delete from %s.la_debit_repay_plan  where id > %s;"
            self._db.sql_run(sql_query1, db_name, id)

            return
        except:
            pass

    # 删除还贷款计划
    def delete_repay_loan_plan(self, mobile):
        try:
            # step1: 获取刚建立的还贷款计划的id
            db_name = 'lifeapp_uat' if DBC_TAG == 'uat' else 'la'
            sql_query1 = "select * from %s.la_debit_repay_plan  where mobile='%s' order by created_at desc limit 1;"
            id = self._db.sql_run(sql_query1, db_name, mobile)[0]['id']
            serial_no = self._db.sql_run(sql_query1, db_name, mobile)[0]['serial_no']
            # step2: 根据id删除最新的还贷款计划
            sql_query2 = "delete from %s.la_debit_repay_plan where id='%s';"
            self._db.sql_run(sql_query2, db_name, id)

            return serial_no
        except:
            pass

    # 账户-获取登录历史
    def get_login_history(self, mobile):
        _db = DataBase.MySql(GlobalConfig.HuaXinMySql.DBC_BEIDOU)
        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query, db_name, mobile)[0]['cust_no']

            # step2-查询用户登录历史
            db_name1 = 'beidou_uat' if DBC_TAG == 'uat' else 'beidou'
            sql_query1 = "SELECT * FROM %s.milkyuserloginlog WHERE memberId = '%s' ORDER BY time DESC;"
            login_his = _db.sql_run(sql_query1, db_name1, cust_no)
            return login_his
        except Exception, e:
            pass

    # 还贷-还款请求
    def get_repay_request(self, serial_no):
        try:
            db_name = 'lifeapp_uat' if DBC_TAG == 'uat' else 'la'
            sql_query = "SELECT * FROM %s.la_repay_request WHERE serial_no ='%s' ;"
            repay_request = self._db.sql_run(sql_query, db_name, serial_no)
            return repay_request
        except:
            pass

    # 中信联名卡基础校验时落库：中信联名卡申请
    def get_credit_brand_request(self, mobile, brand_type=None, check_state=None, brand_serial_id=None):
        try:
            db_name = 'lifeapp_uat' if DBC_TAG == 'uat' else 'la'
            cust_no = self.get_cust_info('cust_no', '=', mobile)[0]['cust_no']
            if brand_serial_id is None:
                sql_query = "SELECT * FROM %s.la_credit_brand_apply_request WHERE CUST_NO='%s' AND BRAND_TYPE='%s' AND CHECK_STATE='%s' ORDER BY ID DESC LIMIT 1;"
                brand_request = self._db.sql_run(sql_query, db_name, cust_no, brand_type, check_state)
            else:
                sql_query = "SELECT * FROM %s.la_credit_brand_apply_request WHERE CUST_NO='%s' AND serial_no='%s' ORDER BY ID DESC LIMIT 1;"
                brand_request = self._db.sql_run(sql_query, db_name, cust_no, brand_serial_id)

            return brand_request
        except:
            pass

    # 中信联名卡预申请落库:中信联名卡申请信息
    def get_credit_brand_detail(self):
        try:
            db_name = 'lifeapp_uat' if DBC_TAG == 'uat' else 'la'
            sql_query = "SELECT * FROM %s.la_credit_brand_apply_detail ORDER BY ID DESC LIMIT 1;"
            brand_detail = self._db.sql_run(sql_query, db_name)

            return brand_detail
        except:
            pass

    # 积分-我的优惠券列表(V3.1)
    def get_my_coupon_list(self, mobile, status):
        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query, db_name, mobile)[0]['cust_no']

            # step2-查询用户拥有的所有优惠券
            db_name1 = 'points_uat' if DBC_TAG == 'uat' else 'points'
            sql_query1 = "select a.* from %s.COUPON_ECARD a " \
                         "JOIN %s.COUPON_ISSUE b " \
                         "on a.ECARD_NO = b.ECARD_NO " \
                         "where b.CUST_NO = '%s' " \
                         "and STATUS = '%s'" \
                         "order by b.CREATED_AT DESC, a.COUPON_AMOUNT DESC, a.AMOUNT DESC ;"
            coupon_list = self._db.sql_run(sql_query1, db_name1, db_name1, cust_no, status)
            return coupon_list
        except Exception, e:
            pass

    # 消息中心-查询消息分类(V3.1)
    def get_message_category_list(self):
        try:
            # step1 获取消息所有种类
            db_name = 'as_uat' if DBC_TAG == 'uat' else 'as'
            sql_query = "select * from %s.as_msg_category order by id desc;"
            msg_category_list = self._db.sql_run(sql_query, db_name)

            # step2 获取每个消息种类包括的消息
            db_name1 = 'as_uat' if DBC_TAG == 'uat' else 'as'
            now_time = datetime.datetime.now()
            msg_list = {}
            for i in range(0, len(msg_category_list)):
                sql_query1 = "select * from %s.as_msg where category_no = '%s' and expire_time > '%s' order by id desc;"
                msg_list[i] = self._db.sql_run(sql_query1, db_name1, msg_category_list[i]['category_no'], now_time)
            return msg_category_list, msg_list
        except Exception, e:
            pass

    # 消息中心-查询消息列表(V3.1)
    def get_category_message_list_db(self, category_no):
        try:
            # 查询消息详情
            db_name = 'as_uat' if DBC_TAG == 'uat' else 'as'
            now_time = datetime.datetime.now()
            if category_no == '':
                sql_query = "select a.* from %s.as_msg a " \
                            "JOIN %s.as_msg_category b " \
                            "ON a.category_no=b.category_no " \
                            "where expire_time > '%s'" \
                            "ORDER BY a.id DESC ; "
                message_list = self._db.sql_run(sql_query, db_name, db_name, now_time)

            else:
                sql_query = "select a.* from %s.as_msg a " \
                            "JOIN %s.as_msg_category b " \
                            "ON a.category_no=b.category_no " \
                            "where a.category_no = '%s' " \
                            "and expire_time > '%s' " \
                            "ORDER BY a.id DESC ; "
                message_list = self._db.sql_run(sql_query, db_name, db_name, category_no, now_time)
            return message_list
        except Exception, e:
            print e
            pass

    # 工资理财--清除新增的计划
    def delete_salary_financing_plan(self, mobile):
        try:
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query, db_name, mobile)[0]['cust_no']

            db_name = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            sql_query2 = "delete from %s.CTS_FUND_INVEST_PLAN where cust_no='%s' "
            fund_plans = self._db.sql_run(sql_query2, db_name, cust_no)

            return fund_plans
        except Exception, e:
            pass

    # 交易-获取现金管理支付手段
    def get_payment_list(self, mobile):
        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s';"
            cust_no = self._db.sql_run(sql_query, db_name, mobile)[0]['cust_no']

            # step2-获取现金管理支付手段
            db_name1 = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            sql_query1 = "select * from %s.CTS_PROD_QUTY where 1=1 and CUST_NO = '%s' order by PROD_TYPE, PROD_ID;"
            payment_list = self._db.sql_run(sql_query1, db_name1, cust_no)
            return payment_list
        except:
            pass

    # 产品-全部理财产品列表(V3.1)
    def get_all_fin_product_list(self, period_id, product_type_id, min_invest_amt_id):
        try:
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            if period_id == '':
                if min_invest_amt_id == '':
                    if product_type_id == '':
                        sql_qury = "select p.*, b.onsale_status, b.close_period_pic, b.is_redem_anytime, d.invest_period_desc, " \
                                   "d.brief_desc,d.detail_url,b.support_fast_redeem,b.recommended,b.recommend_tags,b.client_type FROM %s.pdc_productinfo p left join %s.pdc_product_detail d " \
                                   "on p.productid = d.productid LEFT JOIN %s.pdc_product_marketing b " \
                                   "on p.productid = b.productid LEFT JOIN %s.pdc_issued_info i on p.productid = i.productid " \
                                   "where b.accept_mode = 'M' and ((d.invest_period_unit = 0 and d.invest_period * 1>=0) " \
                                   "or (d.invest_period_unit = 1 and d.invest_period * 30>=0) " \
                                   "or (d.invest_period_unit = 2 and d.invest_period * 720>=0)) and ((NOW() <= i.dssub_endtime and NOW()>= i.issue_time and " \
                                   "p.min_subscribe_amount >=0.01) or( NOW() >= i.dssub_endtime and p.min_buy_amount >=0.01)); "
                    if product_type_id == '0':
                        sql_qury = "select p.*, b.onsale_status, b.close_period_pic, b.is_redem_anytime, d.invest_period_desc, " \
                                   "d.brief_desc,d.detail_url,b.support_fast_redeem,b.recommended,b.recommend_tags,b.client_type FROM %s.pdc_productinfo p left join %s.pdc_product_detail d on p.productid = d.productid " \
                                   "LEFT JOIN %s.pdc_product_marketing b on p.productid = b.productid LEFT JOIN %s.pdc_issued_info i on p.productid = i.productid " \
                                   "where b.accept_mode = 'M' and ((d.invest_period_unit = 0 and d.invest_period * 1>=0) or (d.invest_period_unit = 1 and d.invest_period * 30>=0) " \
                                   "or (d.invest_period_unit = 2 and d.invest_period * 720>=0)) and ( (NOW() <= i.dssub_endtime and NOW()>= i.issue_time and p.min_subscribe_amount >=0.01) " \
                                   "or(NOW() >= i.dssub_endtime and p.min_buy_amount >=0.01) ) and p.product_type ='1'; "
                    if product_type_id == '1':
                        sql_qury = "select p.*, b.onsale_status, b.close_period_pic, b.is_redem_anytime, d.invest_period_desc, " \
                                   "d.brief_desc,d.detail_url,b.support_fast_redeem,b.recommended,b.recommend_tags,b.client_type FROM %s.pdc_productinfo p left join %s.pdc_product_detail d on p.productid = d.productid " \
                                   "LEFT JOIN %s.pdc_product_marketing b on p.productid = b.productid LEFT JOIN %s.pdc_issued_info i on p.productid = i.productid " \
                                   "where b.accept_mode = 'M' and ((d.invest_period_unit = 0 and d.invest_period * 1>=0) or (d.invest_period_unit = 1 and d.invest_period * 30>=0) " \
                                   "or (d.invest_period_unit = 2 and d.invest_period * 720>=0)) and ( (NOW() <= i.dssub_endtime and NOW()>= i.issue_time and p.min_subscribe_amount >=0.01) " \
                                   "or(NOW() >= i.dssub_endtime and p.min_buy_amount >=0.01) ) and (p.product_type ='3' and p.high_wealth_type = '1'); "
                    if product_type_id == '2':
                        sql_qury = "select p.*, b.onsale_status, b.close_period_pic, b.is_redem_anytime, d.invest_period_desc, " \
                                   "d.brief_desc,d.detail_url,b.support_fast_redeem,b.recommended,b.recommend_tags,b.client_type FROM %s.pdc_productinfo p left join %s.pdc_product_detail d on p.productid = d.productid " \
                                   "LEFT JOIN %s.pdc_product_marketing b on p.productid = b.productid LEFT JOIN %s.pdc_issued_info i on p.productid = i.productid " \
                                   "where b.accept_mode = 'M' and ((d.invest_period_unit = 0 and d.invest_period * 1>=0) or (d.invest_period_unit = 1 and d.invest_period * 30>=0) " \
                                   "or (d.invest_period_unit = 2 and d.invest_period * 720>=0)) and ( (NOW() <= i.dssub_endtime and NOW()>= i.issue_time and p.min_subscribe_amount >=0.01) " \
                                   "or(NOW() >= i.dssub_endtime and p.min_buy_amount >=0.01) ) and (p.product_type ='3' and p.high_wealth_type = '2'); "
                    if product_type_id == '3':
                        sql_qury = "select p.*, b.onsale_status, b.close_period_pic, b.is_redem_anytime, d.invest_period_desc, " \
                                   "d.brief_desc,d.detail_url,b.support_fast_redeem,b.recommended,b.recommend_tags,b.client_type FROM %s.pdc_productinfo p left join %s.pdc_product_detail d on p.productid = d.productid " \
                                   "LEFT JOIN %s.pdc_product_marketing b on p.productid = b.productid LEFT JOIN %s.pdc_issued_info i on p.productid = i.productid " \
                                   "where b.accept_mode = 'M' and ((d.invest_period_unit = 0 and d.invest_period * 1>=0) or (d.invest_period_unit = 1 and d.invest_period * 30>=0) " \
                                   "or (d.invest_period_unit = 2 and d.invest_period * 720>=0)) and ( (NOW() <= i.dssub_endtime and NOW()>= i.issue_time and p.min_subscribe_amount >=0.01) " \
                                   "or(NOW() >= i.dssub_endtime and p.min_buy_amount >=0.01) ) and (p.product_type ='3' and ((p.high_wealth_type = 0 or p.high_wealth_type = 3))); "

            pro_list = self._db.sql_run(sql_qury, db_name, db_name, db_name, db_name)
            return pro_list
        except Exception, e:
            pass

    # 获取产品剩余额度
    def get_left_quota(self, period_id, product_type_id, min_invest_amt_id):
        try:
            db_name1 = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            pro_list = self.get_all_fin_product_list(period_id, product_type_id, min_invest_amt_id)
            left_quota = {}
            for i in range(0, len(pro_list)):
                if i < 10:
                    sql_qury1 = "select * from %s.CTS_PROD_QUOTA_CONTROL where PROD_ID = '%s' and ACCPT_MODE = 'M'"
                    prod_id = pro_list[i]['productid']
                    left_quota[i] = self._db.sql_run(sql_qury1, db_name1, prod_id)
            left_amt = {}
            for i in range(0, len(left_quota)):
                left_amt[i] = decimal.Decimal(left_quota[i][0]['LEFT_QUOTA'])
            left_amt1 = left_amt
            # for j in range(1, len(left_amt1)):
            #     for h in range(0, len(left_amt1)-j):
            #         if left_amt1[h] < left_amt1[h+1]:
            #             t = left_amt1[h]
            #             left_amt1[h]=left_amt1[h+1]
            #             left_amt1[h+1] = t
            return left_amt1
        except Exception, e:
            pass

    # 产品-理财产品介绍(v3.0.0)
    def get_pro_intro(self, user_name, categary_code):
        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query, db_name, user_name)[0]['cust_no']

            # 根据categary_code获取产品介绍详情
            db_name1 = 'as_uat' if DBC_TAG == 'uat' else 'as'
            sql_query1 = "select * from %s.as_dict where categaryCode = '%s' and availability='1' ORDER BY orderNo "
            pro_intro = self._db.sql_run(sql_query1, db_name1, categary_code)
            return pro_intro
        except Exception, e:
            pass

    # 获取投资期限的费率
    def get_max_yield_by_period(self):
        try:
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            query_sql = "SELECT concat(max(y.yield), '%%') max_yield FROM (" \
                        "SELECT CASE WHEN p.high_wealth_type = 1 THEN cast(REPLACE(float_yield, '%%', '') AS DECIMAL(18, 3)) ELSE cast(fixed_yield AS DECIMAL(18, 2)) END AS yield FROM %s.pdc_productinfo p LEFT JOIN %s.pdc_product_detail d ON p.productid = d.productid LEFT JOIN %s.pdc_issued_info i ON p.productid = i.productid WHERE 1 = 1 AND ((d.invest_period_unit = 0 AND d.invest_period * 1) OR (d.invest_period_unit = 1 AND d.invest_period * 30) OR (d.invest_period_unit = 2 AND d.invest_period * 720)) AND ((NOW() <= i.dssub_endtime AND NOW() >= i.issue_time AND p.min_subscribe_amount >= 0.01) OR (NOW() >= i.dssub_endtime AND p.min_buy_amount >= 0.01))) y;"
            get_max_yield = self._db.sql_run(query_sql, db_name, db_name, db_name)
            return get_max_yield
        except:
            pass

    # 交易-高端报价式年化业绩比较基准，获取高端报价式产品的年化收益率和时间
    def get_vip_rate(self, product_id):
        try:
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            query_sql = "SELECT * FROM %s.pdc_yield_cfg WHERE productid = '%s' ORDER BY id DESC;"
            pdc_yield_cfg = self._db.sql_run(query_sql, db_name, product_id)
            return pdc_yield_cfg
        except:
            pass

    # 删除在途
    def delete_asset_in_transit(self, mobile, balance, prod_id=None, prod_name=None):
        try:
            if prod_id is None:
                prod_id = self.get_product_info(product_name=prod_name)[0]['productid']

            cust_no = self.get_cust_info(columns='cust_no', match='=', mobile=mobile)[0]['cust_no']

            db_name = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            query_sql = "delete from %s.CTS_ASSET_IN_TRANSIT where cust_no = '%s' and PROD_ID = '%s' and BALANCE = '%s' order by created_at desc limit 1;"
            delete_record = self._db.sql_run(query_sql, db_name, cust_no, prod_id, balance)

            return delete_record
        except:
            pass

    # 账户-查询修改手机号码审核状态信息
    def get_modify_mobile_check_info(self, user_name):
        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query, db_name, user_name)[0]['cust_no']

            # step2-查用户修改手机号最新的审核记录
            sql_query1 = "select * from %s.cif_mobile_audit where cust_no='%s' ORDER BY created_at DESC LIMIT 1;"
            mobile_audit_list = self._db.sql_run(sql_query1, db_name, cust_no)
            return mobile_audit_list
        except:
            pass

    # 交易-提交(V3.1)
    def get_trade_confirm_db(self, user_name):
        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query, db_name, user_name)[0]['cust_no']

            # step2-查该用户最新的存入订单
            db_name1 = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            sql_query1 = "SELECT * FROM %s.CTS_TRADE_ORDER where CUST_NO='%s' ORDER BY created_at DESC LIMIT 1;"
            trade_order = self._db.sql_run(sql_query1, db_name1, cust_no)

            # step3-查开始计算收益的工作日
            sql_query2 = "SELECT WORK_DATE FROM %s.CTS_WORK_DAYS where WORK_DATE > '%s' and WORK_FLAG = 'Y' order by WORK_DATE ASC limit 1;"
            profit_day1 = self._db.sql_run(sql_query2, db_name1, trade_order[0]['WORK_DATE'])

            # step4-查收益到账日(可以在非工作日)
            sql_query2 = "SELECT WORK_DATE FROM %s.CTS_WORK_DAYS where WORK_DATE > '%s' order by WORK_DATE ASC limit 1;"
            profit_day2 = self._db.sql_run(sql_query2, db_name1, profit_day1[0]['WORK_DATE'])
            return trade_order, profit_day1, profit_day2
        except Exception, e:
            pass

    # 交易-高端报价式产品修改到期处理方式
    def test_modify_expire_dispose_type_db(self, user_name, product_id, value_date):
        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query, db_name, user_name)[0]['cust_no']

            # step2-查份额明细表、查产品滚存表
            db_name1 = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            sql_query1 = "select * from %s.CTS_PROD_QUTY_DETAIL where cust_no = '%s' and prod_id = '%s' and value_date = '%s' order by created_at desc limit 1;"
            sql_query2 = "select * from %s.CTS_PROD_RENEW where cust_no = '%s' and prod_id = '%s' and value_date = '%s' order by updated_at desc limit 1;"
            prod_quty_detail = self._db.sql_run(sql_query1, db_name1, cust_no, product_id, value_date)
            prod_renew = self._db.sql_run(sql_query2, db_name1, cust_no, product_id, value_date)
            return prod_quty_detail, prod_renew
        except Exception, e:
            pass

    # 修改到期日期(为了高端报价式产品持续保持到期5天前的状态)
    def modify_expire_date(self, user_name, product_id, value_date, expired_date):
        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query, db_name, user_name)[0]['cust_no']

            # step2-修改CTS_PROD_QUTY_DETAIL表
            db_name1 = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            sql_query1 = "update %s.CTS_PROD_QUTY_DETAIL set expired_date='%s' where cust_no='%s' and prod_id='%s' and value_date='%s';"
            self._db.sql_run(sql_query1, db_name1, expired_date, cust_no, product_id, value_date)
        except Exception, e:
            pass

    # 获取发放券记录, 返回所有发放记录，按降序排序
    def get_coupon_import_record(self, cust_no, trade_acco):
        try:
            db_name = 'points_uat' if DBC_TAG == 'uat' else 'points'
            sql = "SELECT * from %s.COUPON_IMPORT_RECORD WHERE CUST_NO = '%s' and TRADE_ACCO = '%s' ORDER BY id DESC;"
            coupon_records = self._db.sql_run(sql, db_name, cust_no, trade_acco)

            return coupon_records
        except Exception, e:
            print e

    # 账户-资产证明申请记录
    def get_asset_cert_apply_record(self, user_name):
        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query, db_name, user_name)[0]['cust_no']

            # step2-查资产证明申请记录
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query1 = "select * from %s.cif_asset_certificate where cust_no = '%s' order by created_at asc; "
            asset_cert = self._db.sql_run(sql_query1, db_name, cust_no)
            return asset_cert
        except Exception, e:
            pass

    # 账户-查询我的邀请人
    def query_my_inviter(self, user_name):
        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query, db_name, user_name)[0]['cust_no']
            # step2-查询我的邀请人
            sql_query1 = "SELECT * FROM %s.cif_inviter WHERE cust_no = '%s';"
            inviter_info = self._db.sql_run(sql_query1, db_name, cust_no)
            return inviter_info
        except:
            pass

    # 获取用户绑定的普通卡详细信息
    def get_cust_all_bank_cards_detail(self, bank_mobile):

        try:
            # step1 获取用户绑定所有银行卡的卡号
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "select * from %s.cif_bank_card_info where bank_mobile = '%s' and protocal_exists = '01' GROUP BY card_no"
            cust_bank_cards = self._db.sql_run(sql_query, db_name, bank_mobile)

            return cust_bank_cards
        except Exception, e:

            pass

    # 账户-查询个人账户信息
    def get_account_info(self, user_name):
        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query, db_name, user_name)[0]['cust_no']

            # step2-再查用户积分数量
            db_name1 = 'points_uat' if DBC_TAG == 'uat' else 'points'
            sql_query1 = "select * from %s.POINTS_ACCOUNT where cust_no = '%s';"
            points_amount = self._db.sql_run(sql_query1, db_name1, cust_no)

            # step3-查用户绑定的所有卡
            cards_list = self.get_cust_all_bank_cards_detail(bank_mobile=user_name)

            # step4-查每个卡绑定的通道信息
            db_name2 = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            bank_no_list = {}
            for i in range(0, len(cards_list)):
                sql_query2 = "select * from %s.cif_bank_card_info where card_no = '%s';"
                bank_no_list[i] = self._db.sql_run(sql_query2, db_name2, cards_list[i]['card_no'])

            # step5-查用户绑定的银行卡所属的每个银行优先级最高的通道
            db_name3 = 'be_uat' if DBC_TAG == 'uat' else 'be'
            hightest_bank_no_list = {}
            for i in range(0, len(cards_list)):
                sql_query3 = "select * from %s.be_channel_conf where bank_group_id='%s' and app_recharge='01' and recharge_state = 'Y' and recharge_priority IS NOT null and is_delete='0' ORDER BY recharge_priority ASC limit 1;"
                hightest_bank_no_list[i] = self._db.sql_run(sql_query3, db_name3, cards_list[i]['bank_group_id'])

            # step6-查询待升级的银行卡
            db_name2 = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            card_improve = 0
            for i in range(0, len(bank_no_list)):
                t = 0
                for j in range(0, len(bank_no_list[i])):
                    sql_query4 = "select * from %s.cif_bank_card_info where bank_mobile = '%s' and bank_group_id = '%s' and card_no = '%s' and bank_no!='%s' and id = '%s';"
                    card_im = self._db.sql_run(sql_query4, db_name2, user_name, bank_no_list[i][j]['bank_group_id'],
                                               cards_list[i]['card_no'], hightest_bank_no_list[i][0]['bank_no'],
                                               bank_no_list[i][j]['id'])
                    t = t + len(card_im)
                if t == len(bank_no_list[i]):
                    card_improve = card_improve + 1

            return card_improve, points_amount
        except Exception, e:
            pass

    # 查询质押还款金额
    def get_pldge_amount(self, user_name):
        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query, db_name, user_name)[0]['cust_no']

            # step2-计算质押还款金额
            db_name1 = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            sql_query1 = "select sum(t1.AMOUNT) as amount from %s.CTS_PLEDGE_REPAY_PLAN t1 " \
                         "JOIN %s.CTS_PLEDGE_LOAN t2 on t1.LOAN_ID=t2.ID " \
                         "and t1.STATUS in ('UNPAID','OVERDUE') and t2.STATUS in ('UNPAID','OVERDUE')" \
                         " and t2.CUST_NO = '%s';"

            load_amount = self._db.sql_run(sql_query1, db_name1, db_name1, cust_no)[0]['amount']

            # step3-查询在途金额
            sql_query2 = "select sum(t1.REPAY_AMT) as repay_amt from %s.CTS_PLEDGE_REPAY_RECORD_HIS t1 JOIN %s.CTS_PLEDGE_REPAY_PLAN t2 " \
                         "on t1.REPAY_PLAN_ID = t2.ID where t2.STATUS in ('UNPAID','OVERDUE') " \
                         "and t1.STATUS in ('NEW', 'SUCCESS') and t1.CUST_NO = '%s'"

            transit_amount = self._db.sql_run(sql_query2, db_name1, db_name1, cust_no)[0]['repay_amt']

            if str(load_amount) == 'None':
                total_load_amount = 0
            else:
                if str(transit_amount) == 'None':
                    total_load_amount = load_amount
                else:
                    total_load_amount = load_amount - transit_amount

            return total_load_amount
        except Exception, e:
            pass

    # 查询待激活的卡
    def get_activate_card_count(self, user_name):
        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT * FROM %s.cif_cust_base where mobile = '%s'"
            cust_base = self._db.sql_run(sql_query, db_name, user_name)[0]

            # step2-查询待激活的卡
            db_name1 = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query1 = "select DISTINCT card_no from %s.cif_bank_card_info where protocal_exists != '01' and cust_no = '%s';"
            activate_list1 = self._db.sql_run(sql_query1, db_name1, cust_base['cust_no'])

            db_name1 = 'qydf_uat' if DBC_TAG == 'uat' else 'qydf'
            sql_query2 = "select DISTINCT card_no from %s.qy_df_employee_info where mobile='%s' and cert_no='%s'; "
            activate_list2 = self._db.sql_run(sql_query2, db_name1, user_name, cust_base['cert_no'])

            return len(activate_list1) + len(activate_list2)
        except Exception, e:
            pass

    # 账户-修改用户基本信息
    def update_cust_base_info(self, user_name):
        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query, db_name, user_name)[0]['cust_no']

            # 查询用户基本信息
            sql_query1 = "select * from %s.cif_cust_detail where cust_no = '%s'; "
            sql_query2 = "select * from %s.cif_address where cust_no='%s' ORDER BY created_at DESC LIMIT 1;"
            cust_detail = self._db.sql_run(sql_query1, db_name, cust_no)
            cust_address = self._db.sql_run(sql_query2, db_name, cust_no)
            return cust_detail, cust_address
        except Exception, e:
            pass

    # 质押还款计划表
    def get_pledge_replay_plan(self, user_name):
        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT * FROM %s.cif_cust_base where mobile = '%s'"
            cust_base = self._db.sql_run(sql_query, db_name, user_name)[0]

            # step2-根据cust查loan_id
            db_name1 = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            sql_query1 = "SELECT * FROM %s.CTS_PLEDGE_LOAN WHERE CUST_NO='%s' ORDER BY ID DESC limit 1;"
            pledge_loan = self._db.sql_run(sql_query1, db_name1, cust_base['cust_no'])[0]

            # step3-根据loan_id查质押还款计划表
            sql_query2 = "SELECT * FROM %s.CTS_PLEDGE_REPAY_PLAN WHERE LOAN_ID='%s' ORDER BY ID DESC ;"
            pledge_replay_plan = self._db.sql_run(sql_query2, db_name1, pledge_loan['ID'])

            return pledge_replay_plan
        except:
            pass

    # 质押还款记录表
    def pledge_repay_record(self, user_name):
        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT * FROM %s.cif_cust_base where mobile = '%s'"
            cust_base = self._db.sql_run(sql_query, db_name, user_name)[0]

            # step2-根据cust_no查质押还款记录表
            db_name1 = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            sql_query2 = "SELECT * FROM %s.CTS_PLEDGE_REPAY_RECORD WHERE CUST_NO='%s' ORDER BY ID DESC ;"
            pledge_replay_record = self._db.sql_run(sql_query2, db_name1, cust_base['cust_no'])
            return pledge_replay_record
        except:
            pass

    # 中信联名卡信息表
    def get_credit_ecitic_brand_card(self, user_name):
        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT * FROM %s.cif_cust_base where mobile = '%s'"
            cust_base = self._db.sql_run(sql_query, db_name, user_name)[0]

            # step2-根据cust_no查中信联名卡信息表
            db_name1 = 'lifeapp_uat' if DBC_TAG == 'uat' else 'la'
            sql_query2 = "SELECT * FROM %s.la_credit_ecitic_brand_card WHERE CUST_NO='%s' ORDER BY ID DESC limit 1;"
            credit_ecitic_brand_card = self._db.sql_run(sql_query2, db_name1, cust_base['cust_no'])
            return credit_ecitic_brand_card
        except:
            pass

    # 更新联名卡的状态为未激活
    def update_ecitic_active_status(self, user_name):
        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT * FROM %s.cif_cust_base where mobile = '%s'"
            cust_base = self._db.sql_run(sql_query, db_name, user_name)[0]

            # 更新状态，0 未激活 ； 1 激活
            db_name1 = 'lifeapp_uat' if DBC_TAG == 'uat' else 'la'
            sql_update = "UPDATE %s.la_credit_ecitic_brand_card set is_active='0' WHERE CUST_NO='%s';"
            update_ecitic_active_status = self._db.sql_run(sql_update, db_name1, cust_base['cust_no'])
            return update_ecitic_active_status
        except:
            pass

    # 交易-质押还款明细
    def get_loan_repay_detail_list(self, user_name, my_loan_id):
        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query, db_name, user_name)[0]['cust_no']

            # step2-查询质押还款明细
            db_name1 = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            sql_query1 = "select * from %s.CTS_PLEDGE_LOAN where ORDER_NO = '%s'"
            pledge_loan = self._db.sql_run(sql_query1, db_name1, my_loan_id)

            sql_query2 = "select * from %s.CTS_PLEDGE_REPAY_RECORD where LOAN_ID = '%s' and CUST_NO = '%s'; "
            pledge_repay_record = self._db.sql_run(sql_query2, db_name1, pledge_loan[0]['ID'], cust_no)
            if pledge_repay_record == []:
                sql_query3 = "select * from %s.CTS_PLEDGE_REPAY_RECORD_HIS where LOAN_ID = '%s' and CUST_NO = '%s' ORDER BY ID DESC; "
                pledge_repay_record = self._db.sql_run(sql_query3, db_name1, pledge_loan[0]['ID'], cust_no)
            return pledge_repay_record
        except:
            pass

    # 基金-极速赎回说明
    def get_fast_redeem_info(self, fund_id):
        try:
            # step1-查产品极速赎回变现比
            db_name1 = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            sql_query = "select * from %s.pdc_productinfo where productid = '%s' ;"
            sql_query1 = "select * from %s.pdc_product_marketing where productid = '%s' ;"
            pdc_latest_nav = self._db.sql_run(sql_query, db_name1, fund_id)
            pdc_marketing = self._db.sql_run(sql_query1, db_name1, fund_id)

            return pdc_latest_nav, pdc_marketing
        except:
            pass

    # 获取质押已还本金
    def get_loan_repay_amt(self, user_name):
        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT * FROM %s.cif_cust_base where mobile = '%s'"
            cust_base = self._db.sql_run(sql_query, db_name, user_name)[0]

            # step2-根据cust_no查loan_id
            db_name1 = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            sql_query1 = "SELECT * FROM %s.CTS_PLEDGE_LOAN WHERE CUST_NO='%s' ORDER BY ID DESC limit 1;"
            pledge_loan = self._db.sql_run(sql_query1, db_name1, cust_base['cust_no'])[0]

            # 求和 - 已还本金
            sql_query2 = "SELECT sum(REPAY_AMT) sum_repay FROM %s.CTS_PLEDGE_REPAY_RECORD_HIS WHERE CUST_NO='%s' and LOAN_ID='%s' ORDER BY ID DESC ;"
            loan_repay_amt = self._db.sql_run(sql_query2, db_name1, cust_base['cust_no'], pledge_loan['ID'])[0]
            if loan_repay_amt['sum_repay'] is None:
                remain_loan_amt = pledge_loan['PLEDGE_AMT']
            # 剩余借款本金 = 借款金额 - 已还本金
            else:
                remain_loan_amt = pledge_loan['PLEDGE_AMT'] - loan_repay_amt['sum_repay']

            return pledge_loan, loan_repay_amt, remain_loan_amt
        except:
            pass

    # 日期是否是工作日
    def determine_if_work_day(self, date):
        try:
            db_name = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            sql_query = "select * from %s.CTS_WORK_DAYS where WORK_DATE = '%s';"
            day = self._db.sql_run(sql_query, db_name, date)
            if str(day[0]['WORK_FLAG']) == 'Y':
                work_day = True
            else:
                work_day = False
            return work_day
        except:
            pass

    # 获取cts下一个工作日
    def get_next_work_date(self, pre_work_date):
        try:
            # 查下一个工作日
            db_name1 = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            sql_query1 = "SELECT WORK_DATE FROM %s.CTS_WORK_DAYS where WORK_DATE > '%s' and WORK_FLAG = 'Y' order by WORK_DATE ASC limit 1;"
            next_work_date = self._db.sql_run(sql_query1, db_name1, pre_work_date)
            return next_work_date
        except:
            pass

    # 判断某日是否是工作日,如果不是获取下一个最近工作日
    def judge_is_work_date(self, day):
        try:
            db_name1 = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            sql_query1 = "SELECT WORK_DATE FROM %s.CTS_WORK_DAYS where WORK_DATE >= '%s' and WORK_FLAG = 'Y' order by WORK_DATE ASC limit 1;"
            new_work_date = self._db.sql_run(sql_query1, db_name1, day)
            return new_work_date
        except:
            pass

    # 获取任意自然日的前一个工作日
    def get_pre_work_date(self, work_day):
        try:
            # 查上一个工作日
            db_name1 = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            sql_query1 = "SELECT WORK_DATE FROM %s.CTS_WORK_DAYS where WORK_DATE < '%s' and WORK_FLAG = 'Y' order by WORK_DATE DESC limit 1;"
            pre_work_date = self._db.sql_run(sql_query1, db_name1, work_day)
            return pre_work_date
        except:
            pass

    # 信用卡银行通道列表
    def get_credit_bank_channel(self, group_id):
        try:
            # step-1 查询la库信用卡通道
            db_name1 = 'lifeapp_uat' if DBC_TAG == 'uat' else 'la'
            sql_query = "SELECT * FROM %s.la_credit_bank_channel ORDER BY bank_no;"
            credit_bank_channel = self._db.sql_run(sql_query, db_name1)

            # step-2 查询be库银行卡通道
            db_name2 = 'be_uat' if DBC_TAG == 'uat' else 'be'
            sql_query1 = "SELECT * FROM %s.be_channel_conf WHERE is_credit='Y' ORDER BY bank_group_id;"
            be_channel_conf = self._db.sql_run(sql_query1, db_name2)

            # 查询银行卡的名称
            sql_query2 = "SELECT group_name FROM %s.be_bank_group where group_id = '%s';"
            group_name = self._db.sql_run(sql_query2, db_name2, group_id)
            return credit_bank_channel, be_channel_conf, group_name
        except:
            pass

    # 获取积分发放事件规则
    def get_points_issue_event_rule(self):
        try:
            db_name = 'points_uat' if DBC_TAG == 'uat' else 'points'
            sql_query = "SELECT * FROM %s.POINTS_ISSUE_EVENT_RULE WHERE DISPLAY = 'Y' ORDER BY ORDER_BY ASC ;"
            points_issue_event_rule = self._db.sql_run(sql_query, db_name)
            return points_issue_event_rule
        except:
            pass

    # 获取积分方法和积分消费详情
    def get_points_detail(self, user_name):
        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT * FROM %s.cif_cust_base where mobile = '%s'"
            cust_base = self._db.sql_run(sql_query, db_name, user_name)[0]

            # step2-根据custNo查询用户积分发放
            db_name1 = 'points_uat' if DBC_TAG == 'uat' else 'points'
            sql_query1 = "SELECT * FROM %s.POINTS_ACCOUNT WHERE CUST_NO='%s';"
            points_account = self._db.sql_run(sql_query1, db_name1, cust_base['cust_no'])

            sql_query2 = "SELECT * FROM %s.POINTS_ACCOUNT_HIS WHERE CUST_NO='%s' AND POINT_TYPE = 'ISSUE';"
            issue_points_account_his = self._db.sql_run(sql_query2, db_name1, cust_base['cust_no'])

            # step3-根据积分方法id查询积分消费明细
            sql_query3 = "SELECT * FROM %s.POINTS_ACCOUNT_HIS WHERE CUST_NO='%s' AND POINT_TYPE = 'CONSUME';"
            consume_points_account_his = self._db.sql_run(sql_query3, db_name1, cust_base['cust_no'])
            return points_account, issue_points_account_his, consume_points_account_his
        except:
            pass

    # 获取积分抵扣规则
    def get_points_deducte_rule(self):
        try:
            db_name1 = 'points_uat' if DBC_TAG == 'uat' else 'points'
            sql_query1 = "SELECT * FROM %s.POINTS_DEDUCTE_RULE ;"
            points_deducte_rule = self._db.sql_run(sql_query1, db_name1)
            return points_deducte_rule
        except:
            pass

    # 查询预约申请记录
    def get_apply_reservation_code(self, user_name, product_id):
        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query, db_name, user_name)[0]['cust_no']

            db_name1 = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            sql_query1 = "select * from %s.CTS_PROD_RESERVE_APPLY where PROD_ID='%s' and CUST_NO= '%s';"
            apply_list = self._db.sql_run(sql_query1, db_name1, product_id, cust_no)
            return apply_list
        except:
            pass

    # 删除预约申请记录
    def delete_apply_reservation_code(self, user_name, product_id):
        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query, db_name, user_name)[0]['cust_no']

            db_name1 = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            sql_query1 = "delete from %s.CTS_PROD_RESERVE_APPLY where PROD_ID='%s' and CUST_NO='%s';"
            self._db.sql_run(sql_query1, db_name1, product_id, cust_no)
        except:
            pass

    # 产品预售信息
    def get_product_presale(self, product_id):
        try:
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            sql_query = "select * from %s.pdc_product_presale where productid='%s';"
            product_presale = self._db.sql_run(sql_query, db_name, product_id)
            return product_presale
        except:
            pass

    # 获取APP热门产品（排除已售罄）
    def get_hot_on_saling_product_list(self, product_type):
        try:
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            sql = "SELECT DISTINCT * FROM %s.pdc_product_marketing m ,%s.pdc_productinfo p ,%s.pdc_issued_info n " \
                  "where m.productid = p.productid and p.productid=n.productid and hot = '1' and p.product_type = '%s' " \
                  "and m.accept_mode = 'M' and m.onsale_flag = '1' and n.product_status !=2 ORDER BY n.issue_time;"
            hot_product_list = self._db.sql_run(sql, db_name, db_name, db_name, product_type)
            return hot_product_list
        except:
            pass

    # 根据指定coupon_batch_id查找客户的该种可使用优惠券
    # prod_type_scope_val 是指支持的产品类型，coupon_batch_id是指券种类id标识
    def get_coupon_count_new(self, mobile, amount, prod_type_scope_val, prod_id, coupon_batch_id):

        try:
            cust_no = self.get_cust_info(columns='cust_no', match='=', mobile=mobile)[0]['cust_no']
            points_db_name = 'points_uat' if DBC_TAG == 'uat' else 'points'
            sql_coupon_account = "select * from %s.COUPON_ISSUE i,%s.COUPON_ECARD c where i.ECARD_NO=c.ECARD_NO and i.CUST_NO='%s' and c.status='ISSUE' and c.start_at<SYSDATE() and c.end_at>SYSDATE() and COUPON_BATCH_ID in (SELECT DISTINCT COUPON_BATCH_ID from %s.COUPON_BATCH_SCOPE WHERE SCOPE_VAL in (%s) or SCOPE_VAL='%s' and STATUS='Y') ORDER BY AMOUNT DESC, COUPON_ACCOUNT_HIS_ID ASC"
            coupon_count = self._db.sql_run(sql_coupon_account, points_db_name, points_db_name, cust_no, points_db_name,
                                            prod_type_scope_val, prod_id)

            sql_coupon_available = "select * from %s.COUPON_ISSUE i,%s.COUPON_ECARD c where i.ECARD_NO=c.ECARD_NO and i.CUST_NO='%s' and c.status='ISSUE' and c.start_at<SYSDATE() and c.end_at>SYSDATE() and COUPON_AMOUNT <= %s and COUPON_BATCH_ID = '%s' ORDER BY c.CREATED_AT DESC; "
            coupon_available = self._db.sql_run(sql_coupon_available, points_db_name, points_db_name, cust_no, amount,
                                                coupon_batch_id)

            sql_coupon_not_used = "select * from %s.COUPON_ISSUE i,%s.COUPON_ECARD c where i.ECARD_NO=c.ECARD_NO and i.CUST_NO='%s' and c.status='ISSUE' and c.start_at<SYSDATE() and c.end_at>SYSDATE() and (COUPON_AMOUNT > %s and COUPON_BATCH_ID in (SELECT DISTINCT COUPON_BATCH_ID from %s.COUPON_BATCH_SCOPE WHERE SCOPE_VAL in (%s) or SCOPE_VAL='%s' and STATUS='Y')) ORDER BY AMOUNT DESC, COUPON_ACCOUNT_HIS_ID ASC"
            coupon_not_used = self._db.sql_run(sql_coupon_not_used, points_db_name, points_db_name, cust_no, amount,
                                               points_db_name, prod_type_scope_val, prod_id)

            return coupon_count, coupon_available, coupon_not_used
        except:
            pass

    # 基金-公告列表
    def get_fund_notice_list(self, fund_id, notice_type):
        try:
            db_name1 = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            if str(notice_type) == '-1':
                sql_query = "select * from %s.pdc_fund_announcement where fund_id='%s' and fin_id IS NOT NULL ORDER BY bulletin_date DESC ;"
                notice_list = self._db.sql_run(sql_query, db_name1, fund_id)
            else:
                sql_query = "select * from %s.pdc_fund_announcement where fund_id='%s' and bulletin_type='%s' and fin_id IS NOT NULL ORDER BY bulletin_date DESC ;"
                notice_list = self._db.sql_run(sql_query, db_name1, fund_id, notice_type)
            return notice_list
        except:
            pass

    # 产品-搜索定期或高端
    def get_search_fin_product(self, keyword):
        try:
            db_name1 = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            sql_query = "select a.productid, a.product_no, a.product_type, a.product_short_name,a.product_pinyin, " \
                        "case when a.product_type = 3 and a.high_wealth_type = 2 then " \
                        "CONCAT(cast(a.fixed_yield as decimal(8,2)),'%%') " \
                        "when a.product_type = 3 and a.high_wealth_type = 1 then " \
                        "(case when (select issue_time from %s.pdc_issued_info where productid=a.productid) <= NOW() " \
                        "and (select dssub_endtime from %s.pdc_issued_info where productid= a.productid) > NOW() " \
                        "then '--' else (select CONCAT(cast(yield as decimal(8,3)),'%%%%') from %s.pdc_nav n where " \
                        "n.fundid=a.product_no order by n.nav_date desc limit 1) end) " \
                        "when a.product_type = 3 and a.high_wealth_type != 2 and a.high_wealth_type != 1 then " \
                        "cast(a.latest_nav as decimal(8,4)) " \
                        "when a.product_type = 1 then CONCAT(cast(a.fixed_yield as decimal(8,2)),'%%%%') " \
                        "end as product_yield, " \
                        "case when a.product_type = 3 and a.high_wealth_type = 2 then '年化业绩比较基准' " \
                        "when a.product_type = 3 and a.high_wealth_type = 1 then '七日年化收益率' " \
                        "when a.product_type = 3 and a.high_wealth_type != 2 and a.high_wealth_type != 1 THEN '单位净值' " \
                        "when a.product_type = 1 then '年化业绩比较基准' " \
                        "end as product_yield_des " \
                        "from %s.pdc_productinfo a join %s.pdc_product_marketing b on a.productid=b.productid " \
                        "where b.onsale_flag=1 " \
                        "AND b.accept_mode = 'M' AND product_type in(1,3) " \
                        "AND ( " \
                        "a.product_short_name LIKE '%%%s%%' " \
                        "OR a.product_pinyin LIKE '%%%s%%' " \
                        ") " \
                        "order by a.product_type desc;"

            product_list = self._db.sql_run(sql_query, db_name1, db_name1, db_name1, db_name1, db_name1,
                                            keyword, keyword)
            return product_list
        except:
            pass

    # 获取产品剩余额度
    def get_prod_left_quota(self, product_id):
        try:
            db_name = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            sql_query = "select * from %s.CTS_PROD_QUOTA_CONTROL where PROD_ID = '%s' and ACCPT_MODE = 'M'"
            left_quota = self._db.sql_run(sql_query, db_name, product_id)
            return left_quota
        except:
            pass

    # 基金-热搜关键词
    def get_fund_hot_keys(self):
        try:
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            sql_query = "SELECT * FROM %s.pdc_hot_keywords WHERE is_delete ='0' ORDER BY display_order ;"
            fund_hot_keys = self._db.sql_run(sql_query, db_name)
            return fund_hot_keys
        except:
            pass

    # 基金-基金经理看好情况
    def get_support_detail(self, user_name, fund_manager_id):
        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query, db_name, user_name)[0]['cust_no']

            db_name1 = 'as_uat' if DBC_TAG == 'uat' else 'as'
            sql_query1 = "select * from %s.as_cust_favorite where cust_no='%s' and object_id='%s' and type='0' and is_delete='0';"
            cust_fav_list = self._db.sql_run(sql_query1, db_name1, cust_no, fund_manager_id)
            return cust_fav_list
        except:
            pass

    # 基金-分红和拆分
    def get_share_and_split(self, fund_id):
        try:
            # step1-先查用户cust_no
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            sql_query = "select * from %s.pdc_dividend_split where productid='%s' ORDER BY register_date DESC ;"
            div_split_list = self._db.sql_run(sql_query, db_name, fund_id)
            return div_split_list
        except:
            pass

    # 查询基金涨幅信息
    def get_fund_rise_amplitude(self, fund_id):
        try:
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            sql_query = "SELECT * FROM %s.pdc_fund_rise_amplitude where productid ='%s' ORDER BY change_pct_date DESC ;"
            fund_rise_amplitude = self._db.sql_run(sql_query, db_name, fund_id)
            return fund_rise_amplitude
        except:
            pass

    # 根据code查询通用配置结果
    def get_common_config_by_code(self, key):
        try:
            db_name = 'as_uat' if DBC_TAG == 'uat' else 'as'
            sql_query = "select * from %s.as_dict where code = '%s';"
            key_list = self._db.sql_run(sql_query, db_name, key)
            return key_list
        except:
            pass

    # 根据mobile获取用户信息
    def get_cust_base(self, user_name):
        try:
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "select * from %s.cif_cust_base where mobile = '%s';"
            cust_base = self._db.sql_run(sql_query, db_name, user_name)
            return cust_base
        except:
            pass

    # 根据产品id获取产品详情
    def get_product_detail(self, productid):
        try:
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            sql_query = "select * from %s.pdc_product_detail where productid='%s';"
            product_detail = self._db.sql_run(sql_query, db_name, productid)
            return product_detail
        except:
            pass

    # 基金-定投排行
    def get_find_invest_yield_product(self, fund_type, period_type, sort_type, order_desc):
        try:
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            # 按照定投周期分段
            if str(sort_type) == '0':
                # 按照结果排序类型分段
                if str(order_desc) == '0':
                    sql_query = "select b.productid,a.product_full_name,a.product_short_name,a.product_no,a.fund_income_unit," \
                                "a.daily_return, a.float_yield, a.fund_type,a.latest_nav,a.latest_nav_date,c.is_new_issue, " \
                                "b.week_invest_yield,b.week_invest_count,b.month_invest_yield,b.month_invest_count " \
                                "from  %s.pdc_productinfo a left join %s.pdc_product_marketing c on a.productid = c.productid " \
                                "join %s.pdc_fund_invest_yield b on a.productid = b.productid " \
                                "join (select productid,change_type from %s.pdc_issued_suspension  where bus_type = 3 and " \
                                "is_delete = 1 AND ( change_type = 17 OR change_type = 19 ) and " \
                                "change_date != '1900-01-01 00:00:00') s on " \
                                "a.productid = s.productid where a.fund_type='%s' " \
                                "and b.period_type='%s' and b.is_show = 1 and c.accept_mode='M' and c.onsale_flag = 1 " \
                                "and c.is_sale = 1 and c.support_invest_regularly=1 " \
                                "ORDER BY b.week_invest_yield, b.month_invest_yield, a.productid;"
                if str(order_desc) == '1':
                    sql_query = "select b.productid,a.product_full_name,a.product_short_name,a.product_no,a.fund_income_unit," \
                                "a.daily_return, a.float_yield, a.fund_type,a.latest_nav,a.latest_nav_date,c.is_new_issue, " \
                                "b.week_invest_yield,b.week_invest_count,b.month_invest_yield,b.month_invest_count " \
                                "from  %s.pdc_productinfo a left join %s.pdc_product_marketing c on a.productid = c.productid " \
                                "join %s.pdc_fund_invest_yield b on a.productid = b.productid " \
                                "join (select productid,change_type from %s.pdc_issued_suspension  where bus_type = 3 and " \
                                "is_delete = 1 AND ( change_type = 17 OR change_type = 19 ) and " \
                                "change_date != '1900-01-01 00:00:00') s on " \
                                "a.productid = s.productid where a.fund_type='%s' " \
                                "and b.period_type='%s' and b.is_show = 1 and c.accept_mode='M' and c.onsale_flag = 1 " \
                                "and c.is_sale = 1 and c.support_invest_regularly=1 " \
                                "ORDER BY b.week_invest_yield desc, b.month_invest_yield desc,a.productid desc;"
            if str(sort_type) == '1':
                if str(order_desc) == '0':
                    sql_query = "select b.productid,a.product_full_name,a.product_short_name,a.product_no,a.fund_income_unit," \
                                "a.daily_return, a.float_yield, a.fund_type,a.latest_nav,a.latest_nav_date,c.is_new_issue, " \
                                "b.week_invest_yield,b.week_invest_count,b.month_invest_yield,b.month_invest_count " \
                                "from  %s.pdc_productinfo a left join %s.pdc_product_marketing c on a.productid = c.productid " \
                                "join %s.pdc_fund_invest_yield b on a.productid = b.productid " \
                                "join (select productid,change_type from %s.pdc_issued_suspension  where bus_type = 3 and " \
                                "is_delete = 1 AND ( change_type = 17 OR change_type = 19 ) and " \
                                "change_date != '1900-01-01 00:00:00') s on " \
                                "a.productid = s.productid where a.fund_type='%s' " \
                                "and b.period_type='%s' and b.is_show = 1 and c.accept_mode='M' and c.onsale_flag = 1 " \
                                "and c.is_sale = 1 and c.support_invest_regularly=1 " \
                                "ORDER BY b.month_invest_yield , b.week_invest_yield ,a.productid;"
                if str(order_desc) == '1':
                    sql_query = "select b.productid,a.product_full_name,a.product_short_name,a.product_no,a.fund_income_unit," \
                                "a.daily_return, a.float_yield, a.fund_type,a.latest_nav,a.latest_nav_date,c.is_new_issue, " \
                                "b.week_invest_yield,b.week_invest_count,b.month_invest_yield,b.month_invest_count " \
                                "from  %s.pdc_productinfo a left join %s.pdc_product_marketing c on a.productid = c.productid " \
                                "join %s.pdc_fund_invest_yield b on a.productid = b.productid " \
                                "join (select productid,change_type from %s.pdc_issued_suspension where bus_type = 3 and " \
                                "is_delete = 1 AND ( change_type = 17 OR change_type = 19 ) and " \
                                "change_date != '1900-01-01 00:00:00') s on " \
                                "a.productid = s.productid where a.fund_type='%s' " \
                                "and b.period_type='%s'and b.is_show = 1 and c.accept_mode='M' and c.onsale_flag = 1 " \
                                "and c.is_sale = 1 and c.support_invest_regularly=1 " \
                                "ORDER BY b.month_invest_yield desc, b.week_invest_yield desc,a.productid desc;"

            find_invest_yield_product_list = self._db.sql_run(sql_query, db_name, db_name, db_name, db_name,
                                                              fund_type, period_type)
            return find_invest_yield_product_list
        except:
            pass

    # 获取精选基金
    def get_fund_best_choices_list(self):
        try:
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            sql_query = "select a.product_full_name,a.productid,a.product_no,a.product_short_name,a.fund_type,c.detail_url,r.rate_star, weekly_return as riseAmplitude from %s.pdc_productinfo a " \
                        "join %s.pdc_product_marketing b on a.productid=b.productid left join %s.pdc_product_detail c on a.productid=c.productid " \
                        "left join (select rate_star,productid from %s.pdc_fund_rate where rate_agency_code ='organizationCode') r on a.productid = r.productid " \
                        "where product_type = 2 and b.accept_mode = 'M' and b.recommended = 1 and b.onsale_flag = 1 and b.is_sale = 1 order by weekly_return desc;"
            fund_best_choices_list = self._db.sql_run(sql_query, db_name, db_name, db_name, db_name)
            return fund_best_choices_list
        except:
            pass

    # 通用-获取基金枚举值
    def get_fund_enum_list(self):
        try:
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            sql_query = "SELECT * FROM %s.pdc_product_cfg where cfg_type ='1';"
            fund_enum_list = self._db.sql_run(sql_query, db_name)
            return fund_enum_list
        except:
            pass

    # 获取首页和理财页模块信息
    def get_modlue_list(self):
        try:
            db_name = 'as_uat' if DBC_TAG == 'uat' else 'as'
            sql_query = "SELECT * FROM %s.as_module where name ='我的理财日历';"
            module_list = self._db.sql_run(sql_query, db_name)
            return module_list
        except:
            pass

    # 静态份额表更新新增份额
    def insert_prod_quty(self, user_name, product_id, amt):
        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query, db_name, user_name)[0]['cust_no']

            # step2-根据产品查询相应份额
            db_name1 = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            sql_query1 = "select balance from %s.CTS_PROD_QUTY where cust_no = '%s' and prod_id='%s';"
            balance = self._db.sql_run(sql_query1, db_name1, cust_no, product_id)[0]
            new_balance = balance['balance'] + decimal.Decimal(amt)

            # 插入新份额
            sql_query1 = "update %s.CTS_PROD_QUTY set balance = '%s' where cust_no = '%s' and prod_id='%s';"
            self._db.sql_run(sql_query1, db_name1, new_balance, cust_no, product_id)
        except:
            pass

    # 理财日历
    def get_noc(self, user_name):
        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query, db_name, user_name)[0]['cust_no']

            # step2-查询用户相应的理财日历
            db_name1 = 'noc_uat' if DBC_TAG == 'uat' else 'noc'
            sql_query1 = "select * from %s.NOC_BUILDER where cust_no='%s';"
            noc = self._db.sql_run(sql_query1, db_name1, cust_no)

            # step3-查询模板内容
            sql_query2 = "select * from %s.NOC_TEMPLATE where id='%s';"
            template = self._db.sql_run(sql_query2, db_name1, noc[0]['TEMPLATE_ID'])
            return noc, template
        except:
            pass

    # 删除noc_builder中的非法数据
    def delete_noc_builder_useless_data(self, user_name, type=None, order_serial_no_delete='0'):
        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query, db_name, user_name)[0]['cust_no']

            order_serial_no = order_serial_no_delete
            if type == 'reserve_pay':
                # step2-查询用户相应的预约还款记录状态为'N'的order_serial_no
                db_name = 'lifeapp_uat' if DBC_TAG == 'uat' else 'la'
                sql_query = "select * from %s.la_credit_repay_order where cust_no = '%s' and state='N' ORDER BY id desc "
                order_serial_no = self._db.sql_run(sql_query, db_name, cust_no)[0]['order_serial_no']
                # step3-将用户相应的预约还款记录状态为'N'的数据改为'C'
                self.update_creditcard_order_state(card_id='422', orign_state='N', update_state='C')

            # step4-删除noc_builder中的相应的非法数据
            db_name1 = 'noc_uat' if DBC_TAG == 'uat' else 'noc'
            sql_query2 = "delete from %s.NOC_BUILDER where OUTER_KEY='%s';"
            self._db.sql_run(sql_query2, db_name1, order_serial_no)
        except:
            pass

    # 获取优惠券批次
    def get_coupon_batch(self, code):
        try:
            db_name1 = 'points_uat' if DBC_TAG == 'uat' else 'points'
            sql_query1 = "SELECT * FROM %s.COUPON_BATCH WHERE CODE='%s' ORDER BY id DESC;"
            coupon_batch = self._db.sql_run(sql_query1, db_name1, code)
            return coupon_batch
        except:
            pass

    # 获取高端货币类历史收益
    def get_vip_product_history_profit(self, product_id):
        try:
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            sql_query = "select n.* from %s.pdc_nav n join %s.pdc_productinfo p on n.fundid=p.product_no " \
                        "left JOIN %s.pdc_fund_rise_amplitude f on f.productid=p.productid and " \
                        "f.change_pct_date=n.nav_date where fundid='%s' order by nav_datetime DESC ;"
            his_profit = self._db.sql_run(sql_query, db_name, db_name, db_name, str(product_id).split('#')[1])
            return his_profit
        except:
            pass

    # 获取高端投资目标
    def get_highend_detail(self, product_id):
        try:
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            sql_query = "select id, product_id, open_desc, profit_assign, profit_assign_desc, invest_goal, create_at, " \
                        "update_at, is_delete from %s.pdc_highend_detail where product_id='%s' and is_delete='1';"
            highend_detail_list = self._db.sql_run(sql_query, db_name, product_id)
            sql_query1 = " select i.* from %s.pdc_highend_investor i where i.is_delete=1 and id IN " \
                         "(select v.investor_id from %s.pdc_product_investor v where v.product_id='%s');"
            highend_investor_list = self._db.sql_run(sql_query1, db_name, db_name, product_id)
            return highend_detail_list, highend_investor_list
        except:
            pass

    # 获取产品issue信息
    def get_issue_info(self, product_id):
        try:
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            sql_query = "select * from %s.pdc_issued_info where productid='%s';"
            issue_info_list = self._db.sql_run(sql_query, db_name, product_id)
            return issue_info_list
        except:
            pass

    # 用户实名信息
    def cust_real_name_info(self, user_name):
        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query, db_name, user_name)[0]['cust_no']

            sql_query1 = "SELECT * FROM %s.cif_cust_base_audit where cust_no = '%s'"
            cust_real_name_info = self._db.sql_run(sql_query1, db_name, cust_no)
            return cust_real_name_info
        except:
            pass

    # 查询表CTS_PROD_RENEW
    def select_cts_prod_renew(self, user_name, fund_id, value_date):
        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query, db_name, user_name)[0]['cust_no']

            # step2-再查表CTS_PROD_RENEW
            db_name1 = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            sql_query1 = "select * from %s.CTS_PROD_RENEW where CUST_NO='%s' and PROD_ID='%s' and VALUE_DATE='%s';"
            prod_renew_list = self._db.sql_run(sql_query1, db_name1, cust_no, fund_id, value_date)
            return prod_renew_list
        except:
            pass

    # 更新表CTS_PROD_RENEW
    def update_cts_prod_renew(self, user_name, fund_id, due_process_type, red_amt, value_date):
        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query, db_name, user_name)[0]['cust_no']

            # step2-更新表CTS_PROD_RENEW
            db_name1 = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            sql_query1 = "update %s.CTS_PROD_RENEW set DUE_PROCESS_TYPE='%s', RED_AMT='%s', RESULT_CODE='N' where CUST_NO='%s' and VALUE_DATE='%s' and PROD_ID='%s';"
            self._db.sql_run(sql_query1, db_name1, due_process_type, red_amt, cust_no, value_date, fund_id)
        except:
            pass

    # 交易-查询理财型基金份额明细
    def get_finance_fund_prod_detail(self, user_name, product_id, value_date):
        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query, db_name, user_name)[0]['cust_no']

            # step2-查份额明细表、查产品滚存表
            db_name1 = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            sql_query1 = "select * from %s.CTS_PROD_QUTY_DETAIL where cust_no = '%s' and prod_id = '%s' and value_date = '%s' order by created_at desc limit 1;"
            prod_detail_list = self._db.sql_run(sql_query1, db_name1, cust_no, product_id,
                                                str(value_date).replace('-', ''))
            return prod_detail_list
        except:
            pass

    # 搜索极速转换基金
    def search_can_transfer_fast_fund(self, keyword, from_product_id):
        try:
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            sql_query = "select * from " \
                        "( " \
                        "(select " \
                        "a.productid,a.product_no,a.product_type, a.fund_type, a.product_short_name,a.product_pinyin, " \
                        "a.float_yield, a.latest_nav, null heavy_asset_name, null heavy_asset_code, a.halfyear_return , " \
                        "null heavy_asset_type, b.support_fast_transfer,a.min_convert_amount,a.ack_buy_day,b.transfer_status " \
                        "from %s.pdc_productinfo a " \
                        "join %s.pdc_product_marketing b on a.productid=b.productid and b.onsale_flag = 1 and b.is_sale = 1 " \
                        "join %s.pdc_issued_suspension d on a.productid = d.productid and d.bus_type=1 " \
                        "and d.change_type != 13 and d.is_delete = 1 " \
                        "left join %s.pdc_issued_info x on a.productid = x.productid " \
                        "where 1=1 " \
                        "AND b.accept_mode = 'M' " \
                        "AND a.productid != '%s' " \
                        "AND ( " \
                        "locate('%s',a.product_short_name) " \
                        "OR locate('%s',a.product_no) " \
                        "OR locate('%s',a.product_pinyin) " \
                        ") " \
                        "AND a.product_type= 2 " \
                        "and (x.bid_time != '' AND NOW() >= x.bid_time and " \
                        "(x.liquidation_time is NULL or x.liquidation_time = '' or NOW() < x.liquidation_time)) " \
                        "limit 100 " \
                        ") " \
                        "union " \
                        "(select d.productid,d.product_no,d.product_type, d.fund_type, " \
                        "d.product_short_name,d.product_pinyin, d.float_yield, d.latest_nav, e.name " \
                        "heavy_asset_name, e.code heavy_asset_code, d.halfyear_return, e.type as heavy_asset_type, " \
                        "m.support_fast_transfer,d.min_convert_amount,d.ack_buy_day,m.transfer_status " \
                        "from %s.pdc_fund_portfolio e " \
                        "left join %s.pdc_productinfo d on d.productid=e.productid " \
                        "join %s.pdc_product_marketing m on e.productid=m.productid and m.onsale_flag=1 and m.is_sale = 1 " \
                        "join %s.pdc_issued_suspension q on e.productid = q.productid and q.bus_type=1 " \
                        "and q.change_type != 13 and q.is_delete = 1 " \
                        "left join pdc.pdc_issued_info y on e.productid = y.productid " \
                        "where m.accept_mode = 'M' AND d.productid != '%s' " \
                        "AND (locate('%s',e.name) or locate('%s',e.code)) " \
                        "AND d.product_type= 2 " \
                        "and (y.bid_time != '' AND NOW() >= y.bid_time and " \
                        "(y.liquidation_time is NULL or y.liquidation_time = '' or NOW() < y.liquidation_time)) " \
                        "limit 100 " \
                        ") " \
                        "limit 200 " \
                        ") ab;"
            search_can_transfer_fast_fund_list = self._db.sql_run(sql_query, db_name, db_name, db_name, db_name,
                                                                  from_product_id, keyword, keyword, keyword, db_name,
                                                                  db_name, db_name, db_name, from_product_id, keyword,
                                                                  keyword)
            return search_can_transfer_fast_fund_list
        except:
            pass

    # 搜索普通转换基金
    def search_can_transfer_normal_fund(self, keyword):
        try:
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            sql_query = "select * from " \
                        "( " \
                        "(select " \
                        "a.productid,a.product_no,a.product_type, a.fund_type, a.product_short_name,a.product_pinyin, " \
                        "a.float_yield, a.latest_nav, null heavy_asset_name, null heavy_asset_code, a.halfyear_return , " \
                        "null heavy_asset_type, b.support_fast_transfer,a.min_convert_amount,a.ack_buy_day,b.transfer_status " \
                        "from %s.pdc_productinfo a " \
                        "join %s.pdc_product_marketing b on a.productid=b.productid and b.onsale_flag = 1 and b.is_sale = 1 " \
                        "join %s.pdc_issued_suspension d on a.productid = d.productid and d.bus_type=1 and d.change_type !=13 and d.is_delete = 1 " \
                        "left join %s.pdc_issued_info x on a.productid = x.productid " \
                        "where 1=1 AND b.accept_mode = 'M' and a.ack_buy_day = '1' AND ( " \
                        "locate('%s',a.product_short_name) " \
                        "OR locate('%s',a.product_no) " \
                        "OR locate('%s',a.product_pinyin) " \
                        ") " \
                        "AND a.product_type= 2 " \
                        "and (x.bid_time != '' AND NOW() >= x.bid_time and " \
                        "(x.liquidation_time is NULL or x.liquidation_time = '' or NOW() < x.liquidation_time)) " \
                        "limit 50 " \
                        ") " \
                        "union " \
                        "(select d.productid,d.product_no,d.product_type, d.fund_type, " \
                        "d.product_short_name,d.product_pinyin, d.float_yield, d.latest_nav, e.name " \
                        "heavy_asset_name, e.code heavy_asset_code, d.halfyear_return, e.type as heavy_asset_type, " \
                        "m.support_fast_transfer,d.min_convert_amount,d.ack_buy_day,m.transfer_status " \
                        "from %s.pdc_fund_portfolio e " \
                        "left join %s.pdc_productinfo d on d.productid=e.productid " \
                        "join %s.pdc_product_marketing m on e.productid=m.productid and m.onsale_flag=1 and m.is_sale = 1 " \
                        "join %s.pdc_issued_suspension q on e.productid = q.productid and q.bus_type=1 and q.change_type !=13 and q.is_delete = 1 " \
                        "left join %s.pdc_issued_info y on e.productid = y.productid " \
                        "where m.accept_mode = 'M' and d.ack_buy_day = '1' " \
                        "AND (locate('%s',e.name) " \
                        "or locate('%s',e.code)) " \
                        "AND d.product_type= 2 and (y.bid_time != '' AND NOW() >= y.bid_time " \
                        "and (y.liquidation_time is NULL or y.liquidation_time = '' or NOW() < y.liquidation_time)) " \
                        "limit 50 " \
                        ") " \
                        "limit 100 ) ab;"
            search_can_transfer_normal_fund_list = self._db.sql_run(sql_query, db_name, db_name, db_name, db_name,
                                                                    keyword, keyword, keyword, db_name, db_name,
                                                                    db_name, db_name, db_name, keyword, keyword)
            return search_can_transfer_normal_fund_list
        except:
            pass

    # 获取基金费率详情
    def get_fund_base_rate(self, product_id, charge_rate_type):
        try:
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            now_day = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            sql_query = "select *  from %s.pdc_base_rate where productid = '%s' and charge_rate_type = '%s' " \
                        "and (excute_date is not null and excute_date<'%s') and (cancel_date is null " \
                        "or cancel_date >= '%s') and fin_id > 0 ORDER by charge_rate_unit asc, max_charge_rate desc;"
            fund_base_rate = self._db.sql_run(sql_query, db_name, product_id, charge_rate_type, now_day, now_day)
            return fund_base_rate
        except:
            pass

    # 获取极速转换基金列表
    def get_fast_transfer_fund_list(self):
        try:
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            sql_query = "select a.productid,a.product_no,a.product_short_name,a.latest_nav,a.latest_nav_date, " \
                        "if(a.fund_type=1 or a.fund_type=8,CAST(replace(a.float_yield,'%%%%','') AS DECIMAL(9,4))," \
                        "a.halfyear_return) as floatOrder, a.ack_redeem_day,a.float_yield,a.fund_type, " \
                        "c.discount,c.is_fixedfee_discount,c.critical_rate,a.min_buy_amount, " \
                        "b.major_secondary_transfer,a.ack_buy_day,a.daily_return,a.min_convert_amount, " \
                        "a.max_buy_rate as max_charge_rate_subscribe, " \
                        "a.max_buy_rate_unit as charge_rate_unit_subscribe " \
                        "from %s.pdc_productinfo a " \
                        "join %s.pdc_product_marketing b on a.productid=b.productid " \
                        "and b.accept_mode='M' " \
                        "join %s.pdc_issued_suspension d on a.productid = d.productid and d.bus_type=1 and d.change_type != 13 and d.is_delete = 1 " \
                        "left join %s.pdc_issued_info x on a.productid=x.productid " \
                        "left join %s.pdc_discount_rate c on c.productid=a.productid " \
                        "and c.is_base_discount=0 and NOW()>= c.preferential_period_start and NOW()<= c.preferential_period_end " \
                        "where a.product_type=2 and a.ta_no !='05' and b.onsale_flag =1 and b.is_sale = 1 " \
                        "and (x.bid_time != '' AND NOW() >= x.bid_time " \
                        "AND (x.liquidation_time is NULL or x.liquidation_time = '' or NOW() < x.liquidation_time)) " \
                        "ORDER BY if(a.fund_type=1 or a.fund_type=8,1,0), " \
                        "floatOrder desc;"
            fast_transfer_fund_list = self._db.sql_run(sql_query, db_name, db_name, db_name, db_name, db_name)
            return fast_transfer_fund_list
        except:
            pass

    # 获取普通转换基金列表
    def get_normal_transfer_fund_list(self, product_id):
        try:
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            sql_query = "select a.productid,a.product_no,a.product_short_name,a.latest_nav,a.latest_nav_date, " \
                        "if(a.fund_type=1 or a.fund_type=8,CAST(replace(a.float_yield,'%%%%','') AS DECIMAL(9,4))," \
                        "a.halfyear_return) as floatOrder, a.ack_redeem_day,a.float_yield,a.fund_type, " \
                        "c.discount,c.is_fixedfee_discount,c.critical_rate,a.min_buy_amount, " \
                        "b.major_secondary_transfer,a.ack_buy_day,a.daily_return,a.min_convert_amount, " \
                        "a.max_buy_rate as max_charge_rate_subscribe, " \
                        "a.max_buy_rate_unit as charge_rate_unit_subscribe " \
                        "from %s.pdc_productinfo a " \
                        "join %s.pdc_product_marketing b on a.productid=b.productid " \
                        "and b.accept_mode='M' and (b.transfer_status = 0 or b.transfer_status =1) " \
                        "join %s.pdc_issued_suspension d on a.productid = d.productid and d.bus_type=1 and d.change_type != 13 and d.is_delete = 1 " \
                        "left join %s.pdc_issued_info x on a.productid=x.productid " \
                        "left join %s.pdc_discount_rate c on c.productid=a.productid " \
                        "and c.is_base_discount=0 and NOW()>= c.preferential_period_start and NOW()<= c.preferential_period_end " \
                        "where a.product_type=2 and a.productid!='%s' and a.ta_no='%s' and a.ack_buy_day = '1' " \
                        "and b.onsale_flag =1 and b.is_sale = 1 and (x.bid_time != '' AND NOW() >= x.bid_time " \
                        "AND (x.liquidation_time is NULL or x.liquidation_time = '' or NOW() < x.liquidation_time)) " \
                        "ORDER BY if(a.fund_type=1 or a.fund_type=8,1,0), " \
                        "floatOrder desc;"
            normal_transfer_fund_list = self._db.sql_run(sql_query, db_name, db_name, db_name, db_name, db_name,
                                                        product_id, str(product_id).split('#')[0])
            return normal_transfer_fund_list
        except:
            pass

    # 交易-我的历史持有列表
    def get_holding_his(self, user_name, product_type, fund_type):
        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query, db_name, user_name)[0]['cust_no']

            db_name1 = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            db_name2 = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            if str(product_type) == '2':
                sql_query1 = "select * from %s.CTS_PROD_HOLDING_HIS where CUST_NO = '%s' and BRANCH_CODE = '675' and " \
                             "SHARE_TYPE = 'A' and END_TIME is not null and PROD_TYPE = '%s' and PROD_SEC_TYPE='%s' " \
                             "order by START_TIME DESC,ID desc;"
                prod_holding_his = self._db.sql_run(sql_query1, db_name1, cust_no, product_type, fund_type)
            else:
                sql_query1 = "select * from %s.CTS_PROD_HOLDING_HIS where CUST_NO = '%s' and BRANCH_CODE = '675' and " \
                             "SHARE_TYPE = 'A' and END_TIME is not null and PROD_TYPE = '%s'" \
                             "order by START_TIME DESC,ID desc;"
                prod_holding_his = self._db.sql_run(sql_query1, db_name1, cust_no, product_type)

            prod_info_list = {}
            for i in range(0, len(prod_holding_his)):
                sql_query2 = "select * from %s.pdc_productinfo where productid='%s';"
                prod_info = self._db.sql_run(sql_query2, db_name2, prod_holding_his[i]['PROD_ID'])
                prod_info_list[i] = prod_info
            return prod_holding_his, prod_info_list
        except:
            pass

    # 根据batch_no查询历史持有列表
    def get_history_list_by_batch_no(self, user_name, batch_no):
        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query, db_name, user_name)[0]['cust_no']

            db_name = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            sql_query = "select * from %s.CTS_PROD_HOLDING_HIS where ID='%s' and CUST_NO='%s';"
            prod_his = self._db.sql_run(sql_query, db_name, batch_no, cust_no)

            db_name2 = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            sql_query2 = "select * from %s.pdc_productinfo where productid='%s';"
            prod_info = self._db.sql_run(sql_query2, db_name2, prod_his[0]['PROD_ID'])
            prod_marketing = self.get_pdc_product_marketing(product_id=prod_his[0]['PROD_ID'])
            prod_issue = self.get_issue_info(product_id=prod_his[0]['PROD_ID'])
            sql_query3 = "select * from %s.pdc_open_day where productid='%s' and allow_redeem=1 order by open_day_time desc limit 1;"
            open_day = self._db.sql_run(sql_query3, db_name2, prod_his[0]['PROD_ID'])
            return prod_his, prod_info, prod_marketing, prod_issue, open_day
        except:
            pass

    # 获取前一个工作日
    def get_last_work_date(self, day):
        try:
            db_name = 'cts_uat' if DBC_TAG == 'uat' else 'cts'
            sql_query = "select * FROM %s.CTS_WORK_DAYS where WORK_DATE < '%s' and WORK_FLAG = 'Y' order by WORK_DATE DESC limit 1;"
            last_work_date = self._db.sql_run(sql_query, db_name, day)
            return last_work_date
        except:
            pass

    # 根据题号获取题目
    def cal_total_score(self, question_no):
        try:
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "select * from %s.cif_risk_question a, %s.cif_risk_test_topic b where a.topic_id = b.id " \
                        "and a.status = 'N' and a.question_no = '%s' order by a.topic_row;"

            question_info = self._db.sql_run(sql_query, db_name, db_name, question_no)
            return question_info
        except:
            pass

    # 账户-查询税收居民身份
    def get_tax_type(self, user_name):
        try:
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "select * from %s.cif_cust_base where mobile='%s';"
            tax_type_list = self._db.sql_run(sql_query, db_name, user_name)
            return tax_type_list
        except:
            pass

    # 获取用户元宝信息
    def get_coin(self, mobile):
        try:
            db_name = 'points_uat' if DBC_TAG == 'uat' else 'points'
            cust_no = self.get_cust_info(columns='cust_no', match='=', mobile=mobile)[0]['cust_no']
            sql = "SELECT * FROM %s.COIN_ACCOUNT WHERE CUST_NO = '%s' ORDER BY id desc LIMIT 1;"
            coin = self._db.sql_run(sql, db_name, cust_no)
            return coin
        except:
            pass

    # 获取用户福利中心交易明细
    def get_trade_detail_points_or_coin(self, user_name, points_type, type):
        try:
            # step1-先查用户cust_no
            db_name = 'cif_uat' if DBC_TAG == 'uat' else 'cif'
            sql_query = "SELECT cust_no FROM %s.cif_cust_base where mobile = '%s'"
            cust_no = self._db.sql_run(sql_query, db_name, user_name)[0]['cust_no']

            # step2-查询用户福利中心交易明细
            db_name1 = 'points_uat' if DBC_TAG == 'uat' else 'points'
            if str(type) == '0':
                if str(points_type) == '0':
                    sql_query1 = "select * from %s.POINTS_ACCOUNT_HIS where CUST_NO='%s' and POINT_TYPE in " \
                                 "('ISSUE', 'UNFROZEN', 'CANCEL') ORDER BY CREATED_AT DESC ;"
                else:
                    sql_query1 = "select * from %s.COIN_ACCOUNT_HIS where CUST_NO='%s' and COIN_TYPE in " \
                                 "('ISSUE', 'UNFROZEN', 'CANCEL') ORDER BY CREATED_AT DESC ;"
            else:
                if str(points_type) == '0':
                    sql_query1 = "select * from %s.POINTS_ACCOUNT_HIS where CUST_NO='%s' and POINT_TYPE in " \
                                 "('FROZEN') ORDER BY CREATED_AT DESC ;"
                else:
                    sql_query1 = "select * from %s.COIN_ACCOUNT_HIS where CUST_NO='%s' and COIN_TYPE in " \
                                 "('FROZEN') ORDER BY CREATED_AT DESC ;"

            weal_list = self._db.sql_run(sql_query1, db_name1, cust_no)
            return weal_list
        except:
            pass

    # 获取物品兑换批次配置
    def get_goods_exchange_batch(self, id):
        try:
            # 获取兑换商品的消费
            db_name1 = 'points_uat' if DBC_TAG == 'uat' else 'points'
            sql_query1 = "select * from %s.GOODS_EXCHANGE_BATCH where ACTIVITY_DETAIL_ID='%s' limit 1;"
            goods_exchange_batch_list = self._db.sql_run(sql_query1, db_name1, id)
            return goods_exchange_batch_list
        except:
            pass

    # 获取积分、元宝说明
    def get_points_description(self, code):
        try:
            db_name = 'points_uat' if DBC_TAG == 'uat' else 'points'
            sql = "SELECT * FROM %s.POINTS_DESCRIPTION where CODE = '%s' AND STATUS = 'Y';"
            points_description = self._db.sql_run(sql, db_name, code)
            return points_description
        except:
            pass

    # 现金宝签到
    def get_points_sign_in(self):
        try:
            db_name = 'points_uat' if DBC_TAG == 'uat' else 'points'
            now_day = Utility.DateUtil().getToday()
            sql_query = "SELECT * FROM %s.COIN_ISSUE_EVENT_RULE where(START_AT is null or START_AT <= '%s') and (END_AT is null or END_AT >= '%s') and EVENT_KEY = 'XJB_DAILY_SIGN' and STATUS = 'Y';"
            sign_in_points = self._db.sql_run(sql_query, db_name, now_day, now_day)
            return sign_in_points
        except:
            pass

    # 积分 - 查询积分发放规则
    def get_points_issue_event_rules(self):
        try:
            db_name = 'points_uat' if DBC_TAG == 'uat' else 'points'
            sql_query = "select * from %s.POINTS_ISSUE_EVENT_RULE WHERE STATUS = 'Y' and EVENT_KEY != 'POINT_MANUAL_PLUS' and START_AT is null or START_AT <=now() and (END_AT is null or END_AT >=now()) order BY  ORDER_BY asc,id asc;"
            points_issue_event_rules = self._db.sql_run(sql_query, db_name)
            return points_issue_event_rules
        except:
            pass

    # 基金-基金申购、认购、赎回费率
    def get_product_ext(self, product_id):
        try:
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            sql_query = " select a.*, b.onsale_flag, b.is_new_issue,b.is_sale from %s.pdc_productinfo a left join " \
                        "%s.pdc_product_marketing b on a.productid=b.productid and b.accept_mode='M' " \
                        "where a.productid='%s';"

            product_ext = self._db.sql_run(sql_query, db_name, db_name, product_id)
            return product_ext
        except:
            pass

    # 获取会员专属产品
    def get_exclusive_product_list(self, member_level):
        try:
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            sql_query = " select b.user_identify, a.*, b.onsale_status, b.close_period_pic, b.is_redem_anytime, d.product_status, " \
                        "c.invest_period_desc, b.client_type from %s.pdc_productinfo a join %s.pdc_product_marketing b on " \
                        "a.productid=b.productid and b.accept_mode='M' left join %s.pdc_product_detail c on " \
                        "a.productid=c.productid left join %s.pdc_issued_info d on a.productid=d.productid where " \
                        "locate('%s',b.user_identify) and (a.product_type=1 or a.product_type =3) and b.onsale_flag =1 " \
                        "order by if(b.is_sale=1,0,1), if(b.is_archive=1,0,1), d.dssub_endtime desc limit 1;"

            exclusive_list = self._db.sql_run(sql_query, db_name, db_name, db_name, db_name, member_level)
            return exclusive_list
        except:
            pass

    # 查询会员等级
    def get_member_level(self, code):
        try:
            db_name = 'points_uat' if DBC_TAG == 'uat' else 'points'
            sql_query = "select * from %s.MEMBER_INTERESTS where CODE = '%s';"
            member_level = self._db.sql_run(sql_query, db_name, code)
            return member_level
        except:
            pass

    # 基金类型列表
    def fund_type_list(self):
        try:
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            sql_query = "SELECT * FROM %s.pdc_fund_type where is_delete = 0 order by display_order;"
            fund_type_list = self._db.sql_run(sql_query, db_name)
            return fund_type_list
        except:
            pass

    # 更新现金宝充值限额
    def update_xjb_recharge_amount(self):
        try:
            db_name = 'pdc_uat' if DBC_TAG == 'uat' else 'pdc'
            sql_query = "update %s.pdc_productinfo set large_amount_per_buying = '5000000', large_amount_per_day = '10000000000' where productid='ZX05#000730';"
            self._db.sql_run(sql_query, db_name)
        except:
            pass


if __name__ == '__main__':
    m = MysqlXjbTools()
    # print m.get_loan_repay_amt(user_name='17200000209')
    print m.get_normal_transfer_fund_list(product_id='05#000811').__len__()
