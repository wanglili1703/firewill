# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
from _common.global_config import ASSERT_DICT
import re
import huaxin_ui.ui_android_xjb_3_0.user_operation_succeed_page
from _common.global_config import ASSERT_DICT

REDEEM_AMOUNT = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/cedt_dqb_redeem_product_amt']"
FUND_REDEEM_AMOUNT = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/product_redeem_amt']"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"
REDEEM_CONFIRM = "xpath_//android.widget.Button[@text='确认']"
REDEEM_TIPS = "com.shhxzq.xjb:id/tv_dqb_redeem_product_tips"
FAST_REDEEM = "xpath_//android.widget.RadioButton[@resource-id='com.shhxzq.xjb:id/rbtn_redeem_faster_select']"


class RedeemDetailPage(PageObject):
    def __init__(self, web_driver):
        super(RedeemDetailPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self, product_type=None):
        if product_type is None:
            self.assert_values('卖出', self.get_text('com.shhxzq.xjb:id/title_actionbar', 'find_element_by_id'))
        elif product_type == 'DHB':
            self.assert_values('取回', self.get_text('com.shhxzq.xjb:id/title_actionbar', 'find_element_by_id'))
        page = self

        return page

    @robot_log
    def redeem_product(self, redeem_amount, trade_password, product_type=None, redeem_type='normal'):
        if redeem_type == 'fast':
            self.perform_actions(FAST_REDEEM)
            self.assert_values(True, self.element_exist(
                "//android.widget.TextView[@text='极速卖出']/following-sibling::android.widget.RadioButton[@checked='true']"))
            self.assert_values(True, self.element_exist("//android.widget.TextView[contains(@text,'实时到账')]"))
        if product_type == "dhb" or product_type == "vip":
            redeem_max_text = self.get_text('com.shhxzq.xjb:id/tv_dqb_redeem_product_max', 'find_element_by_id')
            self.perform_actions(REDEEM_AMOUNT, redeem_amount)
        else:
            redeem_max_text = self.get_text('com.shhxzq.xjb:id/fund_redeem_max', 'find_element_by_id')
            self.perform_actions(FUND_REDEEM_AMOUNT, redeem_amount)
            if redeem_type == 'fast':
                self.assert_values(True, self.element_exist("//android.widget.TextView[contains(@text,'预计到账')]"))
                self.assert_values(True, self.element_exist("//android.widget.TextView[contains(@text,'说明')]"))

        redeem_max = re.findall(r'(\d{1,3}(,\d{3})*.\d+)', redeem_max_text)[0][0].replace(',', '')
        ASSERT_DICT.update({'success_flag': '0'})

        if float(redeem_amount) > 0:
            if float(redeem_amount) > float(redeem_max):
                if product_type == "dhb" or product_type == "vip":
                    amt = self.get_text('com.shhxzq.xjb:id/cedt_dqb_redeem_product_amt', 'find_element_by_id')
                    amt = '%.2f' % float(filter(lambda ch: ch in '0123456789.', str(amt)))
                    self.assert_values(float(amt), float(redeem_max), '==')
                page = self
            else:
                ASSERT_DICT.update({'success_flag': '1'})
                if product_type == 'dhb':
                    redeem_tips = self.get_text(REDEEM_TIPS, 'find_element_by_id')
                    redeem_amount_expected = re.findall(r'(\d{1,3}(,\d{3})*.\d+)', redeem_tips)[1][0].replace(',', '')
                    ASSERT_DICT.update({'redeem_amount': redeem_amount_expected})
                self.perform_actions(REDEEM_CONFIRM,
                                     TRADE_PASSWORD, trade_password)

                page = huaxin_ui.ui_android_xjb_3_0.user_operation_succeed_page.UserOperationSucceedPage(
                    self.web_driver)

        else:
            self.perform_actions(REDEEM_CONFIRM)
            page = self

            # if product_type == 'DHB':
            #     self.assert_values('取回', self.get_text(self.page_title, 'find_element_by_id'))
            # else:
            #     self.assert_values('卖出', self.get_text(self.page_title, 'find_element_by_id'))

        return page
