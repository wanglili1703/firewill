# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log

TITLE_LIST = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/actionbar_text']"
SWIPE_BEGIN = "swipe_xpath_//"
SCROLL = "swipe_xpath_//scroll_2"
CONFIRM = "xpath_//android.widget.TextView[@text='完成']"
FUND_TYPE = "xpath_//android.widget.TextView[@text='%s']"
PERIOD_MONDAY = "xpath_//android.widget.TextView[@text='每周一定投']"
PERIOD_MONTH = "xpath_//android.widget.TextView[@text='每月1号定投']"
# FUND_INCOME_STATUS_1 = "//android.widget.TextView[@text='基金名称']/../following-sibling::android.widget.LinearLayout[1]//android.widget.TextView[3]"
# FUND_INCOME_STATUS_2 = "//android.widget.TextView[@text='基金名称']/../following-sibling::android.widget.LinearLayout[2]//android.widget.TextView[3]"
# FUND_INCOME_STATUS_3 = "//android.widget.TextView[@text='基金名称']/../following-sibling::android.widget.LinearLayout[1]//android.widget.TextView[5]"
# FUND_INCOME_STATUS_4 = "//android.widget.TextView[@text='基金名称']/../following-sibling::android.widget.LinearLayout[2]//android.widget.TextView[5]"
FUND_INCOME_STATUS_1 = "//android.widget.TextView[@text='招商央视财经50指数A']/../following-sibling::android.widget.HorizontalScrollView//android.widget.TextView[1]"
FUND_INCOME_STATUS_2 = "//android.widget.TextView[@text='诺安低碳经济股票']/../following-sibling::android.widget.HorizontalScrollView//android.widget.TextView[1]"
FUND_INCOME_STATUS_3 = "//android.widget.TextView[@text='诺安新经济股票']/../following-sibling::android.widget.HorizontalScrollView/android.widget.LinearLayout/android.widget.LinearLayout/following-sibling::android.widget.LinearLayout[1]//android.widget.TextView[1]"
# FUND_INCOME_STATUS_3 = "//android.widget.TextView[@text='诺安新经济股票']/../following-sibling::android.widget.HorizontalScrollView//android.widget.TextView[3]"
# FUND_INCOME_STATUS_4 = "//android.widget.TextView[@text='招商财经大数据股票']/../following-sibling::android.widget.HorizontalScrollView//android.widget.TextView[3]"
FUND_INCOME_STATUS_4 = "//android.widget.TextView[@text='广发信息技术联接C']/../following-sibling::android.widget.HorizontalScrollView/android.widget.LinearLayout/android.widget.LinearLayout/following-sibling::android.widget.LinearLayout[1]//android.widget.TextView[1]"


class FundPlanRankingPage(PageObject):
    def __init__(self, web_driver):
        super(FundPlanRankingPage, self).__init__(web_driver)

    @robot_log
    def verify_fund_plan_rankings_details(self):
        self.assert_values('近1年', self.get_text('com.shhxzq.xjb:id/actionbar_text', 'find_element_by_id'))
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='全部']"))
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='股票型']"))
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='混合型']"))
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='债券型']"))
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='QDII']"))
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='基金名称']"))
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='每周一定投']"))
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='每月1号定投']"))
        self.assert_values(True,
                           self.element_exist('com.shhxzq.xjb:id/tv_fund_invest_regular_num', 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def view_fund_plan_rankings(self, fund_type):
        self.perform_actions(TITLE_LIST,
                             SWIPE_BEGIN, SCROLL, 'U',
                             CONFIRM)
        self.perform_actions(FUND_TYPE % fund_type,
                             PERIOD_MONDAY)

        eles = self.get_elements_with_same_id(id='com.shhxzq.xjb:id/tv_fund_income_status')
        self.perform_actions(FUND_TYPE % fund_type)
        period_monday_1 = float(eles[0].text.strip("%").encode('utf-8')) / 100
        period_monday_2 = float(eles[2].text.strip("%").encode('utf-8')) / 100
        self.assert_values(True, self.assert_values(period_monday_1, period_monday_2, '>='))

        self.perform_actions(PERIOD_MONTH,
                             PERIOD_MONTH)

        period_month_1 = float(eles[1].text.strip("%").encode('utf-8')) / 100
        period_month_2 = float(eles[3].text.strip("%").encode('utf-8')) / 100

        self.assert_values(period_month_1, period_month_2, '<=')
        fund_type = '混合型'
        self.perform_actions(FUND_TYPE % fund_type)
        self.assert_values(True, self.element_exist("//android.widget.TextView[contains(@text,'共定投')]"))
        fund_type = '债券型'
        self.perform_actions(FUND_TYPE % fund_type)
        self.assert_values(True, self.element_exist("//android.widget.TextView[contains(@text,'共定投')]"))
        fund_type = 'QDII'
        self.perform_actions(FUND_TYPE % fund_type)
        self.assert_values(True, self.element_exist("//android.widget.TextView[contains(@text,'共定投')]"))

        page = self

        return page
