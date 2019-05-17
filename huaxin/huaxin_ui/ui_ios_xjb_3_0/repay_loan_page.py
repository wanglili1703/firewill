# coding: utf-8
import decimal

from _common.global_config import ASSERT_DICT
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.make_repay_plan_page
import huaxin_ui.ui_ios_xjb_3_0.repay_loan_plan_detail_page

MAKE_REPAY_PLAN = "xpathIOS_UIAButton_//UIAButton[@label='createplan btn']"
RESERVATION_CODE_CONFIRM = "accId_UIAButton_(btnNext)"
ADD_REPAY_PLAN = "accId_UIAButton_新增还款计划"
REPAY_HOUSING_LOAN = "accId_UIAStaticText_还房贷"
REPAY_CAR_LOAN = "accId_UIAStaticText_还车贷"
OTHER_LOAN = "accId_UIAStaticText_%s"


class RepayLoanPage(PageObject):
    def __init__(self, web_driver):
        super(RepayLoanPage, self).__init__(web_driver)

    @robot_log
    def go_to_make_repay_plan_page(self):
        if self.element_exist("(自动还贷)", 'find_element_by_accessibility_id'):
            self.perform_actions(MAKE_REPAY_PLAN)
        else:
            self.perform_actions(ADD_REPAY_PLAN)

        page = huaxin_ui.ui_ios_xjb_3_0.make_repay_plan_page.MakeRepayPlanPage(self.web_driver)
        page.verify_at_make_repay_loan_plan()
        return page

    @robot_log
    def verify_repay_loan(self, repay_type, repay_amount, last_no):
        if repay_type == 'housing_loan':
            self.assert_values('还房贷', self.get_text('还房贷', 'find_element_by_accessibility_id'))
        elif repay_type == 'car_loan':
            self.assert_values('还车贷', self.get_text('还车贷', 'find_element_by_accessibility_id'))
        else:
            self.assert_values(str("其他用途"), self.get_text('其他用途', 'find_element_by_accessibility_id'))

        repay_amount = decimal.Decimal(repay_amount).quantize(decimal.Decimal('0.00'))
        self.assert_values('%s 还贷 %s 元' % (str(ASSERT_DICT['repay_date']), str(repay_amount)),
                           self.get_text('%s 还贷 %s 元' % (str(ASSERT_DICT['repay_date']), str(repay_amount)),
                                         "find_element_by_accessibility_id"), '==')
        self.assert_values('至 工商银行(%s)' % last_no,
                           self.get_text('至 工商银行(%s)' % last_no, 'find_element_by_accessibility_id'), '==')

    @robot_log
    def go_to_repay_loan_plan_detail_page(self, repay_type=None, other_purpose=None):

        loans = self.web_driver.find_elements_by_xpath("//UIATableCell")
        ASSERT_DICT.update({
            "loan_count": len(loans)
        })

        if repay_type == 'housing_loan':
            self.perform_actions(REPAY_HOUSING_LOAN)

        elif repay_type == 'car_loan':
            self.perform_actions(REPAY_CAR_LOAN)

        else:
            self.perform_actions(OTHER_LOAN % other_purpose)

        page = huaxin_ui.ui_ios_xjb_3_0.repay_loan_plan_detail_page.RepayLoanPlanDetailPage(self.web_driver)
        return page

    @robot_log
    def verify_loan_count(self):
        loans = self.web_driver.find_elements_by_xpath("//UIATableCell")
        expected = int(ASSERT_DICT['loan_count']) - 1
        self.assert_values(expected, len(loans), '==')

        page = self
        return page

    @robot_log
    def verify_at_repay_loan_page(self):
        self.assert_values("还贷款", self.get_text("//UIAStaticText[@label='还贷款']"))

        page = self
        return page
