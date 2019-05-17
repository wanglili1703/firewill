# coding: utf-8
import re

import time

from _common.global_config import ASSERT_DICT
from _common.page_object import PageObject

from _common.xjb_decorator import robot_log, user_info_close_afterwards, message_i_know_afterwards
import huaxin_ui.ui_ios_xjb_3_0.fund_page_all_fund_page
import huaxin_ui.ui_ios_xjb_3_0.trade_complete_page
from huaxin_ui.ui_ios_xjb_3_0.fund_trade_detail_page import FundTradeDetailPage
import huaxin_ui.ui_ios_xjb_3_0.trade_detail_page
import huaxin_ui.ui_ios_xjb_3_0.my_fund_plan_page
import huaxin_ui.ui_ios_xjb_3_0.start_fund_plan_page
import huaxin_ui.ui_ios_xjb_3_0.fund_assets_structure_page
import huaxin_ui.ui_ios_xjb_3_0.holding_assets_description_page
import huaxin_ui.ui_ios_xjb_3_0.fund_holding_detail_page
import huaxin_ui.ui_ios_xjb_3_0.history_holding_fund_detail_page
import huaxin_ui.ui_ios_xjb_3_0.fund_redeem_page

TRADE_DETAIL = "accId_UIAButton_UIBarButtonItemLocationRight"
FUND_MORE_PRODUCT = "accId_UIAButton_查看更多产品"
REDEEM = "accId_UIAButton_卖出"
TRADE_RECORD = "accId_UIAButton_UIBarButtonItemLocationRight"
REDEEM_AMOUNT = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField"
REDEEM_CONFIRM = "accId_UIAButton_(UIButton_确认)"
TRADE_PASSWORD = "xpathIOS_UIATextField_IOS//UIAImage[@name='(entryPwd.png)']/./following-sibling::UIATextField[1]"
REDEEM_DONE = "accId_UIAButton_UIButton_确认"

TITLE_START = "swipe_xpath_//"
FUND_PRODUCT_STOP = "swipe_accId_%s"
FUND_PRODUCT = "accId_UIAStaticText_%s"
NORMAL_REDEEM = "accId_UIAButton_(icon_selected)"
FAST_REDEEM = "accId_UIAButton_(icon_unselected)"
MY_FUND_PLAN = "accId_UIAButton_我的定投计划"
FUND_TOTAL = "accId_UIAButton_(UIButton_fund_tips_white_tips)"

HIDE_KEYBOARD = "accId_UIAButton_(UIButton_SafeKeyBoard_Hide)"
QUESTION_MARK = "accId_UIAButton_(UIButton_icon_questionAbout)"
SWIPE_STOP = "swipe_accId_购买金额"
SELECT_PRODUCT = "xpathIOS_UIAStaticText_" \
                 "//UIAStaticText[@label='%s(%s)']/following-sibling::UIAStaticText[@label='购买金额'][2]"

SELECT_PRODUCT_1 = "xpathIOS_UIAStaticText_" \
                   "//UIAStaticText[@label='%s']/following-sibling::UIAStaticText[@label='持有金额'][1]"
HISTORY_HOLDING = "xpathIOS_UIAButton_//UIAButton[contains(@label, '历史持有')]"
HISTORY_PRODUCT = "accId_UIAStaticText_%s"
FUND_REDEEM_STOP = "swipe_xpath_IOS//UIAStaticText[contains(@label,'%s')]/" \
                   "following-sibling::UIAStaticText[@label='持有金额'][1]"
HOLDING_AMOUNT = "//UIAStaticText[contains(@label,'%s')]/" \
                   "following-sibling::UIAStaticText[3]"
FUND_REDEEM = "xpathIOS_UIAStaticText_//UIAStaticText[contains(@label,'%s')]/" \
                   "following-sibling::UIAStaticText[@label='持有金额'][1]"
current_page = []


class AssetsFundDetailPage(PageObject):
    def __init__(self, web_driver):
        super(AssetsFundDetailPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def go_to_trade_detail_page(self):
        self.perform_actions(TRADE_DETAIL)
        page = huaxin_ui.ui_ios_xjb_3_0.trade_detail_page.TradeDetailPage(self.web_driver)
        return page

    @robot_log
    def verify_at_fund_holding_list_page(self):
        self.assert_values("基金", self.get_text("//UIAStaticText[@label='基金']"))
        page = self
        return page

    @robot_log
    def go_to_fund_description(self):
        self.perform_actions(QUESTION_MARK)

        page = huaxin_ui.ui_ios_xjb_3_0.holding_assets_description_page.HoldingAssetsDescriptionPage(self.web_driver)
        return page

    @robot_log
    @message_i_know_afterwards
    def go_to_fund_more_product_page(self):
        self.perform_actions(
            FUND_MORE_PRODUCT,
        )

        page = huaxin_ui.ui_ios_xjb_3_0.fund_page_all_fund_page.FundPageAllFundPage(self.web_driver)

        return page

    @robot_log
    def view_fund_trade_record(self, fund_product_name_for_redeem=None):
        self.perform_actions(
            TRADE_RECORD,
        )
        title = self.get_text("//UIAStaticText[@label='交易记录']")
        self.assert_values('交易记录', title)

        page = FundTradeDetailPage(self.web_driver)

        return page

    @robot_log
    def redeem_fund_product(self, amount, trade_password, fund_product_name_for_redeem):
        self.perform_actions(
            # TITLE_START, FUND_PRODUCT_STOP % fund_product_name_for_redeem, 'U',
            FUND_PRODUCT % fund_product_name_for_redeem,
            REDEEM)

        most_redeem = self.get_text("//UIATextField[@value='请输入卖出份额']/./following-sibling::UIAStaticText[1]")
        most_redeem = re.findall(r'(\d{1,3}(,\d{3})*.\d+)', most_redeem)[0][0].replace(',', '')

        self.perform_actions(
            REDEEM_AMOUNT, amount,
            HIDE_KEYBOARD
        )
        input_redeem = self.get_text('/AppiumAUT/UIAApplication/UIAWindow/UIATextField').replace(',', '')

        if input_redeem == most_redeem:
            # 验证还在卖出页面
            self.assert_values(True, self.element_exist("//UIAButton[@label='全部卖出']"))
            page = self
            return page

        if input_redeem == '0':
            self.perform_actions(
                REDEEM_CONFIRM,
            )
            # 验证还在卖出页面
            self.assert_values(True, self.element_exist("//UIAButton[@label='全部卖出']"))

            # msg = self.get_text('(交易金额不合法)', 'find_element_by_accessibility_id')
            # self.assert_values('交易金额不合法', msg)
            page = self
            return page

        self.perform_actions(REDEEM_CONFIRM)

        time.sleep(1)
        self.perform_actions(
            TRADE_PASSWORD, trade_password,
        )

        page = huaxin_ui.ui_ios_xjb_3_0.trade_complete_page.TradeCompletePage(self.web_driver)

        return page

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
        )

        page = huaxin_ui.ui_ios_xjb_3_0.trade_complete_page.TradeCompletePage(self.web_driver)

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
        )

        page = huaxin_ui.ui_ios_xjb_3_0.trade_complete_page.TradeCompletePage(self.web_driver)

        return page

    @robot_log
    def go_to_my_fund_plan_page(self):
        self.perform_actions(MY_FUND_PLAN)

        if self.element_exist("//UIAStaticText[@label='我的定投计划']"):
            page = huaxin_ui.ui_ios_xjb_3_0.my_fund_plan_page.MyFundPlanPage(self.web_driver)
            ASSERT_DICT.update({'page': 'MyFundPlanPage'})
        else:
            ASSERT_DICT.update({'page': 'StartFundPlanPage'})
            page = huaxin_ui.ui_ios_xjb_3_0.start_fund_plan_page.StartFundPlanPage(self.web_driver)

        page.verify_page_title()
        return page

    @robot_log
    def go_to_fund_assets_structure_page(self):
        time.sleep(2)
        self.perform_actions(
            FUND_TOTAL
        )

        page = huaxin_ui.ui_ios_xjb_3_0.fund_assets_structure_page.FundAssetsStructurePage(self.web_driver)
        time.sleep(3)

        return page

    @robot_log
    def go_to_fund_holding_detail_page(self, product_name, product_code):
        self.perform_actions('swipe_accId_//', SWIPE_STOP, 'U',
                             SELECT_PRODUCT % (product_name, product_code)
                             )

        page = huaxin_ui.ui_ios_xjb_3_0.fund_holding_detail_page.FundHoldingDetailPage(
            self.web_driver)

        return page

    # 已经持有的高端产品
    @robot_log
    def go_to_confirmed_fund_holding_detail_page(self, product_name):
        holding_amount = self.get_text(HOLDING_AMOUNT % product_name)
        ASSERT_DICT.update({'holding_amount': holding_amount})

        self.perform_actions(SELECT_PRODUCT_1 % product_name
                             )

        page = huaxin_ui.ui_ios_xjb_3_0.fund_holding_detail_page.FundHoldingDetailPage(
            self.web_driver)

        return page

    # 进入历史持有详情页面
    @robot_log
    def go_to_fund_history_detail_page(self, product_name):
        self.perform_actions(HISTORY_HOLDING)

        # 点击某个具体历史持有产品
        self.perform_actions(HISTORY_PRODUCT % product_name)
        page = huaxin_ui.ui_ios_xjb_3_0.history_holding_fund_detail_page.HistoryHoldingFundDetailPage(self.web_driver)
        return page
