# coding=utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log

INDEX_START = "swipe_xpath_//android.widget.TextView[@text='市场指数']"
INDEX_STOP = "swipe_xpath_//android.widget.TextView[@text='%s']"
CSI_INDEX = "xpath_//android.widget.TextView[@text='%s']"
INDEX_TYPE_STOP = "swipe_xpath_//android.widget.TextView[@text='%s']"


class FundMarketIndexPage(PageObject):
    def __init__(self, web_driver):
        super(FundMarketIndexPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('市场指数', self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def verify_index_type(self, index_type, index_name):
        self.perform_actions(INDEX_START, INDEX_TYPE_STOP % index_type, 'U')
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='%s']" % index_name))

        page = self
        return page

    # 基金频道--市场指数
    @robot_log
    def fund_market_index(self, csi_index):
        self.perform_actions(
            INDEX_START, INDEX_STOP % csi_index, 'U',
                         CSI_INDEX % csi_index
        )

        page = self
        return page
