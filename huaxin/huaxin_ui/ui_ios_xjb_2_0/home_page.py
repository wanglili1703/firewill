# coding=utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
from huaxin_ui.ui_ios_xjb_2_0.assets_page import AssetsPage
from huaxin_ui.ui_ios_xjb_2_0.finance_page import FinancePage
from huaxin_ui.ui_ios_xjb_2_0.fund_page import FundPage
from huaxin_ui.ui_ios_xjb_2_0.home_essence_recommend_page import HomeEssenceRecommendPage
from huaxin_ui.ui_ios_xjb_2_0.login_page import LoginPage
from huaxin_ui.ui_ios_xjb_2_0.message_center import MessageCenterPage
from huaxin_ui.ui_ios_xjb_2_0.personal_center_page import PersonalCenterPage
from huaxin_ui.ui_ios_xjb_2_0.recharge_page import RechargePage
from huaxin_ui.ui_ios_xjb_2_0.withdraw_page import WithdrawPage

WITHDRAW = "accId_UIAButton_取出"
RECHARGE = "accId_UIAButton_存入"

LOGIN_REGISTER = "accId_UIAButton_(UIButton_登录 / 注册)"

PERSONAL_CENTER = "accId_UIAButton_UIBarButtonItemLocationLeft"

HOME = "accId_UIAButton_(UITabBarButton_)"
FINANCE = "accId_UIAButton_(UITabBarButton_item_1)"
FUND = "accId_UIAButton_(UITabBarButton_item_2)"
ASSETS = "accId_UIAButton_(UITabBarButton_item_3)"

ESSENCE_RECOMMEND = "accId_UIAButton_精品推荐"

MESSAGE_CENTER = "accId_UIAButton_UIBarButtonItemLocationRight"

current_page = []


class HomePage(PageObject):
    def __init__(self, web_driver):
        super(HomePage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def go_to_personal_center_page(self):
        self.perform_actions(PERSONAL_CENTER)
        page = PersonalCenterPage(self.web_driver)

        return page

    @robot_log
    def go_to_login_page(self):
        self.perform_actions(
            LOGIN_REGISTER,
        )
        page = LoginPage(self.web_driver)

        return page

    @robot_log
    def go_to_finance_page(self):
        self.perform_actions(FINANCE)
        page = FinancePage(self.web_driver)

        return page

    @robot_log
    def go_to_fund_page(self):
        self.perform_actions(FUND)
        page = FundPage(self.web_driver)

        return page

    @robot_log
    def go_to_assets_page(self):
        self.perform_actions(ASSETS)
        page = AssetsPage(self.web_driver)

        return page

    @robot_log
    def go_to_recharge_page(self):
        self.perform_actions(RECHARGE)
        page = RechargePage(self.web_driver)
        return page

    @robot_log
    def go_to_withdraw_page(self):
        self.perform_actions(WITHDRAW)
        page = WithdrawPage(self.web_driver)
        return page

    @robot_log
    def go_to_essence_recommend_page(self):
        self.perform_actions(ESSENCE_RECOMMEND)
        page = HomeEssenceRecommendPage(self.web_driver)
        return page

    @robot_log
    def go_to_message_center_page(self):
        self.perform_actions(MESSAGE_CENTER)
        page = MessageCenterPage(self.web_driver)
        return page
