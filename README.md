# My Budget
#### Video Demo:  https://youtu.be/xfrnoeq_bFw
#### Description:

My-Budget is a personal or family Budget solition. 

The application was written in Visual Studio Locally using Flash and Jinja 2. Mysql database server was used.

Please note: a Database backup is kept in the project rootfolder for reference. 


Pages and its discription:

1) Fixed Expenditure: This Page has 2 section:

	a) Category: Here we Give Cateroy names i.e. Home or Repayments.
	b) Fixed Expenditure: Here we assign Amount to the Categories. 

We do have the ability to edit the data i.e. append or delete any record form either of the section.


2) Sub-Category: This is where we assign Sub-categories to the primary category.
for example: One might have multiple repayment i.e. auto loan, personal loan etc. So these can be the Sub-Category.

One can only assign value no exceeding the amount assigned for the primary Category in Fixed Exepnditure.


3) Daily Expenses: This Page has 2 section:

	a) Here we can see our daily expenses which can be filtered by from and to date.
	Note: daily expenses gets registered on the Overview page which is a dashbord.

	b) We can see Month wise statistics, Expenses category wise and sub-category wise along with balance and total spendings.

4) Overview: This is a Dashbord page which give you statics of overall details including a pie chart should all the assigned value categories and the ability to register expenses.





**CODE DETAILS**

Python flask: View.py is the primary file. 

It uses multiple routes and extensively communicates with MySQL server for insert and retrive data.

HTML: We have used primarily 7 templates i.e

1) Login: login page uses css file StyleSheet.css

2) Register

3) Layout: a general page using all header and used as extension across 3 main html pages.

4) Fixed expenses: Splitted the page in 2 section. Uses form to insert and select table to display records.
Edit function was written in JS File name: templatescript.js. it creates elements inside a from by reading data from table in a loop and give user ability to append or delete data.

5) Sub-Category: Uses form to insert and select table to display records.
Edit function was written in JS File name: templatescript.js. it creates elements inside a from by reading data from table in a loop and give user ability to append or delete data.

6) Daily Expenses: This page uses form with post and get method to retrive data from database and display in table form.

We have used Jinja with if condition to display sub-category table only if category dropdown is selcted.

7) Overview: here we have user Google Pie chart to display category assignment stats. Also used form to insert daily expenditure and last 5 transactions.
also used 4 cards to display some info like total budget and balance etc.

We have used an SP i.e. INS_EXPENSES to insert espenses record from this page form.

DB: Budget

We have used 5 Tables to store various data and interlinked them with primary and reference keys. 

Category: saves category and categoryid is referenced into rest of the tables.

Fixesexpenses: Stores category assigned value with reference to userid and categoryid.

Subcat: This is a subcategory table stores subcategory and links to category and amount for each subcategory. This table is also referenced into expenses table.

Expenses: Registeres expenses and references them to subcat, category and fixedexpenses table to give concrete linked entries.

Users: Login table storing User name and Eyncripted Password.





-------------------------------------------------------------------------------END--------------------------------------------------------------------------------
