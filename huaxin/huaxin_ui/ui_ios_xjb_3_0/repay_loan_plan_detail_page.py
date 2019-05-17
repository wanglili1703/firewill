# coding:utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.make_repay_plan_page
import huaxin_ui.ui_ios_xjb_3_0.repay_loan_page
import huaxin_ui.ui_ios_xjb_3_0.trade_complete_page

PAUSE_BUTTON = "accId_UIAButton_暂停"
RESTART_BUTTON = "accId_UIAButton_启用"
MODIFY_BUTTON = "accId_UIAButton_修改"
DELETE_BUTTON = "accId_UIAButton_UIBarButtonItemLocationRight"
DELETE = "accId_UIAButton_删除"
MODIFY_BUTTON_OTHER_LOAN = "xpath_//android.widget.TextView[@text='修改']"
CONFIRM = "accId_UIAButton_确定"
TRADE_PASSWORD = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField"


class RepayLoanPlanDetailPage(PageObject):
    def __init__(self, web_driver):
        super(RepayLoanPlanDetailPage, self).__init__(web_driver)

    @robot_log
    def verify_at_repay_loan_detail_page(self, status=None):
        self.assert_values('还贷款详情', self.get_text("//UIAStaticText[@label='还贷款详情']"))
        if status is not None:
            self.assert_values(True, self.element_exist("//UIAStaticText[contains(@label, %s)]" % status), '==')

        page = self
        return page

    @robot_log
    def pause_repay_loan_plan(self, trade_password):
        self.perform_actions(PAUSE_BUTTON,
                             CONFIRM,
                             TRADE_PASSWORD, trade_password)

        page = huaxin_ui.ui_ios_xjb_3_0.trade_complete_page.TradeCompletePage(self.web_driver)
        return page

    @robot_log
    def restart_repay_loan_plan(self, trade_password):
        self.perform_actions(RESTART_BUTTON,
                             CONFIRM,
                             TRADE_PASSWORD, trade_password)

        page = huaxin_ui.ui_ios_xjb_3_0.trade_complete_page.TradeCompletePage(self.web_driver)
        return page

    @robot_log
    def go_to_modify_repay_loan_plan_page(self):
        self.perform_actions(MODIFY_BUTTON)

        page = huaxin_ui.ui_ios_xjb_3_0.make_repay_plan_page.MakeRepayPlanPage(self.web_driver)

        return page

    @robot_log
    def delete_repay_loan_plan(self, trade_password):
        self.perform_actions(DELETE_BUTTON,
                             DELETE,
                             CONFIRM)

        # self.assert_values('删除还贷款计划', self.get_text('//android.widget.TextView'))

        self.perform_actions(TRADE_PASSWORD, trade_password)

        page = huaxin_ui.ui_ios_xjb_3_0.trade_complete_page.TradeCompletePage(self.web_driver)

        return page
