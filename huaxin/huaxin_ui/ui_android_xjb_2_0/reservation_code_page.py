# coding: utf-8
from _common.page_object import PageObject
import huaxin_ui.ui_android_xjb_2_0.home_page

from _common.xjb_decorator import robot_log
from huaxin_ui.ui_android_xjb_2_0.personal_setting_page import PersonalSettingPage
from huaxin_ui.ui_android_xjb_2_0.security_center_page import SecurityCenterPage

RESERVATION_CODE = "xpath_//android.widget.EditText[@text='请输入收到的预约码']"
RESERVATION_CODE_CONFIRM = "xpath_//android.widget.Button[@text='确定']"

USE_OTHER_RESERVATION_CODE="xpath_//android.widget.TextView[@text='使用其他预约码'][POP]"
USE_RESERVATION_CODE="xpath_//android.widget.TextView[@text='立即使用']"
USE_RESERVATION_CODE_COMFIRM="xpath_//android.widget.Button[@text='¥ 1.00  确认买入']"
TRADE_PASSWORD="xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"
USE_RESERVATION_CODE_COMPELETED="xpath_//android.widget.Button[@text='确认']"

current_page = []


class ReservationCodePage(PageObject):
    def __init__(self, web_driver):
        super(ReservationCodePage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    # 使用其他预约码
    @robot_log
    def use_other_reservation_code(self, reserve_code,trade_password):
        self.perform_actions(
            USE_OTHER_RESERVATION_CODE,
            RESERVATION_CODE, reserve_code,
            RESERVATION_CODE_CONFIRM,
            USE_RESERVATION_CODE_COMFIRM,
            TRADE_PASSWORD, trade_password,
            USE_RESERVATION_CODE_COMPELETED
            )

        page = huaxin_ui.ui_android_xjb_2_0.home_page.HomePage(self.web_driver)

        return page

    # 使用自己的预约码
    @robot_log
    def use_reservation_code(self,trade_password):
        self.perform_actions(USE_RESERVATION_CODE,
                             USE_RESERVATION_CODE_COMFIRM,
                             TRADE_PASSWORD,trade_password,
                             USE_RESERVATION_CODE_COMPELETED
                             )

        page=huaxin_ui.ui_android_xjb_2_0.home_page.HomePage(self.web_driver)

        return  page
