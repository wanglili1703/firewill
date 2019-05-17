# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
from _common.global_config import ASSERT_DICT
import huaxin_ui.ui_android_xjb_3_0.user_operation_succeed_page

current_page = []

PLEDGE_AMOUNT = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/cedt_vip_pledge_input']"
PLEDGE_USE = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_vip_pledge_use']"
SELECT_PLEDGE_USE = "xpath_//android.widget.ListView/android.widget.CheckedTextView[2]"
PLEDGE_SUBMIT = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_vip_pledge_submit']"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"
PLEDGE_DONE = "xpath_//android.widget.Button[@text='确认']"


class PledgeDetailPage(PageObject):
    def __init__(self, web_driver):
        super(PledgeDetailPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_page_title(self):
        self.assert_values('随心借', self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def pledge(self, pledge_amount, trade_password):
        self.perform_actions(PLEDGE_AMOUNT, pledge_amount,
                             PLEDGE_USE,
                             SELECT_PLEDGE_USE)

        interest = self.get_text('com.shhxzq.xjb:id/tv_vip_pledge_every_day_interest', 'find_element_by_id')
        repay_day = self.get_text('com.shhxzq.xjb:id/vip_pledge_repay_day', 'find_element_by_id')

        ASSERT_DICT.update({'interest': interest,
                            'repay_day': repay_day})

        self.perform_actions(PLEDGE_SUBMIT,
                             TRADE_PASSWORD, trade_password,
                             )

        page = huaxin_ui.ui_android_xjb_3_0.user_operation_succeed_page.UserOperationSucceedPage(self.web_driver)
        return page
