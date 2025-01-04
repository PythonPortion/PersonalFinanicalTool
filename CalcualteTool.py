from Models.M import EachMonthPayment
from Models.M import LoanType
from Models.M import LoanSubItem
from Models.M import LoanInfo
from Models.M import Result
from datetime import datetime
from dateutil.relativedelta import relativedelta


def fetch_result_detail(info: EachMonthPayment,
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
    :return: 返回每个月还款的值
    """

    month_index = info.month_index + month_interval
    new_date = loan_sub_item.init_date + relativedelta(months=month_index)
    date_str = new_date.strftime("%Y-%m-%d")
    formatted_month = f"{month_index:03}"

    result = Result(date_str,
                    formatted_month,
                    info.each_month_payment,
                    info.each_month_principal,
                    info.each_month_interest,
                    total_payment,
                    total_interest,
                    total_payment_principal, info.rest_principal)

    # print(result)
    return result


def calculate_equal_installment(principle, monthly_rate, months):
    """
    核心业务逻辑: 计算等额本息每月的还款信息
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
    """
    获取公积金或者商贷每个月的还款信息
    :param loan_info: 贷款信息
    :param loan_item_list: 每一个利率周期的信息
    :return: 每月还款额的实体
    """
    month_interval: int = 0
    total_payment: float = 0.0
    total_interest: float = 0.0
    total_payment_principal: float = 0.0
    result_list: list[Result] = []

    for index, loanItem in enumerate(loan_item_list):
        # 每个利率周期内的月度还款信息
        equal_installment = calculate_equal_installment(
            loan_info.rest_principal,
            loanItem.month_rate,
            loan_info.rest_months
        )
        # 输出详细信息
        for each_month_pay_info in equal_installment:
            # 每个利率周期内的 month_index 都是从 1 开始的
            # 因此,当month_index 大于 利率周期的月数,则需要退出，进入下一次利率周期
            if each_month_pay_info.month_index > loanItem.interval_month:
                break

            total_payment += each_month_pay_info.each_month_payment
            total_interest += each_month_pay_info.each_month_interest
            total_payment_principal += each_month_pay_info.each_month_principal

            result_item = fetch_result_detail(each_month_pay_info,
                                              loanItem,
                                              total_payment,
                                              total_interest,
                                              total_payment_principal,
                                              month_interval)
            result_list.append(result_item)

        last_portion_index = loanItem.interval_month - 1
        tmp_rest_p = equal_installment[last_portion_index].rest_principal
        loan_info.rest_principal = tmp_rest_p
        loan_info.rest_months -= loanItem.interval_month
        # 获取上一次的间隔值
        month_interval += loanItem.interval_month

    return result_list


def print_loan_result_detail(result_list: list[Result],
                             loan_sub_items: list[LoanSubItem],
                             need_print_all: bool = False):
    print(f"初始年化利息:\t{loan_sub_items[0].year_rate * 100:.3f}%")

    for index, result in enumerate(result_list):
        print(result)
        date_tmp = datetime.strptime(result.current_date, "%Y-%m-%d")

        # 默认输出两年后的信息
        if not need_print_all:
            today = datetime.today()
            two_years_later = today + relativedelta(years=2)
            if date_tmp > two_years_later:
                return

        for k_index, loan_sub_item in enumerate(loan_sub_items):
            if k_index > 0:
                target_end_tmp = loan_sub_item.end_date
                target_start_tmp = loan_sub_item.start_date
                if date_tmp == target_start_tmp:
                    print(f"--利率调整为:\t{loan_sub_item.year_rate * 100:.3f}%-----------------------------------\n")
                elif date_tmp == target_end_tmp and date_tmp != loan_sub_item.terminate_date:
                    print("--利率结束调整---------------------------------------\n")


def deal_with_gj(loan_info: LoanInfo, need_print: bool = True):
    # 设置起始值
    # loan_info.need_all_detail = False
    loan_info.rest_principal = loan_info.gj_principal
    loan_info.rest_months = loan_info.total_months
    result_list = get_gj_or_sd_info(loan_info, loan_info.gj_loan_items)
    if need_print:
        # print_loan_result_detail(result_list, loan_info.gj_loan_items, True)
        print_loan_result_detail(result_list,
                                 loan_info.gj_loan_items)
    return result_list


def deal_with_sd(loan_info: LoanInfo, need_print: bool = True):
    # 设置起始值
    loan_info.rest_principal = loan_info.sd_principal
    loan_info.rest_months = loan_info.total_months
    result_list = get_gj_or_sd_info(loan_info, loan_info.loan_items)
    if need_print:
        print_loan_result_detail(result_list, loan_info.loan_items)
    return result_list


def deal_with_combination(loan_info: LoanInfo):
    gj_result_list = deal_with_gj(loan_info, False)
    sd_result_list = deal_with_sd(loan_info, False)
    assert len(gj_result_list) == len(sd_result_list), "组合贷,其还款周期必须相等"
    for index, item in enumerate(gj_result_list):
        gj_result = item
        sd_result = sd_result_list[index]
        each_month_payment = gj_result.each_month_payment + sd_result.each_month_payment
        each_month_principal = gj_result.each_month_principal + sd_result.each_month_principal
        each_month_interest = gj_result.each_month_interest + sd_result.each_month_interest
        total_payment = gj_result.total_payment + sd_result.total_payment
        total_interest = gj_result.total_interest + sd_result.total_interest
        total_payment_principal = gj_result.total_payment_principal + sd_result.total_payment_principal
        rest_principle = gj_result.rest_principle + sd_result.rest_principle

        desc = (f"\t{item.current_date}," +
                f"第{item.current_month:^5}月: " +
                f"还款 {each_month_payment:.2f} ({gj_result.each_month_payment:.2f}+{sd_result.each_month_payment: .2f}), " +
                f"本金 {each_month_principal:.2f}, " +
                f"利息 {each_month_interest:.2f}, " +
                f"总还款 {total_payment:.2f}, " +
                f"总支付利息 {total_interest:.2f}, " +
                f"总支付本金 {total_payment_principal:.2f}, " +
                f"剩余本金 {rest_principle:.2f}")
        print(desc)

        if (index+1) % 12 == 0:
            print("****** " * 20)
            print("\n")

def get_loan_info(loan_type: LoanType):
    loan_info = LoanInfo()

    # 获取所有年化利率区间的总月数
    variant_months = [x.interval_month for x in loan_info.loan_items]

    month_count = sum(variant_months)

    assert month_count == loan_info.total_months, "月数必须一致"

    match loan_type:
        case LoanType.GJ:
            deal_with_gj(loan_info)
        case LoanType.SD:
            deal_with_sd(loan_info)
        case LoanType.ALL:
            deal_with_combination(loan_info)


def start():
    # get_loan_info(LoanType.GJ)
    get_loan_info(LoanType.ALL)
    # get_loan_info(LoanType.SD)
