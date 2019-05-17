# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log

DOWNLOAD = "accId_UIAStaticText_下载"
ALLOW = ""
APPLY_PAPER = "accId_UIAButton_申请纸质版"


class AssetsCertificationPreviewPage(PageObject):
    def __init__(self, web_driver):
        super(AssetsCertificationPreviewPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('资产证明预览', self.get_text("//UIAStaticText[@label='资产证明预览']"))

        page = self
        return page

    @robot_log
    def close_alert(self):
        self.perform_actions(ALLOW)

        page = self
        return page

    @robot_log
    def download_assets_certification(self):
        self.perform_actions(DOWNLOAD)

        page = self
        return page

    @robot_log
    def verify_alert_title(self):
        self.assert_values(True, self.element_exist("打印", "find_element_by_accessibility_id"))

        page = self
        return page

    @robot_log
    def apply_for_paper_offline(self):
        self.perform_actions(APPLY_PAPER)

        page = self
        return page
