# coding=utf-8
import huaxin_ui.ui_ios_xjb_3_0.useroperation_succeed_page
from _common.global_config import ASSERT_DICT
from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
from _tools.mysql_xjb_tools import MysqlXjbTools

AMOUNT = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIAScrollView/UIATextField"
PAY_WEEK = "//UIAStaticText[@label='扣款周期']/following-sibling::UIAStaticText[1]"
PURCHASE_CYCLE_WEEK_LIST = "xpathIOS_UIAStaticText_%s" % PAY_WEEK
DONE = "accId_UIAButton_完成"
PAY_DATE = "//UIAStaticText[@label='扣款日期']/following-sibling::UIAStaticText[1]"
PURCHASE_CYCLE_DAY_LIST = "xpathIOS_UIAStaticText_%s" % PAY_DATE

PURCHASE_COMFIRM = "accId_UIAButton_确认"
TRADE_PASSWORD = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField"
PURCHASE_DONE = "accId_UIAButton_确认"
START_FUND_PLAN = "accId_UIAButton_开启定投"
SWIPE_BEGIN = "swipe_xpath_//"
SCROLL_1 = "swipe_accId_scroll_1"
COMFIRM_SWIPE_STOP = "swipe_xpath_//android.widget.Button[@text='确认']"
HIDE_KEYBOARD = "accId_UIAButton_(UIButton_SafeKeyBoard_Hide)"
VERIFY_CODE_CONFIRM = "accId_UIAButton_(UIButton_确认)"
BUY_CONTINUE = "accId_UIAButton_继续买入"
FIRST_BUY_INFO = "accId_UIAButton_(UIButton_确定)[POP]"
MOBILE_CODE = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField"
BUY_DONE = "accId_UIAButton_确认"

current_page = []


class FundPlanPage(PageObject):
    def __init__(self, web_driver):
        super(FundPlanPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_page_title(self):
        self.assert_values('制定定投计划', self.get_text("//UIAStaticText[@label='制定定投计划']"))

    @robot_log
    def verify_at_my_fund_plan_list_page(self):
        self.assert_values('我的定投计划', self.get_text("//UIAStaticText[@label='我的定投计划']"))

    # @robot_log
    # def fund_plan_detail(self, amount, trade_password):
    #     self.perform_actions(AMOUNT, amount,
    #                          PURCHASE_CYCLE_WEEK_LIST,
    #                          PURCHASE_CYCLE_WEEK,
    #                          PURCHASE_CYCLE_DAY_LIST,
    #                          PURCHASE_CYCLE_DAY,
    #                          PURCHASE_COMFIRM,
    #                          TRADE_PASSWORD, trade_password,
    #                          PURCHASE_DONE)
    #
    #     page = self
    #
    #     return page

    @robot_log
    def make_fund_plan(self, mobile, amount, trade_password, return_page=None):

        if return_page is None:
            if self.element_exist("//UIAStaticText[@label='我的定投计划']"):
                self.perform_actions(START_FUND_PLAN)

            self.perform_actions(AMOUNT, amount,
                                 HIDE_KEYBOARD,
                                 PURCHASE_CYCLE_WEEK_LIST,
                                 SWIPE_BEGIN, SCROLL_1, 'U',
                                 DONE,
                                 PURCHASE_CYCLE_DAY_LIST,
                                 SWIPE_BEGIN, SCROLL_1, 'U',
                                 DONE)
        else:
            self.perform_actions(AMOUNT, amount,
                                 HIDE_KEYBOARD,
                                 PURCHASE_CYCLE_WEEK_LIST,
                                 SWIPE_BEGIN, SCROLL_1, 'U',
                                 DONE,
                                 PURCHASE_CYCLE_DAY_LIST,
                                 SWIPE_BEGIN, SCROLL_1, 'U',
                                 DONE, )

        purchase_cycle_week = self.get_text(PAY_WEEK)
        purchase_cycle_day = self.get_text(PAY_DATE)

        ASSERT_DICT.update({'purchase_cycle_week': purchase_cycle_week,
                            'purchase_cycle_day': purchase_cycle_day})

        self.perform_actions("swipe_accId_//", "swipe_accId_确认", 'U',
                             PURCHASE_COMFIRM
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
                # BUY_DONE,
            )

            if self.element_exist(u'UIButton_确定', 'find_element_by_accessibility_id'):
                self.perform_actions(
                    FIRST_BUY_INFO,
                )

        page = huaxin_ui.ui_ios_xjb_3_0.useroperation_succeed_page.UserOperationSucceedPage(self.web_driver)

        return page
