import csv
from lxml import etree
import pandas as pd

# XML file path
xml_file_path = 'All-MasterArt.xml'

parser = etree.XMLParser(remove_blank_text=True)
tree = etree.parse(xml_file_path, parser)

namespaces = {
    "stDsp": "http://ns.adobe.com/xap/1.0/sType/FileDisposition#",
    "xwnvtmp": "http://ns.xinet.com/ns/xwnvtmp#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
}

# The fields to be collected
fields_to_extract = [
    'xwnvtmp:Contributor',
    'xwnvtmp:Format_Code',
    'xwnvtmp:Client_Code',
    'xwnvtmp:Product_Code',
    'xwnvtmp:Job_Number',
    'xwnvtmp:More_Info',
    'xwnvtmp:Original_Files_and_Source/rdf:Bag/rdf:li',
]

field_map = {fieldname.split(":")[-1]: fieldname for fieldname in fields_to_extract}

def parse_description(description):
    # Derive filename from the URL in the rdf:about field
    rdf_about = description.attrib['{{{}}}about'.format(namespaces['rdf'])]
    filename_url = rdf_about.split('/')[-1].rstrip('#')
    # Find filename in the XML fields, if it's available
    filename_xml = description.find('stDsp:filename', namespaces)
    filename = filename_xml.text if filename_xml is not None else filename_url
    desc_data = {'filename': filename}
    
    for field, xpath in field_map.items():
        elem = description.find(xpath, namespaces)
        desc_data[field] = elem.text if elem is not None else None

    return desc_data

description_data = [parse_description(desc) for desc in tree.xpath("//rdf:Description", namespaces=namespaces)]
df = pd.DataFrame(description_data)

# Perform aggregations on data
aggregations = {field: lambda x: next((i for i in x if i is not None), None) for field in field_map.keys()}
df = df.groupby('filename', sort=False).agg(aggregations).reset_index()

# Change column name 'li' to 'Original_Files_and_Source'
df.rename(columns={'li': 'Original_Files_and_Source'}, inplace=True)

# Save data to CSV
df.to_csv('output.csv', index=False)