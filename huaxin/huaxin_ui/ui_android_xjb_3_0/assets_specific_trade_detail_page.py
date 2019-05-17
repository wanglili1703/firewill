# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
from _common.global_config import ASSERT_DICT
import huaxin_ui.ui_android_xjb_3_0.user_operation_succeed_page

CANCEL_ORDER = "xpath_//android.widget.Button[@text='撤单']"
COMFIRM = "xpath_//android.widget.Button[@text='确认']"
TRADE_PASSWORD = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/trade_pop_password_et']"


class AssetsSpecificTradeDetailPage(PageObject):
    def __init__(self, web_driver):
        super(AssetsSpecificTradeDetailPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('交易详情', self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def verify_trade_details(self, product_name, status=None, from_account=None, to_detail=None):
        if from_account is not None:
            self.assert_values(product_name, self.get_text('com.shhxzq.xjb:id/to_title', 'find_element_by_id'))
        if to_detail is not None:
            self.assert_values(to_detail, self.get_text('com.shhxzq.xjb:id/to_detail', 'find_element_by_id'))
        self.assert_values(product_name, self.get_text('com.shhxzq.xjb:id/to_title', 'find_element_by_id'))

        self.assert_values(status, self.get_text('com.shhxzq.xjb:id/trade_status', 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def cancel_order(self, trade_password, trade_type=None):
        if trade_type == 'fund_normal_convert':
            trade_amount = float(filter(lambda ch: ch in '0123456789.',
                                        self.get_text('com.shhxzq.xjb:id/trade_amount', 'find_element_by_id')))
            available_amount = ASSERT_DICT['available_amount'] + trade_amount
            ASSERT_DICT.update({'available_amount': available_amount})
        self.perform_actions(CANCEL_ORDER,
                             COMFIRM,
                             TRADE_PASSWORD, trade_password)

        page = huaxin_ui.ui_android_xjb_3_0.user_operation_succeed_page.UserOperationSucceedPage(self.web_driver)
        return page
