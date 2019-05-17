# coding=utf-8
import decimal

from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.invite_friend_page
import huaxin_ui.ui_ios_xjb_3_0.points_yb_details_page
from _common.global_config import ASSERT_DICT
import huaxin_ui.ui_ios_xjb_3_0.goods_detail_page

TITLE_ELE = "//UIAStaticText[@label='福利中心']"
TITLE = "//UIAStaticText[@label='福利放送']"
RECOMMEND = "//UIAButton[@label='去推荐']"
SHARE = "//UIAButton[@label='去分享']"
FOCUS = "//UIAButton[@label='去关注']"
GOOD = "//UIAButton[@label='去点赞']"
BIND = "//UIAButton[@label='去绑定']"
MY_POINTS = "xpathIOS_UIAStaticText_//UIAStaticText[@label='我的积分']"
MY_POINTS_QUESTION_MARK = "xpathIOS_UIAImage_//UIAStaticText[@label='我的积分']/following-sibling::UIAImage[1]"
MY_YB = "xpathIOS_UIAStaticText_//UIAStaticText[@label='我的元宝']"
YB_NUMBER = "//UIAStaticText[@label='我的元宝']/following-sibling::UIAStaticText"
POINTS_NUMBER = "//UIAStaticText[@label='我的积分']/following-sibling::UIAStaticText"
MY_YB_QUESTION_MARK = "xpathIOS_UIAImage_//UIAStaticText[@label='我的元宝']/following-sibling::UIAImage[1]"
VIEW_POINTS_DETAIL = "xpathIOS_UIAStaticText_//UIAStaticText[@label='查看积分明细']"
VIEW_YB_DETAIL = "xpathIOS_UIAStaticText_//UIAStaticText[@label='查看元宝明细']"
CHECK_IN = "accId_UIAButton_签到"
DISCOUNT_MORE = "xpathIOS_UIAStaticText_//UIAStaticText[@label='限时特惠']/following-sibling::UIAStaticText"
EXCHANGE_MORE = "xpathIOS_UIAStaticText_//UIAStaticText[@label='边逛边兑']/following-sibling::UIAStaticText"
ACTIVITY_MORE = "xpathIOS_UIAStaticText_//UIAStaticText[@label='福利放送']/following-sibling::UIAStaticText"
BUY_FUND_IMAGE = "xpathIOS_UIAImage_//UIAStaticText[@label='限时特惠']/following-sibling::UIAImage[1]"
BUY_VIP_IMAGE = "xpathIOS_UIAImage_//UIAStaticText[@label='限时特惠']/following-sibling::UIAImage[2]"
BACK = "accId_UIAButton_UIBarButtonItemLocationLeft"
COUPON_ITEM = "xpathIOS_UIAStaticText_//UIAStaticText[@label='28元优惠券']"

current_page = []


class WelfareCenterPage(PageObject):
    def __init__(self, web_driver):
        super(WelfareCenterPage, self).__init__(web_driver)
        self.elements_exist(*current_page)
        self._return_page = {
        }

    @robot_log
    def check_in(self):
        yb = self.get_text(YB_NUMBER)
        ASSERT_DICT.update({"yb": yb})
        if self.element_exist("//UIAButton[@label='签到']"):
            self.perform_actions(CHECK_IN)
            self.assert_values("签到成功", self.get_text("//UIAStaticText[@label='签到成功']"))
            # 关闭弹出框
            self.perform_actions("xpathIOS_UIAImage_//UIAStaticText[@label='签到成功']/following-sibling::UIAImage")

            yb_update = self.get_text(YB_NUMBER)
            self.assert_values(decimal.Decimal(yb).quantize(decimal.Decimal('0.00')) + decimal.Decimal(5.00),
                               decimal.Decimal(yb_update), "==")

        self.assert_values('已签到', self.get_text("//UIAButton[@label='已签到']"))

    @robot_log
    def discount_more(self):
        self.perform_actions(BUY_FUND_IMAGE)
        self.assert_values("买基金，用积分，更实惠", self.get_text("//UIAStaticText[@label='买基金，用积分，更实惠']"))
        self.perform_actions(BACK)
        self.perform_actions(BUY_VIP_IMAGE)
        self.assert_values("买高端，积分抵，更划算", self.get_text("//UIAStaticText[@label='买高端，积分抵，更划算']"))
        self.perform_actions(BACK)
        self.perform_actions(DISCOUNT_MORE)
        self.assert_values("限时特惠", self.get_text("//UIAStaticText[@label='限时特惠']"))
        self.perform_actions("xpathIOS_UIAImage_//UIAWebView/UIAImage")
        self.assert_values("买基金，用积分，更实惠", self.get_text("//UIAStaticText[@label='买基金，用积分，更实惠']"))
        self.perform_actions(BACK)
        self.perform_actions("xpathIOS_UIAImage_//UIAWebView/UIAImage[2]")
        self.assert_values("买高端，积分抵，更划算", self.get_text("//UIAStaticText[@label='买高端，积分抵，更划算']"))
        self.perform_actions(BACK)
        self.assert_values("限时特惠", self.get_text("//UIAStaticText[@label='限时特惠']"))

    @robot_log
    def exchange_coupon(self):
        ASSERT_DICT.update({
            "yb": self.get_text(YB_NUMBER),
            "points": self.get_text(POINTS_NUMBER)
        })
        self.perform_actions(COUPON_ITEM)

        page = huaxin_ui.ui_ios_xjb_3_0.goods_detail_page.GoodsDetailPage(self.web_driver)
        return page

    @robot_log
    def verify_at_welfare_center_page_title(self):
        title = self.get_text(TITLE_ELE)
        self.assert_values('福利中心', title)

    @robot_log
    def go_to_my_points(self):
        self.perform_actions(MY_POINTS)
        page = huaxin_ui.ui_ios_xjb_3_0.points_yb_details_page.PointsYbDetailsPage(self.web_driver)
        return page

    @robot_log
    def go_to_my_points_description_page(self):
        self.perform_actions(MY_POINTS_QUESTION_MARK)
        self.assert_values("积分说明", self.get_text("//UIAStaticText[@label='积分说明']"))
        self.perform_actions(VIEW_POINTS_DETAIL)
        page = huaxin_ui.ui_ios_xjb_3_0.points_yb_details_page.PointsYbDetailsPage(self.web_driver)
        return page

    @robot_log
    def go_to_my_yb_description_page(self):
        self.perform_actions(MY_YB_QUESTION_MARK)
        self.assert_values("元宝说明", self.get_text("//UIAStaticText[@label='元宝说明']"))
        self.perform_actions(VIEW_YB_DETAIL)
        page = huaxin_ui.ui_ios_xjb_3_0.points_yb_details_page.PointsYbDetailsPage(self.web_driver)
        return page

    @robot_log
    def go_to_my_yb(self):
        self.perform_actions(MY_YB)
        page = huaxin_ui.ui_ios_xjb_3_0.points_yb_details_page.PointsYbDetailsPage(self.web_driver)
        return page

    @robot_log
    def recommend(self):
        self.perform_actions("xpathIOS_UIAButton_%s" % RECOMMEND)
        page = huaxin_ui.ui_ios_xjb_3_0.invite_friend_page.InviteFriendPage(self.web_driver)
        return page

    @robot_log
    def share(self):
        self.perform_actions("swipe_xpath_//", "swipe_xpath_IOS%s" % SHARE, 'U')
        self.perform_actions("xpathIOS_UIAButton_%s" % SHARE)
        self.assert_values("研究报告", self.get_text("//UIAStaticText[@label='研究报告']"))

    @robot_log
    def focus(self):
        self.perform_actions("swipe_xpath_//", "swipe_xpath_IOS%s" % SHARE, 'U')
        self.perform_actions(ACTIVITY_MORE)
        self.perform_actions("xpathIOS_UIAButton_%s" % FOCUS)

        self.assert_values("关注绑定方法", self.get_text("//UIAStaticText[@label='关注绑定方法']"))

        page = self
        return page

    @robot_log
    def good(self):
        self.perform_actions("swipe_xpath_//", "swipe_xpath_IOS%s" % SHARE, 'U')
        self.perform_actions(ACTIVITY_MORE)
        self.perform_actions("xpathIOS_UIAButton_%s" % GOOD)
        page = self
        self.assert_values('福利放送', self.get_text(TITLE))
        self.assert_values("手机开户", self.get_text("//UIAStaticText[@label='手机开户']"))
        self.assert_values("极速行情", self.get_text("//UIAStaticText[@label='极速行情']"))
        self.assert_values("闪电交易", self.get_text("//UIAStaticText[@label='闪电交易']"))
        self.assert_values("随心借", self.get_text("//UIAStaticText[@label='随心借']"))
        self.assert_values(True, self.element_exist("//UIAButton[@label='下载涨停宝APP']"))
        return page

    @robot_log
    def bind(self):
        self.perform_actions("swipe_xpath_//", "swipe_xpath_IOS%s" % SHARE, 'U')
        self.perform_actions(ACTIVITY_MORE)
        self.perform_actions("swipe_xpath_//", "swipe_xpath_IOS%s" % BIND, 'U')
        self.perform_actions("xpathIOS_UIAButton_%s" % BIND)
        page = self
        self.assert_values('福利放送', self.get_text(TITLE))
        self.assert_values("手机开户", self.get_text("//UIAStaticText[@label='手机开户']"))
        self.assert_values("极速行情", self.get_text("//UIAStaticText[@label='极速行情']"))
        self.assert_values("闪电交易", self.get_text("//UIAStaticText[@label='闪电交易']"))
        self.assert_values("随心借", self.get_text("//UIAStaticText[@label='随心借']"))
        self.assert_values(True, self.element_exist("//UIAButton[@label='下载涨停宝APP']"))
        return page
