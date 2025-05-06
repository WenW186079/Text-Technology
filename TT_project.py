import json
import re
import pandas as pd
import json
import xml.etree.ElementTree as ET
from lxml import etree

def convert_csv_to_json(df):
    df = df.drop(columns=['job description'])
    df.to_json(r'tt_project_data_og.json',orient='records')


def classify_company_size(size):
    if size in ["1 to 50 Employees", "51 to 200 Employees"]:
        return "XS"
    elif size in ["201 to 500 Employees", "501 to 1000 Employees"]:
        return "S"
    elif size in ["1001 to 5000 Employees", "5001 to 10000 Employees"]:
        return "M"
    elif size == "10000+ Employees":
        return "L"
    else:
        return size   
    
def modify_data():

    with open('tt_project_data_og.json') as file:
        data = json.load(file)

    state_codes = {
        'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California',
        'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia',
        'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa',
        'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
        'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri',
        'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey',
        'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio',
        'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
        'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont',
        'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming',
        'AS': 'American Samoa', 'DC': 'District of Columbia', 'FM': 'Federated States of Micronesia',
        'GU': 'Guam', 'MH': 'Marshall Islands', 'MP': 'Northern Mariana Islands', 'PW': 'Palau',
        'PR': 'Puerto Rico', 'VI': 'Virgin Islands'
    }

    for document in data:
        salary_estimate = document.get('salary estimate')


        if salary_estimate is not None:
            if '/yr' in salary_estimate:
                # Extract the salary value from the string
                salary_value = re.sub(r'[^0-9]', '', salary_estimate)
            
                if salary_value:
                    # Convert the salary to a number and divide by 12
                    monthly_salary = int(salary_value) / 12
                    document['salary estimate'] = monthly_salary

            elif '/hr' in salary_estimate:
                # Extract the salary value from the string
                salary_value = re.sub(r'[^0-9]', '', salary_estimate)
                if salary_value:
                    # Convert the salary to a number and multiply by 168
                    monthly_salary = int(salary_value) * 168
                    document['salary estimate'] = monthly_salary

            elif '/mo' in salary_estimate:
                # Extract the salary value from the string
                salary_value = re.sub(r'[^0-9]', '', salary_estimate)
                if salary_value:
                    # Convert the salary to a number
                    monthly_salary = int(salary_value)
                    document['salary estimate'] = monthly_salary


            
    for item in data:
        if 'salary estimate' in item:
            item['monthly_salary'] = item.pop('salary estimate')

        if 'company' in item:
            item['company'] = item['company'].strip('\n')
        
        if 'company_size' in item:
            item['company_size'] = classify_company_size(item['company_size'])
        
        if 'Unnamed: 0' in item:
            item['number'] = item.pop('Unnamed: 0')
        
        if 'job title' in item:
            item['job_title'] = item.pop('job title')

        job_title = item["job_title"].lower()

        if "jr." in job_title or "junior" in job_title or "junior" in job_title.lower():
            item["experience_level"] = "Junior"
        elif "senior" in job_title:
            item["experience_level"] = "Senior"
        else:
            item["experience_level"] = None

        if "software" in job_title:
            item["job_title"] = "Software engineer"
        elif "data" in job_title:
            item["job_title"] = "Data Scientist"
        elif "machine" in job_title:
            item["job_title"] = "Machine Learning engineer"
        
    for document in data:
        # Check if the location is not null and contains a comma
        location = document.get('location')

        # Check if the location is not null and contains a state code
        if location is not None and location[-2:] in state_codes:
            # Update the location with the corresponding state name
            document['location'] = state_codes[location[-2:]]

    # Filter out data with null monthly_salary
    data = [document for document in data if document.get('monthly_salary') is not None]

    with open('tt_project_data_modified.json', 'w') as file:
        json.dump(data, file, indent=4)


# Helper function to convert JSON data to XML
def json_to_xml(element, data):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "$oid":
                key = "oid"
                
            if isinstance(value, dict) or isinstance(value, list):
                sub_element = ET.SubElement(element, key)
                json_to_xml(sub_element, value)
            else:
                sub_element = ET.SubElement(element, key)
                sub_element.text = str(value)
    elif isinstance(data, list):
        for item in data:
            sub_element = ET.SubElement(element, 'item')
            json_to_xml(sub_element, item)

def encode_xml():
    with open('tt_project_data_modified.json', 'r') as file:
        data = json.load(file)

    root = ET.Element('data')

    json_to_xml(root, data)

    tree = ET.ElementTree(root)

    tree.write('tt_project_data.xml', encoding='utf-8', xml_declaration=True)

def creating_xslt_file():
    xslt_stylesheet = '''<?xml version="1.0" encoding="UTF-8"?>
    <xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <html>
        <head>
            <title>Job Listings</title>
            <style>
            body {
                font-family: Arial, sans-serif;
            }
            h1 {
                color: #333;
            }
            table {
                border-collapse: collapse;
                width: 100%;
            }
            th, td {
                padding: 10px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }
            th {
                background-color: #f2f2f2;
            }
            .logo {
                max-width: 80px;
                max-height: 80px;
            }
            </style>
        </head>
        <body>
            <h1>Job Listings</h1>
            <table>
            <tr>
                <th>Company</th>
                <th>Location</th>
                <th>Company Size</th>
                <th>Company Type</th>
                <th>Company Sector</th>
                <th>Company Industry</th>
                <th>Company Founded</th>
                <th>Company Revenue</th>
                <th>Monthly Salary</th>
                <th>Number</th>
                <th>Job Title</th>
                <th>Experience Level</th>
            </tr>
            <xsl:for-each select="data/item">
                <tr>
                <td><xsl:value-of select="company"/></td>
                <td><xsl:value-of select="location"/></td>
                <td><xsl:value-of select="company_size"/></td>
                <td><xsl:value-of select="company_type"/></td>
                <td><xsl:value-of select="company_sector"/></td>
                <td><xsl:value-of select="company_industry"/></td>
                <td><xsl:value-of select="company_founded"/></td>
                <td><xsl:value-of select="company_revenue"/></td>
                <td><xsl:value-of select="monthly_salary"/></td>
                <td><xsl:value-of select="number"/></td>
                <td><xsl:value-of select="job_title"/></td>
                <td><xsl:value-of select="experience_level"/></td>
                </tr>
            </xsl:for-each>
            </table>
        </body>
        </html>
    </xsl:template>
    </xsl:stylesheet>
    '''
    xslt_filename = 'tt_project_data.xslt'
    with open(xslt_filename, 'w') as f:
        f.write(xslt_stylesheet)

    print(f"XSLT file '{xslt_filename}' created successfully.")

def apply_xslt():
    xml_file = "tt_project_data.xml"
    xslt_file = "tt_project_data.xslt"
    output_file = "tt_project_data.html"

    xml_doc = etree.parse(xml_file)
    xslt_doc = etree.parse(xslt_file)

    transformer = etree.XSLT(xslt_doc)

    result_tree = transformer(xml_doc)

    result_tree.write(output_file, pretty_print=True)

if __name__ == "__main__":
    
    df = pd.read_csv('machine_learning_engineer.csv')

    convert_csv_to_json(df)
    print('convert_csv_to_json done')

    modify_data()
    print('modify_data done')

    encode_xml()
    print('encode_xml done')

    creating_xslt_file()
    print('creating_xslt_file done')
    
    apply_xslt()
    print('apply_xslt done')
