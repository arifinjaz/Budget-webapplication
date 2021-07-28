from __future__ import print_function
from mysql.connector import connection,Error
import mysql.connector



def connect():
    """ Connect to MySQL database """
    conn = None
    try:


        conn =connection.MySQLConnection(user='root', password='root',
                                 host='localhost',
                                 database='budget')
        
        
        if conn.is_connected():
            cursor = conn.cursor(dictionary=True)

            selectall = '''SELECT DISTINCT CATEGORY,AMOUNT,USERNAME 
                   from fixedexpenses F 
                   INNER JOIN CATEGORY C ON C.CATEGORYID = F.CATEGORYID  
                   INNER JOIN USERS U ON U.USERID = F.USERID 
                   where F.userid = 3'''

            cursor.execute(selectall)

            scategory = cursor.fetchall()

            t = 'Loans'
            tamt = '''SELECT SUM(F.AMOUNT) as TAMT 
                          FROM FIXEDEXPENSES F 
                          INNER JOIN SUBCAT SC ON SC.CATEGORYID = F.CATEGORYID
                          INNER JOIN CATEGORY C ON C.CATEGORYID = SC.CATEGORYID
                          WHERE SC.USERID = 3 AND C.CATEGORY = %s'''

            
            cursor.execute(tamt,(t,))

            tamt = cursor.fetchall()
            print(tamt[0]['TAMT'])

            query1 = "SELECT SUM(AMOUNT) AS TOTALAMOUNT FROM fixedexpenses where USERID = %s;"

            query2 = "SELECT SUM(AMOUNT) AS AMOUNTSPENT FROM EXPENSES where USERID = %s;"

            cursor.execute(query1,(3,))
            totalamount = cursor.fetchall() # total budget

            cursor.execute(query2,(3,))
            totalspent = cursor.fetchall() #total spent across all category

            balance = totalamount[0]['TOTALAMOUNT'] - totalspent[0]['AMOUNTSPENT'] # way to read sql query data directly
            print(totalamount[0]['TOTALAMOUNT'])
            #totalamount = totalamount[TOTALAMOUNT]
            #totalspent = totalspent[0][AMOUNTSPENT]
    
    except Error as e:
        print(e)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()


test1 = connect()
