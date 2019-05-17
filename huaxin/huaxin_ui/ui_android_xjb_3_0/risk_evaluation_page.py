# coding=utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
from _common.global_config import ASSERT_DICT
import time
import huaxin_ui.ui_android_xjb_3_0.personal_setting_page
import huaxin_ui.ui_android_xjb_3_0.user_account_information_page

BEGAIN_TESTING = "xpath_//android.view.View[@content-desc='%s']"
# ANSWER_1_A = "xpath_//*[contains(@content-desc,'B')]"
# ANSWER_1_D = "xpath_//*[contains(@content-desc,'D')]"
# ANSWER_2 = "xpath_//*[contains(@content-desc,'B')]"
# ANSWER_3 = "xpath_//*[contains(@content-desc,'B')]"
# ANSWER_4 = "xpath_//*[contains(@content-desc,'B')]"
# ANSWER_5 = "xpath_//*[contains(@content-desc,'B')]"
# ANSWER_6 = "xpath_//*[contains(@content-desc,'B')]"
# ANSWER_7 = "xpath_//*[contains(@content-desc,'B')]"
# ANSWER_8 = "xpath_//*[contains(@content-desc,'B')]"
# ANSWER_9 = "xpath_//*[contains(@content-desc,'B')]"
# ANSWER_10 = "xpath_//*[contains(@content-desc,'B')]"
# ANSWER_11 = "xpath_//*[contains(@content-desc,'B')]"
# ANSWER_12 = "xpath_//*[contains(@content-desc,'B')]"
# ANSWER_13 = "xpath_//*[contains(@content-desc,'A')]"
# ANSWER_14 = "xpath_//*[contains(@content-desc,'B')]"
# ANSWER_15 = "xpath_//*[contains(@content-desc,'D')]"
# ANSWER_16 = "xpath_//*[contains(@content-desc,'B')]"
# ANSWER_17 = "xpath_//*[contains(@content-desc,'5人以上')]"
# ANSWER_18 = "xpath_//*[contains(@content-desc,'B')]"
# ANSWER_19 = "xpath_//*[contains(@content-desc,'B')]"
# ANSWER_20 = "xpath_//*[contains(@content-desc,'B')]"
# ANSWER_21 = "xpath_//*[contains(@content-desc,'D')]"
NEXT = "xpath_//android.widget.Button[@content-desc='下一题']"
SUBMIT = "xpath_//android.widget.Button[@content-desc='提交']"
ANSWER_CONFIRM = "xpath_//android.view.View[@content-desc='确认']"
REEVALUATION = "xpath_//android.view.View[@content-desc='重新测评']"
ANSWER = "xpath_//*[contains(@content-desc,'%s')]"


class RiskEvaluationPage(PageObject):
    def __init__(self, web_driver):
        super(RiskEvaluationPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self, title='风险承受能力测试'):
        self.assert_values(title, self.get_text(self.page_title, 'find_element_by_id'))
        page = self

        return page

    @robot_log
    def risk_evaluating(self, test='开始测试'):
        self.perform_actions(BEGAIN_TESTING % test)
        answer_cautious = (
            'B', 'D', 'A', 'B', 'A', 'B', 'C', 'E', 'D', 'A', 'D', 'A', 'D', 'D', 'A', 'C', 'E', 'B', 'D', 'B', 'E',
            'A')
        answer_moderate = (
            'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'C', 'A', 'B', 'D', 'B', 'E',
            'A')

        if ASSERT_DICT['risk_type'] == '谨慎型' or ASSERT_DICT['risk_type'] == '未测评':
            for i in range(0, 22):
                time.sleep(2)
                self.perform_actions(ANSWER % answer_moderate[i])

                if i == 1:
                    self.perform_actions(NEXT)
        elif ASSERT_DICT['risk_type'] == '稳健型':
            for i in range(0, 22):
                time.sleep(2)
                self.perform_actions(ANSWER % answer_cautious[i])

                if i == 1:
                    self.perform_actions(NEXT)

        # self.perform_actions(ANSWER_1_A)
        # self.perform_actions(ANSWER_1_D)
        # self.perform_actions(NEXT)
        # time.sleep(2)
        # self.perform_actions(ANSWER_2)
        # time.sleep(2)
        # self.perform_actions(ANSWER_3)
        # time.sleep(2)
        # self.perform_actions(ANSWER_4)
        # time.sleep(2)
        # self.perform_actions(ANSWER_5)
        # time.sleep(2)
        # self.perform_actions(ANSWER_6)
        # time.sleep(2)
        # self.perform_actions(ANSWER_7)
        # time.sleep(2)
        # self.perform_actions(ANSWER_8)
        # time.sleep(2)
        # self.perform_actions(ANSWER_9)
        # time.sleep(2)
        # self.perform_actions(ANSWER_10)
        # time.sleep(2)
        # self.perform_actions(ANSWER_11)
        # time.sleep(2)
        # self.perform_actions(ANSWER_12)
        # time.sleep(2)
        # self.perform_actions(ANSWER_13)
        # time.sleep(2)
        #
        # self.perform_actions(ANSWER_14)
        # time.sleep(2)
        # self.perform_actions(ANSWER_15)
        # # self.click_screen(x=0.5, y=0.5, try_time=1)
        # time.sleep(2)
        # self.perform_actions(ANSWER_16)
        # time.sleep(2)
        # self.perform_actions(ANSWER_17)
        # time.sleep(2)
        # self.perform_actions(ANSWER_18)
        # time.sleep(2)
        # self.perform_actions(ANSWER_19)
        # time.sleep(2)
        # self.perform_actions(ANSWER_20)
        # # self.perform_actions(NEXT)
        # time.sleep(2)
        # self.perform_actions(ANSWER_21)

        self.perform_actions(SUBMIT)

        self.assert_values(True, self.element_exist("//android.view.View[@content-desc='您的投资类型']"))
        risk_type = self.get_attribute(
            "//android.view.View[@content-desc='您的投资类型']/following-sibling::android.view.View[1]")

        self.assert_values(True, self.assert_values(ASSERT_DICT['risk_type'], risk_type, '!='))
        ASSERT_DICT.update({'risk_type': risk_type})

        self.perform_actions(ANSWER_CONFIRM)

        page = huaxin_ui.ui_android_xjb_3_0.user_account_information_page.UserAccountInformationPage(self.web_driver)
        time.sleep(2)
        return page
