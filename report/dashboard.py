from fasthtml.common import *
import matplotlib.pyplot as plt
import sys
import os

# Add the parent directory (project root) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'python-package')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'report')))

# Now you can import the classes
from employee_events.employee import Employee
from employee_events.team import Team

# Import the load_model function from the utils.py file
from report.utils import load_model

"""
Below, we import the parent classes you will use for subclassing
"""
from base_components import (
    Dropdown,
    BaseComponent,
    Radio,
    MatplotlibViz,
    DataTable
)

from combined_components import FormGroup, CombinedComponent


class ReportDropdown(Dropdown):
    def build_component(self, entity_id, model=None, **kwargs):
        self.label = model.name  # Set the label to the model's name
        # Pass the entity_id to the parent class method
        return super().build_component(entity_id=entity_id, model=model, **kwargs)

    def component_data(self, entity_id, model, **kwargs):
        # Now handle entity_id and model here
        # Call the method to fetch employee names and IDs from the model
        return model.names()






# Create a subclass of base_components/BaseComponent called `Header`
class Header(BaseComponent):
    def build_component(self, entity_id, model, **kwargs):
        # Use kwargs if needed, or just return the header
        return H1(model.name)  # For example, model.name can be used here


# Create a subclass of base_components/MatplotlibViz called `LineChart`
class LineChart(MatplotlibViz):
    def visualization(self, model, asset_id):
        # Pass the `asset_id` argument to the model's `event_counts` method to get event counts
        event_data = model.event_counts(asset_id)

        # Process the data and make it cumulative
        event_data = event_data.fillna(0).set_index('event_date').sort_index()
        event_data = event_data.cumsum()

        # Plot the data
        fig, ax = plt.subplots(figsize=(7, 4))
        event_data.plot(ax=ax)

        # Apply styling and set titles
        ax.set_axis_styling(border_color='black', font_color='black')
        ax.set_title(f"{model.name} Event Counts", fontsize=20)
        ax.set_xlabel('Event Date')
        ax.set_ylabel('Event Count')


# Create a subclass of base_components/MatplotlibViz called `BarChart`
class BarChart(MatplotlibViz):
    # Create a `predictor` class attribute
    predictor = load_model()

    def visualization(self, model, asset_id):
        # Using the model and asset_id arguments, pass the `asset_id` to the `.model_data` method
        # to receive the data that can be passed to the machine learning model
        data = model.model_data(asset_id)

        # Using the predictor class attribute, pass the data to the `predict_proba` method
        predictions = self.predictor.predict_proba(data)

        # Index the second column of predict_proba output
        pred = predictions[:, 1]  # Ensure we get the probabilities for the positive class

        # Below, create a `pred` variable set to the number we want to visualize
        # If the model's name attribute is "team", we want to visualize the mean of the predict_proba output
        if model.name == "team":
            pred = pred.mean()
        else:
            pred = pred[0]  # Otherwise set `pred` to the first value of the predict_proba output

        # Initialize a matplotlib subplot
        fig, ax = plt.subplots(figsize=(7, 2))

        # Run the following code unchanged
        ax.barh([''], [pred])
        ax.set_xlim(0, 1)
        ax.set_title('Predicted Recruitment Risk', fontsize=20)

        # Pass the axis variable to the `.set_axis_styling` method
        ax.set_axis_styling(border_color='black', font_color='black')


# Create a subclass of combined_components/CombinedComponent called Visualizations       
class Visualizations(CombinedComponent):
    # Set the `children` class attribute to a list containing initialized instances 
    # of `LineChart` and `BarChart`
    children = [
        LineChart(),
        BarChart()
    ]

    # Leave this line unchanged
    outer_div_type = Div(cls='grid')


# Create a subclass of base_components/DataTable called `NotesTable`
class NotesTable(DataTable):
    def component_data(self, model, entity_id):
        # Using the model and entity_id arguments, pass the entity_id to the model's .notes 
        # method. Return the output
        return model.notes(entity_id)


class DashboardFilters(FormGroup):
    id = "top-filters"
    action = "/update_data"
    method = "POST"

    children = [
        Radio(
            values=["Employee", "Team"],
            name='profile_type',
            hx_get='/update_dropdown',
            hx_target='#selector'
        ),
        ReportDropdown(
            id="selector",
            name="user-selection")
    ]


# Create a subclass of CombinedComponents called `Report`
class Report(CombinedComponent):
    # Set the `children` class attribute to a list containing initialized instances 
    # of the header, dashboard filters, data visualizations, and notes table
    children = [
        Header(),
        DashboardFilters(),
        Visualizations(),
        NotesTable()
    ]


# Initialize a fasthtml app
app = FastHTML()

# Initialize the `Report` class
report = Report()

# Create a route for a get request
# Set the route's path to the root
@app.route('/')
def home():
    employee = Employee(1)  # Create an Employee instance with ID 1
    return report(employee, Employee())  # Pass the actual Employee instance


# Create a route for a get request for employee details
@app.route('/employee/{id}')
def employee(id: str):
    employee = Employee(int(id))  # Create an Employee object using the ID
    return report(employee, Employee())  # Pass the Employee instance for individual employee report


# Create a route for a get request for team details
@app.route('/team/{id}')
def team(id: str):
    return report(id, Team())  # Passing team ID for team report


# Keep the below code unchanged!
@app.get('/update_dropdown{r}')
def update_dropdown(r):
    dropdown = DashboardFilters.children[1]
    print('PARAM', r.query_params['profile_type'])
    if r.query_params['profile_type'] == 'Team':
        return dropdown(None, Team())
    elif r.query_params['profile_type'] == 'Employee':
        return dropdown(None, Employee())


@app.post('/update_data')
async def update_data(r):
    from fasthtml.common import RedirectResponse
    data = await r.form()
    profile_type = data._dict['profile_type']
    id = data._dict['user-selection']
    if profile_type == 'Employee':
        return RedirectResponse(f"/employee/{id}", status_code=303)
    elif profile_type == 'Team':
        return RedirectResponse(f"/team/{id}", status_code=303)


serve()
