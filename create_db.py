import sqlite3
from sklearn.ensemble import RandomForestClassifier
import dill

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS scorers (scorer_id text PRIMARY KEY, scorer_obj BLOB, scorer_summary TEXT, scorer_uploaded TEXT)"
cursor.execute(create_table)

# query = "INSERT INTO models VALUES (?, ?, ?, datetime('now'))"
# cursor.execute(query, ('model_test', dill.dumps(RandomForestClassifier()), str(RandomForestClassifier)))

connection.commit()

connection.close()
