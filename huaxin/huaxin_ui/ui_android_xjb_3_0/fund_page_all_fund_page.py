# coding=utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
from decimal import Decimal
import time

import huaxin_ui.ui_android_xjb_3_0.assets_fund_detail_page
import huaxin_ui.ui_android_xjb_3_0.fund_product_search_page
import huaxin_ui.ui_android_xjb_3_0.fund_filter_page
import huaxin_ui.ui_android_xjb_3_0.fund_page_fund_detail

BACK_BUTTON = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left']"
I_KNOW = "xpath_//android.widget.Button[@text='我知道了'][POP]"
FUND_PRODUCT_SEARCH = "xpath_//android.widget.TextView[@text='基金代码/简拼/重仓资产']"
FUND_FILTER = "xpath_//android.widget.TextView[@text='筛选']"
FUND_TYPE = "xpath_//android.widget.TextView[contains(@text,'%s')]"
FUND_PRODUCT = "xpath_//android.widget.TextView[contains(@text,'%s')]"
SWIPE_BEGIN = "swipe_xpath_//"
FUND_STOP = "swipe_xpath_//android.widget.TextView[contains(@text,'%s')]"
FUND_ALL = "xpath_//android.widget.TextView[@text='全部']"
NET_ASSET_VALUE_DESCEND = "xpath_//android.widget.TextView[@text='单位净值']"
NET_ASSET_VALUE_ASCEND = "xpath_//android.widget.TextView[@text='单位净值']"
DAILY_INCREASES_DESCEND = "xpath_//android.widget.TextView[@text='日涨幅']"
DAILY_INCREASES_ASCEND = "xpath_//android.widget.TextView[@text='日涨幅']"
SEVEN_DAYS_DESCEND = "xpath_//android.widget.TextView[@text='七日年化']"
SEVEN_DAYS_ASCEND = "xpath_//android.widget.TextView[@text='七日年化']"
RECENT_ONE_MONTH_DESCEND = "xpath_//android.widget.TextView[@text='近1月']"
RECENT_ONE_MONTH_ASCEND = "xpath_//android.widget.TextView[@text='近1月']"
RECENT_THREE_MONTH_DESCEND = "xpath_//android.widget.TextView[@text='近3月']"
RECENT_THREE_MONTH_ASCEND = "xpath_//android.widget.TextView[@text='近3月']"
RECENT_SIX_MONTH_DESCEND = "xpath_//android.widget.TextView[@text='近6月']"
RECENT_SIX_MONTH_ASCEND = "xpath_//android.widget.TextView[@text='近6月']"
RECENT_ONE_YEAR_DESCEND = "xpath_//android.widget.TextView[@text='近1年']"
RECENT_ONE_YEAR_ASCEND = "xpath_//android.widget.TextView[@text='近1年']"
RECENT_THREE_YEAR_DESCEND = "xpath_//android.widget.TextView[@text='近3年']"
RECENT_THREE_YEAR_ASCEND = "xpath_//android.widget.TextView[@text='近3年']"
SWIPE_BEGAIN = "swipe_xpath_//"
FUND_TYPE_SCROLL_1 = "swipe_xpath_//scroll_8"
FUND_TYPE_SCROLL_2 = "swipe_xpath_//scroll_8"
STOCK_FUNDS = "xpath_//android.widget.TextView[@text='股票型']"
MONETARY_FUNDS = "xpath_//android.widget.TextView[@text='货币型']"
BOND_FUNDS = "xpath_//android.widget.TextView[@text='债券型']"
BLEND_FUNDS = "xpath_//android.widget.TextView[@text='混合型']"
QDII = "xpath_//android.widget.TextView[@text='QDII']"
OTHER_FUNDS = "xpath_//android.widget.TextView[@text='其他']"

current_page = []


class FundPageAllFundPage(PageObject):
    def __init__(self, web_driver):
        super(FundPageAllFundPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('我知道了', self.get_text('com.shhxzq.xjb:id/btn_mask_fund_query', 'find_element_by_id'))
        page = self

        return page

    @robot_log
    def go_to_assets_fund_detail_page(self):
        self.perform_actions(I_KNOW,
                             BACK_BUTTON)
        page = huaxin_ui.ui_android_xjb_3_0.assets_fund_detail_page.AssetsFundDetailPage(self.web_driver)

        return page

    @robot_log
    def close_tips(self):
        self.perform_actions(I_KNOW)
        page = self

        return page

    @robot_log
    def go_to_fund_product_search_page(self):
        self.perform_actions(FUND_PRODUCT_SEARCH)

        page = huaxin_ui.ui_android_xjb_3_0.fund_product_search_page.FundProductSearchPage(self.web_driver)

        return page

    @robot_log
    def go_to_fund_filter_page(self):
        self.perform_actions(FUND_FILTER)

        page = huaxin_ui.ui_android_xjb_3_0.fund_filter_page.FundFilterPage(self.web_driver)

        return page

    @robot_log
    def select_fund_type(self, fund_type='全部'):
        self.perform_actions(FUND_TYPE % fund_type)

        page = self

        return page

    @robot_log
    def go_to_fund_detail_page(self, fund_product_name):
        self.perform_actions(SWIPE_BEGIN, FUND_STOP % fund_product_name, 'U')
        self.perform_actions(FUND_PRODUCT % fund_product_name)

        page = huaxin_ui.ui_android_xjb_3_0.fund_page_fund_detail.FundPageFundDetail(self.web_driver)

        return page

    # 基金频道--全部基金
    @robot_log
    def fund_all_funds(self, fund_type):
        # 日涨幅默认排序
        self.perform_actions(FUND_TYPE % fund_type)
        if fund_type != '指数型':
            if fund_type != 'QDII':
                eles = self.get_elements_with_same_id(id='com.shhxzq.xjb:id/increaseDay')
                daily_1 = float(eles[0].text.strip("%").encode('utf-8')) / 100
                daily_2 = float(eles[1].text.strip("%").encode('utf-8')) / 100
                self.assert_values(True, self.assert_values(daily_1, daily_2, '>='))
                self.assert_values(True, self.element_exist("//android.widget.TextView[@text='基金名称']"))

            if fund_type == '货币型':
                self.assert_values(True, self.element_exist("//android.widget.TextView[@text='万份收益']"))
                self.assert_values(True, self.element_exist("//android.widget.TextView[@text='七日年化']"))
            else:
                self.assert_values(True, self.element_exist("//android.widget.TextView[@text='单位净值']"))
                self.assert_values(True, self.element_exist("//android.widget.TextView[@text='日涨幅']"))
            self.assert_values(True, self.element_exist("//android.widget.TextView[@text='近1月']"))
            # 日涨幅降序排序
            if fund_type == '货币型':
                self.perform_actions(SEVEN_DAYS_DESCEND)
            else:
                self.perform_actions(DAILY_INCREASES_DESCEND)
            if fund_type != 'QDII':
                eles = self.get_elements_with_same_id(id='com.shhxzq.xjb:id/increaseDay')
                self.perform_actions(FUND_TYPE % fund_type)
                daily_1 = float(eles[0].text.strip("%").encode('utf-8')) / 100
                daily_2 = float(eles[1].text.strip("%").encode('utf-8')) / 100
                self.assert_values(True, self.assert_values(daily_1, daily_2, '>='))

            # 日涨幅升序排序
            if fund_type == '货币型':
                self.perform_actions(SEVEN_DAYS_ASCEND)
            else:
                self.perform_actions(DAILY_INCREASES_ASCEND)
            if fund_type != 'QDII':
                eles = self.get_elements_with_same_id(id='com.shhxzq.xjb:id/increaseDay')
                self.perform_actions(FUND_TYPE % fund_type)
                daily_1 = float(eles[0].text.strip("%").encode('utf-8')) / 100
                daily_2 = float(eles[1].text.strip("%").encode('utf-8')) / 100
                self.assert_values(True, self.assert_values(daily_1, daily_2, '<='))

                self.perform_actions(SWIPE_BEGAIN, FUND_TYPE_SCROLL_1, 'L')
                self.assert_values(True, self.element_exist("//android.widget.TextView[@text='近3月']"))
                self.assert_values(True, self.element_exist("//android.widget.TextView[@text='近6月']"))
                self.perform_actions(SWIPE_BEGAIN, FUND_TYPE_SCROLL_2, 'L')
                self.assert_values(True, self.element_exist("//android.widget.TextView[@text='近1年']"))
                self.assert_values(True, self.element_exist("//android.widget.TextView[@text='近3年']"))

        page = self

        return page
