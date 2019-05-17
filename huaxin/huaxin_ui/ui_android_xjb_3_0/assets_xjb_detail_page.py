# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
from _common.global_config import ASSERT_DICT
from huaxin_ui.ui_android_xjb_3_0.recharge_page import RechargePage
from huaxin_ui.ui_android_xjb_3_0.withdraw_page import WithdrawPage
import huaxin_ui.ui_android_xjb_3_0.assets_analysis_page

from huaxin_ui.ui_android_xjb_3_0.xjb_trade_detail_page import XjbTradeDetailPage
import huaxin_ui.ui_android_xjb_3_0.income_detail_page
import huaxin_ui.ui_android_xjb_3_0.xjb_asset_in_transit_page
import huaxin_ui.ui_android_xjb_3_0.xjb_product_detail_page
import huaxin_ui.ui_android_xjb_3_0.description_page
import huaxin_ui.ui_android_xjb_3_0.what_is_xjb_page
from decimal import *

WITHDRAW = "xpath_//android.widget.Button[@text='取出']"
RECHARGE = "xpath_//android.widget.Button[@text='存入']"
XJB_TRADE_DETAIL = "xpath_//android.widget.Button[@text='收支明细']"
XJB_TOTAL_ASSETS = "com.shhxzq.xjb:id/xjb_home_balance"
INTEREST_PER_WAN = "xpath_//android.widget.TextView[@text='万份收益(元)']"
INTEREST_ACCUMULATED = "xpath_//android.widget.TextView[@text='累计收益(元)']"
SEVEN_DAYS_ANNUAL_RATE_OF_RETURN = "xpath_//android.widget.TextView[@text='查看历史']"
BACK = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left_orange']"
ASSET_IN_TRANSIT = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_xjb_header_transit']"
XJB_PRODUCT_DETAIL = "xpath_//android.widget.TextView[@text='查看产品详情']"
PROFIT_HOME = "xpath_//android.widget.RadioButton[@text='%s']"
SWIPE_BEGIN = "swipe_xpath_//"
SWIPE_STOP = "swipe_xpath_//android.widget.RadioButton[@text='7日']"
SHOW_TIPS = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/img_xjb_home_show_tips']"

current_page = []


class AssetsXjbDetailPage(PageObject):
    def __init__(self, web_driver):
        super(AssetsXjbDetailPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

        self._return_page = {
            'RechargePage': huaxin_ui.ui_android_xjb_3_0.recharge_page.RechargePage(self.web_driver),
            'WhatIsXjbPage': huaxin_ui.ui_android_xjb_3_0.what_is_xjb_page.WhatIsXjbPage(self.web_driver)
        }

    @robot_log
    def verify_page_title(self):
        self.assert_values('现金宝', self.get_text('com.shhxzq.xjb:id/title_actionbar_orange', 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def go_to_recharge_page_from_assets_page(self, return_page='RechargePage'):
        self.perform_actions(RECHARGE)
        page = self._return_page[return_page]
        return page

    @robot_log
    def go_to_withdraw_page(self):
        self.perform_actions(WITHDRAW)
        page = WithdrawPage(self.web_driver)
        return page

    @robot_log
    def go_to_xjb_trade_detail_page(self):
        self.perform_actions(XJB_TRADE_DETAIL)
        page = XjbTradeDetailPage(self.web_driver)
        return page

    @robot_log
    def get_xjb_total_assets(self):
        xjb_total_assets = self.get_text(XJB_TOTAL_ASSETS, 'find_element_by_id')
        ASSERT_DICT.update({'xjb_total_assets': xjb_total_assets})

        page = self
        return page

    @robot_log
    def verify_xjb_total_assets(self, amount, operate_type=None):
        xjb_total_assets_content = self.get_text(XJB_TOTAL_ASSETS, 'find_element_by_id')
        xjb_total_assets_actual = '%.2f' % float(filter(lambda ch: ch in '0123456789.', xjb_total_assets_content))
        if operate_type is None:
            xjb_total_assets_expected = float(
                Decimal(float(str(ASSERT_DICT['xjb_total_assets_login']).replace(',', ''))).quantize(
                    Decimal('0.00'))) + float(amount)
        else:
            # xjb_total_assets_login='%.2f' % float(filter(lambda ch: ch in '0123456789.', xjb_total_assets_content))
            # xjb_total_assets_expected = float(xjb_total_assets_login)- float(amount)
            xjb_total_assets_expected = float(
                Decimal(float(str(ASSERT_DICT['xjb_total_assets_login']).replace(',', ''))).quantize(
                    Decimal('0.00'))) - float(amount)
        ASSERT_DICT.update({'xjb_total_assets': xjb_total_assets_expected})
        self.assert_values('%.2f' % xjb_total_assets_expected, xjb_total_assets_actual, '==')

        page = self
        return page

    @robot_log
    def go_to_interest_page_per_wan(self):
        self.perform_actions(INTEREST_PER_WAN)
        page = huaxin_ui.ui_android_xjb_3_0.income_detail_page.IncomeDetailPage(self.web_driver)

        return page

    @robot_log
    def go_to_interest_page_accumulated(self):
        self.perform_actions(INTEREST_ACCUMULATED)
        page = huaxin_ui.ui_android_xjb_3_0.income_detail_page.IncomeDetailPage(self.web_driver)

        return page

    @robot_log
    def go_to_seven_days_annual_rate_of_return_page(self):
        self.perform_actions(SEVEN_DAYS_ANNUAL_RATE_OF_RETURN)
        page = huaxin_ui.ui_android_xjb_3_0.income_detail_page.IncomeDetailPage(self.web_driver)

        return page

    @robot_log
    def back_to_assets_analysis_page(self):
        self.perform_actions(
            BACK
        )

        page = huaxin_ui.ui_android_xjb_3_0.assets_analysis_page.AssetsAnalysisPage(self.web_driver)

        return page

    @robot_log
    def go_to_asset_in_transit_page(self):
        self.perform_actions(
            ASSET_IN_TRANSIT
        )

        page = huaxin_ui.ui_android_xjb_3_0.xjb_asset_in_transit_page.XjbAssetInTransitPage(self.web_driver)

        return page

    @robot_log
    def go_to_xjb_product_detail_page(self):
        self.perform_actions(
            XJB_PRODUCT_DETAIL
        )

        page = huaxin_ui.ui_android_xjb_3_0.xjb_product_detail_page.XjbProductDetailPage(self.web_driver)

        return page

    @robot_log
    def view_xjb_seven_days_annual_rate_of_return(self, term):
        self.perform_actions(SWIPE_BEGIN, SWIPE_STOP, 'U')
        self.perform_actions(PROFIT_HOME % term)
        page = self

        return page

    @robot_log
    def go_to_description_page(self):
        self.perform_actions(SHOW_TIPS)

        page = huaxin_ui.ui_android_xjb_3_0.description_page.DescriptionPage(self.web_driver)

        return page
