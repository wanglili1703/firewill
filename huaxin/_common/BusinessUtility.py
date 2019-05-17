# coding=utf-8
import decimal

import datetime


class BusinessUtility(object):
    def __init__(self):
        pass

    def calculate_pledge_quty(self, loan_amt, pledge_ratio, prod_nav, interest=0):
        pledge_quty = (decimal.Decimal(loan_amt) + decimal.Decimal(interest)) / (
            decimal.Decimal(pledge_ratio) * decimal.Decimal(prod_nav))

        return decimal.Decimal(pledge_quty).quantize(decimal.Decimal('0.00'))

    # 计算质押的最后还款日
    # prod_carry_date 产品到期日 pledge_force_repay_date 最终强制还款日 repay_days 借款日
    def calculate_pledge_final_repay_date(self, prod_carry_date, pledge_force_repay_date, repay_days):
        # 不能超过到期日的前一个工作日
        before_carry_date = datetime.datetime.strftime(
            datetime.datetime.strptime(str(prod_carry_date), '%Y%m%d') - datetime.timedelta(days=1), '%Y%m%d')
        # 借款日 + 借款期限
        repay_date = None
        if repay_days != '' and repay_days != None and repay_days != 'None':
            repay_date = datetime.datetime.strftime(
                datetime.datetime.today() + datetime.timedelta(days=int(repay_days)), '%Y%m%d')

        temp = self.get_min_date(date1=before_carry_date, date2=repay_date)
        min_date = self.get_min_date(temp, pledge_force_repay_date)

        return min_date

    # 返回日期小的
    def get_min_date(self, date1, date2):
        if date1 is None or date1 == '':
            return date2

        if date2 is None or date2 == '':
            return date1

        if date1 >= date2:
            return date2
        else:
            return date1

    # 根据选择的日期，如果选择的这个日期在今天之后，则直接返回选择日期，否则计算下个月的这一天, 返回其相应格式的日期
    def get_next_pay_date(self, day, date_format):
        today = datetime.date.today()
        next_month = today.month + 1
        year = today.year
        if next_month > 12:
            next_month -= 12
            year = today.year+1
        the_day_next_month = datetime.date(year, next_month, int(day))
        the_day_this_month = datetime.date(year, today.month, int(day))
        if the_day_this_month > today:
            return the_day_this_month.strftime(date_format)
        else:
            return the_day_next_month.strftime(date_format)

    # 保留几位小数，但是不进行四舍五入
    def cut(self, num, c):
        c = 10 ** (-c)
        return (num // c) * c

    # 计算定活宝赎回金额
    def calculate_dhb_redeem_amount(self, redeem_amt, hold_start_date, rate):
        today = datetime.datetime.today()
        hold_days = (today - datetime.datetime.strptime(str(hold_start_date), '%Y%m%d')).days
        # 赎回总金额 = 赎回金额 + 赎回金额收益 （赎回金额收益=持有天数 * 利率 * 赎回金额/ 365）
        rate = decimal.Decimal(rate) / 100
        redeem_income = rate * decimal.Decimal(redeem_amt) * hold_days / 365
        # redeem_income = self.cut(float(redeem_income), 2)
        redeem_income = round(redeem_income, 2)

        total_redeem_amt = float(redeem_amt) + redeem_income
        return total_redeem_amt, redeem_income

    # 借款利息 = 借款金额 * 借款利率 * 实际借贷天数 / 365，结果进行四舍五入（质押）
    def cal_interest(self, loan_amt, loan_rate, borrow_days):
        if borrow_days == '0':
            borrow_days = 1
        interest = decimal.Decimal(loan_amt) * decimal.Decimal(loan_rate) * decimal.Decimal(borrow_days) / 365
        interest = round(interest, 2)
        return interest

    # 还款利息 = 还款本金 / 剩余未还借款本金 * 利息 （质押还款）
    def cal_repay_interest(self, repay_amt, borrow_amt, interest):
        repay_interest = decimal.Decimal(repay_amt) / decimal.Decimal(borrow_amt) * decimal.Decimal(interest)
        repay_interest = round(repay_interest, 2)
        if repay_interest == 0.0:
            repay_interest = 0.01
        return repay_interest

    # 解压份额 = 原本质押份额 - 仍然需要质押的份额
    # 仍然需要质押的份额 = （原应还本息-本次还款本息）/(最初的质押比*现在的净值）
    def cal_pledge_quty(self, total_pledge_quty, total_repay_amt, repay_amt, repay_amt_before, pledge_rate,
                        pledge_quty_before):
        if repay_amt_before is None or pledge_quty_before is None:
            repay_amt_before = 0
            pledge_quty_before = 0
        need_pledge = (decimal.Decimal(total_repay_amt) - decimal.Decimal(repay_amt) - decimal.Decimal(
            repay_amt_before)) / decimal.Decimal(pledge_rate)
        need_pledge = round(need_pledge + decimal.Decimal(0.004), 2)
        pledge_quty = decimal.Decimal(total_pledge_quty) - decimal.Decimal(need_pledge) - decimal.Decimal(
            pledge_quty_before)
        print 'pledge_quty = ' + str(pledge_quty)
        if pledge_quty < 0:
            pledge_quty = 0.00
        return pledge_quty


if __name__ == '__main__':
    m = BusinessUtility()
    print m.get_next_pay_date(day=5, date_format='%Y%m%d')
    # print m.calculate_dhb_redeem_amount(redeem_amt='10', hold_start_date='20170530', rate='5.0000')
    # print m.cal_interest(loan_amt='5000', loan_rate='0.0500', borrow_days='1')
    # print m.cal_repay_interest(repay_amt='10', borrow_amt='40000', interest='10.96')
    # print m.cal_pledge_quty(total_pledge_quty='999886.95', total_repay_amt='799909.56', repay_amt='50.01',
    #                         repay_amt_before='500.1', pledge_rate='0.8', pledge_quty_before='625.12')
