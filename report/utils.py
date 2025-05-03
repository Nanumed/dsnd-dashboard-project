import pickle
from pathlib import Path

# Using the Path object, create a `project_root` variable
# set to the absolute path for the root of this project directory
project_root = Path(__file__).resolve().parent.parent  # Going two levels up from utils.py

# Using the `project_root` variable, create a `model_path` variable
# that points to the file `model.pkl` inside the assets directory
model_path = project_root / 'assets' / 'model.pkl'

def load_model():
    # Open and load the model from the model.pkl file
    with model_path.open('rb') as file:
        model = pickle.load(file)

    return model
