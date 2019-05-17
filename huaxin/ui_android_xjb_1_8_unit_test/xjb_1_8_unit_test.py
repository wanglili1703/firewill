import time
from robot.api.deco import keyword

from _tools.ui_android_xjb_tools_1_8 import AndroidXjbTools18


class UiAndroidXjb18UnitTest:
    @keyword('Set Environemt Args')
    def set_environemt_args(self, app_path, platform_version, device_id, port, package_name):
        self.xjb = AndroidXjbTools18(app_path, platform_version, device_id, port, package_name)
        self.xjb.main_page.screen_shot()

    @keyword('Case Tear Down')
    def tear_down(self):
        time.sleep(1)
        self.xjb.main_page.screen_shot()
        self.xjb.web_driver.quit()
        return

    @keyword('test_home_page_recharge')
    def home_page_recharge(self):
        self.xjb.home_page_recharge(username='15666666669', login_password='a0000000', recharge_amount='100',
                                    trade_password='135790')

    @keyword('test_home_page_regular_withdraw')
    def home_page_regular_withdraw(self):
        self.xjb.home_page_regular_withdraw(username='15666666669', login_password='a0000000', withdraw_amount='0.1',
                                            trade_password='135790')
