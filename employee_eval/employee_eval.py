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
pipeline_path = 'employee_eval/tuned_model_with_smote_checkpoint.pkl'
pipeline = joblib.load(pipeline_path)

# Define feature columns (based on the model training process)
feature_columns = [
    'employee_id', 'department', 'region', 'education', 'gender',
    'recruitment_channel', 'no_of_trainings', 'age', 'previous_year_rating',
    'length_of_service', 'awards_won', 'avg_training_score'
]

# Define categorical columns (based on the model training process)
categorical_cols = [
    'department', 'region', 'education', 'gender', 'recruitment_channel'
]

# Manually define dropdown options for categorical fields and validation ranges for numerical fields
options = {
    'department': ['Sales & Marketing', 'Operations', 'Technology', 'Analytics', 'R&D', 'Procurement', 'Finance', 'HR', 'Legal'],
    'region': [
        'region_7', 'region_22', 'region_19', 'region_23', 'region_26',
        'region_2', 'region_20', 'region_34', 'region_1', 'region_4',
        'region_29', 'region_31', 'region_15', 'region_14', 'region_11',
        'region_5', 'region_28', 'region_17', 'region_13', 'region_16',
        'region_25', 'region_10', 'region_27', 'region_30', 'region_12',
        'region_21', 'region_8', 'region_32', 'region_6', 'region_33',
        'region_24', 'region_3', 'region_9', 'region_18'
    ],
    'education': ["Master's & above", "Bachelor's", 'Below Secondary'],
    'gender': ['f', 'm'],
    'recruitment_channel': ['sourcing', 'other', 'referred']
}

# Validation ranges for numerical columns
numerical_ranges = {
    'no_of_trainings': (1, 10),
    'age': (20, 60),
    'previous_year_rating': (1.0, 5.0),
    'length_of_service': (1, 37),
    'awards_won': (0, 1),
    'avg_training_score': (39.0, 99.0)
}

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
                # Apply range validation for numerical fields
                if column in numerical_ranges:
                    try:
                        value = float(value)
                        min_val, max_val = numerical_ranges[column]
                        if not (min_val <= value <= max_val):
                            errors.append(f"{column} must be between {min_val} and {max_val}.")
                    except ValueError:
                        errors.append(f"{column} must be a valid number.")
                form_data[column] = value

        if errors:
            for error in errors:
                flash(error)
            return render_template('employee_form.html', columns=feature_columns, options=options, form_data=form_data)

        # Convert form data into a DataFrame for prediction
        input_data = pd.DataFrame([form_data])

        # Make a prediction using the loaded pipeline
        try:
            prediction = pipeline.predict(input_data)
            probability = pipeline.predict_proba(input_data)[0][1]  # Get probability of being promoted
            prediction_status = 'Promoted' if prediction[0] == 1 else 'Not Promoted'
            probability_percentage = round(probability * 100, 2)

            # Redirect to summary page with prediction details
            return render_template('summary.html', prediction_status=prediction_status, probability=probability_percentage, form_data=form_data)

        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            flash(f"An error occurred during prediction: {str(e)}")
            return render_template('employee_form.html', columns=feature_columns, options=options, form_data=form_data)

    return render_template('employee_form.html', columns=feature_columns, options=options, form_data=form_data)

if __name__ == '__main__':
    app.run(debug=True)
