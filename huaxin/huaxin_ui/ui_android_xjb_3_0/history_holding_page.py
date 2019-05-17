# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.assets_high_end_detail_page

RECENT_THREE_MONTH = "xpath_//android.view.View[@index='1']"
RECENT_SIX_MONTH = "xpath_//android.view.View[@index='2']"
RECENT_ONE_YEAR = "xpath_//android.view.View[@index='3']"
RECENT_THREE_YEAR = "xpath_//android.view.View[@index='4']"
BACK = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left']"


class HistoryHoldingPage(PageObject):
    def __init__(self, web_driver):
        super(HistoryHoldingPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self, product_name):
        self.assert_values(product_name, self.get_text(self.page_title, 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def verify_history_holding_page_details(self, product_type='fund'):
        if product_type == 'fund':
            self.assert_values('查看产品详情', self.get_text('com.shhxzq.xjb:id/tv_hold_fund_name', 'find_element_by_id'))
            self.assert_values(True, self.element_exist("//android.widget.TextView[@text='累计收益(元)']"))
            self.assert_values(True, self.element_exist("//android.widget.TextView[contains(@text,'本基金')]"))
            self.assert_values(True, self.element_exist("//android.widget.TextView[contains(@text,'同类均值')]"))
            self.assert_values(True, self.element_exist("//android.widget.TextView[contains(@text,'沪深300')]"))
            self.assert_values(True, self.element_exist("//android.widget.TextView[contains(@text,'最大回撤')]"))
            self.perform_actions(RECENT_THREE_MONTH)
            self.perform_actions(RECENT_SIX_MONTH)
            self.perform_actions(RECENT_ONE_YEAR)
            self.perform_actions(RECENT_THREE_YEAR)
        elif product_type == 'dhb':
            self.assert_values(True, self.element_exist("//android.widget.TextView[@text='累计收益']"))
            self.assert_values('10.00', self.get_text('com.shhxzq.xjb:id/tv_dqb_history_income', 'find_element_by_id'))
            self.assert_values(True, self.element_exist("//android.widget.TextView[@text='年化业绩比较基准']"))
            self.assert_values(True, self.element_exist("//android.widget.TextView[@text='查看产品详情']"))
            self.assert_values(True, self.element_exist("//android.widget.TextView[@text='产品期限']"))
            self.assert_values(True, self.element_exist("//android.widget.TextView[@text='交易记录']"))
        elif product_type == 'vip':
            self.assert_values(True, self.element_exist("//android.widget.TextView[@text='累计收益(元)']"))
            self.assert_values(True, self.element_exist("//android.widget.TextView[@text='10.00']"))
            self.assert_values(True, self.element_exist("//android.widget.TextView[@text='年化业绩比较基准']"))
            self.assert_values(True, self.element_exist("//android.widget.TextView[@text='起息日']"))
            self.assert_values(True, self.element_exist("//android.widget.TextView[@text='到期日']"))
            self.assert_values(True, self.element_exist("//android.widget.TextView[@text='查看产品详情']"))
            self.assert_values(True, self.element_exist("//android.widget.TextView[@text='开放说明']"))
            self.assert_values(True, self.element_exist("//android.widget.TextView[@text='交易记录']"))

        page = self

        return page

    @robot_log
    def back_to_high_end_holding_list_page(self):
        self.perform_actions(BACK)

        page = huaxin_ui.ui_android_xjb_3_0.assets_high_end_detail_page.AssetsHighEndDetailPage(self.web_driver)

        return page

