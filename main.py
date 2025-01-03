from LoanTool import Equal_Installment


def house_mortgage():
    tool = Equal_Installment(1210000, 0.041, 30)
    tool.print_equal_installment_info()

def house_gj():
    tool = Equal_Installment(900000, 0.0285, 30)
    tool.print_gj_info()

def fast_loan():
    tool = Equal_Installment(200000, 0.029, 2)
    tool.print_fast_loan_installment_info()



if __name__ == '__main__':
    # house_mortgage()
    # fast_loan()
    house_gj()
    # tool.print_after_1_year()
    # tool.print_after_2_year()

    # t = LoanInfo(principal=1210000, loan=Loan(interest=0.041, years=30), changes=[])
    #
    #
    # print(t)


