# coding=utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.recharge_page
import huaxin_ui.ui_android_xjb_3_0.credit_card_repay_detail_page

SWIPE_BEGIN = "swipe_xpath_//"
NONSUPERCOMPOSED_COUPON_SWIPE_STOP = "swipe_xpath_//android.widget.RelativeLayout[@clickable='true']//android.widget.TextView[@text='不可叠加使用']"
SUPERCOMPOSED_COUPON_SWIPE_STOP = "swipe_xpath_//android.widget.RelativeLayout[@clickable='true']//android.widget.TextView[@text='可叠加使用']"
SUPERPOSED_COUPON_1 = "xpath_//android.widget.RelativeLayout[@clickable='true']//android.widget.TextView[@text='可叠加使用']"
SUPERCOMPOSED_COUPON_SWIPE_BEGIN = "swipe_xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/img_coupons_item_select']"
SUPERCOMPOSED_COUPON_SWIPE_STOP_1 = "swipe_xpath_//android.widget.ImageView/../../following-sibling::android.widget.FrameLayout/android.widget.RelativeLayout[@clickable='true']"
SUPERPOSED_COUPON_2 = "xpath_//android.widget.RelativeLayout[@clickable='true']/../following-sibling::android.widget.FrameLayout/android.widget.RelativeLayout[@clickable='true']"
COUPONS = "xpath_//android.widget.RelativeLayout[@clickable='true']//android.widget.TextView[@text='不可叠加使用']"
COUPONS_CONFIRM = "xpath_//android.widget.TextView[@text='确认']"


class CouponUseCouponPage(PageObject):
    def __init__(self, web_driver):
        super(CouponUseCouponPage, self).__init__(web_driver)
        self._return_page = {
            'RechargePage': huaxin_ui.ui_android_xjb_3_0.recharge_page.RechargePage(self.web_driver),
            'CreditCardRepayDetailPage': huaxin_ui.ui_android_xjb_3_0.credit_card_repay_detail_page.CreditCardRepayDetailPage(
                self.web_driver),
        }

    @robot_log
    def verify_page_title(self):
        self.assert_values('使用优惠券', self.get_text(self.page_title, 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def select_coupon(self, coupon='nonsuperposed', return_page=None):
        if coupon == 'superposed':
            self.perform_actions(SWIPE_BEGIN, SUPERCOMPOSED_COUPON_SWIPE_STOP, 'U',
                                 SUPERPOSED_COUPON_1,
                                 SUPERCOMPOSED_COUPON_SWIPE_BEGIN, SUPERCOMPOSED_COUPON_SWIPE_STOP_1, 'U',
                                 SUPERPOSED_COUPON_2,
                                 COUPONS_CONFIRM)
        else:
            self.perform_actions(SWIPE_BEGIN, NONSUPERCOMPOSED_COUPON_SWIPE_STOP, 'U',
                                 COUPONS,
                                 COUPONS_CONFIRM)

        page = self._return_page[return_page]

        return page
