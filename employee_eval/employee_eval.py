from flask import Flask, render_template, request, flash, redirect, url_for
import pandas as pd
import joblib
import logging
from werkzeug.utils import secure_filename
import os
from db_utils import (
    insert_employee_data,
    get_all_employees,
    get_employees_by_ids,
    store_analysis_results,
    get_all_results
)
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'potato')  # Replace with secure key in production

# Load the trained pipeline
pipeline_path = os.path.join(os.path.dirname(__file__), 'tuned_model_with_smote_checkpoint.pkl')
pipeline = joblib.load(pipeline_path)

# Define feature columns
feature_columns = [
    'employee_id', 'department', 'region', 'education', 'gender',
    'recruitment_channel', 'no_of_trainings', 'age', 'previous_year_rating',
    'length_of_service', 'awards_won', 'avg_training_score'
]

@app.route('/', methods=['GET'])
def index():
    """Display the main page with file upload and employee selection"""
    try:
        employees = get_all_employees()
        return render_template('upload_and_select.html', employees=employees)
    except Exception as e:
        logger.error(f"Error loading index page: {str(e)}")
        flash(f"Error: {str(e)}", 'danger')
        return render_template('upload_and_select.html', employees=[])

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle CSV file upload"""
    if 'csvFile' not in request.files:
        flash('No file selected', 'warning')
        return redirect(url_for('index'))
    
    file = request.files['csvFile']
    if file.filename == '':
        flash('No file selected', 'warning')
        return redirect(url_for('index'))

    try:
        # Read CSV file
        df = pd.read_csv(file)
        
        # Validate required columns
        missing_cols = [col for col in feature_columns + ['is_promoted'] if col not in df.columns]
        if missing_cols:
            flash(f'Missing required columns: {", ".join(missing_cols)}', 'danger')
            return redirect(url_for('index'))
        
        # Insert data into database
        rows_affected = insert_employee_data(df)
        flash(f'Successfully processed {rows_affected} employee records', 'success')
        
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        flash(f'Error processing file: {str(e)}', 'danger')
        
    return redirect(url_for('index'))

@app.route('/analyze', methods=['POST'])
def analyze_employees():
    """Analyze selected employees"""
    selected_employees = request.form.getlist('selected_employees')
    
    if not selected_employees:
        flash('Please select at least one employee to analyze', 'warning')
        return redirect(url_for('index'))
    
    try:
        # Get employee data from database
        employees_data = get_employees_by_ids(selected_employees)
        
        # Convert to DataFrame for prediction
        df = pd.DataFrame(employees_data)
        
        # Make predictions
        results = []
        for _, employee in df.iterrows():
            # Prepare input data
            input_data = employee[feature_columns].to_frame().T
            
            # Get prediction and probability
            prediction = pipeline.predict(input_data)[0]
            probability = pipeline.predict_proba(input_data)[0][1]
            
            # Get feature importances if available
            factors = "Model analysis completed"  # Placeholder for feature importance
            
            # Store results
            store_analysis_results(
                employee_id=employee['employee_id'],
                probability=probability,
                factors=factors
            )
            
            results.append({
                'employee_id': employee['employee_id'],
                'department': employee['department'],
                'prediction': 'Promoted' if prediction == 1 else 'Not Promoted',
                'probability': round(probability * 100, 2)
            })
        
        return render_template('analysis_results.html', results=results)
        
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        flash(f'Error during analysis: {str(e)}', 'danger')
        return redirect(url_for('index'))

@app.route('/results')
def view_results():
    """Display all analysis results"""
    try:
        results = get_all_results()
        return render_template('view_results.html', results=results)
    except Exception as e:
        logger.error(f"Error retrieving results: {str(e)}")
        flash(f'Error retrieving results: {str(e)}', 'danger')
        return redirect(url_for('index'))

if __name__ == '__main__':
    # Add the parent directory to Python path for imports
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    app.run(debug=True)
