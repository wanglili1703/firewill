# coding: utf-8
from _common.page_object import PageObject

IDENTIFIER = "xpath_//android.widget.TextView[@text='个人中心']"
INVITE_FRIEND = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/setting_item_inviter']"
SHARE_FRIEND = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/setting_item_share']"
SECURITY_CENTER = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/setting_item_secure']"
SETTINGS_BUTTON = "xpath_//android.widget.ImageButton[@resource-id='com.shhxzq.xjb:id/ibtn_actionbar_right']"

current_page = []


class PersonalCenterPage(PageObject):
    def __init__(self, web_driver):
        super(PersonalCenterPage, self).__init__(web_driver)
        self.elements_exist(*current_page)
