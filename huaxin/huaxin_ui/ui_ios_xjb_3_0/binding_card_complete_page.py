# coding: utf-8
import time

from _common.page_object import PageObject

from _tools.mysql_xjb_tools import MysqlXjbTools

import huaxin_ui.ui_ios_xjb_3_0.bank_card_management_page

BINDIND_CARD_DONE = "accId_UIAButton_(UIButton_先逛逛)"
DO_RISK_TEST = "accId_UIAButton_(UIButton_去风险测评)"
FINISH = "accId_UIAButton_完成"
SUCCESS_ICON = "//UIAImage[@name='(icon_done.png)']"

current_page = []


class BindingCardCompletePage(PageObject):
    def __init__(self, web_driver):
        super(BindingCardCompletePage, self).__init__(web_driver)
        self.elements_exist(*current_page)
        self._db = MysqlXjbTools()

    def binding_card_confirm(self):
        self.assert_values(True, self.element_exist(SUCCESS_ICON), "==")
        self.perform_actions(BINDIND_CARD_DONE)

        page = huaxin_ui.ui_ios_xjb_3_0.bank_card_management_page.BankCardManagementPage(self.web_driver)

        return page
