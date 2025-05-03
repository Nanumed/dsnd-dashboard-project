# In employee.py
from .query_base import QueryBase


class Employee(QueryBase):
    
    # Set the class attribute `name` to the string "employee"
    name = "employee"

    # Define the constructor to accept employee_id
    def __init__(self, employee_id=None):
        self.employee_id = employee_id
        self.name = self.fetch_name_from_database()  # Initialize the employee name

    def fetch_name_from_database(self):
        # Simulate fetching employee name from the database based on employee_id
        if self.employee_id:
            # Replace this with actual database fetching logic
            return f"Employee {self.employee_id}"  # Dummy name based on employee_id
        return "Unknown Employee"  # If no employee_id is provided

    def names(self):
        query = f"""
        SELECT first_name || ' ' || last_name AS full_name, employee_id
        FROM {self.name};
        """
        return self.query(query)

    def username(self, id):
        query = f"""
        SELECT first_name || ' ' || last_name AS full_name
        FROM {self.name}
        WHERE employee_id = {id};
        """
        return self.query(query)

    def model_data(self, id):
        query = f"""
                    SELECT SUM(positive_events) AS positive_events,
                           SUM(negative_events) AS negative_events
                    FROM {self.name}
                    JOIN employee_events
                        ON {self.name}.employee_id = employee_events.employee_id
                    WHERE {self.name}.employee_id = {id}
                    GROUP BY {self.name}.employee_id;
                """
        return self.pandas_query(query)
