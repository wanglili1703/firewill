# coding: utf-8

from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
import time
import huaxin_ui.ui_android_xjb_3_0.finance_product_search_page
import huaxin_ui.ui_android_xjb_3_0.assets_page
import huaxin_ui.ui_android_xjb_3_0.dhb_history_product_page

REGULAR_START = "swipe_xpath_//android.widget.TextView[@text='定活宝']"
REGULAR_PRODUCT_STOP = "swipe_xpath_//android.widget.TextView[@text='%s']"
REGULAR_PRODUCT = "xpath_//android.widget.TextView[@text='%s']"

BUY_NOW = "xpath_//android.widget.Button[@text='立即购买']"
# AMOUNT = "xpath_//android.widget.EditText[@text='请输入购买金额']"
AMOUNT = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/product_purchase_amt']"
BUY_CONFIRM = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/product_purchase_bt']"

TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"
POINT_SWITCH = "xpath_//android.widget.ToggleButton[@resource-id='com.shhxzq.xjb:id/tbtn_point_switch']"
COUPONS_INFO = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_purchase_coupons_info']"
COUPONS = "xpath_//android.widget.RelativeLayout[@clickable='true']//android.widget.TextView[@text='不可叠加使用']"
COUPON_SWIPE_BEGAIN = "swipe_xpath_//"
NONSUPERCOMPOSED_COUPON_SWIPE_STOP = "swipe_xpath_//android.widget.RelativeLayout[@clickable='true']//android.widget.TextView[@text='不可叠加使用']"
SUPERCOMPOSED_COUPON_SWIPE_BEGAIN = "swipe_xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/img_coupons_item_select']"
SUPERCOMPOSED_COUPON_SWIPE_STOP = "swipe_xpath_//android.widget.RelativeLayout[@clickable='true']//android.widget.TextView[@text='可叠加使用']"
SUPERCOMPOSED_COUPON_SWIPE_STOP_1 = "swipe_xpath_//android.widget.ImageView/../../following-sibling::android.widget.FrameLayout/android.widget.RelativeLayout[@clickable='true']"
SUPERPOSED_COUPON_1 = "xpath_//android.widget.RelativeLayout[@clickable='true']//android.widget.TextView[@text='可叠加使用']"
# SUPERPOSED_COUPON_2="xpath_//android.widget.ImageView/../../following-sibling::android.widget.FrameLayout/android.widget.RelativeLayout[@clickable='true']"
SUPERPOSED_COUPON_2 = "xpath_//android.widget.RelativeLayout[@clickable='true']/../following-sibling::android.widget.FrameLayout/android.widget.RelativeLayout[@clickable='true']"

COUPONS_CONFIRM = "xpath_//android.widget.TextView[@text='确认']"

BUY_DONE = "xpath_//android.widget.Button[@text='确认']"
INPUT_FUND_PRODUCT = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/cet_search_tile']"
DQB_PRODUCT_NAME = "xpath_//android.widget.TextView[contains(@text,'%s')]"
# ASSETS = "xpath_//android.widget.RelativeLayout[4]/android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/tab_image']"
ASSETS = "xpath_//android.widget.RelativeLayout[5]/android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/tab_image']"
DQB = "xpath_//android.widget.TextView[@text='定活宝']"
DQB_SWIPE_BEGIN = "swipe_xpath_//"
DQB_SWIPE_STOP = "swipe_xpath_//android.widget.TextView[@text='购买金额']"
DQB_PRODUCT = "xpath_//android.widget.TextView[@text='购买金额']"
CANCEL_BUTTON = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/button1']"
MAX_CONFIRM = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/button2']"

COMFIRM_BUTTON_SWIPE_BENGIN = "swipe_xpath_//"
COMFIRM_BUTTON_SWIPE_STOP = "swipe_xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/product_purchase_bt']"
KEEP_OBTAINING_POINTS = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/button2']"
SEARCH = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/iv_to_finproduct_search']"
HISTORY_PRODUCT = "swipe_xpath_//android.widget.TextView[@text='查看历史产品']"
VIEW_HISTORY_PRODUCT = "xpath_//android.widget.TextView[@text='查看历史产品']"
current_page = []


class FinanceDqbPage(PageObject):
    def __init__(self, web_driver):
        super(FinanceDqbPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_page_title(self):
        self.assert_values('定活宝(5万起)', self.get_text('com.shhxzq.xjb:id/tv_product_name', 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def buy_dqb_product(self, product_name, amount, trade_password, points='N', nonsuperposed_coupon='N',
                        superposed_coupon='N'):
        self.perform_actions(INPUT_FUND_PRODUCT, product_name,
                             DQB_PRODUCT_NAME % product_name, )

        # if self.element_exist("//android.widget.Button[@resource-id='com.shhxzq.xjb:id/product_details_pruchase']"):
        #     page = self

        # else :
        self.perform_actions(
            # REGULAR_START, REGULAR_PRODUCT_STOP % product_name, 'U',
            # REGULAR_PRODUCT % product_name,
            # BUY_NOW,
            # AMOUNT, amount
            BUY_NOW)

        time.sleep(5)

        self.perform_actions(AMOUNT, amount)

        if points == 'Y':
            self.perform_actions(POINT_SWITCH)
            time.sleep(5)
            # for i in range(0, 3):
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

        self.perform_actions(COMFIRM_BUTTON_SWIPE_BENGIN, COMFIRM_BUTTON_SWIPE_STOP, 'U')

        self.perform_actions(BUY_CONFIRM)

        if float(amount) >= 1 and float(amount) < 50000:
            self.perform_actions(TRADE_PASSWORD, trade_password)
            self.assert_values('完成', self.get_text(self.page_title, 'find_element_by_id'))

            self.perform_actions(BUY_DONE)

            self.perform_actions(ASSETS,
                                 DQB,
                                 DQB_SWIPE_BEGIN, DQB_SWIPE_STOP, 'U',
                                 DQB_PRODUCT, )

            self.assert_values(float(amount),
                               float(self.get_text('com.shhxzq.xjb:id/purchase_amount', 'find_element_by_id')), '==')

        elif float(amount) >= 50000 and float(amount) <= 100000000:
            self.perform_actions(MAX_CONFIRM)
            self.assert_values('买入', self.get_text('com.shhxzq.xjb:id/title_actionbar', 'find_element_by_id'))

        elif float(amount) < 1:
            self.assert_values('买入', self.get_text('com.shhxzq.xjb:id/title_actionbar', 'find_element_by_id'))

        elif float(amount) > 100000000:
            self.perform_actions(CANCEL_BUTTON)
            self.assert_values('买入', self.get_text('com.shhxzq.xjb:id/title_actionbar', 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def go_to_finance_product_search_page(self):
        self.perform_actions(SEARCH)

        page = huaxin_ui.ui_android_xjb_3_0.finance_product_search_page.FinanceProductSearchPage(
            self.web_driver)

        return page

    @robot_log
    def go_to_assets_page(self):
        self.perform_actions(ASSETS)

        page = huaxin_ui.ui_android_xjb_3_0.assets_page.AssetsPage(self.web_driver)

        return page

    @robot_log
    def go_to_dhb_history_product_page(self):
        self.perform_actions(DQB_SWIPE_BEGIN, HISTORY_PRODUCT, 'U')

        self.perform_actions(VIEW_HISTORY_PRODUCT)

        page = huaxin_ui.ui_android_xjb_3_0.dhb_history_product_page.DhbHistoryProductPage(self.web_driver)

        return page
