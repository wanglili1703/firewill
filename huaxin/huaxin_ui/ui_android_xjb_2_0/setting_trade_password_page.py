# coding=utf-8
from _common.page_object import PageObject
from selenium.common.exceptions import NoSuchElementException

import huaxin_ui.ui_android_xjb_2_0.security_center_page
from _common.xjb_decorator import robot_log

FIND_TRADE_PASSWORD = "xpath_//android.widget.TextView[@text='找回交易密码']"
MODIFY_TRADE_PASSWORD = "xpath_//android.widget.TextView[@text='修改交易密码']"
CURRENT_TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/tradepwd_et']"
CURRENT_TRADE_PASSWORD_CONFIRM = "xpath_//android.widget.Button[@text='下一步']"
SETTING_TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/tradepwd_et']"
SETTING_TRADE_PASSWORD_AGAIN = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/tradepwd_et']"
SETTING_TRADE_PASSWORD_AGAIN_CONFIRM = "xpath_//android.widget.Button[@text='下一步']"

ID_FACE = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/pickFront']"
FIND_TRADE_PASSWORD_NEXT = "//android.widget.Button[@content-desc='下一步']"
ID_BACK = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/pickBack']"
FROM_PHONE_PICTURE = "xpath_//android.widget.TextView[@text='从手机相册选择']"
# FROM_PHONE_PICTURE="xpath_//android.widget.ImageView[@resource-id='com.android.gallery3d:id/album_cover_image']"

ALBUM = "xpath_//android.widget.TextView[@text='相册']"
CAMERA = "xpath_//android.widget.TextView[@text='相机']"
# SELECT_PICTURES="xpath_//android.widget.TextView[@text='选择图片']"
# ID_FACE_PICTURE = "xpath_//*[contains(@text,'月')]"
# ID_BAC_PICTURE = "xpath_//*[contains(@text,'月')]"
ID_FACE_PICTURE = "axis_Android_选择图片_-0.125,0.125"
REPEATED_SUBMIT_COMFIRM = "xpath_//android.widget.Button[@text='确定']"

ID_CONFIRM = "xpath_//android.widget.ImageButton[@content-desc='确定']"
ID_SUBMIT_CONFIRM = "xpath_//android.widget.Button[@text='确认']"
SETTING_TRADE_PASSWORD_DONE = "xpath_//android.widget.Button[@text='确认']"

current_page = []


class SettingTradePasswordPage(PageObject):
    def __init__(self, web_driver):
        super(SettingTradePasswordPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def modify_trade_password(self, trade_password_old, trade_password_new):
        self.perform_actions(
            MODIFY_TRADE_PASSWORD,
            CURRENT_TRADE_PASSWORD, trade_password_old,
            CURRENT_TRADE_PASSWORD_CONFIRM,
            SETTING_TRADE_PASSWORD, trade_password_new,
            SETTING_TRADE_PASSWORD_AGAIN, trade_password_new,
            SETTING_TRADE_PASSWORD_AGAIN_CONFIRM,
        )

        page = huaxin_ui.ui_android_xjb_2_0.security_center_page.SecurityCenterPage(self.web_driver)

        return page

    @robot_log
    def find_trade_password(self):
        self.perform_actions(
            FIND_TRADE_PASSWORD,
        )

        try:
            button = self.web_driver.find_element_by_xpath(FIND_TRADE_PASSWORD_NEXT)
            button.click()
        except NoSuchElementException:
            pass

        self.perform_actions(
            ID_FACE,
            FROM_PHONE_PICTURE,
            CAMERA,
            # ALBUM,
            ID_FACE_PICTURE,
            ID_CONFIRM,
            ID_SUBMIT_CONFIRM,
            REPEATED_SUBMIT_COMFIRM,
            SETTING_TRADE_PASSWORD_DONE,
        )

        page = huaxin_ui.ui_android_xjb_2_0.security_center_page.SecurityCenterPage(self.web_driver)

        return page
