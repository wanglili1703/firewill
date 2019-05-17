# coding=utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
from huaxin_ui.ui_ios_xjb_1_8.login_page import LoginPage

LOGIN_REGISTER_BUTTON = u"accId[UIAButton]_(UIButton_登录 / 注册)"
WITHDRAW_BUTTON = u"accId_(UIButton_取出)"
RECHARGE_BUTTON = u"accId_(UIButton_存入)"
PERSONAL_CENTER_BUTTON = "predicate_label CONTAINS 'H*****'"

current_page = []


class HomePage(PageObject):
    def __init__(self, web_driver):
        super(HomePage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def go_to_login_page(self):
        self.perform_actions(LOGIN_REGISTER_BUTTON)
        page = LoginPage(self.web_driver)

        return page
