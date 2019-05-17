# coding: utf-8
import re

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.trade_complete_page

REDEEM_AMOUNT = "xpathIOS_UIATextField_//UIATextField[@value='请输入卖出份额']"
REDEEM_AMOUNT_2 = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField"
REDEEM_AMOUNT_LOCATOR = "/AppiumAUT/UIAApplication/UIAWindow/UIATextField"
NORMAL_REDEEM_VIP_PRODUCT_AMOUNT = "xpathIOS_UIATextField_//UIATextField[@value='请输入卖出份额']"
REDEEM_CONFIRM = "accId_UIAButton_(UIButton_确认)"
TRADE_PASSWORD = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField"

NORMAL_REDEEM = "accId_UIAButton_(UIButton_icon_selected)"
FAST_REDEEM = "accId_UIAButton_(UIButton_icon_unselected)"

REDEEM_RULE = "accId_UIAButton_(UIButton_卖出规则)"


class HighEndRedeemPage(PageObject):
    def __init__(self, web_driver):
        super(HighEndRedeemPage, self).__init__(web_driver)

    @robot_log
    def redeem_high_end_product(self, redeem_amount, trade_password):
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
            message = self.get_text('卖出金额要大于0元哦', 'find_element_by_accessibility_id')
            self.assert_values('卖出金额要大于0元哦', message)

            page = self
            return page

        self.perform_actions(
            REDEEM_CONFIRM,
            TRADE_PASSWORD, trade_password
        )

        page = huaxin_ui.ui_ios_xjb_3_0.trade_complete_page.TradeCompletePage(self.web_driver)

        return page

    @robot_log
    def normal_redeem_vip_product(self, redeem_amount, trade_password):
        self.perform_actions(
            NORMAL_REDEEM,
            NORMAL_REDEEM_VIP_PRODUCT_AMOUNT, redeem_amount,
            REDEEM_CONFIRM,
            TRADE_PASSWORD, trade_password,
        )

        page = huaxin_ui.ui_ios_xjb_3_0.trade_complete_page.TradeCompletePage(self.web_driver)

        return page

    @robot_log
    def fast_redeem_vip_product(self, redeem_amount, trade_password):
        self.perform_actions(
            FAST_REDEEM,
            REDEEM_AMOUNT, redeem_amount,
            REDEEM_CONFIRM,
            TRADE_PASSWORD, trade_password
        )

        page = huaxin_ui.ui_ios_xjb_3_0.trade_complete_page.TradeCompletePage(self.web_driver)

        return page
