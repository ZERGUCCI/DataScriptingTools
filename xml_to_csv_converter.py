import csv
import xml.sax
from xml.sax.handler import ContentHandler

class XMLtoCSVHandler(ContentHandler):
    def __init__(self):
        super().__init__()
        self.buffer = ''
        self.current_tag = ''
        self.record = {}
        self.all_records = []  # List to keep all records
        self.all_tags = set()  # Set to keep all unique tags

    def startElement(self, name, attrs):
        self.current_tag = name
        if name == 'rdf:Description':
            self.record = {}  # Starting a new record
        self.buffer = ''  # Clear the character buffer

    def characters(self, content):
        self.buffer += content.strip()

    def endElement(self, name):
        if name != 'rdf:Description' and self.buffer:
            self.record[name] = self.buffer
            self.all_tags.add(name)  # Add the tag to the set of all unique tags
        elif name == 'rdf:Description':
            self.all_records.append(self.record)  # Add the record to our list

        self.current_tag = ''  # Clear the current tag
        self.buffer = ''  # Clear the character buffer

def main(xml_file_path, csv_file_path):
    # Creating an XML parser
    handler = XMLtoCSVHandler()
    parser = xml.sax.make_parser()
    parser.setContentHandler(handler)

    # Parsing the XML file
    with open(xml_file_path, 'r') as xml_file:
        parser.parse(xml_file)

    # Now, we write to the CSV, now that we have all unique fieldnames and records
    with open(csv_file_path, 'w', newline='') as csv_file:
        headers = list(handler.all_tags)  # Convert set to list to use as fieldnames
        csv_writer = csv.DictWriter(csv_file, fieldnames=headers, extrasaction='ignore')  # Ignore extra values
        csv_writer.writeheader()
        for record in handler.all_records:
            csv_writer.writerow(record)

if __name__ == "__main__":
    # Replace 'your_file.xml' with the path to your XML file
    xml_file_path = 'All-MasterArt.xml'
    # The resulting CSV file will be saved with this name
    csv_file_path = 'output.csv'

    main(xml_file_path, csv_file_path)