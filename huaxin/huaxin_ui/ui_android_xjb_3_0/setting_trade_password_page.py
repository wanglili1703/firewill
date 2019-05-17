# coding=utf-8
from _common.page_object import PageObject
from selenium.common.exceptions import NoSuchElementException

import huaxin_ui.ui_android_xjb_3_0.security_center_page
import huaxin_ui.ui_android_xjb_3_0.binding_card_detail_page
import huaxin_ui.ui_android_xjb_3_0.binding_card_page
import huaxin_ui.ui_android_xjb_3_0.binding_card_input_id_information_page
import huaxin_ui.ui_android_xjb_3_0.setting_modify_mobile_page
from _common.xjb_decorator import robot_log

FIND_TRADE_PASSWORD = "xpath_//android.widget.TextView[@text='找回交易密码']"
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
# ID_FACE_PICTURE = "axis_Android_选择图片_-0.125,0.125"
# ID_FACE_PICTURE = "axis_Android_选择图片_-0.125,0.125"
REPEATED_SUBMIT_COMFIRM = "xpath_//android.widget.Button[@text='确定']"
ID_CONFIRM = "xpath_//android.widget.ImageButton[@content-desc='确定']"
ID_SUBMIT_CONFIRM = "xpath_//android.widget.Button[@text='确认']"
SETTING_TRADE_PASSWORD_DONE = "xpath_//android.widget.Button[@text='确认']"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/tradepwd_et']"
NEXT = "xpath_//android.widget.Button[@text='下一步']"

current_page = []


class SettingTradePasswordPage(PageObject):
    def __init__(self, web_driver):
        super(SettingTradePasswordPage, self).__init__(web_driver)
        self.elements_exist(*current_page)
        self._return_page = {'BindingCardPage': huaxin_ui.ui_android_xjb_3_0.binding_card_page.BindingCardPage(
            self.web_driver)
        }

    @robot_log
    def verify_page_title(self, title='设置交易密码'):
        self.assert_values(title, self.get_text(self.page_title, 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def modify_trade_password(self, trade_password_old, trade_password_new):
        self.perform_actions(
            CURRENT_TRADE_PASSWORD, trade_password_old,
            CURRENT_TRADE_PASSWORD_CONFIRM,
            SETTING_TRADE_PASSWORD, trade_password_new,
            SETTING_TRADE_PASSWORD_AGAIN, trade_password_new,
            SETTING_TRADE_PASSWORD_AGAIN_CONFIRM,
        )

        page = huaxin_ui.ui_android_xjb_3_0.security_center_page.SecurityCenterPage(self.web_driver)

        return page

    @robot_log
    def set_trade_password(self, trade_password):
        self.perform_actions(TRADE_PASSWORD, trade_password)

        page = self

        return page

    @robot_log
    def confirm_trade_password(self, trade_password, return_page='BindingCardInputIdInformationPage',
                               device_id=None):
        self.perform_actions(TRADE_PASSWORD, trade_password)

        if return_page == 'SettingModifyMobilePage':
            self.perform_actions(SETTING_TRADE_PASSWORD_DONE)
            page = huaxin_ui.ui_android_xjb_3_0.setting_modify_mobile_page.SettingModifyMobilePage(self.web_driver,
                                                                                                   device_id)
        else:
            self.perform_actions(NEXT)

            if return_page == 'BindingCardInputIdInformationPage':
                page = huaxin_ui.ui_android_xjb_3_0.binding_card_input_id_information_page.BindingCardInputIdInformationPage(
                    self.web_driver)
            else:
                page = self._return_page[return_page]

        return page
