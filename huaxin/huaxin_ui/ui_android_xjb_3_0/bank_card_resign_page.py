# coding=utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.user_operation_succeed_page
from _tools.mysql_xjb_tools import MysqlXjbTools

GET_VERIFY_CODE = "xpath_//android.widget.Button[@text='获取验证码']"
VERIFY_CODE_INPUT = "xpath_//android.widget.EditText[@text='请输入验证码']"
NEXT = "xpath_//android.widget.Button[@text='下一步']"


class BankCardResignPage(PageObject):
    def __init__(self, web_driver):
        super(BankCardResignPage, self).__init__(web_driver)
        self._db = MysqlXjbTools()

    @robot_log
    def verify_page_title(self, last_no):
        self.assert_values('尾号' + last_no + '银行卡重新签约',
                           self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def resign(self, mobile):
        self.assert_values(mobile,
                           self.get_text('com.shhxzq.xjb:id/component_cet_mobile', 'find_element_by_id').replace(" ",
                                                                                                                 ""))
        self.perform_actions(GET_VERIFY_CODE)
        verification_code = self._db.get_sms_verify_code(mobile=mobile, template_id='cif_bindBankCard')
        self.perform_actions(VERIFY_CODE_INPUT, verification_code,
                             NEXT)

        page = huaxin_ui.ui_android_xjb_3_0.user_operation_succeed_page.UserOperationSucceedPage(self.web_driver)
        return page
