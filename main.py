from CalcualteTool import calculate_equal_installment
from CalcualteTool import EachMonthPayment
from datetime import datetime
from dataclasses import dataclass
from typing import Optional
from enum import Enum


class LoanType(Enum):
    """
    相当于其他语言中的枚举类型
    贷款类型
    """
    GJ = 1  # 公积金
    SD = 2  # 商贷
    ALL = 3  # 组合


"""
@dataclass 的作用
@dataclass 可以自动生成以下方法，使代码更加简洁和易读：

__init__：自动生成初始化方法，省去了手动定义的繁琐。
__repr__：生成一个便于调试和打印的字符串表示方法。
__eq__：生成对象比较的逻辑（基于字段的值）。
其他方法：如 __hash__（可选，需满足某些条件）。
"""


@dataclass
class LoanSubItem:
    """
    这个类是用来保存每次利率调整的信息实体，包含：
        1. 年利率
        2. 起始时间
        3. 计算属性 获取 起始时间的  月度数量
        4. 获取 月利率
    """
    year_rate: float
    start_date: datetime
    end_date: datetime = datetime(2053, 5, 22)  # 默认结束日期

    """
    @property 的作用
        将方法转换为只读属性。
        控制属性的获取和设置逻辑。
        提高代码的封装性和安全性，支持动态计算属性值。
        通过 getter 和 setter 方法控制属性的访问和修改。
    """

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
    rest_months: Optional[int] = None  # 剩余月数,此处作为可选属性，在计算的时候设置其真实值
    sd_principal: float = (121 * 10000)  # 起始本金
    rest_principal: Optional[float] = None  # 剩余本金

    gj_principal: float = (90 * 10000)
    gj_rest_principal: Optional[float] = None  # 剩余本金

    total_months: int = 360

    @property
    def loan_items(self):
        items = []
        # 2023年 利率为 4.3, 贷款是 减掉 20个几点
        sub_item_01 = LoanSubItem(year_rate=(4.1 * 0.01),
                                  start_date=datetime(2023, 5, 22),
                                  end_date=datetime(2024, 5, 22)
                                  )
        items.append(sub_item_01)
        # 2024年 利率为 3.95, 贷款是 减掉 20个几点
        sub_item_02 = LoanSubItem(year_rate=(3.75 * 0.01),
                                  start_date=datetime(2024, 5, 22),
                                  end_date=datetime(2024, 10, 22)
                                  )
        items.append(sub_item_02)

        # 2024年 7 月 利率为 3.85, 贷款是 减掉 20个几点
        # sub_item_03 = LoanSubItem(year_rate=(3.65 * 0.01),
        # 不知道啥原因，如果按照3.65来计算，2024年11月22日应该还款是5543.91，
        # 但实际还款是5550.51，反推出来年化为 3.66
        sub_item_03 = LoanSubItem(year_rate=(3.659999 * 0.01),
                                  start_date=datetime(2024, 10, 22),
                                  end_date=datetime(2024, 11, 22)
                                  )
        items.append(sub_item_03)

        # 2024年 10 月 利率为 3.6, 贷款是 减掉 30个几点
        sub_item_04 = LoanSubItem(year_rate=(3.3 * 0.01),
                                  start_date=datetime(2024, 11, 22))
        items.append(sub_item_04)

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


def print_detail(info: EachMonthPayment):
    print(
        f"\t第{info.month_index:^5}月: "
        f"还款 {info.each_month_payment:.2f}, "
        f"本金 {info.each_month_principal:.2f}, "
        f"利息 {info.each_month_interest:.2f}, "
        f"总还款 {info.has_payment_value:.2f}, "
        f"总支付利息 {info.has_pay_interest:.2f}, "
        f"剩余本金 {info.rest_principal:.2f}")


def get_loan_info(loan_type: LoanType):

    loan_info = LoanInfo()

    variant_months = [x.interval_month for x in loan_info.loan_items]

    month_count = sum(variant_months)

    assert month_count == loan_info.total_months, "月数必须一致"

    match loan_type:
        case LoanType.GJ:
            print("gjj")
            # 设置起始值
            loan_info.rest_principal = loan_info.gj_principal
            loan_info.rest_months = loan_info.total_months

            for loanItem in loan_info.gj_loan_items:
                equal_installment = calculate_equal_installment(loan_info.rest_principal,
                                                                loanItem.month_rate,
                                                                loan_info.rest_months)
                for each_month_pay_info in equal_installment:
                    if each_month_pay_info.month_index > loanItem.interval_month:
                        print("------------------------------------" * 2)
                        break
                    print_detail(each_month_pay_info)

                last_portion_index = loanItem.interval_month - 1
                tmp_rest_p = equal_installment[last_portion_index].rest_principal
                loan_info.rest_principal = tmp_rest_p
                loan_info.rest_months -= loanItem.interval_month
        case LoanType.SD:
            print("商贷")
            # 设置起始值
            loan_info.rest_principal = loan_info.sd_principal
            loan_info.rest_months = loan_info.total_months

            for loanItem in loan_info.loan_items:
                equal_installment = calculate_equal_installment(loan_info.rest_principal,
                                                                loanItem.month_rate,
                                                                loan_info.rest_months)
                for each_month_pay_info in equal_installment:
                    if each_month_pay_info.month_index > loanItem.interval_month:
                        print("------------------------------------" * 2)
                        break
                    print_detail(each_month_pay_info)

                last_portion_index = loanItem.interval_month - 1
                tmp_rest_p = equal_installment[last_portion_index].rest_principal
                loan_info.rest_principal = tmp_rest_p
                loan_info.rest_months -= loanItem.interval_month
        case LoanType.ALL:
            print("zh")


if __name__ == '__main__':
    # get_loan_info(LoanType.GJ)
    # get_loan_info(LoanType.ALL)
    get_loan_info(LoanType.SD)
