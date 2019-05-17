# coding: utf-8

from _common.page_object import PageObject

from _common.xjb_decorator import robot_log

HIGH_END_START = "swipe_xpath_//android.widget.TextView[@text='高端']"
HIGH_END_PRODUCT_STOP = "swipe_xpath_//android.widget.TextView[@text='%s']"
HIGH_END_PRODUCT = "xpath_//android.widget.TextView[@text='%s']"

BUY_NOW = "xpath_//android.widget.Button[@text='立即购买']"
AMOUNT = "xpath_//android.widget.EditText[@text='请输入购买金额']"
POINT_SWITCH="xpath_//android.widget.ToggleButton[@resource-id='com.shhxzq.xjb:id/tbtn_point_switch']"
BUY_CONFIRM = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/product_purchase_bt']"

TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"

BUY_DONE = "xpath_//android.widget.Button[@text='确认']"

COUPONS_INFO="xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_purchase_coupons_info']"
COUPONS="xpath_//android.widget.RelativeLayout[@clickable='true']//android.widget.TextView[@text='不可叠加使用']"
COUPONS_CONFIRM="xpath_//android.widget.TextView[@text='确认']"
SUPERPOSED_COUPON_1="xpath_//android.widget.RelativeLayout[@clickable='true']//android.widget.TextView[@text='可叠加使用']"
# SUPERPOSED_COUPON_2="xpath_//android.widget.ImageView/../../following-sibling::android.widget.FrameLayout/android.widget.RelativeLayout[@clickable='true']"
SUPERPOSED_COUPON_2="xpath_//android.widget.RelativeLayout[@clickable='true']/../following-sibling::android.widget.FrameLayout/android.widget.RelativeLayout[@clickable='true']"
COUPON_SWIPE_BEGAIN= "swipe_xpath_//"
NONSUPERCOMPOSED_COUPON_SWIPE_STOP = "swipe_xpath_//android.widget.RelativeLayout[@clickable='true']//android.widget.TextView[@text='不可叠加使用']"
SUPERCOMPOSED_COUPON_SWIPE_BEGAIN= "swipe_xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/img_coupons_item_select']"
SUPERCOMPOSED_COUPON_SWIPE_STOP = "swipe_xpath_//android.widget.RelativeLayout[@clickable='true']//android.widget.TextView[@text='可叠加使用']"
SUPERCOMPOSED_COUPON_SWIPE_STOP_1 = "swipe_xpath_//android.widget.ImageView/../../following-sibling::android.widget.FrameLayout/android.widget.RelativeLayout[@clickable='true']"


current_page = []


class FinanceHighEndPage(PageObject):
    def __init__(self, web_driver):
        super(FinanceHighEndPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def buy_high_end_product(self, product_name, amount, trade_password,points='N',nonsuperposed_coupon='N',superposed_coupon='N'):
        self.perform_actions(
            HIGH_END_START, HIGH_END_PRODUCT_STOP % product_name, 'U',
            HIGH_END_PRODUCT % product_name,
            BUY_NOW,
            AMOUNT, amount)

        if points=='Y':
            self.perform_actions(POINT_SWITCH)

        if nonsuperposed_coupon == 'Y':
            self.perform_actions(COUPONS_INFO,
                                 COUPON_SWIPE_BEGAIN,NONSUPERCOMPOSED_COUPON_SWIPE_STOP,'U',
                                 COUPONS,
                                 COUPONS_CONFIRM)

        if superposed_coupon == 'Y':
            self.perform_actions(COUPONS_INFO,
                                 COUPON_SWIPE_BEGAIN, SUPERCOMPOSED_COUPON_SWIPE_STOP, 'U',
                                 SUPERPOSED_COUPON_1,
                                 SUPERCOMPOSED_COUPON_SWIPE_BEGAIN,SUPERCOMPOSED_COUPON_SWIPE_STOP_1, 'U',
                                 SUPERPOSED_COUPON_2,
                                 COUPONS_CONFIRM)

        self.perform_actions(
                BUY_CONFIRM,
                TRADE_PASSWORD, trade_password,
                BUY_DONE)

        page = self

        return page
