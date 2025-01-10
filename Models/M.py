from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from typing import Optional


def interval_months(start: datetime, end: datetime):
    """
    :param start: start date
    :param end: end date
    :return: the number of months between start and end
    """
    months = (end.year - start.year) * 12 + (end.month - start.month)
    return months


"""
@dataclass 的作用
@dataclass 可以自动生成以下方法，使代码更加简洁和易读：

__init__：自动生成初始化方法，省去了手动定义的繁琐。
__repr__：生成一个便于调试和打印的字符串表示方法。
__eq__：生成对象比较的逻辑（基于字段的值）。
其他方法：如 __hash__（可选，需满足某些条件）。
"""


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


class LoanType(Enum):
    """
    相当于其他语言中的枚举类型
    贷款类型
    """
    GJ = 1  # 公积金
    SD = 2  # 商贷
    ALL = 3  # 组合


@dataclass
class LoanPeriodicalItem:
    """
    这个类是用来保存每次利率调整的信息实体，包含：
        1. 年利率
        2. 起始时间
        3. 计算属性 获取 起始时间的  月度数量
        4. 获取 月利率
    """

    """
    注意带有默认值的属性,需要放在前面。
    """
    year_rate: float  # 年利率
    start_date: datetime
    end_date: datetime = datetime(2053, 5, 22)  # 默认结束日期,如果遇到利率调整，则需要更改这个值

    """
    @property 的作用
        将方法转换为只读属性。
        控制属性的获取和设置逻辑。
        提高代码的封装性和安全性，支持动态计算属性值。
        通过 getter 和 setter 方法控制属性的访问和修改。
    """

    @property
    def interval_month(self):
        return interval_months(self.start_date, self.end_date)

    @property
    def month_rate(self):
        """
        月利率
        :return: 月利率
        """
        return self.year_rate / 12.0


@dataclass
class LoanInfo:
    """
    贷款信息实体
    """
    rest_months: Optional[int] = None  # 剩余月数,此处作为可选属性，在计算的时候设置其真实值
    rest_principal: Optional[float] = None  # 剩余月数,此处作为可选属性，在计算的时候设置其真实值

    sd_principal: float = (121 * 10000)  # 起始本金
    gj_principal: float = (90 * 10000)  # 起始本金

    init_date: datetime = datetime(2023, 5, 22)  # 合同开始时间,不要进行修改！！！
    terminate_date: datetime = datetime(2053, 5, 22)  # 合同结束时间,不要进行修改！！！

    @property
    def total_months(self):
        return interval_months(self.init_date, self.terminate_date)

    @property
    def sd_loan_items(self):
        items = []
        # 2023年 利率为 4.3, 贷款是 减掉 20个几点
        sub_item_01 = LoanPeriodicalItem(year_rate=(4.1 * 0.01),
                                         start_date=datetime(2023, 5, 22),
                                         end_date=datetime(2024, 5, 22)
                                         )
        items.append(sub_item_01)
        # 2024年 利率为 3.95, 贷款是 减掉 20个几点
        sub_item_02 = LoanPeriodicalItem(year_rate=(3.75 * 0.01),
                                         start_date=datetime(2024, 5, 22),
                                         end_date=datetime(2024, 10, 22)
                                         )
        items.append(sub_item_02)

        # 2024年 7 月 利率为 3.85, 贷款是 减掉 20个几点
        # sub_item_03 = LoanSubItem(year_rate=(3.65 * 0.01),
        # 不知道啥原因，如果按照3.65来计算，2024年11月22日应该还款是5543.91，
        # 但实际还款是5550.51，反推出来年化为 3.66
        sub_item_03 = LoanPeriodicalItem(year_rate=(3.659999 * 0.01),
                                         start_date=datetime(2024, 10, 22),
                                         end_date=datetime(2024, 11, 22)
                                         )
        items.append(sub_item_03)

        # 2024年 10 月 利率为 3.6, 贷款是 减掉 30个几点
        sub_item_04 = LoanPeriodicalItem(year_rate=(3.3 * 0.01),
                                         start_date=datetime(2024, 11, 22))
        items.append(sub_item_04)

        return items

    @property
    def gj_loan_items(self):
        items = []
        sub_item_01 = LoanPeriodicalItem(year_rate=(3.1 * 0.01),
                                         start_date=datetime(2023, 5, 22),
                                         end_date=datetime(2024, 12, 22)
                                         )
        items.append(sub_item_01)

        sub_item_02 = LoanPeriodicalItem(year_rate=(2.85 * 0.01),
                                         start_date=datetime(2024, 12, 22),
                                         )
        items.append(sub_item_02)

        return items


def get_result_detail(current_date,
                      current_month,
                      each_month_payment,
                      each_month_principal,
                      each_month_interest,
                      total_payment,
                      total_interest,
                      total_payment_principal,
                      rest_principle):
    desc = (f"\t{current_date}," +
            f"第{current_month:^5}月: " +
            f"还款 {each_month_payment:.2f}, " +
            f"本金 {each_month_principal:.2f}, " +
            f"利息 {each_month_interest:.2f}, " +
            f"总还款 {total_payment:.2f}, " +
            f"总支付利息 {total_interest:.2f}, " +
            f"总支付本金 {total_payment_principal:.2f}, " +
            f"剩余本金 {rest_principle:.2f}")
    return desc


@dataclass
class Result:
    date: datetime
    current_date: str
    current_month: str
    each_month_payment: float

    each_month_principal: float
    each_month_interest: float
    total_payment: float

    total_interest: float
    total_payment_principal: float
    rest_principle: float

    def __str__(self):
        desc = get_result_detail(self.current_date,
                                 self.current_month,
                                 self.each_month_payment,
                                 self.each_month_principal,
                                 self.each_month_interest,
                                 self.total_payment,
                                 self.total_interest,
                                 self.total_payment_principal,
                                 self.rest_principle)
        return desc
