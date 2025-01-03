from CalcualteTool import calculate_equal_installment
from dataclasses import dataclass


@dataclass
class MultiRate:
    annual_rate: float
    year_index: int


class LoanTool:
    def __init__(self, principle: float, annual_rate: float, year_interval: int):
        self.principle = principle
        self.annual_rate = annual_rate
        self.year_interval = year_interval
        self._rest_principle = principle
        self._rest_month = self.year_interval * 12

    def calculate_interest_only(self):
        pass


class Equal_Installment(LoanTool):
    # 假设全部是 0.041 的利率
    # 已还款总额:2104812.10,
    # 已还款本金:1210000.00,
    # 已还款利息:894812.10,
    # 剩余本金:-0.00

    """
    已还款总额:70160.40,已还款本金:20941.01,已还款利息:49219.39,剩余本金:1189058.99
    """

    def _print_info(self, rate_list=None):
        if rate_list is None:
            rate_list = [MultiRate(annual_rate=0.041, year_index=1)]

        has_repayment_amount = 0.0
        has_repayment_principle = 0.0
        has_repayment_interest = 0.0
        has_repayment_months = 0

        for rate_index, rate_entity in enumerate(rate_list):
            monthly_rate = rate_entity.annual_rate / 12.0
            equal_installment = calculate_equal_installment(self._rest_principle,
                                                            monthly_rate,
                                                            self._rest_month)

            print(f"rest_principle--{self._rest_principle:->30.2f}")
            print(f"monthly_rate--{monthly_rate:->30f}")
            print(f"_rest_month--{self._rest_month:->30d}")

            for month_index, each_month_payment, each_month_principal, each_month_interest in equal_installment:
                has_repayment_amount += each_month_payment
                has_repayment_principle += each_month_principal
                has_repayment_interest += each_month_interest
                has_repayment_months += 1
                self._rest_month -= 1
                self._rest_principle -= each_month_principal

                print(
                    f"\t第{has_repayment_months:^5}月: "
                    f"还款 {each_month_payment:.2f}, "
                    f"本金 {each_month_principal:.2f}, "
                    f"利息 {each_month_interest:.2f}")

                if has_repayment_months == rate_entity.year_index * 12 and rate_index != (len(rate_list) - 1):
                    print("---------rate_index------", rate_index)
                    break

            print(f"已还款总额:{has_repayment_amount:.2f},"
                  f"已还款本金:{has_repayment_principle:.2f},"
                  f"已还款利息:{has_repayment_interest:.2f},"
                  f"剩余本金:{self._rest_principle:.2f}")



    def print_equal_installment_info(self):
        rate_list = [MultiRate(annual_rate=self.annual_rate, year_index=1),
                     MultiRate(annual_rate=0.0375, year_index=2),
                     MultiRate(annual_rate=0.033, year_index=3)
                     ]
        self._print_info(rate_list)


    def print_fast_loan_installment_info(self):
        rate_list = [MultiRate(annual_rate=self.annual_rate, year_index=1),
                     MultiRate(annual_rate=self.annual_rate, year_index=2)
                     ]
        self._print_info(rate_list)

    def print_gj_info(self):
        rate_list = [MultiRate(annual_rate=self.annual_rate, year_index=1),
                     # MultiRate(annual_rate=self.annual_rate, year_index=2),
                     # MultiRate(annual_rate=0.0285, year_index=3)
                     ]
        self._print_info(rate_list)

