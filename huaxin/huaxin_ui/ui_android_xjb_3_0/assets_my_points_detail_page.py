# coding: utf-8
import time

from _common.page_object import PageObject

from _common.xjb_decorator import robot_log, user_info_close_afterwards

import huaxin_ui.ui_android_xjb_3_0.fund_page_fund_detail
import huaxin_ui.ui_android_xjb_3_0.finance_high_end_page

EARN_POINTS = "xpath_//android.widget.TextView[@text='赚积分']"
SPEND_POINTS = "xpath_//android.widget.TextView[@text='花积分']"
BUY_FUND = "xpath_//android.widget.TextView[@text='去购买']"
USER_INFO = "xpath_//android.widget.Button[@text='我知道了']"

RECOMMEND = "xpath_//android.widget.TextView[@text='去推荐']"

BUY_FUND_SPEND_POINTS = "xpath_//android.widget.TextView[@text='基金']/following-sibling::android.widget.TextView[2][@text='去购买']"
BUY_VIPPRODUCT_SPEND_POINTS = "xpath_//android.widget.TextView[@text='高端理财']/following-sibling::android.widget.TextView[2][@text='去购买']"
BUY_DQB_SPEND_POINTS = "xpath_//android.widget.TextView[@text='定活宝']/following-sibling::android.widget.TextView[2][@text='去购买']"

SEARCH_FUND = "xpath_//android.widget.TextView[@text='基金代码/简拼/重仓资产']"
INPUT_FUND_PRODUCT = "xpath_//android.widget.EditText[@text='基金代码/简拼/重仓资产']"
FUND_PRODUCT_NAME = "xpath_//android.widget.TextView[@text='%s%s']"

SEARCH_RESULT = "xpath_//*[contains(@text,'%s')]"
POINT_DETAILS="xpath_//android.widget.Button[@text='积分明细']"
TYPES_LISTS="xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/header_points_traderecord']"
TYPES_ALL="xpath_//android.widget.CheckedTextView[@text='全部']"
TYPES_INCOME="xpath_//android.widget.CheckedTextView[@text='收入']"
TYPES_PAYMENT="xpath_//android.widget.CheckedTextView[@text='支出']"

FUND_SELECTED="xpath_//android.widget.TextView[@text='%s%s']"

current_page = []


class AssetsMyPointsDetailPage(PageObject):
    def __init__(self, web_driver):
        super(AssetsMyPointsDetailPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def earn_points_by_buy_fund(self, fund_product_name, fund_product_code):
        time.sleep(3)

        self.perform_actions(
            EARN_POINTS,
            BUY_FUND,
            USER_INFO,
            SEARCH_FUND,
            INPUT_FUND_PRODUCT, fund_product_name,
            FUND_SELECTED % (fund_product_name, fund_product_code),
        )

        page = huaxin_ui.ui_android_xjb_3_0.fund_page_fund_detail.FundPageFundDetail(self.web_driver)

        return page

    # 赚积分--推荐用户注册并绑卡
    @robot_log
    def earn_points_by_recommend_user_register(self):
        time.sleep(3)

        self.perform_actions(
            EARN_POINTS,
            RECOMMEND
        )

    # 花积分--买基金
    @robot_log
    def spend_points_by_buy_fund(self, fund_product_name, fund_product_code):
        time.sleep(3)

        self.perform_actions(SPEND_POINTS,
                             BUY_FUND_SPEND_POINTS,
                             USER_INFO,
                             SEARCH_FUND,
                             INPUT_FUND_PRODUCT, fund_product_name,
                             FUND_PRODUCT_NAME % (fund_product_name, fund_product_code),
                             )

        page = huaxin_ui.ui_android_xjb_3_0.fund_page_fund_detail.FundPageFundDetail(self.web_driver)

        return page

    # 花积分--买高端
    @robot_log
    def spend_points_by_buy_vipproduct_use_product_name(self):
        time.sleep(3)

        self.perform_actions(SPEND_POINTS,
                             BUY_VIPPRODUCT_SPEND_POINTS, )

        page = huaxin_ui.ui_android_xjb_3_0.finance_high_end_page.FinanceHighEndPage(self.web_driver)

        return page

    # 花积分--买定期宝
    def spend_points_by_buy_dqb(self):
        time.sleep(3)

        self.perform_actions(SPEND_POINTS,
                             BUY_DQB_SPEND_POINTS)

        page=huaxin_ui.ui_android_xjb_3_0.finance_dqb_page.FinanceDqbPage(self.web_driver)

        return  page

    # 积分明细
    @robot_log
    def my_points_details(self):
        time.sleep(3)

        self.perform_actions(POINT_DETAILS,
                             TYPES_LISTS,
                             TYPES_ALL,
                             TYPES_LISTS,
                             TYPES_INCOME,
                             TYPES_LISTS,
                             TYPES_PAYMENT
                            )

        page=self

        return page