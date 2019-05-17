# coding: utf-8
import time

from _common.global_config import ASSERT_DICT
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.trade_complete_page
import huaxin_ui.ui_ios_xjb_3_0.finance_high_end_cash_management_page
import huaxin_ui.ui_ios_xjb_3_0.finance_high_end_fixed_rate_page
import huaxin_ui.ui_ios_xjb_3_0.finance_high_end_best_recommend_page
import huaxin_ui.ui_ios_xjb_3_0.product_detail_page
from _tools.mysql_xjb_tools import MysqlXjbTools

HIGH_END_START = "swipe_xpath_//"
HIGH_END_PRODUCT_STOP = "swipe_accId_%s"
HIGH_END_PRODUCT = "accId_UIAStaticText_%s"

BUY_NOW = "accId_UIAButton_立即购买[POP]"
BUY_NOW_2 = "accId_UIAButton_追加购买[POP]"
BUY_NOW_3 = "accId_UIAButton_立即抢购[POP]"
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

FIXED_RATE_PRODUCT = "xpathIOS_UIAStaticText_//UIAStaticText[@label='华睿尊享系列']"
CASH_MANAGEMENT_PRODUCT = "xpathIOS_UIAStaticText_//UIAStaticText[@label='现金管理系列']"
BEST_RECOMMEND_PRODUCT = "xpathIOS_UIAStaticText_//UIAStaticText[@label='精选系列']"

SEARCH_PRODUCT = "accId_UIAButton_UIBarButtonItemLocationRight"
SEARCH_INPUT = "accId_UIASearchBar_产品名称/简拼"
PRODUCT_NAME = "accId_UIAStaticText_%s"
MOBILE_CODE = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField"
VERIFY_CODE_CONFIRM = "accId_UIAButton_(UIButton_确认)"

current_page = []


class FinanceHighEndPage(PageObject):
    def __init__(self, web_driver):
        super(FinanceHighEndPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_at_high_end_page(self):
        self.assert_values("高端理财(100万起)", self.get_text("//UIAStaticText[@name='(高端理财(100万起))']"))

    @robot_log
    def go_to_cash_management_series(self):
        self.perform_actions(CASH_MANAGEMENT_PRODUCT)

        page = huaxin_ui.ui_ios_xjb_3_0.finance_high_end_cash_management_page.FinanceHighEndCashManagementPage(
            self.web_driver)

        return page

    @robot_log
    def go_to_fixed_rate_series(self):
        self.perform_actions(FIXED_RATE_PRODUCT)

        page = huaxin_ui.ui_ios_xjb_3_0.finance_high_end_fixed_rate_page.FinanceHighEndFixedRatePage(
            self.web_driver)

        return page

    @robot_log
    def go_to_best_recommend_series(self):
        self.perform_actions(BEST_RECOMMEND_PRODUCT)

        page = huaxin_ui.ui_ios_xjb_3_0.finance_high_end_best_recommend_page.FinanceHighEndBestRecommendPage(
            self.web_driver)

        return page

    # 高端理财搜索功能
    @robot_log
    def finance_product_search(self, product_name):
        self.perform_actions(
            SEARCH_PRODUCT,
            SEARCH_INPUT, product_name,
            PRODUCT_NAME % product_name,
        )

        page = huaxin_ui.ui_ios_xjb_3_0.product_detail_page.ProductDetailPage(self.web_driver)
        return page

    @robot_log
    def buy_high_end_product(self, product_name, amount, trade_password, points='N', nonsuperposed_coupon='N',
                             superposed_coupon='N', mobile=None):

        if self.element_exist(u'已售罄', 'find_element_by_accessibility_id'):
            page = self

            return page

        self.perform_actions(
            HIGH_END_START, HIGH_END_PRODUCT_STOP % product_name, 'U',
                            HIGH_END_PRODUCT % product_name,
            BUY_NOW,
            BUY_NOW_2,
            BUY_NOW_3
        )

        # 当出现购买产品风险高于用户的风险测评结果, 就会出现风险提示, 有些还需要验证码输入.
        if self.element_exist(u'风险提示', 'find_element_by_accessibility_id'):
            self.perform_actions(BUY_CONTINUE, )

        title = self.get_text("//UIAStaticText[@label='买入']")
        self.assert_values('买入', title)

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

            # amount_new = float(amount) - float(ASSERT_DICT['usable_points'])

            # label = self.get_text('(btnNext)', 'find_element_by_accessibility_id')
            # self.assert_values('¥', label)
            # self.perform_actions('assert_IOS_(btnNext)[@label=¥]')
            # self.perform_actions('assert_IOS_(btnNext)[@label=确认买入]')
            # self.perform_actions('assert_IOS_(btnNext)[@label==%.2f]' % float(amount_new))

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
                COUPON_1_STOP,
                "swipe_xpathIOS_//UIATableCell/UIAStaticText[@label='满10减1所有产品可叠加' and @visible='true'][2]", "U",
                COUPON_1_2,
                COUPON_CONFIRM,
            )

        self.perform_actions(
            BUY_CONFIRM)

        if self.element_exist(u'风险提示', 'find_element_by_accessibility_id'):
            self.perform_actions(BUY_CONTINUE, )
            verify_code = MysqlXjbTools().get_sms_verify_code(mobile=mobile, template_id='as_risk_not_match')

            self.perform_actions(
                MOBILE_CODE, verify_code,
                VERIFY_CODE_CONFIRM,
            )

        self.perform_actions(
            TRADE_PASSWORD, trade_password)

        page = huaxin_ui.ui_ios_xjb_3_0.trade_complete_page.TradeCompletePage(self.web_driver)

        return page
