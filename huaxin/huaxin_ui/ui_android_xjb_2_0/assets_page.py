# coding: utf-8

from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
from huaxin_ui.ui_android_xjb_2_0.assets_dqb_detail_page import AssetsDqbDetailPage
from huaxin_ui.ui_android_xjb_2_0.assets_fund_detail_page import AssetsFundDetailPage
from huaxin_ui.ui_android_xjb_2_0.assets_high_end_detail_page import AssetsHighEndDetailPage
from huaxin_ui.ui_android_xjb_2_0.assets_xjb_detail_page import AssetsXjbDetailPage
from huaxin_ui.ui_android_xjb_2_0.bank_card_management_page import BankCardManagementPage
from huaxin_ui.ui_android_xjb_2_0.credit_card_repay_page import CreditCardRepayPage
import huaxin_ui.ui_android_xjb_2_0.assets_my_points_detail_page
import huaxin_ui.ui_android_xjb_2_0.pledge_detail_page


XJB_DETAIL = "xpath_//android.widget.TextView[@text='现金宝']"
DQB_DETAIL = "xpath_//android.widget.TextView[@text='定期宝']"
FUND_DETAIL = "xpath_//android.widget.TextView[@text='基金']"
HIGH_END_DETAIL = "xpath_//android.widget.TextView[@text='高端理财']"

CARD_MANAGEMENT = "xpath_//android.widget.TextView[@text='银行卡管理']"
CREDIT_CARD_REPAY_STOP = "swipe_xpath_//android.widget.TextView[@text='信用卡还款']"
CREDIT_CARD_REPAY = "xpath_//android.widget.TextView[@text='信用卡还款']"
MY_POINTS_STOP = "swipe_xpath_//android.widget.TextView[@text='我的积分']"
MY_POINTS = "xpath_//android.widget.TextView[@text='我的积分']"

HOME = "xpath_//android.widget.RelativeLayout[1]/android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/tab_image']"
FINANCE = "xpath_//android.widget.RelativeLayout[2]/android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/tab_image']"
FUND = "xpath_//android.widget.RelativeLayout[3]/android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/tab_image']"

SWIPE_START = "swipe_xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/title_actionbar']"
SWIPE_STOP = "swipe_xpath_//android.widget.RelativeLayout[@resource-id='com.shhxzq.xjb:id/realcontent']"

SWIPE_BEGAIN = "swipe_xpath_//"
PLEDGE_STOP = "swipe_xpath_//android.widget.TextView[@text='随心借']"
PLEDGE_REPAY_STOP = "swipe_xpath_//android.widget.TextView[@text='%s']"
PLEDGE_REPAY_BUTTON_STOP="swipe_xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/bottom_bt']"
ASSETS_PLEDGE="xpath_//android.widget.RelativeLayout[@resource-id='com.shhxzq.xjb:id/realcontent']"
PLEDGE_BUTTON="xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_vip_pledge_footer_panel']"
PLEDGE_SWIPE_STOP = "swipe_xpath_//android.widget.TextView[@text='%s']"
SELECT_PLEDGE_PRODUCT="xpath_//android.widget.TextView[@text='%s']"
PLEDGE_REPAY="xpath_//android.widget.TextView[@text='%s']"
PLEDGE_REPAY_BUTTON="xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/bottom_bt']"

TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"
PLEDGE_REPAY_DONE="xpath_//android.widget.Button[@text='确认']"


current_page = []


class AssetsPage(PageObject):
    def __init__(self, web_driver):
        super(AssetsPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def go_to_xjb_detail_page(self):
        self.perform_actions(
            XJB_DETAIL,
        )

        page = AssetsXjbDetailPage(self.web_driver)

        return page

    @robot_log
    def go_to_dqb_detail_page(self):
        self.perform_actions(
            DQB_DETAIL,
        )

        page = AssetsDqbDetailPage(self.web_driver)

        return page

    @robot_log
    def go_to_fund_detail_page(self):
        self.perform_actions(
            FUND_DETAIL,
        )

        page = AssetsFundDetailPage(self.web_driver)

        return page

    @robot_log
    def go_to_high_end_detail_page(self):
        self.perform_actions(
            HIGH_END_DETAIL,
        )

        page = AssetsHighEndDetailPage(self.web_driver)

        return page

    @robot_log
    def go_to_bank_card_management_page(self):
        self.perform_actions(
            SWIPE_START, SWIPE_STOP, 'U',
            CARD_MANAGEMENT, )
        page = BankCardManagementPage(self.web_driver)

        return page

    @robot_log
    def go_to_credit_card_repay_page(self):
        self.perform_actions(
            "swipe_xpath_//", CREDIT_CARD_REPAY_STOP, 'U',
            CREDIT_CARD_REPAY,
        )

        page = CreditCardRepayPage(self.web_driver)

        return page

    @robot_log
    def go_to_my_points_page(self):
        self.perform_actions(
            "swipe_xpath_//", MY_POINTS_STOP, 'U',
            MY_POINTS,
        )

        page = huaxin_ui.ui_android_xjb_2_0.assets_my_points_detail_page.AssetsMyPointsDetailPage(self.web_driver)

        return page

    @robot_log
    def go_to_pledge_detail_page(self,product_name):
        self.perform_actions(SWIPE_BEGAIN,PLEDGE_STOP,'U',
                             ASSETS_PLEDGE,
                             PLEDGE_BUTTON,
                             SWIPE_BEGAIN,PLEDGE_SWIPE_STOP % product_name,'U',
                             SELECT_PLEDGE_PRODUCT % product_name
                             )

        page=huaxin_ui.ui_android_xjb_2_0.pledge_detail_page.PledgeDetailPage(self.web_driver)

        return page

    @robot_log
    def pledge_repay(self,product_name,trade_password):
        self.perform_actions(SWIPE_BEGAIN,PLEDGE_STOP,'U',
                             ASSETS_PLEDGE,
                             SWIPE_BEGAIN,PLEDGE_REPAY_STOP % product_name,'U',
                             PLEDGE_REPAY % product_name,
                             SWIPE_BEGAIN,PLEDGE_REPAY_BUTTON_STOP,'U',
                             PLEDGE_REPAY_BUTTON,
                             TRADE_PASSWORD,trade_password,
                             PLEDGE_REPAY_DONE
                             )


