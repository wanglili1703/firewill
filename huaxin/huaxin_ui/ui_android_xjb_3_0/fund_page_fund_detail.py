# coding=utf-8
from _common.page_object import PageObject
import time

import huaxin_ui.ui_android_xjb_3_0.fund_page
import huaxin_ui.ui_android_xjb_3_0.fund_plan_page
import huaxin_ui.ui_android_xjb_3_0.fund_product_search_page
import huaxin_ui.ui_android_xjb_3_0.fund_selected_page
import huaxin_ui.ui_android_xjb_3_0.fund_purchase_page
import huaxin_ui.ui_android_xjb_3_0.fund_product_search_page
import huaxin_ui.ui_android_xjb_3_0.product_history_income_page
import huaxin_ui.ui_android_xjb_3_0.fund_notice_page
import huaxin_ui.ui_android_xjb_3_0.user_operation_succeed_page
import huaxin_ui.ui_android_xjb_3_0.fund_convert_page
import huaxin_ui.ui_android_xjb_3_0.fund_topic_detail_page

from _common.xjb_decorator import robot_log

BUY_FUND = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_fund_purchase']"
BUY_AMOUNT = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/product_purchase_amt']"
BUY_CONFIRM = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/product_purchase_bt']"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"
BUY_DONE = "xpath_//android.widget.Button[@text='确认']"
CANCEL = "xpath_//android.widget.TextView[@text='取消']"
POINT_SWITCH = "xpath_//android.widget.ToggleButton[@resource-id='com.shhxzq.xjb:id/tbtn_point_switch']"
COUPONS_INFO = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_purchase_coupons_info']"
COUPONS = "xpath_//android.widget.RelativeLayout[@clickable='true']//android.widget.TextView[@text='不可叠加使用']"
# NONSUPERCOMPOSED_COUPON_SWIPE_STOP = "swipe_xpath_//android.widget.RelativeLayout[@clickable='true']//android.widget.TextView[@text='不可叠加使用']"
COUPONS_CONFIRM = "xpath_//android.widget.TextView[@text='确认']"
SUPERPOSED_COUPON_1 = "xpath_//android.widget.RelativeLayout[@clickable='true']//android.widget.TextView[@text='可叠加使用']"
# SUPERPOSED_COUPON_2="xpath_//android.widget.ImageView/../../following-sibling::android.widget.FrameLayout/android.widget.RelativeLayout[@clickable='true']"
SUPERPOSED_COUPON_2 = "xpath_//android.widget.RelativeLayout[@clickable='true']/../following-sibling::android.widget.FrameLayout/android.widget.RelativeLayout[@clickable='true']"
COUPON_SWIPE_BEGAIN = "swipe_xpath_//"
NONSUPERCOMPOSED_COUPON_SWIPE_STOP = "swipe_xpath_//android.widget.RelativeLayout[@clickable='true']//android.widget.TextView[@text='不可叠加使用']"
SUPERCOMPOSED_COUPON_SWIPE_STOP = "swipe_xpath_//android.widget.RelativeLayout[@clickable='true']//android.widget.TextView[@text='可叠加使用']"
SUPERCOMPOSED_COUPON_SWIPE_BEGAIN = "swipe_xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/img_coupons_item_select']"
SUPERCOMPOSED_COUPON_SWIPE_STOP_1 = "swipe_xpath_//android.widget.ImageView/../../following-sibling::android.widget.FrameLayout/android.widget.RelativeLayout[@clickable='true']"

FUND_PLAN_BUTTON = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_fund_plan_detail']"
ASSETS = "xpath_//android.widget.RelativeLayout[5]/android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/tab_image'][POP]"
FUND = "xpath_//android.widget.TextView[@text='基金']"
SWIPE_BEGIN = "swipe_xpath_//"
FUND_SWIPE_STOP = "swipe_xpath_//android.widget.TextView[@text='购买金额']"
FUND_PRODUCT = "xpath_//android.widget.TextView[@text='购买金额']"
CANCEL_BUTTON = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/button1']"
BACK = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left']"
BACK_BUTTON = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left']"
BACK_BUTTON_POINTS = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left_orange']"
KEEP_OBTAINING_POINTS = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/button2']"
FUND_DETAIL_PAGE_BACK = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/actionbar_back'][POP]"

COMFIRM_BUTTON_SWIPE_STOP = "swipe_xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/product_purchase_bt']"
SELECT = "xpath_//android.widget.TextView[@text='自选']"
DELETE_SELECTED_FUND = "xpath_//android.widget.TextView[@text='删自选']"
RECENT_THREE_MONTHS = "xpath_//android.view.View[@index='1']"
RECENT_SIX_MONTHS = "xpath_//android.view.View[@index='2']"
RECENT_ONE_YEAR = "xpath_//android.view.View[@index='3']"
RECENT_THREE_YEARS = "xpath_//android.view.View[@index='4']"
ANNUAL_RETURN_STOP = "swipe_xpath_//android.widget.TextView[@text='年度回报']"
RISK_EVALUATION_STOP = "swipe_xpath_//android.widget.TextView[@text='风险收益特征']"
HISTORY = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/goto_histroy']"
VIEW_HISTORY = "xpath_//android.widget.TextView[@text='查看历史']"
GENERAL_SITUATION = "xpath_//android.widget.TextView[@text='概况']"
COMBINATION = "xpath_//android.widget.TextView[@text='组合']"
NOTICE = "xpath_//android.widget.TextView[@text='公告']"
RATE = "xpath_//android.widget.TextView[@text='费率']"
NOTICE_CONTENT = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_item_fund_notice_content']"
INCOME_PER_WAN = "xpath_//android.widget.TextView[@text='万份收益']"
THINK = "xpath_//android.widget.Button[@text='再考虑一下']"
GO_ON = "xpath_//android.widget.Button[@text='继续买入']"

current_page = []


class FundPageFundDetail(PageObject):
    def __init__(self, web_driver):
        super(FundPageFundDetail, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_page_title(self, operation_type=None):
        page = self
        if operation_type is None:
            self.assert_values('基金详情', self.get_text('com.shhxzq.xjb:id/actionbar_title', 'find_element_by_id'))
        elif operation_type == 'fund_convert':
            self.assert_values('转换', self.get_text('com.shhxzq.xjb:id/title_actionbar', 'find_element_by_id'))
            page = huaxin_ui.ui_android_xjb_3_0.fund_convert_page.FundConvertPage(self.web_driver)

        return page

    @robot_log
    def buy_fund_product(self, amount, trade_password, points='N', nonsuperposed_coupon='N', superposed_coupon='N',
                         source='1'):

        self.perform_actions(
            BUY_FUND,
            BUY_AMOUNT, amount)

        if points == 'Y':
            self.perform_actions(POINT_SWITCH)

            time.sleep(5)

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

        self.perform_actions(SWIPE_BEGIN, COMFIRM_BUTTON_SWIPE_STOP, 'U')

        self.perform_actions(
            BUY_CONFIRM)

        if float(amount) >= 1 and float(amount) < 50000:
            self.perform_actions(TRADE_PASSWORD, trade_password)

            self.assert_values('完成', self.get_text(self.page_title, 'find_element_by_id'))

            self.perform_actions(BUY_DONE,
                                 FUND_DETAIL_PAGE_BACK)

            if source == '1':
                self.perform_actions(
                    CANCEL,
                    ASSETS)

            else:
                self.perform_actions(CANCEL,
                                     BACK,
                                     BACK_BUTTON,
                                     BACK_BUTTON_POINTS)

            self.perform_actions(FUND,
                                 SWIPE_BEGIN, FUND_SWIPE_STOP, 'U',
                                 FUND_PRODUCT)

            time.sleep(3)

            page = huaxin_ui.ui_android_xjb_3_0.fund_page.FundPage(self.web_driver)

        elif float(amount) >= 100000000:
            page = self
            self.perform_actions(CANCEL_BUTTON)

            self.assert_values('买入', self.get_text('com.shhxzq.xjb:id/title_actionbar', 'find_element_by_id'))

        else:
            page = self
            self.assert_values('买入', self.get_text('com.shhxzq.xjb:id/title_actionbar', 'find_element_by_id'))
        return page

    @robot_log
    def go_to_fund_plan_page(self):
        self.perform_actions(FUND_PLAN_BUTTON)

        page = huaxin_ui.ui_android_xjb_3_0.fund_plan_page.FundPlanPage(self.web_driver)

        return page

    @robot_log
    def select_fund(self):
        self.perform_actions(SELECT)

        page = self

        return page

    @robot_log
    def back_to_fund_selected_page(self):
        self.perform_actions(FUND_DETAIL_PAGE_BACK,
                             CANCEL)

        page = huaxin_ui.ui_android_xjb_3_0.fund_selected_page.FundSelectedPage(self.web_driver)
        return page

    @robot_log
    def go_to_fund_purchase_page(self, user_type=None, risk=None):
        self.perform_actions(BUY_FUND)
        page = huaxin_ui.ui_android_xjb_3_0.fund_purchase_page.FundPurchasePage(self.web_driver)

        if risk == 'high':
            if user_type == 'conservative':
                self.assert_values('风险提示', self.get_text('com.shhxzq.xjb:id/alertTitle', 'find_element_by_id'))
                self.assert_values('再考虑一下', self.get_text('com.shhxzq.xjb:id/button1', 'find_element_by_id'))
                self.assert_values('去测试', self.get_text('com.shhxzq.xjb:id/button2', 'find_element_by_id'))
                self.perform_actions(THINK)
                page = self
            elif user_type == 'moderate':
                self.assert_values('风险提示', self.get_text('com.shhxzq.xjb:id/alertTitle', 'find_element_by_id'))
                self.assert_values('再考虑一下', self.get_text('com.shhxzq.xjb:id/button1', 'find_element_by_id'))
                self.assert_values('继续买入', self.get_text('com.shhxzq.xjb:id/button2', 'find_element_by_id'))
                self.perform_actions(GO_ON)
        elif risk == 'middle_high':
            if user_type == 'cautious':
                self.assert_values('风险提示', self.get_text('com.shhxzq.xjb:id/alertTitle', 'find_element_by_id'))
                self.assert_values('再考虑一下', self.get_text('com.shhxzq.xjb:id/button1', 'find_element_by_id'))
                self.assert_values('继续买入', self.get_text('com.shhxzq.xjb:id/button2', 'find_element_by_id'))
                self.perform_actions(GO_ON)

        return page

    @robot_log
    def go_to_product_history_income_page(self, type='ImageView'):
        if type == 'ImageView':
            self.perform_actions(HISTORY)
        elif type == 'TextView':
            self.perform_actions(VIEW_HISTORY)

        page = huaxin_ui.ui_android_xjb_3_0.product_history_income_page.ProductHistoryIncomePage(self.web_driver)

        return page

    @robot_log
    def go_to_fund_notice_page(self):
        self.perform_actions(NOTICE_CONTENT)

        page = huaxin_ui.ui_android_xjb_3_0.fund_notice_page.FundNoticePage(self.web_driver)

        return page

    @robot_log
    def back_to_fund_product_search_page(self):
        self.perform_actions(FUND_DETAIL_PAGE_BACK)

        page = huaxin_ui.ui_android_xjb_3_0.fund_product_search_page.FundProductSearchPage(self.web_driver)
        return page

    @robot_log
    def back_to_fund_topic_detail_page(self):
        self.perform_actions(FUND_DETAIL_PAGE_BACK)

        page = huaxin_ui.ui_android_xjb_3_0.fund_topic_detail_page.FundTopicDetailPage(self.web_driver)

        return page

    @robot_log
    def delete_selected_fund(self):
        self.perform_actions(DELETE_SELECTED_FUND)

        page = self

        return page

    @robot_log
    def check_fund_basic_information(self, fund_product_name, fund_type='混合型'):
        self.assert_values(True,
                           self.element_exist("//android.widget.TextView[contains(@text,'%s')]" % fund_product_name))
        self.assert_values('基金类型', self.get_text('com.shhxzq.xjb:id/first_left_title', 'find_element_by_id'))
        self.assert_values(fund_type, self.get_text('com.shhxzq.xjb:id/first_left_content', 'find_element_by_id'))
        self.assert_values('风险等级', self.get_text('com.shhxzq.xjb:id/second_left_title', 'find_element_by_id'))
        self.assert_values('低', self.get_text('com.shhxzq.xjb:id/second_left_content', 'find_element_by_id'))
        self.assert_values('开放状态', self.get_text('com.shhxzq.xjb:id/third_left_title', 'find_element_by_id'))
        if fund_type == '混合型':
            self.assert_values(True, self.element_exist("//android.widget.TextView[contains(@text,'单位净值')]"))
            self.assert_values('开放申购  开放赎回',
                               self.get_text('com.shhxzq.xjb:id/third_left_content', 'find_element_by_id'))
            self.assert_values('银河证券', self.get_text('com.shhxzq.xjb:id/fourth_left_title', 'find_element_by_id'))
            self.assert_values('日涨幅', self.get_text('com.shhxzq.xjb:id/second_right_title', 'find_element_by_id'))
        elif fund_type == '货币型':
            self.assert_values(True, self.element_exist("//android.widget.TextView[contains(@text,'七日年化')]"))
            # self.assert_values('暂停申购  开放赎回',
            #                    self.get_text('com.shhxzq.xjb:id/third_left_content', 'find_element_by_id'))
            self.assert_values('收益分配日', self.get_text('com.shhxzq.xjb:id/fourth_left_title', 'find_element_by_id'))
            self.assert_values('万份收益', self.get_text('com.shhxzq.xjb:id/second_right_title', 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def view_non_monetary_fund_details(self, detail_type):
        if detail_type == '业绩':
            self.assert_values(True, self.element_exist("//android.widget.TextView[contains(@text,'本基金')]"))
            self.assert_values(True, self.element_exist("//android.widget.TextView[contains(@text,'同类均值')]"))
            self.assert_values(True, self.element_exist("//android.widget.TextView[contains(@text,'沪深300')]"))
            self.assert_values(True, self.element_exist("//android.widget.TextView[contains(@text,'最大回撤')]"))

            self.perform_actions(RECENT_THREE_MONTHS,
                                 RECENT_SIX_MONTHS,
                                 RECENT_ONE_YEAR,
                                 RECENT_THREE_YEARS)

            self.perform_actions(SWIPE_BEGIN, ANNUAL_RETURN_STOP, 'U')
            self.assert_values('历史回报', self.get_text('com.shhxzq.xjb:id/tv_header', 'find_element_by_id'))
            self.assert_values(True, self.element_exist("//android.widget.TextView[@text='时间区间']"))
            self.assert_values(True, self.element_exist("//android.widget.TextView[@text='回报率(%)']"))
            self.assert_values(True, self.element_exist("//android.widget.TextView[@text='同类平均(%)']"))
            self.perform_actions(SWIPE_BEGIN, RISK_EVALUATION_STOP, 'U')
            self.assert_values(True, self.element_exist("//android.widget.TextView[@text='风险评估']"))
            self.assert_values(True, self.element_exist("//android.widget.TextView[@text='风险统计']"))
        elif detail_type == '概况':
            self.perform_actions(GENERAL_SITUATION)
        elif detail_type == '组合':
            self.perform_actions(COMBINATION)
        elif detail_type == '费率':
            self.perform_actions(RATE)
        elif detail_type == '公告':
            self.perform_actions(NOTICE)
            self.assert_values(True,
                               self.element_exist("//android.widget.TextView[contains(@text,'关于博时基金管理有限公司旗下部分开放式基金')]"))

        page = self

        return page

    @robot_log
    def view_monetary_fund_details(self, detail_type):
        if detail_type == '业绩':
            self.assert_values(True, self.element_exist("//android.widget.TextView[@text='七日年化收益率']"))
            self.assert_values(True, self.element_exist("//android.widget.TextView[contains(@text,'本基金')]"))
            self.assert_values(True, self.element_exist("//android.widget.TextView[contains(@text,'同类货币基金')]"))

            self.perform_actions(RECENT_THREE_MONTHS,
                                 RECENT_SIX_MONTHS,
                                 RECENT_ONE_YEAR)

            # self.perform_actions(INCOME_PER_WAN)

            self.perform_actions(SWIPE_BEGIN, ANNUAL_RETURN_STOP, 'U')
            self.assert_values('历史回报', self.get_text('com.shhxzq.xjb:id/tv_header', 'find_element_by_id'))
            self.assert_values(True, self.element_exist("//android.widget.TextView[@text='时间区间']"))
            self.assert_values(True, self.element_exist("//android.widget.TextView[@text='回报率(%)']"))
            self.assert_values(True, self.element_exist("//android.widget.TextView[@text='同类平均(%)']"))
            self.perform_actions(SWIPE_BEGIN, RISK_EVALUATION_STOP, 'U')
            self.assert_values(True, self.element_exist("//android.widget.TextView[@text='风险评估']"))
        elif detail_type == '概况':
            self.perform_actions(GENERAL_SITUATION)
        elif detail_type == '组合':
            self.perform_actions(COMBINATION)
        elif detail_type == '费率':
            self.perform_actions(RATE)
        elif detail_type == '公告':
            self.perform_actions(NOTICE)
            self.assert_values(True,
                               self.element_exist(
                                   "//android.widget.TextView[contains(@text,'中海')]"))

        page = self
        return page

    @robot_log
    def view_newly_raised_fund_details(self):
        self.assert_values('认购中', self.get_text('com.shhxzq.xjb:id/subscribe_status_info', 'find_element_by_id'))
        self.assert_values('距离认购期结束还有',
                           self.get_text('com.shhxzq.xjb:id/subscribe_countdown_text', 'find_element_by_id'))
        self.assert_values('天', self.get_text('com.shhxzq.xjb:id/day_unit', 'find_element_by_id'))
        self.assert_values('时', self.get_text('com.shhxzq.xjb:id/hour_unit', 'find_element_by_id'))
        self.assert_values('分', self.get_text('com.shhxzq.xjb:id/minute_unit', 'find_element_by_id'))
        self.assert_values('秒', self.get_text('com.shhxzq.xjb:id/second_unit', 'find_element_by_id'))
        self.assert_values('认购期仅供参考，以基金公司公告为准。为避免基金认购提前结束，请及时购买。',
                           self.get_text('com.shhxzq.xjb:id/fund_detail_title_note_text', 'find_element_by_id'))
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='新基金认购流程']"))
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='认购募集期']"))
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='验证备案']"))
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='封闭运作']"))
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='开放赎回申购']"))
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='概况']"))
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='费率']"))
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='公告']"))

        page = self
        return page
