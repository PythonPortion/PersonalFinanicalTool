from Models.M import LoanType, LoanPeriodicalItem, LoanInfo, Result
from datetime import datetime
from dateutil.relativedelta import relativedelta
from math import pow


def periodical_loan_items(loan_info: LoanInfo, loan_type: LoanType):
    """
    每个利率周期的信息
    :param loan_info:
    :param loan_type:
    :return:
    """
    loan_item_list: list[LoanPeriodicalItem] = []

    if loan_type == LoanType.SD:
        loan_item_list = loan_info.sd_loan_items
    elif loan_type == LoanType.GJ:
        loan_item_list = loan_info.gj_loan_items
    elif loan_type == LoanType.ALL:
        assert False, "如果是组合贷款,需要再外面单独计算在合并,不要直接调用此方法"
    return loan_item_list


def get_gj_or_sd_info(loan_info: LoanInfo, loan_type: LoanType):
    """
    获取公积金或者商贷每个月的还款信息
    :param loan_info: 贷款信息
    :param loan_type: 贷款类型
    :return: 每月还款额的实体
    """
    result_list: list[Result] = []
    loan_item_list = periodical_loan_items(loan_info, loan_type)

    rest_principal: float = 0

    if loan_type == LoanType.SD:
        rest_principal = loan_info.sd_principal
    elif loan_type == LoanType.GJ:
        rest_principal = loan_info.gj_principal

    rest_months = loan_info.total_months
    tmp_date = loan_info.init_date
    month_index = 0

    total_payment: float = 0
    total_interest: float = 0
    total_payment_principal: float = 0

    for index, loanItem in enumerate(loan_item_list):
        # 每个利率周期内的月度还款信息
        r, m = loanItem.month_rate, rest_months
        # 等额本息计算公式
        each_month_payment = (rest_principal * (r * pow(1 + r, m)) / (pow(1 + r, m) - 1))
        for interval_index in range(0, loanItem.interval_month):
            each_month_interest = rest_principal * r
            each_month_principal = each_month_payment - each_month_interest

            rest_months -= 1
            rest_principal -= each_month_principal

            month_index += 1
            tmp_date = tmp_date + relativedelta(months=1)

            total_payment += each_month_payment
            total_interest += each_month_interest
            total_payment_principal += each_month_principal

            result_info = Result(date=tmp_date,
                                 current_month=month_index,
                                 each_month_payment=each_month_payment,
                                 each_month_principal=each_month_principal,
                                 each_month_interest=each_month_interest,
                                 total_payment=total_payment,
                                 total_interest=total_interest,
                                 total_payment_principal=total_payment_principal,
                                 rest_principle=rest_principal)

            result_list.append(result_info)

    return result_list


def print_loan_result_detail(result_list: list[Result],
                             loan_info: LoanInfo,
                             loan_type: LoanType,
                             need_print_all: bool = False):
    loan_sub_items = periodical_loan_items(loan_info, loan_type)

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
                elif date_tmp == target_end_tmp and date_tmp != loan_info.terminate_date:
                    print("--利率结束调整---------------------------------------\n")


def deal_with_gj(loan_info: LoanInfo, need_print: bool = True):
    # 设置起始值
    result_list = get_gj_or_sd_info(loan_info, LoanType.GJ)
    if need_print:
        print_loan_result_detail(result_list, loan_info, LoanType.GJ, need_print)
    return result_list


def deal_with_sd(loan_info: LoanInfo, need_print: bool = True):
    result_list = get_gj_or_sd_info(loan_info, LoanType.SD)
    if need_print:
        print_loan_result_detail(result_list, loan_info, LoanType.SD, need_print)
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

        if (index + 1) % 12 == 0:
            print("****** " * 20)


def get_loan_info(loan_type: LoanType):
    loan_info = LoanInfo()

    # 获取所有年化利率区间的总月数
    variant_months = [x.interval_month for x in loan_info.sd_loan_items]

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
    get_loan_info(LoanType.SD)
    # get_loan_info(LoanType.ALL)
