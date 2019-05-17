# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.binding_card_page

USER_NM = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATableView/UIATableCell/UIATextField"
ID_TYPE = "accId_UIATableCell_(HXBindCardStepTwoIDTypeCell)"
SWIPE_BEGIN = "swipe_accId_//"
SCROLL = "swipe_accId_scroll_%s"
FINISH = "accId_UIAButton_完成"
ID_NO = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATableView/UIATableCell[3]/UIATextField"
NEXT = "accId_UIAButton_下一步"

current_page = []


class IdInputPage(PageObject):
    def __init__(self, web_driver):
        super(IdInputPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def input_user_id_info(self, user_name, id_type, id_number):
        self.perform_actions(USER_NM, user_name,
                             ID_TYPE)

        if str(id_type) == '身份证':
            self.perform_actions(FINISH)
        elif str(id_type) == '港澳通行证':
            self.perform_actions(SWIPE_BEGIN, SCROLL % 1, 'U',
                                 FINISH)
        elif str(id_type) == '台湾通行证':
            self.perform_actions(SWIPE_BEGIN, SCROLL % 2, 'U',
                                 FINISH)
        elif str(id_type) == '外国人居留证':
            self.perform_actions(SWIPE_BEGIN, SCROLL % 3, 'U',
                                 FINISH)

        self.perform_actions(ID_NO, id_number,
                             NEXT)

        page = huaxin_ui.ui_ios_xjb_3_0.binding_card_page.BindingCardPage(self.web_driver)
        return page
