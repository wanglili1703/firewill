# coding: utf-8
import random

import huaxin_ui
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.fund_page
import huaxin_ui.ui_ios_xjb_3_0.product_detail_page

LEFT_BUTTON = "accId_UIAButton_UIBarButtonItemLocationLeft"
SWIPE_BEGIN = "swipe_xpath_//"
TIME_SCROLL_1 = "swipe_accId_scroll_1"
FUND_TYPE_ALL = "accId_UIAButton_(UIButton_全部)"
FUND_TYPE_STOCK = "accId_UIAButton_(UIButton_股票型)"
FUND_TYPE_MIXED = "accId_UIAButton_(UIButton_混合型)"
FUND_TYPE_BOND = "accId_UIAButton_(UIButton_债券型)"
FUND_TYPE_QDII = "accId_UIAButton_(UIButton_QDII)"

WEEK_SORT = "accId_UIAButton_(UIButton_每周一定投order_type_none.png)"
DATE_SORT = "accId_UIAButton_(UIButton_每月1号定投order_type_desc.png)"
TIME = "(UIButton_近1年icon_arrowfold)"
FINISH = "accId_UIAButton_完成"
FUND_INDEX = "xpathIOS_UIAStaticText_//UIATableView/UIATableCell[%s]/UIAStaticText[1]"

current_page = []


class FundInvestRankingPage(PageObject):
    def __init__(self, web_driver):
        super(FundInvestRankingPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def go_back_to_fund_page(self):
        self.perform_actions(LEFT_BUTTON)

        page = huaxin_ui.ui_ios_xjb_3_0.fund_page.FundPage(self.web_driver)
        return page

    @robot_log
    def verify_at_fund_invest_ranking_page(self):
        self.assert_values(True, self.element_exist("(UIButton_全部)", "find_element_by_accessibility_id"))
        self.assert_values('基金名称/代码', self.get_text("(基金名称/代码)", "find_element_by_accessibility_id"))

    @robot_log
    def click_different_fund_type(self):
        # 默认显示近1年
        self.assert_values("近1年", self.get_text(TIME, "find_element_by_accessibility_id"))

        self.perform_actions(FUND_TYPE_ALL,
                             FUND_TYPE_STOCK,
                             FUND_TYPE_MIXED,
                             FUND_TYPE_BOND,
                             FUND_TYPE_QDII)

        # 点击页面上的排序
        self.perform_actions(WEEK_SORT,
                             WEEK_SORT,
                             WEEK_SORT,
                             )
        self.verify_at_fund_invest_ranking_page()

        self.perform_actions(DATE_SORT,
                             DATE_SORT,
                             DATE_SORT,
                             )
        self.verify_at_fund_invest_ranking_page()

        # 滑动时间
        self.perform_actions("accId_UIAButton_%s" % TIME,
                             SWIPE_BEGIN, TIME_SCROLL_1, 'U',
                             FINISH)

        self.assert_values("近2年", self.get_text(TIME, "find_element_by_accessibility_id"))

        page = self
        return page

    # 随机进入一个基金详情页面
    @robot_log
    def go_to_fund_details_page(self):
        index = random.randint(1, 5)
        self.perform_actions(FUND_INDEX % index)

        page = huaxin_ui.ui_ios_xjb_3_0.product_detail_page.ProductDetailPage(self.web_driver)
        return page
