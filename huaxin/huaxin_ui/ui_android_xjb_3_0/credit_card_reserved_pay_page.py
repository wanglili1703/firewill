# coding=utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
from _common.global_config import ASSERT_DICT

import huaxin_ui.ui_android_xjb_3_0.credit_card_repay_page
import huaxin_ui.ui_android_xjb_3_0.user_operation_succeed_page

RESERVED_PAY = "xpath_//android.widget.TextView[@text='信用卡还款']"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"
CREDIT_CARD_SELECTED = "xpath_//android.widget.RelativeLayout[@resource-id='com.shhxzq.xjb:id/rl_credit_item']"
RESERVED_PAY_AMOUNT = "xpath_//android.widget.EditText[@text='请输入预约还款金额']"
RESERVED_PAY_DATE = "xpath_//android.widget.TextView[@text='请选择信用卡还款日']"
DEDUCTION_DATE = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_cr_deduction_date']"
RESERVED_PAY_DATE_MONTH = "xpath_//android.view.View[@resource-id='com.shhxzq.xjb:id/month']"
RESERVED_PAY_DATE_DAY = "xpath_//android.view.View[@resource-id='com.shhxzq.xjb:id/day']"
RESERVED_PAY_DATE_COMPELETED = "xpath_//android.widget.TextView[@text='完成']"
RESERVED_PAY_COMFIRM = "xpath_//android.widget.Button[@text='确认还款']"
RESERVED_PAY_DONE = "xpath_//android.widget.Button[@text='确认']"
COUPONS_INFO = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_coupons_module_info']"
SWIPE_BEGIN = "swipe_xpath_//"
NONSUPERCOMPOSED_COUPON_SWIPE_STOP = "swipe_xpath_//android.widget.RelativeLayout[@clickable='true']//android.widget.TextView[@text='不可叠加使用']"
COUPONS = "xpath_//android.widget.RelativeLayout[@clickable='true']//android.widget.TextView[@text='不可叠加使用']"
COUPONS_CONFIRM = "xpath_//android.widget.TextView[@text='确认']"

current_page = []


class ReservedPayPage(PageObject):
    def __init__(self, web_driver):
        super(ReservedPayPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self, ):
        self.assert_values('预约还款', self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def verify_credit_card_details(self, last_card_no):
        last_no_text = self.get_text('com.shhxzq.xjb:id/tv_bank_desc', 'find_element_by_id')
        last_no_actual = filter(lambda ch: ch in '0123456789.', last_no_text)

        self.assert_values(last_card_no, last_no_actual)

        page = self
        return page

    # 信用卡预约还款
    @robot_log
    def reserved_pay(self, reserved_pay_amount, trade_password, coupon=None):
        coupon_amount = 0
        self.perform_actions(RESERVED_PAY_AMOUNT, reserved_pay_amount,
                             RESERVED_PAY_DATE,
                             RESERVED_PAY_DATE_MONTH,
                             RESERVED_PAY_DATE_DAY,
                             RESERVED_PAY_DATE_COMPELETED)

        if coupon =='nonsuperposed':
            self.perform_actions(COUPONS_INFO)

            self.perform_actions(SWIPE_BEGIN, NONSUPERCOMPOSED_COUPON_SWIPE_STOP, 'U',
                                 COUPONS,
                                 COUPONS_CONFIRM)

            coupon_amount_text = self.get_text('com.shhxzq.xjb:id/tv_coupons_module_info', 'find_element_by_id')
            coupon_amount = float(filter(lambda ch: ch in '0123456789.', coupon_amount_text))

        amount_repay = float(reserved_pay_amount) - coupon_amount
        amount_repay_actual = self.get_text('com.shhxzq.xjb:id/tv_amount_repay', 'find_element_by_id').replace(',', '')
        self.assert_values('%.2f' % amount_repay, amount_repay_actual)

        deduction_date = self.get_text('com.shhxzq.xjb:id/tv_cr_deduction_date', 'find_element_by_id')
        ASSERT_DICT.update({'deduction_date': deduction_date})

        self.perform_actions(RESERVED_PAY_COMFIRM,
                             TRADE_PASSWORD, trade_password
                             )

        page = huaxin_ui.ui_android_xjb_3_0.user_operation_succeed_page.UserOperationSucceedPage(self.web_driver)
        return page
