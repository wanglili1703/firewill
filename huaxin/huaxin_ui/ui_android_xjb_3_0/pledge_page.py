# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.pledge_repay_page
import huaxin_ui.ui_android_xjb_3_0.pledge_history_page
import huaxin_ui.ui_android_xjb_3_0.select_pledge_product_page
import re
from _common.global_config import ASSERT_DICT
from decimal import Decimal

SWIPE_BEGIN = "swipe_xpath_//"
# SWIPE_STOP = "swipe_xpath_//android.widget.TextView[@text='查看历史借款']"

PLEDGE_PRODUCT = "xpath_//android.widget.TextView[contains(@text,'%s')]"
# PLEDGE_HISTORY = "xpath_//android.widget.TextView[@text='查看历史借款']"
PLEDGE_HISTORY = "xpath_//android.widget.TextView[contains(@text,'历史借款')]"
PLEDGE_STOP = "swipe_xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_vip_pledge_footer_panel']"
PLEDGE_BUTTON = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_vip_pledge_footer_panel']"


class PledgePage(PageObject):
    def __init__(self, web_driver):
        super(PledgePage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('随心借', self.get_text('com.shhxzq.xjb:id/title_actionbar_orange', 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def go_to_pledge_repay_page(self, product_name):
        self.perform_actions(PLEDGE_PRODUCT % product_name)

        page = huaxin_ui.ui_android_xjb_3_0.pledge_repay_page.PledgeRepayPage(self.web_driver)
        return page

    @robot_log
    def go_to_pledge_history_page(self):
        # self.perform_actions(SWIPE_BEGIN, SWIPE_STOP, 'U')
        self.perform_actions(PLEDGE_HISTORY)

        page = huaxin_ui.ui_android_xjb_3_0.pledge_history_page.PledgeHistoryPage(self.web_driver)
        return page

    @robot_log
    def go_to_select_pledge_product_page(self):
        self.perform_actions(SWIPE_BEGIN, PLEDGE_STOP, 'U')
        self.perform_actions(PLEDGE_BUTTON)

        page = huaxin_ui.ui_android_xjb_3_0.select_pledge_product_page.SelectpledgeProductPage(self.web_driver)
        return page

    @robot_log
    def verify_pledge_details(self, product_name, pledge_amount):
        pledge_amount_text = self.get_text('com.shhxzq.xjb:id/tv_item_left_top_content', 'find_element_by_id')
        interest_text = self.get_text('com.shhxzq.xjb:id/tv_item_right_top_content', 'find_element_by_id')
        pledge_amount_actual = re.findall(r'(\d{1,3}(,\d{3})*.\d+)', pledge_amount_text)[0][0].replace(',', '')
        interest_actual = re.findall(r'(\d{1,3}(,\d{3})*.\d+)', interest_text)[0][0].replace(',', '')

        self.assert_values(product_name, self.get_text('com.shhxzq.xjb:id/tv_title_name', 'find_element_by_id'))
        self.assert_values(str(Decimal(float(pledge_amount)).quantize(Decimal('0.00'))), pledge_amount_actual)
        self.assert_values(ASSERT_DICT['interest'], interest_actual)

        page = self
        return page
