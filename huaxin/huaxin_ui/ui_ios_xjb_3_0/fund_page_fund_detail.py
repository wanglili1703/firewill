# coding=utf-8
from _common.global_config import ASSERT_DICT
from _common.page_object import PageObject

import huaxin_ui.ui_ios_xjb_3_0.fund_page
import huaxin_ui.ui_ios_xjb_3_0.fund_plan_page
import huaxin_ui.ui_ios_xjb_3_0.trade_complete_page
import huaxin_ui.ui_ios_xjb_3_0.fund_selected_page
import huaxin_ui.ui_ios_xjb_3_0.home_page
from _common.xjb_decorator import robot_log
from _tools.mysql_xjb_tools import MysqlXjbTools

BUY_NOW = "accId_UIAButton_立即购买[POP]"
BUY_NOW_2 = "accId_UIAButton_追加购买[POP]"
BUY_NOW_3 = "accId_UIAButton_立即抢购[POP]"
BUY_NOW_4 = "accId_UIAButton_购买[POP]"
BUY_NOW_5 = "accId_UIAButton_1折费率购买[POP]"
BUY_AMOUNT = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIAScrollView/UIATextField"
# USE_POINTS = "axis_IOS_(integralSwitch)"
USE_POINTS = "xpathIOS_UIASwitch_//UIASwitch"
BUY_CONFIRM = "xpathIOS_UIAButton_//UIAButton[@name='(UIButton_确认)']"
# BUY_CONFIRM = "axis_IOS_(UIButton_确认)"
TRADE_PASSWORD = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField"
BUY_DONE = "accId_UIAButton_确认"
CANCEL = "accId_UIAButton_取消"

USE_COUPON = "axis_IOS_优惠券_0.5,0"
# COUPON_1 = "axis_IOS_满10减1所有产品可叠加"
# COUPON_1_STOP = "swipe_accId_满10减1所有产品可叠加"
COUPON_1 = "xpathIOS_UIAStaticText_//UIATableCell/UIAStaticText[@label='满10减1所有产品可叠加']"
COUPON_1_STOP = "swipe_accId_满10减1所有产品可叠加"

# COUPON_1_2 = "axis_IOS_满10减1所有产品可叠加[index]1"
# COUPON_2 = "axis_IOS_满10减1所有产品不可叠加"
COUPON_2_STOP = "swipe_accId_满10减1所有产品不可叠加"
COUPON_1_2 = "xpathIOS_UIAStaticText_//UIATableCell/UIAStaticText[@label='满10减1所有产品可叠加' and @visible='true'][2]"
COUPON_1_2_STOP = "swipe_xpathIOS_//UIATableCell/UIAStaticText[@label='满10减1所有产品可叠加' and @visible='true'][2]"
COUPON_2 = "xpathIOS_UIAStaticText_//UIATableCell/UIAStaticText[@label='满10减1所有产品不可叠加' and @visible='true']/./following-sibling::UIAStaticText[1]"

COUPON_CONFIRM = "accId_UIAButton_(UIButton_确定)"

FUND_PLAN_BUTTON = "axis_IOS_定投"
FUND_PLAN_BUTTON_START = "accId_UIAButton_开启定投[POP]"

HIDE_KEYBOARD = "accId_UIAButton_(UIButton_SafeKeyBoard_Hide)"
BACK = "accId_UIAButton_UIBarButtonItemLocationLeft"
FUND_SELECTED = "accId_UIAButton_自选"
FUND_SELECTED_DELETE = "accId_UIAButton_删自选"
VERIFY_CODE_CONFIRM = "accId_UIAButton_(UIButton_确认)"
BUY_CONTINUE = "accId_UIAButton_继续买入"
FIRST_BUY_INFO = "accId_UIAButton_(UIButton_确定)[POP]"
MOBILE_CODE = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField"

current_page = []


class FundPageFundDetail(PageObject):
    def __init__(self, web_driver):
        super(FundPageFundDetail, self).__init__(web_driver)
        self.elements_exist(*current_page)

        self._return_page = {
            'FundSelectedPage': huaxin_ui.ui_ios_xjb_3_0.fund_selected_page.FundSelectedPage(
                self.web_driver),
            'HomePage': huaxin_ui.ui_ios_xjb_3_0.home_page.HomePage(self.web_driver),
        }

    @robot_log
    def verify_at_fund_detail_page(self):
        self.assert_values("基金详情", self.get_text("//UIAStaticText[@label='基金详情']"))

    @robot_log
    def verify_money_fund_detail_page(self):
        self.assert_values(True, self.element_exist("//UIAButton[@label='七日年化收益率']"))
        self.assert_values(True, self.element_exist("//UIAButton[@label='万份收益']"))

    @robot_log
    def verify_equity_fund_detail_page(self):
        self.assert_values(True, self.element_exist("//UIAButton[contains(@name, '最大回撤')]"))

    @robot_log
    def verify_fund_name(self, product_name):
        self.assert_values(True, self.element_exist("//UIAStaticText[contains(@label, %s)]" % product_name))

    # 点击自选
    @robot_log
    def fund_selected_click(self):
        self.perform_actions(FUND_SELECTED)

        page = self
        return page

    # 点击删自选
    @robot_log
    def fund_selected_delete_click(self):
        self.perform_actions(FUND_SELECTED_DELETE)

        page = self
        return page

    @robot_log
    def back_to_home_page(self):
        self.perform_actions(BACK)

        page = huaxin_ui.ui_ios_xjb_3_0.home_page.HomePage(self.web_driver)
        return page

    @robot_log
    def back_to_previous_page(self, return_page):
        self.perform_actions(BACK)

        page = self._return_page[return_page]
        return page

    @robot_log
    def buy_fund_product(self, amount, mobile, trade_password, points='N', nonsuperposed_coupon='N',
                         superposed_coupon='N'):

        if self.element_exist(u'已售罄', 'find_element_by_accessibility_id'):
            page = self

            return page

        self.perform_actions(
            BUY_NOW,
            BUY_NOW_2,
            BUY_NOW_3,
            BUY_NOW_4,
            BUY_NOW_5,
        )

        # 当出现购买产品风险高于用户的风险测评结果, 就会出现风险提示, 有些还需要验证码输入.
        if self.element_exist(u'风险提示', 'find_element_by_accessibility_id'):
            self.perform_actions(
                BUY_CONTINUE,
            )

        self.perform_actions(
            BUY_AMOUNT, amount,
            HIDE_KEYBOARD
        )

        if not points == 'N':
            self.perform_actions(
                USE_POINTS,
            )

            usable_points = self.get_text("//UIAStaticText[contains(@label, '可用积分')]")
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
                COUPON_1_STOP, COUPON_1_2_STOP, "U",
                COUPON_1_2,
                COUPON_CONFIRM,
            )

        self.perform_actions(
            BUY_CONFIRM,
        )

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

    @robot_log
    def go_to_fund_plan_page(self):
        self.perform_actions(FUND_PLAN_BUTTON,
                             FUND_PLAN_BUTTON_START,
                             )

        # 当出现购买产品风险高于用户的风险测评结果, 就会出现风险提示, 有些还需要验证码输入.
        if self.element_exist(u'风险提示', 'find_element_by_accessibility_id'):
            self.perform_actions(
                BUY_CONTINUE,
            )

        page = huaxin_ui.ui_ios_xjb_3_0.fund_plan_page.FundPlanPage(self.web_driver)

        return page

    @robot_log
    def view_newly_raised_fund_details(self):
        self.assert_values('认购中', self.get_text('认购中', 'find_element_by_accessibility_id'))
        self.assert_values('距离认购期结束还剩',
                           self.get_text('距离认购期结束还剩', 'find_element_by_accessibility_id'))
        self.assert_values('天', self.get_text('天', 'find_element_by_accessibility_id'))
        self.assert_values('时', self.get_text('时', 'find_element_by_accessibility_id'))
        self.assert_values('分', self.get_text('分', 'find_element_by_accessibility_id'))
        self.assert_values('秒', self.get_text('秒', 'find_element_by_accessibility_id'))
        self.assert_values('认购期仅供参考，以基金公司公告为准。为避免基金认购提前结束，请及时购买。',
                           self.get_text('认购期仅供参考，以基金公司公告为准。为避免基金认购提前结束，请及时购买。', 'find_element_by_accessibility_id'))
        self.assert_values(True, self.element_exist("新基金认购流程：", "find_element_by_accessibility_id"))
        self.assert_values(True, self.element_exist("认购募集期", "find_element_by_accessibility_id"))
        self.assert_values(True, self.element_exist("验证备案", "find_element_by_accessibility_id"))
        self.assert_values(True, self.element_exist("封闭运作", "find_element_by_accessibility_id"))
        self.assert_values(True, self.element_exist("开放申购赎回", "find_element_by_accessibility_id"))
        self.assert_values(True, self.element_exist("概况", "find_element_by_accessibility_id"))
        self.assert_values(True, self.element_exist("费率", "find_element_by_accessibility_id"))
        self.assert_values(True, self.element_exist("公告", "find_element_by_accessibility_id"))

        page = self
        return page
