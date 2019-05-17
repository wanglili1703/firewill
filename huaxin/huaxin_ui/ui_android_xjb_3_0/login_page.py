# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log, user_info_close_afterwards, \
    gesture_close_afterwards, dialog_close_afterwards
from huaxin_ui.ui_android_xjb_3_0.register_page import RegisterPage
from _common.global_config import ASSERT_DICT
from _tools.mysql_xjb_tools import MysqlXjbTools

import huaxin_ui.ui_android_xjb_3_0.assets_page
import huaxin_ui.ui_android_xjb_3_0.security_center_page
import huaxin_ui.ui_android_xjb_3_0.personal_setting_page
import huaxin_ui.ui_android_xjb_3_0.home_page
import time

USER_NAME = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/account_edit']"
# PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/etPwd']"
PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/psw_edit']"
LOGIN_BUTTON = "xpath_//android.widget.Button[@text='登录']"
REGISTER_ACCOUNT = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/login_register_bt']"
FORGET_LOGIN_PASSWORD = "xpath_//android.widget.TextView[@text='忘记密码？']"
SWIPE_BEGIN = "swipe_xpath_//"
SWIPE_STOP = "swipe_xpath_//android.widget.TextView[@text='我的优惠券']"
ACCOUNT_SWITCH = "xpath_//android.widget.TextView[@text='账号密码登录'][POP]"
ACCOUNT_SWITCH_CODE = "xpath_//android.widget.TextView[@text='短信验证码登录'][POP]"

POP_CANCEL = "xpath_//android.widget.TextView[@text='取消'][POP]"
POP_DIALOG_CLOSE = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/img_dialog_close'][POP]"
PERMISSION_CLOSE = "xpath_//android.widget.Button[@resource-id='com.android.packageinstaller:id/permission_allow_button'][POP]"
# MODIFIED_USER_NAME_CLICK="xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/etAccount']"
MODIFIED_USER_NAME_CLICK = "axis_Android_****_0,0"
USER_NAME_MODIFIED = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/etAccount']"
VERIFICATION_CODE = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/mobile_code_edit']"
GET_VERIFY_CODE = "xpath_//android.widget.TextView[@text='获取验证码']"

current_page = []


class LoginPage(PageObject):
    def __init__(self, web_driver):
        super(LoginPage, self).__init__(web_driver)
        self.elements_exist(*current_page)
        self._return_page = {
            'AssetsPage': huaxin_ui.ui_android_xjb_3_0.assets_page.AssetsPage(self.web_driver),
            'SecurityCenterPage': huaxin_ui.ui_android_xjb_3_0.security_center_page.SecurityCenterPage(self.web_driver),
            'PersonalSettingPage': huaxin_ui.ui_android_xjb_3_0.personal_setting_page.PersonalSettingPage(
                self.web_driver),
            'HomePage': huaxin_ui.ui_android_xjb_3_0.home_page.HomePage(self.web_driver)
        }

    @robot_log
    def verify_login_button(self):
        self.assert_values('登录', self.get_text('com.shhxzq.xjb:id/login_bt', 'find_element_by_id'))

        page = self

        return page

    @robot_log
    @user_info_close_afterwards
    # @dialog_close_afterwards
    # @gesture_close_afterwards
    def login(self, user_name=None, password=None, return_page=None, flag=None):
        if flag is None or flag == 'setting_page_login':
            self.perform_actions(ACCOUNT_SWITCH)
        else:
            self.perform_actions(MODIFIED_USER_NAME_CLICK)

        self.perform_actions(USER_NAME, user_name,
                             PASSWORD, password,
                             LOGIN_BUTTON,
                             POP_CANCEL,
                             POP_DIALOG_CLOSE,
                             PERMISSION_CLOSE
                             )

        time.sleep(3)

        if flag is None:
            associator_center = str(self.get_text('//android.widget.TextView[@text=\'会员中心\']'))

            # self.perform_actions(SWIPE_BEGIN, SWIPE_STOP, 'U')

            total_asset = str(self.get_text('com.shhxzq.xjb:id/total_assets', 'find_element_by_id')).replace(',', '')
            xjb_total_assets = str(self.get_text(
                '//android.widget.TextView[@text=\'现金宝\']/./following-sibling::android.widget.TextView[1]')).replace(
                ',', '')
            fund_asset = str(self.get_text(
                '//android.widget.TextView[@text=\'基金\']/./following-sibling::android.widget.TextView[1]')).replace(',',
                                                                                                                    '')
            dhb_asset = str(self.get_text(
                '//android.widget.TextView[@text=\'定活宝\']/./following-sibling::android.widget.TextView[1]')).replace(
                ',', '')
            vip_asset = str(self.get_text(
                '//android.widget.TextView[@text=\'高端\']/./following-sibling::android.widget.TextView[1]')).replace(',',
                                                                                                                    '')
            # associator_center = str(self.get_text('com.shhxzq.xjb:id/user_level'), 'find_element_by_id').replace(',', '')

            ASSERT_DICT.update({'total_asset': total_asset,
                                # 'xjb_total_assets': xjb_total_assets,
                                'xjb_total_assets_login': xjb_total_assets,
                                # 'dhb_asset': dhb_asset,
                                'dhb_asset_login': dhb_asset,
                                # 'fund_asset': fund_asset,
                                'fund_asset_login': fund_asset,
                                # 'vip_asset': vip_asset,
                                'vip_asset_login': vip_asset,
                                'associator_center': associator_center,
                                })

        page = self._return_page[return_page]

        return page

    @robot_log
    def go_to_register_page(self, device_id=None):
        self.perform_actions(REGISTER_ACCOUNT)
        page = RegisterPage(self.web_driver, device_id)
        return page

    @robot_log
    def login_use_verification_code(self, user_name=None, verification_code='123456', mode='on', return_page=None,
                                    flag=None):
        self.perform_actions(ACCOUNT_SWITCH_CODE)

        if user_name is not None:
            self.perform_actions(USER_NAME, user_name)

        self.perform_actions(GET_VERIFY_CODE)

        if user_name is not None:
            verification_code = MysqlXjbTools().get_sms_verify_code(mobile=user_name, template_id='cif_login')

        if flag == 'modify_mobile':
            self.assert_values('您输入的手机号码有误或尚未注册现金宝账号', self.get_text('com.shhxzq.xjb:id/message', 'find_element_by_id'))

        page = huaxin_ui.ui_android_xjb_3_0.assets_page.AssetsPage(self.web_driver)

        if mode == 'on':
            self.perform_actions(VERIFICATION_CODE, verification_code,
                                 LOGIN_BUTTON,
                                 POP_CANCEL,
                                 POP_DIALOG_CLOSE,
                                 PERMISSION_CLOSE
                                 )
            page = self._return_page[return_page]

        elif mode == 'off':
            self.assert_values('短信验证码登录', self.get_text('com.shhxzq.xjb:id/sms_login', 'find_element_by_id'))
            page = self

        return page
