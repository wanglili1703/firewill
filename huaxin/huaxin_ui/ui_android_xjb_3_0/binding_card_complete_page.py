# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
from _common.xjb_decorator import gesture_close_afterwards
import huaxin_ui.ui_android_xjb_3_0.assets_page
import huaxin_ui.ui_android_xjb_3_0.add_credit_card_page
import huaxin_ui.ui_android_xjb_3_0.bank_card_management_page

BINDIND_CARD_DONE = "xpath_//android.widget.TextView[@text='先逛逛']"
STROLL = "xpath_//android.widget.TextView[@text='先逛逛']"
DO_RISK_TEST = "xpath_//android.widget.Button[@text='去风险测评']"
PERMISSION_CLOSE="xpath_//android.widget.Button[@resource-id='com.android.packageinstaller:id/permission_allow_button'][POP]"

class BindingCardCompletePage(PageObject):
    def __init__(self, web_driver):
        super(BindingCardCompletePage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('完成', self.get_text(self.page_title, 'find_element_by_id'))
        page = self

        return page

    @gesture_close_afterwards
    def binding_card_confirm(self):
        self.perform_actions(BINDIND_CARD_DONE)

        page = huaxin_ui.ui_android_xjb_3_0.assets_page.AssetsPage(self.web_driver)
        self.perform_actions(PERMISSION_CLOSE)

        return page

    def go_to_add_credit_card_page(self):
        self.perform_actions(BINDIND_CARD_DONE)

        page = huaxin_ui.ui_android_xjb_3_0.add_credit_card_page.AddCreditCardPage(self.web_driver)

        return page

    @robot_log
    def stroll_first(self):
        self.perform_actions(STROLL)

        page = huaxin_ui.ui_android_xjb_3_0.bank_card_management_page.BankCardManagementPage(self.web_driver)
        self.perform_actions(PERMISSION_CLOSE)

        return page




