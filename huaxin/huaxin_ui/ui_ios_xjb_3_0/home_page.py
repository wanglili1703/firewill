# coding=utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log, message_i_know_afterwards
from huaxin_ui.ui_ios_xjb_3_0.assets_page import AssetsPage
from huaxin_ui.ui_ios_xjb_3_0.finance_dqb_page import FinanceDqbPage
from huaxin_ui.ui_ios_xjb_3_0.finance_high_end_page import FinanceHighEndPage
import huaxin_ui.ui_ios_xjb_3_0.finance_page
from huaxin_ui.ui_ios_xjb_3_0.fund_page import FundPage
from huaxin_ui.ui_ios_xjb_3_0.fund_page_fund_detail import FundPageFundDetail
from huaxin_ui.ui_ios_xjb_3_0.login_page import LoginPage
from huaxin_ui.ui_ios_xjb_3_0.message_center import MessageCenterPage
from huaxin_ui.ui_ios_xjb_3_0.personal_center_page import PersonalCenterPage
from huaxin_ui.ui_ios_xjb_3_0.recharge_page import RechargePage
from huaxin_ui.ui_ios_xjb_3_0.withdraw_page import WithdrawPage
import huaxin_ui.ui_ios_xjb_3_0.fund_page_all_fund_page
import huaxin_ui.ui_ios_xjb_3_0.deposit_salary_page
import huaxin_ui.ui_ios_xjb_3_0.calendar_page
import huaxin_ui.ui_ios_xjb_3_0.trade_record_detail_page
import huaxin_ui.ui_ios_xjb_3_0.fund_plan_detail_page
import huaxin_ui.ui_ios_xjb_3_0.repay_loan_plan_detail_page
import huaxin_ui.ui_ios_xjb_3_0.salary_financing_plan_detail_page
import huaxin_ui.ui_ios_xjb_3_0.credit_card_repay_page

WITHDRAW = "accId_UIAButton_取出"
RECHARGE = "accId_UIAButton_存入"
DEPOSIT_SALARY = "accId_UIAButton_存工资"

LOGIN_REGISTER = "accId_UIAButton_(UIButton_登录 / 注册)[POP]"

PERSONAL_CENTER = "accId_UIAButton_UIBarButtonItemLocationLeft"

HOME = "accId_UIAButton_(UITabBarButton_item_0)"
FINANCE = "accId_UIAButton_(UITabBarButton_item_1)"
FUND = "accId_UIAButton_(UITabBarButton_item_2)"
STOCK = "accId_UIAButton_(UITabBarButton_item_3)"
ASSETS = "accId_UIAButton_(UITabBarButton_item_4)"

LOGIN_BUTTON = "accId_UIAButton_(UIButton_登录)"

ESSENCE_RECOMMEND = "swipe_accId_//"
ESSENCE_RECOMMEND_END = "swipe_accId_了解华信现金宝"

# MESSAGE_CENTER = "accId_UIAButton_navMessageCenter"
MESSAGE_CENTER = "accId_UIAButton_(UIButton_)"
SEARCH_CLICK = "accId_UIASearchBarCLICK_高端理财/定活宝/基金"
SEARCH_INPUT = "accId_UIASearchBar_高端理财/定活宝/基金"
PRODUCT_NAME = "accId_UIAStaticText_%s"

CANCEL = "accId_UIAButton_(UIButton_取消)"
CALENDAR = "accId_UIAButton_理财日历"

CALENDAR_REMINDER = "xpathIOS_UIAStaticText_//UIAStaticText[@label='理财日历']"
MORE_REMINDER = "accId_UIAButton_(UIButton_查看更多)"
SWIPE_STOP = "swipe_accId_(UIButton_查看更多)"

FIRST_EVENT_LOCATOR = "//UIATableCell[@name='(HXFinancialEventTableViewCell)'][1]/UIAStaticText[2]"
FIRST_EVENT = "xpathIOS_UIAStaticText_%s"

current_page = []


class HomePage(PageObject):
    def __init__(self, web_driver):
        super(HomePage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    def verify_at_home_page(self):
        self.assert_values(True, self.element_exist('(UIButton_存入)', 'find_element_by_accessibility_id'), '==')

    @robot_log
    def go_to_personal_center_page(self):
        self.perform_actions(PERSONAL_CENTER)
        page = PersonalCenterPage(self.web_driver)

        return page

    @robot_log
    def go_to_login_page(self):
        self.perform_actions(
            LOGIN_REGISTER,
        )
        page = LoginPage(self.web_driver)

        return page

    @robot_log
    @message_i_know_afterwards
    def go_to_finance_page(self):
        self.perform_actions(FINANCE,
                             )
        self.assert_values('查看全部产品', self.get_text("(查看全部产品)", "find_element_by_accessibility_id"))
        page = huaxin_ui.ui_ios_xjb_3_0.finance_page.FinancePage(self.web_driver)

        return page

    @robot_log
    def go_to_fund_page(self):
        self.perform_actions(FUND)
        self.assert_values('基金代码/简拼/重仓资产', self.get_text('基金代码/简拼/重仓资产', 'find_element_by_accessibility_id'))

        page = FundPage(self.web_driver)

        return page

    @robot_log
    def go_to_assets_page(self):
        self.perform_actions(ASSETS)
        self.assert_values('我的', self.get_text("//UIAStaticText[@name='我的']"))

        page = AssetsPage(self.web_driver)

        return page

    @robot_log
    def go_to_recharge_page(self):
        self.perform_actions(RECHARGE)
        self.assert_values('存入现金宝', self.get_text("//UIAStaticText[@name='存入现金宝']"))

        page = RechargePage(self.web_driver)
        return page

    @robot_log
    def go_to_withdraw_page(self):
        self.perform_actions(WITHDRAW,
                             )
        self.assert_values('取出', self.get_text("//UIAStaticText[@label='取出']"))

        page = WithdrawPage(self.web_driver)
        return page

    @robot_log
    def go_to_message_center_page(self):
        self.perform_actions(MESSAGE_CENTER,
                             )
        self.assert_values('消息中心', self.get_text("//UIAStaticText[@label='消息中心']"))

        page = MessageCenterPage(self.web_driver)
        return page

    @robot_log
    # 高端理财/定活宝/基金 prd_tag=0,1,2
    def finance_product_search(self, product_name, product_code=None, prd_tag=None):
        page = None

        self.perform_actions(
            SEARCH_CLICK,
            SEARCH_INPUT, product_name
        )

        if prd_tag is None:
            return
        else:
            if not product_code is None:
                self.perform_actions(
                    PRODUCT_NAME % (product_name + product_code),
                )
            else:
                self.perform_actions(
                    PRODUCT_NAME % product_name,
                )

            if prd_tag == 0:
                page = FinanceHighEndPage(self.web_driver)

            elif prd_tag == 1:
                page = FinanceDqbPage(self.web_driver)

            elif prd_tag == 2:
                page = FundPageFundDetail(self.web_driver)

            return page

    @robot_log
    def cancel_search(self):
        self.perform_actions(CANCEL)

        page = self
        return page

    @robot_log
    def cancel_search_to_all_fund_page(self):
        self.perform_actions(CANCEL)

        page = huaxin_ui.ui_ios_xjb_3_0.fund_page_all_fund_page.FundPageAllFundPage(self.web_driver)
        return page

    @robot_log
    def go_to_login_page_(self):
        self.perform_actions(ASSETS,
                             )

        page = LoginPage(self.web_driver)

        return page

    @robot_log
    def view_essence_recommend_list(self):
        self.perform_actions(
            ESSENCE_RECOMMEND, ESSENCE_RECOMMEND_END, 'U',
        )

    @robot_log
    def verify_search_result(self, product_name, expected):
        self.assert_values(expected, str(product_name)[0:3] in self.get_text("//UIATableCell/UIAStaticText"))

    @robot_log
    def go_to_deposit_salary_page(self):
        self.perform_actions(DEPOSIT_SALARY)

        page = huaxin_ui.ui_ios_xjb_3_0.deposit_salary_page.DepositSalaryPage(self.web_driver)
        return page

    @robot_log
    def go_to_calendar_page(self):
        self.perform_actions(CALENDAR)
        page = huaxin_ui.ui_ios_xjb_3_0.calendar_page.CalendarPage(self.web_driver)
        return page

    @robot_log
    def go_to_calendar_page_by_clicking_calendar_activity(self):
        self.perform_actions("swipe_accId_//", SWIPE_STOP, "U")
        self.perform_actions(CALENDAR_REMINDER)

        page = huaxin_ui.ui_ios_xjb_3_0.calendar_page.CalendarPage(self.web_driver)
        return page

    @robot_log
    def go_to_calendar_page_by_clicking_more(self):
        self.perform_actions("swipe_accId_//", SWIPE_STOP, "U")
        self.perform_actions(MORE_REMINDER)

        page = huaxin_ui.ui_ios_xjb_3_0.calendar_page.CalendarPage(self.web_driver)
        return page

    @robot_log
    def view_calendar_event(self):
        page = None
        self.perform_actions("swipe_accId_//", SWIPE_STOP, "U")
        event_name = self.get_text(FIRST_EVENT_LOCATOR)

        self.perform_actions(FIRST_EVENT % FIRST_EVENT_LOCATOR)

        if str(event_name).__contains__('信用卡预约还款'):
            page = huaxin_ui.ui_ios_xjb_3_0.credit_card_repay_page.CreditCardRepayPage(self.web_driver)
            page.verify_at_credit_card_repay_page()

        elif str(event_name).__contains__('信用卡还款'):
            page = huaxin_ui.ui_ios_xjb_3_0.trade_record_detail_page.TradeRecordDetailPage(self.web_driver)
            page.verify_at_trade_record_detail_page()

        elif str(event_name).__contains__('基金定投'):
            page = huaxin_ui.ui_ios_xjb_3_0.fund_plan_detail_page.FundPlanDetailPage(self.web_driver)
            page.verify_page_title()

        elif str(event_name).__contains__('还贷款') or str(event_name).__contains__('还车贷') \
                or str(event_name).__contains__('还房贷'):
            page = huaxin_ui.ui_ios_xjb_3_0.repay_loan_plan_detail_page.RepayLoanPlanDetailPage(self.web_driver)
            page.verify_at_repay_loan_detail_page()

        elif str(event_name).__contains__('工资理财'):
            page = huaxin_ui.ui_ios_xjb_3_0.salary_financing_plan_detail_page.SalaryFinancingPlanDetailPage(
                self.web_driver)
            page.verify_at_salary_detail_title()

        return page
