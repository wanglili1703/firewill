# coding=utf-8
from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.trade_complete_page
import huaxin_ui.ui_ios_xjb_3_0.assets_page
import decimal

RECHARGE_AMOUNT = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIAScrollView/UIATextField"
RECHARGE_CONFIRM_BUTTON = "accId_UIAButton_确认"
TRADE_PASSWORD = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField"

USE_COUPON = "axis_IOS_优惠券_0.5,0"
COUPON = "accId_UIAStaticText_满10减1所有产品不可叠加"
NON_SUPER_COMPOSED_COUPON_SWIPE_STOP = "swipe_accId_满10减1所有产品不可叠加"
COUPON_CONFIRM = "accId_UIAButton_(UIButton_确定)"
current_page = []


class RechargePage(PageObject):
    def __init__(self, web_driver):
        super(RechargePage, self).__init__(web_driver)
        self.elements_exist(*current_page)
        self._return_page = {
            'AssetsPage': huaxin_ui.ui_ios_xjb_3_0.assets_page.AssetsPage(
                self.web_driver)
        }

    @robot_log
    def verify_at_recharge_page(self):
        self.assert_values("存入现金宝", self.get_text("//UIAStaticText[@label='存入现金宝']"))

    @robot_log
    def recharge(self, recharge_amount, trade_password, non_superposed_coupon=None, return_page=None):
        coupon_amount = 0
        self.perform_actions(
            RECHARGE_AMOUNT, recharge_amount
        )

        if non_superposed_coupon is not None:
            self.perform_actions(USE_COUPON)
            coupon_amount = 1

            self.perform_actions("swipe_accId_//", NON_SUPER_COMPOSED_COUPON_SWIPE_STOP, 'U',
                                 COUPON,
                                 COUPON_CONFIRM)
            actual_pay_amount = (decimal.Decimal(recharge_amount) - decimal.Decimal(coupon_amount)).quantize(
                decimal.Decimal('0.00'))
            self.assert_values(str(actual_pay_amount),
                               self.get_text("//UIAStaticText[@label='应付金额']/following-sibling::UIAStaticText"), '==')

        self.perform_actions(RECHARGE_CONFIRM_BUTTON)
        if (float(recharge_amount) >= 0.01) and (float(recharge_amount) < 999999999):
            self.perform_actions(TRADE_PASSWORD, trade_password)

            page = huaxin_ui.ui_ios_xjb_3_0.trade_complete_page.TradeCompletePage(self.web_driver)
        else:
            page = self

        return page
