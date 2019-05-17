# coding: utf-8

from  _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.useroperation_succeed_page
from _tools.mysql_xjb_tools import MysqlXjbTools

CARD_NO = "xpath_//android.widget.EditText[@text='请输入您的储蓄卡卡号']"
PHONE_NO = "xpath_//android.widget.EditText[@text='请输入银行预留手机号码']"
GET_VERIFY_CODE = "xpath_//android.widget.Button[@text='获取验证码']"
VERIFY_CODE_INPUT = "xpath_//android.widget.EditText[@text='请输入验证码']"
BINDIND_CARD_CONFIRM = "xpath_//android.widget.Button[@text='下一步']"

class BindingCardDetailPage(PageObject):
    def __init__(self,web_driver,device_id=None):
        super(BindingCardDetailPage,self).__init__(web_driver,device_id)
        self._db = MysqlXjbTools()

    @robot_log
    def verify_page_title(self):
        self.assert_values('绑定银行卡', self.get_text('com.shhxzq.xjb:id/title_actionbar_orange', 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def binding_card(self, bank_card_no, mobile):
        self.perform_actions(
            CARD_NO, bank_card_no,
            PHONE_NO, mobile,
            GET_VERIFY_CODE,
        )

        verification_code = self._db.get_sms_verify_code(mobile=mobile, template_id='cif_bindBankCard')

        self.perform_actions(
            VERIFY_CODE_INPUT, verification_code,
            BINDIND_CARD_CONFIRM
        )

        page = huaxin_ui.ui_ios_xjb_3_0.useroperation_succeed_page.UserOperatinSucceedPage(self.web_driver)

        return page