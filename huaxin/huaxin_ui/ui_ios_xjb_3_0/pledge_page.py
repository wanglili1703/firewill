# coding: utf-8
import time

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.pledge_repay_page
import huaxin_ui.ui_ios_xjb_3_0.pledge_history_page
import huaxin_ui.ui_ios_xjb_3_0.pledge_product_select_page
import re
from _common.global_config import ASSERT_DICT
from decimal import Decimal

SWIPE_BEGIN = "swipe_xpath_//"
SWIPE_STOP = "swipe_accId_历史借款"

SWIPE_BEGAIN = "swipe_accId_//"
PLEDGE_STOP = "swipe_accId_随心借"

PLEDGE_PRODUCT = "xpathIOS_UIAStaticText_//UIAStaticText[@label='%s']"
PLEDGE_HISTORY = "xpathIOS_UIAButton_//UIAButton[contains(@label, '历史借款')]"
PLEDGE_BUTTON = "axis_IOS_我要借款"


class PledgePage(PageObject):
    def __init__(self, web_driver):
        super(PledgePage, self).__init__(web_driver)

    @robot_log
    def verify_at_pledge_list_page(self):
        self.assert_values("随心借", self.get_text("//UIAStaticText[@label='随心借']"))

        page = self
        return page

    @robot_log
    def go_to_pledge_repay_page(self, product_name):
        self.perform_actions(PLEDGE_PRODUCT % product_name)

        page = huaxin_ui.ui_ios_xjb_3_0.pledge_repay_page.PledgeRepayPage(self.web_driver)
        return page

    @robot_log
    def go_to_pledge_history_page(self):
        # self.perform_actions(SWIPE_BEGIN, SWIPE_STOP, 'U')
        self.perform_actions(PLEDGE_HISTORY)

        page = huaxin_ui.ui_ios_xjb_3_0.pledge_history_page.PledgeHistoryPage(self.web_driver)
        return page

    @robot_log
    def go_to_select_pledge_product_page(self):
        self.perform_actions(PLEDGE_BUTTON)

        page = huaxin_ui.ui_ios_xjb_3_0.pledge_product_select_page.PledgeProductSelectPage(self.web_driver)
        return page

    @robot_log
    def verify_pledge_record(self, product_name, exist=True):
        time.sleep(1)
        self.assert_values(exist, self.element_exist("//UIAStaticText[@label='%s']" % product_name))

        page = self
        return page