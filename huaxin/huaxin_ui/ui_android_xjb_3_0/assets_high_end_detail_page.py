# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
from _common.global_config import ASSERT_DICT
import huaxin_ui.ui_android_xjb_3_0.trade_detail_page
import huaxin_ui.ui_android_xjb_3_0.high_end_redeem_page
import huaxin_ui.ui_android_xjb_3_0.finance_high_end_page
import huaxin_ui.ui_android_xjb_3_0.assets_analysis_page
import huaxin_ui.ui_android_xjb_3_0.product_detail_page
import huaxin_ui.ui_android_xjb_3_0.high_end_supplementary_purchase_page
import huaxin_ui.ui_android_xjb_3_0.description_page
import huaxin_ui.ui_android_xjb_3_0.history_holding_page
import huaxin_ui.ui_android_xjb_3_0.assets_page
import huaxin_ui.ui_android_xjb_3_0.expiry_processing_type_page

TRADE_DETAIL = "xpath_//android.widget.Button[@text='交易记录']"
HIGH_END_MORE_PRODUCT = "xpath_//android.widget.TextView[@text='查看更多产品']"
HIGH_END_MORE_PRODUCT_STOP = "swipe_xpath_//android.widget.TextView[@text='查看更多产品']"

HIGH_END_START = "swipe_xpath_//android.widget.TextView[@text='高端']"
HISTORY_PRODUCT_STOP = "swipe_xpath_//android.widget.TextView[@text='查看历史产品']"
HISTORY_PRODUCT = "xpath_//android.widget.TextView[@text='查看历史产品']"

TITLE_START = "swipe_xpath_//android.widget.TextView[@text='高端理财']"
# HIGH_END_PRODUCT_STOP = "swipe_xpath_//android.widget.TextView[@text='%s']"
# HIGH_END_PRODUCT_STOP = "swipe_xpath_//android.widget.TextView[@text='%s']/../../following-sibling::android.widget.LinearLayout[1]//android.widget.TextView[@text='持有金额']"
HIGH_END_PRODUCT_STOP = "swipe_xpath_//android.widget.TextView[@text='%s']/../../following-sibling::android.widget.RelativeLayout[1]//android.widget.TextView[@text='持有金额']"
# HIGH_END_PRODUCT = "xpath_//android.widget.TextView[@text='%s']"
# HIGH_END_PRODUCT = "xpath_//android.widget.TextView[@text='%s']/../../following-sibling::android.widget.LinearLayout[1]//android.widget.TextView[@text='持有金额']"
HIGH_END_PRODUCT = "xpath_//android.widget.TextView[@text='%s']/../../following-sibling::android.widget.RelativeLayout[1]//android.widget.TextView[@text='持有金额']"
HIGH_END_PRODUCT_OVERLAPPED = "//android.widget.TextView[@text='%s']/../../following-sibling::android.widget.RelativeLayout[1]//android.widget.TextView[@text='持有金额']"
REDEEM = "xpath_//android.widget.Button[@text='卖出']"
NORMAL_REDEEM = "xpath_//android.widget.RadioButton[@resource-id='com.shhxzq.xjb:id/rbtn_redeem_normal_select']"
FAST_REDEEM = "xpath_//android.widget.RadioButton[@resource-id='com.shhxzq.xjb:id/rbtn_redeem_faster_select']"
REDEEM_AMOUNT = "xpath_//android.widget.EditText[@text='请输入卖出份额']"
REDEEM_CONFIRM = "xpath_//android.widget.Button[@text='确认']"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"
REDEEM_DONE = "xpath_//android.widget.Button[@text='确认']"
TRADE_RECORDS = "xpath_//android.widget.TextView[@text='交易记录']"
SCROLL = "swipe_xpath_//scroll_3"
VALUE_DATE = "xpath_//android.widget.TextView[@text='起息日']"
VALUE_DATE_STOP = "swipe_xpath_//android.widget.TextView[@text='起息日']"

SWIPE_BEGIN = "swipe_xpath_//"
BACK = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left_orange']"
VIP_SWIPE_STOP = "swipe_xpath_//android.widget.TextView[@text='购买金额']"
VIP_STOP = "swipe_xpath_//android.widget.TextView[@text='购买确认中']/preceding-sibling::android.widget.LinearLayout/android.widget.TextView[contains(@text,'%s')]"
VIP = "xpath_//android.widget.TextView[@text='购买确认中']/preceding-sibling::android.widget.LinearLayout/android.widget.TextView[contains(@text,'%s')]"
VIP_PRODUCT = "xpath_//android.widget.TextView[@text='购买金额']"
SHOW_TIPS = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/img_vip_show_tips']"
HISTORY_HOLDING_STOP = "swipe_xpath_//android.widget.TextView[@text='%s']"
HISTORY_HOLDING = "xpath_//android.widget.TextView[@text='%s']"
HISTORY_HOLDING_BUTTON = "xpath_//android.widget.TextView[@text='历史持仓']"
EXPIRY_PROCESSING = "xpath_//android.widget.TextView[@text='更改']"
EXPIRY_PROCESSING_MODIFY = "swipe_xpath_//android.widget.TextView[@text='更改']"

current_page = []


class AssetsHighEndDetailPage(PageObject):
    def __init__(self, web_driver):
        super(AssetsHighEndDetailPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_page_title(self):
        self.assert_values('高端理财', self.get_text('com.shhxzq.xjb:id/title_actionbar_orange', 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def verify_high_end_assets_details(self):
        self.assert_values('True', str(self.element_exist("//android.widget.TextView[@text='高端总资产(元)']")))
        vip_total_actual = self.get_text('com.shhxzq.xjb:id/tv_vip_total', 'find_element_by_id').replace(',', '')
        self.assert_values(ASSERT_DICT['vip_asset_login'], vip_total_actual)
        self.assert_values('True', str(self.element_exist("//android.widget.TextView[@text='累计收益(元)']")))

        page = self

        return page

    @robot_log
    def go_to_trade_detail_page(self):
        self.perform_actions(TRADE_DETAIL)
        page = huaxin_ui.ui_android_xjb_3_0.trade_detail_page.TradeDetailPage(self.web_driver)
        return page

    @robot_log
    def view_high_end_more_product(self):
        self.perform_actions(SWIPE_BEGIN, HIGH_END_MORE_PRODUCT_STOP, 'U')
        self.perform_actions(HIGH_END_MORE_PRODUCT)

        page = huaxin_ui.ui_android_xjb_3_0.finance_high_end_page.FinanceHighEndPage(self.web_driver)

        return page

    @robot_log
    def view_high_end_history_product(self):
        self.perform_actions(
            HIGH_END_MORE_PRODUCT,
            HIGH_END_START, HISTORY_PRODUCT_STOP, 'U',
            HISTORY_PRODUCT,
        )

    @robot_log
    def go_to_high_end_redeem_page(self, high_end_product):
        self.perform_actions(TITLE_START, HIGH_END_PRODUCT_STOP % high_end_product, 'U')
        while self.is_overlapped(HIGH_END_PRODUCT_OVERLAPPED % high_end_product):  # 若被浮层遮挡,则进行滑动
            self.screen_swipe('U')
        self.perform_actions(HIGH_END_PRODUCT % high_end_product)

        page = huaxin_ui.ui_android_xjb_3_0.high_end_redeem_page.HighEndRedeemPage(self.web_driver)

        return page

    @robot_log
    def redeem_high_end_product(self, redeem_amount, trade_password, high_end_product):
        self.perform_actions(TITLE_START, HIGH_END_PRODUCT_STOP % high_end_product, 'U',
                             HIGH_END_PRODUCT % high_end_product,
                             REDEEM)

        redeem_max = self.get_text('com.shhxzq.xjb:id/tv_dqb_redeem_product_max', 'find_element_by_id')
        redeem_max = '%.2f' % float(filter(lambda ch: ch in '0123456789.', redeem_max))
        self.perform_actions(REDEEM_AMOUNT, redeem_amount)

        if float(redeem_amount) >= 1:
            if float(redeem_amount) > float(redeem_max):
                redeem_amt_actual = self.get_text('com.shhxzq.xjb:id/cedt_dqb_redeem_product_amt', 'find_element_by_id')
                redeem_amt_actual = '%.2f' % float(filter(lambda ch: ch in '0123456789.', redeem_amt_actual))
                self.assert_values(float(redeem_max), float(redeem_amt_actual), '==')
            else:
                self.perform_actions(REDEEM_CONFIRM,
                                     TRADE_PASSWORD, trade_password)
                self.assert_values('完成', self.get_text(self.page_title, 'find_element_by_id'))

                self.perform_actions(REDEEM_DONE)

                self.perform_actions(TITLE_START, HIGH_END_PRODUCT_STOP % high_end_product, 'U',
                                     HIGH_END_PRODUCT % high_end_product,
                                     TRADE_RECORDS)

                redeem_amt_actual = self.get_text('com.shhxzq.xjb:id/trade_amount', 'find_element_by_id')
                redeem_amt_actual = '%.2f' % float(filter(lambda ch: ch in '0123456789.', redeem_amt_actual))
                self.assert_values(float(redeem_amount), float(redeem_amt_actual))

        else:
            self.assert_values('卖出', self.get_text(self.page_title, 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def normal_redeem_vipproduct(self, redeem_amount, trade_password, high_end_product_for_fast_redeem):
        self.perform_actions(
            TITLE_START, HIGH_END_PRODUCT_STOP % high_end_product_for_fast_redeem, 'U',
                         HIGH_END_PRODUCT % high_end_product_for_fast_redeem,
            REDEEM,
            NORMAL_REDEEM,
            REDEEM_AMOUNT, redeem_amount,
            REDEEM_CONFIRM,
            TRADE_PASSWORD, trade_password,
            REDEEM_DONE,
        )

        page = self

        return page

    @robot_log
    def fast_redeem_vipproduct(self, redeem_amount, trade_password, high_end_product_for_fast_redeem):
        self.perform_actions(
            TITLE_START, HIGH_END_PRODUCT_STOP % high_end_product_for_fast_redeem, 'U',
                         HIGH_END_PRODUCT % high_end_product_for_fast_redeem,
            REDEEM,
            FAST_REDEEM,
            REDEEM_AMOUNT, redeem_amount,
            REDEEM_CONFIRM,
            TRADE_PASSWORD, trade_password,
            REDEEM_DONE,
        )

        page = self

        return page

    @robot_log
    def back_to_assets_analysis_page(self):
        self.perform_actions(
            BACK
        )

        page = huaxin_ui.ui_android_xjb_3_0.assets_analysis_page.AssetsAnalysisPage(self.web_driver)

        return page

    @robot_log
    def go_to_high_end_supplementary_purchase_page(self):
        self.perform_actions(SWIPE_BEGIN, VIP_SWIPE_STOP, 'U',
                             VIP_PRODUCT
                             )

        page = huaxin_ui.ui_android_xjb_3_0.high_end_supplementary_purchase_page.HighEndSupplementaryPurchasePage(
            self.web_driver)

        return page

    @robot_log
    def go_to_high_end_supplementary_purchase_page_(self, product_name):
        self.perform_actions(SWIPE_BEGIN, VIP_STOP % product_name, 'U',
                             VIP % product_name
                             )

        page = huaxin_ui.ui_android_xjb_3_0.high_end_supplementary_purchase_page.HighEndSupplementaryPurchasePage(
            self.web_driver)

        return page

    @robot_log
    def go_to_description_page(self):
        self.perform_actions(SHOW_TIPS)

        page = huaxin_ui.ui_android_xjb_3_0.description_page.DescriptionPage(self.web_driver)

        return page

    @robot_log
    def go_to_dhb_history_holding_list_page(self):
        self.perform_actions(HISTORY_HOLDING_BUTTON)

        page = self

        return page

    @robot_log
    def verify_vip_history_holding_detail(self, product_name):
        self.assert_values('产品名称', self.get_text('com.shhxzq.xjb:id/tv_myassets_amt_title', 'find_element_by_id'))
        self.assert_values(product_name, self.get_text('com.shhxzq.xjb:id/myassets_amt', 'find_element_by_id'))
        self.assert_values('累计收益', self.get_text('com.shhxzq.xjb:id/tv_item_yield_type_title', 'find_element_by_id'))
        self.assert_values('10.00元', self.get_text('com.shhxzq.xjb:id/myassets_yield', 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def go_to_history_holding_page(self, product_name):
        self.perform_actions(SWIPE_BEGIN, HISTORY_HOLDING_STOP % product_name, 'U')
        self.perform_actions(HISTORY_HOLDING % product_name)

        page = huaxin_ui.ui_android_xjb_3_0.history_holding_page.HistoryHoldingPage(self.web_driver)

        return page

    @robot_log
    def back_to_assets_page(self):
        self.perform_actions(BACK)

        page = huaxin_ui.ui_android_xjb_3_0.assets_page.AssetsPage(self.web_driver)

        return page

    @robot_log
    def go_to_expiry_processing_type_page(self):
        self.perform_actions(SWIPE_BEGIN, EXPIRY_PROCESSING_MODIFY, 'U')
        self.perform_actions(EXPIRY_PROCESSING)

        page = huaxin_ui.ui_android_xjb_3_0.expiry_processing_type_page.ExpiryProcessingTypePage(self.web_driver)
        return page
