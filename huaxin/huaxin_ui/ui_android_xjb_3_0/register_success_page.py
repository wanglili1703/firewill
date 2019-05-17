# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log, gesture_close_afterwards
import huaxin_ui.ui_android_xjb_3_0.assets_page
import huaxin_ui.ui_android_xjb_3_0.setting_trade_password_page

STROLL="xpath_//android.widget.TextView[@text='先逛逛']"
BINDING_CARD="xpath_//android.widget.Button[@text='绑定银行卡']"
PERMISSION_CLOSE="xpath_//android.widget.Button[@resource-id='com.android.packageinstaller:id/permission_allow_button'][POP]"

class RegisterSuccessPage(PageObject):
    def __init__(self, web_driver):
        super(RegisterSuccessPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('注册成功', self.get_text('com.shhxzq.xjb:id/title_actionbar', 'find_element_by_id'))

        page = self

        return page

    @gesture_close_afterwards
    @robot_log
    def stroll_first(self):
        self.perform_actions(STROLL)

        page = huaxin_ui.ui_android_xjb_3_0.assets_page.AssetsPage(self.web_driver)
        self.perform_actions(PERMISSION_CLOSE)

        return page

    @robot_log
    def go_to_set_trade_password_page(self):
        self.perform_actions(BINDING_CARD)

        page = huaxin_ui.ui_android_xjb_3_0.setting_trade_password_page.SettingTradePasswordPage(self.web_driver)

        return page







