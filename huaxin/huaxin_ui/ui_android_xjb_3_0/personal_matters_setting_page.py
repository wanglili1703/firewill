# coding=utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.credit_card_repay_page
import huaxin_ui.ui_android_xjb_3_0.financing_calendar_page

SWIPE_BEGIN = "swipe_xpath_//"
CREDIT_CARD_REPAY_STOP = "swipe_xpath_//android.widget.TextView[@text='信用卡还款']"
CREDIT_CARD_REPAY = "xpath_//android.widget.TextView[@text='信用卡还款']"
BACK = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left']"


class PersonalMattersSettingPage(PageObject):
    def __init__(self, web_driver):
        super(PersonalMattersSettingPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('个人事项设置', self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def go_to_credit_card_repay_page(self, device_id=None):
        self.perform_actions(SWIPE_BEGIN, CREDIT_CARD_REPAY_STOP, 'U')

        self.perform_actions(CREDIT_CARD_REPAY)

        page = huaxin_ui.ui_android_xjb_3_0.credit_card_repay_page.CreditCardRepayPage(self.web_driver, device_id)
        return page

    @robot_log
    def back_to_financing_calender_page(self):
        self.perform_actions(BACK)

        page = huaxin_ui.ui_android_xjb_3_0.financing_calendar_page.FinancingCalendarPage(self.web_driver)
        return page

