# coding=utf-8
from _common.page_object import PageObject

import huaxin_ui.ui_android_xjb_2_0.fund_page
import huaxin_ui.ui_android_xjb_2_0.fund_plan_page

from _common.xjb_decorator import robot_log

BUY_FUND = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_fund_purchase']"
BUY_AMOUNT = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/product_purchase_amt']"
BUY_CONFIRM = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/product_purchase_bt']"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"
BUY_DONE = "xpath_//android.widget.Button[@text='确认']"
CANCEL = "xpath_//android.widget.TextView[@text='取消']"
POINT_SWITCH="xpath_//android.widget.ToggleButton[@resource-id='com.shhxzq.xjb:id/tbtn_point_switch']"
COUPONS_INFO="xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_purchase_coupons_info']"
COUPONS="xpath_//android.widget.RelativeLayout[@clickable='true']//android.widget.TextView[@text='不可叠加使用']"
NONSUPERCOMPOSED_COUPON_SWIPE_STOP = "swipe_xpath_//android.widget.RelativeLayout[@clickable='true']//android.widget.TextView[@text='不可叠加使用']"
COUPONS_CONFIRM="xpath_//android.widget.TextView[@text='确认']"
SUPERPOSED_COUPON_1="xpath_//android.widget.RelativeLayout[@clickable='true']//android.widget.TextView[@text='可叠加使用']"
# SUPERPOSED_COUPON_2="xpath_//android.widget.ImageView/../../following-sibling::android.widget.FrameLayout/android.widget.RelativeLayout[@clickable='true']"
SUPERPOSED_COUPON_2="xpath_//android.widget.RelativeLayout[@clickable='true']/../following-sibling::android.widget.FrameLayout/android.widget.RelativeLayout[@clickable='true']"
COUPON_SWIPE_BEGAIN= "swipe_xpath_//"
NONSUPERCOMPOSED_COUPON_SWIPE_STOP = "swipe_xpath_//android.widget.RelativeLayout[@clickable='true']//android.widget.TextView[@text='不可叠加使用']"
SUPERCOMPOSED_COUPON_SWIPE_STOP = "swipe_xpath_//android.widget.RelativeLayout[@clickable='true']//android.widget.TextView[@text='可叠加使用']"
SUPERCOMPOSED_COUPON_SWIPE_BEGAIN= "swipe_xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/img_coupons_item_select']"
SUPERCOMPOSED_COUPON_SWIPE_STOP_1 = "swipe_xpath_//android.widget.ImageView/../../following-sibling::android.widget.FrameLayout/android.widget.RelativeLayout[@clickable='true']"

FUND_PLAN_BUTTON="xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_fund_plan_detail']"

current_page = []


class FundPageFundDetail(PageObject):
    def __init__(self, web_driver):
        super(FundPageFundDetail, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def buy_fund_product(self, amount, trade_password,points='N',nonsuperposed_coupon='N',superposed_coupon='N'):

        self.perform_actions(
            BUY_FUND,
            BUY_AMOUNT, amount)

        if points=='Y':
            self.perform_actions(POINT_SWITCH)

        if nonsuperposed_coupon == 'Y':
            self.perform_actions(COUPONS_INFO,
                                 COUPON_SWIPE_BEGAIN, NONSUPERCOMPOSED_COUPON_SWIPE_STOP, 'U',
                                 COUPONS,
                                 COUPONS_CONFIRM)

        if superposed_coupon == 'Y':
            self.perform_actions(COUPONS_INFO,
                                 COUPON_SWIPE_BEGAIN, SUPERCOMPOSED_COUPON_SWIPE_STOP, 'U',
                                 SUPERPOSED_COUPON_1,
                                 SUPERCOMPOSED_COUPON_SWIPE_BEGAIN, SUPERCOMPOSED_COUPON_SWIPE_STOP_1, 'U',
                                 SUPERPOSED_COUPON_2,
                                 COUPONS_CONFIRM)

        self.perform_actions(
            BUY_CONFIRM,
            TRADE_PASSWORD, trade_password,
            BUY_DONE
        )

        page = huaxin_ui.ui_android_xjb_2_0.fund_page.FundPage(self.web_driver)

        return page


    @robot_log
    def go_to_fund_plan_page(self):
        self.perform_actions(FUND_PLAN_BUTTON)

        page = huaxin_ui.ui_android_xjb_2_0.fund_plan_page.FundPlanPage(self.web_driver)

        return page