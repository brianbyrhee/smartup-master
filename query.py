# Import module
import pymysql

# create connection
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='ferhat437',
                             db='mydatabase')

# Create cursor
my_cursor = connection.cursor()

# define the category
main_category = "Publishing" 

# query for finding all categories and storing them in a list

sqlquery = "SELECT DISTINCT main_category from projects"

my_cursor.execute(sqlquery)
result = my_cursor.fetchall()

maincategory_lst = []

for i in result:
    maincategory_lst.append(i[0])

print(maincategory_lst)

# query to find count of projects of main category
sqlquery = "SELECT COUNT(id) from projects WHERE main_category = '{}'".format(main_category)
my_cursor.execute(sqlquery)
count = my_cursor.fetchall()

print(count[0][0])



# query to find count of successful projects of main category
sqlquery = "SELECT COUNT(id) from projects WHERE main_category = '{}' AND (state = 'successful' OR state = 'live')".format(main_category)
my_cursor.execute(sqlquery)
success_count = my_cursor.fetchall()

print(success_count[0][0])


# query to find avg goal amount of main category
sqlquery = "SELECT AVG(usd_goal_real) from projects WHERE main_category = '{}'".format(main_category)
my_cursor.execute(sqlquery)
success_count = my_cursor.fetchall()

print(success_count[0][0])


# Close the connection
connection.close()

# things to note:
# the result of this query that is stored in "result" is a tuple. To perform actions on it, you can iterate through it.
# each "i" in "result" is a row of the database. each line can be indexed to get specific members.