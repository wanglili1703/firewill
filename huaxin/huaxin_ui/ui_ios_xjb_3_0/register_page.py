# coding: utf-8
from _common.page_object import PageObject

from _common.xjb_decorator import gesture_close_afterwards, user_info_close_afterwards, robot_log, \
    message_cancel_afterwards, message_i_know_afterwards
from _tools.mysql_xjb_tools import MysqlXjbTools
from huaxin_ui.ui_ios_xjb_3_0.binding_card_page import BindingCardPage
import huaxin_ui.ui_ios_xjb_3_0.home_page
import huaxin_ui.ui_ios_xjb_3_0.upload_id_card_page

# PHONE_NUMBER = "accId_UIATextField_(inputTextField)请输入手机号码"
GET_VERIFICATION_CODE = "accId_UIAButton_获取验证码"
PHONE_NUMBER = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIAScrollView/UIATextField"
VERIFICATION_CODE_INPUT = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIAScrollView/UIATextField[2]"
# VERIFICATION_CODE_INPUT = "accId_UIATextField_(inputTextField)请输入验证码"
PASSWORD = "xpathIOS_UIASecureTextField_/AppiumAUT/UIAApplication/UIAWindow/UIAScrollView/UIASecureTextField"
# PASSWORD = "accId_UIASecureTextField_(inputTextField)8~20位字母,数字,符号组成"
LOGIN_PASSWORD_CONFIRM = "accId_UIAButton_(UIButton_注册)"

BINDING_CARD = "accId_UIAButton_绑定银行卡"
SHOPPING_FIRST = "accId_UIAButton_(UIButton_稍后再说)"

TRADE_PASSWORD = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField"
TRADE_PASSWORD_CONFIRM = "accId_UIAButton_下一步"

MEMBER_ALERT_WINDOW_CLOSE = "accId_UIAButton_(UIButton_delete)[POP]"

current_page = []


class RegisterPage(PageObject):
    def __init__(self, web_driver):
        super(RegisterPage, self).__init__(web_driver)
        self.elements_exist(*current_page)
        self._db = MysqlXjbTools()

    # @message_i_know_afterwards
    # @message_cancel_afterwards
    def register(self, phone_number, login_password):
        self.perform_actions(
            PHONE_NUMBER, phone_number,
            GET_VERIFICATION_CODE,
            PASSWORD, login_password,
        )

        verification_code = self._db.get_sms_verify_code(mobile=phone_number, template_id='cif_register')

        self.perform_actions(
            VERIFICATION_CODE_INPUT, verification_code,
            LOGIN_PASSWORD_CONFIRM,
            SHOPPING_FIRST,
        )

        print self.web_driver.page_source

        self.perform_actions(MEMBER_ALERT_WINDOW_CLOSE,
                             "accId_UIAButton_取消[POP]")

        page = huaxin_ui.ui_ios_xjb_3_0.home_page.HomePage(self.web_driver)

        return page

    @robot_log
    def register_binding_card(self, phone_number, login_password, trade_password):
        self.perform_actions(PHONE_NUMBER, phone_number,
                             GET_VERIFICATION_CODE,
                             PASSWORD, login_password)

        verification_code = self._db.get_sms_verify_code(mobile=phone_number, template_id='cif_register')

        self.perform_actions(VERIFICATION_CODE_INPUT, verification_code, )

        self.perform_actions(
            LOGIN_PASSWORD_CONFIRM,
            BINDING_CARD,
            TRADE_PASSWORD, trade_password,
            TRADE_PASSWORD, trade_password,
            TRADE_PASSWORD_CONFIRM,
        )

        page = huaxin_ui.ui_ios_xjb_3_0.upload_id_card_page.UploadIdCardPage(self.web_driver)

        # page = BindingCardPage(self.web_driver)
        return page
