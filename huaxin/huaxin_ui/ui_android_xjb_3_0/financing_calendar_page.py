# coding=utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.personal_matters_setting_page
import huaxin_ui.ui_android_xjb_3_0.home_page
import time

SWIPE_BEGIN = "swipe_xpath_//"
YEAR_SWIPE_BEGIN = "swipe_xpath_//android.view.View[@resource-id='com.shhxzq.xjb:id/year']"
MONTH_SWIPE_BEGIN = "swipe_xpath_//android.view.View[@resource-id='com.shhxzq.xjb:id/month']"
CALENDAR_SWIPE_STOP = "swipe_xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_left_date_selector']/preceding-sibling::android.widget.TextView[@text='%s']"
MORE_PERSONAL_SETTINGS = "xpath_//android.widget.TextView[@text='更多个人事项设置']"
BACK = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left']"
DATA_SELECTOR = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_left_date_selector']"
YEAR = "xpath_//android.view.View[@resource-id='com.shhxzq.xjb:id/year']"
MONTH = "xpath_//android.view.View[@resource-id='com.shhxzq.xjb:id/month']"
SCROLL = "swipe_xpath_//scroll_1"
COMPLETE = "xpath_//android.widget.TextView[@text='完成']"
MORE_PERSONAL_SETTINGS_STOP = "swipe_xpath_//android.widget.TextView[@text='更多个人事项设置']"


class FinancingCalendarPage(PageObject):
    def __init__(self, web_driver):
        super(FinancingCalendarPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('理财日历', self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def go_to_personal_matters_setting_page(self):
        self.perform_actions(SWIPE_BEGIN, MORE_PERSONAL_SETTINGS_STOP, 'U')
        self.perform_actions(MORE_PERSONAL_SETTINGS)

        page = huaxin_ui.ui_android_xjb_3_0.personal_matters_setting_page.PersonalMattersSettingPage(self.web_driver)
        return page

    @robot_log
    def back_to_home_page(self):
        self.perform_actions(BACK)

        page = huaxin_ui.ui_android_xjb_3_0.home_page.HomePage(self.web_driver)
        return page

    @robot_log
    def swipe_calendar(self, month, swipe_direction):
        if swipe_direction == 'L':
            self.perform_actions(SWIPE_BEGIN, CALENDAR_SWIPE_STOP % month, 'L')
        else:
            self.perform_actions(SWIPE_BEGIN, CALENDAR_SWIPE_STOP % month, 'R')

        page = self
        return page

    @robot_log
    def select_calendar_date(self):
        self.perform_actions(DATA_SELECTOR)
        self.perform_actions(YEAR_SWIPE_BEGIN, SCROLL, 'U')
        time.sleep(3)
        self.perform_actions(COMPLETE)

        page = self
        return page

    @robot_log
    def verify_calender_date(self):
        self.assert_values('月  2018年', self.get_text('com.shhxzq.xjb:id/tv_left_date_selector', 'find_element_by_id'))
        self.assert_values('09', self.get_text('com.shhxzq.xjb:id/tv_left_date_month', 'find_element_by_id'))

        page = self
        return page
