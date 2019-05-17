# coding=utf-8
from _common.page_object import PageObject

from _common.global_config import ASSERT_DICT
# from huaxin_ui.ui_android_xjb_3_0.coupon_use_coupon_page import CouponUseCouponPage
import huaxin_ui.ui_android_xjb_3_0.coupon_use_coupon_page
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.home_page
import huaxin_ui.ui_android_xjb_3_0.assets_xjb_detail_page
import huaxin_ui.ui_android_xjb_3_0.xjb_trade_detail_page
import huaxin_ui.ui_android_xjb_3_0.assets_page
import huaxin_ui.ui_android_xjb_3_0.user_operation_succeed_page
import huaxin_ui.ui_android_xjb_3_0.coupon_use_coupon_page
import huaxin_ui.ui_android_xjb_3_0.bank_card_resign_page
import huaxin_ui.ui_android_xjb_3_0.binding_card_detail_page
import time

RECHARGE_AMOUNT = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/cedt_recharge_amount']"
RECHARGE_CONFIRM_BUTTON = "xpath_//android.widget.Button[@text='确认']"
HIDE_SRCURE_KEYBORD = "xpath_//android.widget.TextView[@text='存入金额']"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"
SUCCESS_BUTTON = "xpath_//android.widget.Button[@text='确认']"
XJB_TRADE_DETAIL = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_actionbar_right_orange']"
CANCEL = "xpath_//android.widget.Button[@text='取消']"
ASSETS = "xpath_//android.widget.RelativeLayout[5]/android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/tab_image']"
XJB_DETAIL = "xpath_//android.widget.TextView[@text='现金宝']"
BACK = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left_orange']"
RECHARGE_BACK = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left']"
PAGE_TITLE = 'com.shhxzq.xjb:id/title_actionbar'
GO_AHEAD = 'com.shhxzq.xjb:id/button1'

SWIPE_BEGIN = "swipe_xpath_//"
CONFIRM_BUTTON_SWIPE_STOP = "swipe_xpath_//android.widget.Button[@text='确认']"
COUPONS_INFO = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_coupons_module_info']"
NONSUPERCOMPOSED_COUPON_SWIPE_STOP = "swipe_xpath_//android.widget.RelativeLayout[@clickable='true']//android.widget.TextView[@text='不可叠加使用']"
COUPONS = "xpath_//android.widget.RelativeLayout[@clickable='true']//android.widget.TextView[@text='不可叠加使用']"
COUPONS_CONFIRM = "xpath_//android.widget.TextView[@text='确认']"
SIGN = "xpath_//android.widget.Button[@text='去签约']"
CHOOSE_BANK_CARD_NAME = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_choose_bankcard_name']"
NEW_BANK_CARD_STOP = "swipe_xpath_//android.widget.TextView[@text='使用新卡付款']"
ADD_NEW_BANK_CARD = "xpath_//android.widget.TextView[@text='使用新卡付款']"


class RechargePage(PageObject):
    def __init__(self, web_driver):
        super(RechargePage, self).__init__(web_driver)
        # self.coupon = CouponUseCouponPage(web_driver)
        self._return_page = {
            'AssetsPage': huaxin_ui.ui_android_xjb_3_0.assets_page.AssetsPage(self.web_driver)
        }

    @robot_log
    def verify_page_title(self):
        self.assert_values('存入', self.get_text('com.shhxzq.xjb:id/title_actionbar', 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def recharge(self, recharge_amount, trade_password, nonsuperposed_coupon=None, type='recharge'):
        coupon_amount = 0
        page = self
        self.perform_actions(RECHARGE_AMOUNT, recharge_amount)

        if nonsuperposed_coupon is not None:
            # self.go_to_use_coupon_page()
            # self.coupon.select_coupon(return_page='RechargePage')
            self.perform_actions(COUPONS_INFO)

            self.perform_actions(SWIPE_BEGIN, NONSUPERCOMPOSED_COUPON_SWIPE_STOP, 'U',
                                 COUPONS,
                                 COUPONS_CONFIRM)

            coupon_amount_text = self.get_text('com.shhxzq.xjb:id/tv_coupons_module_info', 'find_element_by_id')
            coupon_amount = float(filter(lambda ch: ch in '0123456789.', coupon_amount_text))

        if type == 'recharge':
            amount_repay = float(recharge_amount) - coupon_amount
            amount_repay_actual = self.get_text('com.shhxzq.xjb:id/tv_amount_repay', 'find_element_by_id').replace(',',
                                                                                                                   '')
            self.assert_values('%.2f' % amount_repay, amount_repay_actual)

        self.perform_actions(SWIPE_BEGIN, CONFIRM_BUTTON_SWIPE_STOP, 'U')
        self.perform_actions(RECHARGE_CONFIRM_BUTTON)

        if float(recharge_amount) >= 0.01 and float(recharge_amount) <= 99999999.99:
            self.perform_actions(
                TRADE_PASSWORD, trade_password, )

            if type == 'recharge':
                page = huaxin_ui.ui_android_xjb_3_0.user_operation_succeed_page.UserOperationSucceedPage(
                    self.web_driver)

                ASSERT_DICT.update({'success_flag': '1'})

            elif type == 'resign':
                self.assert_values('提示', self.get_text('com.shhxzq.xjb:id/alertTitle', 'find_element_by_id'))
                self.assert_values('交易失败，请重新进行签约', self.get_text('com.shhxzq.xjb:id/message', 'find_element_by_id'))
                self.perform_actions(SIGN)
                page = huaxin_ui.ui_android_xjb_3_0.bank_card_resign_page.BankCardResignPage(self.web_driver)

        else:
            ASSERT_DICT.update({'success_flag': '0'})
            if float(recharge_amount) < 0.01:
                self.verify_page_title()
            else:
                self.assert_values('前往', self.get_text(GO_AHEAD, 'find_element_by_id'))
                self.perform_actions(CANCEL)

        return page

    @robot_log
    def back_to_xjb_detail_page(self):
        self.perform_actions(RECHARGE_BACK)

        page = huaxin_ui.ui_android_xjb_3_0.assets_xjb_detail_page.AssetsXjbDetailPage(self.web_driver)

        return page

    @robot_log
    def back_to_home_page(self):
        self.perform_actions(RECHARGE_BACK)

        page = huaxin_ui.ui_android_xjb_3_0.home_page.HomePage(self.web_driver)

        return page

    @robot_log
    def go_to_use_coupon_page(self):
        self.perform_actions(COUPONS_INFO)

        # page = huaxin_ui.ui_android_xjb_3_0.coupon_use_coupon_page.CouponUseCouponPage(self.web_driver)

        # return page

    @robot_log
    def add_new_bank_card(self, device_id):
        self.perform_actions(CHOOSE_BANK_CARD_NAME)
        self.perform_actions(SWIPE_BEGIN, NEW_BANK_CARD_STOP, 'U')
        self.perform_actions(ADD_NEW_BANK_CARD)

        page = huaxin_ui.ui_android_xjb_3_0.binding_card_detail_page.BindingCardDetailPage(self.web_driver, device_id)
        return page

    @robot_log
    def verify_bank_card_info(self, last_card_no):
        self.perform_actions(CHOOSE_BANK_CARD_NAME)
        self.assert_values(True, self.element_exist("//android.widget.TextView[contains(@text,'%s')]" % last_card_no))

        page = self
        return page
