# coding: utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log

PHONE_NO = "xpath_//android.widget.EditText[@resource-id='com.shhxzq.xjb:id/et_inviter_mobile']"
REFEREE_CONFIRM = "xpath_//android.widget.Button[@text='确定']"
CONTACTS = "xpath_//android.widget.TextView[@text='邀请人手机号']/following-sibling::android.widget.LinearLayout[1]/android.widget.ImageView[1]"
PERMISSION = "xpath_//android.widget.Button[@text='始终允许']"
SELECT_CONTACTS = "xpath_//android.widget.TextView[@text='选择联系人']"


class MyRefereePage(PageObject):
    def __init__(self, web_driver):
        super(MyRefereePage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('邀请人', self.get_text(self.page_title, 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def my_referee(self, phone_no):
        self.perform_actions(PHONE_NO, phone_no,
                             REFEREE_CONFIRM,
                             CONTACTS,
                             )

        # self.perform_actions(PERMISSION)
        # self.assert_values('选择联系人', self.get_text('android:id/action_bar_title', 'find_element_by_id'))
        self.perform_actions(SELECT_CONTACTS)
        # self.assert_values('选择联系人', self.get_text('android:id/text1', 'find_element_by_id'))
        self.assert_values('请选择联系人', self.get_text('android:id/title', 'find_element_by_id'))

        page = self

        return page
