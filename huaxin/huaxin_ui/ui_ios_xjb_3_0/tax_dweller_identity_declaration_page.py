# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.account_info_page
import time

IDENTITY = "xpathIOS_UIAStaticText_//UIAStaticText[@label='%s']"
CONFIRM = "xpathIOS_UIAButton_//UIAButton[@label='确定']"
IDENTITY_CONFIRM = "xpathIOS_UIAButton_//UIAButton[@label='确认']"
IDENTITY_SELECTED = "//UIAStaticText[@label='仅为中国税收居民']/following-sibling::UIAImage"


class TaxDwellerIdentityDeclarationPage(PageObject):
    def __init__(self, web_driver):
        super(TaxDwellerIdentityDeclarationPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        time.sleep(1)
        self.assert_values('选择税收居民身份', self.get_text("//UIAStaticText[@label='选择税收居民身份']"))

        page = self
        return page

    @robot_log
    def select_tax_dweller_identity(self, identity):
        self.perform_actions(IDENTITY % identity)
        page = self
        if identity == '既为中国税收居民又是其他国家（地区）税收居民' or identity == '仅为非居民':
            self.perform_actions(CONFIRM)
        if identity == '仅为中国税收居民':
            self.perform_actions(IDENTITY_CONFIRM)
            page = huaxin_ui.ui_ios_xjb_3_0.account_info_page.AccountInfoPage(self.web_driver)

        return page

    @robot_log
    def verify_tax_dweller_identity_result(self):
        self.assert_values(True, self.element_exist(IDENTITY_SELECTED))

        page = self
        return page
