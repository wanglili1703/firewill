# coding: utf-8
from _common.page_object import PageObject

from _common.xjb_decorator import robot_log

import huaxin_ui.ui_ios_xjb_2_0.home_page

MY_REFEREE = "accId_UIAStaticText_我的推荐人"
PHONE_NO = "accId_UIATextField_(textField)请输入11位手机号码"
REFEREE_CONFIRM = "accId_UIAButton_提交"
SAFETY_LOGOUT = "accId_UIAStaticText_安全退出"
SAFETY_LOGOUT_CONFIRM = "axis_IOS_退出[index]1"

RISK_EVALUATING = "accId_UIAStaticText_风险测评"
BEGAIN_TESTING = "axis_IOS_开始测试"
ANSWER_1 = "axis_IOS_B."
ANSWER_2 = "axis_IOS_B."
ANSWER_3 = "axis_IOS_B."
ANSWER_4 = "axis_IOS_B."
ANSWER_5 = "axis_IOS_B."
ANSWER_6 = "axis_IOS_B."
ANSWER_7 = "axis_IOS_B."
ANSWER_8 = "axis_IOS_B."
ANSWER_9 = "axis_IOS_B."
ANSWER_10 = "axis_IOS_B."
ANSWER_11 = "axis_IOS_B."
ANSWER_12 = "axis_IOS_B."
ANSWER_13 = "axis_IOS_A."
ANSWER_14 = "axis_IOS_B."
ANSWER_15 = "axis_IOS_B."
ANSWER_16 = "axis_IOS_B."
ANSWER_17 = "axis_IOS_B."
ANSWER_18 = "axis_IOS_B."
ANSWER_19 = "axis_IOS_B."
ANSWER_20 = "axis_IOS_B."
ANSWER_CONFIRM = "axis_IOS_确定"

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
                             ANSWER_13,
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

    @robot_log
    def logout_app(self):
        self.perform_actions(SAFETY_LOGOUT,
                             SAFETY_LOGOUT_CONFIRM,
                             )

        page = huaxin_ui.ui_ios_xjb_2_0.home_page.HomePage(self.web_driver)

        return page
