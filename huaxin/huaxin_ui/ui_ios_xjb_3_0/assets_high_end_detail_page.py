# coding: utf-8
import re

import time

from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
# from huaxin_ui.ui_ios_xjb_3_0.trade_detail_page import TradeDetailPage
import huaxin_ui.ui_ios_xjb_3_0.trade_detail_page
import huaxin_ui.ui_ios_xjb_3_0.assets_page
from huaxin_ui.ui_ios_xjb_3_0.vip_trade_detail_page import ViPTradeDetailPage
import huaxin_ui.ui_ios_xjb_3_0.finance_high_end_page
import huaxin_ui.ui_ios_xjb_3_0.trade_complete_page
import huaxin_ui.ui_ios_xjb_3_0.holding_assets_description_page
import huaxin_ui.ui_ios_xjb_3_0.high_end_holding_detail_page
import huaxin_ui.ui_ios_xjb_3_0.history_holding_vip_detail_page
import huaxin_ui.ui_ios_xjb_3_0.expiry_processing_type_page

TRADE_DETAIL = "accId_UIAButton_交易记录"
HIGH_END_MORE_PRODUCT = "accId_UIAButton_查看更多产品"

HIGH_END_START = "swipe_accId_高端"
# HISTORY_PRODUCT_STOP = "swipe_accId_查看历史产品"
# HISTORY_PRODUCT = "accId_UIAButton_查看历史产品"
HISTORY_PRODUCT_STOP = "swipe_accId_固定收益系列"
FIXED_RATE_PRODUCT = "accId_UIAStaticText_固定收益系列"

TITLE_START = "swipe_accId_//"
HIGH_END_PRODUCT_STOP = "swipe_accId_%s"
HIGH_END_PRODUCT = "accId_UIAStaticText_%s"
REDEEM = "accId_UIAButton_卖出"
TRADE_RECORD = "accId_UIAButton_交易记录"
REDEEM_AMOUNT = "xpathIOS_UIATextField_//UIATextField[@value='请输入卖出份额']"
# REDEEM_AMOUNT_2 = "accId_UIATextField_(textField)请输入卖出份额"
REDEEM_AMOUNT_2 = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField"
REDEEM_AMOUNT_LOCATOR = "/AppiumAUT/UIAApplication/UIAWindow/UIATextField"
NORMAL_REDEEM_VIPPRODUCT_AMOUNT = "xpathIOS_UIATextField_//UIATextField[@value='请输入卖出份额']"
REDEEM_CONFIRM = "accId_UIAButton_(UIButton_确认)"
TRADE_PASSWORD = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField"
REDEEM_DONE = "accId_UIAButton_(UIButton_确认)"

NORMAL_REDEEM = "accId_UIAButton_(UIButton_icon_selected)"
FAST_REDEEM = "accId_UIAButton_(UIButton_icon_unselected)"

REDEEM_RULE = "accId_UIAButton_(UIButton_卖出规则)"
QUESTION_MARK = "accId_UIAImage_(icon_questionAbout)"
# VIP_SWIPE_STOP = "swipe_accId_购买金额"
VIP_SWIPE_STOP = "swipe_xpath_IOS//UIAStaticText[@label='%s']/following-sibling::UIAStaticText[@label='购买金额'][1]"
VIP_PRODUCT = "xpathIOS_UIAStaticText_//UIAStaticText[@label='%s']/following-sibling::UIAStaticText[@label='购买金额'][1]"

VIP_PRODUCT_SELECT = "xpathIOS_UIAStaticText_" \
                     "//UIAStaticText[@label='%s']/following-sibling::UIAStaticText[@label='持有金额'][1]"
HISTORY_HOLDING = "xpathIOS_UIAButton_//UIAButton[contains(@label, '历史持有')]"
HISTORY_PRODUCT = "accId_UIAStaticText_%s"
EXPIRY_PROCESSING_MODIFY = "swipe_accId_更改"
EXPIRY_PROCESSING = "accId_UIAButton_更改"

current_page = []


class AssetsHighEndDetailPage(PageObject):
    def __init__(self, web_driver):
        super(AssetsHighEndDetailPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def go_to_trade_detail_page(self):
        self.perform_actions(TRADE_DETAIL)
        page = huaxin_ui.ui_ios_xjb_3_0.trade_detail_page.TradeDetailPage(self.web_driver)
        return page

    @robot_log
    def verify_at_high_end_holding_list_page(self):
        self.assert_values("高端理财", self.get_text("//UIAStaticText[@label='高端理财']"))
        page = self
        return page

    @robot_log
    def view_high_end_more_product(self):
        self.perform_actions(
            HIGH_END_MORE_PRODUCT,
        )

        page = huaxin_ui.ui_ios_xjb_3_0.finance_high_end_page.FinanceHighEndPage(self.web_driver)

        return page

    @robot_log
    def go_to_high_end_description(self):
        self.perform_actions(QUESTION_MARK)

        page = huaxin_ui.ui_ios_xjb_3_0.holding_assets_description_page.HoldingAssetsDescriptionPage(self.web_driver)
        return page

    @robot_log
    def view_high_end_trade_record(self, high_end_product=None):
        self.perform_actions(
            # TITLE_START, HIGH_END_PRODUCT_STOP % high_end_product, 'U',
            # HIGH_END_PRODUCT % high_end_product,
            TRADE_RECORD,
        )
        self.assert_values('交易记录', self.get_text("//UIAStaticText[@label='交易记录']"))
        page = ViPTradeDetailPage(self.web_driver)

        return page

    @robot_log
    def redeem_high_end_product(self, redeem_amount, trade_password, high_end_product):
        self.perform_actions(
            TITLE_START, HIGH_END_PRODUCT_STOP % high_end_product, 'U',
                         HIGH_END_PRODUCT % high_end_product,
            REDEEM,
        )
        most_redeem = self.get_text("//UIATextField[@value='请输入卖出份额']/./following-sibling::UIAStaticText[1]")
        most_redeem = re.findall(r'(\d{1,3}(,\d{3})*.\d+)', most_redeem)[0][0].replace(',', '')

        self.perform_actions(
            REDEEM_AMOUNT_2, redeem_amount,
        )
        input_redeem = self.get_text(REDEEM_AMOUNT_LOCATOR).replace(',', '')

        if input_redeem == most_redeem:
            page = self

            # 验证还在卖出页面
            self.assert_values(True, self.element_exist("//UIAButton[@label='卖出规则']"))
            return page

        if input_redeem == '0':
            self.perform_actions(
                REDEEM_CONFIRM,
            )
            # message = self.get_text('卖出金额要大于0元哦', 'find_element_by_accessibility_id')
            # self.assert_values('卖出金额要大于0元哦', message)
            self.assert_values(True, self.element_exist("//UIAButton[@label='卖出规则']"))

            page = self
            return page

        self.perform_actions(
            REDEEM_CONFIRM,
            TRADE_PASSWORD, trade_password
        )

        page = huaxin_ui.ui_ios_xjb_3_0.trade_complete_page.TradeCompletePage(self.web_driver)

        return page

    @robot_log
    def normal_redeem_vipproduct(self, redeem_amount, trade_password, high_end_product_for_fast_redeem):
        self.perform_actions(
            TITLE_START, HIGH_END_PRODUCT_STOP % high_end_product_for_fast_redeem, 'U',
                         HIGH_END_PRODUCT % high_end_product_for_fast_redeem,
            REDEEM,
            NORMAL_REDEEM,
            NORMAL_REDEEM_VIPPRODUCT_AMOUNT, redeem_amount,
            REDEEM_CONFIRM,
            TRADE_PASSWORD, trade_password,
        )

        page = huaxin_ui.ui_ios_xjb_3_0.trade_complete_page.TradeCompletePage(self.web_driver)

        return page

    @robot_log
    def fast_redeem_vipproduct(self, redeem_amount, trade_password, high_end_product_for_fast_redeem):
        self.perform_actions(
            TITLE_START, HIGH_END_PRODUCT_STOP % high_end_product_for_fast_redeem, 'U',
                         HIGH_END_PRODUCT % high_end_product_for_fast_redeem,
            REDEEM,
            FAST_REDEEM,
            REDEEM_AMOUNT, redeem_amount,
            REDEEM_CONFIRM,
            TRADE_PASSWORD, trade_password,
        )

        page = huaxin_ui.ui_ios_xjb_3_0.trade_complete_page.TradeCompletePage(self.web_driver)

        return page

    # 购买确认中的产品持有.
    @robot_log
    def go_to_high_end_holding_detail_page(self, product_name):
        self.perform_actions('swipe_xpath_//', VIP_SWIPE_STOP % product_name, 'U')

        time.sleep(1)
        self.perform_actions(
            VIP_PRODUCT % product_name
        )

        page = huaxin_ui.ui_ios_xjb_3_0.high_end_holding_detail_page.HighEndHoldingDetailPage(
            self.web_driver)

        return page

    # 已经持有的高端产品
    @robot_log
    def go_to_confirmed_high_end_holding_detail_page(self, product_name):
        self.perform_actions("swipe_accId_//",
                             "swipe_xpath_IOS//UIAStaticText[@label='%s']/following-sibling::UIAStaticText[@label='持有金额'][1]" % product_name,
                             'U',
                             VIP_PRODUCT_SELECT % product_name
                             )

        page = huaxin_ui.ui_ios_xjb_3_0.high_end_holding_detail_page.HighEndHoldingDetailPage(
            self.web_driver)

        return page

    # 进入历史持有详情页面
    @robot_log
    def go_to_vip_history_detail_page(self, product_name):
        self.perform_actions(HISTORY_HOLDING)

        # 点击某个具体历史持有产品
        self.perform_actions(HISTORY_PRODUCT % product_name)
        page = huaxin_ui.ui_ios_xjb_3_0.history_holding_vip_detail_page.HistoryHoldingVipDetailPage(self.web_driver)
        return page

    @robot_log
    def go_to_expiry_processing_type_page(self):
        self.perform_actions("swipe_accId_//", EXPIRY_PROCESSING_MODIFY, 'U')
        self.perform_actions(EXPIRY_PROCESSING)

        page = huaxin_ui.ui_ios_xjb_3_0.expiry_processing_type_page.ExpiryProcessingTypePage(self.web_driver)
        return page
