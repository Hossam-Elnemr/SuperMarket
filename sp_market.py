import sqlite3
import time
entriesDiscount = 5
Discount = 25

# Date to be printed in receipt
t = time.localtime(time.time())
localtime = time.asctime(t)
strtime = "Current Time: " + time.asctime(t)

# Connecting to the database and creating cursor 
conn = sqlite3.connect('all_data.sqlite')
cur = conn.cursor()
cur2 = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS PRODUCTSDATA (product_name TEXT, price INTEGER, barcode TEXT )''')
cur.execute('''CREATE TABLE IF NOT EXISTS CUSTOMERSDATA (name TEXT , email TEXT , count INTEGER)''')

values =list()
receipt = dict()
count_of_current_prod = dict()

def AddProduct():
    newproduct = input('Enter product name! : ')
    product_price = float(input('Enter the price! : '))
    barcode = input('Enter the product barocde!: ')
    cur.execute('INSERT INTO PRODUCTSDATA (product_name, price, barcode)VALUES (?,?,?)',(newproduct,product_price,barcode))
    cur.execute('SELECT product_name,price FROM PRODUCTSDATA WHERE barcode = ? ', (barcode,))
    # sqlstr1 = 'SELECT product_name, price,barcode FROM PRODUCTSDATA ORDER BY price DESC LIMIT 30'
    # something = cur.execute(sqlstr1)
def CustomerDataEntry():
    name = input("Enter your name: ").capitalize()
    email = input("Enter your email: ").lower()

    cur.execute('SELECT count FROM CUSTOMERSDATA WHERE email = ? ', (email,))
    row = cur.fetchone()
    
    if row is None:
        cur.execute('''INSERT INTO CUSTOMERSDATA (name, email, count)VALUES (?,?,1)''', (name,email))
    else:
        cur.execute('UPDATE CUSTOMERSDATA SET count = count + 1 WHERE email = ?',(email,))
    conn.commit()
    return email
def HasDiscount(entries):
    return entries == entriesDiscount
def CalcDiscount(total):
    # total = 0.75*total # (1-25/100)*total
    calc_offer = lambda amount_to_pay, dis: (1-dis/100)*amount_to_pay
    AfterDiscount = calc_offer(total, Discount)
    return AfterDiscount
def CashierProcess():
    total = 0
    print()
    email = CustomerDataEntry()
    cur.execute('''SELECT * FROM PRODUCTSDATA ORDER BY price DESC LIMIT 40 ''')
    rows = cur.fetchall()
    for row in rows:
        count_of_current_prod[row[0]] = 0
    while True :   
        try:      
            # sqlstr1 = 'SELECT product_name,barcode FROM PRODUCTSDATA ORDER BY price DESC LIMIT 30'
            # something = cur.execute(sqlstr1)
            # for row1 in something:
            #    products_and_barcode[row1[0]] = row1[1]
            cur.execute('''SELECT * FROM PRODUCTSDATA ORDER BY price DESC LIMIT 40 ''')
            rows = cur.fetchall()
            print("Products list: ")
            for row in rows:
                # print(row)    
                print(f"({row[0]}) Price: {row[1]}, Barcode: {row[2]}")
            print()
            cashier_barcode = input("BARCODE: ")
            cur.execute("SELECT product_name,price,barcode FROM PRODUCTSDATA WHERE barcode = ?",(cashier_barcode,))
            row = cur.fetchone()
            nametaken = row[0]
            pricetaken = row[1]
            # barcodetaken = row[2]
            count_of_current_prod[nametaken] += 1
            total += pricetaken
            print('\nYour list:')
            for key,val in count_of_current_prod.items():
                if val != 0:
                    print(f"{key} {val}")
            print(f"\nYour total amount to pay sofar is {total} $.")
            print('###################################\n')            
            receipt[nametaken] = count_of_current_prod[nametaken]
        except :
            # Discount
            cur.execute('SELECT count FROM CUSTOMERSDATA WHERE email = ?', (email,))
            entries = cur.fetchone()[0]
            AfterDiscount = 0
            print("Your receipt")
            print(receipt)
            if HasDiscount(entries):
                AfterDiscount = CalcDiscount(total)
                print("Total price before discount =",total,"$")
                print("Total price after discount =",AfterDiscount,"$")
            if(AfterDiscount == 0):
                print("Total price", total ,"$" )
            print(strtime)
            return total


# Adding a product
while True:
    q = input("Type 'y' if you want to add a new product: ")
    bool_add_prod = (q == 'y')
    if bool_add_prod:
        AddProduct()
    else:
        break
        # sqlstr1 = 'SELECT product_name, price,barcode FROM PRODUCTSDATA ORDER BY price DESC LIMIT 30'
        # something = cur.execute(sqlstr1)
        
# Cashier process till the end of the code
cashier_q = input("Type 'y' if you want to enter the Cashier: ")
bool_cashier = (cashier_q == 'y')
if bool_cashier:
    CashierProcess()
else:
    exit()
print()

cur.execute('SELECT email, count FROM CUSTOMERSDATA ORDER BY count DESC LIMIT 10')
rows = cur.fetchall()
print("*** Customers' email ***")
for row in rows:
    print(str(row[0]), row[1])
cur.close()
cur2.close()
