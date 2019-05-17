# coding: utf-8
import decimal

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
from _common.global_config import ASSERT_DICT
import time
import huaxin_ui.ui_ios_xjb_3_0.trade_complete_page
import huaxin_ui.ui_ios_xjb_3_0.high_end_holding_detail_page
import huaxin_ui.ui_ios_xjb_3_0.fund_holding_detail_page
import huaxin_ui.ui_ios_xjb_3_0.product_detail_page
from _tools.mysql_xjb_tools import MysqlXjbTools

AMOUNT_LOCATOR = "/AppiumAUT/UIAApplication/UIAWindow/UIATableView/UIATableCell/UIATextField"
FUND_BUY_AMOUNT = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIAScrollView/UIATextField"
AMOUNT = "xpathIOS_UIATextField_%s" % AMOUNT_LOCATOR
PAYMENT_TYPE = "accId_UIATableCell_(HXShowPaytypeCell)[POP]"
PAYMENT_TYPE_FUND = "accId_UIAStaticText_(华信现金宝)[POP]"
SWIPE_BEGIN = "swipe_accId_//"

USE_POINTS = "xpathIOS_UIASwitch_//UIASwitch"
USE_COUPON = "axis_IOS_优惠券_0.5,0"
COUPON_1 = "axis_IOS_满10减1所有产品可叠加"
COUPON_1_STOP = "swipe_accId_满10减1所有产品可叠加"
# COUPON_1_2 = "axis_IOS_满10减1所有产品可叠加[index]1"
COUPON_1_2 = "xpathIOS_UIAStaticText_//UIATableCell/UIAStaticText[@label='满10减1所有产品可叠加' and @visible='true'][2]"
COUPON_1_2_STOP = "swipe_xpathIOS_//UIATableCell/UIAStaticText[@label='满10减1所有产品可叠加' and @visible='true'][2]"
COUPON_2 = "accId_UIAStaticText_满10减1所有产品不可叠加"
COUPON_2_STOP = "swipe_accId_满10减1所有产品不可叠加"
# COUPON_CONFIRM = "axis_IOS_确定"
COUPON_CONFIRM = "accId_UIAButton_(UIButton_确定)"

BUY_CONFIRM = "accId_UIAButton_(UIButton_确认)"
BUY_CONFIRM_FUND = "xpathIOS_UIAButton_//UIAButton[@name='(UIButton_确认)']"
VERIFY_CODE_CONFIRM = "accId_UIAButton_(UIButton_确认)"
FIRST_BUY_INFO = "accId_UIAButton_(UIButton_确定)[POP]"
BUY_CONTINUE = "accId_UIAButton_继续买入[POP]"
BUY_CONSIDER = "accId_UIAButton_再考虑一下[POP]"

MOBILE_CODE = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField"
TRADE_PASSWORD = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField"

BUY_DONE = "accId_UIAButton_(confirmButton)[POP]"
POP_CONFIRM = "accId_UIAButton_(UIButton_确定)"
RETURN = "accId_UIAButton_返回"
PURCHASE_AMOUNT_TEXT = "accId_UIAStaticText_(买入金额)"
PAY_ACCOUNT = "accId_UIAStaticText_(华信现金宝)"
HIDE_KEYBOARD = "accId_UIAButton_(UIButton_SafeKeyBoard_Hide)"

CASH_MANAGEMENT_PRODUCT = "xpathIOS_UIAStaticText_//UIAStaticText[@label='%s']"

BACK = "accId_UIAButton_UIBarButtonItemLocationLeft"


class ProductPurchasePage(PageObject):
    def __init__(self, web_driver):
        super(ProductPurchasePage, self).__init__(web_driver)
        self._return_page = {
            "HighEndHoldingDetailPage": huaxin_ui.ui_ios_xjb_3_0.high_end_holding_detail_page.HighEndHoldingDetailPage(
                self.web_driver),
            "FundHoldingDetailPage": huaxin_ui.ui_ios_xjb_3_0.fund_holding_detail_page.FundHoldingDetailPage(
                self.web_driver),
            "ProductDetailPage": huaxin_ui.ui_ios_xjb_3_0.product_detail_page.ProductDetailPage(self.web_driver)

        }

    @robot_log
    def verify_at_product_purchase_page(self):
        self.assert_values('买入', self.get_text("//UIAStaticText[@label='买入']"))

        page = self
        return page

    @robot_log
    def back_to_previous_page(self, return_page):
        self.perform_actions(BACK)

        page = self._return_page[return_page]
        return page

    @robot_log
    def verify_purchase_amount(self, amount):
        self.assert_values("%s" % format(decimal.Decimal(amount), ','), self.get_text(AMOUNT_LOCATOR))

    @robot_log
    def verify_cash_management_left_amount(self, amount, cash_management_product):
        if self.element_exist('(HXShowPaytypeCell)', 'find_element_by_accessibility_id'):
            self.perform_actions(PAYMENT_TYPE)
        else:
            self.perform_actions(PAYMENT_TYPE_FUND)

        # 获取现金管理产品的余额
        left_amount = self.get_text(
            "//UIAStaticText[@label='%s']/following-sibling::UIAStaticText[1]" % cash_management_product)
        left_amount = '%.2f' % float(filter(lambda ch: ch in '0123456789.', left_amount))
        left_amount = (decimal.Decimal(left_amount) + decimal.Decimal(amount)).quantize(decimal.Decimal('0.00'))
        self.assert_values(decimal.Decimal(ASSERT_DICT['left_amount']), left_amount, "==")

    @robot_log
    def buy_finance_product(self, mobile, amount, trade_password, cash_management_product=None, points='N',
                            non_superposed_coupon=None, superposed_coupon=None, cash_management='N'):
        ASSERT_DICT.update({'success_flag': '0'})

        if self.element_exist(AMOUNT_LOCATOR):
            self.perform_actions(AMOUNT, amount)
        else:
            self.perform_actions(FUND_BUY_AMOUNT, amount)

        self.perform_actions(HIDE_KEYBOARD)

        if cash_management == 'Y':
            if self.element_exist('(HXShowPaytypeCell)', 'find_element_by_accessibility_id'):
                self.perform_actions(PAYMENT_TYPE)
            else:
                self.perform_actions(PAYMENT_TYPE_FUND)

            # 获取现金管理产品的余额
            left_amount = self.get_text(
                "//UIAStaticText[@label='%s']/following-sibling::UIAStaticText[1]" % cash_management_product)
            left_amount = '%.2f' % float(filter(lambda ch: ch in '0123456789.', left_amount))
            ASSERT_DICT.update({'left_amount': left_amount})
            self.perform_actions(CASH_MANAGEMENT_PRODUCT % cash_management_product)

        if points == 'Y':
            self.perform_actions(USE_POINTS)

            usable_points = self.get_text("//UIASwitch")
            usable_points = '%.2f' % float(filter(lambda ch: ch in '0123456789.', usable_points))
            ASSERT_DICT.update({'usable_points': usable_points})

        if non_superposed_coupon == 'Y':
            self.perform_actions(USE_COUPON)

            self.perform_actions(
                "swipe_accId_//", COUPON_2_STOP, "U",
                COUPON_2,
                COUPON_CONFIRM,
            )

        if superposed_coupon == 'Y':
            self.perform_actions(
                USE_COUPON,
                "swipe_accId_//", COUPON_1_STOP, "U",
                COUPON_1,
                COUPON_1_STOP, COUPON_1_2_STOP, "U",
                COUPON_1_2,
                COUPON_CONFIRM,
            )

        if self.element_exist("(UIButton_确认)", "find_element_by_accessibility_id"):
            self.perform_actions(BUY_CONFIRM)
        else:
            self.perform_actions(BUY_CONFIRM_FUND)

        if self.element_exist(u'您已经购买过定期宝产品，不能购买新手专享产品', 'find_element_by_accessibility_id'):
            self.perform_actions(
                POP_CONFIRM,
            )

            page = self
            return page

        # 当出现购买产品风险高于用户的风险测评结果, 就会出现风险提示, 有些还需要验证码输入.
        if self.element_exist(u'风险提示', 'find_element_by_accessibility_id'):
            self.perform_actions(
                BUY_CONTINUE,
            )

            if self.element_exist("(UIButton_确认)", "find_element_by_accessibility_id"):
                verify_code = MysqlXjbTools().get_sms_verify_code(mobile=mobile, template_id='as_risk_not_match')

                self.perform_actions(
                    MOBILE_CODE, verify_code,
                    VERIFY_CODE_CONFIRM,
                )

        self.perform_actions(
            TRADE_PASSWORD, trade_password,
            BUY_DONE,
        )

        if self.element_exist(u'UIButton_确定', 'find_element_by_accessibility_id'):
            self.perform_actions(
                FIRST_BUY_INFO,
            )

        page = huaxin_ui.ui_ios_xjb_3_0.trade_complete_page.TradeCompletePage(self.web_driver)
        return page
