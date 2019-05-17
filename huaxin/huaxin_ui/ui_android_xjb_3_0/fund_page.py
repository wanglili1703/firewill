# coding=utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import time
import huaxin_ui.ui_android_xjb_3_0.fund_page_fund_detail
import huaxin_ui.ui_android_xjb_3_0.fund_product_search_page
import huaxin_ui.ui_android_xjb_3_0.fund_selected_page
import huaxin_ui.ui_android_xjb_3_0.fund_page_all_fund_page
import huaxin_ui.ui_android_xjb_3_0.assets_page
import huaxin_ui.ui_android_xjb_3_0.fund_plan_ranking_page
import huaxin_ui.ui_android_xjb_3_0.fund_best_performance_fund_page
import huaxin_ui.ui_android_xjb_3_0.fund_hot_topics_page
import huaxin_ui.ui_android_xjb_3_0.fund_market_index_page
import huaxin_ui.ui_android_xjb_3_0.fund_newly_raised_funds_page

HOME = "xpath_//android.widget.RelativeLayout[1]/android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/tab_image']"
FINANCE = "xpath_//android.widget.RelativeLayout[2]/android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/tab_image']"
ASSETS = "xpath_//android.widget.RelativeLayout[5]/android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/tab_image']"

FUND_PRODUCT_SEARCH = "xpath_//android.widget.TextView[@text='基金代码/简拼/重仓资产']"
FUND_PRODUCT_INPUT = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/cet_search_tile']"
FUND_PRODUCT_NAME = "xpath_//android.widget.TextView[@text='%s%s']"

RESEARCH_REPORT = "xpath_//android.widget.TextView[@text='研究报告']"
INSTITUTION_VIEWPOINT = "xpath_//android.widget.TextView[@text='机构观点']"
TALENT_FUND_DISCUSSION = "xpath_//android.widget.TextView[@text='达人论基']"
MARKET_INDEX = "xpath_//android.widget.TextView[@text='市场指数']"
ALL_FUNDS = "xpath_//android.widget.TextView[@text='全部基金']"
RATING_AND_RANKING = "xpath_//android.widget.TextView[@text='晨星评级']"
SELECTED_FUNDS = "xpath_//android.widget.TextView[@text='自选基金']"
COMPARISION_AND_ANALYSIS = "xpath_//android.widget.TextView[@text='对比分析']"
BEST_FUND = "xpath_//android.widget.TextView[@text='最佳基金']"
EXPERTS_CHANNEL = "xpath_//android.widget.TextView[@text='专家开讲']"
NEW_FUNDS = "xpath_//android.widget.TextView[@text='新发基金']"
TYPICAL_FUNDS = "xpath_//android.widget.TextView[@text='精选基金']"
REPORT_CONTENT = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/fund_channel_title']"
BACK_BUTTON = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left']"
BACK_IMAGEVIEW = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/img_actionbar_left']"
BACK_IMAGEVIEW_1 = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left']"
# FONT_SIZE = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/switch_right_txt']"
FONT_SIZE = "xpath_//android.widget.ToggleButton[@resource-id='com.shhxzq.xjb:id/switch_btn']"
LIST = "xpath_//android.widget.ImageButton[@resource-id='com.shhxzq.xjb:id/ibtn_actionbar_right']"
I_KNOW = "xpath_//android.widget.Button[@text='我知道了'][POP]"

NET_ASSET_VALUE_DESCEND = "xpath_//android.widget.TextView[@text='单位净值']"
NET_ASSET_VALUE_ASCEND = "xpath_//android.widget.TextView[@text='单位净值']"
DAILY_INCREASES_DESCEND = "xpath_//android.widget.TextView[@text='日涨幅']"
DAILY_INCREASES_ASCEND = "xpath_//android.widget.TextView[@text='日涨幅']"
RECENT_ONE_MONTH_DESCEND = "xpath_//android.widget.TextView[@text='近1月']"
RECENT_ONE_MONTH_ASCEND = "xpath_//android.widget.TextView[@text='近1月']"
RECENT_THREE_MONTH_DESCEND = "xpath_//android.widget.TextView[@text='近3月']"
RECENT_THREE_MONTH_ASCEND = "xpath_//android.widget.TextView[@text='近3月']"
RECENT_SIX_MONTH_DESCEND = "xpath_//android.widget.TextView[@text='近6月']"
RECENT_SIX_MONTH_ASCEND = "xpath_//android.widget.TextView[@text='近6月']"
RECENT_ONE_YEAR_DESCEND = "xpath_//android.widget.TextView[@text='近1年']"
RECENT_ONE_YEAR_ASCEND = "xpath_//android.widget.TextView[@text='近1年']"
RECENT_THREE_YEAR_DESCEND = "xpath_//android.widget.TextView[@text='近3年']"
RECENT_THREE_YEAR_ASCEND = "xpath_//android.widget.TextView[@text='近3年']"

SWIPE_BEGIN = "swipe_xpath_//"
FUND_TYPE_SCROLL_1 = "swipe_xpath_//scroll_8"
FUND_TYPE_SCROLL_2 = "swipe_xpath_//scroll_8"

SWIPE_FROM = "swipe_xpath_//axis_0.7"
SWIPE_TO = "swipe_xpath_//axis_0.1"

DATA_SCROLL_1 = "swipe_xpath_//scroll_8"
RANKING_TYPE_SCROLL_1 = "swipe_xpath_//scroll_1"
DOUBLE_RANGE_SLIDER_SWIPE_BEGAIN = "swipe_xpath_//android.view.View[@resource-id='com.shhxzq.xjb:id/doublerangeslider']"

FUND_ALL = "xpath_//android.widget.TextView[@text='全部']"
STOCK_FUNDS = "xpath_//android.widget.TextView[@text='股票型']"
MONETARY_FUNDS = "xpath_//android.widget.TextView[@text='货币型']"
BOND_FUNDS = "xpath_//android.widget.TextView[@text='债券型']"
BLEND_FUNDS = "xpath_//android.widget.TextView[@text='混合型']"
QDII = "xpath_//android.widget.TextView[@text='QDII']"
OTHER_FUNDS = "xpath_//android.widget.TextView[@text='其他']"

CHENXING_RANKING_DESCEND = "xpath_//android.widget.TextView[@text='晨星评级']"
CHENXING_RANKING_ASCEND = "xpath_//android.widget.TextView[@text='晨星评级']"
RANKING_INSTITUTION_TYPE = "xpath_//android.widget.CheckBox[@resource-id='com.shhxzq.xjb:id/dccb_center_titlebar']"
DATA_TYPE = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/all_fund_date_ddv']"
RATING_TYPE = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/all_fund_rating_ddv']"

SELECT_FUNDS_BUTTON = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/iv_fund_fav_empty_add']"
INPUT_FUND_PRODUCT = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/cet_search_tile']"
FUND_PRODUCT_NAME = "xpath_//android.widget.TextView[@text='%s%s']"
SELECT = "xpath_//android.widget.TextView[@text='自选']"
FUND_DETAIL_BACK = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/actionbar_back']"
CANCEL = "xpath_//android.widget.TextView[@text='取消']"
CANCEL_SELECT = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/img_operate_fund']"
ADD_SELECT = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/img_operate_fund']"
# FILTER="xpath_//android.widget.Button[@text='筛选']"
FILTER = "xpath_//android.widget.TextView[@text='筛选']"

FUND_TYPE = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/all_fund_type_ddv']"
SELECT_DONE = "xpath_//android.widget.TextView[@text='完成']"
STAR_RATING = "xpath_//android.view.View[@resource-id='com.shhxzq.xjb:id/ratebar']"
SEARCH_BAR = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/cet_search_tile']"
# MANAGE_SELECTED_FUNDS="xpath_//android.widget.Button[@text='管理']"
MANAGE_SELECTED_FUNDS = "xpath_//android.widget.TextView[@text='管理']"
DELETE_SELECTED_FUNDS = "xpath_//android.widget.TextView[contains(@text,'%s')]/preceding-sibling::android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/iv_fund_fav_del']"

FUND_COMPANY_LIST = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/all_fund_company_ddv']"
SEARCH_FUND_COMPANY = "xpath_//android.widget.TextView[@text='搜索基金公司']"
INPUT_FUND_COMPANY_NAME = "xpath_//android.widget.EditText[@text='搜索基金公司']"
FUND_COMPANY_NAME = "xpath_//android.widget.TextView[@text='%s']"
DELETE_COMFIRM = "xpath_//android.widget.Button[@text='确认删除']"
DELETE_COMPLETE = "xpath_//android.widget.Button[@text='完成']"

COMBINED_SIMULATOR = "xpath_//android.support.v7.widget.LinearLayoutCompat/android.view.View[2]"
ADD_FUND_BUTTON = "xpath_//android.widget.ImageButton[@resource-id='com.shhxzq.xjb:id/ibtn_actionbar_right']"
# SEEKBAR_SWIPE_BEGIN="swipe_xpath_//android.widget.SeekBar[@resource-id='com.shhxzq.xjb:id/two_item_seekBar']"
# SEEKBAR_SCROLL_1="swipe_xpath_//scroll_1"
SEEKBAR_SWIPE_FROM = ""
SEEKBAR_SWIPE = "axis_Android_博时医疗保健行业混合A050026_0.3,0.05"
# SEEKBAR_SWIPE = "axis_Android_华安股票040002_0.3,0.05"
ADD_FUND = "xpath_//android.widget.TextView[contains(@text,'%s')]/following-sibling::android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/img_operate_fund']"
SEARCH = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/search_bar']"
PERMISSION_CLOSE = "xpath_//android.widget.Button[@resource-id='com.android.packageinstaller:id/permission_allow_button'][POP]"
FUND_PLAN_RANKING = "xpath_//android.widget.TextView[@text='定投排行']"
BEST_PERFORMANCE = "xpath_//android.widget.TextView[@text='最佳表现基金']"
HOT_TOPICS = "xpath_//android.widget.TextView[@text='热门主题']"
NEWLY_RAISED_FUND = "xpath_//android.widget.TextView[@text='新发基金']"
NEWLY_RAISED_FUND_STOP = "swipe_xpath_//android.widget.TextView[@text='新发基金']"
INDEX_NAME = "xpath_//android.widget.TextView[contains(@text,'%s')]"

current_page = []


class FundPage(PageObject):
    def __init__(self, web_driver):
        super(FundPage, self).__init__(web_driver)

    # 基金频道--研究报告
    @robot_log
    def fund_research_report(self):
        self.perform_actions(
            RESEARCH_REPORT,
            REPORT_CONTENT,
            # SHARE,
            FONT_SIZE,
            BACK_BUTTON,
            LIST,
            RESEARCH_REPORT,  # 研究报告
            LIST,
            INSTITUTION_VIEWPOINT,  # 机构观点
            BACK_BUTTON,
            LIST,
            TALENT_FUND_DISCUSSION,  # 达人论基
            BACK_BUTTON,
            LIST,
            MARKET_INDEX,  # 市场指数
            BACK_BUTTON,
            LIST,
            ALL_FUNDS,  # 全部基金
            I_KNOW,
            BACK_IMAGEVIEW_1,
            LIST,
            RATING_AND_RANKING,  # 评级排行
            BACK_IMAGEVIEW,
            LIST,
            SELECTED_FUNDS,  # 自选基金
            BACK_IMAGEVIEW_1,
            LIST,
            COMPARISION_AND_ANALYSIS,  # 对比分析
            BACK_BUTTON,
            LIST,
            BEST_FUND,  # 最佳基金
            BACK_IMAGEVIEW,
            LIST,
            EXPERTS_CHANNEL,  # 专家开讲
            BACK_BUTTON,
            LIST,
            NEW_FUNDS,  # 新发基金
            BACK_BUTTON,
            LIST,
            TYPICAL_FUNDS  # 精选基金
        )

    # 基金频道--机构观点
    @robot_log
    def fund_institution_viewpoint(self):
        self.perform_actions(
            INSTITUTION_VIEWPOINT,
            REPORT_CONTENT,
            FONT_SIZE,
            BACK_BUTTON
        )

    # 基金频道--达人论基
    @robot_log
    def fund_talent_fund_discussion(self):
        self.perform_actions(
            TALENT_FUND_DISCUSSION,
            REPORT_CONTENT,
            FONT_SIZE,
            BACK_BUTTON
        )

    # 基金频道--评级排行
    @robot_log
    def fund_rating_and_ranking(self):
        self.perform_actions(RATING_AND_RANKING,
                             CHENXING_RANKING_DESCEND,
                             CHENXING_RANKING_ASCEND,
                             STOCK_FUNDS,
                             # MONETARY_FUNDS,
                             BOND_FUNDS,
                             BLEND_FUNDS,
                             QDII,
                             OTHER_FUNDS,
                             RANKING_INSTITUTION_TYPE,
                             SWIPE_BEGIN, RANKING_TYPE_SCROLL_1, 'U',
                             SELECT_DONE
                             )

    # 基金频道--对比分析
    @robot_log
    def fund_comparasion_and_analysis(self, fund_product_code, fund_product_code_2):
        self.perform_actions(COMPARISION_AND_ANALYSIS,
                             ADD_FUND_BUTTON,
                             FUND_PRODUCT_SEARCH,
                             INPUT_FUND_PRODUCT, fund_product_code,
                             ADD_FUND % fund_product_code,
                             CANCEL,
                             BACK_BUTTON,
                             COMBINED_SIMULATOR,
                             ADD_FUND_BUTTON,
                             FUND_PRODUCT_SEARCH,
                             INPUT_FUND_PRODUCT, fund_product_code,
                             ADD_FUND % fund_product_code,
                             SEARCH_BAR, fund_product_code_2,
                             ADD_FUND % fund_product_code_2,
                             CANCEL,
                             BACK_BUTTON,
                             # SEEKBAR_SWIPE,
                             # ADD_FUND_BUTTON,
                             # CANCEL_SELECT,
                             # CANCEL_SELECT
                             )

    @robot_log
    def go_to_fund_selected_page(self):
        self.perform_actions(SELECTED_FUNDS,
                             I_KNOW)

        page = huaxin_ui.ui_android_xjb_3_0.fund_selected_page.FundSelectedPage(self.web_driver)

        return page

    @robot_log
    def go_to_fund_page_all_fund_page(self):
        self.perform_actions(ALL_FUNDS,
                             I_KNOW)

        page = huaxin_ui.ui_android_xjb_3_0.fund_page_all_fund_page.FundPageAllFundPage(self.web_driver)

        return page

    @robot_log
    def go_to_fund_product_search_page(self):
        self.perform_actions(SEARCH)

        page = huaxin_ui.ui_android_xjb_3_0.fund_product_search_page.FundProductSearchPage(self.web_driver)

        return page

    @robot_log
    def go_to_assets_page(self):
        self.perform_actions(ASSETS)

        page = huaxin_ui.ui_android_xjb_3_0.assets_page.AssetsPage(self.web_driver)
        self.perform_actions(PERMISSION_CLOSE)

        return page

    @robot_log
    def go_to_fund_plan_ranking_page(self):
        self.perform_actions(FUND_PLAN_RANKING)

        page = huaxin_ui.ui_android_xjb_3_0.fund_plan_ranking_page.FundPlanRankingPage(self.web_driver)
        return page

    @robot_log
    def go_to_market_index_page(self, name='市场指数'):
        if name == '市场指数':
            self.perform_actions(MARKET_INDEX)
        else:
            self.perform_actions(INDEX_NAME % name)

        page = huaxin_ui.ui_android_xjb_3_0.fund_market_index_page.FundMarketIndexPage(self.web_driver)
        return page

    @robot_log
    def go_to_best_performance_fund_page(self):
        self.perform_actions(BEST_PERFORMANCE)

        page = huaxin_ui.ui_android_xjb_3_0.fund_best_performance_fund_page.FundBestPerformanceFundPage(self.web_driver)
        return page

    @robot_log
    def go_to_fund_hot_topics_page(self):
        self.perform_actions(HOT_TOPICS)

        page = huaxin_ui.ui_android_xjb_3_0.fund_hot_topics_page.FundHotTopicsPage(self.web_driver)
        return page

    @robot_log
    def verify_newly_raised_fund_details(self):
        self.perform_actions(SWIPE_BEGIN, NEWLY_RAISED_FUND_STOP, 'U')
        self.assert_values('募集中', self.get_text('com.shhxzq.xjb:id/raise_status', 'find_element_by_id'))
        self.assert_values(True, self.element_exist("//android.widget.TextView[contains(@text,'募集结束')]"))

        page = self
        return page

    @robot_log
    def go_to_newly_raised_funds_page(self):
        self.perform_actions(NEWLY_RAISED_FUND)

        page = huaxin_ui.ui_android_xjb_3_0.fund_newly_raised_funds_page.FundNewlyRaisedFundsPage(self.web_driver)
        return page

    @robot_log
    def verify_index_name(self, index_name):
        self.assert_values(True, self.element_exist("//android.widget.TextView[contains(@text,'%s')]" % index_name))

        page = self
        return page
