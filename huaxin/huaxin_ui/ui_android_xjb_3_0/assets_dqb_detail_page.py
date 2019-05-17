# coding: utf-8

from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
from _common.global_config import ASSERT_DICT
from huaxin_ui.ui_android_xjb_3_0.trade_detail_page import TradeDetailPage
import huaxin_ui.ui_android_xjb_3_0.assets_analysis_page
import huaxin_ui.ui_android_xjb_3_0.dqb_supplementary_purchase_page
import huaxin_ui.ui_android_xjb_3_0.description_page
import huaxin_ui.ui_android_xjb_3_0.finance_dqb_page
import huaxin_ui.ui_android_xjb_3_0.dqb_redeem_page
import time
import re

TRADE_DETAIL = "xpath_//android.widget.Button[@text='交易记录']"
DQB_MORE_PRODUCT = "xpath_//android.widget.TextView[@text='查看更多产品']"
DQB_MORE_PRODUCT_STOP = "swipe_xpath_//android.widget.TextView[@text='查看更多产品']"

DQB_START = "swipe_xpath_//android.widget.TextView[@text='定活宝']"
HISTORY_PRODUCT_STOP = "swipe_xpath_//android.widget.TextView[@text='查看历史产品']"
HISTORY_PRODUCT = "xpath_//android.widget.TextView[@text='查看历史产品']"

TITLE_START = "swipe_xpath_//android.widget.TextView[@text='定活宝']"
DQB_PRODUCT_STOP = "swipe_xpath_//android.widget.TextView[@text='%s']"
DQB_PRODUCT = "xpath_//android.widget.TextView[@text='%s']"
REDEEM = "xpath_//android.widget.Button[@text='取回']"
REDEEM_AMOUNT = "xpath_//android.widget.EditText[@text='请输入取回金额']"
REDEEM_CONFIRM = "xpath_//android.widget.Button[@text='确认']"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"
REDEEM_DONE = "xpath_//android.widget.Button[@text='确认']"
SWIPE_BEGIN = "swipe_xpath_//"
SWIPE_STOP = "swipe_xpath_//android.widget.TextView[@text='交易记录']"
TRADE_RECORDS = "xpath_//android.widget.TextView[@text='交易记录']"
REDEEM_TIPS = "com.shhxzq.xjb:id/tv_dqb_redeem_product_tips"
BACK = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left_orange']"
DHB_SWIPE_STOP = "swipe_xpath_//android.widget.TextView[@text='购买金额']"
DHB_STOP = "swipe_xpath_//android.widget.TextView[@text='购买确认中']/preceding-sibling::android.widget.LinearLayout/android.widget.TextView[contains(@text,'%s')]"
DHB_PRODUCT = "xpath_//android.widget.TextView[@text='购买金额']"
SHOW_TIPS = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/img_mydqb_show_tips']"
DHB = "xpath_//android.widget.TextView[@text='购买确认中']/preceding-sibling::android.widget.LinearLayout/android.widget.TextView[contains(@text,'%s')]"
HISTORY_HOLDING_BUTTON = "xpath_//android.widget.TextView[@text='历史持仓']"
HISTORY_HOLDING_STOP = "swipe_xpath_//android.widget.TextView[@text='%s']"
HISTORY_HOLDING = "xpath_//android.widget.TextView[@text='%s']"

current_page = []


class AssetsDqbDetailPage(PageObject):
    def __init__(self, web_driver):
        super(AssetsDqbDetailPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_page_title(self):
        self.assert_values('定活宝', self.get_text('com.shhxzq.xjb:id/title_actionbar_orange', 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def verify_dhb_assets_details(self):
        self.assert_values('True', str(self.element_exist("//android.widget.TextView[@text='定活宝总资产(元)']")))
        dhb_total_actual = self.get_text('com.shhxzq.xjb:id/mydqb_total', 'find_element_by_id').replace(',', '')
        self.assert_values(ASSERT_DICT['dhb_asset_login'], dhb_total_actual)
        self.assert_values('True', str(self.element_exist("//android.widget.TextView[@text='累计收益(元)']")))

        page = self

        return page

    @robot_log
    def go_to_trade_detail_page(self):
        self.perform_actions(TRADE_DETAIL)
        page = TradeDetailPage(self.web_driver)
        return page

    @robot_log
    def view_dqb_more_product(self):
        self.perform_actions(SWIPE_BEGIN, DQB_MORE_PRODUCT_STOP, 'U')
        self.perform_actions(DQB_MORE_PRODUCT)

        page = huaxin_ui.ui_android_xjb_3_0.finance_dqb_page.FinanceDqbPage(self.web_driver)
        return page

    @robot_log
    def view_dqb_history_product(self):
        self.perform_actions(
            DQB_MORE_PRODUCT)

        time.sleep(3)
        self.perform_actions(DQB_START, HISTORY_PRODUCT_STOP, 'U',
                             HISTORY_PRODUCT,
                             )

    @robot_log
    def back_to_assets_analysis_page(self):
        self.perform_actions(
            BACK
        )

        page = huaxin_ui.ui_android_xjb_3_0.assets_analysis_page.AssetsAnalysisPage(self.web_driver)

        return page

    @robot_log
    def go_to_dqb_supplementary_purchase_page(self):
        time.sleep(3)
        self.perform_actions(TITLE_START, DHB_SWIPE_STOP, 'U',
                             DHB_PRODUCT,
                             )

        page = huaxin_ui.ui_android_xjb_3_0.dqb_supplementary_purchase_page.DqbSupplementaryPurchasePage(
            self.web_driver)

        return page

    @robot_log
    def go_to_description_page(self):
        self.perform_actions(SHOW_TIPS)

        page = huaxin_ui.ui_android_xjb_3_0.description_page.DescriptionPage(self.web_driver)

        return page

    @robot_log
    def go_to_dqb_supplementary_purchase_page_(self, product_name):
        self.perform_actions(TITLE_START, DHB_STOP % product_name, 'U',
                             DHB % product_name,
                             )

        page = huaxin_ui.ui_android_xjb_3_0.dqb_supplementary_purchase_page.DqbSupplementaryPurchasePage(
            self.web_driver)

        return page

    @robot_log
    def go_to_dqb_redeem_page(self, product_name):
        self.perform_actions(SWIPE_BEGIN, DQB_PRODUCT_STOP % product_name, 'U',
                             DQB_PRODUCT % product_name,
                             )

        page = huaxin_ui.ui_android_xjb_3_0.dqb_redeem_page.DqbRedeemPage(self.web_driver)

        return page

    @robot_log
    def go_to_dhb_history_holding_list_page(self):
        self.perform_actions(HISTORY_HOLDING_BUTTON)

        page = self

        return page

    @robot_log
    def verify_dhb_history_holding_detail(self, product_name):
        self.assert_values('产品名称', self.get_text('com.shhxzq.xjb:id/tv_myassets_amt_title', 'find_element_by_id'))
        self.assert_values(product_name, self.get_text('com.shhxzq.xjb:id/myassets_amt', 'find_element_by_id'))
        self.assert_values('累计收益', self.get_text('com.shhxzq.xjb:id/tv_item_yield_type_title', 'find_element_by_id'))
        self.assert_values('10.00元', self.get_text('com.shhxzq.xjb:id/myassets_yield', 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def go_to_history_holding_page(self, product_name):
        self.perform_actions(SWIPE_BEGIN, HISTORY_HOLDING_STOP % product_name, 'U')
        self.perform_actions(HISTORY_HOLDING % product_name)

        page = huaxin_ui.ui_android_xjb_3_0.history_holding_page.HistoryHoldingPage(self.web_driver)

        return page
