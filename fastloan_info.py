from LoanTool import Equal_Installment

"""
Scheme
    1. 10w one year save, annual rate is about 3.5%
    2. each_monthly_pay = 8587.4  2%
    
    
"""
def fast_loan():
    tool = Equal_Installment(200000, 0.029, 2)
    tool.print_fast_loan_installment_info()
    """
    after a year == total interest is 4496.93
    
    one year stable interest is 100000 * 4% = 4000
    """

def after_180_day():
    print("----"*30)
    # 6个月到期项目，需要预备7个月的存款
    each_pay = 8587.4
    invest_180_amount = (100000 - each_pay * 7)
    print("each pay:", each_pay)  # 8587.4
    print("invest_180_amount:", invest_180_amount)  # 39888.20

    # assume annual_rate == 3.5%
    monthly_rate = 0.035 / 12
    p = invest_180_amount * monthly_rate * 6
    print(p)  # 698.0435000000001

    ###
    p2 = 698 + 4000

    ###

def detail():
    total_p = 100000
    each_pay = 8587.4

    """
    买一笔 1个月
    买一笔 2个月
    买一笔 3个月
    买一笔 4个月
    买一笔 5个月
    买一笔 6个月
    买一笔 7个月
    买一笔 8个月
    买一笔 9个月
    买一笔 10个月
    买一笔 11个月
    买一笔 12个月
    """
    # 首先预留4个月的活期的
    remain_4 = each_pay * 4

    mon_r = 0.017 / 12
    huoqi_01 = mon_r * each_pay * 4 * 1
    print("huoqi_01 == ", huoqi_01)
    huoqi_02 = mon_r * each_pay * 3 * 1
    print("huoqi_02 == ", huoqi_02)
    huoqi_03 = mon_r * each_pay * 2 * 1
    print("huoqi_03 == ", huoqi_03)
    huoqi_04 = mon_r * each_pay * 1 * 1
    print("huoqi_04 == ", huoqi_04)



    rest_p4 = total_p - remain_4
    print("rest_p4 == ", rest_p4)





if __name__ == '__main__':
    fast_loan()
    # after_180_day()

    # detail()
