# coding: utf-8
import time

from _common.page_object import PageObject

from _common.xjb_decorator import robot_log
from _tools.mysql_xjb_tools import MysqlXjbTools
import huaxin_ui.ui_ios_xjb_3_0.debit_card_add_finish_page
import huaxin_ui.ui_ios_xjb_3_0.upload_id_card_page

# SWIPE_START = "swipe_accId_//"
BIND_CARD = "axis_IOS_绑定银行卡"
SWIPE_STOP_CONFIRM = "xpathIOS_UIAButton_/AppiumAUT/UIAApplication/UIAWindow/UIAButton"

# CARD_NO = "xpathIOS_UIATextField_//UIATableCell/UIATextField[@value='请输入您的储蓄卡卡号']"
CARD_NO = "xpathIOS_UIATextField_" \
          "/AppiumAUT/UIAApplication/UIAWindow/UIATableView/UIATableCell[2]/UIATextField[@value='请输入您的储蓄卡卡号']"
CARD_TYPE = "accId_UIAStaticText_选择发卡行"
# PHONE_NO = "xpathIOS_UIATextField_//UIATableCell/UIATextField[@value='请输入银行预留手机号码']"
PHONE_NO = "xpathIOS_UIATextField_" \
           "/AppiumAUT/UIAApplication/UIAWindow/UIATableView/UIATableCell[4]/UIATextField[@value='请输入银行预留手机号码']"
GET_VERIFY_CODE = "accId_UIAButton_获取验证码"
# GET_VERIFY_CODE = "accId_UIAButton_重新获取"
VERIFY_CODE_INPUT = "xpathIOS_UIATextField_//UIATableCell/UIATextField[@value='请输入验证码']"
BINDING_CARD_CONFIRM = "accId_UIAButton_(UIButton_确定)"

BINDIND_CARD_DONE = "accId_UIAButton_(UIButton_先逛逛)"

# BANK_CARD_FIRST = "accId_UIAStaticText_(**** **** **** %s)"
BANK_CARD_FIRST = "xpathIOS_UIAStaticText_//UIAStaticText[contains(@name, '**** **** ****')]"
BANK_CARD_LAST_CARD_NO = "xpath_//*[contains(@text,'%s')]"
BANK_CARD_OPERATOR = "accId_UIAButton_UIBarButtonItemLocationRight"
BANK_CARD_DELETE = "accId_UIAButton_删除"
TRADE_PASSWORD = "xpathIOS_UIATextField_/AppiumAUT/UIAApplication/UIAWindow/UIATextField"
BANK_CARD_DELETE_CONFIRM = "accId_UIAButton_(UIButton_确认)"

current_page = []


class BankCardManagementPage(PageObject):
    def __init__(self, web_driver):
        super(BankCardManagementPage, self).__init__(web_driver)
        self.elements_exist(*current_page)
        self._db = MysqlXjbTools()

    @robot_log
    def verify_bank_card_management_page(self):
        self.assert_values("银行卡管理", self.get_text("//UIAStaticText[@label='银行卡管理']"))
        page = self
        return page

    @robot_log
    def click_bind_card(self, trade_password=None, real_named=1):
        self.perform_actions(BIND_CARD)

        page = None
        if real_named == 1:
            # 实名的
            page = self
        elif real_named == 0:
            # 未实名的
            self.perform_actions(TRADE_PASSWORD, trade_password,
                                 TRADE_PASSWORD, trade_password,
                                 )
            page = huaxin_ui.ui_ios_xjb_3_0.upload_id_card_page.UploadIdCardPage(self.web_driver)

        return page

    # flag = 0, 用户银行卡管理页面有绑定的银行卡。
    # flag = 1, 用户银行卡管理页面没有绑定的银行卡。
    @robot_log
    def binding_card(self, bank_card_no, phone_number, flag=0):
        if flag == 0:
            self.perform_actions(
                # SWIPE_START, SWIPE_STOP, 'U',
                SWIPE_STOP_CONFIRM, )
        else:
            self.perform_actions(BIND_CARD)

        self.perform_actions(
            CARD_NO, bank_card_no,
            # CARD_TYPE,
            PHONE_NO, phone_number,
            GET_VERIFY_CODE,
        )

        verification_code = MysqlXjbTools().get_sms_verify_code(mobile=phone_number, template_id='cif_bindBankCard')

        self.perform_actions(
            VERIFY_CODE_INPUT, verification_code,
            # BINDIND_CARD_BLANK,
            BINDING_CARD_CONFIRM,
            # BINDIND_CARD_DONE,
        )

        page = huaxin_ui.ui_ios_xjb_3_0.debit_card_add_finish_page.DebitCardAddFinishPage(self.web_driver)

        return page

    @robot_log
    def delete_band_card(self, trade_password):
        self.perform_actions(
            BANK_CARD_FIRST,
            BANK_CARD_OPERATOR,
            BANK_CARD_DELETE,
            TRADE_PASSWORD, trade_password,
        )

        page = huaxin_ui.ui_ios_xjb_3_0.debit_card_add_finish_page.DebitCardAddFinishPage(self.web_driver)

        return page
