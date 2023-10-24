import os
import csv
import xml.etree.ElementTree as ET

def parse_and_write(xml_file, original_csv_file, cleaned_csv_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Create a list to store all records
    all_records = []
    headers = []  # Using a list to preserve order

    for description in root.findall('.//{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Description'):
        record = {}
        for elem in description:
            # Keeping the full tag including namespace for the original CSV
            record[elem.tag] = elem.text if elem.text else 'NULL'
            # Add to headers if it's not already there
            if elem.tag not in headers:
                headers.append(elem.tag)
        all_records.append(record)

    # Write records to the original CSV
    with open(original_csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for record in all_records:
            writer.writerow(record)

    # Clean headers for the cleaned-up CSV
    clean_headers = [tag.split('}')[-1] for tag in headers]  # Preserving order

    # Adjust records for the cleaned-up CSV
    cleaned_records = []
    for record in all_records:
        cleaned_record = {tag.split('}')[-1]: value for tag, value in record.items()}
        cleaned_records.append(cleaned_record)

    # Write records to the cleaned-up CSV
    with open(cleaned_csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=clean_headers)  # Here we use the ordered headers
        writer.writeheader()
        for record in cleaned_records:
            writer.writerow(record)

# Replace with your file paths
xml_file_path = 'All-MasterArt.xml'
original_csv_file_path = 'output.csv'
cleaned_csv_file_path = 'cleaner_output.csv'

parse_and_write(xml_file_path, original_csv_file_path, cleaned_csv_file_path)
