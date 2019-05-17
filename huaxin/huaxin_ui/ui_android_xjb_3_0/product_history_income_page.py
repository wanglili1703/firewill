# coding=utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.fund_page_fund_detail
import huaxin_ui.ui_android_xjb_3_0.product_detail_page

BACK = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/actionbar_back']"
BACKWARDS = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left']"
BONUS_DIVISION = "xpath_//android.widget.TextView[@text='日期']/../../../../../preceding-sibling::android.support.v7.widget.LinearLayoutCompat[1]/android.view.View[@index='1']"


class ProductHistoryIncomePage(PageObject):
    def __init__(self, web_driver):
        super(ProductHistoryIncomePage, self).__init__(web_driver)
        self._return_page = {
            'FundPageFundDetail': huaxin_ui.ui_android_xjb_3_0.fund_page_fund_detail.FundPageFundDetail(
                self.web_driver),
            'ProductDetailPage': huaxin_ui.ui_android_xjb_3_0.product_detail_page.ProductDetailPage(
                self.web_driver)
        }

    @robot_log
    def verify_page_title(self, fund_product_name=None, product_type='fund'):
        if product_type == 'fund':
            self.assert_values(True,
                               self.element_exist(
                                   "//android.widget.TextView[contains(@text,'%s')]" % fund_product_name))
        elif product_type == '现金管理系列':
            self.assert_values('历史收益', self.get_text(self.page_title, 'find_element_by_id'))
        else:
            self.assert_values('历史净值', self.get_text(self.page_title, 'find_element_by_id'))
        page = self

        return page

    @robot_log
    def view_product_history_income(self, product_type='混合型'):
        if product_type == '混合型' or product_type == '精选系列':
            self.assert_values(True, self.element_exist("//android.widget.TextView[@text='日期']"))
            self.assert_values('单位净值', self.get_text('com.shhxzq.xjb:id/incomeunit_name', 'find_element_by_id'))
            self.assert_values('累计净值', self.get_text('com.shhxzq.xjb:id/incom_total_name', 'find_element_by_id'))
            self.assert_values('日涨跌幅', self.get_text('com.shhxzq.xjb:id/day_rise', 'find_element_by_id'))
            if product_type == '混合型':
                self.perform_actions(BONUS_DIVISION)
        elif product_type == '货币型' or product_type == '现金管理系列':
            self.assert_values(True, self.element_exist("//android.widget.TextView[@text='日期']"))
            self.assert_values('七日年化收益率', self.get_text('com.shhxzq.xjb:id/incomeunit_name', 'find_element_by_id'))
            self.assert_values('日每万份收益(元)', self.get_text('com.shhxzq.xjb:id/incom_total_name', 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def back_to_product_detail_page(self, return_page='FundPageFundDetail', product_type='fund'):
        if product_type == 'fund':
            self.perform_actions(BACK)
        else:
            self.perform_actions(BACKWARDS)

        page = self._return_page[return_page]

        return page
