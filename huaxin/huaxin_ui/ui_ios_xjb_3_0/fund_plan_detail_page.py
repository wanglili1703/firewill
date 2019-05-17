# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.fund_plan_page
import huaxin_ui.ui_ios_xjb_3_0.my_fund_plan_page
import huaxin_ui.ui_ios_xjb_3_0.fund_page_fund_detail
import huaxin_ui.ui_ios_xjb_3_0.fund_history_plan_page
from _common.global_config import ASSERT_DICT

from _tools.mysql_xjb_tools import MysqlXjbTools

PAUSE = "accId_UIAButton_(UIButton_暂停)"
RESTART = "accId_UIAButton_(UIButton_恢复)"
STOP = "accId_UIAButton_(UIButton_终止)"
DELETE = "accId_UIAButton_(UIButton_删除)"
MODIFY = "accId_UIAButton_(UIButton_修改)"
CONFIRM = "accId_UIACollectionCell_确认"
TRADE_PASSWORD = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField"
AMOUNT_INVEST_PERIOD = '//UIAStaticText[@label=\'每期定投(元)\']/following-sibling::UIAStaticText'
PAY_WEEK_DAY = '//UIAStaticText[@label=\'扣款周期\']/following-sibling::UIAStaticText'
PAY_DATE = '//UIAStaticText[@label=\'扣款日期\']/following-sibling::UIAStaticText'
BUY_CONTINUE = "accId_UIAButton_继续买入"
FIRST_BUY_INFO = "accId_UIAButton_(UIButton_确定)[POP]"
MOBILE_CODE = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField"
BUY_DONE = "accId_UIAButton_确认"
VERIFY_CODE_CONFIRM = "accId_UIAButton_(UIButton_确认)"


class FundPlanDetailPage(PageObject):
    def __init__(self, web_driver):
        super(FundPlanDetailPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('定投详情', self.get_text("//UIAStaticText[@label='定投详情']"))

        page = self
        return page

    @robot_log
    def verify_fund_plan_status(self, status):
        # To do, web view could not be exposed to automation tool right now, comment it right now.
        # self.assert_values(status, self.get_text("(定投进行中)", "find_element_by_accessibility_id"))

        page = self

        return page

    @robot_log
    def pause_fund_plan(self, trade_password):
        self.perform_actions(PAUSE,
                             CONFIRM
                             )

        self.perform_actions(TRADE_PASSWORD, trade_password)

        page = self

        return page

    @robot_log
    def restart_fund_plan(self, trade_password, mobile):
        self.perform_actions(RESTART,
                             CONFIRM
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
        page = self

        return page

    @robot_log
    def stop_fund_plan(self, trade_password):
        self.perform_actions(STOP,
                             CONFIRM,
                             TRADE_PASSWORD, trade_password)

        page = huaxin_ui.ui_ios_xjb_3_0.my_fund_plan_page.MyFundPlanPage(self.web_driver)

        return page

    @robot_log
    def delete_fund_history_plan(self):
        self.perform_actions(DELETE,
                             CONFIRM)

        page = huaxin_ui.ui_ios_xjb_3_0.fund_history_plan_page.FundHistoryPlanPage(self.web_driver)

        return page

    @robot_log
    def go_to_make_fund_plan_page(self):
        self.perform_actions(MODIFY)

        page = huaxin_ui.ui_ios_xjb_3_0.fund_plan_page.FundPlanPage(self.web_driver)

        return page

    @robot_log
    def verify_fund_plan_details(self, amount):
        self.assert_values(amount, self.get_text(AMOUNT_INVEST_PERIOD))

        self.assert_values(ASSERT_DICT['purchase_cycle_week'], self.get_text(PAY_WEEK_DAY))
        self.assert_values(ASSERT_DICT['purchase_cycle_day'], self.get_text(PAY_DATE))

        page = self

        return page

    @robot_log
    def get_fund_plan_details(self):
        amount = self.get_text(AMOUNT_INVEST_PERIOD)
        ASSERT_DICT.update({'amount': amount})

        page = self

        return page

    @robot_log
    def go_to_fund_detail_page(self, product_name):
        self.perform_actions("accId_UIAStaticText_(%s)" % product_name)

        page = huaxin_ui.ui_ios_xjb_3_0.fund_page_fund_detail.FundPageFundDetail(self.web_driver)

        page.verify_at_fund_detail_page()

        return page
