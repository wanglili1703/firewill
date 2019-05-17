# coding=utf-8
from _common.page_object import PageObject
from _common.xjb_decorator import robot_log

SWIPE_BEGAIN="swipe_xpath_//"
FUND_TYPE="xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/all_fund_type_ddv']"
RATING_TYPE="xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/all_fund_rating_ddv']"
DATA_TYPE="xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/all_fund_date_ddv']"
FUND_COMPANY_LIST="xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/all_fund_company_ddv']"
SELECT_FUND_COMPANY="xpath_//android.widget.TextView[@text='博时基金管理有限公司']"
TYPE_SCROLL = "swipe_xpath_//scroll_1"
SELECT_DONE = "xpath_//android.widget.TextView[@text='完成']"


class FundFilterPage(PageObject):
    def __init__(self, web_driver):
        super(FundFilterPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self):
        self.assert_values('筛选器', self.get_text(self.page_title, 'find_element_by_id'))
        page = self

        return page

    @robot_log
    def fund_filter(self):
        self.perform_actions(FUND_TYPE,
                             SWIPE_BEGAIN, TYPE_SCROLL, 'U',
                             SELECT_DONE,
                             RATING_TYPE,
                             SWIPE_BEGAIN,TYPE_SCROLL , 'U',
                             SELECT_DONE,
                             DATA_TYPE,
                             SWIPE_BEGAIN,TYPE_SCROLL,'U',
                             SELECT_DONE,
                             FUND_COMPANY_LIST)

        self.assert_values('基金公司', self.get_text(self.page_title, 'find_element_by_id'))

        self.perform_actions(SELECT_FUND_COMPANY
                             )

        page = self
        return page

    @robot_log
    def verify_fund_filter_results(self):
        self.assert_values('股票型', self.get_text('com.shhxzq.xjb:id/all_fund_type_ddv', 'find_element_by_id').replace(' ',''))
        self.assert_values('银河证券', self.get_text('com.shhxzq.xjb:id/all_fund_rating_ddv', 'find_element_by_id').replace(' ',''))
        self.assert_values('近3年', self.get_text('com.shhxzq.xjb:id/all_fund_date_ddv', 'find_element_by_id').replace(' ',''))
        self.assert_values('博时基金管理有限公司', self.get_text('com.shhxzq.xjb:id/all_fund_company_ddv', 'find_element_by_id').replace(' ',''))
        self.assert_values('银河证券', self.get_text('com.shhxzq.xjb:id/tv_fund_rating_name', 'find_element_by_id'))
        self.assert_values('近3年', self.get_text('com.shhxzq.xjb:id/tv_fund_period', 'find_element_by_id'))

        page = self
        return page


