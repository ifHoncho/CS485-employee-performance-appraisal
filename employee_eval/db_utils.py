import mysql.connector
from mysql.connector import Error
import pandas as pd
import numpy as np
from db_config import DB_CONFIG

def get_db_connection():
    """Create and return a database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        raise Exception(f"Error connecting to MySQL Database: {e}")

def insert_employee_data(df):
    """Insert employee data from DataFrame into the database"""
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        # Replace empty strings with None/NULL
        df = df.replace(r'^\s*$', None, regex=True)
        
        # Convert specific columns to appropriate types with NULL handling
        df['previous_year_rating'] = pd.to_numeric(df['previous_year_rating'], errors='coerce')
        df['avg_training_score'] = pd.to_numeric(df['avg_training_score'], errors='coerce')
        
        # Prepare the insert query
        insert_query = """
        INSERT INTO employee_metrics (
            employee_id, department, region, education, gender,
            recruitment_channel, no_of_trainings, age, previous_year_rating,
            length_of_service, awards_won, avg_training_score, is_promoted
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        ) ON DUPLICATE KEY UPDATE
            department = VALUES(department),
            region = VALUES(region),
            education = VALUES(education),
            gender = VALUES(gender),
            recruitment_channel = VALUES(recruitment_channel),
            no_of_trainings = VALUES(no_of_trainings),
            age = VALUES(age),
            previous_year_rating = VALUES(previous_year_rating),
            length_of_service = VALUES(length_of_service),
            awards_won = VALUES(awards_won),
            avg_training_score = VALUES(avg_training_score),
            is_promoted = VALUES(is_promoted)
        """
        
        # Convert DataFrame to list of tuples for insertion
        # Replace NaN with None for SQL NULL
        values = df.replace({np.nan: None}).to_records(index=False).tolist()
        
        # Execute batch insert
        cursor.executemany(insert_query, values)
        connection.commit()
        
        return cursor.rowcount
    except Error as e:
        connection.rollback()
        raise Exception(f"Error inserting data: {e}")
    finally:
        cursor.close()
        connection.close()

def get_all_employees():
    """Retrieve all employees from the database"""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT employee_id, department, region FROM employee_metrics")
        return cursor.fetchall()
    except Error as e:
        raise Exception(f"Error retrieving employees: {e}")
    finally:
        cursor.close()
        connection.close()

def get_employees_by_ids(employee_ids):
    """Retrieve specific employees by their IDs"""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        placeholders = ', '.join(['%s'] * len(employee_ids))
        query = f"SELECT * FROM employee_metrics WHERE employee_id IN ({placeholders})"
        cursor.execute(query, tuple(employee_ids))
        return cursor.fetchall()
    except Error as e:
        raise Exception(f"Error retrieving employees: {e}")
    finally:
        cursor.close()
        connection.close()

def store_analysis_results(employee_id, probability, factors):
    """Store the analysis results in the database"""
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        insert_query = """
        INSERT INTO employee_results (
            employee_id, promotion_probability, analysis_factors
        ) VALUES (%s, %s, %s)
        """
        cursor.execute(insert_query, (employee_id, probability, factors))
        connection.commit()
    except Error as e:
        connection.rollback()
        raise Exception(f"Error storing analysis results: {e}")
    finally:
        cursor.close()
        connection.close()

def get_all_results():
    """Retrieve all analysis results with employee information"""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        query = """
        SELECT 
            r.result_id,
            r.employee_id,
            r.analysis_date,
            r.promotion_probability,
            r.analysis_factors,
            m.department,
            m.region
        FROM employee_results r
        JOIN employee_metrics m ON r.employee_id = m.employee_id
        ORDER BY r.analysis_date DESC
        """
        cursor.execute(query)
        return cursor.fetchall()
    except Error as e:
        raise Exception(f"Error retrieving results: {e}")
    finally:
        cursor.close()
        connection.close()

def get_hiring_data_grouped_by_gender_department():
    """Retrieve employee counts grouped by department and gender"""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        query = """
        SELECT 
            department,
            gender,
            COUNT(*) as employee_count
        FROM employee_metrics
        WHERE department IS NOT NULL 
        AND gender IS NOT NULL
        GROUP BY department, gender
        ORDER BY department, gender
        """
        cursor.execute(query)
        return cursor.fetchall()
    except Error as e:
        raise Exception(f"Error retrieving hiring data: {e}")
    finally:
        cursor.close()
        connection.close()
