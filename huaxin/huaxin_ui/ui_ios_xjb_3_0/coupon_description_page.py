# coding: utf-8
import huaxin_ui
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.my_coupons_list_page

LEFT_BUTTON = "accId_UIAButton_UIBarButtonItemLocationLeft"
current_page = []


class CouponDescriptionPage(PageObject):
    def __init__(self, web_driver):
        super(CouponDescriptionPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def go_back_to_my_coupon(self):
        self.perform_actions(LEFT_BUTTON)

        page = huaxin_ui.ui_ios_xjb_3_0.my_coupons_list_page.MyCouponsListPage(self.web_driver)
        return page

    @robot_log
    def verify_page_elements(self):
        self.assert_values("1、什么是现金宝优惠券?", self.get_text("//UIAStaticText[contains(@label, '现金宝优惠券')]"))
