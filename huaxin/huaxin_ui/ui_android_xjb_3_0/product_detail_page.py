# coding: utf-8

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log

import huaxin_ui.ui_android_xjb_3_0.product_purchase_page
import huaxin_ui.ui_android_xjb_3_0.product_history_income_page
import huaxin_ui.ui_android_xjb_3_0.frequently_asked_question_page
import huaxin_ui.ui_android_xjb_3_0.finance_product_search_page
from _common.global_config import ASSERT_DICT

PURCHASE_BUTTON = "xpath_//android.widget.Button[@text='立即购买']"
INCOME_CALCULATOR = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/profit_caculator']"
CALCULATOR_CONFIRM = "xpath_//android.widget.TextView[@resource-id='com.shhxzq.xjb:id/bt_ok']"
HISTORY = "xpath_//android.widget.ImageView[@resource-id='com.shhxzq.xjb:id/goto_histroy']"
SWIPE_BEGIN = "swipe_xpath_//"
PERFORMANCE_STOP = "swipe_xpath_//android.widget.TextView[@text='投资目标']"
RECENT_THREE_MONTHS = "xpath_//android.view.View[@index='1']"
RECENT_SIX_MONTHS = "xpath_//android.view.View[@index='2']"
RECENT_ONE_YEAR = "xpath_//android.view.View[@index='3']"
RECENT_THREE_YEARS = "xpath_//android.view.View[@index='4']"
NAV_TREND = "xpath_//android.widget.TextView[@text='净值走势']"
INVEST_MANAGER = "xpath_//android.widget.TextView[@text='投资经理']"
RULES = "xpath_//android.widget.TextView[@text='规则']"
CONTRACT = "xpath_//android.widget.TextView[@text='合同公告']"
PLAN_DESCRIPTION = "xpath_//android.widget.TextView[@text='现金管理1号计划说明书']"
PLAN_DESCRIPTION_BACK = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left']"
PROBLEM_STOP = "swipe_xpath_//android.widget.TextView[@text='常见问题']"
PROBLEM = "xpath_//android.widget.TextView[@text='常见问题']"
BACK = "xpath_//android.widget.Button[@resource-id='com.shhxzq.xjb:id/btn_actionbar_left']"


class ProductDetailPage(PageObject):
    def __init__(self, web_driver):
        super(ProductDetailPage, self).__init__(web_driver)

    @robot_log
    def verify_page_title(self, product_name=None):
        if product_name is None:
            self.assert_values('产品详情', self.get_text('com.shhxzq.xjb:id/title_actionbar', 'find_element_by_id'))
        else:
            self.assert_values(product_name, self.get_text('com.shhxzq.xjb:id/title_actionbar', 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def verify_product_name(self, product_name, product_type=None):
        if product_type is None:
            self.assert_values(product_name, self.get_text('com.shhxzq.xjb:id/product_name', 'find_element_by_id'))
        else:
            self.assert_values(product_name, self.get_text('com.shhxzq.xjb:id/tv_product_name', 'find_element_by_id'))

        page = self

        return page

    @robot_log
    def verify_product_basic_information(self, product_name, product_type='精选系列'):
        if product_type == '固定收益系列':
            self.assert_values(product_name, self.get_text('com.shhxzq.xjb:id/tv_product_name', 'find_element_by_id'))
            self.assert_values('年化业绩比较基准',
                               self.get_text('com.shhxzq.xjb:id/product_details_yield_title', 'find_element_by_id'))
            self.assert_values('8.0-8.5%',
                               self.get_text('com.shhxzq.xjb:id/product_details_yield', 'find_element_by_id'))
            self.assert_values(True, self.element_exist("//android.widget.TextView[@text='投资期限']"))
            self.assert_values('100天',
                               self.get_text('com.shhxzq.xjb:id/product_details_deadline', 'find_element_by_id'))
            self.assert_values('低风险',
                               self.get_text('com.shhxzq.xjb:id/tv_product_details_levelofrisk', 'find_element_by_id'))
            # self.assert_values('固定期限', self.get_text('com.shhxzq.xjb:id/tv_freedom_take_out', 'find_element_by_id'))
            self.assert_values('固定收益型', self.get_text('com.shhxzq.xjb:id/tv_freedom_take_out', 'find_element_by_id'))
            self.assert_values('1元起投',
                               self.get_text('com.shhxzq.xjb:id/tv_product_details_pruchaseamt', 'find_element_by_id'))

        else:
            self.assert_values(product_name, self.get_text('com.shhxzq.xjb:id/product_name', 'find_element_by_id'))
            self.assert_values('净值日期', self.get_text('com.shhxzq.xjb:id/first_left_title', 'find_element_by_id'))
            self.assert_values('产品类型', self.get_text('com.shhxzq.xjb:id/second_left_title', 'find_element_by_id'))
            self.assert_values('投资期限', self.get_text('com.shhxzq.xjb:id/third_left_title', 'find_element_by_id'))
            self.assert_values('起投金额', self.get_text('com.shhxzq.xjb:id/fourth_left_title', 'find_element_by_id'))
            self.assert_values('风险等级', self.get_text('com.shhxzq.xjb:id/fifth_left_title', 'find_element_by_id'))
            if product_type == '精选系列':
                self.assert_values('2016.12.06',
                                   self.get_text('com.shhxzq.xjb:id/first_left_content', 'find_element_by_id'))
                self.assert_values('股权型', self.get_text('com.shhxzq.xjb:id/second_left_content', 'find_element_by_id'))
                self.assert_values('每日申赎', self.get_text('com.shhxzq.xjb:id/third_left_content', 'find_element_by_id'))
                self.assert_values('低', self.get_text('com.shhxzq.xjb:id/fifth_left_content', 'find_element_by_id'))
                self.assert_values('单位净值', self.get_text('com.shhxzq.xjb:id/first_right_title', 'find_element_by_id'))
                self.assert_values('1.0000',
                                   self.get_text('com.shhxzq.xjb:id/first_right_content', 'find_element_by_id'))
                self.assert_values('日涨幅', self.get_text('com.shhxzq.xjb:id/second_right_title', 'find_element_by_id'))
            elif product_type == '现金管理系列':
                self.assert_values('七日年化收益率',
                                   self.get_text('com.shhxzq.xjb:id/first_right_title', 'find_element_by_id'))
                self.assert_values('万份收益', self.get_text('com.shhxzq.xjb:id/second_right_title', 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def verify_product_other_information(self, product_name, detail_type='业绩'):
        if detail_type == '业绩':
            self.assert_values(True, self.element_exist("//android.widget.TextView[@text='累计回报']"))
            self.assert_values(True, self.element_exist("//android.widget.TextView[contains(@text,'本产品')]"))
            self.assert_values(True, self.element_exist("//android.widget.TextView[contains(@text,'沪深300')]"))
            self.perform_actions(SWIPE_BEGIN, PERFORMANCE_STOP, 'U')
            self.perform_actions(RECENT_THREE_MONTHS,
                                 RECENT_SIX_MONTHS,
                                 RECENT_ONE_YEAR,
                                 RECENT_THREE_YEARS)
            self.perform_actions(NAV_TREND)
            self.assert_values(True, self.element_exist("//android.widget.TextView[contains(@text,'本产品')]"))
            self.perform_actions(RECENT_THREE_MONTHS,
                                 RECENT_SIX_MONTHS,
                                 RECENT_ONE_YEAR,
                                 RECENT_THREE_YEARS)
            self.assert_values(True, self.element_exist("//android.widget.TextView[@text='投资目标']"))
            self.assert_values(True, self.element_exist("//android.widget.TextView[@text='暂无相关内容']"))
        elif detail_type == '投资经理':
            self.perform_actions(INVEST_MANAGER)
            self.assert_values(True, self.element_exist("//android.view.View[@content-desc='投资经理']"))
            self.assert_values(True, self.element_exist("//android.view.View[@content-desc='暂无相关内容']"))
        elif detail_type == '规则':
            self.perform_actions(RULES)
            self.assert_values(True, self.element_exist("//android.view.View[@content-desc='开放说明']"))
            self.assert_values(True, self.element_exist("//android.view.View[@content-desc='参与金额']"))
            self.assert_values(True, self.element_exist("//android.view.View[@content-desc='起投金额']"))
            self.assert_values(True, self.element_exist("//android.view.View[@content-desc='100万元']"))
            self.assert_values(True, self.element_exist("//android.view.View[@content-desc='追加金额']"))
            self.assert_values(True, self.element_exist("//android.view.View[@content-desc='1元']"))
            self.assert_values(True, self.element_exist("//android.view.View[@content-desc='单位份额面值']"))
            self.assert_values(True, self.element_exist("//android.view.View[@content-desc='1元']"))
            self.assert_values(True, self.element_exist("//android.view.View[@content-desc='费用信息']"))
        elif detail_type == '合同公告':
            self.perform_actions(CONTRACT)
            self.assert_values(True, self.element_exist("//android.widget.TextView[@text='法律文件']"))
            self.assert_values(True, self.element_exist("//android.widget.TextView[@text='现金管理1号计划说明书']"))
            self.perform_actions(PLAN_DESCRIPTION)
            self.perform_actions(PLAN_DESCRIPTION_BACK)
            self.assert_values(product_name, self.get_text('com.shhxzq.xjb:id/title_actionbar', 'find_element_by_id'))

        page = self
        return page

    @robot_log
    def go_to_product_purchase_page(self):
        self.perform_actions(PURCHASE_BUTTON)

        page = huaxin_ui.ui_android_xjb_3_0.product_purchase_page.ProductPurchasePage(self.web_driver)

        return page

    @robot_log
    def income_calculator(self, amount, product_type='DHB'):
        min_purchase_amount = '0'
        max_purchase_amount = '0'
        max_purchase_amount_text = '0'
        if product_type == 'DHB':
            max_purchase_amount_text = '50,000'
            min_purchase_amount_text = self.get_text('com.shhxzq.xjb:id/tv_product_details_pruchaseamt',
                                                     'find_element_by_id')
            min_purchase_amount = filter(lambda ch: ch in '0123456789.', min_purchase_amount_text)
            max_purchase_amount = filter(lambda ch: ch in '0123456789.', max_purchase_amount_text)
        elif product_type == 'VIP':
            max_purchase_amount_text = '100,000'
            min_purchase_amount_text = self.get_text(
                "//android.widget.TextView[@text='起投金额']/following-sibling::android.widget.TextView[1]")
            min_purchase_amount = filter(lambda ch: ch in '0123456789.', min_purchase_amount_text)
            max_purchase_amount = filter(lambda ch: ch in '0123456789.', max_purchase_amount_text)
        ASSERT_DICT.update({'min': float(min_purchase_amount)})
        ASSERT_DICT.update({'max': float(max_purchase_amount)})

        self.perform_actions(INCOME_CALCULATOR)

        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='收益计算器']"))
        self.assert_values(True, self.element_exist("//android.widget.TextView[@text='买入金额']"))
        if product_type == 'DHB':
            self.assert_values('预估累计收益(12个月)',
                               self.get_text('com.shhxzq.xjb:id/forecast_profit_title', 'find_element_by_id'))
        elif product_type == 'VIP':
            self.assert_values('预估累计收益',
                               self.get_text('com.shhxzq.xjb:id/forecast_profit_title', 'find_element_by_id'))
            self.assert_values(True,
                               self.element_exist("//android.widget.TextView[@text='同类货币基金']"))

        default_amount = self.get_text('com.shhxzq.xjb:id/amount_edit', 'find_element_by_id')
        self.assert_values(min_purchase_amount, default_amount)

        if product_type == 'DHB':
            key_code_dict = {
                '1': [0.185, 0.534], '2': [0.5, 0.534], '3': [0.815, 0.534],
                '4': [0.185, 0.604], '5': [0.5, 0.604], '6': [0.815, 0.604],
                '7': [0.185, 0.674], '8': [0.5, 0.674], '9': [0.815, 0.674],
                '.': [0.185, 0.75], '0': [0.5, 0.75], 'delete': [0.815, 0.75],
            }

        elif product_type == 'VIP':
            key_code_dict = {
                '1': [0.185, 0.663], '2': [0.5, 0.663], '3': [0.815, 0.663],
                '4': [0.185, 0.736], '5': [0.5, 0.736], '6': [0.815, 0.736],
                '7': [0.185, 0.807], '8': [0.5, 0.807], '9': [0.815, 0.807],
                '.': [0.185, 0.888], '0': [0.5, 0.888], 'delete': [0.815, 0.888],
            }

        # 删除默认值
        for arg in min_purchase_amount:
            self.click_screen(x=key_code_dict['delete'][0], y=key_code_dict['delete'][1])

        # 输入购买金额
        for arg in amount:
            self.click_screen(x=key_code_dict[arg][0], y=key_code_dict[arg][1])

        # 购买金额小于最小值
        if float(amount) < float(min_purchase_amount):
            self.assert_values(min_purchase_amount + '元起投',
                               self.get_text('com.shhxzq.xjb:id/bt_ok', 'find_element_by_id'))
        elif float(min_purchase_amount) < float(amount) <= float(max_purchase_amount):  # 购买金额正常
            self.assert_values('按此金额买入',
                               self.get_text('com.shhxzq.xjb:id/bt_ok', 'find_element_by_id'))
        elif float(amount) > float(max_purchase_amount):  # 购买金额大于最大值
            self.assert_values('最高买入' + max_purchase_amount_text + '元',
                               self.get_text('com.shhxzq.xjb:id/bt_ok', 'find_element_by_id'))
        page = self

        return page

    @robot_log
    def go_to_product_purchase_page_by_income_calculator(self):
        self.perform_actions(CALCULATOR_CONFIRM)

        page = huaxin_ui.ui_android_xjb_3_0.product_purchase_page.ProductPurchasePage(self.web_driver)

        return page

    @robot_log
    def go_to_high_end_history_income_page(self):
        self.perform_actions(HISTORY)

        page = huaxin_ui.ui_android_xjb_3_0.product_history_income_page.ProductHistoryIncomePage(self.web_driver)

        return page

    @robot_log
    def go_to_frequently_asked_question_page(self):
        self.perform_actions(SWIPE_BEGIN, PROBLEM_STOP, 'U')
        self.perform_actions(PROBLEM)

        page = huaxin_ui.ui_android_xjb_3_0.frequently_asked_question_page.FrequentlyAskedQuestionPage(self.web_driver)

        return page

    @robot_log
    def back_to_finance_product_search_page(self):
        self.perform_actions(BACK)

        page = huaxin_ui.ui_android_xjb_3_0.finance_product_search_page.FinanceProductSearchPage(
            self.web_driver)
        return page
