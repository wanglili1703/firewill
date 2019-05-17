# coding: utf-8
import time

from _common.page_object import PageObject

from _common.xjb_decorator import robot_log, user_info_close_afterwards

import huaxin_ui.ui_ios_xjb_2_0.fund_page_fund_detail
import huaxin_ui.ui_ios_xjb_2_0.finance_high_end_page
import huaxin_ui.ui_ios_xjb_2_0.finance_dqb_page

EARN_POINTS = "accId_UIAButton_赚积分"
RECOMMEND = "accId_UIAButton_去推荐"
SPEND_POINTS = "accId_UIAButton_花积分"
BUY_FUND = "accId_UIAButton_去购买"
USER_INFO = "accId_UIAButton_(UIButton_我知道了)[POP]"
SEARCH_FUND = "axis_IOS_基金代码/简拼/重仓资产"
INPUT_FUND_PRODUCT = "accId_UIASearchBar_(searchField)基金代码/简拼/重仓资产"
FUND_PRODUCT_NAME = "accId_UIAStaticText_%s%s"
DQB_PRODUCT_NAME = "accId_UIAStaticText_%s"

SEARCH_DQB = "accId_UIAButton_UIBarButtonItemLocationRight"
INPUT_DQB_PRODUCT = "accId_UIASearchBar_(searchField)产品名称/简拼"

BUY_DQB_SPEND_POINTS = "axis_IOS_去购买"
BUY_FUND_SPEND_POINTS = "axis_IOS_去购买[index]1"
BUY_VIPPRODUCT_SPEND_POINTS = "axis_IOS_去购买[index]2"

POINT_DETAILS = "accId_UIAButton_积分明细"
TYPES_LISTS = "accId_UIAButton_(titleView)"
POINT_STATUS_DONE = "accId_UIAButton_完成"
POINT_TYPE_SCROLL_1 = "swipe_accId_scroll_1"
POINT_TYPE_SCROLL_2 = "swipe_accId_scroll_1"

current_page = []


class AssetsMyPointsDetailPage(PageObject):
    def __init__(self, web_driver):
        super(AssetsMyPointsDetailPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def earn_points_by_buy_fund(self, fund_product_name, fund_product_code):
        self.perform_actions(
            EARN_POINTS,
            BUY_FUND,
            USER_INFO,
            SEARCH_FUND,
            INPUT_FUND_PRODUCT, fund_product_name,
            FUND_PRODUCT_NAME % (fund_product_name, fund_product_code),
        )

        page = huaxin_ui.ui_ios_xjb_2_0.fund_page_fund_detail.FundPageFundDetail(self.web_driver)

        return page

    # 赚积分--推荐用户注册并绑卡
    @robot_log
    def earn_points_by_recommend_user_register(self):
        self.perform_actions(
            EARN_POINTS,
            RECOMMEND
        )

    # 花积分--买定期宝
    @robot_log
    def spend_points_by_buy_dqb(self, dqb_product_name):
        self.perform_actions(SPEND_POINTS,
                             BUY_DQB_SPEND_POINTS,
                             USER_INFO,
                             SEARCH_DQB,
                             INPUT_DQB_PRODUCT, dqb_product_name,
                             DQB_PRODUCT_NAME % dqb_product_name,
                             )

        page = huaxin_ui.ui_ios_xjb_2_0.finance_dqb_page.FinanceDqbPage(self.web_driver)

        return page

    # 花积分--买基金
    @robot_log
    def spend_points_by_buy_fund(self, fund_product_name, fund_product_code):
        self.perform_actions(SPEND_POINTS,
                             BUY_FUND_SPEND_POINTS,
                             USER_INFO,
                             SEARCH_FUND,
                             INPUT_FUND_PRODUCT, fund_product_name,
                             FUND_PRODUCT_NAME % (fund_product_name, fund_product_code),
                             )

        page = huaxin_ui.ui_ios_xjb_2_0.fund_page_fund_detail.FundPageFundDetail(self.web_driver)

        return page

    # 花积分--买高端
    @robot_log
    def spend_points_by_buy_vipproduct_use_product_name(self):
        self.perform_actions(SPEND_POINTS,
                             BUY_VIPPRODUCT_SPEND_POINTS, )

        page = huaxin_ui.ui_ios_xjb_2_0.finance_high_end_page.FinanceHighEndPage(self.web_driver)

        return page

    # 积分明细
    @robot_log
    def my_points_details(self):
        self.perform_actions(POINT_DETAILS,
                             TYPES_LISTS,
                             POINT_STATUS_DONE,
                             TYPES_LISTS,
                             'swipe_xpath_//', POINT_TYPE_SCROLL_1, 'U',
                             POINT_STATUS_DONE,
                             TYPES_LISTS,
                             'swipe_xpath_//', POINT_TYPE_SCROLL_2, 'U',
                             POINT_STATUS_DONE,
                             )

        page = self

        return page
