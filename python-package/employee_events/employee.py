# Import the QueryBase class
from .query_base import QueryBase

# Import dependencies needed for sql execution from the `sql_execution` module
# (QueryMixin already imported in QueryBase)
# You don't need to import sql_execution explicitly as it's inherited

# Define a subclass of QueryBase called Employee
class Employee(QueryBase):
    
    # Set the class attribute `name` to the string "employee"
    name = "employee"

    # Define a method called `names` that receives no arguments
    # This method should return a list of tuples from an SQL execution
    def names(self):
        # Query 3
        # Write an SQL query that selects two columns: 
        # 1. The employee's full name
        # 2. The employee's id
        # This query should return the data for all employees in the database
        query = f"""
        SELECT first_name || ' ' || last_name AS full_name, employee_id
        FROM {self.name};
        """
        return self.query(query)
    
    # Define a method called `username` that receives an `id` argument
    # This method should return a list of tuples from an SQL execution
    def username(self, id):
        # Query 4
        # Write an SQL query that selects an employee's full name
        # Use f-string formatting and a WHERE filter
        # to only return the full name of the employee with an id equal to the id argument
        query = f"""
        SELECT first_name || ' ' || last_name AS full_name
        FROM {self.name}
        WHERE employee_id = {id};
        """
        return self.query(query)
    
    # Below is a method with an SQL query
    # This SQL query generates the data needed for the machine learning model.
    # Without editing the query, alter this method so when it is called, 
    # a pandas dataframe is returned containing the execution of the sql query.
    def model_data(self, id):
        query = f"""
                    SELECT SUM(positive_events) AS positive_events,
                           SUM(negative_events) AS negative_events
                    FROM {self.name}
                    JOIN employee_events
                        ON {self.name}.employee_id = employee_events.employee_id
                    WHERE {self.name}.employee_id = {id};
                """
        # Return the result as a pandas DataFrame
        return self.pandas_query(query)
