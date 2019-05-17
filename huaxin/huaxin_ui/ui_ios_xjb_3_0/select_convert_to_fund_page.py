# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.fund_convert_page
import huaxin_ui.ui_ios_xjb_3_0.fund_holding_detail_page
import huaxin_ui.ui_ios_xjb_3_0.fund_product_search_page

SWIPE_BEGIN = "swipe_xpath_//"
FUND_CONVERT_SWIPE_STOP = "swipe_xpath_//android.widget.TextView[contains(@text,'%s')]/../following-sibling::android.widget.LinearLayout[1]/android.widget.RelativeLayout"
FUND_CONVERT = "xpath_//android.widget.TextView[contains(@text,'%s')]/../following-sibling::android.widget.LinearLayout[1]/]android.widget.RelativeLayout"
BACK = "accId_UIAButton_UIBarButtonItemLocationLeft"
SEARCH = "accId_UIAButton_UIBarButtonItemLocationRight"


class SelectConvertToFundPage(PageObject):
    def __init__(self, web_driver):
        super(SelectConvertToFundPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('选择转入基金', self.get_text("//UIAStaticText[@label='选择转入基金']"))

        page = self
        return page

    @robot_log
    def go_to_fund_convert_page(self, fund_product):
        self.perform_actions(SWIPE_BEGIN, FUND_CONVERT_SWIPE_STOP % fund_product, 'U')
        self.perform_actions(FUND_CONVERT % fund_product)

        page = huaxin_ui.ui_ios_xjb_3_0.fund_convert_page.FundConvertPage(self.web_driver)

        return page

    @robot_log
    def back_to_fund_holding_page(self):
        self.perform_actions(BACK)

        page = huaxin_ui.ui_ios_xjb_3_0.fund_holding_detail_page.FundHoldingDetailPage(self.web_driver)
        return page

    @robot_log
    def go_to_fund_product_search_page(self):
        self.perform_actions(SEARCH)

        page = huaxin_ui.ui_ios_xjb_3_0.fund_product_search_page.FundProductSearchPage(self.web_driver)
        return page
