from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key

# Load CSV to determine fields
csv_path = 'employee_promotion.csv'
df = pd.read_csv(csv_path)

# Extract column names and generate options for dropdowns if they exist
columns = df.columns
options = {}
for column in columns:
    if df[column].dtype == 'object':
        options[column] = df[column].unique().tolist()

@app.route('/', methods=['GET', 'POST'])
def employee_form():
    if request.method == 'POST':
        # Extract form data and validate
        form_data = {}
        errors = []
        for column in columns:
            value = request.form.get(column)
            if value is None or value.strip() == "":
                errors.append(f"{column} is required.")
            else:
                form_data[column] = value

        if errors:
            for error in errors:
                flash(error)
            return redirect(url_for('employee_form'))

        # Placeholder to demonstrate capturing the input
        flash("Form data submitted successfully!")
        print(form_data)  # Future: store in DB or send to AI model

        return redirect(url_for('employee_form'))

    return render_template('employee_form.html', columns=columns, options=options)

if __name__ == '__main__':
    app.run(debug=True)