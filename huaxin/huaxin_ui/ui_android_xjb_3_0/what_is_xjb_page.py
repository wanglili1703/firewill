# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.recharge_page
import huaxin_ui.ui_android_xjb_3_0.xjb_product_detail_page
import time

SWIPE_BEGIN = "swipe_xpath_//"
BOTTOM_STOP = "swipe_xpath_//android.view.View[@content-desc='查看博时现金宝货币A详情']"
BOTTOM_SCROLL = "swipe_xpath_//scroll_5"
BOTTOM = "xpath_//android.view.View[@content-desc='查看博时现金宝货币A详情']"
RECHARGE = "xpath_//android.widget.Button[@content-desc='立即存入']"
XJB = "xpath_//android.view.View[@content-desc='查看博时现金宝货币A详情']"
# XJB = "xpath_//android.widget.Image[@content-desc='next']"


class WhatIsXjbPage(PageObject):
    def __init__(self, web_driver):
        super(WhatIsXjbPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('什么是现金宝', self.get_text(self.page_title, 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def verify_page_content_details(self):
        self.assert_values(True, self.element_exist("//android.view.View[@content-desc='什么是现金宝']"))
        self.assert_values(True, self.element_exist("//android.view.View[contains(@content-desc,'现金宝七日年化收益率')]"))
        self.assert_values(True, self.element_exist("//android.view.View[@content-desc='直接买入平台其他理财产品，支付无限额']"))
        self.perform_actions(SWIPE_BEGIN, BOTTOM_STOP, 'U')
        self.assert_values(True, self.element_exist("//android.view.View[@content-desc='快取额度1000万，最快1秒到账，免手续费']"))

        page = self
        return page

    @robot_log
    def go_to_recharge_page(self):
        self.perform_actions(RECHARGE)

        page = huaxin_ui.ui_android_xjb_3_0.recharge_page.RechargePage(self.web_driver)
        return page

    @robot_log
    def go_to_xjb_product_detail_page(self):
        self.perform_actions(SWIPE_BEGIN, BOTTOM_SCROLL, 'U')
        self.perform_actions(SWIPE_BEGIN, BOTTOM_SCROLL, 'U')
        self.perform_actions(SWIPE_BEGIN, BOTTOM_SCROLL, 'U')
        self.click_by_link_text(text='查看博时现金宝货币A详情')
        self.perform_actions(XJB)

        page = huaxin_ui.ui_android_xjb_3_0.xjb_product_detail_page.XjbProductDetailPage(self.web_driver)
        return page
