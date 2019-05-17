# coding=utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log, dialog_close
from _common.global_config import ASSERT_DICT
from huaxin_ui.ui_android_xjb_3_0.assets_page import AssetsPage
from huaxin_ui.ui_android_xjb_3_0.finance_page import FinancePage
from huaxin_ui.ui_android_xjb_3_0.fund_page import FundPage
import huaxin_ui.ui_android_xjb_3_0.login_page
import huaxin_ui.ui_android_xjb_3_0.recharge_page
import huaxin_ui.ui_android_xjb_3_0.withdraw_page
import huaxin_ui.ui_android_xjb_3_0.deposit_salary_page
from huaxin_ui.ui_android_xjb_3_0.message_center_page import MessageCenterPage
import huaxin_ui.ui_android_xjb_3_0.assets_associator_center_page
import huaxin_ui.ui_android_xjb_3_0.financing_calendar_page
import huaxin_ui.ui_android_xjb_3_0.global_search_page
import time
import re

WITHDRAW = "xpath_//android.widget.TextView[@text='取出']"
RECHARGE = "xpath_//android.widget.TextView[@text='存入']"

LOGIN_REGISTER = "xpath_//android.widget.TabWidget/android.widget.RelativeLayout[5]"
LOGIN = "xpath_//android.widget.Button[@text='登录']"
PERSONAL_CENTER = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/img_home_actionbar_left']"

HOME = "xpath_//android.widget.RelativeLayout[1]/android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/tab_image']"
FINANCE = "xpath_//android.widget.RelativeLayout[2]/android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/tab_image']"
FUND = "xpath_//android.widget.RelativeLayout[3]/android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/tab_image']"
ASSETS = "xpath_//android.widget.RelativeLayout[5]/android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/tab_image']"

SWIPE_START = "swipe_xpath_//"
INDEX_STOP = "swipe_xpath_//android.widget.TextView[@text='了解华信现金宝']"
# INDEX_STOP = "swipe_xpath_//android.widget.TextView[@text='热门资讯']"
ESSENCE_RECOMMEND = "xpath_//android.widget.TextView[@text='热门资讯']"
DEPOSITE_SALARY = "xpath_//android.widget.TextView[@text='存工资']"

HOME_PAGE = "xpath_//android.widget.TabWidget/android.widget.RelativeLayout[1]"
MESSAGE_CENTER = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/img_home_actionbar_right']"
SETTINGS_BUTTON = "xpath_//android.widget.ImageButton[@resource-id='com.shhxzq.xjb:id/ibtn_actionbar_right']"
POP_DIALOG_CLOSE = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/img_dialog_close'][POP]"
CALENDAR = "xpath_//android.widget.TextView[@text='理财日历']"
CALENDAR_STOP = "swipe_xpath_//android.widget.TextView[@text='%s']"
SCROLL = "swipe_xpath_//scroll_2"
MORE_STOP = "swipe_xpath_//android.widget.TextView[@text='查看更多']"
MORE = "xpath_//android.widget.TextView[@text='查看更多']"
MASK_KNOW = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_mask_know'][POP]"
SEARCH_BAR = "xpath_//android.widget.TextView[@text='高端理财/定活宝/基金']"
current_page = []


class HomePage(PageObject):
    def __init__(self, web_driver):
        super(HomePage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    @dialog_close
    def go_to_login_page(self):
        self.perform_actions(LOGIN_REGISTER,
                             LOGIN)
        page = huaxin_ui.ui_android_xjb_3_0.login_page.LoginPage(self.web_driver)

        return page

    @robot_log
    def go_to_finance_page(self):
        self.perform_actions(FINANCE,
                             MASK_KNOW)
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
    def go_to_recharge_page_from_home_page(self):
        self.perform_actions(RECHARGE)
        page = huaxin_ui.ui_android_xjb_3_0.recharge_page.RechargePage(self.web_driver)
        return page

    @robot_log
    def go_to_withdraw_page(self):
        self.perform_actions(WITHDRAW)
        page = huaxin_ui.ui_android_xjb_3_0.withdraw_page.WithdrawPage(self.web_driver)
        return page

    @robot_log
    def go_to_essence_recommend_page(self):
        self.perform_actions(SWIPE_START, INDEX_STOP, 'U')
        #     ESSENCE_RECOMMEND)
        # page = HomeEssenceRecommendPage(self.web_driver)

        page = self

        return page

    @robot_log
    def go_to_deposit_salary_page(self):
        self.perform_actions(DEPOSITE_SALARY)
        time.sleep(5)

        page = huaxin_ui.ui_android_xjb_3_0.deposit_salary_page.DepositSalaryPage(self.web_driver)
        return page

    @robot_log
    def go_to_message_center_page(self):
        self.perform_actions(MESSAGE_CENTER)
        page = MessageCenterPage(self.web_driver)
        return page

    @robot_log
    def go_to_financing_calendar_page(self):
        self.perform_actions(CALENDAR)
        page = huaxin_ui.ui_android_xjb_3_0.financing_calendar_page.FinancingCalendarPage(self.web_driver)
        return page

    @robot_log
    def click_more_go_to_financing_calendar_page(self):
        self.perform_actions(SWIPE_START, MORE_STOP, 'U')
        self.perform_actions(MORE)
        page = huaxin_ui.ui_android_xjb_3_0.financing_calendar_page.FinancingCalendarPage(self.web_driver)
        return page

    @robot_log
    def verify_financing_calendar_items(self, reserved_pay_amount, last_card_no, item=None):
        if item == '信用卡预约还款':
            self.perform_actions(SWIPE_START, CALENDAR_STOP % item, 'U')
            self.perform_actions(SWIPE_START, SCROLL, 'U')
            calendar_content = self.get_text('com.shhxzq.xjb:id/tv_item_calendar_content', 'find_element_by_id')
            reserve_repay_expected = re.findall(r'(\d+(.\d+)*)', calendar_content)
            reserve_repay_card_no_expected = reserve_repay_expected[0][0]
            reserve_repay_date_expected = reserve_repay_expected[1][0] + '月' + reserve_repay_expected[2][0] + '日'
            reserve_repay_amount_expected = reserve_repay_expected[3][0]

            self.assert_values(last_card_no, reserve_repay_card_no_expected)
            # self.assert_values(ASSERT_DICT['deduction_date'], reserve_repay_date_expected)
            # self.assert_values('%.2f' % float(reserved_pay_amount), '%.2f' % float(reserve_repay_amount_expected))
            # self.assert_values('3.00', '%.2f' % float(reserve_repay_amount_expected))

        page = self
        return page

    @robot_log
    def go_to_global_search_page(self):
        self.perform_actions(SEARCH_BAR)

        page = huaxin_ui.ui_android_xjb_3_0.global_search_page.GlobalSearchPage(self.web_driver)
        return page
