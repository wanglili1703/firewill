# coding=utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.fund_topic_detail_page

ILLUSTRATION = "//android.widget.TextView[contains(@text,'热门主题致力于驾驭优质投资基金')]"
TOPIC = "xpath_//android.widget.TextView[@text='绩效优异 价值之选']"


class FundHotTopicsPage(PageObject):
    def __init__(self, web_driver):
        super(FundHotTopicsPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('热门主题', self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def verify_page_illustration(self):
        self.assert_values(True, self.element_exist(ILLUSTRATION))

        page = self
        return page

    @robot_log
    def go_to_topic_detail_page(self):
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='近一年最高']"))
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='让您轻松选好基']"))
        self.perform_actions(TOPIC)

        page = huaxin_ui.ui_android_xjb_3_0.fund_topic_detail_page.FundTopicDetailPage(self.web_driver)
        return page
