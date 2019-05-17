# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log

import huaxin_ui.ui_android_xjb_3_0.tax_dweller_identity_declaration_page
import huaxin_ui.ui_android_xjb_3_0.personal_setting_page
import huaxin_ui.ui_android_xjb_3_0.risk_evaluation_page
from _common.global_config import ASSERT_DICT

IDENTITY_DECLARATION = "xpath_//android.widget.TextView[@text='税收居民身份声明']"
BACK = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left']"
RISK_EVALUATING = "xpath_//android.widget.TextView[@text='风险测评']"
RISK_RESULT = "//android.widget.TextView[@text='风险测评']/following-sibling::android.widget.LinearLayout[1]/android.widget.TextView"


class UserAccountInformationPage(PageObject):
    def __init__(self, web_driver):
        super(UserAccountInformationPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('账户信息', self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def go_to_identity_declaration_page(self):
        self.perform_actions(IDENTITY_DECLARATION)
        page = huaxin_ui.ui_android_xjb_3_0.tax_dweller_identity_declaration_page.TaxDwellerIdentityDeclarationPage(
            self.web_driver)
        return page

    @robot_log
    def view_user_account_information(self, title, content, type='uncertificated'):
        if type == 'uncertificated':
            self.assert_values(True, self.element_exist("//android.widget.TextView[@text='%s']" % title))
            self.assert_values(content, self.get_text(
                "//android.widget.TextView[@text='%s']/following-sibling::android.widget.LinearLayout[1]/android.widget.TextView" % title))
        elif type == 'certificated':
            self.assert_values(True, self.element_exist("//android.widget.TextView[@text='%s']" % title))
            self.assert_values(True, self.element_exist(
                "//android.widget.TextView[@text='%s']/following-sibling::android.widget.LinearLayout[1]/android.widget.TextView[contains(@text,'%s')]" % (
                    title, content)))
        page = self
        return page

    @robot_log
    def back_to_personal_setting_page(self):
        self.perform_actions(BACK)

        page = huaxin_ui.ui_android_xjb_3_0.personal_setting_page.PersonalSettingPage(self.web_driver)
        return page

    @robot_log
    def verify_risk_evaluation_status(self):
        status = self.get_text(
            "//android.widget.TextView[@text='风险测评']/following-sibling::android.widget.LinearLayout[1]/android.widget.TextView")

        self.assert_values('未测评', status)
        ASSERT_DICT.update({'risk_type': '未测评'})

        page = self
        return page

    @robot_log
    def go_to_risk_evaluation_page(self):
        self.perform_actions(RISK_EVALUATING)
        page = huaxin_ui.ui_android_xjb_3_0.risk_evaluation_page.RiskEvaluationPage(self.web_driver)

        return page

    @robot_log
    def verify_risk_evaluation_result(self, risk_type=None):
        risk_result = self.get_text(RISK_RESULT).split('(')[0]

        if risk_type is not None:
            self.assert_values(risk_type, risk_result)
        ASSERT_DICT.update({'risk_type': risk_result})

        page = self
        return page
