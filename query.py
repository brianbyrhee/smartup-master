# Import module
import pymysql

# create connection
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='ferhat437',
                             db='mydatabase')

# Create cursor
my_cursor = connection.cursor()

# Execute Query
my_cursor.execute("SELECT * from projects WHERE category ='Film & Video'")

# Fetch the records
result = my_cursor.fetchall()

for i in result:
    print(i)
    print(i[0])

# Close the connection
connection.close()

# things to note:
# the result of this query that is stored in "result" is a tuple. To perform actions on it, you can iterate through it.
# each "i" in "result" is a row of the database. each line can be indexed to get specific members.