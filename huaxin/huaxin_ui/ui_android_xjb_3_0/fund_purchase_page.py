# coding=utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import time
import huaxin_ui.ui_android_xjb_3_0.coupon_use_coupon_page
import huaxin_ui.ui_android_xjb_3_0.user_operation_succeed_page
import huaxin_ui.ui_android_xjb_3_0.fund_page_fund_detail
import huaxin_ui.ui_android_xjb_3_0.risk_evaluation_page
from _common.global_config import ASSERT_DICT
from _tools.mysql_xjb_tools import MysqlXjbTools

BUY_AMOUNT = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/product_purchase_amt']"
POINT_SWITCH = "xpath_//android.widget.ToggleButton[@resource-id='com.shhxzq.xjb:id/tbtn_point_switch']"
COUPONS_INFO = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_purchase_coupons_info']"
SWIPE_BEGIN = "swipe_xpath_//"
COMFIRM_BUTTON_SWIPE_STOP = "swipe_xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/product_purchase_bt']"
BUY_CONFIRM = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/product_purchase_bt']"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"
CANCEL = "xpath_//android.widget.TextView[@text='取消']"
ASSETS = "xpath_//android.widget.RelativeLayout[5]/android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/tab_image'][POP]"
BACK = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left']"
BACK_BUTTON = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left']"
BACK_BUTTON_POINTS = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left_orange']"
FUND = "xpath_//android.widget.TextView[@text='基金']"
FUND_SWIPE_STOP = "swipe_xpath_//android.widget.TextView[@text='购买金额']"
FUND_PRODUCT = "xpath_//android.widget.TextView[@text='购买金额']"
CANCEL_BUTTON = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/button1']"
BUY = "xpath_//android.widget.Button[@text='继续买入']"
VERIFY_CODE_INPUT = "xpath_//android.widget.EditText[@text='请输入短信验证码']"
COMFIRM = "xpath_//android.widget.Button[@text='确认']"
THINK = "xpath_//android.widget.Button[@text='再考虑一下']"
EVALUATION_BUTTON = "xpath_//android.widget.Button[@text='去测试']"
PAYMENT_TYPE = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/payment_type_arrow']"
CASH_MANAGEMENT_PRODUCT_SWIPE_STOP = "swipe_xpath_//android.widget.TextView[contains(@text,'%s')]"
CASH_MANAGEMENT_PRODUCT = "xpath_//android.widget.TextView[contains(@text,'%s')]"
GET_VERIFICATION_CODE = "xpath_//android.widget.Button[@text='获取验证码']"


class FundPurchasePage(PageObject):
    def __init__(self, web_driver):
        super(FundPurchasePage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('买入', self.get_text(self.page_title, 'find_element_by_id'))
        page = self

        return page

    @robot_log
    def buy_fund_product(self, amount=None, trade_password=None, points='N', coupon=None, risk=None,
                         user_type=None, phone_number=None, cash_management_product=None, age=None):
        ASSERT_DICT.update({'success_flag': '0'})
        if risk == 'high' and user_type == 'conservative':
            self.assert_values('风险提示', self.get_text('com.shhxzq.xjb:id/alertTitle', 'find_element_by_id'))
            self.assert_values('再考虑一下', self.get_text('com.shhxzq.xjb:id/button1', 'find_element_by_id'))
            # self.assert_values('重新测试', self.get_text('com.shhxzq.xjb:id/button2', 'find_element_by_id'))
            self.assert_values('去测试', self.get_text('com.shhxzq.xjb:id/button2', 'find_element_by_id'))
            self.perform_actions(THINK)

            page = huaxin_ui.ui_android_xjb_3_0.fund_page_fund_detail.FundPageFundDetail(self.web_driver)
            return page

        self.perform_actions(BUY_AMOUNT, amount)

        if cash_management_product is not None:
            self.perform_actions(PAYMENT_TYPE,
                                 SWIPE_BEGIN, CASH_MANAGEMENT_PRODUCT_SWIPE_STOP % cash_management_product, 'U',
                                 CASH_MANAGEMENT_PRODUCT % cash_management_product)

        if points == 'Y':
            self.perform_actions(POINT_SWITCH)

            time.sleep(5)

        if coupon is not None:
            self.go_to_use_coupon_page(coupon=coupon)

        self.perform_actions(SWIPE_BEGIN, COMFIRM_BUTTON_SWIPE_STOP, 'U')

        self.perform_actions(BUY_CONFIRM)

        if risk == 'high':
            if user_type == 'moderate':
                self.assert_values('风险提示', self.get_text('com.shhxzq.xjb:id/alertTitle', 'find_element_by_id'))
                self.perform_actions(BUY)
                # self.perform_actions(GET_VERIFICATION_CODE)
                self.assert_values('输入短信验证码', self.get_text('com.shhxzq.xjb:id/tv_dialog_title', 'find_element_by_id'))
                time.sleep(1)
                verification_code = MysqlXjbTools().get_sms_verify_code(mobile=phone_number,
                                                                        template_id='as_risk_not_match')
                self.perform_actions(VERIFY_CODE_INPUT, verification_code)
            elif user_type == 'radical':
                if age >= 70:
                    if float(amount) >= 5000000:  # 激进型用户,年龄大于70岁,购买金额超过500万
                        self.assert_values('风险提示', self.get_text('com.shhxzq.xjb:id/alertTitle', 'find_element_by_id'))
                        self.assert_values('您购买的是高风险产品、您已满70周岁且交易金额超过500万，确认继续购买？',
                                           self.get_text('com.shhxzq.xjb:id/message', 'find_element_by_id'))
                        self.assert_values('再考虑一下', self.get_text('com.shhxzq.xjb:id/button1', 'find_element_by_id'))
                        self.assert_values('继续买入', self.get_text('com.shhxzq.xjb:id/button2', 'find_element_by_id'))
                        self.perform_actions(BUY)
                        self.assert_values('输入短信验证码',
                                           self.get_text('com.shhxzq.xjb:id/tv_dialog_title', 'find_element_by_id'))
                        self.assert_values(True,
                                           self.element_exist("//android.widget.Button[contains(@text,'后重发')]"))
                        self.assert_values(True,
                                           self.element_exist("//android.widget.Button[@text='确认']"))
                else:
                    self.assert_values('风险提示', self.get_text('com.shhxzq.xjb:id/alertTitle', 'find_element_by_id'))
                    self.assert_values('您购买的是高风险产品，确认继续购买？',
                                       self.get_text('com.shhxzq.xjb:id/message', 'find_element_by_id'))
                    self.assert_values('再考虑一下', self.get_text('com.shhxzq.xjb:id/button1', 'find_element_by_id'))
                    self.assert_values('继续买入', self.get_text('com.shhxzq.xjb:id/button2', 'find_element_by_id'))
                    self.perform_actions(BUY)
                    # self.perform_actions(GET_VERIFICATION_CODE)
                    self.assert_values('输入短信验证码', self.get_text('com.shhxzq.xjb:id/tv_dialog_title', 'find_element_by_id'))
                    verification_code = MysqlXjbTools().get_sms_verify_code(mobile=phone_number,
                                                                            template_id='as_risk_match')
                    self.perform_actions(VERIFY_CODE_INPUT, verification_code)

            self.perform_actions(COMFIRM)

        # elif risk == 'middle_high':
        #     if user_type == 'cautious':
        #         self.assert_values('风险提示', self.get_text('com.shhxzq.xjb:id/alertTitle', 'find_element_by_id'))
        #         self.assert_values('再考虑一下', self.get_text('com.shhxzq.xjb:id/button1', 'find_element_by_id'))
        #         self.assert_values('继续买入', self.get_text('com.shhxzq.xjb:id/button2', 'find_element_by_id'))
        #         self.perform_actions(BUY)

        if 1 <= float(amount) < 50000:
            self.perform_actions(TRADE_PASSWORD, trade_password,
                                 )
            ASSERT_DICT.update({'success_flag': '1'})
            page = huaxin_ui.ui_android_xjb_3_0.user_operation_succeed_page.UserOperationSucceedPage(self.web_driver)

        elif float(amount) >= 100000000:
            page = self
            self.perform_actions(CANCEL_BUTTON)

        else:
            page = self
        return page

    @robot_log
    def go_to_use_coupon_page(self):
        self.perform_actions(COUPONS_INFO)
        page = huaxin_ui.ui_android_xjb_3_0.coupon_use_coupon_page.CouponUseCouponPage(self.web_driver)

        return page

    @robot_log
    def verify_risk_indication_details(self):
        self.assert_values('风险提示', self.get_text('com.shhxzq.xjb:id/alertTitle', 'find_element_by_id'))
        self.assert_values('再考虑一下', self.get_text('com.shhxzq.xjb:id/button1', 'find_element_by_id'))
        self.assert_values('去测试', self.get_text('com.shhxzq.xjb:id/button2', 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def go_to_risk_evaluation_page(self):
        self.perform_actions(EVALUATION_BUTTON)

        page = huaxin_ui.ui_android_xjb_3_0.risk_evaluation_page.RiskEvaluationPage(self.web_driver)

        return page

    @robot_log
    def verify_fund_purchase_page_details(self, fund_product):
        self.assert_values('现在买入', self.get_text('com.shhxzq.xjb:id/product_purchase_title', 'find_element_by_id'))
        self.assert_values(fund_product, self.get_text('com.shhxzq.xjb:id/product_name', 'find_element_by_id'))
        self.assert_values('买入金额', self.get_text('com.shhxzq.xjb:id/amount_title', 'find_element_by_id'))
        self.assert_values('付款账户', self.get_text('com.shhxzq.xjb:id/payment_type_title', 'find_element_by_id'))
        self.assert_values('True', str(self.element_exist("//android.widget.TextView[@text='应付金额']")))

        page = self
        return page
