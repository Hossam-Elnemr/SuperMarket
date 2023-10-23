import sqlite3
import time

# Connecting to the database and creating cursor 
conn = sqlite3.connect('all_data.sqlite')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS PRODUCTSDATA (product_name TEXT, price INTEGER, barcode TEXT )''')
cur.execute('''CREATE TABLE IF NOT EXISTS CUSTOMERSDATA (name TEXT , email TEXT , count INTEGER)''')

# adding a product
while True:
    q =input("Wanna add a product? ")
    if q == "yes":
        newproduct = input('Enter product name! : ')
        product_price = float(input('Enter the price! : '))
        barcode = input('Enter the product barocde!: ')
        cur.execute('INSERT INTO PRODUCTSDATA (product_name, price, barcode)VALUES (?,?,?)',(newproduct,product_price,barcode))
        cur.execute('SELECT product_name,price FROM PRODUCTSDATA WHERE barcode = ? ', (barcode,))
        # sqlstr1 = 'SELECT product_name, price,barcode FROM PRODUCTSDATA ORDER BY price DESC LIMIT 30'
        # something = cur.execute(sqlstr1)
    else:
        break
        # sqlstr1 = 'SELECT product_name, price,barcode FROM PRODUCTSDATA ORDER BY price DESC LIMIT 30'
        # something = cur.execute(sqlstr1)
        

# Cashier process till the end of the code
cashier_q = input('Cashier? : ')
if cashier_q == "yes":
    name = input("Enter your name: ").capitalize()
    email = input("Enter your email: ").lower()

    cur.execute('SELECT count FROM CUSTOMERSDATA WHERE email = ? ', (email,))
    row = cur.fetchone()
    
    if row is None:
        cur.execute('''INSERT INTO CUSTOMERSDATA (name, email, count)VALUES (?,?,1)''', (name,email))
    else:
        cur.execute('UPDATE CUSTOMERSDATA SET count = count + 1 WHERE email = ?',(email,))
    conn.commit()
else:
    exit()

values =list()
receipt = dict()
productinfo = []
products_and_barcode = dict()

# Date to be printed in receipt
t = time.localtime(time.time())
localtime = time.asctime(t)
strtime = "Current Time:" + time.asctime(t)

while True :   
        try:      
            # sqlstr1 = 'SELECT product_name,barcode FROM PRODUCTSDATA ORDER BY price DESC LIMIT 30'
            # something = cur.execute(sqlstr1)
            # for row1 in something:
            #    products_and_barcode[row1[0]] = row1[1]
            cur.execute('''SELECT * FROM PRODUCTSDATA ORDER BY price DESC LIMIT 40 ''')
            rows = cur.fetchall()
            for row in rows:
                # print(row)    
                products_and_barcode[row[0]] = row[2]
            print(products_and_barcode)
            cashier_barcode = input("BARCODE: ")
            result = cur.execute("SELECT product_name,price,barcode FROM PRODUCTSDATA WHERE barcode = ?",(cashier_barcode,))
            row = cur.fetchone()
            nametaken = row[0]
            productinfo.append(nametaken)
            pricetaken = row[1]
            productinfo.append(pricetaken)
            productinfo.append(cashier_barcode)
            print()
            print(productinfo)
            print()            
            values.append(pricetaken)
            receipt[nametaken] = pricetaken
        except :
            total = sum(values)
            print("Your receipt")
            print(receipt)
            print("Total price", total ,"$" )
            print(strtime)
            break
print()

cur.execute('SELECT email, count FROM CUSTOMERSDATA ORDER BY count DESC LIMIT 10')
rows = cur.fetchall()
print("*** Customers' email ***")
for row in rows:
    print(str(row[0]), row[1])

# Offer
if row[1] == 5:
    total = 0.75*total
    print("Total price after offer =",total,"$")
cur.close
