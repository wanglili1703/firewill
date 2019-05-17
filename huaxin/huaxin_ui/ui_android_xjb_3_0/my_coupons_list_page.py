# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.finance_high_end_page
import huaxin_ui.ui_android_xjb_3_0.history_coupons_list_page
import huaxin_ui.ui_android_xjb_3_0.coupon_description_page
import huaxin_ui.ui_android_xjb_3_0.assets_page

DESC = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_actionbar_right']"
COUPON_HISTORY = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_footer_coupons']"
COUPON_ALL_INFO = "//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/rl_coupons_all']"
COUPON_DETAIL = "//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/rl_coupons_all']/RelativeLayout']"
COUPON_ITEM = "//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/csv_coupons_item']"
COUPON_USE = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_coupons_use']"
BACK = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left']"

current_page = []


class MyCouponsListPage(PageObject):
    def __init__(self, web_driver):
        super(MyCouponsListPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def use_coupon_to_buy_page(self):
        self.perform_actions(COUPON_USE)

        page = huaxin_ui.ui_android_xjb_3_0.finance_high_end_page.FinanceHighEndPage(self.web_driver)
        return page

    @robot_log
    def go_to_history_page(self):
        self.perform_actions(COUPON_HISTORY)

        page = huaxin_ui.ui_android_xjb_3_0.history_coupons_list_page.HistoryCouponsListPage(self.web_driver)
        return page

    @robot_log
    def go_to_coupon_description_page(self):
        self.perform_actions(DESC)

        page = huaxin_ui.ui_android_xjb_3_0.coupon_description_page.CouponDescriptionPage(self.web_driver)
        return page

    @robot_log
    def verify_page_title(self):
        self.assert_values('我的优惠券', self.get_text(self.page_title, 'find_element_by_id'))
        page = self
        return page

    @robot_log
    def verify_empty_coupon_record(self):
        empty_text = self.element_exist("//android.widget.TextView[contains(@text,'暂无任何记录')]")
        self.assert_values('True', str(empty_text))

        page = self
        return page

    @robot_log
    def go_back_to_assets_page(self):
        self.perform_actions(BACK)

        page = huaxin_ui.ui_android_xjb_3_0.assets_page.AssetsPage(self.web_driver)

        return page
