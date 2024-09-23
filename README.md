# Employee Performance Evaluation & Appraisal Calculation Using Machine Learning

## Overview

This project is a proof of concept (PoC) for an Employee Performance Evaluation & Appraisal System utilizing Machine Learning techniques, specifically the RandomForest algorithm. The system analyzes employee performance data using predefined metrics and automates the appraisal process. Managers can interact with the model through a web portal, entering employee metrics to receive performance predictions. The results are visualized through CSV or Excel reports to help managers and HR departments make data-driven decisions.

## Table of Contents

1. Project Overview
2. Features
3. System Architecture
4. Technologies Used

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

## Contributing

- Fork the repository.
- Create a new branch:

    ```bash
    git checkout -b feature/new-feature
    ```

- Make your changes and commit:

    ```bash
    git commit -m "Add new feature"
    ```

- Push to your branch:

    ```bash
    git push origin feature/new-feature
    ```

- Create a pull request for your changes to be reviewed.
