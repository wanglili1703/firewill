# coding=utf-8
from _common.page_object import PageObject
import huaxin_ui.ui_ios_xjb_2_0.security_center_page
from _common.xjb_decorator import robot_log

FIND_TRADE_PASSWORD = "accId_UIAElement_找回交易密码"
MODIFY_TRADE_PASSWORD = "accId_UIAElement_修改交易密码"
CURRENT_TRADE_PASSWORD = "accId_UIATextField_(tradePwdTextField)"
CURRENT_TRADE_PASSWORD_CONFIRM = "accId_UIAButton_下一步"
SETTING_TRADE_PASSWORD = "accId_UIATextField_(tradePwdTextField)"
SETTING_TRADE_PASSWORD_AGAIN = "accId_UIATextField_(tradePwdTextField)"
SETTING_TRADE_PASSWORD_AGAIN_CONFIRM = "accId_UIAButton_下一步"

ID_FACE = "accId_UIAButton_(imageButton)"
ID_BACK = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/pickBack']"
FROM_PHONE_PICTURE = "accId_UIAButton_从相册选择"

RECENTLY = "accId_UIATableCell_屏幕快照"
# ID_FACE_PICTURE = "xpathIOS_UIACollectionCell_/AppiumAUT/UIAApplication/UIAWindow/UIACollectionView/UIACollectionCell[contains(@name, '月')]"
ID_FACE_PICTURE = "axis_IOS_月"

ID_FACE_PICTURE_CONFIRM = "axis_IOS_选取"
# ID_BAC_PICTURE = "xpathIOS_UIACollectionCell_/AppiumAUT/UIAApplication/UIAWindow/UIACollectionView/UIACollectionCell[contains(@name, '月')]"
ID_CONFIRM = "accId_UIAButton_确认"
SETTING_TRADE_PASSWORD_CONFIRM = "accId_UIAButton_确定提交"
SETTING_TRADE_PASSWORD_DONE = "accId_UIAButton_确认"

current_page = []


class SettingTradePasswordPage(PageObject):
    def __init__(self, web_driver):
        super(SettingTradePasswordPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

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

        # page = huaxin_ui.ui_ios_xjb_2_0.security_center_page.SecurityCenterPage(self.web_driver)
        page = self

        return page

    @robot_log
    def find_trade_password(self):
        self.perform_actions(
            FIND_TRADE_PASSWORD,
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
            SETTING_TRADE_PASSWORD_DONE,
        )

        page = huaxin_ui.ui_ios_xjb_2_0.security_center_page.SecurityCenterPage(self.web_driver)

        return page
