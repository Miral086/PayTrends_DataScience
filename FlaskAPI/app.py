from flask import Flask, render_template, request, jsonify
import mysql.connector
import pandas as pd
import pickle
import json

app = Flask(__name__)

# Establish connection to your XAMPP server
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="paytrends_ds"
)

def load_models():
    file_name = "D:\ResumeThings\PayTrends_DataScience\FlaskAPI\models\model_file.p"
    with open(file_name, 'rb') as pickled:
        data = pickle.load(pickled)
        model = data['model']
    return model


@app.route('/')
def index():
    # Fetch the list of company names from the database
    cursor = db.cursor()
    cursor.execute("SELECT name FROM company_details")
    companies = [row[0] for row in cursor.fetchall()]
    cursor.close()

    return render_template('index.html', companies=companies)

@app.route('/get_details', methods=['POST'])
def get_details():
    company = request.form['company']

    # Fetch company details from the database based on the selected company
    cursor = db.cursor()
    cursor.execute("SELECT rating, size, ownership, revenue, sector, industry FROM company_details WHERE name = %s", (company,))
    details = cursor.fetchone()
    cursor.close()

    details_dict = {
        "rating": details[0],
        "size": details[1],
        "ownership": details[2],
        "revenue": details[3],
        "sector": details[4],
        "industry": details[5]
    }

    return jsonify(details=details_dict)

@app.route('/predict', methods=['POST'])
def predict():
    columns = ['Rating', 'excel', 'nosql', 'desc_len', 'Location_Ahmedabad', 'Location_Badarpur', 'Location_Bengaluru', 'Location_Bharūch', 'Location_Chennai', 'Location_Daryā Ganj', 'Location_Gāndhīnagar', 'Location_Haveli', 'Location_Hyderābād', 'Location_Janakpuri', 'Location_Kalyan', 'Location_Mumbai', 'Location_Navi Mumbai', 'Location_New Delhi', 'Location_Patel Nagar', 'Location_Pitampura', 'Location_Pune', 'Location_Rājkot', 'Location_Secunderābād', 'Location_Surat', 'Location_Thāne', 'Location_Vadodara', 'Size_-1', 'Size_1 to 50 ', 'Size_10000+ ', 'Size_1001 to 5000 ', 'Size_201 to 500 ', 'Size_5001 to 10000 ', 'Size_501 to 1000 ', 'Size_51 to 200 ', 'Type of ownership_contract', 'Type of ownership_government', 'Type of ownership_na', 'Type of ownership_private', 'Type of ownership_public', 'Type of ownership_self-employed', 'Type of ownership_subsidiary', 'Type of ownership_university', 'Industry_-1', 'Industry_Accounting & Tax', 'Industry_Advertising & Public Relations', 'Industry_Aerospace & Defence', 'Industry_Architectural & Engineering Services', 'Industry_Banking & Lending', 'Industry_Beauty & Wellness', 'Industry_Biotech & Pharmaceuticals', 'Industry_Broadcast Media', 'Industry_Building & Personnel Services', 'Industry_Business Consulting', 'Industry_Chemical Manufacturing', 'Industry_Civic, Welfare & Social Services', 'Industry_Colleges & Universities', 'Industry_Commercial Equipment Services', 'Industry_Computer Hardware Development', 'Industry_Consumer Product Manufacturing', 'Industry_Department, Clothing & Shoe Stores', 'Industry_Education Support & Training Services', 'Industry_Electronics Manufacturing', 'Industry_Energy & Utilities', 'Industry_Enterprise Software & Network Solutions', 'Industry_Film Production', 'Industry_Financial Transaction Processing', 'Industry_Food & Beverage Manufacturing', 'Industry_General Merchandise & Superstores', 'Industry_Grantmaking & Charitable Foundations', 'Industry_HR Consulting', 'Industry_Healthcare Services & Hospitals', 'Industry_Home Furniture & Housewares Stores', 'Industry_Information Technology Support Services', 'Industry_Insurance Agencies & Brokerages', 'Industry_Insurance Carriers', 'Industry_Internet & Web Services', 'Industry_Investment & Asset Management', 'Industry_Legal', 'Industry_Machinery Manufacturing', 'Industry_Metal & Mineral Manufacturing', 'Industry_National Services & Agencies', 'Industry_Other Retail Shops', 'Industry_Publishing', 'Industry_Real Estate', 'Industry_Research & Development', 'Industry_Security & Protective', 'Industry_Software Development', 'Industry_Sports & Recreation', 'Industry_Staffing, Recruitment & Subcontracting', 'Industry_Stock Exchanges', 'Industry_Taxi & Car Services', 'Industry_Telecommunications Services', 'Industry_Ticket Sales', 'Industry_Transportation Equipment Manufacturing', 'Sector_-1', 'Sector_Aerospace & Defence', 'Sector_Arts, Entertainment & Recreation', 'Sector_Construction, Repair & Maintenance Services', 'Sector_Education', 'Sector_Energy, Mining, Utilities', 'Sector_Finance', 'Sector_Government & Public Administration', 'Sector_Healthcare', 'Sector_Human Resources & Staffing', 'Sector_Information Technology', 'Sector_Insurance', 'Sector_Legal', 'Sector_Management & Consulting', 'Sector_Manufacturing', 'Sector_Media & Communication', 'Sector_Non-profit & NGO', 'Sector_Personal Consumer Services', 'Sector_Pharmaceutical & Biotechnology', 'Sector_Real Estate', 'Sector_Retail & Wholesale', 'Sector_Telecommunications', 'Sector_Transportation & Logistics', 'Revenue_$1 to $5 million (USD)', 'Revenue_$10+ billion (USD)', 'Revenue_$100 to $500 million (USD)', 'Revenue_$2 to $5 billion (USD)', 'Revenue_$25 to $50 million (USD)', 'Revenue_$5 to $10 billion (USD)', 'Revenue_$5 to $25 million (USD)', 'Revenue_$500 million to $1 billion (USD)', 'Revenue_-1', 'Revenue_Less than $1 million (USD)', 'Revenue_na', 'Job_simpler_analyst', 'Job_simpler_data engineer', 'Job_simpler_data scientist', 'Job_simpler_manager', 'Job_simpler_mle', 'Job_simpler_na', 'seniority_junior', 'seniority_na', 'seniority_senior']
    # Initialize the dataframe with zeros
    df = pd.DataFrame(0, columns=columns, index=[0])
    # print(df)
    rating = float(request.form['rating'])
    size = request.form['size']
    ownership = request.form['ownership']
    revenue = request.form['revenue']
    sector = request.form['sector']
    industry = request.form['industry']
    job_title = request.form['job_title']
    location = request.form['location']
    description = request.form['description']
    skills = request.form.getlist('skills[]')
    # print(size+'hello')
    # Replace the columns with user input
    df['Revenue_' + revenue] = 1
    df['Sector_' + sector] = 1
    df['Rating'] = rating
    df['desc_len'] = len(description)
    df['Location_' + location] = 1
    df['Size_' + size] = 1
    df['Type of ownership_' + ownership] = 1
    df['Industry_' + industry] = 1
    df['Job_simpler_' + job_title] = 1
    
    for skill in skills:
        print(skill)
        if(skill == 'excel' or skill == 'nosql'):
            df[skill] = 1
    
    # print(df)
    # Perform further processing with the dataframe as needed
    model = load_models()
    prediction = model.predict(df)
    output = round(prediction[0], 2)
    # Return the predicted value
    return jsonify(prediction=output)

    # return 'yes'
   

if __name__ == '__main__':
    app.run()

