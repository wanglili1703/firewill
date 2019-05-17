# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log

SWIPE_BEGIN = "swipe_xpath_//"
PRODUCTS_WITHIN_THREE_MONTH = "xpathIOS_UIAButton_//UIAButton[@label='0-3个月 ']"
PRODUCTS_WITHIN_SIX_MONTH = "xpathIOS_UIAButton_//UIAButton[@label='3-6个月 ']"
PRODUCTS_OVER_SIX_MONTH = "xpathIOS_UIAButton_//UIAButton[@label='6个月以上 ']"
PRODUCTS_ALL = "xpathIOS_UIAButton_//UIAButton[@label='全部 ']"
FILTER = "accId_UIAButton_(UIButton_筛选)"
FILTER_ITEM = "accId_UIAButton_(UIButton_%s)"
CONFIRM = "accId_UIAButton_确定"


class AllProductsPage(PageObject):
    def __init__(self, web_driver):
        super(AllProductsPage, self).__init__(web_driver)

    @robot_log
    def verify_at_all_products_page(self):
        self.assert_values('全部产品', self.get_text("//UIAStaticText[@label='全部产品']"))

        page = self
        return page

    @robot_log
    def view_all_products(self):
        self.assert_values(True, self.element_exist("(年化业绩比较基准)", "find_element_by_accessibility_id"))
        self.perform_actions(PRODUCTS_WITHIN_THREE_MONTH)
        self.assert_values(True, self.element_exist("(年化业绩比较基准)", "find_element_by_accessibility_id"))
        self.perform_actions(PRODUCTS_WITHIN_SIX_MONTH)
        self.assert_values(True, self.element_exist("(年化业绩比较基准)", "find_element_by_accessibility_id"))
        self.perform_actions(PRODUCTS_OVER_SIX_MONTH)
        self.assert_values(True, self.element_exist("(年化业绩比较基准)", "find_element_by_accessibility_id"))
        self.perform_actions(PRODUCTS_ALL)
        self.assert_values(True, self.element_exist("(年化业绩比较基准)", "find_element_by_accessibility_id"))

        page = self
        return page

    @robot_log
    def go_to_filter_detail_page(self):
        self.perform_actions(FILTER)

        page = self
        return page

    @robot_log
    def verify_filter_details(self):
        self.assert_values('取消', self.get_text('取消', 'find_element_by_accessibility_id'))
        self.assert_values(True, self.element_exist("//UIAStaticText[@label='产品类型']"))
        self.assert_values(True, self.element_exist("//UIAStaticText[@label='起投金额']"))

        page = self
        return page

    @robot_log
    def products_filter(self, product_type=None, amount_type=None):
        if product_type is None and amount_type is not None:
            self.perform_actions(FILTER_ITEM % amount_type)
        elif product_type is not None and amount_type is None:
            self.perform_actions(FILTER_ITEM % product_type)

        self.perform_actions(CONFIRM)

        page = self
        return page
