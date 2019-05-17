# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
from _common.global_config import ASSERT_DICT
import huaxin_ui.ui_android_xjb_3_0.security_center_page
import huaxin_ui.ui_android_xjb_3_0.my_referee_page
import huaxin_ui.ui_android_xjb_3_0.assets_page
import huaxin_ui.ui_android_xjb_3_0.login_page
import huaxin_ui.ui_android_xjb_3_0.home_page
from huaxin_ui.ui_android_xjb_3_0.setting_modify_mobile_page import SettingModifyMobilePage
import huaxin_ui.ui_android_xjb_3_0.setting_trade_password_page
import huaxin_ui.ui_android_xjb_3_0.user_account_information_page

MY_REFEREE = "xpath_//android.widget.TextView[@text='我的推荐人']"
SECURITY_CENTER = "xpath_//android.widget.TextView[@text='安全中心']"
BACK = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left']"

BEGAIN_TESTING = "xpath_//android.widget.Button[@content-desc='开始测试']"
ANSWER_CONFIRM = "xpath_//android.widget.Button[@content-desc='确定']"
LOGIN = "xpath_//android.widget.Button[@text='登录']"

SWIPE_BEGIN = "swipe_xpath_//"
LOGOUT_SWIPE_STOP = "swipe_xpath_//android.widget.Button[@text='安全退出']"
LOGOUT = "xpath_//android.widget.Button[@text='安全退出']"
LOGOUT_CONFIRM = "xpath_//android.widget.Button[@text='确认']"
CHANGE_PHONE = "xpath_//android.widget.TextView[@text='手机号码']"
ACCOUNT = "xpath_//android.widget.TextView[@text='账户信息']"

current_page = []


class PersonalSettingPage(PageObject):
    def __init__(self, web_driver):
        super(PersonalSettingPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_page_title(self):
        self.assert_values('设置', self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def go_to_my_referee_page(self):
        self.perform_actions(MY_REFEREE)

        page = huaxin_ui.ui_android_xjb_3_0.my_referee_page.MyRefereePage(self.web_driver)

        return page

    @robot_log
    def go_to_security_center_page(self):
        self.perform_actions(SECURITY_CENTER)
        page = huaxin_ui.ui_android_xjb_3_0.security_center_page.SecurityCenterPage(self.web_driver)

        return page

    # @robot_log
    # def verify_risk_evaluation_result(self):
    #     result = self.get_text(
    #         "//android.widget.TextView[@text='风险测评']/following-sibling::android.widget.LinearLayout[1]/android.widget.TextView").split(
    #         '(')[0]
    #
    #     self.assert_values(ASSERT_DICT['risk_type'], result)
    #     page = self
    #     return page

    @robot_log
    def back_to_assets_page(self):
        self.perform_actions(BACK)
        page = huaxin_ui.ui_android_xjb_3_0.assets_page.AssetsPage(self.web_driver)

        return page

    @robot_log
    def verify_setting_page_details(self, name, risk_type):
        # self.assert_values(name, self.get_text('com.shhxzq.xjb:id/seeting_nm', 'find_element_by_id'))
        # self.assert_values('您的账户已被保护', self.get_text('com.shhxzq.xjb:id/seeting_info', 'find_element_by_id'))
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='我的推荐人']"))
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='账户信息']"))
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='通知设置']"))
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='手机号码']"))
        # self.assert_values(True, self.element_exist("//android.widget.TextView[@text='电子签名约定书']"))
        # self.assert_values(True, self.element_exist("//android.widget.TextView[contains(@text,'签署时间')]"))
        # self.assert_values(True, self.element_exist("//android.widget.TextView[@text='税收居民身份申明']"))
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='安全中心']"))
        # self.assert_values(True, self.element_exist("//android.widget.TextView[@text='风险测评']"))
        # self.assert_values(True, self.element_exist("//android.widget.TextView[contains(@text,'%s')]" % risk_type))
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='帮助中心']"))
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='关于我们']"))

        page = self
        return page

    @robot_log
    def go_to_login_page(self):
        self.perform_actions(LOGIN)

        page = huaxin_ui.ui_android_xjb_3_0.login_page.LoginPage(self.web_driver)
        return page

    @robot_log
    def logout(self):
        self.perform_actions(SWIPE_BEGIN, LOGOUT_SWIPE_STOP, 'U')
        self.perform_actions(LOGOUT,
                             LOGOUT_CONFIRM)

        page = huaxin_ui.ui_android_xjb_3_0.home_page.HomePage(self.web_driver)
        return page

    @robot_log
    def go_to_setting_modify_mobile_page(self, device_id):
        self.perform_actions(CHANGE_PHONE)
        # page = huaxin_ui.ui_android_xjb_3_0.setting_trade_password_page.SettingTradePasswordPage(self.web_driver)
        page = huaxin_ui.ui_android_xjb_3_0.setting_modify_mobile_page.SettingModifyMobilePage(self.web_driver,
                                                                                               device_id)

        return page

    @robot_log
    def go_to_user_account_information_page(self):
        self.perform_actions(ACCOUNT)

        page = huaxin_ui.ui_android_xjb_3_0.user_account_information_page.UserAccountInformationPage(self.web_driver)
        return page
