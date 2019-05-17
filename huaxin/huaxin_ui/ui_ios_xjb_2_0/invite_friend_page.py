# coding: utf-8
from _common.page_object import PageObject

from _common.xjb_decorator import robot_log


current_page = []


class InviteFriendPage(PageObject):
    def __init__(self, web_driver):
        super(InviteFriendPage, self).__init__(web_driver)
        self.elements_exist(*current_page)
