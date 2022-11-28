import psycopg2
from os import system, name

connect = psycopg2.connect(host='localhost',
                        user='postgres',
                        password='2002',
                        database='ProjectDDL')
cur=connect.cursor()

def customerIDs():
    #this function returns an array of all existing customer IDs
    arr = []
    cur.execute("SELECT CID FROM customer;")
    rec = cur.fetchone()
    for row in rec:
        arr.append(row)
    return arr

def showCustomerInformation():
    #This function returns information about the customers
    #Can be accessed by both teller and manager
    table = []
    cur.execute("SELECT * FROM CUSTOMER;")
    rec = cur.fetchone()
    for row in rec:
        table.append(row)
    return table

def showTellerInformation():
    #This function returns information about the Tellers
    #can be accessed by managers only
    table = []
    cur.execute("SELECT * FROM Teller;")
    rec = cur.fetchone()
    for row in rec:
        table.append(row)
    return table


def createAccount():
    #This function allows customers/managers to create an account
    return

def deleteAccount():
    #This function allows customers/managers to delete accounts
    return
def withdraw():
    # This function allows customers/managers/tellers to withdraw amounts
    return

def deposit():
    #This function allows tellers/customers/managers to deposit amounts
    return

def transfer():
    # This function allows customers/managers/tellers to transfer amounts
    return

def externalTransfer():
    # This function allows customers/managers/tellers to transfer amounts to an account of another bank
    return

def showStatement():
    '''the statement of a (past) month of an account should list all the transactions for this account d
    during this month order by time.
    Furthermore, the account balance after each transaction should be shown.
     Finally, you should show the final account balance for the account at the end of the month.
    '''
    return
def showPendingTransactions():
    return

#the following functions can only be executed by managers

def addInterest():
    return

def addOverDraftFees():
    return

def addAccountFees():
    return

def showAnalytics():
    return

def main():
    while True:
        print('''
                *** Welcome To HTM Bank ***

                    1. Customer Access
                    2. Employee Access
                    3. Exit                            ''')

        choice = input("Enter choice: ")
        if (choice == '1'):
            print('''
                Welcome Please choose from the following:

                    1. Customer log-in page (for existing customers only)
                    2. Get Started/ Sign-up (for non existing customers only)

                You can return to main menu by pressing any key
                    ''')
            choice1 = input()
            if choice1 == '1':
                cid = input('Please enter your CID: ')
                if cid in customerIDs():
                    cur.execute("SELECT name FROM customer WHERE customer.cid = '{}';".format(cid))
                    rec = cur.fetchone()
                    print('Welcome ' + rec[0] + '\nHow can we help you?')
                    print('''
                                                1. Create new Account
                                                2. Withdraw Amount
                                                3. Deposit Amount
                                                4. Transfer Amount
                                                5. External Transfer
                                                6. Delete Account
                                                7. Show Statement of Month
                                                8. Show pending Transactions
                                                9. Return to main

                                                ''')
                    choix = input()
                    if choix == 1:
                        createAccount()

                    elif choix == 2:
                        withdraw()

                    elif choix == 3:
                        deposit()

                    elif choix == 4:
                        transfer()

                    elif choix == 5:
                        externalTransfer()

                    elif choix == 6:
                        deleteAccount()

                    elif choix == 7:
                        showStatement()

                    elif choix == 8:
                        showPendingTransactions()

                    elif choix == 9:
                        main()

                else:
                    print('Invalid CID.. Returning to main')
                    main()

            elif choice1 == '2':
                print('Sign up')
            else:
                main()


        elif (choice == '2'):
            print('''
                    Welcome..
                    1. Teller Access
                    2. Manager Access
                    ''')
            choice1 = input('Please enter access')
            eid = input('Enter your SSN: ')

            if choice1 =='1':
                print('Welcome Teller')
                print('''
                        1. Show Customer information
                        2. Withdraw amount
                        3. Deposit amount
                        4. Transfer amount
                        5. External Transfer ''')
                choice2 = input()
                if choice2 == 1:
                    showCustomerInformation()

                elif choice2 == 2:
                    withdraw()

                elif choice2 == 3:
                    deposit()

                elif choice2 == 4:
                    transfer()

                elif choice2 == 5:
                    externalTransfer()

            elif choice1 == '2':
                print('Welcome Manager')
                print('''
                                    1. Show Customer information
                                    2. Show Teller Information
                                    3. Withdraw amount
                                    4. Deposit amount
                                    5. Transfer amount
                                    6. External Transfer 
                                    7. Add Interest
                                    8. Add Overdraft fees
                                    9. Add Account fees
                                    10. Show Analytics''')

                choice2 = input()
                if choice2 == 1:
                    showCustomerInformation()

                elif choice2 == 2:
                    showTellerInformation()

                elif choice2 == 3:
                    withdraw()

                elif choice2 == 4:
                    deposit()

                elif choice2 == 5:
                    transfer()

                elif choice2 == 6:
                    externalTransfer()

                elif choice2 == 7:
                    addInterest()

                elif choice2 == 8:
                    addOverDraftFees()

                elif choice2 == 9:
                    addAccountFees()

                elif choice2 == 10:
                    showAnalytics()

                else:
                    print('Invalid Choice.. Returning to main')
                    main()

        elif (choice == '3'):
            print('Goodbye...Hope to see you soon!')
            exit()

        else:
            print('Invalid Choice')
            main()


main()



