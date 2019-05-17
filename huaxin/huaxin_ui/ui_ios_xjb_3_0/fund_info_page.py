# coding=utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log

EXPERT_TOPIC_CONTENT = "//UIAStaticText[contains(@label, '专题')]"
ORG_REPORT_CONTENT = "accId_UIAStaticText_(HXOrgViewpointViewTableViewCell)"
NEWS = "accId_UIAButton_要闻"
EXPERT_TOPIC = "accId_UIAButton_专题"
MONEY_TOPIC = "accId_UIAButton_理财"
QUICK_TOPIC = "accId_UIAButton_快讯"
VIP_TOPIC = "accId_UIAButton_VIP[POP]"

BACK_BUTTON = "accId_UIAButton_UIBarButtonItemLocationLeft"

current_page = []


class FundInfoPage(PageObject):
    def __init__(self, web_driver):
        super(FundInfoPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_at_fund_info_page(self):
        self.assert_values('资讯', self.get_text("//UIAStaticText[@label='资讯']"))

    # 基金频道--
    @robot_log
    def fund_info(self):
        self.perform_actions(
            NEWS,
        )
        self.assert_values(True, self.element_exist("//UIAWebView/UIAStaticText"))
        self.verify_at_fund_info_page()

        self.perform_actions(
            EXPERT_TOPIC,
        )
        self.assert_values(True, self.element_exist(EXPERT_TOPIC_CONTENT))

        self.verify_at_fund_info_page()

        self.perform_actions(
            MONEY_TOPIC
        )
        self.assert_values(True, self.element_exist("//UIAWebView/UIAStaticText"))
        self.verify_at_fund_info_page()

        self.perform_actions(
            QUICK_TOPIC
        )
        # self.assert_values('今天', self.get_text("//UIAStaticText[@label='今天']"))
        self.verify_at_fund_info_page()

        self.perform_actions(
            VIP_TOPIC
        )
        self.verify_at_fund_info_page()
        self.assert_values(True, self.element_exist("//UIAImage"))

        page = self

        return page
