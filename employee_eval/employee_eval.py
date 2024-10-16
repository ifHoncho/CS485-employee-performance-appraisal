# Import necessary libraries
from flask import Flask, render_template, request, flash
import pandas as pd
import joblib
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = 'potato'  # Replace with a secure key

# Load the trained pipeline (preprocessor + model) using joblib
pipeline_path = 'employee_model.pkl'
pipeline = joblib.load(pipeline_path)

# Load CSV to determine fields
csv_path = 'employee_promotion.csv'
df = pd.read_csv(csv_path)

# Extract column names excluding the target variable 'is_promoted'
target_column = 'is_promoted'
feature_columns = [col for col in df.columns if col != target_column]

# Separate numerical and categorical columns
categorical_cols = df[feature_columns].select_dtypes(include=['object']).columns.tolist()

@app.route('/', methods=['GET', 'POST'])
def employee_form():
    form_data = {}
    if request.method == 'POST':
        # Extract form data and validate
        errors = []
        for column in feature_columns:
            value = request.form.get(column)
            if not value or value.strip() == "":
                errors.append(f"{column} is required.")
            else:
                form_data[column] = value

        if errors:
            for error in errors:
                flash(error)
            return render_template('employee_form.html', columns=feature_columns, options={col: df[col].unique().tolist() for col in categorical_cols}, form_data=form_data)

        # Convert form data into a DataFrame for prediction
        input_data = pd.DataFrame([form_data])

        # Ensure categorical fields are converted to the same categories as during training
        for col in categorical_cols:
            input_data[col] = pd.Categorical(input_data[col], categories=df[col].astype('category').cat.categories)

        # Make a prediction using the loaded pipeline
        try:
            prediction = pipeline.predict(input_data)
            probability = pipeline.predict_proba(input_data)[0][1]  # Get probability of being promoted
            flash(f"Prediction: Employee Promotion Status is {'Promoted' if prediction[0] == 1 else 'Not Promoted'} with a probability of {probability:.2f}")
        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            flash(f"An error occurred during prediction: {str(e)}")
            return render_template('employee_form.html', columns=feature_columns, options={col: df[col].unique().tolist() for col in categorical_cols}, form_data=form_data)

        return render_template('employee_form.html', columns=feature_columns, options={col: df[col].unique().tolist() for col in categorical_cols}, form_data=form_data)

    return render_template('employee_form.html', columns=feature_columns, options={col: df[col].unique().tolist() for col in categorical_cols}, form_data=form_data)

if __name__ == '__main__':
    app.run(debug=True)
