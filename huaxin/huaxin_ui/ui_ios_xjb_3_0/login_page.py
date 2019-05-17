# coding: utf-8
from _common.page_object import PageObject

from _common.global_config import ASSERT_LIST, ASSERT_DICT
from _common.xjb_decorator import robot_log, user_info_close_afterwards, \
    gesture_close_afterwards, message_cancel_afterwards, message_i_know_afterwards, message_dialog_close
from _tools.mysql_xjb_tools import MysqlXjbTools
from huaxin_ui.ui_ios_xjb_3_0.register_page import RegisterPage
import time

import huaxin_ui.ui_ios_xjb_3_0.home_page
import huaxin_ui.ui_ios_xjb_3_0.assets_page

USER_NAME = "xpathIOS_UIATextField_IOS//UIAStaticText[@label='账号']/following-sibling::UIATextField"
PASSWORD = "xpathIOS_UIASecureTextField_//UIAStaticText[@label='密码']/following-sibling::UIASecureTextField"
LOGIN_BUTTON = "accId_UIAButton_登录"
ACCOUNT_LOGIN_BUTTON = "accId_UIAButton_(UIButton_账号密码登录)[POP]"
MESSAGE_LOGIN_BUTTON = "accId_UIAButton_(UIButton_短信验证码登录)[POP]"
REGISTER_ACCOUNT = "accId_UIAButton_新用户注册"
FORGET_LOGIN_PASSWORD = "accId_UIAButton_忘记密码？"
POP_MESSAGE_DELETE = "accId_UIAButton_(UIButton_delete)[POP]"
POP_MESSAGE_CANCEL = "accId_UIAButton_取消[POP]"

HOME = "accId_UIAButton_(UITabBarButton_item_0)"
# TOTAL_ASSET = "xpathIOS_UIAStaticText_//UIAStaticText[@name='(我的总资产)']/./following-sibling::UIAStaticText[1]"
TOTAL_ASSET = "//UIAStaticText[@name='(我的总资产)']/./following-sibling::UIAStaticText[1]"
XJB_ASSET = "//UIAStaticText[@name='(现金宝)']/./following-sibling::UIAStaticText[1]"
FUND_ASSET = "//UIAStaticText[@name='(基金)']/./following-sibling::UIAStaticText[1]"
DHB_ASSET = "//UIAStaticText[@name='(定活宝)']/./following-sibling::UIAStaticText[1]"
VIP_ASSET = "//UIAStaticText[@name='(高端)']/./following-sibling::UIAStaticText[1]"

GET_VERIFY_CODE = 'accId_UIAButton_(UIButton_获取验证码)'
VERIFICATION_CODE = "xpathIOS_UIATextField_IOS//UIATextField[@value='请输入验证码']"
ASSETS = "accId_UIAButton_(UITabBarButton_item_4)"

current_page = []


class LoginPage(PageObject):
    def __init__(self, web_driver):
        super(LoginPage, self).__init__(web_driver)
        self.elements_exist(*current_page)
        self._return_page = {
            'HomePage': huaxin_ui.ui_ios_xjb_3_0.home_page.HomePage(self.web_driver)
        }

    @robot_log
    # @message_i_know_afterwards
    # @message_dialog_close
    # @message_cancel_afterwards
    # @message_dialog_close
    def login(self, user_name, password, return_page):
        # 切换到账号密码登陆, 现在首次登陆默认是短信验证码登陆, 之后就是用第一次登陆的方式
        self.perform_actions(ACCOUNT_LOGIN_BUTTON)

        self.perform_actions(USER_NAME, user_name,
                             PASSWORD, password,
                             LOGIN_BUTTON,
                             POP_MESSAGE_CANCEL,
                             # POP_MESSAGE_DELETE,
                             )

        self.perform_actions(ASSETS)
        total_asset = str(self.get_text(TOTAL_ASSET)).replace(',', '')

        time.sleep(1)
        xjb_asset = str(self.get_text(XJB_ASSET)).replace(',', '')
        fund_asset = str(self.get_text(FUND_ASSET)).replace(',', '')
        dhb_asset = str(self.get_text(DHB_ASSET)).replace(',', '')
        vip_asset = str(self.get_text(VIP_ASSET)).replace(',', '')

        ASSERT_DICT.update({
            'total_asset': total_asset,
            'xjb_asset': xjb_asset,
            'fund_asset': fund_asset,
            'dhb_asset': dhb_asset,
            'vip_asset': vip_asset
        })

        self.perform_actions(
            HOME,
            # POP_MESSAGE_CANCEL,
            POP_MESSAGE_DELETE,
        )
        self.assert_values('存入', self.get_text('(UIButton_存入)', 'find_element_by_accessibility_id'))
        page = self._return_page[return_page]

        return page

    @robot_log
    def go_to_register_page(self):
        self.perform_actions(REGISTER_ACCOUNT)
        page = RegisterPage(self.web_driver)
        return page

    @robot_log
    def login_use_verification_code(self, user_name, can_login=True):
        self.perform_actions(MESSAGE_LOGIN_BUTTON,
                             USER_NAME, user_name,
                             GET_VERIFY_CODE
                             )
        if can_login is True:
            verification_code = MysqlXjbTools().get_sms_verify_code(mobile=user_name, template_id='cif_login')

            self.perform_actions(
                VERIFICATION_CODE, verification_code,
                LOGIN_BUTTON,
                POP_MESSAGE_CANCEL,
            )
            page = huaxin_ui.ui_ios_xjb_3_0.assets_page.AssetsPage(self.web_driver)
        else:
            self.assert_values(False, self.element_exist("(UIButton_获取验证码)", "find_element_by_accessibility_id"))
            page = self

        return page
