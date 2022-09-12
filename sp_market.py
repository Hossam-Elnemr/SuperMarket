import sqlite3
import time
 
t = time.localtime(time.time())
localtime = time.asctime(t)
strtime = "Current Time:" + time.asctime(t)

conn = sqlite3.connect('customers.sqlite')
cur = conn.cursor() 
conn1 = sqlite3.connect('products.sqlite')
cur1 = conn1.cursor()

cur1.execute('''CREATE TABLE IF NOT EXISTS PRODUCTSDATA (product_name TEXT, price INTEGER, barcode TEXT )''')


while True:
    products_name = []
    products_price = []
    products_barcode = []
    q =input("Wanna add a product? ")
    if q == "yes":
        newproduct = input('Enter product name! : ')
        product_price = float(input('Enter the price! : '))
        barcode = input('Enter the product barocde!: ')
        cur1.execute('INSERT INTO PRODUCTSDATA (product_name, price, barcode)VALUES (?,?,?)',(newproduct,product_price,barcode))
        cur1.execute('SELECT product_name,price FROM PRODUCTSDATA WHERE barcode = ? ', (barcode,))
        conn1.commit()
        row1 = cur1.fetchone()
        sqlstr1 = 'SELECT product_name, price,barcode FROM PRODUCTSDATA ORDER BY price DESC LIMIT 30'
        something = cur1.execute(sqlstr1)
        
        '''for row1 in something:
            product_name_column = row1[0]
            price_column = row1[1]
            barcode_column = row1[2]
            products_name.append(product_name_column)
            products_price.append(price_column)
        print(products_name)'''
        
    else:
        sqlstr1 = 'SELECT product_name, price,barcode FROM PRODUCTSDATA ORDER BY price DESC LIMIT 30'
        something = cur1.execute(sqlstr1)
        '''for row1 in something:
            product_name_column = row1[0]
            price_column = row1[1]
            barcode_column = row1[2]
            products_name.append(product_name_column)
            products_price.append(price_column)
            print(barcode_column)'''
    break


cur.execute('''CREATE TABLE IF NOT EXISTS DATA ( name TEXT, email TEXT, count INTEGER )''')
cashier_q = input('Cashier? : ')
if cashier_q == "yes":    
    name = input("Enter your name: ")
    email = input("Enter your email: ")

    cur.execute('SELECT count FROM DATA WHERE name = ? ', (name,))

    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO DATA (name, email, count)VALUES (?,?,1)''', (name,email))
    else:
        cur.execute('UPDATE DATA SET count = count + 1 WHERE email = ?',(email,))
    conn.commit()


values =list()
receipt = dict()
productinfo = []
while True :   
        try:      
            cashbarcode = input("BARCODE: ")
            result = cur1.execute("SELECT product_name,price,barcode FROM PRODUCTSDATA WHERE barcode = ?",(cashbarcode,))
            row_1 = cur1.fetchone()
            nametaken = row_1[0]
            productinfo.append(nametaken)
            pricetaken = row_1[1]
            productinfo.append(pricetaken)
            productinfo.append(cashbarcode)
            print(productinfo)
            values.append(pricetaken)
            receipt[nametaken] = pricetaken
        except :
            total = sum(values)
            print("Your receipt")
            print(receipt)
            print("Total price", total ,"$" )
            print(strtime)
            break

sqlstr = 'SELECT email, count FROM DATA ORDER BY count DESC LIMIT 10'
print("** Customers' email ***")
for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])

#Offer
if row[1] == 5:
    total = 0.75*total
    print("Total price after offer =",total,"$")