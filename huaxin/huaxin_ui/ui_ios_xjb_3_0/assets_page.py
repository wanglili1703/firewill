# coding: utf-8
import time

from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
from huaxin_ui.ui_ios_xjb_3_0.assets_dqb_detail_page import AssetsDqbDetailPage
from huaxin_ui.ui_ios_xjb_3_0.assets_fund_detail_page import AssetsFundDetailPage
from huaxin_ui.ui_ios_xjb_3_0.assets_high_end_detail_page import AssetsHighEndDetailPage
from huaxin_ui.ui_ios_xjb_3_0.assets_xjb_detail_page import AssetsXjbDetailPage
from huaxin_ui.ui_ios_xjb_3_0.bank_card_management_page import BankCardManagementPage
from huaxin_ui.ui_ios_xjb_3_0.credit_card_repay_page import CreditCardRepayPage
import huaxin_ui.ui_ios_xjb_3_0.assets_my_points_detail_page
import huaxin_ui.ui_ios_xjb_3_0.pledge_page
from huaxin_ui.ui_ios_xjb_3_0.invite_friend_page import InviteFriendPage
from huaxin_ui.ui_ios_xjb_3_0.personal_setting_page import PersonalSettingPage
from huaxin_ui.ui_ios_xjb_3_0.reservation_code_page import ReservationCodePage
from huaxin_ui.ui_ios_xjb_3_0.repay_loan_page import RepayLoanPage
import huaxin_ui.ui_ios_xjb_3_0.my_coupons_list_page
import huaxin_ui.ui_ios_xjb_3_0.assets_analysis_page
import huaxin_ui.ui_ios_xjb_3_0.welfare_center_home_page
import huaxin_ui.ui_ios_xjb_3_0.personal_information_page
import huaxin_ui.ui_ios_xjb_3_0.assets_associator_center_page

# TOTAL_DETAIL = "accId_UIAStaticText_(我的总资产)"
TOTAL_DETAIL = "xpathIOS_UIAStaticText_//UIAStaticText[contains(@label, '累计盈亏(元)')]"
CANCEL = "accId_UIACollectionCell_取消[POP]"
XJB_DETAIL = "accId_UIAStaticText_(现金宝)"
DQB_DETAIL = "accId_UIAStaticText_(定活宝)"
FUND_DETAIL = "accId_UIAStaticText_(基金)"
HIGH_END_DETAIL = "accId_UIAStaticText_(高端)"
MEMBER_CENTER = "accId_UIAStaticText_会员中心"

# CARD_MANAGEMENT = "accId_UIAStaticText_银行卡管理"
CARD_MANAGEMENT = "accId_UIAButton_(UIButton_银行卡)"
CARD_MANAGEMENT_TIPS = "accId_UIAStaticText_(￼  您尚未绑卡，请去绑卡)"
# CREDIT_CARD_REPAY = "accId_UIAStaticText_信用卡还款"
CREDIT_CARD_REPAY = "accId_UIAStaticText_还信用卡"
MY_COUPONS = "accId_UIAStaticText_我的优惠券"
MY_POINTS_STOP = "swipe_accId_活动中心"
MY_POINTS = "xpathIOS_UIAStaticText_//UIATableCell/UIAStaticText[@label='我的积分']"

HOME = "accId_UIAButton_(UITabBarButton_)"
FINANCE = "accId_UIAButton_(UITabBarButton_item_1)"
FUND = "accId_UIAButton_(UITabBarButton_item_2)"

SWIPE_START = "swipe_accId_//"
SWIPE_STOP = "swipe_accId_银行卡管理"

SWIPE_BEGIN = "swipe_accId_//"
PLEDGE_STOP = "swipe_accId_随心借"
ASSETS_PLEDGE = "accId_UIAStaticText_随心借"

TRADE_PASSWORD = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField"
PLEDGE_REPAY_DONE = "accId_UIAButton_确认"

RESERVATION_CODE = "accId_UIAButton_(UIButton_预约码)"

INVITE_FRIEND = "axis_IOS_邀请好友"
SETTINGS_BUTTON = "accId_UIAButton_UIBarButtonItemLocationRight"

# REPAY_LOAN = "accId_UIAStaticText_还贷款"
REPAY_LOAN = "xpathIOS_UIAStaticText_//UIATableCell/UIAStaticText[@label='走到哪还到哪']"
WELFARE_CENTER = "xpathIOS_UIAStaticText_//UIATableCell/UIAStaticText[@label='福利中心']"
USER_ICON = "axis_IOS_(user_photo.png)[POP]"
USER_ICON_1 = "axis_IOS_(image0)[index]4"  # 上传了个人头像之后

current_page = []


class AssetsPage(PageObject):
    def __init__(self, web_driver):
        super(AssetsPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_at_assets_page(self):
        self.assert_values('我的', self.get_text("//UIAStaticText[@label='我的']"))
        self.assert_values('现金宝', self.get_text("//UIAStaticText[@label='现金宝']"))

    @robot_log
    def get_total_asset(self):
        return self.get_text("//UIAStaticText[@name='(我的总资产)']/./following-sibling::UIAStaticText[1]")

    @robot_log
    def get_xjb_assets(self):
        return self.get_text("//UIAStaticText[@name='(现金宝)']/./following-sibling::UIAStaticText[1]").replace(',', '')

    @robot_log
    def go_to_assets_analysis_page(self):
        self.perform_actions(
            TOTAL_DETAIL,
        )
        self.assert_values('资产分析', self.get_text("//UIAStaticText[@name='资产分析']"))

        page = huaxin_ui.ui_ios_xjb_3_0.assets_analysis_page.AssetsAnalysisPage(self.web_driver)

        return page

    @robot_log
    def go_to_xjb_detail_page(self):
        self.perform_actions(
            XJB_DETAIL,
        )
        self.assert_values('现金宝', self.get_text("//UIAStaticText[@label='现金宝']"))

        page = AssetsXjbDetailPage(self.web_driver)

        return page

    @robot_log
    def go_to_member_center_page(self):
        self.perform_actions(
            MEMBER_CENTER,
        )
        self.assert_values(True, self.element_exist("会员中心", "find_element_by_accessibility_id"))

        page = huaxin_ui.ui_ios_xjb_3_0.assets_associator_center_page.AssetsAssociatorCenterPage(self.web_driver)

        return page

    @robot_log
    def go_to_dqb_detail_page(self):
        self.perform_actions(
            DQB_DETAIL,
        )
        self.assert_values('定活宝', self.get_text("//UIAStaticText[@label='定活宝']"))
        page = AssetsDqbDetailPage(self.web_driver)

        return page

    @robot_log
    def go_to_fund_detail_page(self):
        self.perform_actions(
            FUND_DETAIL,
        )
        self.assert_values('基金', self.get_text("//UIAStaticText[@label='基金']"))
        page = AssetsFundDetailPage(self.web_driver)

        return page

    @robot_log
    def go_to_high_end_detail_page(self):
        self.perform_actions(
            HIGH_END_DETAIL,
        )
        self.assert_values('高端理财', self.get_text("//UIAStaticText[@label='高端理财']"))
        page = AssetsHighEndDetailPage(self.web_driver)

        return page

    @robot_log
    def go_to_bank_card_management_page(self):
        self.perform_actions(
            # SWIPE_START, SWIPE_STOP, 'U',
            CARD_MANAGEMENT,
        )
        self.assert_values('银行卡管理', self.get_text('//UIAStaticText[@name=\'银行卡管理\']'))
        page = BankCardManagementPage(self.web_driver)

        return page

    @robot_log
    def go_to_bank_card_management_page_by_clicking_tips(self):
        self.perform_actions(CARD_MANAGEMENT_TIPS)
        self.assert_values('银行卡管理', self.get_text('//UIAStaticText[@name=\'银行卡管理\']'))
        page = BankCardManagementPage(self.web_driver)

        return page

    @robot_log
    def go_to_credit_card_repay_page(self):
        self.perform_actions(
            CREDIT_CARD_REPAY,
        )
        page = CreditCardRepayPage(self.web_driver)

        return page

    @robot_log
    def go_to_my_points_page(self):
        self.perform_actions(
            "swipe_xpath_//", MY_POINTS_STOP, 'U',
            # MY_POINTS_STOP
        )
        self.perform_actions(
            MY_POINTS,
        )

        self.assert_values('我的积分', self.get_text('//UIAStaticText[@label=\'我的积分\']'))
        page = huaxin_ui.ui_ios_xjb_3_0.assets_my_points_detail_page.AssetsMyPointsDetailPage(self.web_driver)

        return page

    @robot_log
    def go_to_pledge_list_page(self):
        self.perform_actions(SWIPE_BEGIN, PLEDGE_STOP, 'U',
                             ASSETS_PLEDGE,
                             )

        page = huaxin_ui.ui_ios_xjb_3_0.pledge_page.PledgePage(self.web_driver)

        return page

    @robot_log
    def go_to_reservation_code_page(self):
        self.perform_actions(RESERVATION_CODE)
        self.assert_values('预约码通道', self.get_text("//UIAStaticText[@label='预约码通道']"))
        page = ReservationCodePage(self.web_driver)

        return page

    @robot_log
    def go_to_invite_friend_page(self):
        self.perform_actions(INVITE_FRIEND)
        self.assert_values('华信现金宝', self.get_text("//UIAStaticText[@label='华信现金宝']"))
        page = InviteFriendPage(self.web_driver)

        return page

    @robot_log
    def go_to_personal_setting_page(self):
        self.perform_actions(SETTINGS_BUTTON,
                             )
        self.assert_values('设置', self.get_text('//UIAStaticText[@name=\'设置\']'))
        page = PersonalSettingPage(self.web_driver)

        return page

    @robot_log
    def go_to_repay_loan_page(self):
        self.perform_actions("swipe_accId_//", "swipe_accId_还贷款", "U",
                             REPAY_LOAN)
        self.assert_values('还贷款', self.get_text('//UIAStaticText[@name=\'还贷款\']'))
        page = RepayLoanPage(self.web_driver)

        return page

    @robot_log
    def go_to_my_coupon_list(self):
        self.perform_actions(MY_COUPONS)

        page = huaxin_ui.ui_ios_xjb_3_0.my_coupons_list_page.MyCouponsListPage(self.web_driver)
        return page

    @robot_log
    def go_to_welfare_center(self):
        time.sleep(1)
        self.perform_actions("swipe_accId_//", "swipe_accId_福利中心", "U")
        self.perform_actions(WELFARE_CENTER)

        page = huaxin_ui.ui_ios_xjb_3_0.welfare_center_home_page.WelfareCenterHomePage(self.web_driver)
        return page

    @robot_log
    def go_to_personal_information_page(self):
        self.perform_actions(USER_ICON,
                             USER_ICON_1)

        page = huaxin_ui.ui_ios_xjb_3_0.personal_information_page.PersonalInformationPage(self.web_driver)
        return page
