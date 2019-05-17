# coding: utf-8
import huaxin_ui.ui_android_xjb_3_0.user_operation_succeed_page

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log

BANK_CARD_OPERATOR = "xpath_//android.widget.ImageButton[@resource-id='com.shhxzq.xjb:id/ibtn_actionbar_right']"
BANK_CARD_DELETE = "xpath_//android.widget.TextView[@text='删除']"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"


class MyBankCardPage(PageObject):
    def __init__(self, web_driver):
        super(MyBankCardPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('我的银行卡', self.get_text(self.page_title, 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def verify_bank_card_details(self,last_card_no):
        self.assert_values('工商银行', self.get_text('com.shhxzq.xjb:id/bankNm', 'find_element_by_id'))
        last_card_no_text=self.get_text('com.shhxzq.xjb:id/bankAcc','find_element_by_id')
        last_no_actual = filter(lambda ch: ch in '0123456789.', last_card_no_text)
        self.assert_values(last_card_no, last_no_actual)

        page = self

        return page

    @robot_log
    def delete_bank_card(self, trade_password):
        self.perform_actions(
            BANK_CARD_OPERATOR,
            BANK_CARD_DELETE,
            TRADE_PASSWORD, trade_password)

        page = huaxin_ui.ui_android_xjb_3_0.user_operation_succeed_page.UserOperationSucceedPage(self.web_driver)

        return page

