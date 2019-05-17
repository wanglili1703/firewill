# coding=utf-8
from _common.page_object import PageObject

from _common.xjb_decorator import robot_log

ESSENCE_RECOMMEND = u"swipe_xpath_//android.widget.TextView[@text='资讯']"
ESSENCE_RECOMMEND_END = u"swipe_xpath_//android.widget.TextView[@text='了解华信现金宝']"
ALL="xpath_//android.widget.TextView[@text='全部']"
RESEARCH_REPORT="xpath_//android.widget.TextView[@text='研究报告']"
INSTITUTION_VIEWPOINT="xpath_//android.widget.TextView[@text='机构观点']"
TALENT_FUND_DISCUSSION = "xpath_//android.widget.TextView[@text='达人论基']"


current_page = []


class HomeEssenceRecommendPage(PageObject):
    def __init__(self, web_driver):
        super(HomeEssenceRecommendPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def view_essence_recommend_list(self):
        self.perform_actions(
            RESEARCH_REPORT,
            INSTITUTION_VIEWPOINT,
            TALENT_FUND_DISCUSSION
            # ESSENCE_RECOMMEND, ESSENCE_RECOMMEND_END, 'U',
        )
