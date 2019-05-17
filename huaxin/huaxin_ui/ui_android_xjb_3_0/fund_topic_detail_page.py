# coding=utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.fund_page_fund_detail
ILLUSTRATION = "//android.widget.TextView[contains(@text,'中长期业绩名列在售基金前茅')]"
FUND = "xpath_//android.widget.TextView[contains(@text,'%s')]"


class FundTopicDetailPage(PageObject):
    def __init__(self, web_driver):
        super(FundTopicDetailPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('主题详情', self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def verify_page_illustration(self):
        self.assert_values('绩效优异 价值之选', self.get_text('com.shhxzq.xjb:id/tv_topic_header_title', 'find_element_by_id'))
        self.assert_values('让您轻松选好基', self.get_text('com.shhxzq.xjb:id/tv_topic_header_intro', 'find_element_by_id'))
        self.assert_values(True, self.element_exist(ILLUSTRATION))

        page = self
        return page

    @robot_log
    def go_to_fund_detail_page(self, fund_product):
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='近一年涨幅']"))
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='混合型']"))
        self.perform_actions(FUND % fund_product)

        page = huaxin_ui.ui_android_xjb_3_0.fund_page_fund_detail.FundPageFundDetail(self.web_driver)
        return page
