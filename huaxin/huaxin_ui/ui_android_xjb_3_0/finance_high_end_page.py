# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.finance_high_end_cash_management_page
import huaxin_ui.ui_android_xjb_3_0.finance_high_end_fixed_rate_page
import huaxin_ui.ui_android_xjb_3_0.finance_high_end_best_recommend_page
import huaxin_ui.ui_android_xjb_3_0.finance_product_search_page
import huaxin_ui.ui_android_xjb_3_0.product_detail_page
import huaxin_ui.ui_android_xjb_3_0.assets_page
import huaxin_ui.ui_android_xjb_3_0.financing_product_introduction_page
import time

HIGH_END_START = "swipe_xpath_//android.widget.TextView[@text='高端']"
HIGH_END_PRODUCT_STOP = "swipe_xpath_//android.widget.TextView[@text='%s']"
HIGH_END_PRODUCT = "xpath_//android.widget.TextView[@text='%s']"

BUY_NOW = "xpath_//android.widget.Button[@text='立即购买']"
# AMOUNT = "xpath_//android.widget.EditText[@text='请输入购买金额']"
AMOUNT = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/product_purchase_amt']"
POINT_SWITCH = "xpath_//android.widget.ToggleButton[@resource-id='com.shhxzq.xjb:id/tbtn_point_switch']"
BUY_CONFIRM = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/product_purchase_bt']"

TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"

BUY_DONE = "xpath_//android.widget.Button[@text='确认']"

COUPONS_INFO = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_purchase_coupons_info']"
COUPONS = "xpath_//android.widget.RelativeLayout[@clickable='true']//android.widget.TextView[@text='不可叠加使用']"
COUPONS_CONFIRM = "xpath_//android.widget.TextView[@text='确认']"
SUPERPOSED_COUPON_1 = "xpath_//android.widget.RelativeLayout[@clickable='true']//android.widget.TextView[@text='可叠加使用']"
# SUPERPOSED_COUPON_2="xpath_//android.widget.ImageView/../../following-sibling::android.widget.FrameLayout/android.widget.RelativeLayout[@clickable='true']"
SUPERPOSED_COUPON_2 = "xpath_//android.widget.RelativeLayout[@clickable='true']/../following-sibling::android.widget.FrameLayout/android.widget.RelativeLayout[@clickable='true']"
COUPON_SWIPE_BEGAIN = "swipe_xpath_//"
NONSUPERCOMPOSED_COUPON_SWIPE_STOP = "swipe_xpath_//android.widget.RelativeLayout[@clickable='true']//android.widget.TextView[@text='不可叠加使用']"
SUPERCOMPOSED_COUPON_SWIPE_BEGAIN = "swipe_xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/img_coupons_item_select']"
SUPERCOMPOSED_COUPON_SWIPE_STOP = "swipe_xpath_//android.widget.RelativeLayout[@clickable='true']//android.widget.TextView[@text='可叠加使用']"
SUPERCOMPOSED_COUPON_SWIPE_STOP_1 = "swipe_xpath_//android.widget.ImageView/../../following-sibling::android.widget.FrameLayout/android.widget.RelativeLayout[@clickable='true']"
INPUT_FUND_PRODUCT = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/cet_search_tile']"
VIPPRODUCT_NAME = "xpath_//android.widget.TextView[contains(@text,'%s')]"
# COMFIRM_BUTTON_SWIPE_START="swipe_xpath_//"
# COMFIRM_BUTTON_SWIPE_STOP="swipe_xpath_//scroll_1"
ASSETS = "xpath_//android.widget.RelativeLayout[5]/android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/tab_image']"
# ASSETS = "xpath_//android.widget.RelativeLayout[4]/android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/tab_image']"
HIGH_END_DETAIL = "xpath_//android.widget.TextView[@text='高端']"
VIP_SWIPE_BEGIN = "swipe_xpath_//"
VIP_SWIPE_STOP = "swipe_xpath_//android.widget.TextView[@text='购买金额']"
VIP_PRODUCT = "xpath_//android.widget.TextView[@text='购买金额']"
CANCEL_BUTTON = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/button1']"

COMFIRM_BUTTON_SWIPE_BENGIN = "swipe_xpath_//"
COMFIRM_BUTTON_SWIPE_STOP = "swipe_xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/product_purchase_bt']"
KEEP_OBTAINING_POINTS = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/button2']"
LEFT_BUTTON = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left']"
PAYMENT_TYPE = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/payment_type_arrow']"
SWIPE_BEGIN = "swipe_xpath_//"
CASH_MANAGEMENT_PRODUCT_SWIPE_STOP = "swipe_xpath_//android.widget.TextView[contains(@text,'%s')]"
CASH_MANAGEMENT_PRODUCT = "xpath_//android.widget.TextView[contains(@text,'%s')]"
CASH_MANAGEMENT_SERIES = "xpath_//android.widget.TextView[@text='现金管理系列']"
FIXED_RATE_PRODUCT = "xpath_//android.widget.TextView[@text='固定收益系列']"
BEST_RECOMMEND_PRODUCT = "xpath_//android.widget.TextView[@text='精选系列']"
SERIES_SWIPE_STOP = "swipe_xpath_//android.widget.TextView[@text='%s']"
SEARCH = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/iv_to_finproduct_search']"
MORE_INTRODUCTION = "axis_Android_更多介绍_0,0.062"

current_page = []


class FinanceHighEndPage(PageObject):
    def __init__(self, web_driver):
        super(FinanceHighEndPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_page_title(self):
        self.assert_values('高端理财(100万起)', self.get_text('com.shhxzq.xjb:id/tv_product_name', 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def buy_high_end_product(self, product_name, amount, trade_password, cash_management_product=None, points='N',
                             nonsuperposed_coupon='N', superposed_coupon='N', source='1', cash_management='N'):
        self.perform_actions(
            HIGH_END_START, HIGH_END_PRODUCT_STOP % product_name, 'U',
                            HIGH_END_PRODUCT % product_name,
            # INPUT_FUND_PRODUCT, product_name,
            # VIPPRODUCT_NAME % product_name,
        )

        if self.element_exist("//android.widget.Button[@text='已售磬']"):
            page = self
            return page

        self.perform_actions(BUY_NOW)

        time.sleep(5)

        self.perform_actions(AMOUNT, amount)

        if cash_management == 'Y':
            self.perform_actions(PAYMENT_TYPE,
                                 SWIPE_BEGIN, CASH_MANAGEMENT_PRODUCT_SWIPE_STOP % cash_management_product, 'U')
            if cash_management_product == 'UI作为支付手段异常测试':
                self.assert_values('余额不足',
                                   self.get_text('com.shhxzq.xjb:id/not_sufficient_prompt', 'find_element_by_id'))
                page = self

                return page
            else:
                self.perform_actions(CASH_MANAGEMENT_PRODUCT % cash_management_product)

        if points == 'Y':
            self.perform_actions(POINT_SWITCH)
            time.sleep(5)
            # for i in range(0,3):
            #     if self.element_exist("//android.widget.Button[@resource-id='com.shhxzq.xjb:id/button2']"):
            #         self.perform_actions(KEEP_OBTAINING_POINTS)

        if nonsuperposed_coupon == 'Y':
            self.perform_actions(COUPONS_INFO)

            time.sleep(10)

            self.perform_actions(COUPON_SWIPE_BEGAIN, NONSUPERCOMPOSED_COUPON_SWIPE_STOP, 'U',
                                 COUPONS,
                                 COUPONS_CONFIRM)

        if superposed_coupon == 'Y':
            self.perform_actions(COUPONS_INFO)

            time.sleep(10)
            self.perform_actions(COUPON_SWIPE_BEGAIN, SUPERCOMPOSED_COUPON_SWIPE_STOP, 'U',
                                 SUPERPOSED_COUPON_1,
                                 SUPERCOMPOSED_COUPON_SWIPE_BEGAIN, SUPERCOMPOSED_COUPON_SWIPE_STOP_1, 'U',
                                 SUPERPOSED_COUPON_2,
                                 COUPONS_CONFIRM)

        self.perform_actions(COMFIRM_BUTTON_SWIPE_BENGIN, COMFIRM_BUTTON_SWIPE_STOP, 'U',
                             BUY_CONFIRM,
                             )

        if float(amount) >= 1 and float(amount) < 5000000:
            self.perform_actions(TRADE_PASSWORD, trade_password)
            self.assert_values('完成', self.get_text(self.page_title, 'find_element_by_id'))
            self.perform_actions(BUY_DONE)

            if source == '1':
                self.perform_actions(ASSETS)

            self.perform_actions(HIGH_END_DETAIL,
                                 VIP_SWIPE_BEGIN, VIP_SWIPE_STOP, 'U',
                                 VIP_PRODUCT)
            time.sleep(2)
            self.assert_values('%.2f' % float(amount), self.get_text('com.shhxzq.xjb:id/content', 'find_element_by_id'))

        elif float(amount) > 100000000:
            self.perform_actions(CANCEL_BUTTON)
            self.assert_values('买入', self.get_text('com.shhxzq.xjb:id/title_actionbar', 'find_element_by_id'))

        else:
            self.assert_values('买入', self.get_text('com.shhxzq.xjb:id/title_actionbar', 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def go_back_to_my_coupon(self):
        self.perform_actions(LEFT_BUTTON)

        page = huaxin_ui.ui_android_xjb_3_0.my_coupons_list_page.MyCouponsListPage(self.web_driver)
        return page

    @robot_log
    def go_to_cash_management_series_page(self, series):
        self.perform_actions(SWIPE_BEGIN, SERIES_SWIPE_STOP % series, 'U')

        self.perform_actions(CASH_MANAGEMENT_SERIES)

        page = huaxin_ui.ui_android_xjb_3_0.finance_high_end_cash_management_page.FinanceHighEndCashManagementPage(
            self.web_driver)

        return page

    @robot_log
    def go_to_fixed_rate_series(self, series):
        self.perform_actions(SWIPE_BEGIN, SERIES_SWIPE_STOP % series, 'U')

        self.perform_actions(FIXED_RATE_PRODUCT)

        page = huaxin_ui.ui_android_xjb_3_0.finance_high_end_fixed_rate_page.FinanceHighEndFixedRatePage(
            self.web_driver)

        return page

    @robot_log
    def go_to_best_recommend_series(self, series):
        self.perform_actions(SWIPE_BEGIN, SERIES_SWIPE_STOP % series, 'U')

        self.perform_actions(BEST_RECOMMEND_PRODUCT)

        page = huaxin_ui.ui_android_xjb_3_0.finance_high_end_best_recommend_page.FinanceHighEndBestRecommendPage(
            self.web_driver)

        return page

    @robot_log
    def go_to_finance_product_search_page(self):
        self.perform_actions(SEARCH)

        page = huaxin_ui.ui_android_xjb_3_0.finance_product_search_page.FinanceProductSearchPage(
            self.web_driver)

        return page

    @robot_log
    def go_to_product_detail_page(self, product_name):
        self.perform_actions(HIGH_END_START, HIGH_END_PRODUCT_STOP % product_name, 'U',
                             HIGH_END_PRODUCT % product_name, )

        page = huaxin_ui.ui_android_xjb_3_0.product_detail_page.ProductDetailPage(
            self.web_driver)

        return page

    @robot_log
    def go_to_assets_page(self):
        self.perform_actions(ASSETS)

        page = huaxin_ui.ui_android_xjb_3_0.assets_page.AssetsPage(self.web_driver)

        return page

    @robot_log
    def go_to_high_end_product_introduction_page(self):
        self.perform_actions(MORE_INTRODUCTION)

        page = huaxin_ui.ui_android_xjb_3_0.financing_product_introduction_page.FinancingProductIntroductionPage(
            self.web_driver)

        return page

