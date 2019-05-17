# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log, user_info_close_afterwards
from huaxin_ui.ui_android_xjb_3_0.fund_more_product_page import FundMoreProductPage
import huaxin_ui.ui_android_xjb_3_0.trade_detail_page
import huaxin_ui.ui_android_xjb_3_0.my_fund_plan_page
from _common.global_config import ASSERT_DICT
import huaxin_ui.ui_android_xjb_3_0.start_fund_plan_page
import huaxin_ui.ui_android_xjb_3_0.assets_analysis_page
import huaxin_ui.ui_android_xjb_3_0.fund_assets_structure_page
import huaxin_ui.ui_android_xjb_3_0.description_page
import huaxin_ui.ui_android_xjb_3_0.fund_supplementary_purchase_page
import huaxin_ui.ui_android_xjb_3_0.fund_redeem_page
import huaxin_ui.ui_android_xjb_3_0.history_holding_page
import time

TRADE_DETAIL = "xpath_//android.widget.Button[@text='交易记录']"
FUND_MORE_PRODUCT = "xpath_//android.widget.Button[@text='查看更多产品']"
FUND_MORE_PRODUCT_STOP = "swipe_xpath_//android.widget.Button[@text='查看更多产品']"
REDEEM = "xpath_//android.widget.Button[@text='卖出']"
REDEEM_AMOUNT = "xpath_//android.widget.EditText[@text='输入份额']"
REDEEM_CONFIRM = "xpath_//android.widget.Button[@text='确认']"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"
REDEEM_DONE = "xpath_//android.widget.Button[@text='确认']"

TITLE_START = "swipe_xpath_//"
FUND_PRODUCT_STOP = "swipe_xpath_//*[contains(@text,'%s')]"
FUND_PRODUCT = "xpath_//*[contains(@text,'%s')]"
# FUND_PRODUCT = "xpath_//android.widget.TextView[contains(@text,'%s')]/../../following-sibling::android.widget.LinearLayout[1]//android.widget.TextView[@text='持有金额']"
NORMAL_REDEEM = "xpath_//android.widget.RadioButton[@resource-id='com.shhxzq.xjb:id/rbtn_redeem_normal_select']"
FAST_REDEEM = "xpath_//android.widget.RadioButton[@resource-id='com.shhxzq.xjb:id/rbtn_redeem_faster_select']"
TRADE_RECORDS = "xpath_//android.widget.TextView[@text='交易记录']"
MY_FUND_PLAN = "xpath_//android.widget.Button[@text='我的定投计划']"
MY_FUND_PLAN_STOP = "swipe_xpath_//android.widget.Button[@text='我的定投计划']"
BACK = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left_orange']"
FUND_TOTAL = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_fund_total']"
SHOW_TIPS = "axis_Android_基金总资产_0.12,0"
FUND_STOP = "swipe_xpath_//android.widget.TextView[@text='购买确认中']/preceding-sibling::android.widget.TextView[contains(@text,'%s')]"
# FUND_REDEEM_STOP = "swipe_xpath_//android.widget.TextView[@text='持有金额']/../../preceding-sibling::android.widget.LinearLayout[1]/android.widget.TextView[contains(@text,'%s')]"
FUND_REDEEM_STOP = "swipe_xpath_//android.widget.TextView[@text='持有金额']/../../../../preceding-sibling::android.widget.LinearLayout[1]/android.widget.TextView[contains(@text,'%s')]"
FUND = "xpath_//android.widget.TextView[@text='购买确认中']/preceding-sibling::android.widget.TextView[contains(@text,'%s')]"
# FUND_REDEEM = "xpath_//android.widget.TextView[@text='持有金额']/../../preceding-sibling::android.widget.LinearLayout[1]/android.widget.TextView[contains(@text,'%s')]"
FUND_REDEEM = "xpath_//android.widget.TextView[@text='持有金额']/../../../../preceding-sibling::android.widget.LinearLayout[1]/android.widget.TextView[contains(@text,'%s')]"
HOLDING_AMOUNT = "//android.widget.TextView[contains(@text,'%s')]/../following-sibling::android.widget.LinearLayout[1]/android.widget.LinearLayout/android.widget.TextView[@text='持有金额']"
HISTORY_HOLDING_BUTTON = "xpath_//android.widget.TextView[@text='历史持仓']"
HISTORY_HOLDING_STOP = "swipe_xpath_//android.widget.TextView[@text='%s']"
HISTORY_HOLDING = "xpath_//android.widget.TextView[@text='%s']"

current_page = []


class AssetsFundDetailPage(PageObject):
    def __init__(self, web_driver):
        super(AssetsFundDetailPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_page_title(self):
        self.assert_values('基金', self.get_text('com.shhxzq.xjb:id/title_actionbar_orange', 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def go_to_trade_detail_page(self):
        self.perform_actions(TRADE_DETAIL)
        page = huaxin_ui.ui_android_xjb_3_0.trade_detail_page.TradeDetailPage(self.web_driver)
        return page

    @robot_log
    @user_info_close_afterwards
    def go_to_fund_more_product_page(self):
        self.perform_actions(TITLE_START, FUND_MORE_PRODUCT_STOP, 'U')
        self.perform_actions(FUND_MORE_PRODUCT)

        page = FundMoreProductPage(self.web_driver)

        return page

    #
    # @robot_log
    # def redeem_fund_product(self, fund_product, amount, trade_password):
    #     self.perform_actions(
    #         TITLE_START, FUND_PRODUCT_STOP % fund_product, 'U',
    #                      FUND_PRODUCT % fund_product)
    #
    #     # redeem_available=self.perform_actions("getV_Android_com.shhxzq.xjb:id/content[@text_]")
    #     # redeem_available=self.perform_actions("getV_Android_android.widget.TextView[@text_]")
    #
    #
    #     # trade_num=self.perform_actions("getV_Android_com.shhxzq.xjb:id/content[@text_]")
    #     self.perform_actions(REDEEM)
    #
    #     redeem_max = self.get_text('com.shhxzq.xjb:id/fund_redeem_max', 'find_element_by_id')
    #     redeem_max = '%.2f' % float(filter(lambda ch: ch in '0123456789.', str(redeem_max)))
    #     self.perform_actions(REDEEM_AMOUNT, amount,
    #                          REDEEM_CONFIRM,
    #                          )
    #
    #     if float(amount) >= 1 and float(amount) <= float(redeem_max):
    #         self.perform_actions(
    #             TRADE_PASSWORD, trade_password)
    #
    #         self.assert_values('完成', self.get_text(self.page_title, 'find_element_by_id'))
    #
    #         self.perform_actions(REDEEM_DONE)
    #
    #         redeem_available = float(redeem_max) - float(amount)
    #         # self.perform_actions(
    #         #     TITLE_START, FUND_PRODUCT_STOP % fund_product, 'U',
    #         #                  FUND_PRODUCT % fund_product)
    #
    #         # redeem_available_actual = self.get_text(
    #         #     "//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/title']/./following-sibling::android.widget.LinearLayout[1]/android.widget.TextView")
    #         # self.assert_values('%.2f' % float(redeem_available), str(redeem_available_actual))
    #
    #         self.perform_actions(TRADE_RECORDS)
    #         redeem_amt_actual = str(self.get_text('com.shhxzq.xjb:id/trade_amount', 'find_element_by_id'))
    #         redeem_amt_actual = '%.2f' % float(filter(lambda ch: ch in '0123456789.', redeem_amt_actual))
    #         self.assert_values('%.2f' % float(amount), redeem_amt_actual)
    #
    #     else:
    #         self.assert_values('卖出', str(self.get_text(self.page_title, 'find_element_by_id')))
    #
    #     page = self
    #
    #     return page

    # 基金普通卖出
    @robot_log
    def normal_redeem_fund_product(self, fund_product_name_for_fast_redeem, redeem_amount, trade_password):
        self.perform_actions(
            TITLE_START, FUND_PRODUCT_STOP % fund_product_name_for_fast_redeem, 'U',
                         FUND_PRODUCT % fund_product_name_for_fast_redeem,
            REDEEM,
            NORMAL_REDEEM,
            REDEEM_AMOUNT, redeem_amount,
            REDEEM_CONFIRM,
            TRADE_PASSWORD, trade_password,
            REDEEM_DONE,
        )

        page = self

        return page

    # 基金极速卖出
    @robot_log
    def fast_redeem_fund_product(self, fund_product_name_for_fast_redeem, redeem_amount, trade_password):
        self.perform_actions(
            TITLE_START, FUND_PRODUCT_STOP % fund_product_name_for_fast_redeem, 'U',
                         FUND_PRODUCT % fund_product_name_for_fast_redeem,
            REDEEM,
            FAST_REDEEM,
            REDEEM_AMOUNT, redeem_amount,
            REDEEM_CONFIRM,
            TRADE_PASSWORD, trade_password,
            REDEEM_DONE,
        )

        page = self

        return page

    @robot_log
    def go_to_my_fund_plan_page(self):
        self.perform_actions(TITLE_START, MY_FUND_PLAN_STOP, 'U')
        self.perform_actions(MY_FUND_PLAN)

        if self.element_exist("//android.widget.TextView[@text='我的定投计划']"):
            page = huaxin_ui.ui_android_xjb_3_0.my_fund_plan_page.MyFundPlanPage(self.web_driver)
            ASSERT_DICT.update({'page': 'MyFundPlanPage'})
        else:
            ASSERT_DICT.update({'page': 'StartFundPlanPage'})
            page = huaxin_ui.ui_android_xjb_3_0.start_fund_plan_page.StartFundPlanPage(self.web_driver)
        return page

    @robot_log
    def back_to_assets_analysis_page(self):
        self.perform_actions(
            BACK
        )

        page = huaxin_ui.ui_android_xjb_3_0.assets_analysis_page.AssetsAnalysisPage(self.web_driver)

        return page

    @robot_log
    def go_to_fund_assets_structure_page(self):
        self.perform_actions(
            FUND_TOTAL
        )

        page = huaxin_ui.ui_android_xjb_3_0.fund_assets_structure_page.FundAssetsStructurePage(self.web_driver)
        time.sleep(5)

        return page

    @robot_log
    def go_to_description_page(self):
        self.perform_actions(SHOW_TIPS)

        page = huaxin_ui.ui_android_xjb_3_0.description_page.DescriptionPage(self.web_driver)

        return page

    @robot_log
    def go_to_fund_supplementary_purchase_page(self, fund_product):
        self.perform_actions(TITLE_START, FUND_STOP % fund_product, 'U',
                             FUND % fund_product,
                             )

        page = huaxin_ui.ui_android_xjb_3_0.fund_supplementary_purchase_page.FundSupplementaryPurchasePage(
            self.web_driver)

        return page

    @robot_log
    def go_to_fund_redeem_page(self, fund_product):
        self.perform_actions(TITLE_START, FUND_REDEEM_STOP % fund_product, 'U')
        holding_amount = self.get_text(HOLDING_AMOUNT)
        ASSERT_DICT.update({'holding_amount': holding_amount})
        self.perform_actions(FUND_REDEEM % fund_product)

        page = huaxin_ui.ui_android_xjb_3_0.fund_redeem_page.FundRedeemPage(self.web_driver)

        return page

    @robot_log
    def go_to_fund_history_holding_page(self):
        self.perform_actions(HISTORY_HOLDING_BUTTON)

        page = self

        return page

    @robot_log
    def verify_fund_history_holding_detail(self, fund_product):
        self.assert_values('产品名称', self.get_text('com.shhxzq.xjb:id/tv_fund_asset_item_purchase_amt_title',
                                                 'find_element_by_id'))
        self.assert_values(fund_product, self.get_text('com.shhxzq.xjb:id/tv_fund_asset_item_purchase_amt',
                                                       'find_element_by_id'))
        self.assert_values('累计收益', self.get_text('com.shhxzq.xjb:id/tv_fund_resent_profit_title',
                                                 'find_element_by_id'))
        self.assert_values('10.00元', self.get_text('com.shhxzq.xjb:id/tv_fund_asset_item_resent_profit',
                                                  'find_element_by_id'))

        page = self

        return page

    @robot_log
    def go_to_history_holding_page(self, fund_product):
        self.perform_actions(TITLE_START, HISTORY_HOLDING_STOP % fund_product, 'U')
        self.perform_actions(HISTORY_HOLDING % fund_product)

        page = huaxin_ui.ui_android_xjb_3_0.history_holding_page.HistoryHoldingPage(self.web_driver)

        return page
