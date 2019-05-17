# coding=utf-8
from _common.page_object import PageObject

import huaxin_ui.ui_ios_xjb_3_0.fund_page_fund_detail
import huaxin_ui.ui_ios_xjb_3_0.fund_rating_page
from _common.xjb_decorator import robot_log

HOME = "accId_UIAButton_(UITabBarButton_)"
FINANCE = "accId_UIAButton_(UITabBarButton_item_1)"
ASSETS = "accId_UIAButton_(UITabBarButton_item_3)"

FUND_PRODUCT_SEARCH = "axis_IOS_基金代码/简拼/重仓资产"
FUND_PRODUCT_INPUT = "accId_UIASearchBar_基金代码/简拼/重仓资产"
FUND_PRODUCT_NAME_2 = "accId_UIAStaticText_%s%s"
# FUND_PRODUCT_NAME = "axis_IOS_%s[index]1"
FUND_PRODUCT_NAME = "xpathIOS_UIAStaticText_//UIATableCell[@name='(HXSearchOrAddFundTableViewCell)']/UIAStaticText[contains(@name, '%s')]"

RESEARCH_REPORT_CONTENT = "accId_UIAStaticText_(HXResearchReportTableViewCell)"
ORG_REPORT_CONTENT = "accId_UIAStaticText_(HXOrgViewpointViewTableViewCell)"
RESEARCH_REPORT = "accId_UIAStaticText_研究报告"
TALENT_REPORT_CONTENT = "accId_UIAStaticText_(HXIntelligentSayTableViewCell)"
INSTITUTION_VIEWPOINT = "accId_UIAStaticText_机构观点"
TALENT_FUND_DISCUSSION = "accId_UIAStaticText_达人论基"
MARKET_INDEX = "accId_UIAStaticText_市场指数"
ALL_FUNDS = "accId_UIAStaticText_全部基金"
RATING_AND_RANKING = "accId_UIAButton_(UIButton_星级排行)"
RATING_MENU = "accId_UIAStaticText_评级排行"
SELECTED_FUNDS = "accId_UIAStaticText_自选基金"
COMPARISION_AND_ANALYSIS = "accId_UIAStaticText_对比分析"
BEST_FUND = "accId_UIAStaticText_最佳基金"
EXPERTS_CHANNEL = "accId_UIAStaticText_专家开讲"
NEW_FUNDS = "accId_UIAStaticText_新发基金"
TYPICAL_FUNDS = "accId_UIAStaticText_精选基金"
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
CANCEL = "accId_UIAButton_取消"
CANCEL_2 = "axis_IOS_取消"
CANCEL_SELECT = "accId_UIAButton_(clickButton)"
DELETE_SELECT = "accId_UIAButton_delete compare fund"
ADD_SELECT = "accId_UIAButton_add fund icon"
FILTER = "accId_UIAButton_筛选"
FUND_TYPE = "accId_UIAButton_(fontTypeButton)"
STAR_RATING = "accId_UIAElement_(ratingView)"
SEARCH_BAR = "accId_UIASearchBar_基金代码/简拼/重仓资产"

MANAGE_SELECTED_FUNDS = "accId_UIAStaticText_管理"
DELETE_SELECTED_FUNDS = "xpathIOS_UIAButton_/AppiumAUT/UIAApplication/UIAWindow/UIATableView/UIATableCell/UIAButton[contains(@label,%s)]"
DATA_SCROLL_1 = "swipe_accId_scroll_1"
DOUBLE_RANGE_SLIDER_SWIPE_BEGAIN = "swipe_xpath_//android.view.View[@resource-id='com.shhxzq.xjb:id/doublerangeslider']"
FUND_COMPANY_LIST = "accId_UIAButton_全部基金公司"
SEARCH_FUND_COMPANY = "axis_IOS_搜索"
INPUT_FUND_COMPANY_NAME = "accId_UIASearchBar_(searchField)基金公司"
FUND_COMPANY_NAME = "accId_UIAStaticText_%s"
DELETE_COMFIRM = "accId_UIAButton_(UIButton_删除)"
DELETE_COMPLETE = "accId_UIAButton_完成"

COMBINED_SIMULATOR = "accId_UIAButton_组合模拟器"
FUND_COMPARE = "accId_UIAButton_基金对比"
# ADD_FUND_BUTTON="axis_IOS_点击添加"
ADD_FUND_BUTTON = "axis_IOS_华信现金宝"
ADD_BUTTON = "accId_UIAButton_UIBarButtonItemLocationRight"

SEEKBAR_SWIPE = "axis_IOS_对比分析_0,0.6"
ADD_FUND = "axis_IOS_(clickButton)"

DELETE_ICON = "UIButton_delete_fund_icon"

current_page = []


class FundSelectedPage(PageObject):
    def __init__(self, web_driver):
        super(FundSelectedPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_at_fund_selected_page(self):
        self.assert_values(True, self.element_exist("//UIAButton[@label='管理']"))

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
            SELECT_FUNDS_BUTTON,
            I_KNOW,
            FUND_PRODUCT_SEARCH,
            INPUT_FUND_PRODUCT, fund_product_name,
            FUND_PRODUCT_NAME % fund_product_name,
            SELECT,
            FUND_DETAIL_BACK,
            CANCEL,
            BACK_BUTTON,
        )
        self.verify_fund_if_exist(fund_product_name, True)

    @robot_log
    def go_to_fund_detail_page(self, fund_product_name):
        self.perform_actions("accId_UIAStaticText_%s" % fund_product_name)

        page = huaxin_ui.ui_ios_xjb_3_0.fund_page_fund_detail.FundPageFundDetail(self.web_driver)

        return page

    @robot_log
    def verify_fund_if_exist(self, fund_product_name, exist=True):
        # 刷新页面
        self.perform_actions(BACK_BUTTON,
                             SELECTED_FUNDS)

        self.assert_values(exist,
                           self.element_exist("(%s)" % fund_product_name, "find_element_by_accessibility_id"))

        page = self
        return page
