"""
Routes and views for the flask application.
"""
from __future__ import print_function
from mysql.connector import (connection,Error)
from datetime import datetime
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for, Markup
from flask_session import Session
from FlaskWebProject1 import app
from flask_sessions import Session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug import secure_filename
from tempfile import mkdtemp
from FlaskWebProject1.helper import login_required
from flask_cors import CORS, cross_origin

#app = Flask(__name__)
#app.config.from_object(__name__)

# Ensure templates are auto-reloaded


app.config['UPLOAD_FOLDER'] = "\img"

app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

SECRET_KEY = "sec3244332"
SESSION_TYPE = 'filesystem'
SESSION_FILE_DIR = mkdtemp()
#app.config.from_object(__name__)
Session(app)
CORS(app)

#global variable to get data from forms



conn = connection.MySQLConnection(user='root', password='root',
                                 host='localhost',
                                 database='budget')

commit = conn.commit
cursor = conn.cursor(buffered=True, dictionary=True)

@app.route("/category")
@login_required
def category():
    category = request.args.get("category")
    query = "select distinct category from category where category =%s"
    cursor.execute(query,(category,))
    row = cursor.fetchone()
    

    if row:
        flash(Markup('Category exists, kindly enter a unique name or use the existing one'))
        return redirect(url_for('fexp'))

    query = "insert into category (category,userid) values (%s,%s);"
    cursor.execute(query,(category, session["userid"],))
    conn.commit()
    return redirect("/fexp")


@app.route("/fixed", methods=["GET","POST"])
@login_required
def fixed():
    fixed = request.form.get


    catid = "select CATEGORYID from CATEGORY where CATEGORY = %s"
    cursor.execute(catid,(fixed("category"),))
    row = cursor.fetchall()
    for r in row:
        catid = r['CATEGORYID']

    query = "insert into FIXEDEXPENSES (AMOUNT,CATEGORYID,COMMENTS,USERID) values (%s,%s,%s,%s);"
    cursor.execute(query,(fixed("amount"),catid,fixed("comment"),session["userid"],))
    conn.commit()

    return redirect("/fexp")




@app.route('/')
@cross_origin(supports_credentials=True)
def login():
    session.clear()
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def loggingin():
    req = request.form.get
    if request.method == "POST":
        username = req("username")
        query = "SELECT * FROM USERS WHERE USERNAME = %s;"
        cursor.execute(query,(username,))
        row = cursor.fetchall()
        #check for username and password
        if len(row) != 1 or not check_password_hash(row[0]["PASSWORD"], req("password")):
            flash(Markup('Userid / Password do not match'))
            return redirect (url_for("login"))
        #session created
        session["userid"] = row[0]["USERID"]
        print(session["userid"])
        return redirect("/overview")
    return render_template("/login.html")




@app.route("/register", methods=["GET","POST"])
def register():
    req = request.form.get
    if request.method == "POST":
        fname = req("fname")
        lname = req("lname")
        email = req("email")
        username = req("username")
        query = "SELECT * FROM USERS WHERE EMAIL = %s"
        query2= "SELECT * FROM USERS WHERE username = %s"
        cursor.execute(query,(email,))
        row = cursor.fetchone()
        cursor.execute(query,(username,))
        rowuser = cursor.fetchone()
        if rowuser:
            flash('Username already exists. Please select a new username or login')
            return redirect("/register")
        if row:
            flash('Email address already exists, please ')
            return redirect("/register")
        password = generate_password_hash(req("password"),method='pbkdf2:sha256',salt_length = 8)
        cursor.execute("INSERT INTO USERS (FIRSTNAME,LASTNAME,EMAIL,USERNAME,PASSWORD) VALUES (%s, %s, %s, %s, %s)", (fname,lname,email,username,password))
        conn.commit()
        return render_template("/about.html")
    return render_template("register.html")




@app.route("/overview",methods=["GET", "POST"])
#@login_required
def overview():
    """Renders the home page."""
    user = 'SELECT USERNAME FROM USERS WHERE USERID = %s'
    cursor.execute(user,(session['userid'],))
    row = cursor.fetchone()

    default = 'Select a category'

    query = "SELECT CATEGORY FROM CATEGORY WHERE USERID = %s"
    cursor.execute(query,(session["userid"],))
    categories = cursor.fetchall()

    query = "SELECT DISTINCT AMOUNT,CATEGORY FROM FIXEDEXPENSES E INNER JOIN CATEGORY C ON C.CATEGORYID = E.CATEGORYID WHERE C.USERID = %s"
    cursor.execute(query,(session["userid"],))
    famount = cursor.fetchall()
    
    query = """SELECT CATEGORY,SUBCATNAME,E.AMOUNT AS EXPENDITURE,E.EXPENSESDESCRIPTION FROM
                EXPENSES E
                INNER JOIN CATEGORY C ON C.CATEGORYID = E.CATEGORYID
                INNER JOIN SUBCAT S ON S.SUBCATID = E.SUBCATID
                WHERE E.USERID = %s
                ORDER BY EXPENSESID DESC
                LIMIT 5;
            """
    cursor.execute(query,(session["userid"],))
    expenses = cursor.fetchall()


    # BELOW QURIES USED IN OVERVIEW CARDS

    query1 = "SELECT SUM(AMOUNT) AS TOTALAMOUNT FROM fixedexpenses where USERID = %s;"

    query2 = "SELECT SUM(AMOUNT) AS AMOUNTSPENT FROM EXPENSES where YEAR(CREATIONDATE) = YEAR(CURDATE()) AND MONTH(CREATIONDATE) = MONTH(CURDATE()) AND USERID = %s;"

    cursor.execute(query1,(session["userid"],))
    totalamount = cursor.fetchall() # total budget

    cursor.execute(query2,(session["userid"],))
    totalspent = cursor.fetchall() #total spent across all category

    balance = totalamount[0]['TOTALAMOUNT'] - totalspent[0]['AMOUNTSPENT'] # way to read sql query data directly

    totalamount = totalamount[0]['TOTALAMOUNT']
    totalspent = totalspent[0]['AMOUNTSPENT']


    query = """SELECT DISTINCT C.CATEGORY,
                SUM(S.AMOUNT) AS AMOUNTSPENT,
                F.AMOUNT AS TOTALASSIGNED
                FROM CATEGORY C 
                INNER JOIN EXPENSES S ON S.CATEGORYID = C.CATEGORYID
                INNER JOIN FIXEDEXPENSES F ON F.CATEGORYID = S.CATEGORYID
                WHERE YEAR(S.CREATIONDATE) = YEAR(CURDATE()) AND MONTH(S.CREATIONDATE) = MONTH(CURDATE())
                AND S.USERID = %s
                GROUP BY C.CATEGORY;
                """

    cursor.execute(query,(session["userid"],))
    categorydata = cursor.fetchall()

    overspent = []

    for c in categorydata:
       if (c['TOTALASSIGNED'] - c['AMOUNTSPENT']) < 0:
           overspent.append(c['CATEGORY'])
    print(overspent[0])







    if request.method == "POST":
        if  not request.form.get("subcategory"):
            cate = request.form.get("category")
            query = "SELECT SUBCATNAME FROM SUBCAT S INNER JOIN CATEGORY C ON C.CATEGORYID = S.CATEGORYID WHERE S.USERID = %s AND C.CATEGORY = %s"
            cursor.execute(query,(session["userid"],cate))
            subcategory = cursor.fetchall()
            amount = request.form.get("amount")
            description = request.form.get("particular")

            if subcategory == "":
                flash('Please select a valid subcategory')
                return redirect(url_for('overview'))

            cat = request.form.get("category")
        
            print(subcategory)

            return render_template(
            'overview.html',
            title='My Project',
            year=datetime.now().year,
            username = row["USERNAME"],
            default = cate,
            subcategory = subcategory,
            amount=amount,
            description = description,
            cat=cat,
            categories = categories,
            famount = famount,
            expenses=expenses
            )


        if request.form.get("subcategory"):
            re = request.form.get
            print(re)
            insert = "CALL INS_EXPENSES (%s,%s,%s,%s,%s,%s)"
            try:
                cursor.execute(insert,(re("category"),re("subcategory"),re("amount"),session["userid"],re("particular"),re("date"),))
                conn.commit()
            except (Error) as e:
                flash(Markup(e))

            return redirect("/overview")

    return render_template(
        'overview.html',
        title='My Project',
        year=datetime.now().year,
        username = row["USERNAME"],
        categories = categories,
        default = default,
        famount = famount,
        expenses=expenses,
        totalamount = totalamount,
        totalspent = totalspent,
        balance = balance,
        overspent = overspent
    )




@app.route("/fexp")
@login_required
def fexp():
    selectall = "select * from category where userid = %s;"
    cursor.execute(selectall,(session["userid"],))
    category = cursor.fetchall()

    selectall = "select CATEGORY, F.* from fixedexpenses F INNER JOIN CATEGORY C ON C.CATEGORYID = F.CATEGORYID where F.userid = %s;"
    cursor.execute(selectall,(session["userid"],))
    fixed = cursor.fetchall()

    totalamt = "select SUM(AMOUNT) AS TOTALAMT from fixedexpenses where userid = %s;"
    cursor.execute(totalamt,(session["userid"],))
    tamount = cursor.fetchall()
    #print(tamount)


    user = 'SELECT USERNAME FROM USERS WHERE USERID = %s;'
    cursor.execute(user,(session['userid'],))
    row = cursor.fetchone()

    return render_template(
        "/budget.html",
        title='fixed exp',
        username=row["USERNAME"],
        category=category,
        fixed=fixed,
        tamount = tamount[0]["TOTALAMT"]
        )


@app.route("/edit-budget")
@login_required
def editbudget():
    if request.args.get("Amount"):
        #this whill deal with fixed exp edit.
        if request.args.get("delete"):
            data = request.args.get
            query = "delete from FIXEDEXPENSES where FIXEDEXPENSEID = %s"
            try:
                cursor.execute(query,(data("id"),))
            except (Error) as e:
                flash(Markup(e))
                return redirect (url_for('subcat'))
            conn.commit()

            print(data)

        else:

            data = request.args.get
            query = "update FIXEDEXPENSES set amount = %s where FIXEDEXPENSEID = %s"

            try:
                cursor.execute(query,(data("Amount"),data("id"),))
            except (Error) as e:
                flash(Markup(e))
                return redirect (url_for('subcat'))
            conn.commit()

#this will deal with Category
    else:
        if request.args.get("delete"):
            data = request.args.get
            print(data)
            query = "delete from CATEGORY where CATEGORYID = %s"
            try:
                cursor.execute(query,(data("id"),))
            except (Error) as e:
                flash(Markup(e))
                return redirect (url_for('subcat'))
            conn.commit()

            #print(data)

        else:
            
            data = request.args.get

            query = "update CATEGORY SET CATEGORY = %s where CATEGORYID = %s"

            try:
                cursor.execute(query,(data("Category"),data("id"),))
            except (Error) as e:
                flash(Markup(e))
                return redirect (url_for('subcat'))
            conn.commit()
        print("category")



        

    return redirect("/fexp")



@app.route("/subcat")
@login_required
def subcat():
    active_page = "subcat"
    cursor.reset()
    selectall = '''SELECT DISTINCT CATEGORY,AMOUNT,USERNAME 
                   from fixedexpenses F 
                   INNER JOIN CATEGORY C ON C.CATEGORYID = F.CATEGORYID  
                   INNER JOIN USERS U ON U.USERID = F.USERID 
                   where F.userid = %s'''

    cursor.execute(selectall,(session["userid"],))
    scategory = cursor.fetchall()
    subcat = {}
    tamt = 0
    amount = 0
    category = "SELECT ONE"


    if request.args.get("category"):
        category = request.args.get("category")
        set = ("set @category = %s")
        cursor.execute(set,(category,))
        for s in scategory:
            if s["CATEGORY"] == category:
                amount=s["AMOUNT"]
                print(type(amount))

                query = '''SELECT DISTINCT C.CATEGORY,SUBCATNAME,AMOUNT,USERNAME,SUBCATID FROM 
                            SUBCAT SU 
                            INNER JOIN CATEGORY C ON C.CATEGORYID = SU.CATEGORYID
                            INNER JOIN USERS U ON U.USERID = SU.USERID
                            WHERE SU.USERID = %s AND C.CATEGORY = %s
                            '''
                tamt = '''SELECT ((F.AMOUNT) - SUM(SC.AMOUNT)) AS  BALANCE , SUM(SC.AMOUNT) AS TOTALAMOUNT
                          FROM FIXEDEXPENSES F 
                          INNER JOIN SUBCAT SC ON SC.CATEGORYID = F.CATEGORYID
                          INNER JOIN CATEGORY C ON C.CATEGORYID = SC.CATEGORYID
                          WHERE SC.USERID = %s AND C.CATEGORY = %s'''
                try:
                    cursor.execute(query,(session["userid"],category,))
                except (Error) as e:
                    flash(Markup(e))
                    return redirect (url_for('subcat'))

                subcat = cursor.fetchall()

                try:
                    cursor.execute(tamt,(session["userid"],category,))

                except (Error) as e:
                    flash(Markup(e))
                    return redirect (url_for('subcat'))

                # Total amount of a particular category  
                tamt = cursor.fetchall()

                return render_template("sub-category.html",active_page=active_page,
                           scategory=scategory,
                           amount=int(amount),
                           category = category,
                           subcat = subcat,
                           username = scategory[0]["USERNAME"],
                           totalamount = tamt[0]['TOTALAMOUNT'],
                           balance = tamt[0]['BALANCE']
                           )

    if request.args.get("subcat-name"):
        subcat = request.args.get
        cursor.execute("select @category")
        cat = cursor.fetchone()

        insert = "CALL INS_SUBCAT (%s,%s,%s,%s)"

        cursor.execute(insert,(cat['@category'],subcat("subcat-name"),subcat("subcat-amt"),session["userid"],))
        conn.commit()

        selectall = '''SELECT C.CATEGORY,SUBCATNAME,AMOUNT,USERNAME,SUBCATID FROM 
            SUBCAT SU 
            INNER JOIN CATEGORY C ON C.CATEGORYID = SU.CATEGORYID
            INNER JOIN USERS U ON U.USERID = SU.USERID
            WHERE SU.USERID = %s AND C.CATEGORY = %s
        '''

        tamt = '''SELECT ((F.AMOUNT) - SUM(SC.AMOUNT)) AS  BALANCE , SUM(SC.AMOUNT) AS TOTALAMOUNT
                          FROM FIXEDEXPENSES F 
                          INNER JOIN SUBCAT SC ON SC.CATEGORYID = F.CATEGORYID
                          INNER JOIN CATEGORY C ON C.CATEGORYID = SC.CATEGORYID
                          WHERE SC.USERID = %s AND C.CATEGORY = %s'''


        #cursor.execute(selectall,(session["userid"],subcat("hcat"),))

        try:
            cursor.execute(selectall,(session["userid"],subcat("hcat"),))

        except (Error) as e:
            flash(Markup(e))
            return redirect (url_for('subcat'))

        subcategory = cursor.fetchall()

        print(subcategory)
        try:
            cursor.execute(tamt,(session["userid"],subcat("hcat"),))
        except (Error) as e:
            flash(Markup(e))

            return redirect (url_for('subcat'))
        # Total amount of a particular category  
        tamt = cursor.fetchall()

        return render_template("sub-category.html",active_page=active_page,
                           scategory=scategory,
                           amount=int(amount),
                           category = category,
                           subcat = subcategory,
                           username = scategory[0]["USERNAME"],
                           totalamount = tamt[0]['TOTALAMOUNT'],
                           balance = tamt[0]['BALANCE']
                           )



    return render_template("sub-category.html",active_page=active_page,
                           scategory=scategory,
                           amount=int(amount),
                           category = category,
                           subcat = subcat,
                           username = scategory[0]["USERNAME"],
                           totalamount = tamt
                           )




@app.route("/edit-subcat")
@login_required
def editsubcat():

    if request.args.get("delete"):
        data = request.args.get
        query = "delete from subcat where subcatid = %s"
 
        try:
            cursor.execute(query,(data("id"),))

        except (Error) as e:
            flash(Markup(e))
            return redirect (url_for('subcat'))
        conn.commit()

        print(data)
    else:

        data = request.args.get

        query = "update subcat set amount = %s where subcatid = %s"

        try:
            cursor.execute(query,(data("Amount"),data("id"),))
        except (Error) as e:
            flash(Markup(e))
            return redirect (url_for('subcat'))
        conn.commit()


        print("amend")
    return redirect("/subcat")

@app.route("/expenses",methods=["GET", "POST"])
#@login_required
def expenses():
        
    query = "SELECT CATEGORY FROM CATEGORY WHERE USERID = %s"
    cursor.execute(query,(session["userid"],))
    categories = cursor.fetchall()

    if request.method == "POST": #this shall fetch expenses data
        
        #this whill deal with expenses edit.
        if request.form.get("delete"):
            print("yes delete")
            data = request.form.get
            query = "delete from expenses where expensesid = %s"
            try:
                cursor.execute(query,(data("id"),))
            except (Error) as e:
                flash(Markup(e))
                return redirect (url_for('expenses'))
            conn.commit()

            print(data)

        elif request.form.get("append"):
            print("yes amend")
            data = request.form.get
            query = "update expenses set amount = %s where expensesid = %s"

            try:
                cursor.execute(query,(data("Amount"),data("id"),))
            except (Error) as e:
                flash(Markup(e))
                return redirect (url_for('subcat'))
            conn.commit()


        print(request.form.get)
        req = request.form.get
        fromd = req("from-date")
        tod = req("to-date")
        query = """SELECT C.CATEGORY,S.SUBCATNAME,E.AMOUNT,E.EXPENSESID FROM EXPENSES E
                    INNER JOIN CATEGORY C ON C.CATEGORYID = E.CATEGORYID
                    INNER JOIN SUBCAT S ON S.SUBCATID = E.SUBCATID
                    WHERE E.CREATIONDATE BETWEEN %s and %s
                """
        cursor.execute(query,(fromd,tod,))
        expenses = cursor.fetchall()


        query = "SELECT CATEGORY FROM CATEGORY WHERE USERID = %s"
        cursor.execute(query,(session["userid"],))
        categories = cursor.fetchall()


        return render_template("expenses.html",
                           expenses = expenses,
                           categories=categories
                           )

    #to festch data on monthly basis
    if request.args.get("from-date"):

        fdate = request.args.get("from-date")
        year = fdate[0:4]
        month = fdate[5:7]
        
        query = """
                SELECT DISTINCT C.CATEGORY,
                SUM(S.AMOUNT) AS AMOUNTSPENT,
                F.AMOUNT AS TOTALASSIGNED
                FROM CATEGORY C 
                INNER JOIN EXPENSES S ON S.CATEGORYID = C.CATEGORYID
                INNER JOIN FIXEDEXPENSES F ON F.CATEGORYID = S.CATEGORYID
                WHERE YEAR(S.CREATIONDATE) = %s AND MONTH(S.CREATIONDATE) = %s
                AND S.USERID = %s
                GROUP BY C.CATEGORY;
                """

        cursor.execute(query,(year,month,session["userid"],))
        categorydata = cursor.fetchall()


        
        query1 = "SELECT SUM(AMOUNT) AS TOTALAMOUNT FROM fixedexpenses where USERID = %s;"

        query2 = "SELECT SUM(AMOUNT) AS AMOUNTSPENT FROM EXPENSES where YEAR(CREATIONDATE) = %s AND MONTH(CREATIONDATE) = %s AND USERID = %s;"

        cursor.execute(query1,(session["userid"],))
        totalamount = cursor.fetchall() # total budget

        cursor.execute(query2,(year,month,session["userid"],))
        totalspent = cursor.fetchall() #total spent across all category

        balance = totalamount[0]['TOTALAMOUNT'] - totalspent[0]['AMOUNTSPENT'] # way to read sql query data directly

        totalamount = totalamount[0]['TOTALAMOUNT']
        totalspent = totalspent[0]['AMOUNTSPENT']

        
        if request.args.get("category"):
            print('yes')
            cate = request.args.get("category")
            query = """
                SELECT DISTINCT 
                SU.SUBCATNAME,
                SUM(S.AMOUNT) AS AMOUNTSPENT,
                SU.AMOUNT AS TOTALASSIGNED,
                F.AMOUNT AS CATEGORYASSIGNED,
                C.*
                FROM EXPENSES S
                INNER JOIN SUBCAT SU ON S.SUBCATID = SU.SUBCATID
                LEFT JOIN CATEGORY C ON C.CATEGORYID = SU.CATEGORYID
                INNER JOIN FIXEDEXPENSES F ON F.CATEGORYID = S.CATEGORYID
                WHERE YEAR(S.CREATIONDATE) = %s AND MONTH(S.CREATIONDATE) = %s AND S.USERID =%s AND C.CATEGORY =%s 
                GROUP BY SU.SUBCATNAME;
                """

            cursor.execute(query,(year,month,session["userid"],cate,))
            subcategorydata = cursor.fetchall()

            print(categorydata)
            #query = """SELECT SUBCATNAME FROM subcat s
             #       INNER JOIN CATEGORY C ON C.CATEGORYID = S.CATEGORYID
              #      WHERE C.CATEGORY = %s and S.USERID =%s; 
               #     """
            #cursor.execute(query,(cate,session["userid"],))
            #subcategory = cursor.fetchall()
            query1 = "SELECT SUM(F.AMOUNT) as TOTALAMOUNT FROM fixedexpenses F INNER JOIN CATEGORY C ON C.CATEGORYID = F.CATEGORYID WHERE F.USERID = %s AND C.CATEGORY = %s;"

            query2 = "SELECT SUM(AMOUNT) AS AMOUNTSPENT FROM EXPENSES E INNER JOIN CATEGORY C ON C.CATEGORYID = E.CATEGORYID where E.USERID = %s AND C.CATEGORY = %s;"

            cursor.execute(query1,(session["userid"],cate))
            totalamount = cursor.fetchall() # total budget

            cursor.execute(query2,(session["userid"],cate))
            totalspent = cursor.fetchall() #total spent across all category

            balance = totalamount[0]['TOTALAMOUNT'] - totalspent[0]['AMOUNTSPENT'] # way to read sql query data directly

            totalamount = totalamount[0]['TOTALAMOUNT']
            totalspent = totalspent[0]['AMOUNTSPENT']

            return render_template("expenses.html"
                            , categories = categories,
                            categorydata = categorydata,
                            subcategorydata = subcategorydata,
                            cate = cate,
                            fdate = fdate,
                            ctotalamount = totalamount,
                            ctotalspent = totalspent,
                            cbalance = balance)


        return render_template("expenses.html"
                           , categories = categories,
                           categorydata = categorydata,
                           fdate = fdate,
                           totalamount = totalamount,
                           totalspent = totalspent,
                           balance = balance)

    return render_template("expenses.html"
                           , categories = categories)



if __name__ == '__main__':
    app.run(debug=True)
