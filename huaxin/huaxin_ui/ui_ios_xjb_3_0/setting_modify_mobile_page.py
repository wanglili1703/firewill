# coding: utf-8
import time
from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
from _tools.mysql_xjb_tools import MysqlXjbTools
from huaxin_ui.ui_ios_xjb_3_0.login_page import LoginPage
import huaxin_ui.ui_ios_xjb_3_0.personal_setting_page

TRADE_PASSWORD = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField"
TRADE_PASSWORD_CONFIRM = "accId_UIAButton_确认"

RECEIVE_SMS = "accId_UIAStaticText_能接收短信"
NO_RECEIVE_SMS = "accId_UIAStaticText_不能接收短信"
NEXT = "xpathIOS_UIAButton_//UIAScrollView/UIAWebView/UIAButton[POP]"
UPLOAD_PICTURE = "axis_IOS_(UIButton_)[index]1"
FROM_PHONE_PICTURE = "accId_UIAButton_从相册选择"
RECENTLY = "accId_UIATableCell_屏幕快照"
ID_FACE_PICTURE = "axis_IOS_月"

ID_FACE_PICTURE_CONFIRM = "axis_IOS_(UIButton_选取)"
ID_CONFIRM = "accId_UIAButton_(UIButton_确认)"
CONFIRM_AGAIN = "accId_UIAButton_(UIButton_确定提交)[POP]"

GET_VERIFY_CODE = "accId_UIAButton_获取验证码"
TRADE_PASSWORD_VERIFY_CODE_INPUT = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField"
VERIFY_CODE_CONFIRM = "accId_UIAButton_(UIButton_提交)"

# MOBILE = "accId_UIATextField_(textField)请输入11位手机号码"
MOBILE = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField"
MOBILE_GET_VERIFY_CODE = "accId_UIAButton_(UIButton_获取验证码)"
MOBILE_VERIFY_CODE_INPUT = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField[3]"
MOBILE_CONFIRM = "accId_UIAButton_(UIButton_确认)"

MODIFY_MOBILE_DONE = "accId_UIAButton_(UIButton_确认)"

current_page = []


class SettingModifyMobilePage(PageObject):
    def __init__(self, web_driver):
        super(SettingModifyMobilePage, self).__init__(web_driver)
        self.elements_exist(*current_page)
        self._db = MysqlXjbTools()

    @robot_log
    def modify_mobile(self, mobile_old, trade_password, mobile_new):
        self.perform_actions(
            TRADE_PASSWORD, trade_password,
            # TRADE_PASSWORD_CONFIRM,
            RECEIVE_SMS,
            GET_VERIFY_CODE,
        )

        verify_code = MysqlXjbTools().get_sms_verify_code(mobile=mobile_old, template_id='cif_changeMobile')

        self.perform_actions(
            TRADE_PASSWORD_VERIFY_CODE_INPUT, verify_code,
            VERIFY_CODE_CONFIRM,
            MOBILE, mobile_new,
            MOBILE_GET_VERIFY_CODE
        )

        verify_code = MysqlXjbTools().get_sms_verify_code(mobile=mobile_new, template_id='cif_changeMobile')

        self.perform_actions(
            MOBILE_VERIFY_CODE_INPUT, verify_code,
            MOBILE_CONFIRM,
            MODIFY_MOBILE_DONE,
        )

        page = LoginPage(self.web_driver)

        return page

    @robot_log
    def modify_mobile_without_sms(self, trade_password, mobile_new):
        self.perform_actions(
            TRADE_PASSWORD, trade_password,
            NO_RECEIVE_SMS,
            NEXT,
            UPLOAD_PICTURE,
            # "accId_UIAButton_好",
            FROM_PHONE_PICTURE,
            RECENTLY,
            ID_FACE_PICTURE,
            ID_FACE_PICTURE_CONFIRM,
            ID_CONFIRM,
            CONFIRM_AGAIN,
        )

        self.perform_actions(
            MOBILE, mobile_new,
            MOBILE_GET_VERIFY_CODE,
        )

        verify_code = '123456'  # MysqlXjbTools().get_sms_verify_code(mobile=mobile_new, template_id='cif_changeMobile')

        self.perform_actions(
            MOBILE_VERIFY_CODE_INPUT, verify_code,
            MOBILE_CONFIRM,
            MODIFY_MOBILE_DONE,
        )

        page = huaxin_ui.ui_ios_xjb_3_0.personal_setting_page.PersonalSettingPage(self.web_driver)
        return page
