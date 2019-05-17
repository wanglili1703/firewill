# coding=utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log
import huaxin_ui.ui_android_xjb_3_0.fund_selected_page

DELETE="xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/iv_fund_fav_del']"
COMFIRM="xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/button2']"
TIP="//android.widget.TextView[@text='暂无内容']"
SELECTED_FUND_DELETE_DONE="xpath_//android.widget.Button[@text='完成']"

class FundSelectedFundManagementPage(PageObject):
    def __init__(self, web_driver):
        super(FundSelectedFundManagementPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('自选基金', self.get_text('com.shhxzq.xjb:id/title_actionbar', 'find_element_by_id'))
        page = self

        return page

    @robot_log
    def delete_selected_fund(self):
        self.perform_actions(DELETE,
                             COMFIRM)
        page = self

        return page

    @robot_log
    def verify_no_selected_fund_tip(self):
        self.assert_values('True',str(self.element_exist(TIP)))

        page = self
        return page

    @robot_log
    def back_to_fund_selected_page(self):
        self.perform_actions(SELECTED_FUND_DELETE_DONE)

        page = huaxin_ui.ui_android_xjb_3_0.fund_selected_page.FundSelectedPage(self.web_driver)
        return page



