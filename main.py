import ExchangeRates

def main():
    flag = 0
    while(flag == 0):
        N = input("Please, choose an option: \n1 - Import official exchange rates on selected date from CBR.RU\n0 - exit\n")
        if N == '1':
            ExchangeRates.check_date()
        elif N == '0':
            flag = 1
            print("Bye!")
        else:
            print("Wrong input! Try again\n")

if __name__ == "__main__":
    main()