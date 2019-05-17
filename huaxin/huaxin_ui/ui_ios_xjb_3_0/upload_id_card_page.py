# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_ios_xjb_3_0.id_input_page
import huaxin_ui.ui_ios_xjb_3_0.binding_card_page

ID_NUMBER_SIDE = "accId_UIAStaticText_(HXIDCardListPersonalInfoCell)"
PIC1 = "xpathIOS_UIACollectionCell_//UIACollectionCell[1]"
PIC2 = "xpathIOS_UIACollectionCell_//UIACollectionCell[2]"
ID_NUMBER_OPPOSITE = "accId_UIAStaticText_(HXIDCardListExpirateInfoCell)"
PICTURE = "accId_UIAButton_(UIButton_exocr-photo_camera_btn.png)"
QQ = "accId_UIAStaticText_QQ"
INPUT_ID_INFO = "accId_UIAStaticText_(手动输入身份信息)"
NEXT = "accId_UIAButton_下一步"

current_page = []


class UploadIdCardPage(PageObject):
    def __init__(self, web_driver):
        super(UploadIdCardPage, self).__init__(web_driver)
        self.elements_exist(*current_page)

    @robot_log
    def verify_at_upload_id_card_page(self):
        self.assert_values("绑定银行卡", self.get_text("//UIAStaticText[@label='绑定银行卡']"))

        page = self
        return page

    @robot_log
    def upload_id_card(self):
        self.perform_actions(ID_NUMBER_SIDE,
                             PICTURE,
                             QQ,
                             PIC1,
                             ID_NUMBER_OPPOSITE,
                             PICTURE,
                             QQ,
                             PIC2,
                             NEXT
                             )

        page = self
        return page

    @robot_log
    def go_to_user_input_id_info_page(self):
        self.perform_actions(INPUT_ID_INFO)

        page = huaxin_ui.ui_ios_xjb_3_0.id_input_page.IdInputPage(self.web_driver)
        return page
