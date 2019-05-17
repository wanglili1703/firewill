# coding=utf-8
import time

from _common.page_object import PageObject

import huaxin_ui.ui_ios_xjb_3_0.fund_page_fund_detail
import huaxin_ui.ui_ios_xjb_3_0.fund_rating_page
from _common.xjb_decorator import robot_log

HOME = "accId_UIAButton_(UITabBarButton_)"
FINANCE = "accId_UIAButton_(UITabBarButton_item_1)"
ASSETS = "accId_UIAButton_(UITabBarButton_item_3)"

CANCEL = "accId_UIAButton_取消"
FUND_PRODUCT_SEARCH = "axis_IOS_基金代码/简拼/重仓资产"
FUND_PRODUCT_INPUT = "accId_UIASearchBar_基金代码/简拼/重仓资产"
FUND_PRODUCT_NAME_2 = "accId_UIAStaticText_%s%s"
FUND_PRODUCT_NAME = "xpathIOS_UIAStaticText_//UIATableCell[@name='(HXSearchOrAddFundTableViewCell)']/UIAStaticText[contains(@name, '%s')]"

RESEARCH_REPORT_CONTENT = "accId_UIAStaticText_(HXResearchReportTableViewCell)"
ORG_REPORT_CONTENT = "accId_UIAStaticText_(HXOrgViewpointViewTableViewCell)"
BACK_BUTTON = "accId_UIAButton_UIBarButtonItemLocationLeft"
LIST = "accId_UIAButton_(UIButton_)"
I_KNOW = "accId_UIAButton_我知道了[POP]"

NET_ASSET_VALUE_DESCEND = "accId_UIAButton_单位净值"
NET_ASSET_VALUE_ASCEND = "accId_UIAButton_单位净值"
DAILY_INCREASES_DESCEND = "accId_UIAButton_日涨幅"
DAILY_INCREASES_ASCEND = "accId_UIAButton_日涨幅"
RECENT_ONE_MONTH_DESCEND = "accId_UIAButton_近一月"
RECENT_ONE_MONTH_ASCEND = "accId_UIAButton_近一月"
RECENT_THREE_MONTH_DESCEND = "accId_UIAButton_近3月"
RECENT_THREE_MONTH_ASCEND = "accId_UIAButton_近3月"
RECENT_SIX_MONTH_DESCEND = "accId_UIAButton_近6月"
RECENT_SIX_MONTH_ASCEND = "accId_UIAButton_近6月"
RECENT_ONE_YEAR_DESCEND = "accId_UIAButton_近1年"
RECENT_ONE_YEAR_ASCEND = "accId_UIAButton_近1年"
RECENT_THREE_YEAR_DESCEND = "accId_UIAButton_近3年"
RECENT_THREE_YEAR_ASCEND = "accId_UIAButton_近3年"

FIRST_SWIPE_START = "swipe_accId_日涨幅"
FIRST_SWIPE_STOP = "swipe_accId_近3月"
SECOND_SWIPE_START = "swipe_accId_近6月"
SECOND_SWIPE_STOP = "swipe_accId_近3年"
SWIPE_BEGAIN = "swipe_xpath_//"
FUND_TYPE_SCROLL_1 = "swipe_accId_scroll_1"
FUND_TYPE_SCROLL_2 = "swipe_accId_scroll_1"

CHENXING_RANKING_DESCEND = "accId_UIAButton_晨星评级"
CHENXING_RANKING_ASCEND = "accId_UIAButton_晨星评级"
RANKING_INSTITUTION_TYPE = "accId_UIAButton_(UIButton_晨星评级icon_arrowfold)"
DATA_TYPE = "accId_UIAButton_(timeSectionButton)"
RATING_TYPE = "accId_UIAButton_(ratingButton)"
RANKING_TYPE_SCROLL_1 = "swipe_accId_scroll_5"
SELECT_DONE = "accId_UIAButton_完成"

SELECT_FUNDS_BUTTON = "accId_UIAButton_(UIButton_fund_compare_add)"
INPUT_FUND_PRODUCT = "accId_UIASearchBar_基金代码/简拼/重仓资产"
SELECT = "accId_UIAButton_自选"
FUND_DETAIL_BACK = "accId_UIAButton_UIBarButtonItemLocationLeft"
BACK_BUTTONCANCEL = "accId_UIAButton_取消"
CANCEL_2 = "axis_IOS_取消"
CANCEL_SELECT = "accId_UIAButton_(clickButton)"
DELETE_SELECT = "accId_UIAButton_delete compare fund"
ADD_SELECT = "accId_UIAButton_add fund icon"
FILTER = "accId_UIAButton_筛选"
FUND_TYPE = "accId_UIAButton_(fontTypeButton)"
STAR_RATING = "accId_UIAElement_(ratingView)"
SEARCH_BAR = "accId_UIASearchBar_基金代码/简拼/重仓资产"

MANAGE_SELECTED_FUNDS = "accId_UIAStaticText_管理"

COMBINED_SIMULATOR = "accId_UIAButton_组合模拟器"
FUND_COMPARE = "accId_UIAButton_基金对比"
# ADD_FUND_BUTTON="axis_IOS_点击添加"
ADD_FUND_BUTTON = "axis_IOS_华信现金宝"
ADD_BUTTON = "accId_UIAButton_UIBarButtonItemLocationRight"

SEEKBAR_SWIPE = "axis_IOS_对比分析_0,0.6"
ADD_FUND = "accId_UIAButton_(UIButton_add_fund_icon)"

DELETE_ICON = "UIButton_delete_fund_icon"

current_page = []


class FundCompareCombinationPage(PageObject):
    def __init__(self, web_driver):
        super(FundCompareCombinationPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_at_fund_compare_combination_page(self):
        self.assert_values("对比分析", self.get_text("//UIAStaticText[@label='对比分析']"))

        page = self

        return page

    @robot_log
    def fund_product_search(self, product_name):
        self.perform_actions(
            FUND_PRODUCT_SEARCH,
            FUND_PRODUCT_INPUT, product_name,
            FUND_PRODUCT_NAME % product_name,
        )

        page = huaxin_ui.ui_ios_xjb_3_0.fund_page_fund_detail.FundPageFundDetail(self.web_driver)

        return page

    @robot_log
    def go_to_fund_detail_page(self, fund_product_name, fund_product_code):
        page = self.fund_product_search(product_name=fund_product_name)
        return page

    # 基金频道--自选基金
    @robot_log
    def fund_selected_funds(self, fund_product_name, fund_company):
        self.perform_actions(

        )

    # 组合对比
    @robot_log
    def fund_compare_and_analysis(self, fund_product_code, fund_product_code_2):
        self.perform_actions(ADD_BUTTON)
        if self.element_exist("(已选基金)", "find_element_by_accessibility_id"):
            while self.element_exist("delete compare fund", "find_element_by_accessibility_id"):
                self.perform_actions(DELETE_SELECT)
        self.perform_actions(
            # ADD_FUND_BUTTON,
            FUND_PRODUCT_SEARCH,
            INPUT_FUND_PRODUCT, fund_product_code,
            ADD_FUND,
            CANCEL,
            BACK_BUTTON,
        )

        # self.assert_values(True, self.element_exist("//UIAStaticText[contains(@label, %s)]" % fund_product_code))
        self.perform_actions(COMBINED_SIMULATOR)

        self.perform_actions(ADD_BUTTON)
        if self.element_exist("(已选基金)", "find_element_by_accessibility_id"):
            while self.element_exist("delete compare fund", "find_element_by_accessibility_id"):
                self.perform_actions(DELETE_SELECT)
        self.perform_actions(
            # ADD_FUND_BUTTON,
            FUND_PRODUCT_SEARCH,
            INPUT_FUND_PRODUCT, fund_product_code,
            ADD_FUND)

        time.sleep(1)
        self.perform_actions(
            SEARCH_BAR, fund_product_code_2,
            ADD_FUND,
            CANCEL,
            BACK_BUTTON,
        )
        # self.assert_values(True, self.element_exist("//UIAStaticText[contains(@label, %s)]" % fund_product_code))
        # self.assert_values(True, self.element_exist("//UIAStaticText[contains(@label, %s)]" % fund_product_code_2))

        self.perform_actions(
            ADD_BUTTON,
            DELETE_SELECT,
            DELETE_SELECT,
            BACK_BUTTON,
        )
        # self.assert_values(False, self.element_exist("//UIAStaticText[contains(@label, %s)]" % fund_product_code))
        # self.assert_values(False, self.element_exist("//UIAStaticText[contains(@label, %s)]" % fund_product_code_2))

        self.perform_actions(
            FUND_COMPARE,
            ADD_BUTTON,
            DELETE_SELECT,
            BACK_BUTTON
        )
        # self.assert_values(False, self.element_exist("//UIAStaticText[contains(@label, %s)]" % fund_product_code))

    @robot_log
    def go_to_fund_detail_page(self, fund_product_name):
        self.perform_actions("accId_UIAStaticText_%s" % fund_product_name)

        page = huaxin_ui.ui_ios_xjb_3_0.fund_page_fund_detail.FundPageFundDetail(self.web_driver)

        return page
