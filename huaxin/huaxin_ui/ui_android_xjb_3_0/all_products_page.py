# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log

SWIPE_BEGIN="swipe_xpath_//"
PRODUCTS_WITHIN_THREE_MONTH="xpath_//android.widget.TextView[@text='0-3个月']"
PRODUCTS_WITHIN_SIX_MONTH="xpath_//android.widget.TextView[@text='3-6个月']"
PRODUCTS_OVER_SIX_MONTH="xpath_//android.widget.TextView[@text='6个月以上']"
FILTER="xpath_//android.widget.Button[@text='筛选']"
FILTER_ITEM="xpath_//android.widget.CheckBox[@text='%s']"
COMFIRM="xpath_//android.widget.Button[@text='确定']"

class AllProductsPage(PageObject):
    def __init__(self, web_driver):
        super(AllProductsPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('全部产品', self.get_text(self.page_title, 'find_element_by_id'))
        self.assert_values('筛选', self.get_text('com.shhxzq.xjb:id/btn_actionbar_right','find_element_by_id'))

        page = self
        return page

    @robot_log
    def view_all_products(self):
        self.assert_values('True', str(self.element_exist("//android.widget.TextView[@text='年化业绩比较基准']")))
        self.perform_actions(PRODUCTS_WITHIN_THREE_MONTH)
        self.assert_values('True', str(self.element_exist("//android.widget.TextView[@text='年化业绩比较基准']")))
        self.perform_actions(PRODUCTS_WITHIN_SIX_MONTH)
        self.assert_values('True', str(self.element_exist("//android.widget.TextView[@text='年化业绩比较基准']")))
        self.perform_actions(PRODUCTS_OVER_SIX_MONTH)
        self.assert_values('True', str(self.element_exist("//android.widget.TextView[@text='年化业绩比较基准']")))

        page = self
        return page

    @robot_log
    def go_to_filter_detail_page(self):
        self.perform_actions(FILTER)

        page = self
        return page

    @robot_log
    def verify_filter_details(self):
        self.assert_values('取消', self.get_text('com.shhxzq.xjb:id/btn_actionbar_right','find_element_by_id'))
        self.assert_values('True',str(self.element_exist("//android.widget.TextView[@text='产品类型']")))
        self.assert_values('True',str(self.element_exist("//android.widget.TextView[@text='起投金额']")))

        page = self
        return page

    @robot_log
    def products_filter(self, product_type=None, amount_type=None):
        if product_type is None and amount_type is not None:
            self.perform_actions(FILTER_ITEM % amount_type)
        elif product_type is not None and amount_type is None:
            self.perform_actions(FILTER_ITEM % product_type)

        self.perform_actions(COMFIRM)

        page = self
        return page





