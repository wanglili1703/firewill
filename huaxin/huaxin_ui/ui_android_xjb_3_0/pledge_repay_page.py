# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import re
from _common.global_config import ASSERT_DICT

import huaxin_ui.ui_android_xjb_3_0.user_operation_succeed_page

REPAY_AMOUNT="xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/et_current_repay_amt']"
COMFIRM="xpath_//android.widget.Button[@text='还款']"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"
SWIPE_BEGIN="swipe_xpath_//"
COMFIRM_SWIPE_STOP="swipe_xpath_//android.widget.Button[@text='还款']"

class PledgeRepayPage(PageObject):
    def __init__(self, web_driver):
        super(PledgeRepayPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('随心还', self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def pledge_repay(self,pledge_repay_amount,trade_password):
        pledge_repay_amount_require_text=self.get_text('com.shhxzq.xjb:id/repay_explain_tv', 'find_element_by_id')
        pledge_repay_amount_min=float(re.findall(r'(\d{1,3}(,\d{3})*.\d+)', pledge_repay_amount_require_text)[0][0].replace(',', ''))
        pledge_repay_amount_threshold=float(re.findall(r'(\d{1,3}(,\d{3})*.\d+)', pledge_repay_amount_require_text)[1][0].replace(',', ''))
        interest_text=self.get_text('com.shhxzq.xjb:id/interest_tv','find_element_by_id')
        interest = '%.2f' % float(filter(lambda ch: ch in '0123456789.', interest_text))
        ASSERT_DICT.update({'interest':interest})
        # if pledge_repay_amount<pledge_repay_amount_min:
        #     page = self
        # elif pledge_repay_amount>= pledge_repay_amount_min and pledge_repay_amount

        self.perform_actions(REPAY_AMOUNT,pledge_repay_amount)

        self.perform_actions(SWIPE_BEGIN,COMFIRM_SWIPE_STOP,'U')

        self.perform_actions(COMFIRM)
        self.perform_actions(TRADE_PASSWORD,trade_password)

        page= huaxin_ui.ui_android_xjb_3_0.user_operation_succeed_page.UserOperationSucceedPage(self.web_driver)
        return page
