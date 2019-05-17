# coding=utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
from huaxin_ui.ui_android_xjb_3_0.security_center_find_trade_password_page import SecurityCenterFindTradePasswordPage
import huaxin_ui.ui_android_xjb_3_0.setting_trade_password_page

from huaxin_ui.ui_android_xjb_3_0.upload_materials_page import UploadMaterialsPage

FIND_TRADE_PASSWORD = "xpath_//android.widget.TextView[@text='找回交易密码']"
MODIFY_TRADE_PASSWORD = "xpath_//android.widget.TextView[@text='修改交易密码']"


class SecurityCenterTradePasswordPage(PageObject):
    def __init__(self, web_driver):
        super(SecurityCenterTradePasswordPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('交易密码', self.get_text(self.page_title, 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def go_to_find_trade_password_page(self):
        self.perform_actions(FIND_TRADE_PASSWORD)
        page = SecurityCenterFindTradePasswordPage(self.web_driver)

        return page

    @robot_log
    def go_to_upload_materials_page(self):
        self.perform_actions(FIND_TRADE_PASSWORD)

        page = UploadMaterialsPage(self.web_driver)

        return page

    @robot_log
    def go_to_modify_trade_password_page(self):
        self.perform_actions(MODIFY_TRADE_PASSWORD
                             )

        page = huaxin_ui.ui_android_xjb_3_0.setting_trade_password_page.SettingTradePasswordPage(self.web_driver)

        return page
