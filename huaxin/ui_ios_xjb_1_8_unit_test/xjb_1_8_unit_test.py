import time
from robot.api.deco import keyword

from _tools.ui_ios_xjb_tools_1_8 import IOSXjbTools18


class UiIosXjb18UnitTest:
    @keyword('Set Environemt Args')
    def set_environemt_args(self, app_path, platform_version, device_id, port, package_name):
        self.xjb = IOSXjbTools18(app_path, platform_version, device_id, port, package_name)
        self.xjb.main_page.screen_shot()

    @keyword('Case Tear Down')
    def tear_down(self):
        time.sleep(1)
        self.xjb.main_page.screen_shot()
        self.xjb.web_driver.quit()
        return

    @keyword('test_go_to_home_page')
    def go_to_home_page(self):
        self.xjb.go_to_home_page()
        pass
