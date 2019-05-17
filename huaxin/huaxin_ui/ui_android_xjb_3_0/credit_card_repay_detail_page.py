# coding=utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import time
import huaxin_ui.ui_android_xjb_3_0.coupon_use_coupon_page
import huaxin_ui.ui_android_xjb_3_0.credit_card_reserved_pay_page
import huaxin_ui.ui_android_xjb_3_0.credit_card_repay_page
import huaxin_ui.ui_android_xjb_3_0.credit_card_my_credit_card_page
import huaxin_ui.ui_android_xjb_3_0.user_operation_succeed_page
import huaxin_ui.ui_android_xjb_3_0.credit_card_repay_record_page

RESERVATION_PAY = "axis_Android_预约还款_0.12,0"

CANCEL_RESERVATION = "xpath_//android.widget.TextView[@text='取消预约']"
CANCEL_RESERVATION_CONFIRM = "xpath_//android.widget.Button[@text='确认']"
BACK = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left']"
CREDIT_CARD = "xpath_//*[contains(@text,%s)]"
REPAY_AMOUNT = "xpath_//android.widget.EditText[@text='请输入还款金额']"
REPAY_CONFIRM = "xpath_//android.widget.Button[@text='确认']"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"
RECORD = "xpath_//android.widget.Button[@text='还款记录']"
COUPONS_INFO = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_coupons_module_info']"
SWIPE_BEGIN = "swipe_xpath_//"
SUPERCOMPOSED_COUPON_SWIPE_STOP = "swipe_xpath_//android.widget.RelativeLayout[@clickable='true']//android.widget.TextView[@text='可叠加使用']"
SUPERPOSED_COUPON_1 = "xpath_//android.widget.RelativeLayout[@clickable='true']//android.widget.TextView[@text='可叠加使用']"
SUPERCOMPOSED_COUPON_SWIPE_BEGIN = "swipe_xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/img_coupons_item_select']"
SUPERCOMPOSED_COUPON_SWIPE_STOP_1 = "swipe_xpath_//android.widget.ImageView/../../following-sibling::android.widget.FrameLayout/android.widget.RelativeLayout[@clickable='true']"
SUPERPOSED_COUPON_2 = "xpath_//android.widget.RelativeLayout[@clickable='true']/../following-sibling::android.widget.FrameLayout/android.widget.RelativeLayout[@clickable='true']"
COUPONS_CONFIRM = "xpath_//android.widget.TextView[@text='确认']"

class CreditCardRepayDetailPage(PageObject):
    def __init__(self, web_driver):
        super(CreditCardRepayDetailPage, self).__init__(web_driver)
        # self.coupon = CouponUseCouponPage(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('信用卡还款', self.get_text(self.page_title, 'find_element_by_id'))
        self.assert_values('还款记录', self.get_text('com.shhxzq.xjb:id/btn_actionbar_right', 'find_element_by_id'))

        page = self
        return page

    # 转到预约还款页面
    @robot_log
    def go_to_reserved_pay_page(self):
        self.perform_actions(RESERVATION_PAY)
        # self.click_screen_(x=0.61, y=0.81)
        time.sleep(3)

        page = huaxin_ui.ui_android_xjb_3_0.credit_card_reserved_pay_page.ReservedPayPage(self.web_driver)
        return page

    @robot_log
    def verify_credit_card_details(self, last_card_no):
        last_no_text = self.get_text('com.shhxzq.xjb:id/tv_bank_desc', 'find_element_by_id')
        last_no_actual = filter(lambda ch: ch in '0123456789.', last_no_text)

        self.assert_values(last_card_no, last_no_actual)

        page = self
        return page

    @robot_log
    def verify_credit_card_reserved_pay_flag(self):
        self.assert_values('True', str(
            self.element_exist("//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/tv_credit_reserved_pay']")))

        page = self
        return page

    # 取消预约还款
    @robot_log
    def cancel_reservation(self):
        self.perform_actions(CANCEL_RESERVATION,
                             CANCEL_RESERVATION_CONFIRM)

        page = self

        return page

    @robot_log
    def go_to_my_credit_card_page(self, last_card_no):
        self.perform_actions(CREDIT_CARD % last_card_no)

        page = huaxin_ui.ui_android_xjb_3_0.credit_card_my_credit_card_page.CreditCardMyCreditCardPage(self.web_driver)

        return page

    @robot_log
    def back_to_credit_card_repay_page(self):
        self.perform_actions(BACK)

        page = huaxin_ui.ui_android_xjb_3_0.credit_card_repay_page.CreditCardRepayPage(self.web_driver)
        return page

    # 信用卡还款
    @robot_log
    def repay(self, repay_amount, trade_password, superposed_coupon='N'):
        coupon_amount = 0
        self.perform_actions(REPAY_AMOUNT, repay_amount)
        if superposed_coupon == 'Y':
            # self.go_to_use_coupon_page()
            # self.coupon.select_coupon(return_page='CreditCardRepayDetailPage', coupon='superposed')
            self.perform_actions(COUPONS_INFO)

            self.perform_actions(SWIPE_BEGIN, SUPERCOMPOSED_COUPON_SWIPE_STOP, 'U',
                                 SUPERPOSED_COUPON_1,
                                 SUPERCOMPOSED_COUPON_SWIPE_BEGIN, SUPERCOMPOSED_COUPON_SWIPE_STOP_1, 'U',
                                 SUPERPOSED_COUPON_2,
                                 COUPONS_CONFIRM)

            coupon_amount_text = self.get_text('com.shhxzq.xjb:id/tv_coupons_module_info', 'find_element_by_id')
            coupon_amount = float(filter(lambda ch: ch in '0123456789.', coupon_amount_text))

        amount_repay = float(repay_amount) - coupon_amount
        amount_repay_actual = self.get_text('com.shhxzq.xjb:id/tv_amount_repay', 'find_element_by_id').replace(',', '')
        self.assert_values('%.2f' % amount_repay, amount_repay_actual)

        self.perform_actions(REPAY_CONFIRM,
                             TRADE_PASSWORD, trade_password,
                             )
        page = huaxin_ui.ui_android_xjb_3_0.user_operation_succeed_page.UserOperationSucceedPage(self.web_driver)
        time.sleep(5)
        return page

    @robot_log
    def go_to_credit_card_repay_record_page(self):
        self.perform_actions(RECORD)

        page = huaxin_ui.ui_android_xjb_3_0.credit_card_repay_record_page.CreditCardRepayRecordPage(self.web_driver)
        return page

    @robot_log
    def go_to_use_coupon_page(self):
        self.perform_actions(COUPONS_INFO)

        page = huaxin_ui.ui_android_xjb_3_0.coupon_use_coupon_page.CouponUseCouponPage(self.web_driver)

        return page
