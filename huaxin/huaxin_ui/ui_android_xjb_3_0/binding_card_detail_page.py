# coding: utf-8

from  _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.user_operation_succeed_page
import huaxin_ui.ui_android_xjb_3_0.binding_card_complete_page
from _tools.mysql_xjb_tools import MysqlXjbTools
from _common.global_config import ASSERT_DICT

CARD_NO = "xpath_//android.widget.EditText[@text='请输入您的储蓄卡卡号']"
PHONE_NO = "xpath_//android.widget.EditText[@text='请输入银行预留手机号码']"
GET_VERIFY_CODE = "xpath_//android.widget.Button[@text='获取验证码']"
VERIFY_CODE_INPUT = "xpath_//android.widget.EditText[@text='请输入验证码']"
BINDIND_CARD_CONFIRM = "xpath_//android.widget.Button[@text='下一步']"
USER_NAME = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/bind_card_username']"
ID = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/bind_card_certID']"
SWIPE_BEGIN = "swipe_xpath_//android.view.View[@resource-id='com.shhxzq.xjb:id/lv_filter']"
SCROLL = "swipe_xpath_//scroll_1"
NEXT = "xpath_//android.widget.Button[@text='下一步']"
ID_TYPE = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/bind_card_select_card_type']"
ID_TYPE_COMPLETE = "xpath_//android.widget.TextView[@text='完成']"
MODIFY = "xpath_//android.widget.Button[@text='修改']"


class BindingCardDetailPage(PageObject):
    def __init__(self, web_driver, device_id=None):
        super(BindingCardDetailPage, self).__init__(web_driver, device_id)
        self._db = MysqlXjbTools()

    @robot_log
    def verify_page_title(self):
        self.assert_values('绑定银行卡', self.get_text(self.page_title, 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def binding_card(self, bank_card_no, mobile):
        self.perform_actions(
            CARD_NO, bank_card_no,
            PHONE_NO, mobile,
            GET_VERIFY_CODE,
        )
        last_card_no = bank_card_no[-4:]
        ASSERT_DICT.update({'last_card_no': last_card_no})

        verification_code = self._db.get_sms_verify_code(mobile=mobile, template_id='cif_bindBankCard')

        self.perform_actions(
            VERIFY_CODE_INPUT, verification_code,
            BINDIND_CARD_CONFIRM
        )

        page = huaxin_ui.ui_android_xjb_3_0.user_operation_succeed_page.UserOperationSucceedPage(self.web_driver)

        return page

    @robot_log
    def verify_user_information(self, id_no, user_name, id_type='id_card'):
        user_information = self.get_text('com.shhxzq.xjb:id/dtv_user_info', 'find_element_by_id')
        name_text = user_information.split('\n\n')[0]
        id_text = user_information.split('\n\n')[1]
        name = name_text.split('：')[0]
        name_detail = name_text.split('：')[1]

        id_type_detail = id_text.split('：')[0]
        id_detail = id_text.split('：')[1]

        self.assert_values('姓    名', name)
        self.assert_values(user_name, name_detail)
        self.assert_values(id_no, id_detail)
        if id_type == 'HK_laissez_passer':
            self.assert_values('港澳通行证', id_type_detail)
        elif id_type == 'T_laissez_passer':
            self.assert_values('台湾通行证', id_type_detail)
        elif id_type == 'id_card':
            self.assert_values('身份证', id_type_detail)

        page = self
        return page

    @robot_log
    def modify_user_information(self):
        self.perform_actions(MODIFY)

        page = self
        return page

    @robot_log
    def binding_card_input_user_information(self, banding_card_user_name, id_no, id_type='id_card'):
        self.perform_actions(USER_NAME, banding_card_user_name)
        if id_type == 'laissez_passer':
            self.perform_actions(ID_TYPE)
            self.assert_values('选择证件类型', self.get_text('com.shhxzq.xjb:id/tv_title', 'find_element_by_id'))
            self.perform_actions(SWIPE_BEGIN, SCROLL, 'U',
                                 ID_TYPE_COMPLETE)

        self.perform_actions(ID, id_no,
                             NEXT)

        page = self

        return page

    def binding_card_first_time(self, bank_card_no, mobile):
        self.perform_actions(CARD_NO, bank_card_no,
                             PHONE_NO, mobile,
                             GET_VERIFY_CODE,
                             )
        last_card_no = bank_card_no[-4:]
        ASSERT_DICT.update({'last_card_no': last_card_no})

        verification_code = self._db.get_sms_verify_code(mobile=mobile, template_id='cif_bindBankCard')

        self.perform_actions(
            VERIFY_CODE_INPUT, verification_code,
            BINDIND_CARD_CONFIRM
        )

        page = huaxin_ui.ui_android_xjb_3_0.binding_card_complete_page.BindingCardCompletePage(self.web_driver)

        return page
