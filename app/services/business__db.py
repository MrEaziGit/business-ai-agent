import sqlite3
import re
from pydantic import BaseModel
DATABASE = "business.db"

class OrderInput(BaseModel):
    order_id: str
    customer: str
    status: str
    total: int


def init_db():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id TEXT UNIQUE NOT NULL,
            customer TEXT NOT NULL,
            status TEXT NOT NULL,
            total INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            is_deleted INTEGER NOT NULL DEFAULT 0
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM orders")
    order_count = cursor.fetchone()[0]

    if order_count == 0:
        cursor.execute("""
            INSERT INTO orders (order_id, customer, status, total)
            VALUES (?, ?, ?, ?)
        """, ("ORD006", "Test User", "Cancelled", 20000))

    connection.commit()
    connection.close()
def check_order(order_id):

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM orders
        WHERE order_id = ?
    """, (order_id,))

    order = cursor.fetchone()

    connection.close()

    if order is None:
        return "Order not found"

    database_id, order_id, customer, status, total = order

    return {
        "order_id": order_id,
        "customer": customer,
        "status": status,
        "total": total
    }


def find_customer(customer):

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT order_id, customer, status, total
        FROM orders
        WHERE customer = ? 
    """, (customer,))

    orders = cursor.fetchall()

    connection.close()

    return [
        {
            "order_id": order[0],
            "customer": order[1],
            "status": order[2],
            "total": order[3]
        }
        for order in orders
    ]


def add_order(order_id, customer, status, total):

    order = OrderInput(
        order_id=order_id,
        customer=customer,
        status=status,
        total=total
    )

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    try:

        cursor.execute("""
            INSERT INTO orders (order_id, customer, status, total)
            VALUES (?, ?, ?, ?)
        """, (
            order.order_id,
            order.customer,
            order.status,
            order.total
        ))

        connection.commit()

    except sqlite3.IntegrityError:

        connection.close()

        return "Order ID already exists"

    connection.close()

    return "Order created successfully"


def update_order(order_id, status):

    valid_statuses = ["Processing", "Shipped", "cancelled"]
    if status not in valid_statuses:
        return f"Invalid status. Choose from: {', '}"

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        UPDATE orders
        SET status = ?
        WHERE order_id = ?
    """, (status, order_id))

    connection.commit()

    if cursor.rowcount == 0:

        connection.close()

        return "Order not found"

    connection.close()

    return "Order updated successfully"


def cancel_order(order_id):

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT status
        FROM orders
        WHERE order_id = ?
    """, (order_id,))

    order = cursor.fetchone()

    if order is None:

        connection.close()

        return "Order not found"

    status = order[0]

    if status == "Cancelled":

        connection.close()

        return "Order is already cancelled"

    if status != "Processing":

        connection.close()

        return f"Order cannot be cancelled because it is {status}"

    cursor.execute("""
        UPDATE orders
        SET status = ?
        WHERE order_id = ?
    """, ("Cancelled", order_id))

    connection.commit()

    connection.close()

    return "Order cancelled successfully"

def add_customer(name, email, phone):
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        return "invalid email format."
    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO customers (name, email, phone)
            VALUES (?, ?, ?)
        """, (name, email, phone))

        connection.commit()

    except sqlite3.IntegrityError:
        connection.close()
        return "A customer with that email already exists."

    connection.close()
    return "Customer created successfully"
def update_customer(email, phone):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE customers
        SET phone = ?
        WHERE email = ?

    """, (phone, email))

    connection.commit()

    if cursor.rowcount == 0:
        connection.close()
        return "Customer not found"

    connection.close()

    return "Customer updated succesfully"
def delete_customer(email):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE customers
        SET is_deleted = 1
        WHERE email = ? AND is_deleted = 0

    """, (email,))

    connection.commit()

    if cursor.rowcount == 0:
        connection.close()
        return "Customer not found or already deleted"

    connection.close()

    return "Customer deleted"

def list_orders():
    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT order_id, customer, status, total
        FROM orders
    """)

    orders = cursor.fetchall()

    connection.close()

    return [
        {
            "order_id": order[0],
            "customer": order[1],
            "status": order[2],
            "total": order[3]
        }
        for order in orders 
    ]
def search_orders(customer=None, status=None, order_id=None):
        query = "SELECT * FROM orders"
        conditions = []
        values = []


        if customer:
            conditions.append("customer = ?")
            values.append(customer)
        if status:
            conditions.append("status = ?")
            values.append(status)
        if order_id:
            conditions.append("order_id = ?")
            values.append(order_id)
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()
        cursor.execute(query, values)
        results = cursor.fetchall()
        connection.close()  
        if not results:
            return "No orders found matching those criteria"
        return [
            {
                "order_id": order[1],
                "customer": order[2],
                "status": order[3],
                "total": order[4]
            }
            for order in results
        ]

        
def get_order_stats():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM orders")
    total_orders = cursor.fetchone()[0]

    cursor.execute("""
        SELECT status, COUNT(*)
        FROM orders
        GROUP BY status
    """)
    status_counts = cursor.fetchall()
    cursor.execute("""
        SELECT status, SUM(total)
        FROM orders
        GROUP BY status
    """)
    status_values = cursor.fetchall()
    cursor.execute("SELECT COALESCE(SUM(total), 0) FROM orders")
    total_value = cursor.fetchone()[0]

    connection.close()

    return {
        "total_orders": total_orders,
        "status_counts": {
            status: count
            for status, count in status_counts 
        },
        "status_values": {
                status: value
                for status, value in status_values 
        },
        "total_value": total_value
    }
def get_customer_order_value(customer, status):
    status = status.capitalize()
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(total), 0)
        FROM orders
        WHERE customer = ? AND status = ?
    """, (customer, status))
    total_value = cursor.fetchone()[0]

    connection.close()
    return total_value 

def get_top_customer_by_order_value(status):
    status = status.capitalize()

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT customer, SUM(total)
        FROM orders
        WHERE status = ?
        GROUP BY customer
        ORDER BY SUM(total) DESC
        LIMIT 1
    """, (status,))

    result = cursor.fetchone()

    connection.close()

    if not result:
        return "No orders found for that status."

    return {
        "customer": result[0],
        "total_value": result[1]
    }
def get_order_status_percentage(status):
    status = status.capitalize()

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM orders")
    total_orders = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM orders 
        WHERE status = ?

    """, (status,))

    status_orders = cursor.fetchone()[0]
    connection.close()
    if total_orders == 0:
        return 0 
    return round((status_orders / total_orders) * 100, 2)
def get_average_order_value(status):
    status  = status.capitalize()
    connection =sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT AVG(total)
        FROM orders 
        WHERE status = ?
    """, (status,))

    average_value =cursor.fetchone()[0]
    connection.close()

    if average_value is None:
        return 0 
    return round(average_value, 2)
def compare_order_value_by_status(status1, status2):
    status1 = status1.capitalize()
    status2 = status2.capitalize()

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("""
        SELECT status, COALESCE(SUM(total), 0)
        FROM orders
        WHERE status IN (?, ?)
        GROUP BY status\
    """, (status1, status2))
    results = cursor.fetchall()
    connection.close()
    return {
        status: total
        for status, total in results
    }
def get_top_customer_shipping_stats():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT customer, SUM(total), COUNT(*)
        FROM orders
        WHERE status = 'Shipped'
        GROUP BY customer
        ORDER BY SUM(total) DESC
        LIMIT 1
    """)

    result = cursor.fetchone()

    connection.close()

    if not result:
        return "No shipped orders found."

    return {
        "customer": result[0],
        "total_value": result[1],
        "order_count": result[2]
    }
def get_customer(customer):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name, email, phone
        FROM customers
        WHERE name = ? AND is_deleted = 0
    """, (customer,))

    result = cursor.fetchone()

    connection.close()

    if not result:
        return "Customer not found"

    return {
        "name": result[0],
        "email": result[1],
        "phone": result[2]
    }

init_db()
