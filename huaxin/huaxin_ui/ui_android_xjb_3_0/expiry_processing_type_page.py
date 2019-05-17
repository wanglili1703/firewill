# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.fund_redeem_page
import huaxin_ui.ui_android_xjb_3_0.assets_high_end_detail_page

SWIPE_BEGIN = "swipe_xpath_//"
DIVIDEND_TYPE_SWIPE_STOP = "swipe_xpath_//android.widget.TextView[@text='分红方式']"
REDEEM_AMOUNT = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/ckedt_redeem_amt']"
VIP_REDEEM_AMOUNT = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/exit_amount_edit']"
BACK = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left']"
EXPIRY_DISPOSE_CONFIRM = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_expire_dipose_confirm']"
VIP_EXPIRY_DISPOSE_CONFIRM = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_dqb_redeem_product_sure']"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"
ALL = "xpath_//android.widget.TextView[contains(@text,'全部')]"
TYPE_SWITCH = "xpath_//android.widget.TextView[contains(@text,'%s')]/following-sibling::android.widget.RadioButton[1]"


class ExpiryProcessingTypePage(PageObject):
    def __init__(self, web_driver):
        super(ExpiryProcessingTypePage, self).__init__(web_driver)
        self._return_page = {
            'AssetsHighEndDetailPage': huaxin_ui.ui_android_xjb_3_0.assets_high_end_detail_page.AssetsHighEndDetailPage(
                self.web_driver),
            'FundRedeemPage': huaxin_ui.ui_android_xjb_3_0.fund_redeem_page.FundRedeemPage(self.web_driver)
        }

    @robot_log
    def verify_page_title(self):
        self.assert_values('到期处理方式', self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def verify_expiry_processing_details(self, expiry_dispose_type, expiry_dispose_amount='1,000,000.00',
                                         product_type='fund'):
        if product_type == 'fund':
            if expiry_dispose_type == '全部赎回至现金宝' or expiry_dispose_type == '部分赎回至现金宝':
                self.assert_values(True, self.element_exist(
                    "//android.widget.TextView[@text='自动赎回至现金宝']/following-sibling::android.widget.RadioButton[1][@checked='true']")
                                   )
                self.assert_values(expiry_dispose_amount,
                                   self.get_text('com.shhxzq.xjb:id/ckedt_redeem_amt', 'find_element_by_id'))
            else:
                self.assert_values(True, self.element_exist(
                    "//android.widget.TextView[@text='自动续存']/following-sibling::android.widget.RadioButton[1][@checked='true']")
                                   )
        elif product_type == 'vip':
            if expiry_dispose_type == '到期退出':
                self.assert_values(True, self.element_exist(
                    "//android.widget.TextView[@text='到期退出']/following-sibling::android.widget.RadioButton[1][@checked='true']")
                                   )
                self.assert_values(expiry_dispose_amount,
                                   self.get_text('com.shhxzq.xjb:id/exit_amount_edit', 'find_element_by_id'))
            else:
                self.assert_values(True, self.element_exist(
                    "//android.widget.TextView[@text='自动续存(默认)']/following-sibling::android.widget.RadioButton[1][@checked='true']")
                                   )

        page = self
        return page

    @robot_log
    def product_expiry_processing_type_switch(self, switch_to, trade_password, expiry_redeem_amount='1,000,000.00',
                                              product_type='fund', return_page='FundRedeemPage'):
        if product_type == 'fund':
            if switch_to == '部分赎回至现金宝':
                self.perform_actions(REDEEM_AMOUNT, expiry_redeem_amount)
            elif switch_to == '全部赎回至现金宝':
                switch_to = '自动赎回至现金宝'
                self.perform_actions(TYPE_SWITCH % switch_to,
                                     ALL)
                self.assert_values('1,000,000.00',
                                   self.get_text('com.shhxzq.xjb:id/ckedt_redeem_amt', 'find_element_by_id'))
            else:
                switch_to = '自动续存'
                self.perform_actions(TYPE_SWITCH % switch_to)
            self.perform_actions(EXPIRY_DISPOSE_CONFIRM)
        elif product_type == 'vip':
            if switch_to == '部分退出':
                self.perform_actions(VIP_REDEEM_AMOUNT, expiry_redeem_amount)
            elif switch_to == '全部退出':
                switch_to = '到期退出'
                self.perform_actions(TYPE_SWITCH % switch_to,
                                     ALL)
                self.assert_values('1,000,000.00',
                                   self.get_text('com.shhxzq.xjb:id/exit_amount_edit', 'find_element_by_id'))
            else:
                switch_to = '自动续存'
                self.perform_actions(TYPE_SWITCH % switch_to)
            self.perform_actions(VIP_EXPIRY_DISPOSE_CONFIRM)

        self.perform_actions(TRADE_PASSWORD, trade_password)

        page = self._return_page[return_page]
        return page

    @robot_log
    def back_to_fund_redeem_page(self):
        self.perform_actions(BACK)

        page = huaxin_ui.ui_android_xjb_3_0.fund_redeem_page.FundRedeemPage(self.web_driver)
        return page
