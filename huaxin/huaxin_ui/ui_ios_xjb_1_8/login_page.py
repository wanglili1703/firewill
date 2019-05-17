# coding: utf-8
import sys

from _common.global_config import GlobalConfig
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log, user_info_close_afterwards, \
    gesture_close_afterwards

USER_NAME = "accId[UIATextField]_AID_login_mobile"
PASSWORD = "accId[UIATextField]_AID_login_password"
LOGIN_BUTTON = "accId[UIAButton]_AID_login_btn"
REGISTER_ACCOUNT = "accId_AID_register_btn"
FORGET_LOGIN_PASSWORD = "accId_AID_forget_pwd_btn"

current_page = []


class LoginPage(PageObject):
    def __init__(self, web_driver):
        super(LoginPage, self).__init__(web_driver)
        self.elements_exist(*current_page)
        self.activity_map_return_page = {}

    @robot_log
    # @user_info_close_afterwards
    # @gesture_close_afterwards
    def login(self, user_name, password):
        self.perform_actions(USER_NAME, user_name,
                             PASSWORD, password,
                             LOGIN_BUTTON,
                             )
