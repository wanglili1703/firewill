# coding: utf-8
import random
import datetime
import sys
from time import sleep

from _tools.restful_cms_tools import RestfulCmsTools

reload(sys)
sys.setdefaultencoding('utf-8')

from _common.utility import Utility
from _tools.mysql_xjb_tools import MysqlXjbTools
from huaxin_restful_service.restful_xjb_service.main_restful_xjb_entity import MainResfulXjbEntity


class RestfulXjbTools(object):
    def __init__(self):
        self.entity = MainResfulXjbEntity()
        self.mysql = MysqlXjbTools()
        self._cms = RestfulCmsTools()

    # 登录
    def login(self, user_name, password):
        try:
            self.entity.login(username=user_name, password=password)
        except Exception, e:
            print e
            pass

    # 登录-uat
    def login_uat(self, user_name, password):
        try:
            self.entity.login_uat(username=user_name, password=password)
        except Exception, e:
            print e
            pass

    # 账户-登录（新）
    def login_new(self, user_name, password, type):
        try:
            if type == '0':
                self.entity.login_new(username=user_name, password=password, type=type)
            elif type == '1':
                try:
                    entity = self.entity.sms_login_get_mobile_code(mobile=user_name, captchaCode='567891')
                except Exception:
                    sleep(60)
                    entity = self.entity.sms_login_get_mobile_code(mobile=user_name, captchaCode='567891')

                serial_no = entity.body_serialNo
                self.entity.login_new(password=password, type=type, serialNo=serial_no)
        except:
            pass

    # 注册
    def register(self, mobile, login_password):
        try:

            self.entity.register_get_mobile_code(mobile=mobile)

            mobile_code = self.entity.current_mobile_code
            serial_no = self.entity.current_register_serialno

            self.entity.register_confirm(mobileCode=mobile_code, password=login_password, serialNo=serial_no)
            return mobile, login_password
        except:
            pass

    # 注册绑卡
    def register_binding_card(self, mobile, login_password, card_bin, trade_password):
        try:
            self.register(mobile=mobile, login_password=login_password)

            card_no = Utility.GetData().bank_card_no(card_bin=card_bin).split('-')[0]
            name = 'AUTO' + str(random.randint(0, 99))
            cert_no = Utility.GetData().id_no()

            self.entity.card_set_trade_password(newPassword=trade_password)
            serial_no = self.entity.current_set_trade_passowrd_serialno

            entity = self.entity.card_match_channel(card_bin=card_bin + '1322')

            bank_no = entity.bankChannel_bankNo
            bank_name = entity.bankChannel_bankGroupName
            sms_mode = entity.smsMode

            self.entity.card_get_mobile_code(mobile=mobile,
                                             serialNo=serial_no,
                                             cardNo=card_no,
                                             name=name,
                                             certNo=cert_no,
                                             smsMode=sms_mode,
                                             bankName=bank_name,
                                             bankNo=bank_no
                                             )

            # mobile_code = self.mysql.get_sms_verify_code(mobile=mobile, template_id='cif_bindBankCard')
            mobile_code = self.entity.current_mobile_code

            serial_no = self.entity.current_get_mobile_code_serialno

            self.entity.card_new_binding(mobileCode=mobile_code, serialNo=serial_no)

            return card_no
        except Exception, e:
            pass

    # 登录绑卡
    def login_binding_card(self, mobile, login_password, card_bin, trade_password):
        try:
            self.login(user_name=mobile, password=login_password)

            serial_no = None

            card_no = Utility.GetData().bank_card_no(card_bin=card_bin).split('-')[0]
            name = 'AUTO' + str(random.randint(0, 99))
            cert_no = Utility.GetData().id_no()

            if self.mysql.get_cust_info(columns='*', match='=', mobile=mobile)[0]['passwd'] is None:
                self.entity.card_set_trade_password(newPassword=trade_password)
                serial_no = self.entity.current_set_trade_passowrd_serialno

            entity = self.entity.card_match_channel(card_bin=card_bin)

            bank_no = entity.bankChannel_bankNo
            bank_name = entity.bankChannel_bankGroupName
            sms_mode = entity.smsMode

            entity = self.entity.card_get_mobile_code(mobile=mobile,
                                                      serialNo=serial_no,
                                                      cardNo=card_no,
                                                      name=name,
                                                      certNo=cert_no,
                                                      smsMode=sms_mode,
                                                      bankName=bank_name,
                                                      bankNo=bank_no
                                                      )

            serial_no = entity.body_serialNo
            mobile_code = self.entity.current_mobile_code

            self.entity.card_new_binding(mobileCode=mobile_code, serialNo=serial_no)
        except:
            pass

    # 风险评估
    def risk_evaluating(self, user_name, login_password):
        try:
            self.login(user_name=user_name, password=login_password)
            entity = self.entity.get_risk_question_by_type()
            question_no = entity.questionNo
            self.entity.risk_evaluating(questionNo=question_no)
        except:
            pass

    # 充值
    def recharge(self, user_name, password, trade_password, recharge_amount, bank_card_id=None):
        try:
            self.login(user_name=user_name, password=password)

            entity = self.entity.get_cust_card_list()
            cards = entity.cards.__len__()
            if cards == 1:
                bank_card_id = entity.bankCardId if bank_card_id == '' or bank_card_id is None else bank_card_id
                bank_no = entity.bankNo
            else:
                bank_card_id = entity.bankCardId[0] if bank_card_id == '' else bank_card_id
                bank_no = entity.bankNo[0]

            print bank_card_id
            self.entity.recharge(bankCardId=bank_card_id,
                                 amt=recharge_amount,
                                 bankNo=bank_no
                                 )
            serial_no = self.entity.current_recharge_serialno
            self.entity.trade_confirm(serialNo=serial_no, password=trade_password)
        except:
            pass

    # 使用优惠券充值现金宝
    def recharge_using_coupons(self, user_name, password, bank_card_id, recharge_amount, bank_no, trade_password):
        try:
            self.login(user_name=user_name, password=password)
            self._cms.issue_coupon(code='FULL_OFF_10_1_0029', mobile=user_name, quantity=1)
            entity = self.entity.points_discount_coupon(purchaseAmt=recharge_amount, type='1')
            coupon_id = self.entity.current_coupon_id
            entity = self.entity.can_used_points_count(amt=recharge_amount, couponIds=coupon_id,
                                                       isUsePoints='0')

            self.entity.recharge(bankCardId=bank_card_id, amt=recharge_amount, bankNo=bank_no, couponIds=coupon_id)
            serial_no = self.entity.current_recharge_serialno
            self.entity.trade_confirm(serialNo=serial_no, password=trade_password)
        except:
            pass

    # 取现
    def withdraw(self, user_name, password, withdraw_amount, withdraw_type, trade_password, bank_card_id=None):
        # withdrawType:1是普取,2是快取
        try:
            self.login(user_name=user_name, password=password)

            entity = self.entity.get_cust_card_list()
            cards = entity.cards.__len__()
            if cards == 1:
                bank_card_id = entity.bankCardId if bank_card_id is None else bank_card_id
                bank_no = entity.bankNo
            else:
                bank_card_id = entity.bankCardId[0] if bank_card_id is None else bank_card_id
                bank_no = entity.bankNo[0]

            self.entity.withdraw(bankCardId=bank_card_id, withdrawType=withdraw_type, amt=withdraw_amount,
                                 bankNo=bank_no)
            serial_no = self.entity.current_withdraw_serialno
            entity = self.entity.trade_confirm(serialNo=serial_no,
                                               password=trade_password
                                               )
            withdraw_serial_no = entity.serialNo
            self.entity.withdraw_query(serialNo=withdraw_serial_no)
        except:
            pass

    # 创建一个新用户
    def new_user(self, user_name, login_password, card_bin, trade_password, recharge_amount=None, bank_card_id=None):
        try:
            # 注册绑卡
            card_no = self.register_binding_card(mobile=user_name, login_password=login_password, card_bin=card_bin,
                                                 trade_password=trade_password)

            # # 风险评估
            # self.risk_evaluating(user_name=user_name, login_password=login_password)
            #
            # # 给用户的卡充值
            # self.recharge(user_name=user_name, password=login_password, recharge_amount=recharge_amount,
            #               bank_card_id=bank_card_id)

            return user_name, login_password, trade_password, card_no
        except:
            pass

    def buy_product(self, user_name, login_password, pay_type, amt, product_id, trade_password):
        try:
            self.login(user_name=user_name, password=login_password)

            self.entity.purchase_product(productId=product_id,
                                         payType=pay_type,
                                         amt=amt
                                         )
            serial_no = self.entity.current_purchase_product_serialno

            self.entity.trade_confirm(serialNo=serial_no,
                                      password=trade_password,
                                      )
        except:
            pass

    # 叠加优惠券认购基金
    def buy_product_using_coupon(self, user_name, login_password, product_id, pay_type, pay_amount, coupon_ids,
                                 trade_password):
        try:
            self.login(user_name=user_name, password=login_password)
            self._cms.issue_coupon(code='FULL_OFF_1000_10_0014', mobile=user_name, quantity=1)
            self.entity.purchase_product(productId=product_id, payType=pay_type,
                                         amt=pay_amount, couponIds=coupon_ids)
            serial_no = self.entity.current_purchase_product_serialno

            self.entity.trade_confirm(serialNo=serial_no, password=trade_password)
        except:
            pass

    # 使用预约码认购定期宝
    def buy_product_using_reserve_code(self, user_name, login_password, product_id, reservation_code, amount,
                                       trade_password):
        try:
            self.login(user_name=user_name, password=login_password)
            self.entity.purchase_product(productId=product_id, reservationCode=reservation_code, amt=amount)
            serial_no = self.entity.current_purchase_product_serialno
            self.entity.trade_confirm(serialNo=serial_no, password=trade_password)
        except:
            pass

    # 现金宝收支明细
    def get_xjb_trade_list(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_xjb_trade_list()
        except:
            pass

    # 交易记录
    def get_trade_list(self, user_name, password, product_type):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_trade_list(productType=product_type)
        except:
            pass

    # 定期宝赎回-获取收益信息
    def dqb_redeem_get_income_info(self, user_name, login_password, product_id, trade_amt):
        try:
            self.login(user_name=user_name, password=login_password)
            self.entity.dqb_redeem_get_income_info(productId=product_id, tradeAmt=trade_amt)
        except:
            pass

    # 基金赎回
    def redeem_product(self, user_name, login_password, product_id, sold_share, trade_password, sold_type):
        try:
            self.login(user_name=user_name, password=login_password)
            self.entity.redeem_product(fundId=product_id, soldShare=sold_share, soldType=sold_type)
            serial_no = self.entity.current_redeem_product_share_serialno
            self.entity.trade_confirm(serialNo=serial_no, password=trade_password)
        except:
            pass

    # 交易-高端极速赎回限额信息(V2.0)
    def get_vip_product_fast_redeem_limit_info(self, user_name, password, product_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_vip_product_fast_redeem_limit_info(productId=product_id)
        except:
            pass

    # 高端赎回-获取提示信息
    def get_vip_financial_redeem_tip(self, user_name, password, product_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.redeem_product_tip(productId=product_id)
        except:
            pass

    # 高端赎回
    def redeem_vipproduct(self, user_name, login_password, product_id, sold_share, trade_password, sold_type):
        try:
            self.login(user_name=user_name, password=login_password)
            # self.entity.redeem_product_tip(productId=product_id)
            self.entity.redeem_product_share(productId=product_id, soldShare=sold_share, soldType=sold_type)
            serial_no = self.entity.current_redeem_product_share_serialno
            self.entity.trade_confirm(serialNo=serial_no, password=trade_password)
        except:
            pass

    # 定活宝赎回
    def redeem_dhb(self, user_name, login_password, product_id, amt, trade_password):
        try:
            self.login(user_name=user_name, password=login_password)
            self.entity.redeem_dhb(tradeAmt=amt, productId=product_id)
            serial_no = self.entity.current_redeem_product_share_serialno
            self.entity.trade_confirm(serialNo=serial_no, password=trade_password)
        except:
            pass

    # 首页总资产
    def get_total_asset(self, user_name, login_password):
        try:
            self.login(user_name=user_name, password=login_password)
            self.entity.total_asset()
        except:
            pass

    # 修改登录密码
    def modify_login_password(self, user_name, old_login_password, new_login_password):
        try:
            self.login(user_name=user_name, password=old_login_password)

            self.entity.modify_login_pwd_check_old_pwd(oldPassword=old_login_password)
            serial_no = self.entity.current_modify_login_pwd_check_old_pwd_serialno

            entity = self.entity.modify_login_pwd_set_pwd(serialNo=serial_no, newPassword=new_login_password)
            return entity.returnCode

        except:
            pass

    # 修改交易密码
    def modify_trade_password(self, user_name, login_password, old_trade_password, new_trade_password):
        try:
            self.login(user_name=user_name, password=login_password)

            self.entity.modify_trade_pwd_check_old_pwd(password=old_trade_password)
            serial_no = self.entity.current_modify_trade_pwd_check_old_pwd_serialno

            entity = self.entity.modify_trade_pwd_set_pwd(newPassword=new_trade_password, serialNo=serial_no)
            return entity.returnCode

        except:
            pass

    # 修改手机号码-发送原手机短信
    def modify_mobile(self, mobile_old, login_password, trade_password, mobile_new):
        try:
            self.login(user_name=mobile_old, password=login_password)
            self.entity.trade_password_validate(tradePassword=trade_password)

            serial_no = self.entity.current_trade_password_validate_serialno
            self.entity.modify_mobile_get_old_mobile_code(serialNo=serial_no, mobile=mobile_old)

            mobile_code_old = self.entity.current_mobile_code

            self.entity.modify_mobile_check_old_mobile_code(serialNo=serial_no, mobileCode=mobile_code_old)

            self.entity.modify_mobile_get_new_mobile_code(serialNo=serial_no, mobile=mobile_new)

            mobile_code_new = self.entity.current_mobile_code

            self.entity.modify_mobile_check_new_mobile_code(serialNo=serial_no, mobileCode=mobile_code_new)

        except:
            pass

    # 获取用户绑定银行卡列表
    def get_bank_card_list(self, user_name, login_password):
        try:
            self.login(user_name=user_name, password=login_password)
            self.entity.get_cust_card_list()
            return self.entity.current_entity.cards_bankAcco, self.entity.current_entity.cards_bankCardId, \
                   self.entity.current_entity.cards_bankNo
        except:
            pass

    def fund_sizer(self, user_name, login_password, company_id, grade_org_id, grade_level, rise_min, rise_max,
                   rise_section, page_no, page_size, fund_type):
        try:
            if str(user_name) is not '' and str(login_password) is not '':
                print "login to system."
                self.login(user_name=user_name, password=login_password)

            if str(company_id) is '':
                print "----show specified funds for all fund company."
                self.entity.all_fund_company_fund_sizer(gradeOrgId=grade_org_id, gradeLevel=grade_level,
                                                        riseMin=rise_min, riseMax=rise_max, riseSection=rise_section,
                                                        pageNo=page_no,
                                                        pageSize=page_size)
            else:
                print "----show specified funds for specified fund company."
                if str(fund_type) is '':
                    self.entity.specified_company_fund_sizer(companyId=company_id, gradeOrgId=grade_org_id,
                                                             gradeLevel=grade_level, riseMin=rise_min, riseMax=rise_max,
                                                             riseSection=rise_section, pageNo=page_no,
                                                             pageSize=page_size)
                else:
                    self.entity.fund_sizer_by_fund_type(companyId=company_id, gradeOrgId=grade_org_id,
                                                        gradeLevel=grade_level, riseMin=rise_min, riseMax=rise_max,
                                                        riseSection=rise_section, pageNo=page_no,
                                                        pageSize=page_size, fundType=fund_type)

            print "response body is ", self.entity.current_entity.dataList_fundId
            print "response body is ", self.entity.current_entity.totalCount
            if str(fund_type) is not '':
                return self.entity.current_entity.dataList_fundId, \
                       self.entity.current_entity.totalCount, \
                       self.entity.current_entity.dataList_fundType, \
                       self.entity.current_entity.dataList_nav, \
                       self.entity.current_entity.dataList_recommendContent
            else:
                return self.entity.current_entity.dataList_fundId, \
                       self.entity.current_entity.totalCount, \
                       self.entity.current_entity.dataList_nav, \
                       self.entity.current_entity.dataList_recommendConten
        except:
            pass

    # 首页收益信息
    def trade_asset_total_home_page(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.trade_asset_total_home_page()
        except:
            pass

    # 查询用户各类产品资产明细列表
    def trade_asset_detail_list(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.trade_asset_detail_list()
        except:
            pass

    # 基金搜索提示
    def fund_search_suggestion(self, user_name, password, type, keyword, pageNo, pageSize):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.fund_search_suggestion(type=type, keyword=keyword, pageNo=pageNo, pageSize=pageSize)
        except:
            pass

    # 基金热门搜索
    def fund_hot_search(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.fund_hot_search()
        except:
            pass

    # 基金星级排行（全部）
    def fund_all_star_level_order(self, user_name, login_password, grade_org_id, page_no):
        try:
            if str(user_name) is not '' and str(login_password) is not '':
                print "login to system."
                self.login(user_name=user_name, password=login_password)

            print "star level all, ", grade_org_id, page_no
            self.entity.fund_all_star_level_sort(gradeOrgId=grade_org_id, pageNo=page_no, pageSize='20')

            print "total count for funds is: ", self.entity.current_entity.totalCount

            return self.entity.current_entity.totalCount, self.entity.current_entity.dataList_gradeLevel

        except:
            pass

    # 基金星级排行（全部）排序功能
    def fund_all_order_star_level_order(self, user_name, login_password, grade_org_id, order_type, page_no):
        try:
            if str(user_name) is not '' and str(login_password) is not '':
                print "login to system."
                self.login(user_name=user_name, password=login_password)

            print "star level all with order, ", grade_org_id, page_no
            self.entity.fund_all_order_star_level_sort(gradeOrgId=grade_org_id, orderType=order_type, pageNo=page_no,
                                                       pageSize='20')

            print "total count for funds is: ", self.entity.current_entity.totalCount

            return self.entity.current_entity.totalCount, self.entity.current_entity.dataList_gradeLevel

        except:
            pass

    # 基金星级排行（基金类型）排序
    def fund_type_order_star_level_order(self, user_name, login_password, grade_org_id, order_type, fund_type, page_no):
        try:
            if str(user_name) is not '' and str(login_password) is not '':
                print "login to system."
                self.login(user_name=user_name, password=login_password)

            print "star level under specified fund type with order", grade_org_id, page_no, fund_type
            self.entity.fund_type_order_star_level_sort(gradeOrgId=grade_org_id, orderType=order_type,
                                                        fundType=fund_type, pageNo=page_no, pageSize='20')

            print "total count for funds is: ", self.entity.current_entity.totalCount

            return self.entity.current_entity.totalCount, self.entity.current_entity.dataList_gradeLevel, self.entity.current_entity.dataList_fundType

        except:
            pass

    # 基金 - 精选基金
    def fund_best_choices_fund_list(self, user_name, password, page_no):
        try:
            if str(user_name) is not '' and str(password) is not '':
                print "login to system."
                self.login(user_name=user_name, password=password)

            print "best choices fund list", page_no
            self.entity.fund_best_choices_fund_list(pageNo=page_no, pageSize='10')

            print "total count for funds is: ", self.entity.current_entity.totalCount

            return self.entity.current_entity.totalCount, self.entity.current_entity.dataList_fundId

        except:
            pass

    # 基金公司清单
    def fund_company_list(self):
        try:
            print "all fund company"
            self.entity.all_fund_company_list()

            return self.entity.current_entity.dataList

        except:
            pass

    # 基金类型列表
    def fund_type_list(self, user_name, password):
        try:
            if str(user_name) is not '' and str(password) is not '':
                print "login to system."
                self.login(user_name=user_name, password=password)

            print "all fund type list"
            self.entity.all_fund_type_list()

            return self.entity.current_entity.dataList_typeCode

        except:
            pass

    def fund_new_fund_list(self, user_name, password, page_no, page_size):
        try:
            if str(user_name) is not '' and str(password) is not '':
                print "login to system."
                self.login(user_name=user_name, password=password)

            print "new fund list"
            self.entity.new_fund_list(pageNo=page_no, pageSize=page_size)

            return self.entity.current_entity.totalCount, self.entity.current_entity.dataList_fundId

        except:
            pass

    # 统计热门搜索基金
    def count_hot_search_fund(self, user_name, password):
        try:
            if str(user_name) is not '' and str(password) is not '':
                print "login to system."
                self.login(user_name=user_name, password=password)

            print "count hot search fund list"
            self.entity.count_hot_search_fund()
            print "total count for funds is: ", self.entity.current_entity.totalCount
            return self.entity.current_entity.totalCount, self.entity.current_entity.dataList_fundId

        except:
            pass

    # 获取信用卡列表
    def creditcard_get_cust_cards(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)

            self.entity.get_cust_credit_card()

            return self.entity.current_entity.dataList_cardSerialNo, self.entity.current_entity.dataList_bankNo, self.entity.current_entity.dataList_cardTailNo

        except:
            pass

    # 新用户注册绑卡，绑信用卡
    def register_creditcard_bind_card(self, mobile, password, trade_password, name):
        try:
            self.register_binding_card(mobile=mobile, login_password=password, card_bin='622202',
                                       trade_password=trade_password)

            # 充值, 对于新用户只有当日充值超过1000元，beidou才会给用户信用卡和积分的权限
            entity = self.entity.get_cust_card_list()
            bank_card_id = entity.bankCardId
            bank_no = entity.bankNo

            # 风险评估
            self.entity.risk_evaluating()

            self.entity.recharge(bankCardId=bank_card_id, amt='1000', bankNo=bank_no)
            serial_no = self.entity.current_recharge_serialno
            self.entity.trade_confirm(serialNo=serial_no, password=trade_password)

            credit_card_no = Utility.GetData().bank_card_no(card_type=1).split('-')[0]
            entity = self.entity.get_creditcard_match_channel(bin=str(credit_card_no)[0:10])

            bank_no = entity.bankChannel_bankNo
            bank_name = entity.bankChannel_bankGroupName

            self.entity.get_credit_card_mobile_code(mobile=mobile, bankNo=bank_no, bankGroupName=bank_name,
                                                    cardNo=str(credit_card_no),
                                                    name=name)

            mobile_code = self.mysql.get_sms_verify_code(mobile=mobile, template_id='credit_bind_card')

            serial_no = self.entity.current_get_mobile_code_serialno

            self.entity.creditcard_bind(serialNo=serial_no, mobileCode=str(mobile_code))

            return self.entity.current_entity.body_serialNo, self.entity.current_entity.body_info, credit_card_no

        except:
            pass

    # 老用户绑信用卡
    def creditcard_bind_card_existing_user(self, mobile, password, credit_card_no):
        try:
            self.login(user_name=mobile, password=password)

            # credit_card_no = Utility.GetData().bank_card_no(card_bin=card_bin, card_type=1).split('-')[0]

            entity = self.entity.get_creditcard_match_channel(bin=str(credit_card_no)[0:10])

            bank_no = entity.bankChannel_bankNo
            bank_name = entity.bankChannel_bankGroupName

            name = self.mysql.get_cust_info('name', '=', mobile=mobile)[0]['name']

            self.entity.get_credit_card_mobile_code(mobile=mobile, bankNo=bank_no, bankGroupName=bank_name,
                                                    cardNo=credit_card_no, name=name)

            mobile_code = self.mysql.get_sms_verify_code(mobile=mobile, template_id='credit_bind_card')

            serial_no = self.entity.current_get_mobile_code_serialno

            self.entity.creditcard_bind(serialNo=serial_no, mobileCode=str(mobile_code))

            return self.entity.current_entity.body_serialNo, self.entity.current_entity.body_info

        except Exception, e:
            print e
            pass

    # 用户绑信用卡失敗
    def creditcard_bind_card_invalid_mobile_code(self, mobile, password, card_no, mobile_code):
        try:
            self.login(user_name=mobile, password=password)
            entity = self.entity.get_creditcard_match_channel(bin=str(card_no)[0:10])

            bank_no = entity.bankChannel_bankNo
            bank_name = entity.bankChannel_bankGroupName

            name = self.mysql.get_cust_info('name', '=', mobile=mobile)[0]['name']
            self.entity.get_credit_card_mobile_code(mobile=mobile, bankNo=bank_no, bankGroupName=bank_name,
                                                    cardNo=card_no,
                                                    name=name)
            serial_no = self.entity.current_get_mobile_code_serialno
            if str(mobile_code) is '':
                mobile_code = self.entity.current_mobile_code
            self.entity.creditcard_bind(serialNo=serial_no, mobileCode=mobile_code)

        except:
            pass

    # 用户手机app上信用卡还款
    def creditcard_bind_card_repay(self, mobile, password, card_id, amt, trade_password, image_id):
        try:
            self.login(user_name=mobile, password=password)
            self.entity.creditcard_repay_validate(repayAmt=amt, cardSerialNo=card_id)

            serial_no = self.entity.current_repay_serialno

            self.entity.creditcard_repay(tradePassword=trade_password, serialNo=serial_no)

            serial_no = self.entity.current_creditcard_repay_serialno
            if str(self.entity.current_creditcard_repay_validate_type) == '3':
                self.entity.get_face_recognition_validate(serialNo=serial_no, imageId=image_id)
            if str(self.entity.current_creditcard_repay_validate_type) == '2':
                self.entity.send_sms_code(serialNo=serial_no, mobile=mobile)
                serial_no = self.entity.current_send_sms_code_serialno
                self.entity.get_sms_code_validate(serialNo=serial_no, smsCode='123456')

            # 信用卡还款结果轮询
            self.entity.creditcard_query_repay_result(serialNo=serial_no)
        except:
            pass

    # 获取匹配信用卡通道 bin是10位数字
    def creditcard_get_match_channel(self, user_name, password, card_no):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_creditcard_match_channel(bin=str(card_no)[0:10])
        except:
            pass

    # 基金-全部基金列表
    def fund_all_list(self, user_name, password, pageNo, pageSize):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.fund_all_list(pageNo=pageNo, pageSize=pageSize)
        except:
            pass

    # 删除自选基金
    def fund_del_fav(self, user_name, password, objectIds, favType):
        try:
            if str(user_name) is not '' and str(password) is not '':
                print "login to system."
                self.login(user_name=user_name, password=password)
            print "show all with fav list", objectIds, favType
            self.entity.fund_del_fav(objectIds=objectIds, favType=favType)
        except:
            pass

    # 基金是否已经添加自选
    def fund_add_fav(self, user_name, password, objectIds, favType):
        try:
            if str(user_name) is not '' and str(password) is not '':
                print "login to system."
                self.login(user_name=user_name, password=password)
            print "show all with fav list", objectIds, favType
            self.entity.fund_add_fav(objectIds=objectIds, favType=favType)
        except:
            pass

    # 基金八大分类
    def fund_eight_part(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.fund_eight_part()
        except:
            pass

    # 基金首页下方四大块内容
    def fund_index_four(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.fund_index_four()

        except:
            pass

    # 信用卡卡状态
    def creditcard_status_info(self, user_name, password, card_no):
        try:
            self.login(user_name=user_name, password=password)
            entity = self.entity.get_creditcard_card_status_info(cardSerialNo=card_no)
            return entity.deletedCardMobile, entity.isDeletedCard
        except:
            pass

    # 信用卡重复预约还款
    def creditcard_repay_schedule(self, user_name, password, repay_amt, card_serial_no, trade_password,
                                  image_id):
        try:
            self.login(user_name=user_name, password=password)
            the_day_after_tomorrow = Utility.DateUtil().getToday() + datetime.timedelta(days=2)
            self.entity.creditcard_repay_schedule(repaymentAmt=repay_amt, cardSerialNo=card_serial_no,
                                                  repaymentDate=str(the_day_after_tomorrow.strftime('%Y%m%d')))
            serial_no = self.entity.current_repay_serialno
            self.entity.trade_confirm(serialNo=serial_no, password=trade_password)
            serial_no = self.entity.trade_confirm_serialno
            if str(self.entity.trade_confirm_validate_type) == '3':
                self.entity.get_face_recognition_validate(serialNo=serial_no, imageId=image_id)
            if str(self.entity.trade_confirm_validate_type) == '2':
                self.entity.send_sms_code(serialNo=serial_no, mobile=user_name)
                serial_no = self.entity.current_send_sms_code_serialno
                self.entity.get_sms_code_validate(serialNo=serial_no, smsCode='123456')
        except:
            pass

    # 使用优惠券信用卡预约还款
    def creditcard_reserve_repay_using_coupon(self, user_name, password, repay_amt, card_serial_no, trade_password):
        try:
            self.login(user_name=user_name, password=password)

            self._cms.issue_coupon(code='FULL_OFF_3_1_0070', mobile=user_name, quantity=1)
            entity = self.entity.points_discount_coupon(purchaseAmt=repay_amt, type='2')
            coupon_id = self.entity.current_coupon_id

            the_day_after_tomorrow = Utility.DateUtil().getToday() + datetime.timedelta(days=2)
            self.entity.creditcard_repay_schedule(repaymentAmt=repay_amt, cardSerialNo=card_serial_no,
                                                  repaymentDate=str(the_day_after_tomorrow.strftime('%Y%m%d')),
                                                  couponIds=coupon_id)
            serial_no = self.entity.current_repay_serialno
            self.entity.trade_confirm(serialNo=serial_no, password=trade_password)
        except:
            pass

    # 信用卡删除
    def creditcard_delete(self, user_name, password, trade_password, card_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.creditcard_delete_card(cardSerialNo=card_id)
            serial_no = self.entity.current_delete_bank_card_serialno
            self.entity.trade_confirm(serialNo=serial_no, password=trade_password)
        except:
            pass

    # 我的积分
    def my_points(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.my_points()
        except:
            pass

    # 获取基金经理
    def get_fund_manager_info(self, user_name, password, fundId):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_fund_manager_info(fundId=fundId)
            return self.entity.current_entity.productInfo_productid
        except:
            pass

    # 信用卡预约取消
    def cacel_credit_card_repay_order(self, user_name, password, order_serial_no):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.creditcard_yycanel(yyRepayId=order_serial_no)
        except:
            pass

    # 信用卡还款记录
    def credit_card_repay_record_list(self, user_name, password, bank_card_id, card_type):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.creditcard_repay_record(bankCardId=bank_card_id, cardType=card_type)
        except:
            pass

    # 信用卡默认还款日
    def credit_card_default_repay_date(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.creditcard_default_repay_date()
        except:
            pass

    # 信用卡真实还款日
    def credit_card_actual_repay_date(self, user_name, password, repay_date):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.creditcard_actual_repay_date(repayDate=repay_date)
        except:
            pass

    # 积分定投计划制定成功后积分扣减情况
    def fund_used_points_investment_plan(self, user_name, password, fund_id, purchase_amt):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.fund_used_points_investment_plan(fundId=fund_id, purchaseAmt=purchase_amt)

            return self.entity.current_entity.fundRate_costSaving
        except:
            pass

    # 保存基金组合百分比
    def save_fund_combination(self, user_name, password, object_ids, percents):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.save_fund_combination(objectIds=object_ids, percents=percents)
        except:
            pass

    # 信用卡还款提醒
    def credit_card_set_reminder(self, user_name, password, card_id, open_type, repay_reminder_date):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.creditcard_set_repay_reminder(cardSerialNo=card_id, openType=open_type,
                                                      repayRemindDate=repay_reminder_date)
        except:
            pass

    # 取现额度查询 bank_serial_id来自于cif_bank_card_info的serial_id
    def debit_card_withdraw_limit(self, user_name, password, bank_serial_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.card_withdraw_limit(bankCardId=bank_serial_id)
        except:
            pass

    # 获取精品推荐的产品代码
    def get_market_index(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)

            # 获取精品推荐的产品代码
            self.entity.market_index_list()

        except:
            pass

    # 查看产品的剩余额度
    def product_left_amt(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)

            # 获取精品推荐的产品代码
            entity = self.entity.market_index_list()

            product_ids = entity.productId
            product_id = ""
            for i in range(0, len(product_ids)):
                if i == len(product_ids) - 1:
                    product_id = product_id + str(product_ids[i])
                else:
                    product_id = product_id + str(product_ids[i]) + ","

            self.entity.product_left_amount(productIds=product_id)

        except:
            pass

    # 买入费率计算
    def trade_caltFee(self, user_name, password, purchase_amt, fund_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.trade_calt_fee(purchaseAmt=purchase_amt, fundId=fund_id)

        except:
            pass

    # 基金申购费率
    def get_fund_purchase_fee(self, user_name, password, fund_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_fund_purchase_rate(fundId=fund_id)

        except:
            pass

    # 取现提示文案
    def with_draw_tip_info(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.with_draw_tip_info()

        except:
            pass

    # 充值提示文案
    def recharge_tip_info(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.recharge_tip_info()

        except:
            pass

    # 基金-卖出 费用估算
    def trade_calculate_value(self, user_name, password, redeem_amt, fund_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.trade_fund_calculate_value(redeemAmt=redeem_amt, fundId=fund_id)
        except:
            pass

    # 联名卡激活
    def joint_card_acitvate(self, card_no, mobile, name, cert_type, cert_no, mobile_code=None):
        try:

            self.entity.get_joint_card_mobile_code(cardNo=card_no, mobile=mobile, name=name,
                                                   certType=cert_type,
                                                   certNo=cert_no)
            serial_no = self.entity.current_get_mobile_code_serialno
            if mobile_code is None:
                mobile_code = self.entity.current_mobile_code

            self.entity.activate_joint_card(mobileCode=mobile_code, serialNo=serial_no)
        except:
            pass

    # 是否为联名卡
    def is_joint_card(self, user_name, password, card_no):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.is_joint_card(bankAcco=card_no)

        except:
            pass

    # 获取用户联名卡列表
    def get_cust_joint_card_list(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_joint_card_list()
        except:
            pass

    # 获取用户联名卡详细信息
    def get_cust_joint_card_detail(self, user_name, password, bank_card_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.joint_card_details(bankCardId=bank_card_id)
        except:
            pass

    # 设置联名卡限额
    def set_joint_card_limit(self, user_name, password, limit_type, limit_amt, bank_card_id, trade_password):
        try:
            self.login(user_name=user_name, password=password)
            entity = self.entity.set_joint_card_limits(limitType=limit_type, limitAmt=limit_amt,
                                                       bankCardId=bank_card_id)

            serial_no = entity.body_serialNo
            self.entity.joint_card_confirm_limits(serialNo=serial_no, tradePassword=trade_password)
        except:
            pass

    # 账户交易密码验证
    def trade_password_validate(self, user_name, password, trade_password):
        try:
            self.entity.login(user_name=user_name, password=password)

            self.entity.trade_password_validate(tradePassword=trade_password)

        except:
            pass

    # 删除银行卡
    def delete_card_confirm(self, user_name, password, serial_no, trade_password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.delete_card_confirm(serialNo=serial_no, tradePassword=trade_password)
        except:
            pass

    # 删除银行卡验证
    def delete_bank_card(self, user_name, password, trade_password, bank_card_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.delete_bank_card(bankCardId=bank_card_id)
            serial_no = self.entity.current_delete_bank_card_serialno
            self.entity.delete_card_confirm(serialNo=serial_no, tradePassword=trade_password)
        except:
            pass

    # 现金宝累计收益
    def xjb_last_profit(self, user_name, password, page_no, page_size):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.xjb_last_profit(pageNo=page_no, pageSize=page_size)
        except:
            pass

    # 退出
    def logout(self):
        try:
            self.entity.logout()
        except:
            pass

    # 升级银行卡
    def bank_card_upgrade(self, user_name, password, des_bank_no, bank_card_id, bank_name, mobile_code=None):
        try:
            self.login(user_name=user_name, password=password)

            # get the bank serial id from card list
            entity = self.entity.get_cust_card_list()
            card_list = entity.cards
            for i in range(0, len(card_list)):
                if str(card_list[i]['bankGroupName']) == bank_name:
                    bank_card_id = str(card_list[i]['bankCardId'])
                    break
            try:
                entity = self.entity.get_mobile_code_upgrade(desBankNo=des_bank_no, bankCardId=bank_card_id,
                                                             mobile=user_name)
            except Exception:
                # 如果短信发送频繁，会报错，所以如果碰到这个错，就等待1分钟后再试。
                sleep(60)
                entity = self.entity.get_mobile_code_upgrade(desBankNo=des_bank_no, bankCardId=bank_card_id,
                                                             mobile=user_name)
            serial_no = entity.body_serialNo
            if mobile_code is None:
                # right now it is hard code, since it is very slow to get the result from db.
                if bank_name == '浦发银行':
                    # 短信由银行发出。
                    mobile_code = self.mysql.get_mobile_code_send_by_bank(mobile=user_name)
                else:
                    # 由华信发出
                    mobile_code = self.mysql.get_sms_verify_code(mobile=user_name,
                                                                 template_id='cif_bindBankCard')
            confirm_entity = self.entity.get_mobile_code_upgrade_confirm(mobileCode=mobile_code, serialNo=serial_no)

            if bank_name == '交通银行' or bank_name == '邮储银行' or bank_name == '广发银行' \
                    or bank_name == '中信银行' or bank_name == '光大银行':
                serial_no1 = confirm_entity.body_serialNo
                if bank_name == '光大银行':
                    self.entity.ceb_binding_gateway_h5_page()
                    self.entity.ceb_binding_submit()
                for i in range(1, 15):
                    result = self.entity.binding_result(serialNo=serial_no1)

                    sleep(1)
                    auth_result = result.authResult
                    if str(auth_result) == 'Y':
                        break

        except:
            pass

    # 我的预约码
    def my_reservation_code(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.my_reservation_code()
        except:
            pass

    # 查询预约码
    def query_reserve_code(self, user_name, password, reservation_code):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.query_reserve_code(reservationCode=reservation_code)
        except:
            pass

    # 基金，高端，定期宝持仓资产
    def my_hold_asset(self, user_name, password, product_type):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.my_hold_asset(productType=product_type)
        except:
            pass

    # 绑卡-查询所有通道信息
    def check_all_bank_channel_list(self, user_name, password, cert_type):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.check_all_bank_channel_list(certType=cert_type)
        except:
            pass

    # 设置自选基金
    def set_fav_fund(self, user_name, password, object_ids, fav_type):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.set_fav_fund(objectIds=object_ids, favType=fav_type)
        except:
            pass

    # 基金12大分类
    def fund_twelve_part(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.fund_twelve_part()
        except:
            pass

    # 获取优惠券数量信息
    def get_coupon_info(self, user_name, password, product_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_coupon_info(productId=product_id)
        except:
            pass

    # 计算可用积分
    def can_used_points_count(self, user_name, password, product_id, amt, coupon_ids, is_use_points):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.can_used_points_count(productId=product_id, amt=amt, couponIds=coupon_ids,
                                              isUsePoints=is_use_points)

        except:
            pass

    # 积分-优惠券列表
    def points_discount_coupon(self, user_name, password, purchase_amt, product_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.points_discount_coupon(purchaseAmt=purchase_amt, productId=product_id)
        except Exception, e:
            print repr(e)
            pass

    # 申购高端撤单
    def purchase_then_cancel(self, user_name, password, purchase_amt, product_id, trade_password, coupon_ids):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.purchase_product(productId=product_id,
                                         amt=purchase_amt,
                                         couponIds=coupon_ids
                                         )
            serial_no = self.entity.current_purchase_product_serialno

            self.entity.trade_confirm(serialNo=serial_no,
                                      password=trade_password,
                                      )
            trade_req, trade_order = self.mysql.get_trade_request(mobile=user_name)
            order_no = trade_order[0]['ORDER_NO']

            # 撤单
            entity = self.entity.revoke_validate(tradeSerialNo=str(order_no))
            serial_no = entity.body_serialNo
            self.entity.trade_confirm(serialNo=serial_no,
                                      password=trade_password,
                                      )
        except:
            pass

    # 查询交易详情
    def query_trade_detail(self, user_name, login_password, trade_serial_no):
        try:
            self.login(user_name=user_name, password=login_password)
            self.entity.query_trade_detail(tradeSerialNo=str(trade_serial_no))
        except:
            pass

    # 热门产品列表
    def hot_product_list(self, user_name, password):
        try:
            if user_name is not '':
                self.login(user_name=user_name, password=password)
            self.entity.hot_product_list()
        except:
            pass

    # 定期产品列表
    def dqb_product_list(self, user_name, password):
        try:
            if user_name is not '':
                self.login(user_name=user_name, password=password)
            self.entity.dqb_product_list()
        except:
            pass

    # 高端产品列表
    def vip_product_list(self, user_name, password):
        try:
            if user_name is not '':
                self.login(user_name=user_name, password=password)
            self.entity.vip_product_list()
        except:
            pass

    # 设置合格投资者
    def set_qualified_investor(self, user_name, password):
        try:
            if user_name is not '':
                self.login(user_name=user_name, password=password)
            self.entity.set_qualified_investor()
        except:
            pass

    # 首页收益信息
    def get_index_income_info(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_index_income_info()
        except:
            pass

    # 我的定期宝产品详情
    def my_dqb_detail(self, user_name, password, order_no, product_id, holding_type):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.my_dqb_detail(orderNo=order_no, productId=product_id, holdingType=holding_type)
        except:
            pass

    # 我的高端产品详情
    def my_vip_detail(self, user_name, password, order_no, product_id, holding_type):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.my_vip_detail(orderNo=order_no, productId=product_id, holdingType=holding_type)
        except:
            pass

    # 我的基金产品详情
    def my_fund_detail(self, user_name, password, order_no, fund_id, holding_type):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.my_fund_detail(orderNo=order_no, fundId=fund_id, holdingType=holding_type)
        except:
            pass

    # 获取用户基本信息
    def get_cust_base_info(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_cust_base_info()
        except:
            pass

    # 搜索所有产品（定期、高端）
    def search_all_fin_product(self, user_name, password, keyword):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.search_all_fin_product(keyword=keyword)
        except:
            pass

    # 积分+优惠券购买产品
    def buy_product_using_coupon_points(self, user_name, login_password, product_id, pay_amount, coupon_ids, points,
                                        is_use_points, trade_password):
        try:
            self.login(user_name=user_name, password=login_password)

            entity = self.entity.can_used_points_count(productId=product_id, amt=pay_amount, couponIds=coupon_ids,
                                                       isUsePoints=is_use_points)
            self._cms.issue_coupon(code='FULL_OFF_100_12_0062', mobile=user_name, quantity=2)
            pay_amt = entity.payAmt
            if points == '':
                points = entity.pointsCount
            self.entity.purchase_product(productId=product_id,
                                         amt=pay_amount,
                                         points=points,
                                         payAmt=pay_amt,
                                         couponIds=coupon_ids
                                         )
            serial_no = self.entity.current_purchase_product_serialno

            self.entity.trade_confirm(serialNo=serial_no,
                                      password=trade_password,
                                      )
            return points
        except:
            pass

    # 个人质押信息
    def trade_load_info(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.trade_load_info()
        except:
            pass

    # 交易-我的质押列表
    def my_loan_list(self, user_name, password, is_history):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.trade_my_loan_list(isHistory=is_history)
        except Exception, e:
            print e
            pass

    # 交易-可质押产品详情
    def trade_get_loan_apply_info(self, user_name, password, product_id, loan_amt):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.trade_get_loan_apply_info(productId=product_id, loanAmt=loan_amt)
        except Exception, e:
            print e
            pass

    # 高端赎回费率
    def vip_redeem_rate(self, user_name, login_password, product_id, redeem_amt):
        try:
            self.login(user_name=user_name, password=login_password)
            self.entity.vip_redeem_rate(productId=product_id, redeemAmt=redeem_amt)
        except Exception, e:
            print e
            pass

    # 高端申购费率
    def vip_purchase_rate(self, user_name, login_password, product_id, purchase_amt):
        try:
            self.login(user_name=user_name, password=login_password)
            self.entity.vip_purchase_rate(productId=product_id, purchaseAmt=purchase_amt)
        except:
            pass

    # 基金定投计划
    def fund_make_invest_plan(self, user_name, password, fundId, payType, eachInvestAmt, payCycle, payDay,
                              isConfirmBeyondRisk, trade_password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.fund_make_invest_plan_validate(fundId=fundId, payType=payType, eachInvestAmt=eachInvestAmt,
                                                       payCycle=payCycle, payDay=payDay,
                                                       isConfirmBeyondRisk=isConfirmBeyondRisk)
            serial_no = self.entity.current_entity.body_serialNo
            self.entity.trade_confirm(serialNo=serial_no, password=trade_password)
        except:
            pass

    # 获取基金定投列表
    def get_fund_invest_plan(self, user_name, login_password):
        try:
            self.login(user_name=user_name, password=login_password)
            entity = self.entity.get_fund_invest_plan()
            return entity
        except Exception, e:
            pass

    # 基金定投计划暂停/恢复/终止验证
    def fund_handle_invest_plan_validate(self, user_name, password, protocol_no,
                                         is_confirm_beyond_risk, type, trade_password):
        try:
            self.login(user_name=user_name, password=password)
            # entity = self.entity.get_fund_invest_plan()
            self.entity.fund_handle_invest_plan_validate(investPlanId=protocol_no,
                                                         isConfirmBeyondRisk=is_confirm_beyond_risk, type=type)
            serial_no_handle = self.entity.current_entity.body_serialNo
            self.entity.trade_confirm(serialNo=serial_no_handle, password=trade_password)
        except:
            pass

    # 基金赎回费用估算
    def fund_redeem_cost_calt_value(self, user_name, login_password, redeem_amt, product_id):
        try:
            self.login(user_name=user_name, password=login_password)
            self.entity.fund_redeem_cost_calt_value(productId=product_id, redeemAmt=redeem_amt)
        except:
            pass

    # 质押借款申请
    def loan_apply(self, user_name, login_password, product_id, loan_amt, loan_purpose, trade_password):
        try:
            self.login(user_name=user_name, password=login_password)
            entity = self.entity.trade_loan_apply(productId=product_id, loanAmt=loan_amt, loanPurpose=loan_purpose)

            serial_no = entity.body_serialNo
            self.entity.trade_confirm(serialNo=serial_no, password=trade_password)
        except:
            pass

    # 可质押产品列表
    def loan_product_list(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_loan_product_list()
        except:
            pass

    # 获取协议
    def get_agreenment(self, user_name, password, type):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_agreements(type=type)
        except:
            pass

    # 工资理财-查询下个扣款日
    def get_next_pay_day(self, user_name, password, pay_day):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_next_pay_day(payDay=pay_day)
        except:
            pass

    # 工资理财-创建/修改工资理财计划
    def make_salary_fin_plan(self, user_name, password, salary_fin_plan_id, card_id, purchase_amt, purchase_date,
                             comment, trade_password):
        try:
            self.login(user_name=user_name, password=password)
            if card_id == '':
                card_list = self.entity.get_cust_card_list()
                card_id = card_list.cards[0]['']
            entity = self.entity.make_salary_fin_plan(salaryFinPlanId=salary_fin_plan_id, cardId=card_id,
                                                      purchaseAmt=purchase_amt,
                                                      purchaseDate=purchase_date, comment=comment)
            serial_no = entity.body_serialNo
            self.entity.trade_confirm(serialNo=serial_no, password=trade_password)
        except:
            pass

    # 工资理财-终止、启用、暂停工资理财计划
    def update_salary_fin_plan(self, user_name, password, trade_password, salary_fin_plan_id, status):
        try:
            self.login(user_name=user_name, password=password)
            entity = self.entity.update_salary_fin_plan(salaryFinPlanId=salary_fin_plan_id, status=status)
            serial_no = entity.body_serialNo
            self.entity.trade_confirm(serialNo=serial_no, password=trade_password)
        except:
            pass

    # 获取工资理财计划
    def get_salary_fin_plan(self, user_name, password, is_history):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_salary_fin_plan(isHistory=is_history)
        except:
            pass

    # 工资代发-确认协议
    def confirm_salary_fin_plan(self, user_name, password, employee_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.confirm_salary_fin_plan(employeeId=employee_id)
        except:
            pass

    # 会员等级-查询指定等级权益
    def get_member_level_right_list(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_member_level_right_list()
        except:
            pass

    # 会员等级-查询指定权益详情
    def get_member_level_right_detail(self, user_name, password, rights_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_member_level_right_detail(rightsId=rights_id)
        except:
            pass

    # 会员等级-查询特殊权益
    def get_member_level_right_category_list(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_member_level_right_category_list()
        except:
            pass

    # 用户-保存会员等级banner浏览结果
    def get_view_member_level_banner(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.view_member_level_banner()
        except:
            pass

    # 用户-行为记录（提醒我）
    def get_save_behavior(self, user_name, password, product_type, sub_product_type):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.save_behavior(productType=product_type, subProductType=sub_product_type)
        except:
            pass

    # 工资代发-终止协议
    def stop_salary_fin_plan(self, user_name, password, employee_id, trade_password):
        try:
            self.login(user_name=user_name, password=password)
            entity = self.entity.stop_salary_fin_plan_validate(employeeId=employee_id)
            serial_no = entity.body_serialNo
            self.entity.stop_salary_fin_plan(serialNo=serial_no, password=trade_password)
        except:
            pass

    # 工资代发-获取工资卡信息
    def get_salary_card_info(self, user_name, password, employee_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_salary_card_info(employeeId=employee_id)
        except:
            pass

    # 高端质押产品详情
    def trade_loan_product_detail(self, user_name, password, product_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.trade_loan_product_detail(productId=product_id)
        except:
            pass

    # banner
    def marketing_banner(self, user_name, password, position):
        try:
            if user_name != '' and password != '':
                self.login(user_name=user_name, password=password)
            self.entity.marketing_index_banner(position=position)
        except:
            pass

    # alert
    def marketing_main_page_alert(self, user_name, password, visit_type):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.marketing_main_page_alert(visitType=visit_type)
        except:
            pass

    # 产品-理财产品介绍(v3.0.0)
    # 0-热门 1-定活宝 2-高端 3-固定 4-现金管理 5-精选权益系列
    def get_product_intro(self, user_name, password, common_info_type):
        try:
            if user_name != '' and password != '':
                self.login(user_name=user_name, password=password)
            self.entity.get_product_info(commonInfoType=common_info_type)
        except:
            pass

    # 产品-热门理财产品(v3.0.0)
    def get_hot_product_list(self, user_name, password):
        try:
            if user_name != '' and password != '':
                self.login(user_name=user_name, password=password)
            self.entity.get_hot_product_list()
        except Exception, e:
            pass

    # 产品-理财产品列表(v3.0.0)
    def get_product_list(self, user_name, password, product_type, high_series_type, is_history):
        try:
            if user_name != '' and password != '':
                self.login(user_name=user_name, password=password)
            self.entity.get_product_list(productType=product_type, highSeriesType=high_series_type,
                                         isHistory=is_history)
        except:
            pass

    # 功能
    def get_function_list(self, user_name, password, function_type):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_function_list(functionType=function_type)
        except:
            pass

    # 首页-产品营销信息
    def get_product_marketing_info(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_product_marketing_info()
        except:
            pass

    # 首页-资讯
    def get_doc_list(self, user_name, password, doc_type, position, page_no, page_size):
        try:
            # self.login(user_name=user_name, password=password)
            self.entity.get_doc_list(docType=doc_type, position=position, pageNo=page_no, pageSize=page_size)
        except:
            pass

    # 搜索所有产品（定期、高端、基金）
    def search_all_product(self, user_name, password, keyword):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.search_all_product(keyword=keyword)
        except:
            pass

    # 基金-定投计划详情
    def get_fund_invest_plan_detail(self, user_name, password, invest_plan_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.fund_invest_plan_detail(investPlanId=invest_plan_id)
        except:
            pass

    # 账户-查询电子签名约定书信息
    def get_signature_agreement_info(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_signature_agreement_info()
        except:
            pass

    # 查询工资理财计划详情
    def get_salary_plan_detail(self, user_name, password, salary_fin_plan_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_salary_fin_plan_detail(salaryFinPlanId=salary_fin_plan_id)
        except:
            pass

    # 工资代发-匹配工资卡信息
    def match_salary_card(self, user_name, password, cert_no, employee_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.match_salary_card(certNo=cert_no, employeeId=employee_id)
        except:
            pass

    # 交易-高端极速赎回提示信息(V2.0)
    def get_vip_product_fast_redeem_tip(self, user_name, password, product_id, sold_share):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_vip_product_fast_redeem_tip(productId=product_id, soldShare=sold_share)
        except:
            pass

    # 注册-注册信息验证
    def register_verify_id(self, id_no, real_name, serial_no):
        try:
            self.entity.register_verify_id(idNo=id_no, realName=real_name, serialNo=serial_no)
        except:
            pass

    # 还贷-创建/修改还贷计划
    def make_plan(self, user_name, password, repay_plan_id, repay_type, card_id, repay_amt, repay_date, repay_count,
                  trade_password):
        try:
            self.login(user_name=user_name, password=password)
            entity = self.entity.make_plan_validate(repayPlanId=repay_plan_id, repayType=repay_type, cardId=card_id,
                                                    repayAmt=repay_amt, repayDate=repay_date, repayCount=repay_count)

            # serial_no = entity.body_serialNo
            # self.entity.get_face_recognition_validate(serialNo=serial_no, imageId=image_id)
            serial_no = entity.body_serialNo
            self.entity.make_plan(serialNo=serial_no, tradePassword=trade_password)
        except:
            pass

    # 还贷-查询还款计划列表
    def get_plan_list(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_plan_list()
        except:
            pass

    # 还贷-查询还款计划详情
    def get_plan_detail(self, user_name, password, repay_plan_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_plan_detail(repayPlanId=repay_plan_id)
        except:
            pass

    # 还贷-还贷准入
    def repay_check(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.repay_check()
        except:
            pass

    # 还贷-查询还款提示
    def get_repay_tip(self, user_name, password, repay_date):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_repay_tip(repayDate=repay_date)
        except:
            pass

    # 还贷-提额校验
    def check_raise_quota(self, user_name, password, card_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.check_raise_quota(card_id=card_id)
        except:
            pass

    # 还贷-启用/暂停/删除还贷计划
    def update_plan(self, user_name, password, repay_plan_id, status, trade_password):
        try:
            self.login(user_name=user_name, password=password)
            entity = self.entity.update_plan_validate(repayPlanId=repay_plan_id, status=status)
            serial_no = entity.body_serialNo
            self.entity.update_plan(serialNo=serial_no, tradePassword=trade_password)
        except:
            pass

    # 账户-产品风险验证
    def get_risk_validate(self, user_name, password, product_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_risk_validate(productId=product_id)
        except Exception, e:
            pass

    # 账户-风险测评发送短信
    def get_risk_get_mobile_code(self, user_name, password, product_id):
        try:
            self.login(user_name=user_name, password=password)
            entity = self.entity.get_risk_validate(productId=product_id)
            serial_no = entity.body_serialNo
            self.entity.risk_get_mobile_code(mobile=user_name, serialNo=serial_no)
        except:
            pass

    # 账户-查询登录历史
    def get_login_history(self, user_name, password, page_no, page_size):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_login_history(pageNo=page_no, pageSize=page_size)
        except Exception, e:
            pass

    # 安全-交易密码校验(V3.1)
    def get_trade_password_validate(self, user_name, password, repay_plan_id, loan_type, card_id, repay_amt, repay_date,
                                    repay_count, trade_password):
        try:
            self.login(user_name=user_name, password=password)
            entity = self.entity.make_plan_validate(repayPlanId=repay_plan_id, loanType=loan_type, cardId=card_id,
                                                    repayAmt=repay_amt, repayDate=repay_date, repayCount=repay_count)

            serial_no = entity.body_serialNo
            self.entity.get_trade_password_validate(serialNo=serial_no, tradePassword=trade_password)
        except:
            pass

    # 安全-发送短信验证码(V3.1)
    def send_sms_code(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            entity = self.entity.current_entity
            serial_no = entity.body_serialNo
            self.entity.send_sms_code(serialNo=serial_no, mobile=user_name)
        except:
            pass

    # 安全-短信验证码校验(V3.1)
    def get_sms_code_validate(self, user_name, password, sms_code):
        try:
            self.login(user_name=user_name, password=password)
            entity = self.entity.current_entity
            serial_no = entity.body_serialNo
            self.entity.get_sms_code_validate(serialNo=serial_no, smsCode=sms_code)
        except:
            pass

    # 安全-人脸识别校验(V3.1)
    def get_face_recognition_validate(self, user_name, password, repay_plan_id, repay_type, card_id, repay_amt,
                                      repay_date, repay_count, image_id):
        try:
            self.login(user_name=user_name, password=password)
            entity = self.entity.make_plan_validate(repayPlanId=repay_plan_id, repayType=repay_type, cardId=card_id,
                                                    repayAmt=repay_amt, repayDate=repay_date, repayCount=repay_count)
            serial_no = entity.body_serialNo
            self.entity.get_face_recognition_validate(serialNo=serial_no, imageId=image_id)
        except Exception, e:
            pass

    # 基金-设置基金自选
    def add_fav(self, user_name, password, fund_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.add_fav(fundId=fund_id)
        except:
            pass

    # 基金-删除基金自选
    def del_fav(self, user_name, password, fund_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.del_fav(fundId=fund_id)
        except:
            pass

    # 修改分红方式
    def set_melon_type(self, user_name, password, fund_id, share_type):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.set_melon_type(fundId=fund_id, shareType=share_type)
        except:
            pass

    # 获取下一扣款日期
    def get_fund_next_pay_day(self, user_name, password, fund_id, pay_cycle, pay_day):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_fund_next_pay_day(fundId=fund_id, payCycle=pay_cycle, payDay=pay_day)
        except:
            pass

    # 基金-研究报告
    def research_report(self, user_name, password):
        try:
            # self.login(user_name=user_name, password=password)
            self.entity.research_report()
        except:
            pass

    # 基金-机构观点
    def org_view_point(self, user_name, password):
        try:
            # self.login(user_name=user_name, password=password)
            self.entity.org_view_point()
        except:
            pass

    # 基金-达人论基
    def intelligent_say(self, user_name, password):
        try:
            # self.login(user_name=user_name, password=password)
            self.entity.intelligen_say()
        except:
            pass

    # 积分-我的优惠券列表(V2.3)
    def get_my_coupon_list(self, user_name, password, is_history, page_no, page_size):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_my_coupon_list(isHistory=is_history, pageNo=page_no, pageSize=page_size)
        except Exception, e:
            pass

    # 基金-专家开讲
    def expert_say(self, user_name, password):
        try:
            # self.login(user_name=user_name, password=password)
            self.entity.expert_say()
        except:
            pass

    # 通用-保存附件信息（V3.1）
    def save_attachment(self, user_name, password, send_type, mobile, type):
        try:
            self.login(user_name=user_name, password=password)
            if type == '2':
                entity = self.entity.assert_cert_apply(sendType=send_type, mobile=user_name)
                serial_no = entity.body_serialNo
                self.entity.save_attachment(serialNo=serial_no, type=type)
            else:
                self.entity.save_attachment(type=type)
        except Exception, e:
            pass

    # 消息中心-查询消息分类(V3.1)
    def get_message_category_list(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_message_category_list()
        except Exception, e:
            pass

    # 消息中心-查询消息列表(V3.1)
    def get_category_message_list(self, user_name, password, category_no, page_no, page_size):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_category_message_list(categoryNo=category_no, pageNo=page_no, pageSize=page_size)
        except:
            pass

    # 现金宝在途资产
    def xjb_transit_asset(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.xjb_transit_asset()
        except:
            pass

    # 全部理财产品列表
    def get_all_fin_product_list(self, user_name, password, period_id, product_type_id, min_invest_amt_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.product_get_all_fin_product_list(periodId=period_id, productTypeId=product_type_id,
                                                         minInvestAmtId=min_invest_amt_id)
        except:
            pass

    # 全部理财产品检索条件
    def get_fin_product_search_condition_group_list(self, user_name, password, group_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.product_search_condition_group_list(groupId=group_id)
        except:
            pass

    # 获取现金管理支付列表
    def get_payment_list(self, user_name, password, product_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_payment_list(productId=product_id)
        except:
            pass

    # 中信联名卡申请基础校验发送
    def jointcard_apply_brand_sendsms(self, user_name, password, mobile, id_no, english_name, brand_type,
                                      brand_source):
        try:
            self.login(user_name=mobile, password=password)
            token = self.entity.current_login_token
            self.entity.check_token(token=token)
            self.entity.jointcard_apply_brand_sendsms(userName=user_name, mobile=mobile, idNo=id_no,
                                                      englishName=english_name, brandSource=brand_source,
                                                      brandType=brand_type)

        except:
            pass

    # 中信联名卡申请基础校验提交
    def joint_card_apply_brand_validate(self, user_name, mobile, id_no, english_name, auth_code, serial_no, brand_type,
                                        brand_source
                                        ):
        try:
            self.entity.joint_card_apply_brand_validate(userName=user_name, mobile=mobile, idNo=id_no,
                                                        englishName=english_name, authCode=auth_code,
                                                        brandSource=brand_source,
                                                        brandType=brand_type,
                                                        serialNo=serial_no)
        except:
            pass

    # 中信联名卡预申请
    def joint_card_apply_brand_pre_submit(self, home_pc_ids, home_pc_names, home_area, email, corp_zone,
                                          company_pc_ids, corp_name, company_pc_names, company_area, corp_tel,
                                          serial_no, brand_source, brand_type):
        try:
            self.entity.joint_card_apply_brand_pre_submit(homePcIds=home_pc_ids, homePcNames=home_pc_names,
                                                          homeArea=home_area, corpName=corp_name,
                                                          email=email,
                                                          companyPcIds=company_pc_ids,
                                                          companyPcNames=company_pc_names,
                                                          companyArea=company_area, corpZone=corp_zone,
                                                          brandSource=brand_source,
                                                          brandType=brand_type,
                                                          serialNo=serial_no,
                                                          corpTel=corp_tel)
        except:
            pass

    # 中信联名卡申请
    def joint_card_apply_brand_submit(self, contact_name, contact_rel, contact_rel_nm, contact_mobile,
                                      ins_contact_name, ins_contact_rel, ins_contact_rel_nm, ins_contact_mobile,
                                      serial_no):
        try:
            self.entity.joint_card_apply_brand_submit(contactName=contact_name, contactRel=contact_rel,
                                                      contactRelNm=contact_rel_nm, contactMobile=contact_mobile,
                                                      insContactName=ins_contact_name,
                                                      insContactRel=ins_contact_rel,
                                                      insContactRelNm=ins_contact_rel_nm,
                                                      insContactMobile=ins_contact_mobile, serialNo=serial_no)
        except:
            pass

    # 消息中心-关闭消息推送(V3.1)
    def close_push(self, user_name, password, category_no, status):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.close_push(categoryNo=category_no, status=status)
        except:
            pass

    # 中信联名卡激活
    def activate_citic_card(self, user_name, password, card_no, brand_type, bank_no):
        try:
            self.login(user_name=user_name, password=password)
            entity = self.entity.citic_activation_send_mobile_code(mobile=user_name, cardNo=card_no,
                                                                   brandType=brand_type,
                                                                   bankNo=bank_no)
            serial_no = entity.body_serialNo
            mobile_code = self.mysql.get_sms_verify_code(mobile=user_name, template_id='credit_activate_citicb')
            self.entity.citic_activation_citic_card(serialNo=serial_no, mobileCode=mobile_code)
        except:
            pass

    # 积分-优惠券有效性校验(V3.1)
    def my_coupon_validate(self, user_name, password, coupon_id, accept_mode):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.my_coupon_validate(couponId=coupon_id, acceptMode=accept_mode)
        except:
            pass

    # 现金管理作为支付手段购买产品
    def buy_product_using_cash_management(self, user_name, login_password, product_id, pay_type, amt,
                                          pay_product_id, trade_password):
        try:
            self.login(user_name=user_name, password=login_password)
            entity = self.entity.purchase_product(productId=product_id, amt=amt, payType=pay_type,
                                                  payProductId=pay_product_id)
            serial_no = entity.body_serialNo
            self.entity.trade_confirm(serialNo=serial_no, password=trade_password)
        except Exception, e:
            print e
            pass

    # 账户-资产证明申请(V1.6)
    def assert_cert_apply(self, user_name, password, send_type, mobile):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.assert_cert_apply(sendType=send_type, mobile=user_name)
        except:
            pass

    # 基金-市场指数
    def maket_exponent(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.maket_exponent()
        except:
            pass

    # 基金-首页沪深指数
    def csi_exponent(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.csi_exponent()
        except:
            pass

    # 基金-评级机构列表
    def get_grade_orglist(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_grade_orglist()
        except:
            pass

    # 基金-Shibor
    def get_shibor_exponent(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_shibor_exponent()
        except:
            pass

    # 账户-资产证明预览
    def get_asset_cert_preview(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_asset_cert_preview()
        except:
            pass

    # 账户-登录是否显示图片验证码
    def is_display_captcha_code(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.is_display_captcha_code()
        except:
            pass

    # 账户-查询交易密码审核状态信息
    def trade_password_check_info(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.trade_password_check_info()
        except:
            pass

    # 账户-二维码保存到本地
    def save_to_local(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.save_to_local()
        except:
            pass

    # 交易-高端报价式年化业绩比较基准
    def vip_rate_history(self, user_name, password, product_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.vip_rate_history(productId=product_id)
        except:
            pass

    # 交易-高端报价式产品修改到期处理方式
    def modify_expire_dispose_type(self, user_name, password, expire_dispose_type, expire_quit_amt, product_id,
                                   value_date, trade_password):
        try:
            self.login(user_name=user_name, password=password)
            entity = self.entity.modify_expire_dispose_type(expireDisposeType=expire_dispose_type,
                                                            expireQuitAmt=expire_quit_amt,
                                                            productId=product_id, valueDate=value_date)
            serial_no = entity.body_serialNo
            self.entity.trade_confirm(serialNo=serial_no, password=trade_password)

        except:
            pass

    # 交易-高端报价式产品修改到期处理方式提示信息
    def modify_expire_dispose_type_tip(self, user_name, password, expire_dispose_type, product_id, value_date,
                                       expire_date):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.modify_expire_dispose_type_tip(expireDisposeType=expire_dispose_type, productId=product_id,
                                                       valueDate=value_date, expiryDate=expire_date)

        except:
            pass

    # 账户-查询修改手机号码审核状态信息
    def get_modify_mobile_check_info(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_modify_mobile_check_info()
        except:
            pass

    # 账户-资产证明申请记录
    def get_assert_cert_apply_record(self, user_name, password, page_size):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_assert_cert_apply_record(pageSize=page_size)
        except:
            pass

    # 账户 - 资产证明发送方式tip
    def get_asset_send_type_info(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_asset_send_type_info()
        except:
            pass

    # 账户-查询个人账户信息
    def get_account_info(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_account_info()
        except:
            pass

    # 账户-查询我的邀请人
    def query_my_inviter(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.query_my_inviter()
        except:
            pass

    # 账户-设置我的邀请人
    def set_my_inviter(self, user_name, password, mobile):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.set_my_inviter(mobile=mobile)
        except:
            pass

    # 账户-获取省市
    def get_province_and_city(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_province_and_city()
        except:
            pass

    # 账户-修改用户基本信息
    def update_cust_base_info(self, user_name, password, email, address, pcIds, area):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.update_cust_base_info(email=email, address=address, pcIds=pcIds, area=area)
        except:
            pass

    # 交易-质押还款明细
    def loan_repay_detail_list(self, user_name, password, my_loan_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.loan_repay_detail_list(myLoadId=my_loan_id)
        except:
            pass

    # 交易-质押还款申请
    def loan_repay_apply(self, user_name, password, product_id, my_loan_id, repay_capital_amt, repay_amt,
                         trade_password):
        try:
            self.login(user_name=user_name, password=password)
            entity = self.entity.loan_repay_apply(productId=product_id, myLoadId=my_loan_id,
                                                  repayCapitalAmt=repay_capital_amt, repayAmt=repay_amt)
            serial_no = entity.serialNo
            self.entity.trade_confirm(serialNo=serial_no, password=trade_password)
        except:
            pass

    # 交易-获取质押利息和总金额
    def get_loan_repay_info(self, user_name, password, my_loan_id, repay_capital_amt):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_loan_repay_info(myLoadId=my_loan_id, repayCapitalAmt=repay_capital_amt)
        except:
            pass

    # 通用-全局版本号
    def get_version(self, user_name, password, type):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_version(type=type)
        except:
            pass

    # 基金-极速赎回说明
    def fast_redeem_info(self, user_name, password, sold_share, fund_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.fast_redeem_info(soldShare=sold_share, fundId=fund_id)
        except:
            pass

    # 获取赎回费率
    def get_fund_redeem_rate(self, user_name, password, fund_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_fund_redeem_rate(fundId=fund_id)
        except:
            pass

    # 基金-tip
    def fund_tip(self, user_name, password, tip_type, fund_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.fund_tip(tipType=tip_type, fundId=fund_id)
        except:
            pass

    # 通用-上传地理位置
    def upload_geographic_location(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.upload_geographic_location()
        except:
            pass

    # 基金-货币类月、季、年收益曲线
    def mf_chart_info(self, user_name, password, fund_id, type):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.mf_chart_info(fundId=fund_id, type=type)
        except:
            pass

    # 交易-申请预约码提交(V3.2)
    def apply_reservation_code(self, user_name, password, product_id, yy_amt, money_can_use_start_date,
                               money_can_use_end_date,
                               mobile):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.apply_reservation_code(productId=product_id, yyAmt=yy_amt,
                                               moneyCanUseStartDate=money_can_use_start_date,
                                               moneyCanUseEndDate=money_can_use_end_date,
                                               mobile=mobile)
        except:
            pass

    # 交易-查看预约码审核进度(V3.2)
    def query_reservation_code_audit_status(self, user_name, password, product_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.query_reservation_code_audit_status(productId=product_id)
        except:
            pass

    # 交易-获取搜索条件树(V3.2)
    def get_search_condition_tree(self, user_name, password, type):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_search_condition_tree(type=str(type))
        except:
            pass

    # 基金-权益类月、季，年收益曲线
    def sf_chart_info(self, user_name, password, fund_id, type):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.sf_chart_info(fundId=fund_id, type=type)
        except:
            pass

    # 基金-持有列表数据
    def my_fund_list(self, user_name, password, fund_type):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.my_fund_list(fundType=fund_type)
        except:
            pass

    # 产品-发售预告列表
    def sell_notice(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.sell_notice()
        except:
            pass

    # 产品-在售产品列表
    def sell_product_list(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.sell_product_list()
        except:
            pass

    # 信用卡-银行通道列表
    def bank_channel_list(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.bank_channel_list()
        except:
            pass

    # 基金-详情页历史回报等
    def fund_rise_info(self, user_name, password, fund_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.fund_rise_info(fundId=fund_id)
        except:
            pass

    # 基金-统计热门搜索基金
    def statistic_product_search(self, user_name, password, fund_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.static_product_search(fundId=fund_id)
        except:
            pass

    # 积分-推荐任务
    def point_recommends(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.point_recommends()
        except:
            pass

    # 积分-赚积分
    def earn_points(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.earn_points()
        except:
            pass

    # 积分-积分明细
    def points_detail(self, user_name, password, type):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.points_detail(type=type)
        except:
            pass

    # 积分-花积分
    def spend_points(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.spend_points()
        except:
            pass

    # 基金-统计热门搜索基金
    def statistic_product_search(self, user_name, password, fund_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.statistic_product_search(fundId=fund_id)
        except:
            pass

    # 积分-推荐任务
    def point_recommends(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.point_recommends()
        except:
            pass

    # 基金-对比、组合收益曲线
    def fund_compare(self, user_name, password, fund_ids, type, chart_type):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.fund_compare(fundIds=fund_ids, type=type, chartType=chart_type)
        except:
            pass

    # 积分-兑换
    def points_exchange(self, user_name, password, id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.points_exchange(id=id)
        except:
            pass

    # 产品-产品库版本号
    def product_version(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.product_version()
        except:
            pass

    # 交易-所有交易状态
    def all_trade_status(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.all_trade_status()
        except:
            pass

    # 现金宝炒股-获取资产信息-uat环境
    def get_stock_asset_info(self, user_name, password):
        try:
            self.login_uat(user_name=user_name, password=password)
            self.entity.get_stock_asset_info()
        except:
            pass

    # 信用卡-自动还款开启
    def auto_repay_open(self, user_name, password, card_serial_no):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.auto_repay_open(cardSerialNo=card_serial_no)
        except:
            pass

    # 信用卡-自动还款关闭
    def auto_repay_close(self, user_name, password, card_serial_no):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.auto_repay_close(cardSerialNo=card_serial_no)
        except:
            pass

    # 信用卡-自动还款查询
    def auto_repay_detail(self, user_name, password, card_serial_no):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.auto_repay_detail(cardSerialNo=card_serial_no)
        except:
            pass

    # 基金-公告列表
    def fund_notice_list(self, user_name, password, fund_id, notice_type):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.fund_notice_list(fundId=fund_id, noticeType=notice_type)
        except:
            pass

    # 产品-搜索定期或高端
    def search_fin_product(self, user_name, password, keyword, product_type):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.search_fin_product(keyword=keyword, productType=product_type)
        except:
            pass

    # 产品-高端产品详情
    def vip_product_detail(self, user_name, password, product_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.vip_product_detail(productId=product_id)
        except:
            pass

    # 基金-热搜关键词
    def fund_trending(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.fund_trending()
        except:
            pass

    # 普卡-卡状态信息(兼容是否联名卡接口)
    def card_status_info(self, user_name, password, bank_acco):
        try:
            self.login(user_name=str(user_name), password=str(password))
            self.entity.card_status_info(bankAcco=str(bank_acco))
        except:
            pass

    # 产品-高端权益类月、季，年收益曲线
    def vip_product_sfchart_info(self, user_name, password, product_id, type):
        try:
            self.login(user_name=str(user_name), password=str(password))
            self.entity.vip_product_sfchart_info(productId=product_id, type=type)
        except:
            pass

    # 产品-所有产品类别
    def all_product_types(self):
        try:
            self.entity.all_product_tpes()
        except:
            pass

    # 基金-基金是否已添加自选
    def fund_is_fav(self, user_name, password, fund_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.fund_is_fav(fundId=fund_id)
        except:
            pass

    # 产品-高端货币类月、季，年收益曲线
    def vip_product_mfchart_info(self, user_name, password, product_id, type):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.vip_product_mfchart_info(productId=product_id, type=type)
        except:
            pass

    # 基金-看好他(基金经理)
    def custinfo_support(self, user_name, password, fund_manager_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.custinfo_support(fundManagerId=fund_manager_id)
        except:
            pass

    # 基金-基金经理看好情况
    def custinfo_support_detail(self, user_name, password, fund_manager_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.custinfo_support_detail(fundManagerId=fund_manager_id)
        except:
            pass

    # 基金-分红和拆分
    def get_share_and_split(self, user_name, password, fund_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_share_and_split(fundId=fund_id)
        except:
            pass

    # 基金-基金历史净值
    def fund_nav_history(self, user_name, password, start_date, fund_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.fund_nav_history(startDate=start_date, fundId=fund_id)
        except:
            pass

    # 基金-货币基金历史
    def fund_profit_history(self, user_name, password, start_date, fund_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.fund_profit_history(startDate=start_date, fundId=fund_id)
        except:
            pass

    # 通知中心-首页理财日历(V3.3)
    def index_fin_calendar(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.index_fin_calendar()
        except:
            pass

    # 通知中心-理财日历(V3.3)
    def fin_calendar(self, user_name, password, month):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.fin_calendar(month=month)
        except:
            pass

    # 产品-收益计算器(V3.3)
    def income_calculator(self, user_name, password, product_id, purchase_amt):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.income_calculator(productId=product_id, purchaseAmt=purchase_amt)
        except:
            pass

    # 通用-获取配置项(V3.3)
    def common_config(self, user_name, password, key):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.common_config(key=key)
        except:
            pass

    # 账户-用户修改姓名拼音(V3.3)
    def update_cust_name_spell(self, user_name, password, name_spell):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.update_cust_name_spell(nameSpell=name_spell)
        except:
            pass

    # 信用卡-卡详情
    def credit_card_detail(self, user_name, password, card_serial_no):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.credit_card_detail(cardSerialNo=card_serial_no)
        except:
            pass

    # 通知中心-个人事项设置
    def get_personal_setting_list(self, user_name, password, sub_type):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_personal_setting_list(subType=sub_type)
        except:
            pass

    # 资讯 - 资讯分类
    def get_category_list(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_category_list()
        except:
            pass

    # 通用-获取枚举值
    def get_enum_list(self, user_name, password, type):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_enum_list(type=type)
        except:
            pass

    # 账户-短信验证登录
    def sms_login_get_mobile_code(self, user_name, captcha_code, mobile_code):
        try:
            entity = self.entity.sms_login_get_mobile_code(mobile=user_name, captchaCode=captcha_code)
            serial_no = entity.body_serialNo
            self.entity.sms_login(serialNo=serial_no, mobileCode=mobile_code)
        except:
            pass

    # 账户 - 光大提额获取formbean
    def ceb_bank_quota_form_bean(self, user_name, password, bank_card_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.ceb_bank_quota_form_bean(bankCardId=bank_card_id)
        except:
            pass

    # 基金-定投排行
    def find_invest_yield_product(self, user_name, password, fund_type, period_type, sort_type, order_desc):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.find_invest_yield_product(fundType=fund_type, periodType=period_type, sortType=sort_type,
                                                  orderDesc=order_desc)
        except:
            pass

    # 使用优惠券还信用卡
    def creditcard_repay_using_coupon(self, mobile, password, card_id, amt, trade_password):
        try:
            self.login(user_name=mobile, password=password)
            self._cms.issue_coupon(code='FULL_OFF_3_1_0070', mobile=mobile, quantity=1)

            entity = self.entity.points_discount_coupon(purchaseAmt=amt, type='2')
            coupon_id = self.entity.current_coupon_id

            self.entity.creditcard_repay_validate(repayAmt=amt, cardSerialNo=card_id, couponIds=coupon_id)
            serial_no = self.entity.current_repay_serialno
            self.entity.creditcard_repay(tradePassword=trade_password, serialNo=serial_no)
            serial_no = self.entity.current_creditcard_repay_serialno
            # 信用卡还款结果轮询
            self.entity.creditcard_query_repay_result(serialNo=serial_no)
        except:
            pass

    # 账户-解绑资金账户提交
    def unbinding_capital_account(self, user_name, password, mobile_code):
        try:
            self.login(user_name=user_name, password=password)
            serial_no = self.entity.current_login_serial_no
            self.entity.unbinding_capital_account_get_mobile_code(mobile=user_name, serialNo=serial_no)
            serial_no = self.entity.current_unbiding_serial_no
            entity = self.entity.send_sms_code(mobile=user_name, serialNo=serial_no)
            serial_no = entity.body_serialNo
            self.entity.unbinding_capital_account(mobileCode=mobile_code, serialNo=serial_no)
        except:
            pass

    # 产品-高端货币类产品历史收益
    def vip_product_history_profit(self, user_name, password, product_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.vip_product_history_profit(productId=product_id)
        except:
            pass

    # 产品-高端权益类产品历史收益
    def vip_product_history_nav(self, user_name, password, product_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.vip_product_history_profit(productId=product_id)
        except:
            pass

    # 银行卡 - 重新签约
    def card_sign_again(self, mobile, password, bank_card_id):
        try:
            self.login(user_name=mobile, password=password)
            self.entity.card_sign_again_get_mobile_code(mobile=mobile, bankCardId=bank_card_id)
            mobile_code = self.entity.current_mobile_code
            serial_no = self.entity.current_get_mobile_code_serialno
            self.entity.card_sign_again(mobileCode=mobile_code, serialNo=serial_no)
        except:
            pass

    # 通用 - 开锁页面格言
    def get_maxim(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_maxim()
        except:
            pass

    # 产品-高端历史回报相关内容
    def vip_product_history_income(self, user_name, password, product_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.vip_product_history_income(productId=product_id)
        except:
            pass

    # 消息中心-首页Tips
    def msg_index_tips(self, user_name, password, position):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.msg_index_tips(position=position)
        except:
            pass

    # 积分-福利中心主页积分信息
    def my_points_info(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.my_points_info()
        except:
            pass

    # 积分-福利中心交易明细
    def trade_detail(self, user_name, password, points_type, type):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.trade_detail(pointsType=points_type, type=type)
        except:
            pass

    # 交易 - 基金转换
    def fund_transfer(self, user_name, password, from_fund_id, to_fund_id, expire_dispose_type, transfer_share,
                      type, trade_password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.fund_transfer_validate(fromFundId=from_fund_id, toFundId=to_fund_id, type=type,
                                               expireDisposeType=expire_dispose_type, transferShare=transfer_share)
            serial_no = self.entity.current_fund_transfer_serial_no
            self.entity.trade_confirm(serialNo=serial_no, password=trade_password)
        except:
            pass

    # 积分-福利中心
    def welfare_center(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.welfare_center()
        except:
            pass

    # 积分-兑换积分商品
    def exchange_points_goods(self, user_name, password, goods_id, exchange_count, pay_type, trade_password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.exchange_points_goods(goodsId=goods_id, exchangeCount=exchange_count, payType=pay_type,
                                              tradePassword=trade_password)
        except:
            pass

    # 基金-理财型基金自动续存提示文案
    def finance_fund_auto_purchase_tip(self, user_name, password, fund_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.finance_fund_auto_purchase_tip(fundId=fund_id)
        except:
            pass

    # 产品 - 转换提示信息
    def transfer_to_fund_tip(self, user_name, password, to_fund_id, from_fund_id, type, transfer_share):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.transfer_to_fund_tip(toFundId=to_fund_id, fromFundId=from_fund_id, type=type,
                                             transferShare=transfer_share)
        except:
            pass

    # 产品 - 转换基本信息
    def transfer_to_fund_info(self, user_name, password, to_fund_id, type, from_fund_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.transfer_to_fund_info(toFundId=to_fund_id, type=type, fromFundId=from_fund_id)
        except:
            pass

    # 产品 - 检索可转换基金
    def search_can_transfer_fund_list(self, user_name, password, from_fund_id, keyword):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.search_can_transfer_fund_list(fromFundId=from_fund_id, keyword=keyword)
        except:
            pass

    # 产品 - 可转换基金列表
    def can_transfer_fund_list(self, user_name, password, from_fund_id, type):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.can_transfer_fund_list(fromFundId=from_fund_id, type=type)
        except:
            pass

    # 交易-理财型基金修改到期处理方式
    def modify_finance_fund_expire_dispose_type(self, user_name, password, trade_password, expire_dispose_type,
                                                expire_quit_amt, fund_id, value_date, expire_date):
        try:
            self.login(user_name=user_name, password=password)
            entity = self.entity.modify_finance_fund_expire_dispose_type(expireDisposeType=expire_dispose_type,
                                                                         expireQuitAmt=expire_quit_amt, fundId=fund_id,
                                                                         valueDate=value_date, expireDate=expire_date)
            serial_no = entity.body_serialNo
            self.entity.trade_confirm(serialNo=serial_no, password=trade_password)
        except:
            pass

    # 交易-理财型基金修改到期处理方式提示信息
    def modify_finance_fund_expire_dispose_type_tip(self, user_name, password, expire_dispose_type, fund_id,
                                                    value_date, expire_date, order_no, holding_type, redeem_value):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.modify_finance_fund_expire_dispose_type_tip(expireDisposeType=expire_dispose_type,
                                                                    fundId=fund_id, valueDate=value_date,
                                                                    expireDate=expire_date, orderNo=order_no,
                                                                    holdingType=holding_type, redeemValue=redeem_value)
        except:
            pass

    # 交易 - 我的历史持有列表
    def my_hold_list_history(self, user_name, password, product_type, fund_type):
        try:
            self.login(user_name=user_name, password=password)
            if str(product_type) == '2':
                self.entity.my_hold_list_history_fund(productType=product_type, fundType=fund_type)
            else:
                self.entity.my_hold_list_history_vip_or_dhb(productType=product_type)
        except:
            pass

    # 用户-校验手机号
    def mobile_validate(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.mobile_validate()
        except:
            pass

    # 产品-高端详情概况
    def vip_product_survey(self, user_name, password, product_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.vip_product_survey(productId=product_id)
        except:
            pass

    # 产品-高端详情规则
    def vip_product_ruler(self, user_name, password, product_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.vip_product_ruler(productId=product_id)
        except:
            pass

    # 交易 - 历史持仓买卖点
    def my_trade_points(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.my_trade_points()
        except:
            pass

    # 交易 - 我的历史基金产品详情
    def my_fund_detail_history(self, user_name, password, batch_no):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.my_fund_detail_history(batchNo=batch_no)
        except:
            pass

    # 交易 - 我的历史高端产品详情
    def my_vip_product_detail_history(self, user_name, password, batch_no):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.my_vip_product_detail_history(batchNo=batch_no)
        except:
            pass

    # 交易 - 我的历史定期宝产品详情
    def my_dqb_detail_history(self, user_name, password, batch_no):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.my_dqb_detail_history(batchNo=batch_no)
        except:
            pass

    # 基金-基金费率详情
    def get_fund_info(self, user_name, password, fund_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_fund_info(fundId=fund_id)
        except:
            pass

    # 风险测评-测评结果预确认
    def get_risk_type_by_answer(self, user_name, password, question_no, answer, score):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_risk_type_by_answer(questionNo=question_no, answer=answer, score=score)
        except:
            pass

    # 账户-税收居民身份申明
    def save_tax_type(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.save_tax_type()
        except:
            pass

    # 账户-查询税收居民身份
    def get_tax_type(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_tax_type()
        except:
            pass

    # 积分 - 查询积分、元宝说明
    def get_points_description(self, user_name, password, description_code):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_points_description(descriptionCode=description_code)
        except:
            pass

    # 积分 - 查询积分获取规则
    def get_points_deducte_rules(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_points_deducte_rules()
        except:
            pass

    # 积分-签到
    def get_points_sign_in(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_points_sign_in()
        except:
            pass

    # 积分 - 查询积分发放规则
    def get_points_issue_event_rules(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_points_issue_event_rules()
        except:
            pass

    # 积分-保存分享结果
    def save_share_result(self, user_name, password, share_url):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.save_share_result(shareUrl=share_url)
        except:
            pass

    # 积分-查询签到结果
    def get_sign_result(self, user_name, password):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_sign_result()
        except:
            pass

    # 基金-基金申购、认购、赎回费率接口
    def get_fund_transaction_date(self, user_name, password, fund_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_fund_transaction_date(fundId=fund_id)
        except:
            pass

    # 会员等级-权益专属产品
    def get_exclusive_products(self, user_name, password, member_level, rights_id, parent_rights_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_exclusive_products(memberLevel=member_level, rightsId=rights_id,
                                               parentRightsId=parent_rights_id)
        except:
            pass

    # 会员等级-权益优惠券/积分礼包
    def get_gift_bag(self, user_name, password, member_level, rights_id, parent_rights_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_gift_bag(memberLevel=member_level, rightsId=rights_id, parentRightsId=parent_rights_id)
        except:
            pass

    # 会员等级 - 权益表格数据
    def cust_level_form_data(self, user_name, password, member_level, rights_id, parent_rights_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.cust_level_form_data(memberLevel=member_level, rightsId=rights_id,
                                             parentRightsId=parent_rights_id)
        except:
            pass

    # 账户 - 用户实名信息验证
    def real_name_auth_validate(self, user_name, password, name, cert_type, cert_no, cert_validate_date):
        try:
            self.login(user_name=user_name, password=password)
            serial_no = self.entity.current_login_serial_no
            self.entity.real_name_auth_validate(name=name, certType=cert_type, certNo=cert_no,
                                                certValidDate=cert_validate_date, serialNo=serial_no)
        except:
            pass

    # 注册实名认证绑卡
    def register_name_auth_binding_card(self, mobile, login_password, cert_type, cert_validate_date, card_bin,
                                        trade_password):
        try:
            self.register(mobile=mobile, login_password=login_password)

            card_no = Utility.GetData().bank_card_no(card_bin=card_bin).split('-')[0]
            name = 'API' + str(random.randint(0, 99))
            cert_no = Utility.GetData().id_no()

            self.entity.card_set_trade_password(newPassword=trade_password)
            serial_no = self.entity.current_set_trade_passowrd_serialno

            self.entity.real_name_auth_validate(name=name, certType=cert_type, certNo=cert_no,
                                                certValidDate=cert_validate_date, serialNo=serial_no)

            entity = self.entity.card_match_channel(card_bin=card_bin + '1522')
            bank_no = entity.bankChannel_bankNo
            bank_name = entity.bankChannel_bankGroupName
            sms_mode = entity.smsMode

            self.entity.card_get_mobile_code(mobile=mobile, serialNo=serial_no, cardNo=card_no, name=name,
                                             certNo=cert_no, smsMode=sms_mode, bankName=bank_name, bankNo=bank_no)

            # mobile_code = self.mysql.get_sms_verify_code(mobile=mobile, template_id='cif_bindBankCard')
            mobile_code = self.entity.current_mobile_code
            serial_no = self.entity.current_get_mobile_code_serialno
            self.entity.card_new_binding(mobileCode=mobile_code, serialNo=serial_no)
            return card_no
        except:
            pass

    # 会员等级-权益生日特权
    def get_birthday_rights(self, user_name, password, member_level, rights_id, parent_rights_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_birthday_rights(memberLevel=member_level, rightsId=rights_id,
                                            parentRightsId=parent_rights_id)
        except:
            pass

    # 交易-一键随心取提交
    def one_key_redeem_validate(self, user_name, password, product_ids, redeem_amts, trade_password):
        try:
            self.login(user_name=user_name, password=password)
            entity = self.entity.one_key_redeem_validate(productIds=product_ids, redeemAmts=redeem_amts)
            serial_no = entity.body_serialNo
            self.entity.trade_confirm(serialNo=serial_no, password=trade_password)
        except:
            pass

    # 交易-查询组合支付权限
    def get_combination_payment_auth(self, user_name, password, product_id, should_pay_amt, serial_no):
        try:
            self.login(user_name=user_name, password=password)
            entity = self.entity.get_combination_payment_auth(productId=product_id, shouldPayAmt=should_pay_amt,
                                                              serialNo=serial_no)
            serial_no = entity.body_serialNo
            self.entity.get_combination_payment_auth(productId=product_id, shouldPayAmt=should_pay_amt,
                                                     serialNo=serial_no)
        except:
            pass

    # 交易-查询组合支付方案
    def get_combination_payment_plan(self, user_name, password, product_id, should_pay_amt, serial_no):
        try:
            self.login(user_name=user_name, password=password)
            entity = self.entity.get_combination_payment_auth(productId=product_id, shouldPayAmt=should_pay_amt,
                                                              serialNo=serial_no)
            serial_no = entity.body_serialNo
            self.entity.get_combination_payment_plan(serialNo=serial_no)
        except:
            pass

    # 交易-修改组合支付方案
    def modify_combination_payment_plan(self, user_name, password, product_id, should_pay_amt, serial_no, product_ids,
                                        redeem_amts, set_default):
        try:
            self.login(user_name=user_name, password=password)
            entity = self.entity.get_combination_payment_auth(productId=product_id, shouldPayAmt=should_pay_amt,
                                                              serialNo=serial_no)
            serial_no = entity.body_serialNo
            entity = self.entity.get_combination_payment_plan(serialNo=serial_no)
            serial_no = entity.body_serialNo
            self.entity.modify_combination_payment_plan(productIds=product_ids, redeemAmts=redeem_amts,
                                                        serialNo=serial_no, setDefault=set_default)
        except:
            pass

    # 交易-基金赎回提示信息
    def fund_redeem_tip(self, user_name, password, fund_id, redeem_share):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.fund_redeem_tip(fundId=fund_id, redeemShare=redeem_share)
        except:
            pass

    # 交易-锁定用途列表
    def locked_purpose_list(self, user_name, password, order_no, product_id, holding_type, value_date):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.locked_purpose_list(orderNo=order_no, productId=product_id, holdingType=holding_type,
                                            valueDate=value_date)
        except:
            pass

    # 交易-一键随心取金额校验
    def one_key_redeem_amt_validate(self, user_name, password, product_id, redeem_amt):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.one_key_redeem_amt_validate(oproductId=product_id, redeemAmt=redeem_amt)
        except:
            pass

    # 交易-查询组合支付确认信息
    def get_combination_payment_confirm_info(self, user_name, password, product_id, should_pay_amt, serial_no,
                                             product_ids, redeem_amts, set_default):
        try:
            self.login(user_name=user_name, password=password)
            entity = self.entity.get_combination_payment_auth(productId=product_id, shouldPayAmt=should_pay_amt,
                                                              serialNo=serial_no)
            serial_no = entity.body_serialNo
            entity = self.entity.get_combination_payment_plan(serialNo=serial_no)
            serial_no = entity.body_serialNo
            entity = self.entity.modify_combination_payment_plan(productIds=product_ids, redeemAmts=redeem_amts,
                                                                 serialNo=serial_no, setDefault=set_default)
            serial_no = entity.body_serialNo
            self.entity.get_combination_payment_confirm_info(serialNo=serial_no)
        except:
            pass

    # 交易-使用超级支付方式购买产品
    def buy_product_using_super_payment(self, user_name, login_password, pay_type, product_id, should_pay_amt,
                                        serial_no, product_ids, redeem_amts, set_default, trade_password):
        try:
            self.login(user_name=user_name, password=login_password)
            entity = self.entity.get_combination_payment_auth(productId=product_id, shouldPayAmt=should_pay_amt,
                                                              serialNo=serial_no)
            serial_no = entity.body_serialNo
            entity = self.entity.get_combination_payment_plan(serialNo=serial_no)
            serial_no = entity.body_serialNo
            entity = self.entity.modify_combination_payment_plan(productIds=product_ids, redeemAmts=redeem_amts,
                                                                 serialNo=serial_no, setDefault=set_default)
            serial_no = entity.body_serialNo

            entity = self.entity.purchase_product(productId=product_id, payType=pay_type, amt=should_pay_amt,
                                                  combinationPaySerialNo=serial_no)
            serial_no = entity.body_serialNo

            self.entity.trade_confirm(serialNo=serial_no, password=trade_password)
        except:
            pass

    # 使用超级支付方式申购高端并撤单
    def purchase_using_super_pay_then_cancel(self, user_name, login_password, pay_type, product_id, should_pay_amt,
                                             serial_no, product_ids, redeem_amts, set_default, trade_password):
        try:
            self.login(user_name=user_name, password=login_password)
            entity = self.entity.get_combination_payment_auth(productId=product_id, shouldPayAmt=should_pay_amt,
                                                              serialNo=serial_no)
            serial_no = entity.body_serialNo
            entity = self.entity.get_combination_payment_plan(serialNo=serial_no)
            serial_no = entity.body_serialNo
            entity = self.entity.modify_combination_payment_plan(productIds=product_ids, redeemAmts=redeem_amts,
                                                                 serialNo=serial_no, setDefault=set_default)
            serial_no = entity.body_serialNo

            entity = self.entity.purchase_product(productId=product_id, payType=pay_type, amt=should_pay_amt,
                                                  combinationPaySerialNo=serial_no)
            serial_no = entity.body_serialNo

            self.entity.trade_confirm(serialNo=serial_no, password=trade_password)

            trade_req, trade_order = self.mysql.get_trade_request(mobile=user_name)
            order_no = trade_order[0]['PARENT_ORDER_NO']
            # order_no = '01201802075A7ACA1B00011b0601'
            sleep(60)
            # 撤单
            entity = self.entity.revoke_validate(tradeSerialNo=str(order_no))
            serial_no = entity.body_serialNo
            self.entity.trade_confirm(serialNo=serial_no, password=trade_password)
        except:
            pass

    # 基金-估值排行
    def fund_estimate_leader_board(self, user_name, password, fund_type, sort_type, order_desc):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.fund_estimate_leader_board(fundType=fund_type, sortType=sort_type, orderDesc=order_desc)
        except:
            pass

    # 基金-最新估值
    def get_current_estimate_nav(self, user_name, password, fund_id):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.get_current_estimate_nav(fundId=fund_id)
        except:
            pass

    # 基金-自选基金最新估值
    def fav_fund_estimate_nav(self, user_name, password, fund_ids):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.fav_fund_estimate_nav(fundIds=fund_ids)
        except:
            pass

    # 风险类型不匹配
    def buy_product_nomatch_risk(self, user_name, login_password, pay_type, amt, product_id, is_confirm_beyond_risk,
                                 trade_password):
        try:
            self.login(user_name=user_name, password=login_password)

            self.entity.purchase_product_unmatch(productId=product_id, payType=pay_type, amt=amt,
                                                 isConfirmBeyondRisk=is_confirm_beyond_risk)
            serial_no = self.entity.current_purchase_product_serialno

            self.entity.trade_confirm(serialNo=serial_no, password=trade_password)
        except:
            pass

    # 账户-打开/关闭短信验证码登录
    def save_sms_login_status(self, user_name, password, open_status):
        try:
            self.login(user_name=user_name, password=password)
            self.entity.save_sms_login_status(openStatus=open_status)
        except:
            pass

if __name__ == '__main__':
    m = RestfulXjbTools()
    # m.fund_redeem_cost_calt_value(user_name='18931006600', login_password='1234abcd', product_id='05#050026',
    #                               redeem_amt='1200')
    # phone_number = Utility.GetData().mobile()
    # m.modify_finance_fund_expire_dispose_type(user_name='17200000240', password='12qwaszx', expire_dispose_type='1',
    #                                           expire_quit_amt='4003', fund_id='53#530030', value_date='20171218',
    #                                           expire_date='20181218')

    m.new_user(user_name='18790112336',
               login_password='a0000000',
               card_bin='622202',
               trade_password='135790',)
