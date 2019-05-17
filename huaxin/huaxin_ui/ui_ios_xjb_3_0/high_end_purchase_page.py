# coding: utf-8
import time

from _common.global_config import ASSERT_DICT
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.trade_complete_page
import huaxin_ui.ui_ios_xjb_3_0.my_coupons_list_page

HIGH_END_START = "swipe_xpath_//"
HIGH_END_PRODUCT_STOP = "swipe_accId_%s"
HIGH_END_PRODUCT = "accId_UIAStaticText_%s"

# AMOUNT = "accId_UIATextField_(textField)请输入购买金额"
# AMOUNT = "accId_UIATextField_(textMoney)"
AMOUNT = "xpathIOS_UIATextField_IOS//UIATextField[@value='请输入购买金额']"
USE_POINTS = "xpathIOS_UIASwitch_//UIASwitch"
BUY_CONFIRM = "accId_UIAButton_(UIButton_确认)"
BUY_CONTINUE = "accId_UIAButton_继续买入[POP]"
BUY_CONSIDER = "accId_UIAButton_再考虑一下[POP]"

TRADE_PASSWORD = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField"
# TRADE_PASSWORD = "accId_UIATextField_(tradePwdBoxView)"

BUY_DONE = "accId_UIAButton_(UIButton_确认)"

USE_COUPON = "accId_UIAButton_(cellCoupon)"

# COUPON_1 = "axis_IOS_满10减1所有产品可叠加"
COUPON_1 = "xpathIOS_UIAStaticText_//UIATableCell/UIAStaticText[@label='满10减1所有产品可叠加' and @visible='true'][1]"
COUPON_1_STOP = "swipe_accId_满10减1所有产品可叠加"
# COUPON_1_2 = "axis_IOS_满10减1所有产品可叠加[index]1"
COUPON_1_2 = "xpathIOS_UIAStaticText_//UIATableCell/UIAStaticText[@label='满10减1所有产品可叠加' and @visible='true'][2]"
# COUPON_2 = "axis_IOS_满10减1所有产品不可叠加"
COUPON_2 = "xpathIOS_UIAStaticText_//UIATableCell/UIAStaticText[@label='满10减1所有产品不可叠加' and @visible='true']"
COUPON_2_STOP = "swipe_accId_满10减1所有产品不可叠加"
# COUPON_CONFIRM = "axis_IOS_确定"
COUPON_CONFIRM = "accId_UIAButton_(UIButton_确定)"

HIGH_END_PRODUCT_2 = "accId_UIATableCell_(HXFinancialTableViewCell)"
HIDE_KEYBOARD = "accId_UIAButton_(UIButton_SafeKeyBoard_Hide)"

BACK = "accId_UIAButton_UIBarButtonItemLocationLeft"

current_page = []


class HighEndPurchasePage(PageObject):
    def __init__(self, web_driver):
        super(HighEndPurchasePage, self).__init__(web_driver)
        self.elements_exist(*current_page)
        self._return_page = {
            "MyCouponsListPage": huaxin_ui.ui_ios_xjb_3_0.my_coupons_list_page.MyCouponsListPage(self.web_driver)
        }

    @robot_log
    def verify_at_high_end_purchase_page(self):
        self.assert_values("买入", self.get_text("//UIAStaticText[@label='买入']"))

        page = self

        return page

    @robot_log
    def go_back_previous_page(self, return_page=None):
        self.perform_actions(BACK)

        page = self._return_page[return_page]

        return page

    @robot_log
    def buy_high_end_product(self, amount, trade_password, points='N', nonsuperposed_coupon='N',
                             superposed_coupon='N'):

        self.perform_actions(
            AMOUNT, amount,
            HIDE_KEYBOARD
        )

        if not points == 'N':
            self.perform_actions(
                USE_POINTS,
            )
            usable_points = self.get_text("//UIASwitch")
            usable_points = '%.2f' % float(filter(lambda ch: ch in '0123456789.', usable_points))
            ASSERT_DICT.update({'usable_points': usable_points})

        if not nonsuperposed_coupon == 'N':
            self.perform_actions(
                USE_COUPON,
                "swipe_accId_//", COUPON_2_STOP, "U",
                COUPON_2,
                COUPON_CONFIRM,
            )

        if not superposed_coupon == 'N':
            self.perform_actions(
                USE_COUPON,
                "swipe_accId_//", COUPON_1_STOP, "U",
                COUPON_1,
                "swipe_accId_//",
                "swipe_xpathIOS_//UIATableCell/UIAStaticText[@label='满10减1所有产品可叠加' and @visible='true'][2]", "U",
                COUPON_1_2,
                COUPON_CONFIRM,
            )

        self.perform_actions(
            BUY_CONFIRM,
            BUY_CONTINUE,
            TRADE_PASSWORD, trade_password)

        page = huaxin_ui.ui_ios_xjb_3_0.trade_complete_page.TradeCompletePage(self.web_driver)

        return page
