# coding: utf-8
import huaxin_ui
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.my_coupons_list_page

LEFT_BUTTON = "accId_UIAButton_UIBarButtonItemLocationLeft"
USED_IMAGE = "accId_UIAButton_(UIButton_)"
current_page = []


class HistoryCouponsListPage(PageObject):
    def __init__(self, web_driver):
        super(HistoryCouponsListPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def go_back_to_my_coupon(self):
        self.perform_actions(LEFT_BUTTON)

        page = huaxin_ui.ui_ios_xjb_3_0.my_coupons_list_page.MyCouponsListPage(self.web_driver)
        return page

    @robot_log
    def verify_page_title(self):
        self.assert_values("历史优惠券", self.get_text("//UIAStaticText[@label='历史优惠券']"))

        page = self
        return page

    @robot_log
    def verify_used_coupon_icon(self):
        self.perform_actions(USED_IMAGE)

        page = self
        return page

    @robot_log
    def verify_empty_coupon_record(self):
        self.assert_values("暂无任何记录", self.get_text("", "find_element_by_accessibility_id"))

        page = self
        return page
