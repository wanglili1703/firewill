# coding=utf-8
import time

from _common.page_object import PageObject
import huaxin_ui.ui_ios_xjb_3_0.security_center_page
from _common.xjb_decorator import robot_log

FIND_TRADE_PASSWORD = "accId_UIAElement_找回交易密码"
MODIFY_TRADE_PASSWORD = "accId_UIAElement_修改交易密码"
CURRENT_TRADE_PASSWORD = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField"
CURRENT_TRADE_PASSWORD_CONFIRM = "accId_UIAButton_下一步"
SETTING_TRADE_PASSWORD = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField"
SETTING_TRADE_PASSWORD_AGAIN = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField"
SETTING_TRADE_PASSWORD_AGAIN_CONFIRM = "accId_UIAButton_下一步"

ID_NEXT = "xpathIOS_UIAButton_/AppiumAUT/UIAApplication/UIAWindow/UIAScrollView/UIAWebView/UIAButton[POP]"

ID_FACE = "axis_IOS_(UIButton_)[index]3"
# ID_BACK = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/pickBack']"
ID_BACK = "accId_UIAButton_返回"
FROM_PHONE_PICTURE = "accId_UIAButton_从相册选择"
FROM_PHONE_CANCEL = "accId_UIAButton_取消"
ID_1 = "axis_IOS_(UIButton_)[index]1"
ID_2 = "axis_IOS_(UIButton_)[index]2"

RECENTLY = "accId_UIATableCell_屏幕快照"
# ID_FACE_PICTURE = "xpathIOS_UIACollectionCell_/AppiumAUT/UIAApplication/UIAWindow/UIACollectionView/UIACollectionCell[contains(@name, '月')]"
ID_FACE_PICTURE = "axis_IOS_月"

# ID_FACE_PICTURE_CONFIRM = "axis_IOS_选取"
ID_FACE_PICTURE_CONFIRM = "axis_IOS_(UIButton_选取)"
# ID_FACE_PICTURE_CONFIRM = "accId_UIAButton_(UIButton_选取)"
# ID_BAC_PICTURE = "xpathIOS_UIACollectionCell_/AppiumAUT/UIAApplication/UIAWindow/UIACollectionView/UIACollectionCell[contains(@name, '月')]"
ID_CONFIRM = "accId_UIAButton_(UIButton_确认)"
SETTING_TRADE_PASSWORD_CONFIRM = "accId_UIAButton_(UIButton_确定提交)"
SETTING_TRADE_PASSWORD_CANCEL = "accId_UIAButton_(UIButton_取消)"
SETTING_TRADE_PASSWORD_DONE = "accId_UIAButton_(UIButton_确认)"

current_page = []


class SettingTradePasswordPage(PageObject):
    def __init__(self, web_driver):
        super(SettingTradePasswordPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_at_trade_password_page(self):
        self.assert_values("交易密码", self.get_text("//UIAStaticText[@label='交易密码']"))

    @robot_log
    def modify_trade_password(self, trade_password_old, trade_password_new):
        self.perform_actions(
            MODIFY_TRADE_PASSWORD,
            CURRENT_TRADE_PASSWORD, trade_password_old,
            # CURRENT_TRADE_PASSWORD_CONFIRM,
            SETTING_TRADE_PASSWORD, trade_password_new,
            SETTING_TRADE_PASSWORD_AGAIN, trade_password_new,
            # SETTING_TRADE_PASSWORD_AGAIN_CONFIRM,
        )

        time.sleep(2)
        page = self
        return page

    @robot_log
    def find_trade_password(self):

        # 上传身份证个人信息页面
        self.perform_actions(
            FIND_TRADE_PASSWORD,
            ID_NEXT,
            ID_1,
            FROM_PHONE_PICTURE,
            RECENTLY,
            ID_FACE_PICTURE,
            ID_FACE_PICTURE_CONFIRM)

        # 上传身份证有效信息页面
        self.perform_actions(
            ID_2,
            FROM_PHONE_PICTURE,
            RECENTLY,
            ID_FACE_PICTURE,
            ID_FACE_PICTURE_CONFIRM)

        # 上传手持身份证正面照
        self.perform_actions(
            ID_FACE,
            FROM_PHONE_PICTURE,
            RECENTLY,
            ID_FACE_PICTURE,
            ID_FACE_PICTURE_CONFIRM,
            # ID_BACK,
            # FROM_PHONE_PICTURE,
            # RECENTLY,
            # ID_BAC_PICTURE,
            ID_CONFIRM,
            SETTING_TRADE_PASSWORD_CONFIRM,
        )

        time.sleep(0.5)
        self.perform_actions(SETTING_TRADE_PASSWORD_DONE)

        page = huaxin_ui.ui_ios_xjb_3_0.security_center_page.SecurityCenterPage(self.web_driver)
        return page
