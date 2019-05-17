# coding=utf-8
from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.welfare_center_page

TITLE_ELE = "//UIAStaticText[@label='全部']"
POINTS_DETAILS = "xpathIOS_UIAStaticText_//UIAStaticText[@label='积分明细']"
MY_YB = "accId_UIAStaticText_我的元宝"
BACK = "accId_UIAButton_UIBarButtonItemLocationLeft"
current_page = []

'''只有第一次进入的时候才会出现这个落地页面'''


class PointsYbDetailsPage(PageObject):
    def __init__(self, web_driver):
        super(PointsYbDetailsPage, self).__init__(web_driver)
        self.elements_exist(*current_page)
        self._return_page = {
            "WelfareCenterPage": huaxin_ui.ui_ios_xjb_3_0.welfare_center_page.WelfareCenterPage(self.web_driver)
        }

    @robot_log
    def verify_at_details_page_title(self):
        title = self.get_text(TITLE_ELE)
        self.assert_values('全部', title)

    @robot_log
    def verify_points_details(self):
        self.assert_values(True, self.element_exist("//UIAStaticText[contains(@label, '+')]"))

    @robot_log
    def verify_yb_details(self):
        self.assert_values(True, self.element_exist("//UIAStaticText[contains(@label, '+')]"))
        self.perform_actions(POINTS_DETAILS)
        self.verify_points_details()

    @robot_log
    def back_to_previous_page(self, return_page):
        self.perform_actions(BACK)

        page = self._return_page[return_page]
        return page
