from _common.adb import Adb
from _common.app_compatibility_install import AppCompatibilityInstall
from _common.utility import Utility
from _common.web_driver import WebDriver
from huaxin_ui.ui_ios_xjb_1_8.main_page import MainPage


class IOSXjbTools18(object):
    def __init__(self, app_path, platform_version, device_id, port, package_name):
        # Adb().uninstall_apk(device_id, package_name)
        #
        # AppCompatibilityInstall().app_install_handle(device_id, app_path)
        #
        # if not Adb().is_package_installed(device_id, package_name):
        #     AppCompatibilityInstall().app_install_handle(device_id, app_path)

        self.web_driver = WebDriver.Appium().open_ios_app(app_path, platform_version, device_id, port)
        self.main_page = MainPage(self.web_driver)

    def ui_flow_msg(self):
        print '\r\n'
        print 'ui_flow_is_ '
        for i in self.main_page.ui_flow:
            print i

    def go_to_home_page(self):
        phone_number = '15666666669'
        password = 'a0000000'

        self.main_page.go_to_home_page()
        self.main_page.go_to_login_page()
        self.main_page.login(phone_number, password)

        self.ui_flow_msg()


        # def run_app(self, app_path, platform_version, device_id, port):
        #     web_driver = WebDriver.Appium().open_android_app(app_path, platform_version, device_id, port)
        #     main_page = MainPage(web_driver)
        #     main_page.go_to_home_page()
        #     main_page.go_to_login_page()
        #     print main_page.current_xjb_page
        #     print main_page._ui_flow.keys()


if __name__ == '__main__':
    # app_path = Utility.GetOsPath().get_father_path() + '/apps/hxxjb-uat-latest.apk'
    # AndroidXjbTools20().run_app(app_path=app_path, platform_version='5.1',
    #                             device_id='810EBMC43NGC', port='4723')

    m = IOSXjbTools18(app_path='',
                      platform_version='',
                      device_id='',
                      port='',
                      package_name='')

    m.go_to_home_page()