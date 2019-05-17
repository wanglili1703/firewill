# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log, user_info_close_afterwards, \
    gesture_close_afterwards, message_cancel_afterwards, message_i_know_afterwards, message_dialog_close
from huaxin_ui.ui_ios_xjb_2_0.register_page import RegisterPage

import huaxin_ui.ui_ios_xjb_2_0.home_page

USER_NAME = "accId_UIATextField_AID_login_mobile"
PASSWORD = "accId_UIASecureTextField_AID_login_password"
LOGIN_BUTTON = "accId_UIAButton_AID_login_btn"
REGISTER_ACCOUNT = "accId_UIAButton_注册账号"
FORGET_LOGIN_PASSWORD = "accId_UIAButton_忘记密码？"
POP_MESSAGE_DELETE = "accId_UIAButton_(UIButton_delete)[POP]"
POP_MESSAGE_CANCEL = "accId_UIAButton_取消[POP]"

current_page = []


class LoginPage(PageObject):
    def __init__(self, web_driver):
        super(LoginPage, self).__init__(web_driver)
        self.elements_exist(*current_page)
        self._return_page = {
            'HomePage': huaxin_ui.ui_ios_xjb_2_0.home_page.HomePage(self.web_driver)
        }

    @robot_log
    @message_i_know_afterwards
    # @message_dialog_close
    # @message_cancel_afterwards
    # @message_dialog_close
    def login(self, user_name, password, return_page):
        self.perform_actions(USER_NAME, user_name,
                             PASSWORD, password,
                             LOGIN_BUTTON,
                             POP_MESSAGE_CANCEL,
                             POP_MESSAGE_DELETE,
                             )

        page = self._return_page[return_page]

        return page

    @robot_log
    def go_to_register_page(self):
        self.perform_actions(REGISTER_ACCOUNT)
        page = RegisterPage(self.web_driver)
        return page
