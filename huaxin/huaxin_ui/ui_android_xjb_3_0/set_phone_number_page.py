# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
from _tools.mysql_xjb_tools import MysqlXjbTools

import huaxin_ui.ui_android_xjb_3_0.user_operation_succeed_page

MOBILE = "xpath_//android.widget.EditText[@text='请输入11位手机号码']"
MOBILE_GET_VERIFY_CODE = "xpath_//android.widget.Button[@text='获取验证码']"
MOBILE_VERIFY_CODE_INPUT = "xpath_//android.widget.EditText[@text='请输入验证码']"
MOBILE_CONFIRM = "xpath_//android.widget.Button[@text='下一步']"


class SetPhoneNumberPage(PageObject):
    def __init__(self, web_driver, device_id=None):
        super(SetPhoneNumberPage, self).__init__(web_driver, device_id)

    @robot_log
    def verify_page_title(self):
        self.assert_values('设置手机号码', self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def set_phone_number(self, mobile_new):
        self.perform_actions(MOBILE, mobile_new,
                             MOBILE_GET_VERIFY_CODE)

        verify_code = MysqlXjbTools().get_sms_verify_code(mobile=mobile_new, template_id='cif_changeMobile')

        self.perform_actions(
            MOBILE_VERIFY_CODE_INPUT, verify_code,
            MOBILE_CONFIRM
        )
        page = huaxin_ui.ui_android_xjb_3_0.user_operation_succeed_page.UserOperationSucceedPage(
            self.web_driver)
        return page
