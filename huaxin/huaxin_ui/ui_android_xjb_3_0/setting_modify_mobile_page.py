# coding: utf-8
import time
from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
from _tools.mysql_xjb_tools import MysqlXjbTools
import huaxin_ui.ui_android_xjb_3_0.login_page
import huaxin_ui.ui_android_xjb_3_0.upload_materials_page

TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/tradepwd_et']"
TRADE_PASSWORD_CONFIRM = "xpath_//android.widget.Button[@text='确认']"

RECEIVE_SMS = "xpath_//android.widget.TextView[@text='能接收短信']"
NOT_RECEIVE_SMS = "xpath_//android.widget.TextView[contains(@text,'审核需要')]/preceding-sibling::android.widget.TextView[@text='修改绑定手机']"

GET_VERIFY_CODE = "xpath_//android.widget.Button[@text='获取验证码']"
TRADE_PASSWORD_VERIFY_CODE_INPUT = "xpath_//android.widget.EditText[@text='请输入验证码']"
VERIFY_CODE_CONFIRM = "xpath_//android.widget.Button[@text='下一步']"

MOBILE = "xpath_//android.widget.EditText[@text='请输入11位手机号码']"
MOBILE_GET_VERIFY_CODE = "xpath_//android.widget.Button[@text='获取验证码']"
MOBILE_VERIFY_CODE_INPUT = "xpath_//android.widget.EditText[@text='请输入验证码']"
MOBILE_CONFIRM = "xpath_//android.widget.Button[@text='下一步']"

MODIFY_MOBILE_DONE = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/useroperation_succeed_bt']"

current_page = []


class SettingModifyMobilePage(PageObject):
    def __init__(self, web_driver, device_id):
        super(SettingModifyMobilePage, self).__init__(web_driver, device_id)
        self.elements_exist(*current_page)
        self._db = MysqlXjbTools()

    @robot_log
    def verify_page_title(self):
        self.assert_values('修改绑定手机', self.get_text(self.page_title, 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def modify_mobile(self, mobile_old, trade_password, mobile_new):
        self.perform_actions(
            TRADE_PASSWORD, trade_password,
            TRADE_PASSWORD_CONFIRM,
            RECEIVE_SMS,
            GET_VERIFY_CODE,
        )

        verify_code = self._db.get_sms_verify_code(mobile=mobile_old, template_id='cif_changeMobile')

        self.perform_actions(
            TRADE_PASSWORD_VERIFY_CODE_INPUT, verify_code,
            VERIFY_CODE_CONFIRM,
            MOBILE, mobile_new,
            MOBILE_GET_VERIFY_CODE,
        )

        verify_code = MysqlXjbTools().get_sms_verify_code(mobile=mobile_new, template_id='cif_changeMobile')

        self.perform_actions(
            MOBILE_VERIFY_CODE_INPUT, verify_code,
            MOBILE_CONFIRM,
            MODIFY_MOBILE_DONE,
        )

        page = huaxin_ui.ui_android_xjb_3_0.login_page.LoginPage(self.web_driver)

        return page

    @robot_log
    def modify_mobile_without_sms(self, mobile_old, trade_password, mobile_new):
        self.perform_actions(
            TRADE_PASSWORD, trade_password,
            TRADE_PASSWORD_CONFIRM,
            RECEIVE_SMS,
            GET_VERIFY_CODE,
        )

        verify_code = self._db.get_sms_verify_code(mobile=mobile_old, template_id='cif_changeMobile')

        self.perform_actions(
            TRADE_PASSWORD_VERIFY_CODE_INPUT, verify_code,
            VERIFY_CODE_CONFIRM,
            MOBILE, mobile_new,
            MOBILE_GET_VERIFY_CODE,
        )

        verify_code = MysqlXjbTools().get_sms_verify_code(mobile=mobile_new, template_id='cif_changeMobile')

        self.perform_actions(
            MOBILE_VERIFY_CODE_INPUT, verify_code,
            MOBILE_CONFIRM,
            MODIFY_MOBILE_DONE,
        )

        page = huaxin_ui.ui_android_xjb_3_0.login_page.LoginPage(self.web_driver)

        return page

    @robot_log
    def go_to_upload_materials_page(self, device_id=None):
        self.perform_actions(NOT_RECEIVE_SMS)
        # time.sleep(2)
        # self.assert_values('华信现金宝', self.get_text('com.shhxzq.xjb:id/title_actionbar', 'find_element_by_id'))
        #
        # self.click_screen(x=0.5, y=0.757)

        page = huaxin_ui.ui_android_xjb_3_0.upload_materials_page.UploadMaterialsPage(self.web_driver, device_id)

        return page
