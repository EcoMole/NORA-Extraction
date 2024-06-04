from openai import OpenAI
from dotenv import load_dotenv
import os
import json
load_dotenv() # Load API key from .env file

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) # Create a client

thread = client.beta.threads.create()

assistant = client.beta.assistants.retrieve("asst_0iou8ThB7VJSfzPTrevJb9DM") # Previously created assisstant


test_xml = """<figure xmlns="http://www.tei-c.org/ns/1.0" type="table" xml:id="tab_4" coords="8,70.87,296.86,434.96,230.76">
<head>Table 2 :</head>
<label>2</label>
<figDesc>
<div>
<p>
<s coords="8,124.78,296.86,103.20,9.30;8,73.87,316.80,386.08,8.37">Specifications of the NFDescription: Hydroalcoholic extract from a dried whole plant of Labisia pumila (Blume) Fern.-Vill.</s>
<s coords="8,462.95,316.80,42.88,8.37;8,73.87,327.80,170.78,8.37">mixed with maltodextrin (as a drying aid) in a ratio 2:1</s>
</p>
</div>
</figDesc>
<table coords="8,73.87,344.35,347.08,183.26">
<row>
<cell>Parameter</cell>
<cell>Specifications</cell>
</row>
<row>
<cell>Particle size</cell>
<cell>90% through 120 mesh (125 lm)</cell>
</row>
<row>
<cell>Ash</cell>
<cell>< 10%</cell>
</row>
<row>
<cell>Acid-insoluble ash</cell>
<cell>< 1%</cell>
</row>
<row>
<cell>Moisture</cell>
<cell>< 8%</cell>
</row>
<row>
<cell>Ethanol</cell>
<cell>< 1% (w/w)</cell>
</row>
<row>
<cell>Gallic acid</cell>
<cell>2-10% (w/w)</cell>
</row>
<row>
<cell>Carbohydrate</cell>
<cell>70-90 g/100 g</cell>
</row>
<row>
<cell>Protein</cell>
<cell>< 9% (w/w)</cell>
</row>
<row>
<cell>Total fat</cell>
<cell>< 3% (w/w)</cell>
</row>
<row>
<cell>Saponin (as ardisiacripsin A)</cell>
<cell>< 1.5% (w/w)</cell>
</row>
<row>
<cell>Aerobic plate count</cell>
<cell>< 1 9 10 4 CFU/g</cell>
</row>
<row>
<cell>Yeast and mould</cell>
<cell>< 5 9 10 2 CFU/g</cell>
</row>
<row>
<cell>E. coli</cell>
<cell/>
</row>
</table>
</figure> """


message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=test_xml,
)

run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id,
)

print("Run completed with status: " + run.status)

if run.status == "completed":
    messages = client.beta.threads.messages.list(thread_id=thread.id)

    print("messages: ")
    for message in messages:
        assert message.content[0].type == "text"
        #print({"role": message.role, "message": message.content[0].text.value})
        if message.role == "assistant": #return a json 
            response = message.content[0].text.value
            print("Assistant response: " + response)

    #client.beta.assistants.delete(assistant.id)