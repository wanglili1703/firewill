# coding=utf-8
import huaxin_ui
from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.bank_card_management_page

BACK = "accId_UIAButton_返回"
TITLE = "accId_UIAStaticText_完成"
FINISH_ICON = "xpathIOS_UIAImage_/AppiumAUT/UIAApplication/UIAWindow/UIAImage"

ADD_DEBIT_CARD_DONE = "accId_UIAButton_(UIButton_确认)"
# 弹出来的选环境的框
CANCEL = "accId_UIACollectionCell_取消[POP]"

current_page = []


class DebitCardAddFinishPage(PageObject):
    def __init__(self, web_driver):
        super(DebitCardAddFinishPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    # 验证添加储蓄卡成功
    @robot_log
    def verify_action_debit_card_success(self):
        self.perform_actions(CANCEL,
                             FINISH_ICON,
                             ADD_DEBIT_CARD_DONE,
                             )

        page = huaxin_ui.ui_ios_xjb_3_0.bank_card_management_page.BankCardManagementPage(self.web_driver)
        return page
