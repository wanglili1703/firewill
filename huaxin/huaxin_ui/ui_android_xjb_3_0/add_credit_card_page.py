# coding=utf-8
import time
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
from _tools.mysql_xjb_tools import MysqlXjbTools
import huaxin_ui.ui_android_xjb_3_0.user_operation_succeed_page

CREDIT_CARD_NO = "xpath_//android.widget.EditText[@text='请输入您的信用卡卡号']"
PHONE_NO = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/bind_card_phonenumber']"
GET_VERIFY_CODE = "xpath_//android.widget.Button[@text='获取验证码']"
INPUT_VERIFY_CODE = "xpath_//android.widget.EditText[@text='请输入验证码']"
ADD_CREDIT_CARD_CONFIRM = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/bind_card_sure_bt']"


class AddCreditCardPage(PageObject):
    def __init__(self, web_driver, device_id=None):
        super(AddCreditCardPage, self).__init__(web_driver, device_id)

    @robot_log
    def verify_page_title(self):
        self.assert_values('添加信用卡', self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def add_credit_card(self, credit_card_no, phone_no):
        time.sleep(3)

        self.perform_actions(
            CREDIT_CARD_NO, credit_card_no,
            PHONE_NO, phone_no,
            GET_VERIFY_CODE,
        )

        _db = MysqlXjbTools()
        verify_code = _db.get_sms_verify_code(mobile=phone_no, template_id='credit_bind_card')

        self.perform_actions(
            INPUT_VERIFY_CODE, verify_code,
            ADD_CREDIT_CARD_CONFIRM,
        )

        page = self

        return page

    @robot_log
    def add_credit_card(self, credit_card_no, phone_no):
        self.perform_actions(
            CREDIT_CARD_NO, credit_card_no,
            PHONE_NO, phone_no,
            GET_VERIFY_CODE,
        )

        _db = MysqlXjbTools()
        verify_code = _db.get_sms_verify_code(mobile=phone_no, template_id='credit_bind_card')

        self.perform_actions(
            INPUT_VERIFY_CODE, verify_code,
            ADD_CREDIT_CARD_CONFIRM)

        page = huaxin_ui.ui_android_xjb_3_0.user_operation_succeed_page.UserOperationSucceedPage(self.web_driver)

        return page

