# coding: utf-8

from _common.page_object import PageObject
from  _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.fund_page_all_fund_page
import time

START_FUND_PLAN = "xpath_//android.widget.Image/./following-sibling::android.view.View[1]"
I_KNOW = "xpath_//android.widget.Button[@text='我知道了'][POP]"

class StartFundPlanPage(PageObject):
    def __init__(self, web_driver):
        super(StartFundPlanPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('基金定投开启须知', self.get_text('com.shhxzq.xjb:id/title_actionbar', 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def go_to_fund_page_all_fund_page(self):
        time.sleep(5)

        # if self.element_exist("//android.widget.Image[@resource-id='cunru']", "find_element_by_xpath", 20):
        # self.perform_actions(START_FUND_PLAN)
        self.click_screen_(x=0.53, y=0.96)

        page = huaxin_ui.ui_android_xjb_3_0.fund_page_all_fund_page.FundPageAllFundPage(self.web_driver)

        return page

