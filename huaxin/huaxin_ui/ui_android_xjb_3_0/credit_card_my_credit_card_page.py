# coding=utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
from _common.global_config import ASSERT_DICT
import huaxin_ui.ui_android_xjb_3_0.credit_card_repay_detail_page
import huaxin_ui.ui_android_xjb_3_0.user_operation_succeed_page

REPAYMENT_WARN_SWITCH = "xpath_//android.widget.ToggleButton[@resource-id='com.shhxzq.xjb:id/repayment_warn_switch']"
REPAYMENT_WARN_DATE = "xpath_//android.view.View[@resource-id='com.shhxzq.xjb:id/lv_filter']"
REPAYMENT_WARN_DATE_COMPELETED = "xpath_//android.widget.TextView[@text='完成']"
SWIPE_BEGIN = "swipe_xpath_//"
DAY_SCROLL = "swipe_xpath_//scroll_1"
BACK = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left']"
CREDIT_CARD = "xpath_//*[contains(@text,%s)]"
CREDIT_CARD_CONFIRM = "xpath_//android.widget.RelativeLayout[@resource-id='com.shhxzq.xjb:id/ccv_credit_repayment']"
CREDIT_CARD_OPERATION = "xpath_//android.widget.ImageButton[@resource-id='com.shhxzq.xjb:id/ibtn_actionbar_right']"
CREDIT_CARD_DELETE = "xpath_//android.widget.TextView[@text='删除']"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"


class CreditCardMyCreditCardPage(PageObject):
    def __init__(self, web_driver):
        super(CreditCardMyCreditCardPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('我的信用卡', self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

    # 添加信用卡还款提醒
    @robot_log
    def add_repayment_warn(self):
        self.perform_actions(REPAYMENT_WARN_SWITCH,
                             REPAYMENT_WARN_DATE,
                             SWIPE_BEGIN, DAY_SCROLL, 'U',
                             REPAYMENT_WARN_DATE_COMPELETED
                             )

        repay_day = self.get_text('com.shhxzq.xjb:id/warn_date_txt', 'find_element_by_id')
        ASSERT_DICT.update({'repay_day_reminder': repay_day})

        page = self
        return page

    # 取消信用卡还款提醒
    @robot_log
    def cancel_repayment_warn(self):
        self.perform_actions(REPAYMENT_WARN_SWITCH
                             )

    @robot_log
    def verify_repayment_warn_flag(self):
        self.assert_values('False', str(self.element_exist("//android.widget.TextView[@text='提醒日']")))

        page = self
        return page

    @robot_log
    def back_to_credit_card_repay_detail_page(self):
        self.perform_actions(BACK)

        page = huaxin_ui.ui_android_xjb_3_0.credit_card_repay_detail_page.CreditCardRepayDetailPage(self.web_driver)
        return page

    @robot_log
    def delete_credit_card(self, trade_password):
        self.perform_actions(
            CREDIT_CARD_OPERATION,
            CREDIT_CARD_DELETE,
            TRADE_PASSWORD, trade_password)

        page = huaxin_ui.ui_android_xjb_3_0.user_operation_succeed_page.UserOperationSucceedPage(self.web_driver)

        return page
