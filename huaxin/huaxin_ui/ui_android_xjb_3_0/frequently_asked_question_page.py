# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.product_detail_page

QUESTION = "xpath_//android.view.View[contains(@content-desc,'1.')]"
BACK = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left']"


class FrequentlyAskedQuestionPage(PageObject):
    def __init__(self, web_driver):
        super(FrequentlyAskedQuestionPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('常见问题', self.get_text(self.page_title, 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def view_question_detail(self):
        self.perform_actions(QUESTION)
        self.assert_values(True, self.element_exist("//android.view.View[contains(@content-desc,'答：')]"))

        page = self

        return page

    @robot_log
    def back_to_product_detail_page(self):
        self.perform_actions(BACK)

        page = huaxin_ui.ui_android_xjb_3_0.product_detail_page.ProductDetailPage(self.web_driver)

        return page
