# coding: utf-8
import time

from _common.global_config import ASSERT_DICT
from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.tax_dweller_identity_declaration_page

CAPITAL_ACCOUNT = "accId_UIAStaticText_(资金账户)"
NAME = ""
ID_TYPE = ""
ID_NO = ""
SAFETY_LOGOUT = "accId_UIAStaticText_(安全退出)"
ACCOUNT_INFO = "accId_UIAStaticText_(账户信息)"

RISK_EVALUATING = "accId_UIAStaticText_(风险测评)"
ELECTRONIC_SIGN = "accId_UIAStaticText_(电子签名约定书)"
ID_VERIFY = "accId_UIAStaticText_(税收居民身份声明)"

BEGIN_TESTING = "axis_IOS_开始测试"
C_ANSWER_B = "//UIAStaticText[contains(@label, 'B.')]/following-sibling::UIAImage[1]"
R_ANSWER_B = "//UIAStaticText[contains(@label, 'B.')]"
NEXT = "xpathIOS_UIAButton_//UIAButton[@label='下一题']"
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
COMMIT = "xpathIOS_UIAButton_//UIAButton[@label='提交']"
ANSWER_CONFIRM = "xpathIOS_UIAStaticText_//UIAStaticText[@label='确认']"
RE_EVALUATE = "xpathIOS_UIAStaticText_//UIAStaticText[@label='重新测评']"

current_page = []


class AccountInfoPage(PageObject):
    def __init__(self, web_driver):
        super(AccountInfoPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    # flag = 1, 已实名
    # flag = 0, 未实名
    @robot_log
    def risk_evaluating(self, flag=1):
        self.perform_actions(RISK_EVALUATING,
                             BEGIN_TESTING,
                             )

        for i in range(21):
            print '题目%s' % (i + 1)
            if self.element_exist(C_ANSWER_B):
                self.perform_actions("xpathIOS_UIAImage_%s" % C_ANSWER_B,
                                     NEXT)
            else:
                if i != 19 or flag == 0:
                    # 未实名需要选中年龄段
                    self.perform_actions("xpathIOS_UIAStaticText_%s" % R_ANSWER_B)
                elif i == 19 and flag == 1:
                    # 已实名, 直接点下一题
                    self.perform_actions(NEXT)

        time.sleep(1)
        self.perform_actions(COMMIT)

        result = self.get_text("//UIAStaticText[@label='您的投资类型']/following-sibling::UIAStaticText")
        ASSERT_DICT.update({
            "risk_result": result
        })
        self.perform_actions(ANSWER_CONFIRM)

        page = self

        self.assert_values(True, self.element_exist('账户信息', 'find_element_by_accessibility_id'))
        self.assert_values(ASSERT_DICT['risk_result'],
                           self.get_text("//UIAStaticText[@label='风险测评']/following-sibling::UIAStaticText").split('(')[
                               0])

        return page

    @robot_log
    def go_to_identity_declaration_page(self):
        self.perform_actions(ID_VERIFY)

        page = huaxin_ui.ui_ios_xjb_3_0.tax_dweller_identity_declaration_page.TaxDwellerIdentityDeclarationPage(
            self.web_driver)
        return page

    @robot_log
    def view_user_account_information(self, title, content, type='uncertificated'):
        if type == 'uncertificated':
            self.assert_values(True, self.element_exist(
                "//UIAStaticText[@label='%s']/following-sibling::UIAStaticText[@label='%s']" % (title, content)))

        elif type == 'certificated':
            self.assert_values(True, self.element_exist("//android.widget.TextView[@text='%s']" % title))
            self.assert_values(True, self.element_exist(""))
        page = self
        return page
