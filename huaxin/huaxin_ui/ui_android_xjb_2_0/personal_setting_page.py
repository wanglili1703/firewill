# coding: utf-8
from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
from huaxin_ui.ui_android_xjb_2_0.security_center_page import SecurityCenterPage

MY_REFEREE = "xpath_//android.widget.TextView[@text='我的推荐人']"
PHONE_NO = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/et_inviter_mobile']"
REFEREE_CONFIRM = "xpath_//android.widget.Button[@text='确定']"

RISK_EVALUATING = "xpath_//android.widget.TextView[@text='风险测评']"
BEGAIN_TESTING = "xpath_//android.widget.Button[@content-desc='开始测试']"
ANSWER_1 = "xpath_//*[contains(@content-desc,'B')]"
ANSWER_2 = "xpath_//*[contains(@content-desc,'B')]"
ANSWER_3 = "xpath_//*[contains(@content-desc,'B')]"
ANSWER_4 = "xpath_//*[contains(@content-desc,'B')]"
ANSWER_5 = "xpath_//*[contains(@content-desc,'B')]"
ANSWER_6 = "xpath_//*[contains(@content-desc,'B')]"
ANSWER_7 = "xpath_//*[contains(@content-desc,'B')]"
ANSWER_8 = "xpath_//*[contains(@content-desc,'B')]"
ANSWER_9 = "xpath_//*[contains(@content-desc,'B')]"
ANSWER_10 = "xpath_//*[contains(@content-desc,'B')]"
ANSWER_11 = "xpath_//*[contains(@content-desc,'B')]"
ANSWER_12 = "xpath_//*[contains(@content-desc,'B')]"
ANSWER_13 = "xpath_//*[contains(@content-desc,'A')]"
ANSWER_14 = "xpath_//*[contains(@content-desc,'B')]"
ANSWER_15 = "xpath_//*[contains(@content-desc,'B')]"
ANSWER_16 = "xpath_//*[contains(@content-desc,'B')]"
ANSWER_17 = "xpath_//*[contains(@content-desc,'B')]"
ANSWER_18 = "xpath_//*[contains(@content-desc,'B')]"
ANSWER_19 = "xpath_//*[contains(@content-desc,'B')]"
ANSWER_20 = "xpath_//*[contains(@content-desc,'B')]"
ANSWER_CONFIRM = "xpath_//android.widget.Button[@content-desc='确定']"

current_page = []


class PersonalSettingPage(PageObject):
    def __init__(self, web_driver):
        super(PersonalSettingPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def my_referee(self, phone_no):
        self.perform_actions(MY_REFEREE,
                             PHONE_NO, phone_no,
                             REFEREE_CONFIRM,
                             )

        page = self

        return page

    @robot_log
    def risk_evaluating(self):
        self.perform_actions(RISK_EVALUATING,
                             BEGAIN_TESTING,
                             ANSWER_1,
                             ANSWER_2,
                             ANSWER_3,
                             ANSWER_4,
                             ANSWER_5,
                             ANSWER_6,
                             ANSWER_7,
                             ANSWER_8,
                             ANSWER_9,
                             ANSWER_10,
                             ANSWER_11,
                             ANSWER_12,
                             )

        self.click_screen(x=0.5,y=0.5,try_time=1)

        self.perform_actions(
                             ANSWER_14,
                             ANSWER_15,
                             ANSWER_16,
                             ANSWER_17,
                             ANSWER_18,
                             ANSWER_19,
                             ANSWER_20,
                             ANSWER_CONFIRM,
                             )

        page = self

        return page
