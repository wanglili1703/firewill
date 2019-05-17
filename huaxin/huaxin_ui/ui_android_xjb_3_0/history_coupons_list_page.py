# coding: utf-8
import huaxin_ui
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log

LEFT_BUTTON = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left']"
USED_IMAGE = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/img_my_coupons_item_overdue']"
current_page = []


class HistoryCouponsListPage(PageObject):
    def __init__(self, web_driver):
        super(HistoryCouponsListPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def go_back_to_my_coupon(self):
        self.perform_actions(LEFT_BUTTON)

        page = huaxin_ui.ui_android_xjb_3_0.my_coupons_list_page.MyCouponsListPage(self.web_driver)
        return page

    @robot_log
    def verify_page_title(self):
        self.assert_values('历史优惠券', self.get_text('com.shhxzq.xjb:id/title_actionbar', 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def verify_used_coupon_icon(self):
        self.perform_actions(USED_IMAGE)

    @robot_log
    def verify_empty_coupon_record(self):
        self.assert_values('暂无任何记录', self.get_text('com.shhxzq.xjb:id/tv_empty_plan', 'find_element_by_id'))

        page = self
        return page
