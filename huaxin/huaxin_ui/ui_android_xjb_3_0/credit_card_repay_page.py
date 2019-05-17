# coding=utf-8
import time
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
from _common.global_config import ASSERT_DICT

from _tools.mysql_xjb_tools import MysqlXjbTools
import huaxin_ui.ui_android_xjb_3_0.setting_trade_password_page
import huaxin_ui.ui_android_xjb_3_0.binding_card_page
import huaxin_ui.ui_android_xjb_3_0.credit_card_repay_detail_page
import huaxin_ui.ui_android_xjb_3_0.add_credit_card_page
import huaxin_ui.ui_android_xjb_3_0.personal_matters_setting_page

CREDIT_CARD = "xpath_//*[contains(@text,%s)]"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"
CREDIT_CARD_DELETE_CONFIRM = "xpath_//android.widget.Button[@text='确认']"

CREDIT_CARD_SELECTED = "xpath_//android.widget.RelativeLayout[@resource-id='com.shhxzq.xjb:id/rl_credit_item']"
# CREDIT_CARD = "xpath_//android.widget.TextView[contains(@text,'%s')]"
REPAY_AMOUNT = "xpath_//android.widget.EditText[@text='请输入还款金额']"
REPAY_CONFIRM = "xpath_//android.widget.Button[@text='确认']"
REPAY_DONE = "xpath_//android.widget.Button[@text='确认']"
REPAYMENT_WARN_SET = "xpath_//android.widget.RelativeLayout[@resource-id='com.shhxzq.xjb:id/ccv_credit_repayment']"
REPAYMENT_WARN_SWITCH = "xpath_//android.widget.ToggleButton[@resource-id='com.shhxzq.xjb:id/repayment_warn_switch']"
REPAYMENT_WARN_DATE = "xpath_//android.view.View[@resource-id='com.shhxzq.xjb:id/lv_filter']"
REPAYMENT_WARN_DATE_COMPELETED = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_compeleted']"

ADD_CREDIT_CARD = "xpath_//android.widget.TextView[@text='添加信用卡']"
ADD_CREDIT_CARD_TIP = "xpath_//android.widget.Button[@text='确定']"
CREDIT_CARD_NO = "xpath_//android.widget.EditText[@text='请输入您的信用卡卡号']"
PHONE_NO = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/bind_card_phonenumber']"
GET_VERIFY_CODE = "xpath_//android.widget.Button[@text='获取验证码']"
INPUT_VERIFY_CODE = "xpath_//android.widget.EditText[@text='请输入验证码']"
ADD_CREDIT_CARD_CONFIRM = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/bind_card_sure_bt']"
ADD_CREDIT_CARD_DONE = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/useroperation_succeed_bt']"
BACK = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left']"

current_page = []


class CreditCardRepayPage(PageObject):
    def __init__(self, web_driver, device_id=None):
        super(CreditCardRepayPage, self).__init__(web_driver, device_id)
        self.elements_exist(*current_page)

    @robot_log
    def verify_page_title(self):
        self.assert_values('信用卡还款', self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def verify_credit_card_repay_details(self, reserved_pay_amount):
        repay_amount_text = self.get_text('com.shhxzq.xjb:id/tv_credit_repayinfo_title', 'find_element_by_id')
        repay_date_text = self.get_text('com.shhxzq.xjb:id/tv_credit_repayinfo_content', 'find_element_by_id')
        repay_amount_actual = filter(lambda ch: ch in '0123456789.', repay_amount_text)
        repay_date_actual = filter(lambda ch: ch in '0123456789.-', repay_date_text)
        repay_date_prefix = ASSERT_DICT['deduction_date'].replace('日', '')
        repay_date_expected = repay_date_prefix.replace('月', '-')

        self.assert_values('预约还款' + '%.2f' % float(reserved_pay_amount), '预约还款' + repay_amount_actual)
        self.assert_values(repay_date_expected, repay_date_actual)

        page = self
        return page

    @robot_log
    def verify_credit_card_repay_reminder_details(self):
        self.assert_values('还款提醒', self.get_text('com.shhxzq.xjb:id/tv_credit_repayinfo_title', 'find_element_by_id'))
        self.assert_values(ASSERT_DICT['repay_day_reminder'],
                           self.get_text('com.shhxzq.xjb:id/tv_credit_repayinfo_content', 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def verify_credit_card_delete_result(self, last_card_no):
        self.assert_values(False, self.element_exist("//*[contains(@text,%s)]" % last_card_no))

        page = self
        return page

    @robot_log
    def verify_credit_card_add_result(self, last_card_no):
        self.assert_values(True, self.element_exist("//*[contains(@text,%s)]" % last_card_no))

        page = self
        return page

    @robot_log
    def go_to_set_trade_password_page(self):
        self.perform_actions(ADD_CREDIT_CARD)

        page = huaxin_ui.ui_android_xjb_3_0.setting_trade_password_page.SettingTradePasswordPage(self.web_driver)
        return page

    @robot_log
    def go_to_binding_bank_card_page(self, device_id):
        self.perform_actions(ADD_CREDIT_CARD,
                             ADD_CREDIT_CARD_TIP)

        page = huaxin_ui.ui_android_xjb_3_0.binding_card_page.BindingCardPage(self.web_driver, device_id=device_id)
        return page

    @robot_log
    def go_to_credit_card_repay_detail_page(self, last_card_no):
        self.perform_actions(CREDIT_CARD % last_card_no)

        page = huaxin_ui.ui_android_xjb_3_0.credit_card_repay_detail_page.CreditCardRepayDetailPage(self.web_driver)
        return page

    @robot_log
    def go_to_add_card_repay_page(self):
        self.perform_actions(ADD_CREDIT_CARD)

        page = huaxin_ui.ui_android_xjb_3_0.add_credit_card_page.AddCreditCardPage(self.web_driver,
                                                                                   device_id=self.device_id)
        return page

    @robot_log
    def back_to_personal_matters_setting_page(self):
        self.perform_actions(BACK)

        page = huaxin_ui.ui_android_xjb_3_0.personal_matters_setting_page.PersonalMattersSettingPage(self.web_driver)
        return page
