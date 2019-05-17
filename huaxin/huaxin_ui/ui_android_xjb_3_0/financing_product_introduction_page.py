# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import time
import huaxin_ui.ui_android_xjb_3_0.finance_high_end_page

MORE_PRODUCT = "xpath_//android.widget.Button[@content-desc='查看更多产品']"
SWIPE_BEGIN = "swipe_xpath_//"
MORE_PRODUCT_STOP = "swipe_xpath_//android.view.View[@instance='58']"


class FinancingProductIntroductionPage(PageObject):
    def __init__(self, web_driver):
        super(FinancingProductIntroductionPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('产品介绍', self.get_text(self.page_title, 'find_element_by_id'))
        self.assert_values(True, self.element_exist("//android.view.View[@content-desc='高端理财']"))

        page = self

        return page

    @robot_log
    def go_to_finance_high_end_page(self):
        # print self.web_driver.page_source
        self.perform_actions(SWIPE_BEGIN, MORE_PRODUCT_STOP, 'U')
        self.perform_actions(MORE_PRODUCT)
        page = huaxin_ui.ui_android_xjb_3_0.finance_high_end_page.FinanceHighEndPage(
            self.web_driver)

        return page
