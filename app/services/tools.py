from datetime import datetime
from app.services.business__db import check_order, find_customer, add_order, update_order, cancel_order, add_customer, update_customer, delete_customer, list_orders, search_orders, get_order_stats, get_customer_order_value, get_top_customer_by_order_value, get_order_status_percentage, get_average_order_value, compare_order_value_by_status

def calculate(a, b):
    return a + b


def get_time():
    return datetime.now().strftime("%H:%M:%S")



tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Add two numbers together.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "The first number."
                    },
                    "b": {
                        "type": "number",
                        "description": "The second number."
                    }
                },
                "required": ["a", "b"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "Get the current local time.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
       {
        "type": "function",
        "function": {
            "name": "check_order",
            "description": "Look up a customer's order using the order ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The customer's order ID."
                    }
                },
                "required": ["order_id"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "find_customer",
            "description": "Find all orders belonging to a customer by their name. Use this only for questions about orders. Do not use it for payment history, payments, transactions, or other financial records.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer": {
                        "type": "string",
                        "description": "The customer's name."
                    }
                },
                "required": ["customer"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_order",
            "description": "create a new customer order.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The unique order ID."
                    },
                    "customer": {
                        "type": "string",
                        "description": "The customer name",
                    },
                    "status": {
                        "type": "string",
                        "description": "The current status of the order",
                    },
                    "total": {
                        "type": "string",
                        "description": "The current state of the order"
                    }
                },
                "required": ["order_id", "customer", "status", "total"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_order",
            "description": "Update the status of an existing customer order.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The order ID to update."
                    },
                    "status": {
                        "type": "string",
                        "description": "The new status for the order."
                    }
                },
                "required": ["order_id", "status"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cancel_order",
            "description": "Cancel an existing customer order.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The order ID to cancel."
                    }
                },
                "required": ["order_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_customer",
            "description": "Add a new customer to the database.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The customer's name."
                    },
                    "email": {
                        "type": "string",
                        "description": "The customer's email address."
                    },
                    "phone": {
                        "type": "string",
                        "description": "The customer's phone number."
                    }
                },
                "required": ["name", "email", "phone"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_customer",
            "description": "Update a customer's phone number.",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "The customer's email address."
                    },
                    "phone": {
                        "type": "string",
                        "description": "The customer's new phone number."
                    }
                },
                "required": ["email", "phone"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_customer",
            "description": "Soft delete a customer from the database.",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "The email address of the customer to delete."
                    }
                },
                "required": ["email"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_orders",
            "description": "Retrieve all customer orders from the database.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_orders",
            "description": "Search customer orders using one or more optional filters.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer": {
                        "type": "string",
                        "description": "The customer's name to search for."
                    },
                    "status": {
                        "type": "string",
                        "description": "The order status to search for."
                    },
                    "order_id": {
                        "type": "string",
                        "description": "The order ID to search for."
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_order_stats",
            "description": "Get overall order statistics, including the total number of orders, number of orders by status and total value of orders.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_customer_order_value",
            "description": "Get the total value of a customer's orders for a specific status.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer": {
                        "type": "string",
                        "description": "The customer's name."
                    },
                    "status": {
                        "type": "string",
                        "description": "The order status to calculate the total value for."
                    }
                },
                "required": ["customer", "status"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_top_customer_by_order_value",
            "description": "Find the customer with the highest total order value for a specific status.",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "description": "The order status to check, such as Shipped, Processing, or Cancelled."
                    }
                },
                "required": ["status"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_order_status_percentage",
            "description": "Calculate the percentage of all orders that have a specific status.",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "description": "The order status to calculate the percentage for."
                    }
                },
                "required": ["status"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_average_order_value",
            "decription": "calculate the average of all orders that have a spcific status.",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "description": "The order status to calculate the average value for."

                    }
                },
                "required": ["status"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "compare_order_value_by_status",
            "description": "Compare the total value of orders between two different statuses.",
            "parameters": {
                "type": "object",
                "properties": {
                    "status1": {
                        "type": "string",
                        "description": "The first order status to compare."
                    },
                    "status2": {
                        "type": "string",
                        "description": "The second order status to compare."
                    }
                },
                "required": ["status1", "status2"]
            }
        }
    }
]

tool_functions = {
    "calculate": calculate,
    "get_time": get_time,
    "check_order": check_order,
    "find_customer": find_customer,
    "add_order": add_order,
    "update_order": update_order,
    "cancel_order": cancel_order,
    "add_customer": add_customer,
    "update_customer": update_customer,
    "delete_customer": delete_customer,
    "list_orders": list_orders,
    "search_orders": search_orders,
    "get_order_stats": get_order_stats,
    "get_customer_order_value": get_customer_order_value,
    "get_top_customer_by_order_value": get_top_customer_by_order_value,
    "get_order_status_percentage": get_order_status_percentage,
    "get_average_order_value": get_average_order_value,
    "compare_order_value_by_status": compare_order_value_by_status
}