# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
from _common.global_config import ASSERT_DICT
from _tools.mysql_xjb_tools import MysqlXjbTools
import time
import huaxin_ui.ui_android_xjb_3_0.user_operation_succeed_page

AMOUNT = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/product_purchase_amt']"
PAYMENT_TYPE = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/payment_type_arrow']"
SWIPE_BEGIN = "swipe_xpath_//"
CASH_MANAGEMENT_PRODUCT_SWIPE_STOP = "swipe_xpath_//android.widget.TextView[contains(@text,'%s')]"
CASH_MANAGEMENT_PRODUCT = "xpath_//android.widget.TextView[contains(@text,'%s')]"
POINT_SWITCH = "xpath_//android.widget.ToggleButton[@resource-id='com.shhxzq.xjb:id/tbtn_point_switch']"
COUPONS_INFO = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_purchase_coupons_info']"
NONSUPERCOMPOSED_COUPON_SWIPE_STOP = "swipe_xpath_//android.widget.RelativeLayout[@clickable='true']//android.widget.TextView[@text='不可叠加使用']"
COUPONS = "xpath_//android.widget.RelativeLayout[@clickable='true']//android.widget.TextView[@text='不可叠加使用']"
COMFIRM_BUTTON_SWIPE_STOP = "swipe_xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/product_purchase_bt']"
BUY_CONFIRM = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/product_purchase_bt']"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"
CANCEL_BUTTON = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/button1']"
KEEP_BUY = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/button2']"
VERIFY_CODE_INPUT = "xpath_//android.widget.EditText[@text='请输入短信验证码']"
VERIFY_CODE_CONFIRM = "xpath_//android.widget.Button[@text='确认']"


class ProductPurchasePage(PageObject):
    def __init__(self, web_driver):
        super(ProductPurchasePage, self).__init__(web_driver)
        self._db = MysqlXjbTools()

    @robot_log
    def verify_page_title(self):
        self.assert_values('买入', self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def verify_purchase_amount(self, amount):
        default_amount_text = self.get_text('com.shhxzq.xjb:id/product_purchase_amt', 'find_element_by_id')
        default_amount = filter(lambda ch: ch in '0123456789.', default_amount_text)
        if float(amount) <= ASSERT_DICT['max']:
            self.assert_values('%.2f' % float(amount), default_amount)
        else:
            self.assert_values('%.2f' % ASSERT_DICT['max'], default_amount)
        page = self
        return page

    @robot_log
    def verify_product_purchase_page_details(self, product_name):
        self.assert_values('现在买入', self.get_text('com.shhxzq.xjb:id/product_purchase_title', 'find_element_by_id'))
        self.assert_values(product_name, self.get_text('com.shhxzq.xjb:id/product_name', 'find_element_by_id'))
        self.assert_values('剩余额度', self.get_text('com.shhxzq.xjb:id/purchase_limit_title', 'find_element_by_id'))
        self.assert_values('买入金额', self.get_text('com.shhxzq.xjb:id/amount_title', 'find_element_by_id'))
        self.assert_values('付款账户', self.get_text('com.shhxzq.xjb:id/payment_type_title', 'find_element_by_id'))
        self.assert_values('True', str(self.element_exist("//android.widget.TextView[@text='应付金额']")))

        page = self
        return page

    @robot_log
    def buy_finance_product(self, amount, trade_password=None, mobile=None, cash_management_product=None, points='N',
                            nonsuperposed_coupon='N', superposed_coupon='N', age=None):
        ASSERT_DICT.update({'success_flag': '0'})

        self.perform_actions(AMOUNT, amount)

        if cash_management_product is not None:
            self.perform_actions(PAYMENT_TYPE,
                                 SWIPE_BEGIN, CASH_MANAGEMENT_PRODUCT_SWIPE_STOP % cash_management_product, 'U')
            if cash_management_product == 'UI作为支付手段异常测试':
                self.assert_values('余额不足',
                                   self.get_text('com.shhxzq.xjb:id/not_sufficient_prompt', 'find_element_by_id'))
                page = self

                return page
            else:
                self.perform_actions(CASH_MANAGEMENT_PRODUCT % cash_management_product)

        if points == 'Y':
            self.perform_actions(POINT_SWITCH)
            time.sleep(5)

        # if nonsuperposed_coupon == 'Y':
        #     self.perform_actions(COUPONS_INFO)
        #
        #     time.sleep(10)
        #
        #     self.perform_actions(SWIPE_BEGIN, NONSUPERCOMPOSED_COUPON_SWIPE_STOP, 'U',
        #                          COUPONS,
        #                          COUPONS_CONFIRM)
        #
        # if superposed_coupon == 'Y':
        #     self.perform_actions(COUPONS_INFO)
        #
        #     time.sleep(10)
        #     self.perform_actions(COUPON_SWIPE_BEGAIN, SUPERCOMPOSED_COUPON_SWIPE_STOP, 'U',
        #                          SUPERPOSED_COUPON_1,
        #                          SUPERCOMPOSED_COUPON_SWIPE_BEGAIN, SUPERCOMPOSED_COUPON_SWIPE_STOP_1, 'U',
        #                          SUPERPOSED_COUPON_2,
        #                          COUPONS_CONFIRM)

        self.perform_actions(SWIPE_BEGIN, COMFIRM_BUTTON_SWIPE_STOP, 'U',
                             BUY_CONFIRM
                             )

        xjb_assets = ASSERT_DICT['xjb_total_assets_login']
        if 1 <= float(amount) < float(xjb_assets):
            ASSERT_DICT.update({'success_flag': '1'})

            if age >= 70:
                self.assert_values('风险提示', self.get_text('com.shhxzq.xjb:id/alertTitle', 'find_element_by_id'))
                self.assert_values('您已满70周岁，确认继续购买？', self.get_text('com.shhxzq.xjb:id/message', 'find_element_by_id'))
                self.perform_actions(KEEP_BUY)

                time.sleep(2)  # 数据库数据更新有点滞后
                verification_code = self._db.get_sms_verify_code(mobile=mobile, template_id='as_risk_match')

                self.perform_actions(
                    VERIFY_CODE_INPUT, verification_code,
                    VERIFY_CODE_CONFIRM
                )

            if float(amount) >= 5000000:
                self.assert_values('风险提示', self.get_text('com.shhxzq.xjb:id/alertTitle', 'find_element_by_id'))
                self.assert_values('您的交易金额为500万，确认继续购买？',
                                   self.get_text('com.shhxzq.xjb:id/message', 'find_element_by_id'))
                self.perform_actions(KEEP_BUY)
                self.assert_values('输入短信验证码', self.get_text('com.shhxzq.xjb:id/tv_dialog_title', 'find_element_by_id'))
                self.assert_values(True, self.element_exist("//android.widget.Button[contains(@text,'后重发')]"))
                self.assert_values(True, self.element_exist("//android.widget.Button[@text='确认']"))

                page = self
            else:
                self.perform_actions(TRADE_PASSWORD, trade_password)

                page = huaxin_ui.ui_android_xjb_3_0.user_operation_succeed_page.UserOperationSucceedPage(
                    self.web_driver)
        elif float(amount) > float(xjb_assets):
            self.perform_actions(CANCEL_BUTTON)
            page = self

        else:
            page = self

        return page
