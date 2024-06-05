from openai import OpenAI
from dotenv import load_dotenv
import os
import pandas as pd
import xml.etree.ElementTree as ET 
import time

load_dotenv() # Load API key and folder with opinionsfrom .env file

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) # Create a client
assistant = client.beta.assistants.retrieve("asst_0iou8ThB7VJSfzPTrevJb9DM") # Previously created assisstant
TEI_NAMESPACES = {"tei": "http://www.tei-c.org/ns/1.0"}


def call_assistant(xml_string : str):
    thread = client.beta.threads.create()

    message = client.beta.threads.messages.create(thread_id=thread.id, role="user", content=xml_string)
    time.sleep(2) # sleep for 2s not to exceed the rate limit

    run = client.beta.threads.runs.create_and_poll(thread_id=thread.id,assistant_id=assistant.id,)

    print("Run completed with status: " + run.status)
    if run.status == "failed":
        return None

    if run.status == "completed":
        messages = client.beta.threads.messages.list(thread_id=thread.id)

        for message in messages:
            assert message.content[0].type == "text"
            if message.role == "assistant": # take the last response from the assistant
                response = message.content[0].text.value
                break

        return response


data_info = pd.read_csv('../outputs/data_info.csv')
data_tuples = zip(data_info['question'], data_info['group'], data_info['type'])

root_dir = os.getenv("OPINIONS_FOLDER ") #directory where the data is stored
extracted_tables = []

for data_tuple in data_tuples:
    specifications = []
    if data_tuple[2] != 'opinion': # we only want opinions, not guidances etc.
        continue
    question_path = os.path.join(root_dir, data_tuple[0])
    for root, _, files in os.walk(question_path):
        for file in files:
            if file.endswith('.tei.xml'):
                tei_file = ET.parse(os.path.join(root, file)).getroot()
                tables = tei_file.findall(".//tei:figure[@type='table']", TEI_NAMESPACES)
                for table in tables:
                    table_text = "".join(table.itertext())
                    if 'specifications' in table_text.lower() and 'batch' not in table_text.lower():
                        table_object = table.find('.//tei:table', TEI_NAMESPACES)
                        # get all the text from the table object, in xml format
                        table_xml = ET.tostring(table_object, encoding='unicode')
                        # call GPT to process it
                        result = call_assistant(table_xml)
                        if result is None or result == '[]':
                            continue
                        else:
                            elements = result.replace('`', '').replace('python', '').split(';')
                            for element in elements:
                                specifications.append(element.strip().replace('"', ''))
                            break # break the loop, we found the table


    if len(specifications) > 1: #if its only one, its the empty specification
        df = pd.DataFrame({'EFSA Q number': [data_tuple[0]] * len(specifications), 'Parameter': specifications})
        df.to_csv(f'../outputs/specifications/{data_tuple[0]}.csv', index=False)
        extracted_tables.append(df)
    
print(f'total extracted tables: {len(extracted_tables)}')
