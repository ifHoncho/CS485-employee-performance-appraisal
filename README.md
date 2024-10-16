# Employee Performance Evaluation & Appraisal Calculation Using Machine Learning

## Overview

This project is a proof of concept (PoC) for an Employee Performance Evaluation & Appraisal System utilizing Machine Learning techniques, specifically the RandomForest algorithm. The system analyzes employee performance data using predefined metrics and automates the appraisal process. Managers can interact with the model through a web portal, entering employee metrics to receive performance predictions. The results are visualized through CSV or Excel reports to help managers and HR departments make data-driven decisions.

## Table of Contents

1. Project Overview
2. Features
3. System Architecture
4. Technologies Used
5. Contributing

## Features

- **Employee Performance Prediction**: Use a RandomForest model trained on labeled employee data to predict performance outcomes.
- **Performance Evaluation**: Automatically compute and generate performance appraisal scores based on employee metrics.
- **Interactive Web Portal**: Allows managers to input employee data and view AI predictions regarding performance.
- **Report Generation**: Export appraisal results into CSV/Excel formats for visualization and further analysis.
- **User-Friendly Interface**: A web interface for easy interaction with the AI model.

## System Architecture

The system consists of the following components:

- **Frontend**: Web interface for data input, model interaction, and performance prediction visualization.
- **Backend**: Processes employee data, trains the RandomForest model, and generates performance predictions.
- **Database**: MySQL stores employee data, performance metrics, and appraisal results.
- **Machine Learning Module**: Implements RandomForest for performance analysis and prediction.

## Infrastructure

- **Database**: MySQL (hosted locally or on the cloud)
- **Compute Server**: Python environment (can be hosted on HPC or any cloud provider)
- **Web Interface**: Flask/Django for the backend with user interaction features

## Technologies Used

- **Python**: Core programming language for data processing and machine learning.
- **Flask/Django**: Web framework for backend API and data processing.
- **Pandas**: Data manipulation and cleaning.
- **Scikit-learn**: Implementing the RandomForest algorithm for performance prediction.
- **MySQL**: Relational database for storing employee performance data.
- **HTML/CSS/JavaScript**: For the web-based user interface.

### Sample CSV Structure

| Employee_ID | Department | Region | Education | Gender | Recruitment_Channel | Num_Trainings | Age | Previous_Year_Rating | Length_of_Service | Awards_Won | Avg_Training_Score | Promotion_Status |
|-------------|------------|--------|-----------|--------|---------------------|---------------|-----|----------------------|-------------------|------------|--------------------|------------------|
| 001         | Sales      | North  | Bachelor  | Male   | Agency              | 3             | 30  | 4                    | 5                 | 1          | 80                 | 0                |
| 002         | IT         | East   | Master    | Female | Sourcing            | 2             | 28  | 3                    | 4                 | 0          | 70                 | 1                |

## Contributing/Instructions to run this application

- Create a new branch (or fork, if you want):

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Activate the Virtual Environment**:
   A `.venv` file is already included in the repository. Activate it to keep dependencies isolated:
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```
     
5. **Run the Flask App**:
   Start the Flask application:
   ```bash
   cd employee_eval
   python3 employee_eval.py
   ```

6. **Access the Application**:
   Open your web browser and go to `http://127.0.0.1:5000/` to view the employee data input form.

### Notes
- **CSV Path**: Make sure the CSV file (`employee_promotion.csv`) is correctly placed in the specified path (`/mnt/data/employee_promotion.csv`) or update the `csv_path` in the Python script accordingly.
- **Secret Key**: Replace `your_secret_key_here` with a strong secret key for production use.
- **Debug Mode**: In production, do not use `debug=True` as it poses a security risk.
