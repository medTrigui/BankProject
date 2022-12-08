import psycopg2
from datetime import date
from os import system, name
import random

connect = psycopg2.connect(host='localhost',
                        user='postgres',
                        password='Tonsofun02!',
                        database='BankProject2')

cur=connect.cursor()
#clear screen function
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        system('clear')

def customerIDs():
    #this function returns an array of all existing customer IDs
    arr = []

    cur.execute("SELECT CID FROM customer;")
    rec = cur.fetchall()

    for row in rec:
        arr.append(row[0])
    return arr

#task for Mohamed
def showCustomerInformation():
    #This function returns information about the customers
    #Can be accessed by both teller and manager
    table = []
    cur.execute("SELECT * FROM CUSTOMER;")
    rec = cur.fetchone()
    for row in rec:
        table.append(row)
    print(table)
    return table

#Task for Timmy
def showTellerInformation():
    #This function returns information about the Tellers
    #can be accessed by managers only
    table = []
    cur.execute("SELECT * FROM Teller;")
    rec = cur.fetchone()
    for row in rec:
        table.append(row)
    print(table)
    return table


#Task for Mohamed
def checkUniqueAccount():
    tab = []
    cur.execute("SELECT accid FROM account;")
    rec = cur.fetchall()
    for row in rec:
        tab.append(row[0])
    return tab
checkUniqueAccount()
def createAccountExistingCust(cid):
    #This function allows existing customers to create new accounts

    ans = input('''What type of account would you like to open? 
                    1. Savings Account
                    2. Checking Account \n''')

    acc = random.randrange(1000000000, 9999999999)
    while acc in checkUniqueAccount():
        acc = random.randrange(1000000000, 9999999999)
    try:
        acc_id = acc
        if ans == '1':
            acc_type = 'Savings'
        elif ans == '2':
            acc_type = 'Checking'
        else:
            print('Invalid Choice.. Try again')
            createAccountExistingCust(id)
        balance = 0
        cur.execute("Insert into account values ({}, {} ,'{}');".format(acc_id, balance, acc_type))
        connect.commit()
        cur.execute("Insert into owns values ({}, {});".format(acc_id, cid))
        connect.commit()
        cur.execute("SELECT name FROM customer WHERE customer.cid = '{}';".format(cid))
        a = cur.fetchone()
        print("New "+str(acc_type)+" account for Customer: "+str(a[0])+" ; ID = "+str(cid)+ " successfully created!")
        print("Your Account_ID is: "+ str(acc) + " \n   Please remember this.")

    except(Exception, psycopg2.DatabaseError) as e:
        print(e)


#Task for Mohamed
def checkUniqueCustID():
    tab0 = []
    cur.execute("SELECT CID FROM customer;")
    rec = cur.fetchall()
    for row in rec:
        tab0.append(row[0])
    return tab0
def showBranhes():
    text = ''
    cur.execute("SELECT * FROM branch;")
    rec = cur.fetchall()
    n = 0
    for row in rec:
        n = n+1
        separator = ', '
        text = str(7-n) +". " +  separator.join(row) + "\n" + text
    print(text)
    return text

def checkExistingBranch():
    tab = []
    cur.execute("SELECT bid FROM branch;")
    rec = cur.fetchall()
    for row in rec:
        tab.append(row[0])
    return tab

def createAccountNewCust():
    #This function allows customers/managers to create an account
    #Ask for home branch
    i = input('''Please enter a personal  10-digit Customer ID that you can remember.
                    Your Customer ID should include characters only : ''')

    while i in checkUniqueCustID():
        print("Error.. The ID you chose already exists. ")
        i = input("Please choose another CID: ")
    name = input("Please enter your full name: ")
    state = input("Please enter your state (this should only be a 2-character string): ")
    while len(state) != 2:
        state = input("Error. Please enter 2 characters for the state: ")
    city = input("Please enter your city: ")
    street = input("Please enter your street: ")
    zip = input("Please enter your zip_code: ")
    clear()
    print('Please chose a Branch from the following (Please enter the 3-digit branch ID): +\n ')
    showBranhes()
    branch = input()
    while branch not in checkExistingBranch():
        clear()
        print("The branch you entered does not exist. Try again: \n")
        print('Please chose a Branch from the following (Please enter the 3-digit branch ID): \n')
        showBranhes()
        branch = input()
    cur.execute("Insert into customer values ('{}', '{}' , '{}', '{}', '{}', '{}', '{}');".format(name, i, state, city, street, zip, branch))
    connect.commit()

    clear()
    ans = input('''What type of account would you like to open today ? 
                        1. Savings Account
                        2. Checking Account \n''')

    acc = random.randrange(1000000000, 9999999999)
    while acc in checkUniqueAccount():
        acc = random.randrange(1000000000, 9999999999)
    while ans not in ['1','2']:
        ans = input('''Invalid choice.. Try again:
                        What type of account would you like to open today ? 
                        
                            1. Savings Account
                            2. Checking Account \n''')
    try:
        acc_id = acc
        if ans == '1':
            acc_type = 'Savings'
        elif ans == '2':
            acc_type = 'Checking'
        balance = 0
        cur.execute("Insert into account values ({}, {} ,'{}');".format(acc_id, balance, acc_type))
        connect.commit()
        cur.execute("Insert into owns values ({}, {});".format(acc_id, i))
        connect.commit()
        cur.execute("SELECT name FROM customer WHERE customer.cid = '{}';".format(i))
        a = cur.fetchone()
        clear()
        print("New Savings account for Customer: " + str(a[0]) + " ; ID = " + str(i) + " successfully created!")
        print("Your Account_ID is: " + str(acc) + " \n   Please remember this.")
    except(Exception, psycopg2.DatabaseError) as e:
        print(e)

#Task for Mohamed
def deleteAccount():
    #This function allows customers/managers to delete accounts
    print("Are you sure you would like to remove your account? ")
    ans = input()
    if ans.lower() == 'yes':
        id = input("Please enter your CID: ")
        acc = input("Please enter the accout ID that you would like to remove: ")
        cur.execute("Delete from account  where account.accid = '{}';".format(acc))
        connect.commit()
        cur.execute("Delete from owns  where owns.account = '{}';".format(acc))
        connect.commit()

        clear()
        print("Account deleted successfully!")
        tab = []
        cur.execute("SELECT ownedby FROM owns;")
        rec = cur.fetchall()
        for row in rec:
            tab.append(row[0])
        if id not in tab:
            print('''You currently do not have any account open at HTM Bank.
                    Would you like to open a new account? ''')
            ans1 = input()
            while ans1 not in ['yes','no']:
                ans1 = input("Invalid choice. Please try again.  Would you like to open a new account?")
            if ans1.lower() == 'yes':
                createAccountNewCust()
            elif ans1.lower() == 'no':
                print("In this case, we are sorry to inform you that your customer record will be deleted from our database. You can alwys sign-up again as a new customer. See you soon!")
                cur.execute("Delete from Customer  where Customer.cid = '{}';".format(id))
                connect.commit()
                main()


    elif ans.lower() == 'no':
        print("No problem.. Returning to main")
        main()
    else:
        print("Invalid answer.. Try again.")
        deleteAccount()
def check_account(cid,accids):
    cur.execute("SELECT ownedby FROM owns WHERE owns.account = '{}';".format(accids))
    check = cur.fetchall()
    arr = []
    for row in check:
        arr.append(row[0])
    if cid not in arr:
        return False
    return True
def check_manager(ssn):
    cur.execute("SELECT ssn FROM manager")
    check = cur.fetchall()
    arr = []
    for row in check:
        arr.append(row[0])
    if ssn not in arr:
        return False
    return True









#Task for Timmy
def withdraw(cid, man):
    # This function allows customers/managers/tellers to withdraw amounts
    accids = ""
    if man != 1:
        accids = input('Enter Account ID: ')
        if check_account(cid, accids) != True:
            print('Not your account')
            return
    cur.execute("SELECT balance FROM account WHERE account.accid = '{}';".format(accids))
    amt = cur.fetchone()
    take = input('Enter withdraw amount')
    bal = float(amt[0])-float(take)
    cur.execute("UPDATE account SET balance = {} WHERE account.accid = '{}';".format(bal, accids))
    connect.commit()
    desc = input('Type withdraw description: ')
    take = -1 * float(take)
    cur.execute("INSERT into transactions values ('{}', {}, '{}', {}, {}, '{}');".format(desc, take, "withdraw", random.randint(100000000000, 999999999999), accids, date.today()))
    connect.commit()
    print('Withdraw Complete')

#Task for Timmy

def deposit(cid, man):
    #This function allows tellers/customers/managers to deposit amounts
    accids = ""
    if man != 1:
        accids = input('Enter Account ID: ')
        if check_account(cid, accids) != True:
            print('Not your account')
            return
    cur.execute("SELECT balance FROM account WHERE account.accid = '{}';".format(accids))
    amt = cur.fetchone()
    dep = input('Enter deposit amount')
    bal = float(amt[0]) + float(dep)
    cur.execute("UPDATE account SET balance = {} WHERE account.accid = '{}';".format(bal, accids))
    connect.commit()
    desc = input('Type deposit description: ')
    dep = float(dep)
    cur.execute("INSERT into transactions values ('{}', {}, '{}', {}, {}, '{}');".format(desc, dep, "deposit", random.randint(100000000000, 999999999999), accids, date.today()))
    connect.commit()
    print('Withdraw Complete')
    print('Deposit Complete')


    return


#Task for Timmy      I'll have to check once I get the database connected but I don't think we need the external
# transfer function. I think one will be fine because knowing the account ID is all that we need, regardless of the branch.

def transfer(cid, man):
    # This function allows customers/managers/tellers to transfer amounts
    initial = input('Enter account number from the account you wish to transfer from: ')
    if man != 1:
        if check_account(cid, initial) != True:
            print('Not your account')
            return
    if man == 0:
        cur.execute("SELECT homebranch FROM customer WHERE customer.cid = '{}';".format(cid))
        branch1 = cur.fetchone()
        destination = input('Enter account number that you would like to transfer funds into: ')
        cur.execute("SELECT ownedby FROM owns WHERE owns.account = '{}';".format(destination))
        num = cur.fetchone()
        cur.execute("SELECT homebranch FROM customer WHERE customer.cid = '{}';".format(num[0]))
        branch2 = cur.fetchone()
    else:
        cur.execute("SELECT homebranch FROM customer WHERE customer.cid = (SELECT ownedby FROM owns WHERE owns.account "
                    "= '{}');".format(initial))
        branch1 = cur.fetchone()
        destination = input('Enter account number that you would like to transfer funds into: ')
        cur.execute("SELECT ownedby FROM owns WHERE owns.account = '{}';".format(destination))
        num = cur.fetchone()
        cur.execute("SELECT homebranch FROM customer WHERE customer.cid = (SELECT ownedby FROM owns WHERE owns.account "
                    "= '{}');".format(destination))
        branch2 = cur.fetchone()
    if branch1[0] != branch2[0]:
        print('This is an external transfer')
        return
    cur.execute("SELECT balance FROM account WHERE account.accid = '{}';".format(initial))
    amt_i = cur.fetchone()
    cur.execute("SELECT balance FROM account WHERE account.accid = '{}';".format(destination))
    amt_d = cur.fetchone()
    trans = input('Enter transfer amount: ')
    bal_i = float(amt_i[0]) - float(trans)
    bal_d = float(amt_d[0]) + float(trans)
    cur.execute("UPDATE account SET balance = {} WHERE account.accid = '{}';".format(bal_d, destination))
    connect.commit()
    cur.execute("UPDATE account SET balance = {} WHERE account.accid = '{}';".format(bal_i, initial))
    connect.commit()
    desc = input('Type transfer description: ')
    transf = 'transfer'
    trans = float(trans)
    cur.execute("INSERT into transactions values ('{}', {}, '{}', {}, {}, '{}');".format(desc, (trans*-1), transf, random.randint(100000000000, 999999999999), initial, date.today()))
    cur.execute("INSERT INTO transactions values ('{}', {}, '{}', {}, {}, '{}');".format(desc, trans, transf, random.randint(100000000000, 999999999999), destination, date.today()))
    connect.commit()
    print('Transfer Complete')
    return
#Task for Timmy
def externalTransfer(cid, man):
    # This function allows customers/managers/tellers to transfer amounts to an account of another bank
    initial = input('Enter account number from the account you wish to transfer from: ')
    if man == 0:
        cur.execute("SELECT homebranch FROM customer WHERE customer.cid = '{}';".format(cid))
        branch1 = cur.fetchone()
        destination = input('Enter account number that you would like to transfer funds into: ')
        cur.execute("SELECT ownedby FROM owns WHERE owns.account = '{}';".format(destination))
        num = cur.fetchone()
        cur.execute("SELECT homebranch FROM customer WHERE customer.cid = '{}';".format(num[0]))
        branch2 = cur.fetchone()
    else:
        cur.execute("SELECT homebranch FROM customer WHERE customer.cid = (SELECT ownedby FROM owns WHERE owns.account "
                    "= '{}');".format(initial))
        branch1 = cur.fetchone()
        destination = input('Enter account number that you would like to transfer funds into: ')
        cur.execute("SELECT ownedby FROM owns WHERE owns.account = '{}';".format(destination))
        num = cur.fetchone()
        cur.execute("SELECT homebranch FROM customer WHERE customer.cid = (SELECT ownedby FROM owns WHERE owns.account "
                    "= '{}');".format(destination))
        branch2 = cur.fetchone()
    if branch1[0] == branch2[0]:
        print('This is not an external transfer')
        return
    destination = input('Enter account number that you would like to transfer funds into: ')
    cur.execute("SELECT balance FROM account WHERE account.accid = '{}';".format(initial))
    amt_i = cur.fetchone()
    cur.execute("SELECT balance FROM account WHERE account.accid = '{}';".format(destination))
    amt_d = cur.fetchone()
    trans = input('Enter transfer amount: ')
    bal_i = float(amt_i[0]) - float(trans)
    bal_d = float(amt_d[0]) + float(trans)
    cur.execute("UPDATE account SET balance = {} WHERE account.accid = '{}';".format(bal_d, destination))
    connect.commit()
    cur.execute("UPDATE account SET balance = {} WHERE account.accid = '{}';".format(bal_i, initial))
    connect.commit()
    desc = input('Type transfer description: ')
    transf = 'transfer'
    trans = float(trans)
    cur.execute("INSERT into transactions values ('{}', {}, '{}', {}, {}, '{}');".format(desc, (trans * -1), transf, random.randint(100000000000,999999999999), initial, date.today()))
    cur.execute("INSERT INTO transactions values ('{}', {}, '{}', {}, {}, '{}');".format(desc, trans, transf, random.randint(100000000000, 999999999999), destination, date.today()))
    connect.commit()
    print('Transfer Complete')
    return

#task for Timmy
def showStatement(cid):
    '''the statement of a (past) month of an account should list all the transactions for this account d
    during this month order by time.
    Furthermore, the account balance after each transaction should be shown.
     Finally, you should show the final account balance for the account at the end of the month.
    '''
    acct = input('Enter account number: ')
    if check_account(cid,acct) != True:
        print('Incorrect account number')
        return
    latest = date.today()
    latest.month = latest.month - 1
    cur.execute("SELECT * FROM transactions WHERE transactions.performedby = '{}' AND transactions.date < {}};".format(acct, latest))
    return
#task for Humberto
def showPendingTransactions():
    return

#the following functions can only be executed by managers

#Task for Humberto: manager functions
def addInterest():
    return

def addOverDraftFees():
    return

def addAccountFees():
    return

def showAnalytics():
    return
#whoever has time can add the loan stuff
def main():
    while True:

        print('''
                *** Welcome To MHT Bank ***

                    1. Customer Access
                    2. Employee Access
                    3. Exit                            ''')

        choice = input("Enter choice: ")
        clear()
        if (choice == '1'):
            print('''
                Welcome Please choose from the following:

                    1. Customer log-in page (For existing Customers only)
                    2. Get Started/ Sign-up (For new Customers only)

                You can return to main menu by pressing any key
                    ''')
            choice1 = input()
            clear()
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
                    clear()
                    if choix == '1':
                        createAccountExistingCust(cid)

                    elif choix == '2':
                        withdraw(cid, 0)

                    elif choix == '3':
                        deposit(cid, 0)

                    elif choix == '4':
                        transfer(cid, 0)

                    elif choix == '5':
                        externalTransfer(cid, 0)

                    elif choix == '6':
                        deleteAccount()

                    elif choix == '7':
                        showStatement(cid)

                    elif choix == '8':
                        showPendingTransactions()

                    elif choix == '9':
                        main()

                else:
                    print('CID does not exist.. Would you like to open a new account? ')
                    ans = input()
                    if ans.lower() == 'yes':
                        createAccountNewCust()
                    elif ans.lower() == 'no':
                        print("No problem. Let's return to main menu. ")
                        main()
                    else:
                        main()

            elif choice1 == '2':
                print('''
                            Welcome to HTM Bank .. We are happy to have you as a new customer ''')
                createAccountNewCust()
            else:
                main()


        elif (choice == '2'):
            print('''
                    Welcome..
                    1. Teller Access
                    2. Manager Access
                    ''')
            choice1 = input('Please enter access: ')
            eid = input('Enter your SSN: ')
            clear()

            if choice1 =='1':
                print('Welcome Teller')
                print('''
                        1. Show Customer information
                        2. Withdraw amount
                        3. Deposit amount
                        4. Transfer amount
                        5. External Transfer ''')
                choice2 = input()
                clear()
                if choice2 == '1':
                    showCustomerInformation()

                elif choice2 == '2':
                    withdraw()

                elif choice2 == '3':
                    deposit()

                elif choice2 == '4':
                    transfer()

                elif choice2 == '5':
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
                clear()
                if choice2 == '1':
                    showCustomerInformation()

                elif choice2 == '2':
                    showTellerInformation()

                elif choice2 == '3':
                    withdraw(0, 1)

                elif choice2 == '4':
                    deposit(0, 1)

                elif choice2 == '5':
                    transfer(0, 1)

                elif choice2 == '6':
                    externalTransfer(0, 1)

                elif choice2 == '7':
                    addInterest()

                elif choice2 == '8':
                    addOverDraftFees()

                elif choice2 == '9':
                    addAccountFees()

                elif choice2 == '10':
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



