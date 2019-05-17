# coding=utf-8
from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.welfare_center_page

TITLE_ELE = "//UIAStaticText[@label='福利中心']"
EXPERIENCE = "//UIAButton[@label='立即体验']"
current_page = []

'''只有第一次进入的时候才会出现这个落地页面'''


class WelfareCenterHomePage(PageObject):
    def __init__(self, web_driver):
        super(WelfareCenterHomePage, self).__init__(web_driver)
        self.elements_exist(*current_page)
        self._return_page = {
        }

    @robot_log
    def verify_at_welfare_center_page_home_title(self):
        title = self.get_text(TITLE_ELE)
        self.assert_values('福利中心', title)

    @robot_log
    def experience_immediately(self):
        self.verify_at_welfare_center_page_home_title()
        if self.element_exist(EXPERIENCE):
            self.perform_actions("xpathIOS_UIAButton_%s" % EXPERIENCE)

        page = huaxin_ui.ui_ios_xjb_3_0.welfare_center_page.WelfareCenterPage(self.web_driver)
        return page
