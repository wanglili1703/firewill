# coding: utf-8

from _common.page_object import PageObject

from _common.xjb_decorator import robot_log

import huaxin_ui.ui_ios_xjb_3_0.home_page
from huaxin_ui.ui_ios_xjb_3_0.security_center_page import SecurityCenterPage
import huaxin_ui.ui_ios_xjb_3_0.account_info_page
import huaxin_ui.ui_ios_xjb_3_0.setting_modify_mobile_page

MY_REFEREE = "accId_UIAStaticText_(我的推荐人)"
# PHONE_NO = "accId_UIATextField_(textField)请输入11位手机号码"
PHONE_NO = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField"
REFEREE_CONFIRM = "accId_UIAButton_提交"
SAFETY_LOGOUT = "accId_UIAStaticText_(安全退出)"
ACCOUNT_INFO = "accId_UIAStaticText_(账户信息)"
SAFETY_LOGOUT_CONFIRM = "axis_IOS_退出[index]1"

# RISK_EVALUATING = "accId_UIAStaticText_(风险评测)"
RISK_EVALUATING = "xpathIOS_UIAStaticText_//UIAStaticText[@label='风险评测']"
NOTICE_SETTING = "accId_UIAStaticText_(通知设置)"
HELP_CENTER = "accId_UIAStaticText_(帮组中心)"
ABOUT_US = "accId_UIAStaticText_(关于我们)"

# SECURITY_CENTER = "accId_UIAStaticText_(安全中心)"
SECURITY_CENTER = "xpathIOS_UIAStaticText_//UIAStaticText[@label='安全中心']"
DIGITAL_SIGNATURE = "accId_UIAStaticText_(电子签名约定书)"

TRADE_PASSWORD_BUTTON = "accId_UIAStaticText_交易密码"
CHANGE_PHONE_BUTTON = "accId_UIAStaticText_手机号码"

current_page = []


class PersonalSettingPage(PageObject):
    def __init__(self, web_driver):
        super(PersonalSettingPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_at_personal_setting_page(self):
        self.assert_values('设置', self.get_text('//UIAStaticText[@name=\'设置\']'))
        page = self
        return page

    @robot_log
    def my_referee(self, phone_no):
        self.perform_actions(MY_REFEREE,
                             PHONE_NO, phone_no,
                             REFEREE_CONFIRM,
                             )

        page = self
        self.assert_values('设置', self.get_text('//UIAStaticText[@name=\'设置\']'))

        return page

    @robot_log
    def go_to_account_info_page(self):
        self.perform_actions(ACCOUNT_INFO)

        page = huaxin_ui.ui_ios_xjb_3_0.account_info_page.AccountInfoPage(self.web_driver)
        return page

    @robot_log
    def logout_app(self):
        self.perform_actions(SAFETY_LOGOUT,
                             SAFETY_LOGOUT_CONFIRM,
                             )

        page = huaxin_ui.ui_ios_xjb_3_0.home_page.HomePage(self.web_driver)

        return page

    @robot_log
    def go_to_security_center_page(self):
        self.perform_actions(SECURITY_CENTER)
        page = SecurityCenterPage(self.web_driver)

        return page

    @robot_log
    def go_to_setting_modify_mobile_page(self):
        self.perform_actions(CHANGE_PHONE_BUTTON)
        page = huaxin_ui.ui_ios_xjb_3_0.setting_modify_mobile_page.SettingModifyMobilePage(self.web_driver)

        return page
