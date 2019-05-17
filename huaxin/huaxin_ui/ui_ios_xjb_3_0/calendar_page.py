# coding: utf-8
import huaxin_ui
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.home_page
import huaxin_ui.ui_ios_xjb_3_0.personal_event_setting_page
import datetime

LEFT_BUTTON = "accId_UIAButton_UIBarButtonItemLocationLeft"
SWIPE_STOP = "swipe_accId_更多个人事项设置"
MORE_SETTINGS = "accId_UIAButton_更多个人事项设置"
current_page = []


class CalendarPage(PageObject):
    def __init__(self, web_driver):
        super(CalendarPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def go_back_to_home_page(self):
        self.perform_actions(LEFT_BUTTON)

        page = huaxin_ui.ui_ios_xjb_3_0.home_page.HomePage(self.web_driver)
        return page

    @robot_log
    def verify_at_calendar_page(self):
        self.assert_values("理财日历", self.get_text("//UIAStaticText[@label='理财日历']"))

    @robot_log
    def go_to_personal_event_setting_page(self):
        self.perform_actions("swipe_accId_//", SWIPE_STOP, 'U')

        self.perform_actions(MORE_SETTINGS)

        page = huaxin_ui.ui_ios_xjb_3_0.personal_event_setting_page.PersonalEventSettingPage(self.web_driver)
        return page

    @robot_log
    def swipe_calendar(self):
        month = (datetime.datetime.now().month + 1) % 12
        if month == 0:
            month = 12
        self.perform_actions("swipe_accId_(14)", "swipe_accId_(%s 月)" % month, "L")
