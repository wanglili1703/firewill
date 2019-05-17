# coding: utf-8
from _common.page_object import PageObject
import huaxin_ui.ui_android_xjb_3_0.home_page
import huaxin_ui.ui_android_xjb_3_0.product_purchase_page
# import huaxin_ui.ui_android_xjb_3_0.assets_page

from _common.xjb_decorator import robot_log

# from huaxin_ui.ui_android_xjb_3_0.personal_setting_page import PersonalSettingPage
# from huaxin_ui.ui_android_xjb_3_0.security_center_page import SecurityCenterPage

RESERVATION_CODE = "xpath_//android.widget.EditText[@text='请输入收到的预约码']"
RESERVATION_CODE_CONFIRM = "xpath_//android.widget.Button[@text='确定']"

USE_OTHER_RESERVATION_CODE = "xpath_//android.widget.TextView[@text='使用其他预约码']"
USE_RESERVATION_CODE = "xpath_//android.widget.TextView[@text='立即使用']"
USE_RESERVATION_CODE_COMFIRM = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/product_purchase_bt']"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"
USE_RESERVATION_CODE_COMPELETED = "xpath_//android.widget.Button[@text='确认']"

COMFIRM_BUTTON_SWIPE_BENGIN = "swipe_xpath_//"
COMFIRM_BUTTON_SWIPE_STOP = "swipe_xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/product_purchase_bt']"

current_page = []


class ReservationCodePage(PageObject):
    def __init__(self, web_driver):
        super(ReservationCodePage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_page_title(self):
        self.assert_values('预约码通道', self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

        # 使用其他预约码
        # @robot_log
        # def use_other_reservation_code(self, reserve_code, trade_password):
        #     self.perform_actions(
        #         USE_OTHER_RESERVATION_CODE,
        #         RESERVATION_CODE, reserve_code,
        #         RESERVATION_CODE_CONFIRM)
        #
        #     self.perform_actions(COMFIRM_BUTTON_SWIPE_BENGIN, COMFIRM_BUTTON_SWIPE_STOP, 'U')
        #
        #     self.perform_actions(USE_RESERVATION_CODE_COMFIRM,
        #                          TRADE_PASSWORD, trade_password,
        #                          USE_RESERVATION_CODE_COMPELETED
        #                          )

        # page = huaxin_ui.ui_android_xjb_3_0.assets_page.AssetsPage(self.web_driver)
        #
        # return page

    @robot_log
    def verify_reservation_code_details(self):
        self.assert_values('可用预约码', self.get_text('com.shhxzq.xjb:id/tv_header', 'find_element_by_id'))
        self.assert_values('产品预约码', self.get_text('com.shhxzq.xjb:id/tv_product_resere_code', 'find_element_by_id'))
        self.assert_values('产品名称', self.get_text('com.shhxzq.xjb:id/tv_product_resere_code_name', 'find_element_by_id'))
        self.assert_values('预约额度',
                           self.get_text('com.shhxzq.xjb:id/tv_product_resere_code_amount', 'find_element_by_id'))
        self.assert_values('有效期起',
                           self.get_text('com.shhxzq.xjb:id/tv_product_resere_code_start', 'find_element_by_id'))
        self.assert_values('有效期至', self.get_text('com.shhxzq.xjb:id/tv_product_resere_code_end', 'find_element_by_id'))
        self.assert_values('立即使用', self.get_text('com.shhxzq.xjb:id/reserve_code_btn', 'find_element_by_id'))

        page = self
        return page

    # 使用其他预约码
    @robot_log
    def use_other_reservation_code(self, reserve_code, have_reserve_code='no'):
        if have_reserve_code == 'yes':
            self.perform_actions(USE_OTHER_RESERVATION_CODE)
            self.assert_values('预约码通道', self.get_text(self.page_title, 'find_element_by_id'))

        self.perform_actions(RESERVATION_CODE, reserve_code,
                             RESERVATION_CODE_CONFIRM)

        page = huaxin_ui.ui_android_xjb_3_0.product_purchase_page.ProductPurchasePage(self.web_driver)
        return page

    # 使用自己的预约码
    @robot_log
    def use_reservation_code(self, trade_password):
        self.perform_actions(USE_RESERVATION_CODE)

        self.perform_actions(COMFIRM_BUTTON_SWIPE_BENGIN, COMFIRM_BUTTON_SWIPE_STOP, 'U')

        self.perform_actions(USE_RESERVATION_CODE_COMFIRM,
                             TRADE_PASSWORD, trade_password,
                             USE_RESERVATION_CODE_COMPELETED
                             )

        # page=huaxin_ui.ui_android_xjb_3_0.assets_page.AssetsPage(self.web_driver)
        #
        # return  page
