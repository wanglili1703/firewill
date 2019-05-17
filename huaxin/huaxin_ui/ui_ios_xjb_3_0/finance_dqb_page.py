# coding: utf-8
from _common.global_config import ASSERT_DICT
from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
from _tools.mysql_xjb_tools import MysqlXjbTools
import huaxin_ui.ui_ios_xjb_3_0.trade_complete_page
import huaxin_ui.ui_ios_xjb_3_0.product_detail_page
import huaxin_ui.ui_ios_xjb_3_0.assets_page

REGULAR_START = "swipe_accId_定期"
REGULAR_PRODUCT_STOP = "swipe_accId_%s"
REGULAR_PRODUCT = "accId_UIAStaticText_%s"

# BUY_NOW = "accId_UIAButton_(depositImmediatelyButton)"
BUY_NOW = "accId_UIAButton_立即购买[POP]"
BUY_NOW_2 = "accId_UIAButton_追加购买[POP]"
BUY_NOW_3 = "accId_UIAButton_立即抢购[POP]"
# AMOUNT = "accId_UIATextField_(textField)请输入购买金额"
AMOUNT = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATableView/UIATableCell/UIATextField"
USE_POINTS = "xpathIOS_UIASwitch_//UIASwitch"
BUY_CONFIRM = "accId_UIAButton_(UIButton_确认)"
VERIFY_CODE_CONFIRM = "accId_UIAButton_(UIButton_确认)"
BUY_CONTINUE = "accId_UIAButton_继续买入"
FIRST_BUY_INFO = "accId_UIAButton_(UIButton_确定)[POP]"

DHB_PRODUCT = "accId_UIATableCell_(HXDHBTableViewCell)"

MOBILE_CODE = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField"
TRADE_PASSWORD = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField"
# TRADE_PASSWORD = "accId_UIATextField_(tradePwdBoxView)"

BUY_DONE = "accId_UIAButton_(confirmButton)[POP]"
POP_CONFIRM = "accId_UIAButton_(UIButton_确定)"
PURCHASE_AMOUNT_TEXT = "accId_UIAStaticText_(买入金额)"
PAY_ACCOUNT = "accId_UIAStaticText_(华信现金宝)"

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
HIDE_KEYBOARD = "accId_UIAButton_(UIButton_SafeKeyBoard_Hide)"
SEARCH_PRODUCT = "accId_UIAButton_UIBarButtonItemLocationRight"
SEARCH_INPUT = "accId_UIASearchBar_产品名称/简拼"
PRODUCT_NAME = "accId_UIAStaticText_%s"
CANCEL = "accId_UIAButton_(UIButton_取消)"
ASSETS = "accId_UIAButton_(UITabBarButton_item_4)"

current_page = []


class FinanceDqbPage(PageObject):
    def __init__(self, web_driver):
        super(FinanceDqbPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_at_dhb_page(self):
        self.assert_values("定活宝(5万起)", self.get_text("//UIAStaticText[@name='(定活宝(5万起))']"))

    @robot_log
    def go_to_assets_page(self):
        self.perform_actions(ASSETS)
        self.assert_values('我的', self.get_text("//UIAStaticText[@name='我的']"))

        page = huaxin_ui.ui_ios_xjb_3_0.assets_page.AssetsPage(self.web_driver)

        return page

    # 定活宝搜索功能
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
    def cancel_search(self):
        self.perform_actions(CANCEL)

        page = self
        return page

    @robot_log
    def buy_dqb_product(self, product_name, amount, trade_password, mobile, points='N', nonsuperposed_coupon='N',
                        superposed_coupon='N'):
        # if not product_name is None:
        #     self.perform_actions(
        #         REGULAR_START, REGULAR_PRODUCT_STOP % product_name, 'U',
        #                        REGULAR_PRODUCT % product_name,
        #     )

        # self.perform_actions(DHB_PRODUCT)

        # if self.element_exist(u'已售罄', 'find_element_by_accessibility_id'):
        #     page = self
        #
        #     return page

        self.perform_actions(
            BUY_NOW,
            BUY_NOW_2,
            BUY_NOW_3,
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
                USE_COUPON)

            self.perform_actions(
                "swipe_accId_//", COUPON_2_STOP, "U",
                COUPON_2,
                COUPON_CONFIRM,
            )

        if not superposed_coupon == 'N':
            self.perform_actions(
                USE_COUPON,
                "swipe_accId_//", COUPON_1_STOP, "U",
                COUPON_1,
                COUPON_1_STOP, COUPON_1_2_STOP, "U",
                COUPON_1_2,
                COUPON_CONFIRM,
            )

        self.perform_actions(
            BUY_CONFIRM,
        )

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

            verify_code = MysqlXjbTools().get_sms_verify_code(mobile=mobile, template_id='as_risk_not_match')

            self.perform_actions(
                MOBILE_CODE, verify_code,
                VERIFY_CODE_CONFIRM,
                TRADE_PASSWORD, trade_password,
            )

        else:
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
