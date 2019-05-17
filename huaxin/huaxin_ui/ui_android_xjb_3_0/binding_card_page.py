# coding: utf-8
import time

from _common.page_object import PageObject
from _common.xjb_decorator import gesture_close_afterwards, user_info_close_afterwards, robot_log

from _tools.mysql_xjb_tools import MysqlXjbTools

import huaxin_ui.ui_android_xjb_3_0.home_page
import huaxin_ui.ui_android_xjb_3_0.binding_card_complete_page
import huaxin_ui.ui_android_xjb_3_0.user_operation_succeed_page
import huaxin_ui.ui_android_xjb_3_0.binding_card_detail_page

USER_NAME = "xpath_//android.widget.EditText[@text='请输入您本人的姓名']"
ID_NO = "xpath_//android.widget.EditText[@text='请输入您的证件号码']"
CARD_NO = "xpath_//android.widget.EditText[@text='请输入您的储蓄卡卡号']"
PHONE_NUMBER = "xpath_//android.widget.EditText[@text='请输入银行预留手机号码']"
GET_VERIFY_CODE = "xpath_//android.widget.Button[@text='获取验证码']"
VERIFY_CODE_INPUT = "xpath_//android.widget.EditText[@text='请输入验证码']"
BINDIND_CARD_CONFIRM = "xpath_//android.widget.Button[@text='下一步']"
INPUT_ID_INFORMATION = "xpath_//android.widget.TextView[@text='手动输入身份信息']"
current_page = []


class BindingCardPage(PageObject):
    def __init__(self, web_driver, device_id=None):
        super(BindingCardPage, self).__init__(web_driver, device_id)
        self._db = MysqlXjbTools()

    @robot_log
    def verify_page_title(self):
        self.assert_values('绑定银行卡', self.get_text('com.shhxzq.xjb:id/title_actionbar', 'find_element_by_id'))

        page = self

        return page

    # @user_info_close_afterwards
    # @gesture_close_afterwards
    def binding_card(self, user_name, id_no, band_card_no, phone_number):
        self.perform_actions(USER_NAME, user_name,
                             ID_NO, id_no,
                             CARD_NO, band_card_no,
                             PHONE_NUMBER, phone_number,
                             GET_VERIFY_CODE,
                             )

        verification_code = MysqlXjbTools().get_sms_verify_code(mobile=phone_number, template_id='cif_bindBankCard')

        self.perform_actions(VERIFY_CODE_INPUT, verification_code,
                             BINDIND_CARD_CONFIRM
                             )

        page = huaxin_ui.ui_android_xjb_3_0.binding_card_complete_page.BindingCardCompletePage(self.web_driver)

        return page

    @robot_log
    def certificated_user_binding_bank_card(self, bank_card_no, mobile):
        self.perform_actions(
            CARD_NO, bank_card_no,
            PHONE_NUMBER, mobile,
            GET_VERIFY_CODE,
        )

        verification_code = self._db.get_sms_verify_code(mobile=mobile, template_id='cif_bindBankCard')

        self.perform_actions(
            VERIFY_CODE_INPUT, verification_code,
            BINDIND_CARD_CONFIRM
        )

        page = huaxin_ui.ui_android_xjb_3_0.user_operation_succeed_page.UserOperationSucceedPage(self.web_driver)

        return page

    @robot_log
    def go_to_binding_card_detail_page(self, device_id):
        self.perform_actions(INPUT_ID_INFORMATION)

        page = huaxin_ui.ui_android_xjb_3_0.binding_card_detail_page.BindingCardDetailPage(self.web_driver,
                                                                                           device_id)

        return page
