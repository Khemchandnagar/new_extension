import mysql.connector
import json


def execute_sql_query(sql_query):
    # Connect to the database
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="khem",
        database="face_extension"
    )

    try:
        cursor = connection.cursor()

        cursor.execute(sql_query)

        # connection.commit()

        results = cursor.fetchall()
        column_names = cursor.column_names

        rows = []
        for row in results:
            row_dict = dict(zip(column_names, row))
            rows.append(row_dict)

        # Convert the data to JSON
        json_data = json.dumps(rows)

        return json_data

    except mysql.connector.Error as error:
        print("Error executing SQL query:", error)

    finally:
        if cursor:
            cursor.close()
        if connection.is_connected():
            connection.close()

sql_query = "SELECT name FROM userWebId AS t1 JOIN websites AS t2 ON t1.webId = t2.webId WHERE t1.userId = 4014; "
results = execute_sql_query(sql_query)
print(results)
