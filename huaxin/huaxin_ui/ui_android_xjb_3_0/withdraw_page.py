# coding=utf-8
from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.assets_page
from _common.global_config import ASSERT_DICT
# import huaxin_ui.ui_android_xjb_3_0.home_page
from _common.web_driver import WebDriver
import huaxin_ui.ui_android_xjb_3_0.xjb_trade_detail_page
import huaxin_ui.ui_android_xjb_3_0.user_operation_succeed_page
import huaxin_ui.ui_android_xjb_3_0.assets_xjb_detail_page
import time

REGULAR_WITHDRAW_RADIO = "xpath_//android.widget.RadioButton[@resource-id='com.shhxzq.xjb:id/rbtn_enchashment_normal_select']"
FAST_WITHDRAW_RADIO = "xpath_//android.widget.RadioButton[@resource-id='com.shhxzq.xjb:id/rbtn_enchashment_faster_select']"
AMOUNT = "xpath_//android.widget.EditText[@text='请输入取出金额']"
CONFIRM_BUTTON = "xpath_//android.widget.Button[@text='确认取出']"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"
SUCCESS_BUTTON = "xpath_//android.widget.Button[@text='确认']"
ASSETS = "xpath_//android.widget.RelativeLayout[5]/android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/tab_image']"
# ASSETS = "xpath_//android.widget.RelativeLayout[4]/android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/tab_image']"
XJB_DETAIL = "xpath_//android.widget.TextView[@text='现金宝']"
XJB_TRADE_DETAIL = "xpath_//android.widget.Button[@text='收支明细']"
BACK = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left_orange']"
WITHDRAW_BACK = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left']"

current_page = []


class WithdrawPage(PageObject):
    def __init__(self, web_driver):
        super(WithdrawPage, self).__init__(web_driver)
        self.web_driver = web_driver
        self.elements_exist(*current_page)
        self._return_page = {
            'AssetsPage': huaxin_ui.ui_android_xjb_3_0.assets_page.AssetsPage(self.web_driver)
        }

    @robot_log
    def verify_page_title(self):
        self.assert_values('取出', self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def withdraw(self, withdraw_amount, trade_password, type=None):
        if type =='regular_withdraw':
            self.perform_actions(REGULAR_WITHDRAW_RADIO)
        else:
            self.perform_actions(FAST_WITHDRAW_RADIO)

        money_fast_max = self.get_text('com.shhxzq.xjb:id/tv_enchashment_bank_card_balance',
                                       'find_element_by_id').replace(',', '')
        money_fast_max = '%.2f' % float(filter(lambda ch: ch in '0123456789.', str(money_fast_max)))

        self.perform_actions(AMOUNT, withdraw_amount,
                             CONFIRM_BUTTON)

        if float(withdraw_amount) >= 0.01 and float(withdraw_amount) <= float(money_fast_max):
            self.perform_actions(TRADE_PASSWORD, trade_password)

            page = huaxin_ui.ui_android_xjb_3_0.user_operation_succeed_page.UserOperationSucceedPage(self.web_driver)

            ASSERT_DICT.update({'success_flag': '1'})

# total_asset_beforehand = float(filter(lambda ch: ch in '0123456789.', ASSERT_DICT['total_asset']))
            # xjb_asset_beforehand = float(filter(lambda ch: ch in '0123456789.', ASSERT_DICT['xjb_asset']))
            # total_asset = total_asset_beforehand - float(withdraw_amount)
            # xjb_asset = xjb_asset_beforehand - float(withdraw_amount)
            #
            # ASSERT_DICT.update({'total_asset': total_asset})
            # ASSERT_DICT.update({'xjb_asset': xjb_asset})
            #
            # page = huaxin_ui.ui_android_xjb_3_0.xjb_trade_detail_page.XjbTradeDetailPage(self.web_driver)
            #
            # if source == '0':
            #     self.perform_actions(ASSETS)
            #
            # time.sleep(3)
            #
            # self.assert_values(str(ASSERT_DICT['total_asset']),
            #                    self.get_text('com.shhxzq.xjb:id/total_assets', 'find_element_by_id').replace(',', ''))
            # self.assert_values(str(ASSERT_DICT['xjb_asset']),
            #                    self.get_text('com.shhxzq.xjb:id/desc', 'find_element_by_id').replace(',', ''))
            #
            # self.perform_actions(XJB_DETAIL)
            # balance = float(self.get_text('com.shhxzq.xjb:id/xjb_home_balance', 'find_element_by_id').replace(',', ''))
            # self.assert_values(float(xjb_asset), balance, '==')
            # self.perform_actions(XJB_TRADE_DETAIL)

        else:
            ASSERT_DICT.update({'success_flag': '0'})
            self.verify_page_title()

            page = self
        time.sleep(5)
        return page

    @robot_log
    def back_to_xjb_detail_page(self):
        self.perform_actions(WITHDRAW_BACK)

        page = huaxin_ui.ui_android_xjb_3_0.assets_xjb_detail_page.AssetsXjbDetailPage(self.web_driver)

        return page

    @robot_log
    def back_to_home_page(self):
        self.perform_actions(WITHDRAW_BACK)

        page = huaxin_ui.ui_android_xjb_3_0.home_page.HomePage(self.web_driver)

        return page

