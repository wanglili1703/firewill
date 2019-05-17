# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
from _tools.mysql_xjb_tools import MysqlXjbTools
import huaxin_ui.ui_android_xjb_3_0.binding_card_detail_page
import huaxin_ui.ui_android_xjb_3_0.setting_trade_password_page
import huaxin_ui.ui_android_xjb_3_0.my_bank_card_page
from _common.global_config import ASSERT_DICT

SWIPE_START = "swipe_xpath_//android.widget.TextView[@text='银行卡管理']"
SWIPE_STOP = "swipe_xpath_//android.widget.TextView[@text='绑定银行卡']"
SWIPE_STOP_CONFIRM = "xpath_//android.widget.TextView[@text='绑定银行卡']"

CARD_NO = "xpath_//android.widget.EditText[@text='请输入您的储蓄卡卡号']"
PHONE_NO = "xpath_//android.widget.EditText[@text='请输入银行预留手机号码']"
GET_VERIFY_CODE = "xpath_//android.widget.Button[@text='获取验证码']"
VERIFY_CODE_INPUT = "xpath_//android.widget.EditText[@text='请输入验证码']"
BINDIND_CARD_CONFIRM = "xpath_//android.widget.Button[@text='下一步']"

BINDIND_CARD_DONE = "xpath_//android.widget.Button[@text='确认']"

BANK_CARD_LAST_CARD_NO = "xpath_//*[contains(@text,'%s')]"
BANK_CARD_DELETE_CONFIRM = "xpath_//android.widget.Button[@text='确认']"
BINDING_CARD = "xpath_//android.widget.TextView[@text='绑定银行卡']"
BANK_NAME = "//android.widget.TextView[contains(@text,'%s')]/preceding-sibling::android.widget.TextView[2][@resource-id='com.shhxzq.xjb:id/bankNm']"

current_page = []


class BankCardManagementPage(PageObject):
    def __init__(self, web_driver, device_id=None):
        super(BankCardManagementPage, self).__init__(web_driver, device_id)
        self.elements_exist(*current_page)
        self._db = MysqlXjbTools()

    @robot_log
    def verify_page_title(self):
        self.assert_values('银行卡管理', self.get_text(self.page_title, 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def verify_bank_card_details(self, bank_name, last_card_no=None):
        last_card_no_text = self.get_text('com.shhxzq.xjb:id/bankAcc', 'find_element_by_id')
        last_card_no_actual = filter(lambda ch: ch in '0123456789.', last_card_no_text)
        if last_card_no is None:
            self.assert_values(ASSERT_DICT['last_card_no'], last_card_no_actual)
        else:
            # self.assert_values(last_card_no, last_card_no_actual)
            self.assert_values(True,
                               self.element_exist("//android.widget.TextView[contains(@text,'%s')]" % last_card_no))
        # self.assert_values(bank_name, self.get_text(
        #     "//android.widget.TextView[contains(@text,'%s')]/preceding-sibling::android.widget.TextView[2]" % last_card_no_actual))
        self.assert_values(True, self.element_exist(BANK_NAME % last_card_no))
        self.assert_values('储蓄卡', self.get_text(
            "//android.widget.TextView[contains(@text,'%s')]/preceding-sibling::android.widget.TextView[1]" % last_card_no_actual))

        page = self

        return page

    # @robot_log
    # def binding_card(self, band_card_no, phone_number):
    #     self.perform_actions(
    #         SWIPE_START, SWIPE_STOP, 'U',
    #         SWIPE_STOP_CONFIRM,
    #         CARD_NO, band_card_no,
    #         PHONE_NO, phone_number,
    #         GET_VERIFY_CODE,
    #     )
    #
    #     verification_code = self._db.get_sms_verify_code(mobile=phone_number, template_id='cif_bindBankCard')
    #
    #     self.perform_actions(
    #         VERIFY_CODE_INPUT, verification_code,
    #         BINDIND_CARD_CONFIRM,
    #         BINDIND_CARD_DONE,
    #     )
    #
    #     page = self
    #
    #     return page

    @robot_log
    def go_to_binding_card_detail_page(self, device_id=None):
        self.perform_actions(SWIPE_STOP_CONFIRM)

        page = huaxin_ui.ui_android_xjb_3_0.binding_card_detail_page.BindingCardDetailPage(self.web_driver, device_id)

        return page

    @robot_log
    def go_to_set_trade_password_page(self):
        self.perform_actions(BINDING_CARD)

        page = huaxin_ui.ui_android_xjb_3_0.setting_trade_password_page.SettingTradePasswordPage(self.web_driver)

        return page

    @robot_log
    def go_to_my_bank_card_page(self, last_card_no):
        self.perform_actions(BANK_CARD_LAST_CARD_NO % last_card_no)

        page = huaxin_ui.ui_android_xjb_3_0.my_bank_card_page.MyBankCardPage(self.web_driver)

        return page

    @robot_log
    def verify_bank_card_existence(self, last_card_no):
        self.assert_values('False',
                           str(self.element_exist("//android.widget.TextView[contains(@text,'%s')]" % last_card_no)))
        self.assert_values('True', str(self.element_exist("//android.widget.TextView[@text='去绑卡,开启极致理财']")))
        self.assert_values('True', str(self.element_exist("//android.widget.TextView[@text='绑定银行卡']")))

        page = self

        return page
