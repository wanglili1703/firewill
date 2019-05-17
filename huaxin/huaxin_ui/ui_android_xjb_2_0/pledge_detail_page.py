# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log

current_page = []

PLEDGE_AMOUNT="xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/cedt_vip_pledge_input']"
PLEDGE_USE="xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_vip_pledge_use']"
SELECT_PLEDGE_USE="xpath_//android.widget.ListView/android.widget.CheckedTextView[2]"
PLEDGE_SUBMIT="xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_vip_pledge_submit']"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"
PLEDGE_DONE="xpath_//android.widget.Button[@text='确认']"


class PledgeDetailPage(PageObject):
    def __init__(self, web_driver):
        super(PledgeDetailPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def pledge_detail(self,pledge_amount,trade_password):
        self.perform_actions(PLEDGE_AMOUNT,pledge_amount,
                             PLEDGE_USE,
                             SELECT_PLEDGE_USE,
                             PLEDGE_SUBMIT,
                             TRADE_PASSWORD,trade_password,
                             PLEDGE_DONE
                            )

