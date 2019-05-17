# coding=utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
from huaxin_ui.ui_android_xjb_3_0.upload_materials_page import UploadMaterialsPage


NEXT = "xpath_//android.widget.Button[@content-desc='下一步']"


class SecurityCenterFindTradePasswordPage(PageObject):
    def __init__(self, web_driver):
        super(SecurityCenterFindTradePasswordPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('上传资料', self.get_text(self.page_title, 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def verify_illustration_details(self):
        self.assert_values('True', str(self.element_exist("//android.view.View[@content-desc='手持证件正面照示例']")))
        self.assert_values('True', str(self.element_exist("//android.view.View[@content-desc='example']")))

        page = self

        return page

    @robot_log
    def go_to_upload_materials_page(self):
        self.perform_actions(NEXT)

        page = UploadMaterialsPage(self.web_driver)

        return page
