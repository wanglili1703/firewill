# coding=utf-8
import time

from _common.page_object import PageObject

import huaxin_ui.ui_ios_xjb_3_0.fund_page_fund_detail
import huaxin_ui.ui_ios_xjb_3_0.fund_rating_page
import huaxin_ui.ui_ios_xjb_3_0.fund_selected_page
import huaxin_ui.ui_ios_xjb_3_0.fund_compare_combination_page
import huaxin_ui.ui_ios_xjb_3_0.fund_info_page
import huaxin_ui.ui_ios_xjb_3_0.fund_invest_ranking_page
import huaxin_ui.ui_ios_xjb_3_0.product_detail_page
import huaxin_ui.ui_ios_xjb_3_0.fund_topics_page
import huaxin_ui.ui_ios_xjb_3_0.fund_estimated_value_ranking_page
import huaxin_ui.ui_ios_xjb_3_0.fund_best_performance_page
import huaxin_ui.ui_ios_xjb_3_0.fund_newly_raised_funds_page
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
# RESEARCH_REPORT = "accId_UIAStaticText_研究报告"
NEWS = "accId_UIAStaticText_要闻"
TALENT_REPORT_CONTENT = "accId_UIAStaticText_(HXIntelligentSayTableViewCell)"
INSTITUTION_VIEWPOINT = "accId_UIAStaticText_机构观点"
TALENT_FUND_DISCUSSION = "accId_UIAStaticText_达人论基"
MARKET_INDEX = "accId_UIAStaticText_市场指数[POP]"
SH_INDEX = "xpathIOS_UIAStaticText_//UIAStaticText[contains(@label, '上证指数')][POP]"
INFO = "accId_UIAStaticText_资讯"
ALL_FUNDS = "accId_UIAStaticText_全部基金"
RATING_AND_RANKING = "accId_UIAButton_(UIButton_星级排行)"
FUND_INVEST_RANKING = "accId_UIAButton_(UIButton_定投排行)"
RATING_MENU = "accId_UIAStaticText_评级排行"
SELECTED_FUNDS = "accId_UIAStaticText_自选基金"
COMPARISION_AND_ANALYSIS = "accId_UIAStaticText_对比分析"
BEST_FUND = "accId_UIAStaticText_最佳表现基金"
EXPERTS_CHANNEL = "accId_UIAStaticText_专家开讲"
NEW_FUNDS = "accId_UIAStaticText_新发基金"
TYPICAL_FUNDS = "accId_UIAStaticText_精选基金"
FUND_TOPICS = "accId_UIAStaticText_基金主题"
ESTIMATED_VALUE_RANKING = "accId_UIAStaticText_估值排行"
BACK_BUTTON = "accId_UIAButton_UIBarButtonItemLocationLeft"
# BACK_IMAGEVIEW = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/img_actionbar_left']"
# FONT_SIZE = "axis_IOS_navShare_-0.06,0"
# FONT_SIZE = "axis_IOS_(UIButton_nav_font_bigger)"
LIST = "accId_UIAButton_(UIButton_)"
I_KNOW = "accId_UIAButton_我知道了[POP]"

# INDEX_START="swipe_accId_市场指数"
# INDEX_STOP = "swipe_accId_%s"
# CSI_INDEX = "xpath_//android.widget.TextView[@text='%s']"
CSI_INDEX = "axis_IOS_市场指数_0,0.25"

FUND_ALL = "accId_UIAButton_全部"
STOCK_FUNDS = "accId_UIAButton_股票型"
MONETARY_FUNDS = "accId_UIAButton_货币型[POP]"
BOND_FUNDS = "accId_UIAButton_债券型"
BLEND_FUNDS = "accId_UIAButton_混合型"
QDII = "accId_UIAButton_QDII"
OTHER_FUNDS = "accId_UIAButton_其他"

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
RANKING_TYPE_SCROLL_1 = "swipe_accId_scroll_1"
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
NEWLY_RAISED_FUND = "accId_UIAStaticText_新发基金"

current_page = []


class FundPage(PageObject):
    def __init__(self, web_driver):
        super(FundPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_at_fund_page(self):
        self.assert_values('基金名称', self.get_text("(基金名称)", "find_element_by_accessibility_id"))

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
    def fund_search(self, product_name):
        self.perform_actions(
            FUND_PRODUCT_SEARCH,
            FUND_PRODUCT_INPUT, product_name,
            FUND_PRODUCT_NAME % product_name,
        )

        page = huaxin_ui.ui_ios_xjb_3_0.product_detail_page.ProductDetailPage(self.web_driver)

        return page

    @robot_log
    def cancel_search(self):
        self.perform_actions(CANCEL)

        page = self
        return page

    @robot_log
    def go_to_fund_detail_page(self, fund_product_name, fund_product_code):
        page = self.fund_product_search(product_name=fund_product_name)
        # self.perform_actions(
        #     FUND_PRODUCT_NAME_2 % (fund_product_name, fund_product_code),
        # )
        return page

    # 基金频道--研究报告
    @robot_log
    def go_to_fund_info_page(self):
        self.perform_actions(
            INFO,
        )
        page = huaxin_ui.ui_ios_xjb_3_0.fund_info_page.FundInfoPage(self.web_driver)

        return page

    # 基金频道--机构观点
    @robot_log
    def fund_institution_viewpoint(self):
        self.perform_actions(
            RATING_AND_RANKING,
            LIST,
            INSTITUTION_VIEWPOINT
        )

        self.assert_values("机构观点", self.get_text("//UIAStaticText[@label='机构观点']"))
        self.perform_actions(
            ORG_REPORT_CONTENT,
        )

        page = self

        return page

    # 基金频道--达人论基
    @robot_log
    def fund_talent_fund_discussion(self):
        self.perform_actions(
            RATING_AND_RANKING,
            LIST,
            TALENT_FUND_DISCUSSION
        )

        self.assert_values("达人论基", self.get_text("//UIAStaticText[@label='达人论基']"))

        self.perform_actions(
            TALENT_REPORT_CONTENT,
        )

    # 基金频道--市场指数
    @robot_log
    def fund_market_index(self, csi_index):
        self.perform_actions(
            # MARKET_INDEX,
            SH_INDEX
        )

        self.assert_values(True, self.element_exist("(综合指数)", "find_element_by_accessibility_id"))
        self.perform_actions(
            CSI_INDEX
        )

        page = self

        return page

    # 基金频道--全部基金
    @robot_log
    def fund_all_funds(self):
        self.perform_actions(ALL_FUNDS,
                             I_KNOW,
                             FUND_ALL,
                             NET_ASSET_VALUE_DESCEND,
                             NET_ASSET_VALUE_ASCEND,
                             DAILY_INCREASES_DESCEND,
                             DAILY_INCREASES_ASCEND,
                             RECENT_ONE_MONTH_DESCEND,
                             RECENT_ONE_MONTH_ASCEND,
                             SWIPE_BEGAIN, FUND_TYPE_SCROLL_1, 'L',
                             # RECENT_THREE_MONTH_DESCEND,
                             # RECENT_THREE_MONTH_ASCEND,
                             # RECENT_SIX_MONTH_DESCEND,
                             # RECENT_SIX_MONTH_ASCEND,
                             # RECENT_ONE_YEAR_DESCEND,
                             # RECENT_ONE_YEAR_ASCEND,
                             # RECENT_THREE_YEAR_DESCEND,
                             # RECENT_THREE_YEAR_ASCEND,
                             # STOCK_FUNDS,
                             # MONETARY_FUNDS,
                             # BOND_FUNDS,
                             # BLEND_FUNDS,
                             # QDII,
                             # OTHER_FUNDS
                             )

    # 基金频道--评级排行
    @robot_log
    def go_to_fund_rating_page(self):
        self.perform_actions(RATING_AND_RANKING)

        page = huaxin_ui.ui_ios_xjb_3_0.fund_rating_page.FundRatingPage(self.web_driver)

        return page

    # 定投排行页面
    @robot_log
    def go_to_fund_invest_ranking_page(self):
        self.perform_actions(FUND_INVEST_RANKING)

        page = huaxin_ui.ui_ios_xjb_3_0.fund_invest_ranking_page.FundInvestRankingPage(self.web_driver)
        return page

    # 进入基金自选页面
    @robot_log
    def go_to_fund_selected_page(self):
        self.perform_actions(SELECTED_FUNDS)

        page = huaxin_ui.ui_ios_xjb_3_0.fund_selected_page.FundSelectedPage(self.web_driver)
        time.sleep(1)

        page.verify_at_fund_selected_page()

        return page

    # 进入基金对比分析页面
    @robot_log
    def go_to_fund_compare_and_combination_page(self):
        self.perform_actions(COMPARISION_AND_ANALYSIS)

        page = huaxin_ui.ui_ios_xjb_3_0.fund_compare_combination_page.FundCompareCombinationPage(self.web_driver)

        page.verify_at_fund_compare_combination_page()

        return page

    # 基金频道--对比分析
    @robot_log
    def fund_comparison_and_analysis(self, fund_product_code, fund_product_code_2):
        self.perform_actions(COMPARISION_AND_ANALYSIS,
                             ADD_FUND_BUTTON,
                             FUND_PRODUCT_SEARCH,
                             INPUT_FUND_PRODUCT, fund_product_code,
                             ADD_FUND,
                             CANCEL,
                             BACK_BUTTON,
                             COMBINED_SIMULATOR,
                             ADD_FUND_BUTTON,
                             FUND_PRODUCT_SEARCH,
                             INPUT_FUND_PRODUCT, fund_product_code,
                             ADD_FUND,
                             SEARCH_BAR, fund_product_code_2,
                             ADD_FUND,
                             CANCEL,
                             BACK_BUTTON,
                             # SEEKBAR_SWIPE,
                             ADD_BUTTON,
                             DELETE_SELECT,
                             DELETE_SELECT,
                             BACK_BUTTON,
                             FUND_COMPARE,
                             ADD_BUTTON,
                             DELETE_SELECT,
                             )

    @robot_log
    def go_to_fund_topics_page(self):
        self.perform_actions(FUND_TOPICS)

        page = huaxin_ui.ui_ios_xjb_3_0.fund_topics_page.FundTopicPage(self.web_driver)
        return page

    @robot_log
    def go_to_fund_estimated_value_ranking_page(self):
        self.perform_actions(ESTIMATED_VALUE_RANKING)

        page = huaxin_ui.ui_ios_xjb_3_0.fund_estimated_value_ranking_page.FundEstimatedValueRankingPage(self.web_driver)
        return page

    @robot_log
    def go_to_fund_best_performance_page(self):
        self.perform_actions(BEST_FUND)

        page = huaxin_ui.ui_ios_xjb_3_0.fund_best_performance_page.FundBestPerformancePage(self.web_driver)
        return page

    @robot_log
    def go_to_newly_raised_funds_page(self, product_name):
        self.perform_actions("swipe_accId_//", "swipe_accId_%s" % product_name, 'U')
        self.perform_actions(NEWLY_RAISED_FUND)

        page = huaxin_ui.ui_ios_xjb_3_0.fund_newly_raised_funds_page.FundNewlyRaisedFundsPage(self.web_driver)
        return page
