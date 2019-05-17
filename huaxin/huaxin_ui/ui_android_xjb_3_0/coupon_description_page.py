# coding: utf-8
import huaxin_ui
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log

LEFT_BUTTON = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left']"
VIEW = "xpath_//android.view.View"
current_page = []


class CouponDescriptionPage(PageObject):
    def __init__(self, web_driver):
        super(CouponDescriptionPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def go_back_to_my_coupon(self):
        self.perform_actions(LEFT_BUTTON)

        page = huaxin_ui.ui_android_xjb_3_0.my_coupons_list_page.MyCouponsListPage(self.web_driver)
        return page

    @robot_log
    def verify_page_elements(self):
        self.assert_values('优惠券说明', self.get_text('com.shhxzq.xjb:id/title_actionbar', 'find_element_by_id'))
        self.perform_actions(VIEW)