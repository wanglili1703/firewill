from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
from huaxin_ui.ui_android_xjb_1_8.assets_page import AssetsPage
from huaxin_ui.ui_android_xjb_1_8.finance_page import FinancePage
from huaxin_ui.ui_android_xjb_1_8.login_page import LoginPage
from huaxin_ui.ui_android_xjb_1_8.personal_center_page import PersonalCenterPage
from huaxin_ui.ui_android_xjb_1_8.recharge_page import RechargePage
from huaxin_ui.ui_android_xjb_1_8.withdraw_page import WithdrawPage

WITHDRAW_BUTTON = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_home_enchashment']"
RECHARGE_BUTTON = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_home_recharge']"

LOGIN_REGISTER_BUTTON = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_home_not_login_entrance']"
FINANCE_BUTTON = "xpath_//android.widget.RelativeLayout[2]/android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/tab_image']"
ASSETS_BUTTON = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/tab_image']"
PERSONAL_CENTER_BUTTON = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/img_home_actionbar_left']"

current_page = []


class HomePage(PageObject):
    def __init__(self, web_driver):
        super(HomePage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def go_to_login_page(self):
        self.perform_actions(LOGIN_REGISTER_BUTTON)
        page = LoginPage(self.web_driver)

        return page

    @robot_log
    def go_to_finance_page(self):
        self.perform_actions(FINANCE_BUTTON)
        page = FinancePage(self.web_driver)

        return page

    @robot_log
    def go_to_assets_page(self):
        self.perform_actions(ASSETS_BUTTON)
        page = AssetsPage(self.web_driver)

        return page

    @robot_log
    def go_to_personal_center_page(self):
        self.perform_actions(PERSONAL_CENTER_BUTTON)
        page = PersonalCenterPage(self.web_driver)

        return page

    @robot_log
    def go_to_recharge_page(self):
        self.perform_actions(RECHARGE_BUTTON)
        page = RechargePage(self.web_driver)
        return page

    @robot_log
    def go_to_withdraw_page(self):
        self.perform_actions(WITHDRAW_BUTTON)
        page = WithdrawPage(self.web_driver)
        return page
