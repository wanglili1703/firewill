# coding=utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log

RECENT_ONE_WEEK = "xpath_//android.widget.TextView[@text='%s']"
SWIPE_BEGIN = "swipe_xpath_//android.view.View[@resource-id='com.shhxzq.xjb:id/lv_filter']"
SCROLL = "swipe_xpath_//scroll_1"
COMPLETE = "xpath_//android.widget.TextView[@text='完成']"
BEST_TURNOVER = "xpath_//android.widget.CheckBox[@resource-id='com.shhxzq.xjb:id/dccb_center_titlebar']"


class FundBestPerformanceFundPage(PageObject):
    def __init__(self, web_driver):
        super(FundBestPerformanceFundPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self, title):
        self.assert_values(title, self.get_text('com.shhxzq.xjb:id/dccb_center_titlebar', 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def verify_page_details(self):
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='基金名称']"))
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='涨跌幅']"))
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='1']"))

        page = self
        return page

    @robot_log
    def view_best_performance_funds(self, period):
        self.perform_actions(RECENT_ONE_WEEK % period)
        page = self
        return page

    @robot_log
    def view_best_turnover_funds(self):
        self.perform_actions(BEST_TURNOVER,
                             SWIPE_BEGIN, SCROLL, 'U',
                             COMPLETE)
        page = self
        return page
