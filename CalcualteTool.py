from Models.M import EachMonthPayment
from Models.M import LoanType
from Models.M import LoanSubItem
from Models.M import LoanInfo
from dateutil.relativedelta import relativedelta


def print_detail(info: EachMonthPayment,
                 loan_sub_item: LoanSubItem,
                 total_payment: float,
                 total_interest: float,
                 total_payment_principal: float,
                 month_interval: int = 0):
    """
    输出详细信息
    :param info: 每个月的还款信息
    :param loan_sub_item: 每一个利率周期的实体
    :param total_payment: 总还款额
    :param total_interest: 总利息
    :param total_payment_principal: 总共还款本金
    :param month_interval: 每一个利率周期的 月度总数
    :return:
    """

    month_index = info.month_index + month_interval
    new_date = loan_sub_item.init_date + relativedelta(months=month_index)
    date_str = new_date.strftime("%Y-%m-%d")
    formatted_month = f"{month_index:03}"
    print(
        f"\t{date_str},"
        f"第{formatted_month:^5}月: "
        f"还款 {info.each_month_payment:.2f}, "
        f"本金 {info.each_month_principal:.2f}, "
        f"利息 {info.each_month_interest:.2f}, "
        f"总还款 {total_payment:.2f}, "
        f"总支付利息 {total_interest:.2f}, "
        f"总支付本金 {total_payment_principal:.2f}, "
        f"剩余本金 {info.rest_principal:.2f}")


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


def get_gj_or_sd_info(loan_info: LoanInfo, loan_item_list: list[LoanSubItem]):
    month_interval: int = 0
    previous_month_index = 0
    total_payment: float = 0.0
    total_interest: float = 0.0
    total_payment_principal: float = 0.0
    for index, loanItem in enumerate(loan_item_list):
        equal_installment = calculate_equal_installment(
            loan_info.rest_principal,
            loanItem.month_rate,
            loan_info.rest_months
        )
        # 输出详细信息
        for each_month_pay_info in equal_installment:
            if each_month_pay_info.month_index > loanItem.interval_month:
                print("------------------------------------" * 2)
                break

            coming_month_index = each_month_pay_info.month_index + month_interval

            if not loan_info.need_all_detail:
                # 不需要打印太多，最后一次的调整 + 24个月即可
                if index == len(loan_item_list) - 1:
                    if coming_month_index > previous_month_index + 24:
                        break
                else:
                    previous_month_index += 1

            total_payment += each_month_pay_info.each_month_payment
            total_interest += each_month_pay_info.each_month_interest
            total_payment_principal += each_month_pay_info.each_month_principal

            print_detail(each_month_pay_info,
                         loanItem,
                         total_payment,
                         total_interest,
                         total_payment_principal,
                         month_interval)

            if coming_month_index % 12 == 0:
                print("**********"*15)

        last_portion_index = loanItem.interval_month - 1
        tmp_rest_p = equal_installment[last_portion_index].rest_principal
        loan_info.rest_principal = tmp_rest_p
        loan_info.rest_months -= loanItem.interval_month
        # 获取上一次的间隔值
        month_interval += loanItem.interval_month


def get_loan_info(loan_type: LoanType):
    loan_info = LoanInfo()

    # 获取所有年化利率区间的总月数
    variant_months = [x.interval_month for x in loan_info.loan_items]

    month_count = sum(variant_months)

    assert month_count == loan_info.total_months, "月数必须一致"

    match loan_type:
        case LoanType.GJ:
            # 设置起始值
            # loan_info.need_all_detail = False
            loan_info.rest_principal = loan_info.gj_principal
            loan_info.rest_months = loan_info.total_months
            get_gj_or_sd_info(loan_info, loan_info.gj_loan_items)
        case LoanType.SD:
            # 设置起始值
            # loan_info.need_all_detail = True
            loan_info.rest_principal = loan_info.sd_principal
            loan_info.rest_months = loan_info.total_months
            get_gj_or_sd_info(loan_info, loan_info.loan_items)
        case LoanType.ALL:
            print("zh")


def start():
    get_loan_info(LoanType.GJ)
    # get_loan_info(LoanType.ALL)
    # get_loan_info(LoanType.SD)
