# coding: utf-8
from _common.page_object import PageObject

from _common.xjb_decorator import robot_log

current_page = []


class InviteFriendPage(PageObject):
    def __init__(self, web_driver):
        super(InviteFriendPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_at_invite_friend_page(self):
        self.assert_values("推荐用户注册绑卡，", self.get_text("//UIAStaticText[contains(@name, '推荐用户注册绑卡')]"), "==")
