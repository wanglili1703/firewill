# coding: utf-8
import time

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.binding_card_detail_page

SWIPE_BEGIN = "swipe_xpath_//"
INPUT_MANUALLY_STOP = "swipe_xpath_//android.widget.TextView[@text='手动输入身份信息']"
INPUT_MANUALLY = "xpath_//android.widget.TextView[@text='手动输入身份信息']"


class BindingCardInputIdInformationPage(PageObject):
    def __init__(self, web_driver, device_id=None):
        super(BindingCardInputIdInformationPage, self).__init__(web_driver, device_id)

    @robot_log
    def verify_page_title(self):
        self.assert_values('绑定银行卡', self.get_text('com.shhxzq.xjb:id/title_actionbar', 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def input_id_information_manually(self, device_id):
        self.perform_actions(SWIPE_BEGIN, INPUT_MANUALLY_STOP, 'U')
        self.perform_actions(INPUT_MANUALLY)

        page = huaxin_ui.ui_android_xjb_3_0.binding_card_detail_page.BindingCardDetailPage(self.web_driver, device_id)
        return page
