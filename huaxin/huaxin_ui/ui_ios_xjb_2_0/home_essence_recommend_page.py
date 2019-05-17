# coding=utf-8
from _common.page_object import PageObject

from _common.xjb_decorator import robot_log

ESSENCE_RECOMMEND = "swipe_accId_精品推荐"
ESSENCE_RECOMMEND_END = "swipe_accId_上海华信证券荣誉出品"

current_page = []


class HomeEssenceRecommendPage(PageObject):
    def __init__(self, web_driver):
        super(HomeEssenceRecommendPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def view_essence_recommend_list(self):
        self.perform_actions(
            ESSENCE_RECOMMEND, ESSENCE_RECOMMEND_END, 'U',
        )
