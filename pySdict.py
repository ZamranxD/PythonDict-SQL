#importing different libraries needed for the program
import mysql
from mysql import connector
import difflib
from difflib import SequenceMatcher
from difflib import get_close_matches

#establishing a connection with an SQL database through mysql.connector
con = mysql.connector.connect(
user = "ardit700_student",
password = "ardit700_student",
host = "108.167.140.122",
database = "ardit700_pm1database"
)

#taking the word from the user
word = input("Enter a word : ")

#initializing cursors to run queries and fetch results
#running this query to fetch the results for the word that user entered
cursor = con.cursor()
query = cursor.execute(f"SELECT * FROM Dictionary WHERE Expression = '{word}'")
results = cursor.fetchall()
#since the first cursor has done its work, the cursor can be used again.
#NOTEE:: DONT USE THE SECOND CURSOR WITHOUT FETCHING THE RESULTS OF THE FIRST ONE FIRST. I tried and it didn't work lol 
#so i figured

#running this second query to fetch all the keys/expressions from the Dictionary table so-
#that the program can give suggestions if the user enters a mis-spelled word.
cursor = con.cursor()
keey = cursor.execute("SELECT Expression FROM Dictionary")
keyResult = cursor.fetchall()
#keyResult returns a list of tuples, which in turn contain the keys. So, to simplify things, I'm just-
#running this loop to make a list of keys, hence removing the tuples from in between.
plzbkeys = []
for i in keyResult:
    for j in i:
        plzbkeys.append(j)

#now just checking for any mistaken word/giving output according to user entry.
if results:
    for result in results:
        print(result[1])
#this elif seems complex but this this just checks if the user enter a mis-spelled word. And if they did, then-
#it checks for the close matches and returns whatever the word closest to it is.
elif len(get_close_matches(word,plzbkeys,n=1 )) > 0:
    choice = input(f"Did you mean {get_close_matches(word,plzbkeys,n=1 )[0]}? Y/N? ")
    if choice=="Y" or choice=="y":
        cursor = con.cursor()
        query = cursor.execute(f"SELECT * FROM Dictionary WHERE Expression = '{get_close_matches(word,plzbkeys,n=1 )[0]}'")
        result = cursor.fetchall()
        #now result is again a list of tuples, so i'm just looping through to get the definitions instead of entire tuples-
        #or a key-value pair in the output
        if len(result) > 1:
            for item in result:
                print(item[1])
        else:
            print(result[0][1])
    else:
        print("Sorry we couldn't find your intended word!")
else:
    print("No such word found.")
