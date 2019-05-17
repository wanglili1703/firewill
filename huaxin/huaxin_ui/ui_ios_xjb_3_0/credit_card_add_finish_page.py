# coding=utf-8
import time

import huaxin_ui
from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.credit_card_repay_page

BACK = "accId_UIAButton_返回"
TITLE = "accId_UIAStaticText_完成"
FINISH_ICON = "xpathIOS_UIAImage_/AppiumAUT/UIAApplication/UIAWindow/UIAImage"

ADD_CREDIT_CARD_DONE = "accId_UIAButton_(UIButton_确认)"

current_page = []


class CreditCardAddFinishPage(PageObject):
    def __init__(self, web_driver):
        super(CreditCardAddFinishPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    # 验证添加信用卡成功
    @robot_log
    def verify_action_credit_card_success(self):
        time.sleep(1)
        self.perform_actions(FINISH_ICON,
                             ADD_CREDIT_CARD_DONE)

        page = huaxin_ui.ui_ios_xjb_3_0.credit_card_repay_page.CreditCardRepayPage(self.web_driver)
        return page
