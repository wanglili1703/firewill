# coding: utf-8
from _common.page_object import PageObject

from _common.xjb_decorator import gesture_close_afterwards, user_info_close_afterwards, robot_log
from _tools.mysql_xjb_tools import MysqlXjbTools
from huaxin_ui.ui_android_xjb_2_0.binding_card_page import BindingCardPage
import huaxin_ui.ui_android_xjb_2_0.home_page

PHONE_NUMBER = "xpath_//android.widget.EditText[@text='请输入手机号码']"
GET_VERIFICATION_CODE = "xpath_//android.widget.Button[@text='获取验证码']"
VERIFICATION_CODE_INPUT = "xpath_//android.widget.EditText[@text='请输入验证码']"
PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/register_pwd']"
LOGIN_PASSWORD_CONFIRM = "xpath_//android.widget.Button[@text='注册']"

BINDING_CARD = "xpath_//android.widget.Button[@text='绑定银行卡']"
SHOPPING_FIRST = "xpath_//android.widget.TextView[@text='先逛逛']"

TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/tradepwd_et']"
TRADE_PASSWORD_CONFIRM = "xpath_//android.widget.Button[@text='下一步']"

current_page = []


class RegisterPage(PageObject):
    def __init__(self, web_driver):
        super(RegisterPage, self).__init__(web_driver)
        self.elements_exist(*current_page)
        self._db = MysqlXjbTools()

    @user_info_close_afterwards
    @gesture_close_afterwards
    def register(self, phone_number, login_password):
        self.perform_actions(
            PHONE_NUMBER, phone_number,
            GET_VERIFICATION_CODE,
            PASSWORD, login_password,
        )

        verification_code = MysqlXjbTools().get_sms_verify_code(mobile=phone_number, template_id='cif_register')

        self.perform_actions(
            VERIFICATION_CODE_INPUT, verification_code,
            LOGIN_PASSWORD_CONFIRM,
            SHOPPING_FIRST,
        )

        page = huaxin_ui.ui_android_xjb_2_0.home_page.HomePage(self.web_driver)

        return page

    @robot_log
    def register_binding_card(self, phone_number, login_password, trade_password):
        self.perform_actions(PHONE_NUMBER, phone_number,
                             GET_VERIFICATION_CODE,
                             PASSWORD, login_password)

        verification_code = MysqlXjbTools().get_sms_verify_code(mobile=phone_number, template_id='cif_register')

        self.perform_actions(VERIFICATION_CODE_INPUT, verification_code, )

        self.perform_actions(
            LOGIN_PASSWORD_CONFIRM,
            BINDING_CARD,
            TRADE_PASSWORD, trade_password,
            TRADE_PASSWORD, trade_password,
            TRADE_PASSWORD_CONFIRM,
        )

        page = BindingCardPage(self.web_driver)

        return page
