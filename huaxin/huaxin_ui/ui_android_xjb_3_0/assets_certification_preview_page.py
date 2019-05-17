# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log

DOWNLOAD="xpath_//android.widget.TextView[@text='下载']"
FILE_OPEN_WAY="xpath_//android.widget.TextView"
ALLOW="xpath_//android.widget.Button[@resource-id='com.android.packageinstaller:id/permission_allow_button']"

class AssetsCertificationPreviewPage(PageObject):
    def __init__(self, web_driver):
        super(AssetsCertificationPreviewPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('资产证明预览', self.get_text(self.page_title, 'find_element_by_id'))

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
        # self.assert_values('使用以下方式打开',self.get_text('android:id/alertTitle','find_element_by_id'))
        self.assert_values('使用WPS Office打开',self.get_text('miui:id/alertTitle','find_element_by_id'))

        page = self
        return page

