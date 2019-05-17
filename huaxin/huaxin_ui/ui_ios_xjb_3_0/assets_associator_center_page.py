# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log

V1 = "accId_UIAButton_新手会员"
V2 = "accId_UIAButton_白银会员"
V3 = "accId_UIAButton_黄金会员"
V4 = "accId_UIAButton_铂金会员"
V5 = "accId_UIAButton_钻石会员"
DESC = "accId_UIAButton_等级说明"

current_page = []


class AssetsAssociatorCenterPage(PageObject):
    def __init__(self, web_driver):
        super(AssetsAssociatorCenterPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def click_different_member_level(self):
        self.perform_actions(V1,
                             V2,
                             V3,
                             V4,
                             V5)
        self.assert_values(True, self.element_exist("会员中心", "find_element_by_accessibility_id"))

        page = self
        return page

    @robot_log
    def go_to_description_page(self):
        self.perform_actions(DESC)
        self.assert_values(True, self.element_exist("等级说明", "find_element_by_accessibility_id"))

        page = self
        return page
