# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.personal_setting_page
import time
IDENTITY = "xpath_//android.view.View[@content-desc='%s']"
# CONFIRM = "xpath_//android.view.View[contains(@content-desc,'补齐相关信息')]/following-sibling::android.view.View[1]/android.widget.Button[@content-desc='确定']"
CONFIRM = "xpath_//android.widget.Button[@content-desc='确定']"
IDENTITY_CONFIRM = "xpath_//android.widget.Button[@content-desc='确认']"
IDENTITY_SELECTED = "//android.view.View[@content-desc='仅为中国税收居民']/following-sibling::android.widget.Image[1]"


class TaxDwellerIdentityDeclarationPage(PageObject):
    def __init__(self, web_driver):
        super(TaxDwellerIdentityDeclarationPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        time.sleep(2)
        self.assert_values('选择税收居民身份', self.get_text(self.page_title, 'find_element_by_id'))

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
            page = huaxin_ui.ui_android_xjb_3_0.personal_setting_page.PersonalSettingPage(self.web_driver)

        return page

    @robot_log
    def verify_tax_dweller_identity_result(self):
        self.assert_values(True, self.element_exist(IDENTITY_SELECTED))

        page = self
        return page
