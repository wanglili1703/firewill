# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.high_end_purchase_page
import huaxin_ui.ui_ios_xjb_3_0.history_coupons_list_page
import huaxin_ui.ui_ios_xjb_3_0.coupon_description_page
import huaxin_ui.ui_ios_xjb_3_0.assets_page
import huaxin_ui.ui_ios_xjb_3_0.welfare_center_page

TITLE = "//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/title_actionbar']"
DESC = "accId_UIAButton_(UIButton_说明)"
COUPON_HISTORY = "accId_UIAButton_查看历史优惠券"
COUPON_ALL_INFO = ""
COUPON_DETAIL = ""
COUPON_ITEM = ""
COUPON_USE = "xpathIOS_UIAButton_//UIAStaticText[@label='满10减1所有产品不可叠加'][1]/../UIAButton[1]"
BACK = "accId_UIAButton_UIBarButtonItemLocationLeft"
COUPON_STOP = "swipe_accId_满10减1所有产品不可叠加"
MORE_ACTIVITY = "axis_accId_查看更多活动"
BUY_CONTINUE = "accId_UIAButton_继续买入"
current_page = []


class MyCouponsListPage(PageObject):
    def __init__(self, web_driver):
        super(MyCouponsListPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def use_coupon_to_buy_page(self):
        self.perform_actions(
            "swipe_accId_//", COUPON_STOP, "U",
            COUPON_USE)

        # 当出现购买产品风险高于用户的风险测评结果, 就会出现风险提示, 有些还需要验证码输入.
        if self.element_exist(u'风险提示', 'find_element_by_accessibility_id'):
            self.perform_actions(
                BUY_CONTINUE,
            )

        page = huaxin_ui.ui_ios_xjb_3_0.high_end_purchase_page.HighEndPurchasePage(self.web_driver)
        return page

    @robot_log
    def go_to_history_page(self):
        self.perform_actions(COUPON_HISTORY)

        page = huaxin_ui.ui_ios_xjb_3_0.history_coupons_list_page.HistoryCouponsListPage(self.web_driver)
        return page

    @robot_log
    def go_to_coupon_description_page(self):
        self.perform_actions(DESC)

        page = huaxin_ui.ui_ios_xjb_3_0.coupon_description_page.CouponDescriptionPage(self.web_driver)
        return page

    @robot_log
    def verify_page_title(self):
        self.assert_values("我的优惠券", self.get_text("//UIAStaticText[@label='我的优惠券']"))

    @robot_log
    def verify_empty_coupon_record(self):
        self.assert_values(True, self.element_exist("//UIATableView[contains(@label, '暂无任何记录')]"))

        # self.perform_actions(MORE_ACTIVITY)

    @robot_log
    def go_back_to_assets_page(self):
        self.perform_actions(BACK)

        page = huaxin_ui.ui_ios_xjb_3_0.assets_page.AssetsPage(self.web_driver)

        return page

    @robot_log
    def verify_coupon_description(self, description):
        self.assert_values(description, self.get_text("//UIAStaticText[contains(@label,'%s')]" % description))

        page = self
        return page

    @robot_log
    def go_back_to_welfare_center_page(self):
        self.perform_actions(BACK,
                             BACK)

        page = huaxin_ui.ui_ios_xjb_3_0.welfare_center_page.WelfareCenterPage(self.web_driver)

        return page
