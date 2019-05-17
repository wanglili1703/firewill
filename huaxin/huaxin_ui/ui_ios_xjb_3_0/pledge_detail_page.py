# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.pledge_product_select_page
import huaxin_ui.ui_ios_xjb_3_0.trade_complete_page

current_page = []

PLEDGE_AMOUNT = "xpathIOS_UIATextField_//UIATextField[@value='不超过最高可借金额']"
PLEDGE_SUBMIT = "accId_UIAButton_(UIButton_提交申请)"
TRADE_PASSWORD = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField"
PLEDGE_DONE = "accId_UIAButton_(UIButton_确认)"
PRODUCT_NAME = "accId_UIAStaticText_(%s)"
SCROLL_1 = "swipe_accId_scroll_1"
CONFIRM = "accId_UIAButton_确定"
CONSUME_TYPE = "accId_UIAStaticText_(个人或家庭消费)"
PLEDGE_PRODUCT = "accId_UIAStaticText_(%s)"


class PledgeDetailPage(PageObject):
    def __init__(self, web_driver):
        super(PledgeDetailPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_at_pledge_borrow_page(self):
        self.assert_values("随心借", self.get_text("//UIAStaticText[@label='随心借']"))

    @robot_log
    def pledge_detail(self, pledge_amount, trade_password):
        self.perform_actions(PLEDGE_AMOUNT, pledge_amount,
                             CONSUME_TYPE,
                             "swipe_xpath_//", SCROLL_1, "U",
                             CONFIRM,
                             PLEDGE_SUBMIT,
                             TRADE_PASSWORD, trade_password,
                             )

        page = huaxin_ui.ui_ios_xjb_3_0.trade_complete_page.TradeCompletePage(self.web_driver)
        return page

    @robot_log
    def go_to_select_pledge_product_page(self, product_name):
        self.perform_actions(PRODUCT_NAME % product_name)

        page = huaxin_ui.ui_ios_xjb_3_0.pledge_product_select_page.PledgeProductSelectPage(self.web_driver)
        return page
