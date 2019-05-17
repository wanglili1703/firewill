# coding: utf-8
import decimal
import re

from _common.page_object import PageObject
from _common.xjb_decorator import robot_log

import huaxin_ui.ui_ios_xjb_3_0.product_purchase_page
import huaxin_ui.ui_ios_xjb_3_0.fund_invest_ranking_page
import huaxin_ui.ui_ios_xjb_3_0.finance_dqb_page
import huaxin_ui.ui_ios_xjb_3_0.fund_nav_page
import huaxin_ui.ui_ios_xjb_3_0.fund_annual_rate_page

PURCHASE_LOCATOR = "(UIButton_按此金额买入)"
PURCHASE_BUTTON = "accId_UIAButton_立即购买[POP]"
BUY_NOW_2 = "accId_UIAButton_追加购买[POP]"
BUY_NOW_3 = "accId_UIAButton_立即抢购[POP]"
BUY_NOW_4 = "accId_UIAButton_购买[POP]"
BUY_NOW_5 = "accId_UIAButton_1折费率购买[POP]"
CALCULATOR = "accId_UIAButton_(UIButton_hx_income_calculator)"
RETURN = "accId_UIAButton_UIBarButtonItemLocationLeft"
AMOUNT_INPUT = "accId_UIATextField_"
PURCHASE = "accId_UIAButton_%s" % PURCHASE_LOCATOR
DELETE_NUMBER = "accId_UIAButton_(UIButton_SafeKeyBoard_Back.png)"
NUMBER_KEY = "accId_UIAButton_(UIButton_%s)"
PERFORMANCE_BUTTON = "accId_UIAButton_业绩"
INVEST_MANAGER = "accId_UIAButton_投资经理"
RULE = "accId_UIAButton_规则"
CONTRACT_NOTICE = "accId_UIAButton_合同公告"
BASIC_BUTTON = "accId_UIAButton_概况"
COMBINATION_BUTTON = "accId_UIAButton_组合"
RATE_BUTTON = "accId_UIAButton_费率"
NOTICE_BUTTON = "accId_UIAButton_公告"
NAV = "xpathIOS_UIAButton_//UIAButton[@name='(UIButton_)' and @visible='true']"
DISTRIBUTION = "xpathIOS_UIAStaticText_//UIAScrollView/UIAWebView/UIAStaticText[@label='行业分布']"
BOND_TYPE = "xpathIOS_UIAStaticText_//UIAScrollView/UIAWebView/UIAStaticText[@label='债券品种']"
TEN_STOCKS = "xpathIOS_UIAStaticText_//UIAScrollView/UIAWebView/UIAStaticText[@label='十大股票']"
FIVE_BONDS = "xpathIOS_UIAStaticText_//UIAScrollView/UIAWebView/UIAStaticText[@label='五大债券']"
NOTICE_INFO = "xpathIOS_UIAStaticText_//UIAScrollView/UIATableView/UIATableCell/UIAStaticText[1]"
INTEREST_PER_WAN = "xpathIOS_UIAButton_//UIAButton[@label='万份收益']"
SEVEN_DAYS_RATE = "xpathIOS_UIAButton_//UIAButton[@label='七日年化收益率']"
MORE = "accId_UIAStaticText_(查看更多)"
VIEW_HISTORY = "accId_UIAStaticText_(UIButton_查看历史)"
BUY_CONTINUE = "accId_UIAButton_继续买入"


class ProductDetailPage(PageObject):
    def __init__(self, web_driver):
        super(ProductDetailPage, self).__init__(web_driver)
        self._return_page = {
            "FundInvestRankingPage": huaxin_ui.ui_ios_xjb_3_0.fund_invest_ranking_page.FundInvestRankingPage(
                self.web_driver),
            "FinanceDqbPage": huaxin_ui.ui_ios_xjb_3_0.finance_dqb_page.FinanceDqbPage(self.web_driver)
        }

    # product_type = 1, 高端和定活宝详情
    # product_type = 2, 基金详情
    @robot_log
    def verify_page_title(self, product_type=1):
        if product_type == 1:
            self.assert_values('产品详情', self.get_text("//UIAStaticText[@label='产品详情']"))
        else:
            self.assert_values('基金详情', self.get_text("//UIAStaticText[@label='基金详情']"))

        page = self
        return page

    @robot_log
    def view_monetary_fund_annual_rate_info_by_clicking_more(self):
        self.perform_actions(PERFORMANCE_BUTTON)
        self.perform_actions(INTEREST_PER_WAN,
                             MORE)

        page = huaxin_ui.ui_ios_xjb_3_0.fund_annual_rate_page.FundAnnualRatePage(self.web_driver)
        return page

    @robot_log
    def view_monetary_fund_annual_rate_info_by_clicking_view_history(self):
        self.perform_actions(PERFORMANCE_BUTTON,
                             SEVEN_DAYS_RATE)
        self.assert_values(True, self.element_exist("//UIAButton[contains(@label, '同类货币基金')]"))
        self.perform_actions(VIEW_HISTORY)

        page = huaxin_ui.ui_ios_xjb_3_0.fund_annual_rate_page.FundAnnualRatePage(self.web_driver)
        return page

    # fund_type = 1: 货币型基金
    # fund_type = 2: 非货币型基金
    @robot_log
    def fund_details_info(self, fund_type=1):
        if fund_type == 1:
            self.perform_actions(BASIC_BUTTON)
            self.assert_values("基金经理", self.get_text("//UIAStaticText[@label='基金经理']"))

            self.perform_actions(COMBINATION_BUTTON)
            self.perform_actions(BOND_TYPE)
            self.assert_values("债券名称", self.get_text("//UIAScrollView/UIAWebView/UIAStaticText[@label='债券名称']"))
            self.perform_actions(FIVE_BONDS)
            self.assert_values("债券名称", self.get_text("//UIAScrollView/UIAWebView/UIAStaticText[@label='债券名称']"))
            self.perform_actions(DISTRIBUTION)
            self.assert_values("暂无数据", self.get_text("//UIAScrollView/UIAWebView/UIAStaticText[@label='暂无数据']"))

            self.perform_actions(RATE_BUTTON)
            self.assert_values("申购费用", self.get_text("//UIAScrollView/UIAWebView/UIAStaticText[@label='申购费用']"))

            self.perform_actions(NOTICE_BUTTON,
                                 NOTICE_INFO)
            self.assert_values("基金公告", self.get_text("//UIAStaticText[@label='基金公告']"))
            self.perform_actions(RETURN)

            self.perform_actions(PERFORMANCE_BUTTON)
            self.assert_values(True, self.element_exist("//UIAButton[@label='七日年化收益率']"))

        else:
            self.perform_actions(BASIC_BUTTON)
            self.assert_values("基金经理", self.get_text("//UIAStaticText[@label='基金经理']"))

            self.perform_actions(COMBINATION_BUTTON)
            self.perform_actions(BOND_TYPE)
            # self.assert_values("债券名称", self.get_text("//UIAScrollView/UIAWebView/UIAStaticText[@label='债券名称']"))
            self.perform_actions(TEN_STOCKS)
            self.assert_values("股票名称", self.get_text("//UIAScrollView/UIAWebView/UIAStaticText[@label='股票名称']"))
            self.perform_actions(FIVE_BONDS)
            # self.assert_values("债券名称", self.get_text("//UIAScrollView/UIAWebView/UIAStaticText[@label='债券名称']"))
            self.perform_actions(DISTRIBUTION)
            self.assert_values("行业类别", self.get_text("//UIAScrollView/UIAWebView/UIAStaticText[@label='行业类别']"))

            self.perform_actions(RATE_BUTTON)
            self.assert_values("申购费用", self.get_text("//UIAScrollView/UIAWebView/UIAStaticText[@label='申购费用']"))

            self.perform_actions(NOTICE_BUTTON,
                                 NOTICE_INFO)
            self.assert_values("基金公告", self.get_text("//UIAStaticText[@label='基金公告']"))
            self.perform_actions(RETURN)

            self.perform_actions(PERFORMANCE_BUTTON)
            self.assert_values(True, self.element_exist("//UIAButton[contains(@name, '最大回撤')]"))

        self.verify_page_title(product_type=2)
        page = self
        return page

    @robot_log
    def go_to_history_nav(self):
        self.perform_actions(NAV)

        page = huaxin_ui.ui_ios_xjb_3_0.fund_nav_page.FundNavPage(self.web_driver)
        return page

    @robot_log
    def back_to_previous_page(self, return_page):
        self.perform_actions(RETURN)

        page = self._return_page[return_page]
        return page

    @robot_log
    def go_to_product_purchase_page(self):
        self.perform_actions(PURCHASE_BUTTON,
                             BUY_NOW_2,
                             BUY_NOW_3,
                             BUY_NOW_4,
                             BUY_NOW_5)

        # 当出现购买产品风险高于用户的风险测评结果, 就会出现风险提示, 有些还需要验证码输入.
        if self.element_exist(u'风险提示', 'find_element_by_accessibility_id'):
            self.perform_actions(
                BUY_CONTINUE,
            )

        page = huaxin_ui.ui_ios_xjb_3_0.product_purchase_page.ProductPurchasePage(self.web_driver)
        return page

    @robot_log
    def verify_total_income(self, amount, rate, days):
        expected_income = 0
        if str(days).__contains__('月'):
            month = filter(lambda ch: ch in '0123456789.', days)
            expected_income = decimal.Decimal(amount) * (decimal.Decimal(str(rate).split('%')[0]) / 100) * (
                decimal.Decimal(month) / 12)
        elif str(days).__contains__('天'):
            days = filter(lambda ch: ch in '0123456789.', days)
            expected_income = decimal.Decimal(amount) * decimal.Decimal(str(rate).split('%')[0]) * (
                decimal.Decimal(days) / 365)

        expected_income = decimal.Decimal(expected_income).quantize(decimal.Decimal('0.00'))

        actual_amount = self.get_text("//UIAStaticText[@label='买入金额']/following-sibling::UIAStaticText[3]")
        self.assert_values(actual_amount, '￥%s' % format(expected_income, ','))

        page = self
        return page

    @robot_log
    def dhb_calculator(self, amount, max_amount=None):
        # 获取收益率
        rate = '5.00%'

        self.perform_actions(PURCHASE_BUTTON,
                             BUY_NOW_2,
                             BUY_NOW_3,
                             )
        # 获取起投金额
        start_amount = self.get_text("//UIAButton[@name='(UIButton_)']/following-sibling::UIAStaticText")
        start_amount = re.findall(r'(\d+)元', start_amount)[0]
        self.perform_actions(RETURN)

        self.perform_actions(CALCULATOR)

        # 获取投资时间
        days = self.get_text("//UIAStaticText[contains(@label, '预估累计收益')]")

        # 验证计算器里面的值是默认的起投金额
        self.assert_values('￥%s' % start_amount,
                           self.get_text("//UIAStaticText[@label='买入金额']/following-sibling::UIAStaticText[1]"))

        # 验证累计收益
        self.verify_total_income(start_amount, rate, days)

        # 输入金额
        for i in start_amount:
            self.perform_actions(DELETE_NUMBER)

        for i in amount:
            self.perform_actions(NUMBER_KEY % i)
        if max_amount is None:
            self.verify_total_income(amount, rate, days)
        else:
            self.verify_total_income(max_amount, rate, days)
        if decimal.Decimal(amount) < decimal.Decimal(start_amount):
            # 验证买入按钮变灰, 且值为xxx元起投
            self.assert_values("%s元起投" % start_amount,
                               self.get_text(PURCHASE_LOCATOR, "find_element_by_accessibility_id"))
        else:
            if max_amount is None:
                self.assert_values("按此金额买入", self.get_text(PURCHASE_LOCATOR, "find_element_by_accessibility_id"))
                self.perform_actions(PURCHASE)

                page = huaxin_ui.ui_ios_xjb_3_0.product_purchase_page.ProductPurchasePage(self.web_driver)
                page.verify_at_product_purchase_page()
                page.verify_purchase_amount(amount)
                page.back_to_previous_page(return_page='ProductDetailPage')
            else:
                self.assert_values('￥%s' % format(decimal.Decimal(max_amount), ','),
                                   self.get_text("//UIAStaticText[@label='买入金额']/following-sibling::UIAStaticText[1]"))

        page = self
        return page

    @robot_log
    def vip_calculator(self, amount, min_amount, max_amount=None):
        start_amount = min_amount

        self.perform_actions(CALCULATOR)
        # 输入金额
        for i in str(start_amount).split('.')[0]:
            self.perform_actions(DELETE_NUMBER)

        for i in amount:
            self.perform_actions(NUMBER_KEY % i)

        self.assert_values(True, self.element_exist("//UIAStaticText[contains(@label, '预估累计收益(过去')]"))
        self.assert_values(True, self.element_exist("//UIAStaticText[contains(@label, '同类货币基金')]"))

        if decimal.Decimal(amount) < decimal.Decimal(start_amount):
            # 验证买入按钮变灰, 且值为xxx元起投
            self.assert_values("%s元起投" % format(decimal.Decimal(start_amount), ',').split('.')[0],
                               self.get_text(PURCHASE_LOCATOR, "find_element_by_accessibility_id"))
        else:
            if max_amount is None:
                self.assert_values("按此金额买入", self.get_text(PURCHASE_LOCATOR, "find_element_by_accessibility_id"))
                self.perform_actions(PURCHASE)

                page = huaxin_ui.ui_ios_xjb_3_0.product_purchase_page.ProductPurchasePage(self.web_driver)
                page.verify_at_product_purchase_page()
                page.verify_purchase_amount(amount)
                page.back_to_previous_page(return_page='ProductDetailPage')
            else:
                self.assert_values('￥%s' % format(decimal.Decimal(max_amount), ',').split('.')[0],
                                   self.get_text("//UIAStaticText[@label='买入金额']/following-sibling::UIAStaticText[1]"))

        page = self

        return page

    # product_type = 1: 定活宝
    # product_type = 3: 高端
    @robot_log
    def income_calculator(self, amount, product_type=1, min_amount=None, max_amount=None):
        if product_type == 1:
            if max_amount is None:
                self.dhb_calculator(amount)
            else:
                self.dhb_calculator(amount, max_amount)

        elif product_type == 3:
            self.vip_calculator(amount, min_amount, max_amount)

    # vip_type = 1: 现金管理系列 (一般是货币型产品)
    # vip_type = 2: 固定收益系列 (一般是固定收益产品)
    # vip_type = 3: 精选系列 (一般是股权型产品)
    @robot_log
    def high_end_product_details(self, vip_type):
        if vip_type == 1:
            self.perform_actions(INVEST_MANAGER)
            self.assert_values("投资经理", self.get_text("//UIAStaticText[@label='投资经理']"))

            self.perform_actions(RULE)
            self.assert_values("开放说明", self.get_text("//UIAStaticText[@label='开放说明']"))

            self.perform_actions(CONTRACT_NOTICE)
            self.assert_values("法律文件", self.get_text("//UIAStaticText[@label='法律文件']"))

            self.perform_actions(PERFORMANCE_BUTTON)
            self.assert_values(True, self.element_exist("//UIAButton[@label='七日年化收益率']"))

        elif vip_type == 2:
            self.assert_values(True, self.element_exist("(UIButton_固定收益型)", "find_element_by_accessibility_id"))
            self.assert_values(True, self.element_exist("//UIAButton[contains(@name, '风险')]"))
            self.assert_values("开放说明", self.get_text("//UIAStaticText[@label='开放说明']"))
            self.assert_values("收益分配", self.get_text("//UIAStaticText[@label='收益分配']"))
            self.assert_values("费用信息", self.get_text("//UIAStaticText[@label='费用信息']"))
            self.assert_values("参与金额", self.get_text("//UIAStaticText[@label='参与金额']"))

        elif vip_type == 3:
            self.perform_actions(INVEST_MANAGER)
            self.assert_values("投资经理", self.get_text("//UIAStaticText[@label='投资经理']"))

            self.perform_actions(RULE)
            self.assert_values("开放说明", self.get_text("//UIAStaticText[@label='开放说明']"))

            self.perform_actions(CONTRACT_NOTICE)
            self.assert_values("法律文件", self.get_text("//UIAStaticText[@label='法律文件']"))

            self.perform_actions(PERFORMANCE_BUTTON)
            self.assert_values(True, self.element_exist("//UIAButton[@label='累计回报']"))
            self.assert_values(True, self.element_exist("//UIAButton[@label='净值走势']"))

        self.verify_page_title()
        page = self
        return page
