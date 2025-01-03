from CalcualteTool import calculate_equal_installment
from datetime import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class LoanSubItem:
    year_rate: float
    start_date: datetime
    end_date: datetime = datetime(2053, 5, 22)  # 默认结束日期

    @property
    def interval_month(self):
        """
        当前利率下的总月数
        :return: Int,总月数
        """
        months = (self.end_date.year - self.start_date.year) * 12 + (self.end_date.month - self.start_date.month)
        return months

    @property
    def month_rate(self):
        """
        月利率
        :return: 月利率
        """
        return self.year_rate / 12.0


@dataclass
class LoanInfo:
    rest_principal: Optional[float] = None  # 剩余本金
    rest_months: Optional[int] = None  # 剩余月数
    principal: float = (121 * 10000)  # 起始本金

    gj_principal: float = (90 * 10000)
    gj_rest_principal: Optional[float] = None  # 剩余本金

    total_months: int = 360

    @property
    def loan_items(self):
        items = []
        sub_item_01 = LoanSubItem(year_rate=(4.1 * 0.01),
                                  start_date=datetime(2023, 5, 22),
                                  end_date=datetime(2024, 5, 22)
                                  )
        items.append(sub_item_01)

        sub_item_02 = LoanSubItem(year_rate=(3.75 * 0.01),
                                  start_date=datetime(2024, 5, 22),
                                  end_date=datetime(2024, 10, 22)
                                  )
        items.append(sub_item_02)

        sub_item_03 = LoanSubItem(year_rate=(3.3 * 0.01),
                                  start_date=datetime(2024, 10, 22))
        items.append(sub_item_03)

        return items

    @property
    def gj_loan_items(self):
        items = []
        sub_item_01 = LoanSubItem(year_rate=(3.1 * 0.01),
                                  start_date=datetime(2023, 5, 22),
                                  end_date=datetime(2024, 12, 22)
                                  )
        items.append(sub_item_01)

        sub_item_02 = LoanSubItem(year_rate=(2.85 * 0.01),
                                  start_date=datetime(2024, 12, 22),
                                  )
        items.append(sub_item_02)

        return items


def sd_tt():
    loan_info = LoanInfo()

    variant_months = [x.interval_month for x in loan_info.loan_items]

    month_count = sum(variant_months)

    assert month_count == loan_info.total_months, "月数必须一致"

    # 设置起始值
    loan_info.rest_principal = loan_info.principal
    loan_info.rest_months = loan_info.total_months

    for loanItem in loan_info.loan_items:
        equal_installment = calculate_equal_installment(loan_info.rest_principal,
                                                        loanItem.month_rate,
                                                        loan_info.rest_months)
        for info in equal_installment:
            if info.month_index > loanItem.interval_month:
                print("------------------------------------" * 2)
                break
            print(
                f"\t第{info.month_index:^5}月: "
                f"还款 {info.each_month_payment:.2f}, "
                f"本金 {info.each_month_principal:.2f}, "
                f"利息 {info.each_month_interest:.2f}, "
                f"总还款 {info.has_payment_value:.2f}, "
                f"总支付利息 {info.has_pay_interest:.2f}, "
                f"剩余本金 {info.rest_principal:.2f}")

        last_portion_index = loanItem.interval_month - 1
        tmp_rest_p = equal_installment[last_portion_index].rest_principal
        loan_info.rest_principal = tmp_rest_p
        loan_info.rest_months -= loanItem.interval_month


def gj_tt():
    gj_loan_info = LoanInfo()

    variant_months = [x.interval_month for x in gj_loan_info.gj_loan_items]

    month_count = sum(variant_months)

    assert month_count == gj_loan_info.total_months, "月数必须一致"

    # 设置起始值
    gj_loan_info.rest_principal = gj_loan_info.gj_principal
    gj_loan_info.rest_months = gj_loan_info.total_months

    for loanItem in gj_loan_info.gj_loan_items:
        equal_installment = calculate_equal_installment(gj_loan_info.rest_principal,
                                                        loanItem.month_rate,
                                                        gj_loan_info.rest_months)
        for info in equal_installment:
            if info.month_index > loanItem.interval_month:
                print("------------------------------------" * 2)
                break
            print(
                f"\t第{info.month_index:^5}月: "
                f"还款 {info.each_month_payment:.2f}, "
                f"本金 {info.each_month_principal:.2f}, "
                f"利息 {info.each_month_interest:.2f}, "
                f"总还款 {info.has_payment_value:.2f}, "
                f"总支付利息 {info.has_pay_interest:.2f}, "
                f"剩余本金 {info.rest_principal:.2f}")

        last_portion_index = loanItem.interval_month - 1
        tmp_rest_p = equal_installment[last_portion_index].rest_principal
        gj_loan_info.rest_principal = tmp_rest_p
        gj_loan_info.rest_months -= loanItem.interval_month


if __name__ == '__main__':
    sd_tt()
    gj_tt()
