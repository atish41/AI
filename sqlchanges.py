import sqlite3
import numpy as np
import pandas as pd
connection = sqlite3.connect("rewardola1.db")
cursor = connection.cursor()

'''
query = """ALTER TABLE users RENAME COLUMN plat_form TO platform;"""

try:
  # Execute the query
  cursor.execute(query)
  # Commit the changes
  connection.commit()
  print("Column renamed successfully!")
except sqlite3.Error as error:
  print("Error renaming column:", error)

# Close the connection
connection.close()
'''

query = """select * from users;"""

try:
  # Execute the query
  print(cursor.execute(query))
  # Commit the changes
  connection.commit()
  #print("Column renamed successfully!")
except sqlite3.Error as error:
  print("Error renaming column:", error)

# Close the connection
connection.close()



# import sqlite3

# conn = sqlite3.connect('rewardola1.db')
# c = conn.cursor()

# # c.execute("DROP TABLE freq;")
# c.execute("SELECT name FROM sqlite_master WHERE type='table'")
# tables = c.fetchall()

# print("Tables in the database:")
# for i in tables:
#   print( i)

# conn.close()