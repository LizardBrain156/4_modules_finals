import pymysql
import time


def get_connection():
    return pymysql.connect(
        host="localhost",
        port=3307,
        user="root",
        password="pass",
        database="app",
        cursorclass=pymysql.cursors.DictCursor
    )


import time


def get_payment_status():
    connection = get_connection()

    status = None

    for _ in range(15):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT status FROM payment_entity ORDER BY id DESC LIMIT 1"
            )
            result = cursor.fetchone()

            if result and result.get("status"):
                status = result["status"]
                break

        time.sleep(1)

    connection.close()

    return status


def clear_database():
    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM payment_entity")
        cursor.execute("DELETE FROM credit_request_entity")
        cursor.execute("DELETE FROM order_entity")

    connection.commit()
    connection.close()

def get_payment_count():
    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) as count FROM payment_entity")
        result = cursor.fetchone()

    connection.close()

    return result["count"]