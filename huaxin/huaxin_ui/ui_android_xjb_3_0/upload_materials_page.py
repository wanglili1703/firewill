# coding=utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log

import huaxin_ui.ui_android_xjb_3_0.user_operation_succeed_page
import huaxin_ui.ui_android_xjb_3_0.set_phone_number_page

IMG_PICK_FRONT = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/img_pick_front']"
IMG_PICK_BACK = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/img_pick_back']"
IMG_PICK_HOLD = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/img_pickHold']"
FROM_PHONE_PICTURE = "xpath_//android.widget.TextView[@text='从手机相册选择']"
# CAMERA = "xpath_//android.widget.TextView[@text='相机']"
CAMERA = "xpath_//android.widget.TextView[@text='相册']"
# ID_CONFIRM = "xpath_//android.widget.ImageButton[@content-desc='确定']"
ID_SUBMIT_CONFIRM = "xpath_//android.widget.Button[@text='确认提交']"
REPEATED_SUBMIT_COMFIRM = "xpath_//android.widget.Button[@text='确定']"
PHOTO = "xpath_//android.widget.TextView[@resource-id='com.miui.gallery:id/pick_num_indicator']"
SWIPE_BEGIN = "swipe_xpath_//"
CONFIRM_SWIPE_STOP = "swipe_xpath_//android.widget.Button[@text='确认提交']"


class UploadMaterialsPage(PageObject):
    def __init__(self, web_driver, device_id=None):
        super(UploadMaterialsPage, self).__init__(web_driver)
        self._return_page = {
            'UserOperationSucceedPage': huaxin_ui.ui_android_xjb_3_0.user_operation_succeed_page.UserOperationSucceedPage(
                self.web_driver),
            'SetPhoneNumberPage': huaxin_ui.ui_android_xjb_3_0.set_phone_number_page.SetPhoneNumberPage(
                self.web_driver, device_id),
        }

    @robot_log
    def verify_page_title(self):
        self.assert_values('上传资料', self.get_text(self.page_title, 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def upload_photo(self, return_page='UserOperationSucceedPage'):
        if return_page == 'UserOperationSucceedPage':
            # 上传正面照
            self.perform_actions(IMG_PICK_FRONT,
                                 FROM_PHONE_PICTURE,
                                 # CAMERA
                                 )

            self.perform_actions(PHOTO)

            # 上传反面照
            self.perform_actions(IMG_PICK_BACK,
                                 FROM_PHONE_PICTURE,
                                 # CAMERA
                                 )

            self.perform_actions(PHOTO)

        # 上传手持身份证照
        self.perform_actions(IMG_PICK_HOLD,
                             FROM_PHONE_PICTURE)

        # if return_page == 'UserOperationSucceedPage':
        #     self.perform_actions(CAMERA)

        self.perform_actions(PHOTO)

        self.perform_actions(SWIPE_BEGIN, CONFIRM_SWIPE_STOP, 'U')
        # self.perform_actions(ID_CONFIRM,
        self.perform_actions(ID_SUBMIT_CONFIRM)

        # if return_page == 'UserOperationSucceedPage':
        self.perform_actions(REPEATED_SUBMIT_COMFIRM)

        page = self._return_page[return_page]

        return page
