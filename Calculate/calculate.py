from Models.M import EachMonthPayment

"""
逻辑要求：
    计算每个月还款额.满足一下功能
    - 提前还款
    - 利率调整
    
    分析：
        利率调整，和提前还款一定是数组
        利率调整的实体包含： 调整起始日期，利率
        提前还款的时期包含： 提前还款日期，还款额度
"""

def each_installment(principle, monthly_rate, months):
    """
    核心业务逻辑: 计算等额本息每月的还款信息
    :param principle: 本金
    :param monthly_rate: 月利率
    :param months: 还款月数
    :return: 数组(month_index,each_month_payment,each_month_principal,each_month_interest)
    """
    p = principle
    r = monthly_rate
    m = months

    # 等额本息的算法
    each_month_payment = (p * (r * (1 + r) ** m) / ((1 + r) ** m - 1))

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
