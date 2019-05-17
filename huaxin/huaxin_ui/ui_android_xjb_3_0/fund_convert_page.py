# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
from _common.global_config import ASSERT_DICT
import huaxin_ui.ui_android_xjb_3_0.user_operation_succeed_page

AMOUNT = "xpath_//android.widget.EditText[contains(@text,'份额')]"
FUND_CONVERT_CONFIRM = "xpath_//android.widget.Button[@text='确认']"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"


class FundConvertPage(PageObject):
    def __init__(self, web_driver):
        super(FundConvertPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('基金转换', self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def verify_fund_convert_details(self, fund_convert_from, fund_convert_to, convert_type='fast'):
        self.assert_values(True,
                           self.element_exist("//android.widget.TextView[contains(@text,'%s')]" % fund_convert_from))
        self.assert_values(True,
                           self.element_exist("//android.widget.TextView[contains(@text,'%s')]" % fund_convert_to))
        if convert_type == 'fast':
            self.assert_values('极速转换', self.get_text('com.shhxzq.xjb:id/tv_cash_line_above', 'find_element_by_id'))
        elif convert_type == 'normal':
            self.assert_values('普通转换', self.get_text('com.shhxzq.xjb:id/tv_cash_line_above', 'find_element_by_id'))
        self.assert_values('转入基金',
                           self.get_text('com.shhxzq.xjb:id/tv_fund_convert_to_title', 'find_element_by_id'))
        self.assert_values('转出基金', self.get_text('com.shhxzq.xjb:id/tv_fund_convert_from_title', 'find_element_by_id'))
        self.assert_values(fund_convert_from,
                           self.get_text('com.shhxzq.xjb:id/tv_fund_convert_from_name', 'find_element_by_id'))
        self.assert_values(fund_convert_to,
                           self.get_text('com.shhxzq.xjb:id/tv_fund_convert_to_name', 'find_element_by_id'))
        self.assert_values(True,
                           self.element_exist("//android.widget.TextView[@text='持有份额(份)']"))
        self.assert_values(True,
                           self.element_exist("//android.widget.TextView[@text='可转出份额(份)']"))
        # available_amount = self.get_text('com.shhxzq.xjb:id/tv_available_portion', 'find_element_by_id')
        # ASSERT_DICT.update({'available_amount': available_amount})

        page = self
        return page

    @robot_log
    def fund_convert(self, amount, trade_password):
        available = ASSERT_DICT['available_amount']
        self.perform_actions(AMOUNT, amount,
                             FUND_CONVERT_CONFIRM,
                             TRADE_PASSWORD, trade_password)

        available_amount = available - float(amount)
        ASSERT_DICT.update({'available_amount': available_amount})
        page = huaxin_ui.ui_android_xjb_3_0.user_operation_succeed_page.UserOperationSucceedPage(self.web_driver)

        return page
