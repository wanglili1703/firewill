# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log

current_page = []


class AssetsAssociatorCenterPage(PageObject):
    def __init__(self, web_driver):
        super(AssetsAssociatorCenterPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_page_title(self):
        self.assert_values('会员中心', self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def current_level_verify(self):
        expected_text = str(self.get_text('com.shhxzq.xjb:id/tv_member_lv', 'find_element_by_id'))
        actual = str(
            self.get_text('//android.widget.TextView[@resource-id=com.shhxzq.xjb:id/textView and @selected=\'true\']'))
        self.assert_values(expected_text, actual)
        # current_level = self.perform_actions("getV_Android_com.shhxzq.xjb:id/tv_member_lv[@text_]")
        # self.assert_by_multiple_attributes("assert_Android_com.shhxzq.xjb:id/textView[@selected='true'][@text=%s]" % current_level)
        # if self.element_exist("//android.widget.TextView[@selected='true' and @text=%s]" % current_level):
        #     self.perform_actions("assert_Android_com.shhxzq.xjb:id/textView[@selected='true'][@text=%s]" % current_level)
        # elif (associator_assets >= associator_rank_1) and (associator_assets < associator_rank_2):
        #     self.perform_actions("assert_Android_com.shhxzq.xjb:id/user_level[@text=%s]" % user_level_2)
        # elif (associator_assets >= associator_rank_2) and (associator_assets < associator_rank_3):
        #     self.perform_actions("assert_Android_com.shhxzq.xjb:id/user_level[@text=%s]" % user_level_3)
        # elif (associator_assets >= associator_rank_3) and (associator_assets < associator_rank_4):
        #     self.perform_actions("assert_Android_com.shhxzq.xjb:id/user_level[@text=%s]" % user_level_4)
        # elif associator_assets >= associator_rank_4:
        #     self.perform_actions("assert_Android_com.shhxzq.xjb:id/user_level[@text=%s]" % user_level_5)
