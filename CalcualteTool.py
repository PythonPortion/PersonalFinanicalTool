from dataclasses import dataclass


@dataclass
class EachMonthPayment:
    """
    Class to represent each month payment information.
    """
    month_index: int  # index of month
    each_month_payment: float
    each_month_principal: float
    each_month_interest: float
    rest_principal: float


def calculate_equal_installment(principle, monthly_rate, months):
    """
    计算等额本息每月的还款信息
    :param principle: 本金
    :param monthly_rate: 月利率
    :param months: 还款月数
    :return: 数组(month_index,each_month_payment,each_month_principal,each_month_interest)
    """
    # 等额本息的算法
    each_month_payment = (principle
                          *
                          monthly_rate * (1 + monthly_rate) ** months
                          /
                          ((1 + monthly_rate) ** months - 1))

    # The info_list contains a EachMonthPayment
    info_list = []

    for month_index in range(1, months + 1):
        each_month_interest = principle * monthly_rate
        each_month_principal = each_month_payment - each_month_interest
        principle -= each_month_principal
        rest_principal = principle
        result = EachMonthPayment(month_index,
                                  each_month_payment,
                                  each_month_principal,
                                  each_month_interest,
                                  rest_principal)
        info_list.append(result)
    return info_list
