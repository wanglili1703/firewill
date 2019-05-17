# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.security_center_page

MODE_CHANGE = "xpath_//android.widget.ToggleButton[@resource-id='com.shhxzq.xjb:id/tbtn_login_way']"
OFF = "xpath_//android.widget.Button[@text='关闭']"
BACK = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left']"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"


class LoginModePage(PageObject):
    def __init__(self, web_driver):
        super(LoginModePage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('登录方式', self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def modify_login_mode(self, mode='off', trade_password=None):
        self.perform_actions(MODE_CHANGE)
        if mode == 'off':
            self.perform_actions(OFF)
        elif mode == 'on':
            self.perform_actions(TRADE_PASSWORD, trade_password)
        page = self
        return page

    @robot_log
    def back_to_security_center_page(self):
        self.perform_actions(BACK)

        page = huaxin_ui.ui_android_xjb_3_0.security_center_page.SecurityCenterPage(self.web_driver)
        return page
