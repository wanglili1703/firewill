from selenium.common.exceptions import NoSuchElementException

from _common.adb import Adb
from _common.app_compatibility_install import AppCompatibilityInstall

from _common.global_config import GlobalConfig
from _common.global_controller import GlobalController
from _common.utility import Utility
from _common.web_driver import WebDriver
from _tools.mysql_xjb_tools import MysqlXjbTools
from _tools.restful_xjb_tools import RestfulXjbTools
from huaxin_ui.ui_android_xjb_1_8.main_page import MainPage

HUA_WEI_ACCESS_ALLOW = "//android.widget.Button[@resource-id='com.huawei.systemmanager:id/btn_allow']"


class AndroidXjbTools18(object):
    def __init__(self, app_path, platform_version, device_id, port, package_name):
        self._db = MysqlXjbTools()

        Adb().uninstall_apk(device_id, package_name)

        AppCompatibilityInstall().app_install_handle(device_id, app_path)

        if not Adb().is_package_installed(device_id, package_name):
            AppCompatibilityInstall().app_install_handle(device_id, app_path)

        self.web_driver = WebDriver.Appium().open_android_app(app_path, platform_version, device_id, port)
        self.main_page = MainPage(self.web_driver)

        try:
            button = self.web_driver.find_element_by_xpath(HUA_WEI_ACCESS_ALLOW)
            button.click()
        except NoSuchElementException:
            pass

    def old_user(self, username, login_password):
        self.main_page.go_to_home_page()
        self.main_page.go_to_login_page()
        self.main_page.login(username, login_password, 'HomePage')

    def new_user(self):
        username = Utility.GetData().mobile()
        username, login_password, trade_password = RestfulXjbTools().new_user(username=username,
                                                                              login_password='a0000000',
                                                                              card_bin='622202',
                                                                              trade_password='135790',
                                                                              recharge_amount='10000')
        self.main_page.go_to_home_page()
        self.main_page.go_to_login_page()
        self.main_page.login(username, login_password, 'HomePage')

        return username, login_password, trade_password

    def home_page_recharge(self, username, login_password, recharge_amount, trade_password):
        self.old_user(username=username, login_password=login_password)
        self.main_page.go_to_recharge_page()
        self.main_page.recharge(recharge_amount=recharge_amount, trade_password=trade_password)

    def home_page_regular_withdraw(self, username, login_password, withdraw_amount, trade_password):
        self.old_user(username=username, login_password=login_password)
        self.main_page.go_to_withdraw_page()
        self.main_page.regular_withdraw(withdraw_amount=withdraw_amount, trade_password=trade_password)

    def home_page_fast_withdraw(self, username, login_password, withdraw_amount, trade_password):
        self.old_user(username=username, login_password=login_password)
        self.main_page.go_to_withdraw_page()
        self.main_page.fast_withdraw(withdraw_amount=withdraw_amount, trade_password=trade_password)


if __name__ == '__main__':
    app_path = GlobalController.XJB_CONNECT
    platform_version = '6.0'
    device_id = 'PBV7N16924004496'
    port = '4721'
    package_name = 'com.shhxzq.xjb'

    m = AndroidXjbTools18(app_path=app_path, platform_version=platform_version, device_id=device_id, port=port,
                          package_name=package_name)

    # m.home_page_recharge(username='15666666669', login_password='a0000000', recharge_amount='100',
    #                      trade_password='135790')

    # m.home_page_regular_withdraw(username='15666666669', login_password='a0000000', withdraw_amount='0.1',
    #                              trade_password='135790')

    m.home_page_fast_withdraw(username='15666666669', login_password='a0000000', withdraw_amount='100',
                              trade_password='135790')
