# coding: utf-8
import re
import time

from _common.global_config import ASSERT_DICT
from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
from huaxin_ui.ui_ios_xjb_3_0.dhb_trade_detail_page import DhbTradeDetailPage
from huaxin_ui.ui_ios_xjb_3_0.trade_detail_page import TradeDetailPage
import huaxin_ui.ui_ios_xjb_3_0.assets_page
import huaxin_ui.ui_ios_xjb_3_0.finance_dqb_page
import huaxin_ui.ui_ios_xjb_3_0.finance_dqb_history_page
import huaxin_ui.ui_ios_xjb_3_0.trade_complete_page
import huaxin_ui.ui_ios_xjb_3_0.holding_assets_description_page
import huaxin_ui.ui_ios_xjb_3_0.dhb_holding_detail_page

TRADE_DETAIL = "accId_UIAButton_交易记录"
DQB_MORE_PRODUCT = "accId_UIAButton_查看更多产品"

DQB_START = "swipe_accId_//"
HISTORY_PRODUCT_STOP = "swipe_accId_(查看历史产品)"
HISTORY_PRODUCT = "accId_UIAElement_(查看历史产品)"

TITLE_START = "swipe_accId_定活宝"
DQB_PRODUCT_STOP = "swipe_accId_%s"
DQB_PRODUCT = "accId_UIAStaticText_%s"
REDEEM = "accId_UIAButton_取回"
QUESTION_MARK = "accId_UIAImage_(icon_questionAbout)"
TRADE_RECORD = "accId_UIAButton_交易记录"
# REDEEM_AMOUNT = "accId_UIATextField_(textField)请输入取回金额"
REDEEM_AMOUNT = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField"
REDEEM_CONFIRM = "accId_UIAButton_(UIButton_确认)"
TRADE_PASSWORD = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField"
REDEEM_DONE = "accId_UIAButton_(UIButton_确认)"

REDEEM_ALL = "accId_UIAButton_(UIButton_全部取回)"
REDEEM_RULE = "accId_UIAButton_(UIButton_取回规则)"

REDEEM_AMOUNT_ACTUAL = "//UIAStaticText[@label='取回']/./following-sibling::UIAStaticText[2]"
SWIPE_STOP = "swipe_xpath_IOS//UIAStaticText[@label='%s']/following-sibling::UIAStaticText[@label='购买金额'][1]"
SELECT_PRODUCT = "xpathIOS_UIAStaticText_" \
                 "//UIAStaticText[@label='%s']/following-sibling::UIAStaticText[@label='购买金额'][1]"
HISTORY_HOLDING = "xpathIOS_UIAButton_//UIAButton[contains(@label, '历史持有')]"
current_page = []


class AssetsDqbDetailPage(PageObject):
    def __init__(self, web_driver):
        super(AssetsDqbDetailPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def go_to_trade_detail_page(self):
        self.perform_actions(TRADE_DETAIL)
        page = TradeDetailPage(self.web_driver)
        return page

    @robot_log
    def verify_at_dhb_holding_list_page(self):
        self.assert_values("定活宝", self.get_text("//UIAStaticText[@label='定活宝']"))
        page = self
        return page

    @robot_log
    def view_dqb_more_product(self):
        time.sleep(2)
        self.perform_actions(
            DQB_MORE_PRODUCT,
        )

        page = huaxin_ui.ui_ios_xjb_3_0.finance_dqb_page.FinanceDqbPage(self.web_driver)

        return page

    @robot_log
    def go_to_dhb_description(self):
        self.perform_actions(QUESTION_MARK)

        page = huaxin_ui.ui_ios_xjb_3_0.holding_assets_description_page.HoldingAssetsDescriptionPage(self.web_driver)

        return page

    @robot_log
    def view_dqb_history_product(self):
        time.sleep(2)
        self.perform_actions(
            DQB_MORE_PRODUCT,
            # DQB_START, HISTORY_PRODUCT_STOP, 'U',
        )

        try:
            self.perform_actions(
                HISTORY_PRODUCT,
            )
        except Exception, e:
            print e
            self.perform_actions(HISTORY_PRODUCT)

        page = huaxin_ui.ui_ios_xjb_3_0.finance_dqb_history_page.FinanceDqbHistoryPage(self.web_driver)

        return page

    @robot_log
    def view_dqb_trade_record(self, dqb_product=None):
        self.perform_actions(
            # TITLE_START, DQB_PRODUCT_STOP % dqb_product, 'U',
            # DQB_PRODUCT % dqb_product,
            TRADE_RECORD,
        )
        title = self.get_text("//UIAStaticText[@label='交易记录']")
        self.assert_values('交易记录', title)

        page = DhbTradeDetailPage(self.web_driver)

        return page

    @robot_log
    def redeem_dqb_product(self, redeem_amount, trade_password, dqb_product):
        time.sleep(3)
        self.perform_actions(
            # TITLE_START, DQB_PRODUCT_STOP % dqb_product, 'U',
            DQB_PRODUCT % dqb_product, REDEEM)
        most_redeem = self.get_text("//UIATextField[@value='请输入取回金额']/./following-sibling::UIAStaticText[1]")
        most_redeem = re.findall(r'(\d{1,3}(,\d{3})*.\d+)', most_redeem)[0][0].replace(',', '')

        self.perform_actions(
            REDEEM_AMOUNT, redeem_amount,
        )

        input_redeem = self.get_text("/AppiumAUT/UIAApplication/UIAWindow/UIATextField").replace(',', '')

        if input_redeem is not '0':
            redeem_amount_actual = self.get_text(REDEEM_AMOUNT_ACTUAL)
            redeem_amount_actual = re.findall(r'(\d{1,3}(,\d{3})*.\d+)', redeem_amount_actual)[1][0].replace(',', '')
            ASSERT_DICT.update(
                {'dhb_redeem_actual': redeem_amount_actual})

        if input_redeem == most_redeem:
            page = self

            # 验证还在卖出页面
            self.assert_values(True, self.element_exist("//UIAButton[@label='全部取回']"))
            return page

        if input_redeem == '0':
            self.perform_actions(REDEEM_CONFIRM)
            # message = self.get_text('(取回金额要大于0元哦)', 'find_element_by_accessibility_id')
            self.assert_values(True, self.element_exist("//UIAButton[@label='全部取回']"))
            page = self
            return page

        self.perform_actions(
            REDEEM_CONFIRM,
            TRADE_PASSWORD, trade_password,
        )

        page = huaxin_ui.ui_ios_xjb_3_0.trade_complete_page.TradeCompletePage(self.web_driver)
        return page

    @robot_log
    def go_to_dhb_holding_details_page(self, product_name):
        self.perform_actions('swipe_accId_//', SWIPE_STOP % product_name, 'U',
                             SELECT_PRODUCT % product_name
                             )

        page = huaxin_ui.ui_ios_xjb_3_0.dhb_holding_detail_page.DhbHoldingDetailPage(
            self.web_driver)

        return page
