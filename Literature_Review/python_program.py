# %% [markdown]
# # PaperQA - A Question Answering Dataset for Academic Papers

# %%
api_key = "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"
import os
# Set up the environment and PaperQA
os.environ['OPENAI_API_KEY'] = api_key
!pip install paper-qa
#!pip install openai==1.7.2
!pip install openai==0.28
!pip install langchain==0.1.1
import nest_asyncio
nest_asyncio.apply()
import os
import json
from paperqa import Docs
!pip install sentence-transformers
api_key = "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"
import os
from re import T
os.environ['OPENAI_API_KEY'] = api_key
import nest_asyncio
nest_asyncio.apply()
import langchain
from langchain.cache import InMemoryCache
#model_name = "ggrn/e5-small-v2" # fast
model_name = "WhereIsAI/UAE-Large-V1" # slow
model_kwargs = {'device': 'cpu'}
from langchain.embeddings import HuggingFaceEmbeddings
TOKENIZERS_PARALLELISM=True
embeddings = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs)
# Configuration
#output_folder = "/home/epas/Programming/ResearchAgentSwarm/Literature_Review/json_summaries/"
output_folder_json = "/Users/tomriddle1/Documents/GitHub/ResearchAgentSwarm/Literature_Review/Chemical_Structure_json/" 
output_folder_pdf = "/Users/tomriddle1/Documents/GitHub/ResearchAgentSwarm/Literature_Review/Chemical_Structure_pdf/" 
questions_file_path = "questions_file.txt"
responses_file_path = "responses_file.txt"

docs = Docs(llm='gpt-3.5-turbo', openai_api_key=api_key, embeddings=embeddings)


def process_json_files(folder):
    json_files = os.listdir(folder)
    json_files = [file for file in json_files if file.endswith('.json')]

    for filename in json_files:
        with open(os.path.join(folder, filename), 'r') as file_obj:
            data = json.load(file_obj)
            
            # Check if the JSON data is not empty
            if data:
                citation = ""
                for entry in data:
                    file_id = str(entry["file_id"])
                    citation = str(entry["references"])
                
                # Check if file_id and citation are not empty
                if file_id:
                    docs.add(path=os.path.join(folder, filename), dockey=file_id)
            else:
                print(f"Skipped empty or invalid JSON file: {filename}")

def process_research_papers(folder):
    research_papers = os.listdir(folder)
    research_papers = [file for file in research_papers if file.endswith('.pdf')]
    for filename in research_papers:
        docs.add(path=os.path.join(folder, filename))
            

def read_questions(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

def write_responses(responses, file_path):
    with open(file_path, 'w') as file:
        for response in responses:
            file.write(response.formatted_answer + "\n\n")


# Rest of your main function...

def main():
    process_json_files(output_folder_json)
    process_research_papers(output_folder_pdf)
    questions = read_questions(questions_file_path)
    responses = [docs.query(question) for question in questions]
    write_responses(responses, responses_file_path)

if __name__ == "__main__":
    main()


# %%
#!pip install git+https://github.com/blackadad/paper-scraper.git



# %%
!pip uninstall openai -y
!pip uninstall paperqa -y
!pip install openai==0.28

# %%
import json
import re
import datetime
def extract_urls(reference_text):
    # Regular expression pattern for identifying URLs
    url_pattern = re.compile(r'https?://[^\s,]+')
    urls = url_pattern.findall(reference_text)
    return urls
def parse_qa_responses(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    responses = []
    response = {}
    references_lines = []
    capturing_references = False

    for line in lines:
        if line.startswith('Question:'):
            if response:  # Add the previous response with its references to the list
                response['references'] = ''.join(references_lines).strip()
                responses.append(response)
                references_lines = []
            # Handling split operation
            split_line = line.split('    ')
            if len(split_line) >= 2:
                response = {'question': split_line[1].strip(), 'answer': '', 'references': ''}
            else:
                response = {'question': '', 'answer': '', 'references': ''}
            capturing_references = False
        elif 'I cannot answer' in line.strip() or 'The provided context does not contain' in line.strip():
            response['answer'] = line.strip()
        elif line.strip().startswith('References'):
            capturing_references = True
        elif capturing_references:
            references_lines.append(line)
    
    if response:  # Add the last response with its references to the list
        response['references'] = ''.join(references_lines).strip()
        responses.append(response)

    # Add timestamp and extract URLs from references
    for response in responses:
        response["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if response['references']:
            response['references_urls'] = extract_urls(response['references'])
    return responses


# You would then continue with your original code for saving the JSON.


def save_json_append(responses, output_file):
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    combined_data = existing_data + responses

    with open(output_file, 'w') as f:
        json.dump(combined_data, f, indent=4)

file_path ="responses_file.txt"
output_json_file = 'structured_responses.json'

responses = parse_qa_responses(file_path)
save_json_append(responses, output_json_file)

print(f"Processed responses are saved in JSON format to {output_json_file}")


# %%
import pickle
laptop= "/home/epas/Documents/docs.pickle"
desktop = "/Users/tomriddle1/Documents/GitHub/docs.pickle"
# save
with open(desktop, "wb") as f:
    pickle.dump(docs, f)

# load
with open(desktop, "rb") as f:
    docs = pickle.load(f)

# %%
def build_system_prompt(prompt_type: str):
    # read from file "entity_dense_prompt.md"
    if prompt_type == "Enitity Dense":
        with open("entity_dense_prompt.md", "r") as f:
            system_prompt = f.read()
    if prompt_type == "SPR":
        with open("sparse_prime_representation.md", "r") as f:
            system_prompt = f.read()
    if prompt_type == "Get Entities":
        with open("get_entities.md", "r") as f:
            system_prompt = f.read()
    if prompt_type == "Get Topic":
        with open("get_topic.md", "r") as f:
            system_prompt = f.read()
    if prompt_type == "Get Hypothetical Questions":
        with open("get_hypothetical_questions.md", "r") as f:
            system_prompt = f.read()
    if prompt_type == "Get Knowledge":
        with open("get_knowlege_graph_triples.md", "r") as f:
            system_prompt = f.read()
    if prompt_type == "Generate Search Queries":
        with open("generate_search_queries.md", "r") as f:
            system_prompt = f.read()
    return f"{system_prompt}"

def parse_response(response):

    # Get the text content from the single completion 
    completion = response.choices[0]
    text = completion.message.content

    # Remove unnecessary newlines and whitespace    
    text = text.strip()  

    # Could add additional parsing logic here 

    return text

# %%
#!pip install pydantic==2.0.3
!pip install instructor
#
from datetime import datetime
from pydantic import BaseModel, Field

import os
import json
import instructor
from openai import OpenAI

import re
from typing import List

# %%
api_key = "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"
import os
!pip install openai==0.28
# Set up the environment and PaperQA
os.environ['OPENAI_API_KEY'] = api_key
import json
#import instructor

from datetime import datetime
import os
import json



api_key = "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"
import openai


def generate_search_queries(question: str):
    prompt = build_system_prompt("Generate Search Queries")
    prompt += f"Question: {question}\n"

    # Initialize the OpenAI client without explicitly passing the API key
    #client = OpenAI(api_key=api_key)

    try:
        response =  openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": "Search Queries:"},
            ]
        )
        return parse_response(response)
    except Exception as e:
        print(f"Error: {e}")
        return None

def check_unanswered_questions(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    unanswered_questions = []

    for entry in data:
        # Checking for phrases that indicate an unanswered question
        if "cannot answer" in entry["answer"] or "does not contain" in entry["answer"] or "no answer" in entry["answer"] or "no results" in entry["answer"] or "no information" in entry["answer"]:
            unanswered = True
        else:
            unanswered = False

        # Building the result entry
        result_entry = {
            "question": entry["question"],
            "answerable": not unanswered,
            "timestamp": entry.get("timestamp", "Unknown timestamp")
        }

        if entry.get("references"):
            result_entry["references"] = entry["references"]

        if entry.get("references_urls"):  # Using .get to avoid KeyError
            result_entry["references_urls"] = entry["references_urls"]

        unanswered_questions.append(result_entry)

    return unanswered_questions

json_file = 'structured_responses.json'
unanswered_questions = check_unanswered_questions(json_file)

# Display the results
for item in unanswered_questions:
    print(f"Question: {item['question']}\nAnswerable: {item['answerable']}\n")
    if item.get("references") and item.get("references_urls"):
        print(f"Url(s): {item['references_urls']}\n")
        #print(f"Reference(s): {item['references']}\n")
    # Generate search queries for unanswered questions
    if item['answerable'] == False:
        if item.get("references"):
            search_queries = generate_search_queries(f"{item['question']}\n{item['references']}")
        else:
            search_queries = generate_search_queries(item["question"])
        # save search queries to json file
        with open("search_queries.json", "a") as outfile:
            json.dump(search_queries, outfile)
        print(f"Search Queries: {search_queries}\n")

# %%
import openai
from openai import OpenAI
import os
client = OpenAI(api_key= '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')

messages = [
    {"role":"system", "content": "You are a kind helpfull assistant"}
]

while True:
    message = input("user:")
    if message:
        messages.append(
            {"role":"user", "content": message},
        )
        completion = client.chat.completions.create(
            messages = messages,
            model = "gpt-3.5-turbo"
        )

    reply = completion.choices[0].message.content
    print(f"ChatGPT: {reply}")
    messages.append({"role": "assistant", "content": reply})

# %%


# %%
!pip install paper-qa
#!pip install git+https://github.com/blackadad/paper-scraper.git
!pip install sentence-transformers
#!pip install -U angle-emb
api_key = "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"
import os
from re import T
os.environ['OPENAI_API_KEY'] = api_key
import nest_asyncio
nest_asyncio.apply()
!pip install langchain
import langchain
from langchain.cache import InMemoryCache
langchain.llm_cache = InMemoryCache()
model_name = "ggrn/e5-small-v2" # fast
#model_name = "WhereIsAI/UAE-Large-V1" # slow
model_kwargs = {'device': 'cpu'}
from langchain.embeddings import HuggingFaceEmbeddings
TOKENIZERS_PARALLELISM=True
embeddings = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs)
!export DOI2PDF='https://sci-hub.ru/'
os.environ['DOI2PDF'] = 'https://sci-hub.ru/'
#os.environ["SEMANTIC_SCHOLAR_API_KEY"]

# %%
from re import M
from paperqa import Docs
import os

# Set the API key
api_key = "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"

# Optionally set the environment variable (if needed elsewhere)
os.environ['OPENAI_API_KEY'] = api_key

# Initialize Docs with the API key
#docs = Docs(llm='gpt-3.5-turbo', openai_api_key=api_key, memory=True, embeddings=embeddings)

# load the papers from Mitochondria Papers folder

mito_papers = os.listdir('/home/epas/Programming/ResearchAgentSwarm/Mitochondria Papers/')

for paper in mito_papers:
    #docs.add("Mitochondria Papers/"+paper, chunk_chars=2500)
    print(paper)




# %%

# Query and print the answer
answer = docs.query("What is the current understanding of the role of mitochondria in animal regeneration and aging, and what future research directions are being considered to harness these mechanisms for whole-body regeneration?")
print(answer.formatted_answer)

# %%
import pickle

# save
with open("MitochondrialPapers.pkl", "wb") as f:
    pickle.dump(docs, f)

# load
with open("MitochondrialPapers.pkl", "rb") as f:
    docs = pickle.load(f)

# %%
import os


from paperqa import Docs

try:
    docs = Docs(llm='gpt-3.5-turbo', openai_api_key=api_key)
    print("Initialization successful.")
except Exception as e:
    print(f"Initialization failed: {e}")


# %%
import paperscraper
# Set the API key
api_key = "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"

# Optionally set the environment variable (if needed elsewhere)
os.environ['OPENAI_API_KEY'] = api_key

# Initialize Docs with the API key
#docs = Docs(llm='gpt-3.5-turbo', openai_api_key=api_key)
import paperqa

keyword_search = 'bispecific antibody manufacture'
papers = paperscraper.search_papers(keyword_search)
docs = paperqa.Docs(openai_api_key=api_key)
for path,data in papers.items():
    try:
        #docs.add(path)
        print(path, data['title'])
    except ValueError as e:
        # sometimes this happens if PDFs aren't downloaded or readable
        print('Could not read', path, e)
answer = docs.query("What manufacturing challenges are unique to bispecific antibodies?")
print(answer)

# %%


# %%
import paperscraper
import nest_asyncio
nest_asyncio.apply()
papers = paperscraper.search_papers(query='bayesian model selection',
                                    limit=1,
                                    pdir='downloaded-papers')


# %%
!pip install nougat-ocr
#$ nougat path/to/file.pdf -o output_directory


# %%
!pip install transformers
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
#tokenizer = AutoTokenizer.from_pretrained("studio-ousia/luke-large")
#model = AutoModelForTokenClassification.from_pretrained("studio-ousia/luke-large")
tokenizer = AutoTokenizer.from_pretrained("dbmdz/electra-large-discriminator-finetuned-conll03-english")
model = AutoModelForTokenClassification.from_pretrained("dbmdz/electra-large-discriminator-finetuned-conll03-english")

nlp = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy='simple')
text = "Recent studies have shown that multilingual pretrained language models can be effectively improved with cross-lingual alignment information from entities."
ner_results = nlp(text)
print(ner_results)
# save to file txt
with open('ner_results.txt', 'w') as f:
    print(ner_results, file=f)


# %%
!nougat '/Users/tomriddle1/Documents/GitHub/ResearchAgentSwarm/Mitochondria Papers/izawa2017.pdf' -o "/Users/tomriddle1/Documents/GitHub/ResearchAgentSwarm/swarm_files"

# %% [markdown]
# # Create Research Summary

# %%
import json
import tempfile

# Function to clean entities based on new lines and remove leading hyphens
def clean_and_separate_entities(entities_list):
    entities_str = '\n'.join(entities_list)
    cleaned_entities = []
    dirty_entities = []

    for line in entities_str.split('\n'):
        stripped_line = line.strip()
        if stripped_line.startswith('-'):
            # Remove the leading hyphen and any extra space after it
            cleaned_entities.append(stripped_line.lstrip('-').strip())
        else:
            dirty_entities.append(stripped_line)

    return cleaned_entities, dirty_entities
def test_clean_and_separate_entities():
    
    # Define the summary JSON file path
    SUMMARY_JSON = "summaries.json"

    # Read the summaries.json file
    with open(SUMMARY_JSON, "r") as file:
        summaries_json = json.load(file)

    # Extract the first entities entry
    first_entities_list = summaries_json[0]["entities"][0]

    # Clean the entities and separate the uncleaned ones
    cleaned_entities, dirty_entities = clean_and_separate_entities(first_entities_list)

    # Save the results to a temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
        json.dump({
            "cleaned_entities": cleaned_entities,
            "dirty_entities": dirty_entities
        }, temp_file, indent=4)

    print("Results saved in:", temp_file.name)


# %%
import re
def extract_topics_with_justification(topic_text):
    # Regular expression pattern for identifying topics with their justifications
    topic_pattern = re.compile(r'(\d+)\.\s+([^\n]+)(\n\s+-[^\n]+)*')
    topics = topic_pattern.findall(topic_text)
    
    extracted_topics = []
    for match in topics:
        topic = match[1].strip()
        justification = ' '.join(match[2].split('\n')).strip()
        # Remove "Justification:" if it starts with it
        if justification.lower().startswith('- justification:'):
            justification = justification[len('- justification:'):].strip()
        # Remove the - if it starts with it
        if justification.startswith('-'):
            justification = justification[1:].strip()
        extracted_topics.append({"topic": topic, "justification": justification})

    return extracted_topics



def test_extract_topics_with_justification():
    # Adjusted topic text
    topic_text_list = []
    topic_text_list.append("**Topics Identified:**\n\n1. Importance of Mitochondria in Energy Production, Signaling, and Apoptosis\n   - Mitochondria as the powerhouse of the cell\n   - Role of mitochondria in energy production, signaling, and apoptosis\n   - Significance of studying mitochondrial function and involvement in diseases\n\n2. Challenges with Traditional Methods of Mitochondrial Isolation\n   - Limitations of traditional methods like differential centrifugation\n   - Potential damage to mitochondrial double membrane and variable viability\n\n3. Innovative Techniques for Mitochondrial Isolation\n   - Nitrogen cavitation for gentle disruption and release of intact mitochondria\n   - Affinity purification using anti-TOM22 magnetic beads for efficient isolation\n   - Filtration-based methods to reduce isolation time and improve viability\n   - Differential isopycnic density gradient centrifugation for separation based on buoyant density\n\n4. Quality Control Measures for Validating Mitochondrial Isolation\n   - Assessment of mitochondrial respiration, metabolic activity, protein import, and membrane fusion\n   - High-resolution respirometry and bioluminescent measurements of ATP synthesis\n\n5. Importance of Continued Refinement and Standardization of Techniques\n   - Advancing understanding of mitochondrial biology and implications in health and disease\n   - Need for standardized protocols to facilitate comparisons and translation of research findings into clinical applications\n\n**Notes**: The summary provides a comprehensive overview of the importance of mitochondria, challenges with traditional methods of isolation, innovative techniques for isolation, quality control measures, and the need for continued refinement and standardization. The topics cover the main ideas and themes discussed in the summary, providing a clear and comprehensive analysis of the content.") 
    topic_text_list.append("**Topic List:**\n\n1. Challenges in isolating intact mitochondria from plant cells\n   - Cell walls, mitochondrial membranes, and large amounts of starting material\n2. Comprehensive protocol for isolating intact mitochondria from plant cells\n   - Grinding, filtering, centrifuging, and resuspending\n3. Characterization and analysis of isolated mitochondria\n   - Purity, integrity, and functionality assessment\n   - Techniques: protein profiling, enzymatic activity assays, respiratory chain measurements, and oxygen consumption analysis\n4. Storage of purified mitochondria\n   - Long-term storage at -80°C\n5. Adaptation of isolation process for different tissue types and plant species\n   - Consideration of phenolic compounds and metabolite profiles\n6. Validation and controls for quality and functionality assurance\n7. Downstream applications of isolated mitochondria\n   - Protein and tRNA uptake experiments, enzyme activity assays, Western blot analyses, and mass spectrometry analyses\n\n**Notes:**\n- The revised summary provides a comprehensive overview of the topic, covering various aspects of isolating intact mitochondria from plant cells.\n- The topics are specific and non-repetitive, ensuring a clear and distinct representation of the core themes.\n- The summary is focused on the technical process and considerations involved in isolating mitochondria, as well as the analysis and applications of the isolated mitochondria.")
    topic_text_list.append("**Topics Identified:**\n\n1. Importance of mitochondrial research in understanding cellular biology and addressing diseases related to mitochondrial dysfunction\n    - Justification: The summary highlights the crucial role of mitochondrial research in understanding cellular biology and addressing diseases related to mitochondrial dysfunction.\n\n2. Significance of gentle and effective mitochondrial isolation techniques\n    - Justification: The summary emphasizes the importance of gentle and effective isolation techniques for studying mitochondrial biology and developing mitochondrial-based therapies.\n\n3. Overview of macroscale mitochondrial isolation techniques\n    - Justification: The summary discusses macroscale mitochondrial isolation techniques, such as manual homogenization and differential filtration-based isolation.\n\n4. Advancements in microscale and nanoscale mitochondrial isolation techniques\n    - Justification: The summary mentions microscale and nanoscale techniques, including microfluidic techniques and nanoprobe-based technologies, for mitochondrial isolation.\n\n5. Breakthroughs in sub-cellular isolation techniques for mitochondria\n    - Justification: The summary highlights breakthroughs in sub-cellular isolation techniques that enable the isolation of mitochondria from subcellular compartments with minimal disruption.\n\n6. Challenges in mitochondrial isolation techniques\n    - Justification: The summary mentions challenges such as the presence of whole cell contaminants in mitochondrial isolates and the time sensitivity of isolated mitochondria.\n\n7. Emerging therapeutic approach: Autologous mitochondrial transplants\n    - Justification: The summary discusses the development of autologous mitochondrial transplants as an emerging therapeutic approach.\n\n8. Contributions of the London Centre for Nanotechnology and the McCully laboratory\n    - Justification: The summary mentions the significant contributions of the London Centre for Nanotechnology and the McCully laboratory in optimizing differential filtration-based mitochondrial isolation for use in cellular models.\n\n9. Role of Stem Cell Research & Therapy in advancing mitochondrial medicine\n    - Justification: The summary highlights the role of Stem Cell Research & Therapy in providing in-depth overviews of advancements in mitochondrial research and facilitating the development of novel therapies for mitochondrial diseases.")
    topic_text_list.append("Topics:\n1. Genetic modifications to enhance mitochondrial autonomy\n   - Justification: The main focus of the report is exploring genetic modifications to enhance the autonomy of mitochondria from nuclear-encoded proteins and functions.\n2. Role of mitochondria in cellular function\n   - Justification: The report highlights the crucial role played by mitochondria in cellular function.\n3. Coordination between mtDNA and nuclear DNA\n   - Justification: The report discusses the coordination required between mtDNA and nuclear DNA, as most proteins are encoded by nuclear DNA.\n4. Therapeutic strategies for mitochondrial diseases\n   - Justification: The report mentions that enhancing mitochondrial autonomy could lead to new therapeutic strategies for mitochondrial diseases.\n5. Research on genome engineering, programmable nucleases, and base editors\n   - Justification: The report mentions that recent research in genome engineering, programmable nucleases, and base editors shows promise for treating hereditary mitochondrial diseases.\n6. Challenges in genetic manipulation of mtDNA\n   - Justification: The report discusses challenges such as mtDNA mutations, resistance to genetic manipulation, and limitations in mtDNA recombination.\n7. Advancements in protein-only gene editing platforms\n   - Justification: The report mentions advancements in protein-only gene editing platforms as potential solutions to the challenges in genetic manipulation of mtDNA.\n8. Somatic mitochondrial DNA-replaced cells\n   - Justification: The report mentions the generation of somatic mitochondrial DNA-replaced cells as a potential solution to the challenges in genetic manipulation of mtDNA.\n9. Mitochondrial nucleoids and their role in maintaining genetic autonomy\n   - Justification: The report highlights the concept of mitochondrial nucleoids and their role in maintaining genetic autonomy as a key area of study.\n10. Mitochondrial epigenomics and gene expression regulation\n    - Justification: The report emphasizes the importance of understanding mitochondrial epigenomics and gene expression regulation in different cellular contexts, including stress conditions, for identifying genetic modifications that could enhance mitochondrial autonomy.")
    for topic_text in topic_text_list:
        extracted_topics = extract_topics_with_justification(topic_text)
        print(f'Extracted topics: {extracted_topics}')



# %%
import re
#!pip install pdfx
import pdfx
#!pip install paperscraper
#import paperscraper
import nest_asyncio
nest_asyncio.apply()
import os
!export DOI2PDF='https://sci-hub.ru/'
os.environ['DOI2PDF'] = 'https://sci-hub.ru/'
def extract_urls(reference_text):
    # Regular expression pattern for identifying URLs
    url_pattern = re.compile(r'https?://[^\s,]+')
    urls = url_pattern.findall(reference_text)
    return urls


def test_extract_urls():
    # Define the reference text
    reference_text = """\n\nAmerican Institute of Physics. (2023). The powerhouse of the future: Artificial cells. Phys.org. Retrieved from https://phys.org/news/2023-03-powerhouse-future-artificial-cells.html\n\nNational Institutes of Health. (2023). Artificial mitochondria transfer (AMT) and transplant. PMC. Retrieved from https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5511681/\n\nNature. (2023). Spatiotemporal simulations of mitochondrial dynamics. Nature.com. Retrieved from https://www.nature.com/articles/s41598-019-54159-1\n\nSogang University & Harbin Institute of Technology. (2023). Artificial organelles for sustainable chemical energy conversion and production: Artificial mitochondria and chloroplasts. Biophysics Reviews. Retrieved from https://publishing.aip.org/publications/latest-content/the-powerhouse-of-the-future-artificial-cells/"""

    urls = extract_urls(reference_text)
    print(f'Extracted URLs: {urls}')

#pdf = pdfx.PDFx("filename-or-url.pdf")
#urls = ['/Users/tomriddle1/Documents/GitHub/ResearchAgentSwarm/2308.00352.pdf']




"""
for url in urls:
    try:
        pdf =  pdfx.PDFx(url)
        metadata = pdf.get_metadata()
        print(f'Metadata: {metadata}')
        references_list = pdf.get_references()
        print(f'References: {references_list}')
        references_dict = pdf.get_references_as_dict()
        print(f'References dict: {references_dict}')
        papers = paperscraper.link_to_pdf(url, pdir='downloaded-papers')
        print(f'Papers: {papers}')
    except:
        print("Error in extracting references")
        continue
#pdf.download_pdfs("target-directory")

"""


# %%
import re

def extract_hypothetical_questions(hypothetical_questions_text):
    # Regular expression pattern for identifying hypothetical questions
    question_pattern = re.compile(r'\d+\.\s+([A-Za-z\/-]+ Question):\n\s+-\s+([^\n]+)')
    questions = question_pattern.findall(hypothetical_questions_text)
    print(f'Questions: {questions}')
    if len(questions) == 0:
        return hypothetical_questions_text
    return [{"question_type": question_type, "question": question} for question_type, question in questions]
def test_extract_hypothetical_questions():
    # Example hypothetical questions text
    hypothetical_questions_text_1 = "1. Content-Based Question:\n   - How do genetic modifications contribute to increasing mitochondrial autonomy from nuclear-encoded proteins and functions?\n\n2. Analytical Question:\n   - What are the key tools and methods used in modifying the mitochondrial genome to study the interplay between nuclear and mitochondrial genomes?\n\n3. Creative/Scenario-Based Question:\n   - Imagine a future where mitochondrial autonomy from nuclear-encoded proteins and functions is fully achieved. How might this impact our understanding of cellular functions and the development of new treatments for mitochondrial diseases?\n\n4. Contextual/Relational Question:\n   - How does the research on modifying the mitochondrial genome relate to other areas of genetic engineering and its potential for future advancements in the field?\n\n5. User-Interactive Question:\n   - What are your thoughts on the ethical considerations surrounding genetic modifications in mitochondrial genome engineering? How do you think society should approach this research?"
    hypothetical_questions_text_2 = "1. Content-Based Question: \n   - What does this report investigate regarding mitochondrial ATP production?\n   - How does this report contribute to our understanding of mitochondrial function?\n   - What are the key findings regarding the replication of mitochondrial ATP production outside the cellular environment?\n\n2. Analytical Question:\n   - How do theoretical models help in understanding mitochondrial ATP production?\n   - What experimental evidence supports the concept of artificial organelles for ATP synthesis?\n   - What are the implications of studying mitochondrial dynamics and stress responses for ex vivo methods of ATP synthesis?\n\n3. Creative/Scenario-Based Question:\n   - Imagine a scenario where mitochondrial ATP production could be replicated outside the cellular environment. How could this impact medical research and treatments?\n   - If artificial organelles capable of ATP synthesis were successfully developed, what potential applications could they have in various industries?\n   - How might the understanding of mitochondrial dynamics and stress responses lead to the development of innovative approaches for ATP synthesis?\n\n4. Contextual/Relational Question:\n   - How does the research on mitochondrial ATP production relate to the broader field of cellular bioenergetics?\n   - In what ways does the replication of mitochondrial ATP production outside cells build upon previous studies in the field?\n   - How do the findings in this report align with or challenge existing theories and models of mitochondrial function?\n\n5. User-Interactive Question:\n   - How would you approach studying the replication of mitochondrial ATP production outside the cellular environment?\n   - Can you think of any potential limitations or ethical considerations in developing artificial organelles for ATP synthesis?\n   - What questions or areas of research would you like to see explored further in the study of mitochondrial dynamics and stress responses?"
    hypothetical_questions = []
    hypothetical_questions.append(hypothetical_questions_text_1)
    hypothetical_questions.append(hypothetical_questions_text_2)
    for hypothetical_questions_text in hypothetical_questions:
        extracted_hypothetical_questions = extract_hypothetical_questions(hypothetical_questions_text)
        print(f'Extracted hypothetical questions: {extracted_hypothetical_questions}')

test_extract_hypothetical_questions()



# %%
def clean_entity_relationships(entity_relationships_text):
    # Regular expression pattern for identifying entity relationships
    entity_pattern = re.compile(r'\d+\.\s+\((.+?),\s+(.+?),\s+(.+?)\)')
    entity_relationships = entity_pattern.findall(entity_relationships_text)
    return [{"subject": relationship[0], "relationship": relationship[1], "target": relationship[2]} for relationship in entity_relationships]

# Example entity relationships text
entity_relationships_text =  "Entity Relationships:\n\n1. (mitochondria, responsible for, energy production)\n2. (mitochondria, isolated from, plant cells)\n3. (mitochondria, isolated for, studies involving mitochondrial DNA, protein profiling, and enzymatic activity assays)\n4. (mitochondria, isolated using, continuous colloidal density gradients)\n5. (mitochondria, isolated with, improved methods)\n6. (mitochondria, isolated with, slight modifications)\n7. (mitochondria, isolated with, traditional plant protoplast isolation)\n8. (mitochondria, isolated with, mammalian mitochondria extraction protocols)\n9. (mitochondria, isolated with, adjustments in isolation medium compositions)\n10. (mitochondria, isolated with, reduced need for heavy labor, expensive equipment, and large amounts of starting material)\n11. (mitochondria, used for, respiratory chain measurements, western blot analyses, and mass spectrometry)\n12. (mitochondria, used for, protein and tRNA uptake experiments, enzyme activity assays, and western blot analyses)\n13. (mitochondria, used for, targeted multiple reaction monitoring or quantification by dimethyl or other isotope labels)\n14. (mitochondria, assessed for, purity and integrity)\n15. (mitochondria, assessed using, proteinase digestion assays, electron microscopy, mitochondrial membrane potential measurement, and electron transport chain activity measurement)\n16. (mitochondria, assessed to, confirm the intactness and functional capacity)\n17. (mitochondria, assessed to, evaluate the mitochondrial purity)\n18. (mitochondria, assessed to, evaluate the mitochondrial integrity)\n19. (mitochondria, assessed to, measure the mitochondrial membrane potential)\n20. (mitochondria, assessed to, measure the electron transport chain activity)\n21. (mitochondria, assessed at, the DNA and protein levels)\n22. (mitochondria, assessed using, electron microscopy)\n23. (mitochondria, assessed using, proteinase digestion assays)\n24. (mitochondria, assessed using, mitochondrial membrane potential measurement)\n25. (mitochondria, assessed using, electron transport chain activity measurement)\n26. (mitochondria, isolated from, Arabidopsis thaliana)\n27. (mitochondria, isolated using, continuous colloidal density gradients)\n28. (mitochondria, isolated at, 4 °C)\n29. (mitochondria, isolated for, studies involving mitochondrial DNA, protein profiling, and enzymatic activity assays)\n30. (mitochondria, isolated with, tailored isolation protocol)\n31. (mitochondria, isolated with, minimized damage to ensure the integrity)\n32. (mitochondria, isolated with, reduced contamination from other organelles)\n33. (mitochondria, isolated with, improved methods)\n34. (mitochondria, isolated with, mammalian mitochondria extraction protocols)\n35. (mitochondria, isolated with, adjustments in isolation medium compositions)\n36. (mitochondria, isolated with, reduced need for heavy labor, expensive equipment, and large amounts of starting material)\n37. (mitochondria, isolated with, minimal contamination from other organelles)\n38. (mitochondria, isolated with, improved methods)\n39. (mitochondria, isolated with, slight modifications)\n40. (mitochondria, isolated with, traditional plant protoplast isolation)\n41. (mitochondria, isolated with, mammalian mitochondria extraction protocols)\n42. (mitochondria, isolated with, adjustments in isolation medium compositions)\n43. (mitochondria, isolated with, reduced need for heavy labor, expensive equipment, and large amounts of starting material)\n44. (mitochondria, isolated with, minimal contamination from other organelles)\n45. (mitochondria, isolated from, Arabidopsis thaliana)\n46. (mitochondria, isolated using, continuous colloidal density gradients)\n47. (mitochondria, isolated at, 4 °C)\n48. (mitochondria, used for, protein and tRNA uptake experiments)\n49. (mitochondria, used for, enzyme activity assays)\n50. (mitochondria, used for, western blot analyses)\n51. (mitochondria, used for, mass spectrometry analyses)\n52. (mitochondria, used for, targeted multiple reaction monitoring or quantification by dimethyl or other isotope labels)\n53. (mitochondria, assessed for, purity and integrity)\n54. (mitochondria, assessed using, proteinase digestion assays)\n55. (mitochondria, assessed using, electron microscopy)\n56. (mitochondria, assessedThe article discusses the protocol for isolating mitochondria from plant cells. Mitochondria are double-membraned organelles responsible for energy production in eukaryotic cells. The isolation of mitochondria is crucial for various studies involving mitochondrial DNA, protein profiling, and enzymatic activity assays.\n\nThe isolation process is challenging due to the presence of cell walls, vacuoles, and secondary metabolites in plant cells. The protocol must be tailored to minimize damage to the mitochondria and ensure their integrity. Specificity in isolation protocols is required as different plant species and tissue types have varying phenolic compounds and metabolite profiles. Earlier methods led to contamination with nuclei and chloroplasts, but recent advancements have improved isolation methods, reducing the need for heavy labor, expensive equipment, and large amounts of starting material.\n\nThe protocol for isolating intact mitochondria involves several steps. First, the preparation of grinding medium, wash buffer, and gradient solutions is necessary. The plant material is then homogenized in the grinding medium to release the mitochondria, which are then filtered and centrifuged to pellet the mitochondria. The mitochondrial pellet is resuspended in the wash buffer. Oxygen consumption measurements are crucial for determining the intactness and functional capacity of the isolated mitochondria. Evaluation of mitochondrial purity and integrity can be done through proteinase digestion assays, electron microscopy, and checks of mitochondrial membrane potential and electron transport chain activity.\n\nOnce purified, the isolated mitochondria can be used for various studies, including protein and tRNA uptake experiments, enzyme activity assays, and western blot analyses. For mass spectrometry analyses, targeted multiple reaction monitoring (MRM) or quantification by dimethyl or other isotope labels can be employed.\n\nIn conclusion, the isolation of mitochondria from plant cells is a delicate process that requires careful consideration of the specific requirements of the plant species and tissue type. Recent advancements have made the process more effective and accessible for a range of tissue types and species, allowing for a broader application of mitochondrial studies across different plant species.\n\nReferences:\n- Plant Methods. (2015). https://plantmethods.biomedcentral.com/articles/10.1186/s13007-015-0099-x\n- NCBI. (2018). https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5908444/\n- NCBI. (2018). https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7640673/\n- NCBI. (2018). https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4687074/Extraction and Categorization:\n\n1. (mitochondria, responsible for, energy production)\n2. (mitochondria, isolated from, plant cells)\n3. (mitochondria, isolated for, studies involving mitochondrial DNA, protein profiling, and enzymatic activity assays)\n4. (mitochondria, isolated using, continuous colloidal density gradients)\n5. (mitochondria, isolated with, improved methods)\n6. (mitochondria, isolated with, slight modifications)\n7. (mitochondria, isolated with, traditional plant protoplast isolation)\n8. (mitochondria, isolated with, mammalian mitochondria extraction protocols)\n9. (mitochondria, isolated with, adjustments in isolation medium compositions)\n10. (mitochondria, isolated with, reduced need for heavy labor, expensive equipment, and large amounts of starting material)\n11. (mitochondria, used for, respiratory chain measurements, western blot analyses, and mass spectrometry)\n12. (mitochondria, used for, protein and tRNA uptake experiments, enzyme activity assays, and western blot analyses)\n13. (mitochondria, used for, targeted multiple reaction monitoring or quantification by dimethyl or other isotope labels)\n14. (mitochondria, assessed for, purity and integrity)\n15. (mitochondria, assessed using, proteinase digestion assays, electron microscopy, mitochondrial membrane potential measurement, and electron transport chain activity measurement)\n16. (mitochondria, assessed to, confirm the intactness and functional capacity)\n17. (mitochondria, assessed to, evaluate the mitochondrial purity)\n18. (mitochondria, assessed to, evaluate the mitochondrial integrity)\n19. (mitochondria, assessed to, measure the mitochondrial membrane potential)\n20. (mitochondria, assessed to, measure the electron transport chain activity)\n21. (mitochondria, assessed at, the DNA and protein levels)\n22. (mitochondria, assessed using, electron microscopy)\n23. (mitochondria, assessed using, proteinase digestion assays)\n24. (mitochondria, assessed using, mitochondrial membrane potential measurement)\n25. (mitochondria, assessed using, electron transport chain activity measurement)\n26. (mitochondria, isolated from, Arabidopsis thaliana)\n27. (mitochondria, isolated using, continuous colloidal density gradients)\n28. (mitochondria, isolated at, 4 °C)\n29. (mitochondria, used for, protein and tRNA uptake experiments)\n30. (mitochondria, used for, enzyme activity assays)\n31. (mitochondria, used for, western blot analyses)\n32. (mitochondria, used for, mass spectrometry analyses)\n33. (mitochondria, used for, targeted multiple reaction monitoring or quantification by dimethyl or other isotope labels)\n34. (mitochondria, assessed for, purity and integrity)\n35. (mitochondria, assessed using, proteinase digestion assays)\n36. (mitochondria, assessed using, electron microscopy)\n37. (mitochondria, assessed using, mitochondrial membrane potential measurement)\n38. (mitochondria, assessed using, electron transport chain activity measurement)\n39. (mitochondria, isolated from, Arabidopsis thaliana)\n40. (mitochondria, isolated using, continuous colloidal density gradients)\n41. (mitochondria, isolated at, 4 °C)"

# Clean the entity relationships
cleaned_entity_relationships = clean_entity_relationships(entity_relationships_text)

# Output the cleaned entity relationships
cleaned_entity_relationships



# %%
!pip uninstall pydantic -y
!pip uninstall instructor -y
!pip install openai
!pip install PyPDF2

from datetime import datetime
from pydantic import BaseModel, Field

import os
import json
import instructor
from openai import OpenAI

import re
from typing import List


# %%
!pip install pydantic
!pip install instructor
!pip install openai
!pip install PyPDF2
from PyPDF2 import PdfReader 


from datetime import datetime
from pydantic import BaseModel, Field

import os
import json
import instructor
from openai import OpenAI

import re
from typing import List



api_key = "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"

# Optionally set the environment variable (if needed elsewhere)
os.environ['OPENAI_API_KEY'] = api_key

# Enum for prompt types
    
def extract_urls(reference_text):
    # Regular expression pattern for identifying URLs
    url_pattern = re.compile(r'https?://[^\s,]+')
    urls = url_pattern.findall(reference_text)
    return urls
class SummaryStore:
    def __init__(self, file_id): 
        self.file_id = file_id
        self.file_path = f"{OUTPUT_FOLDER}{file_id}.json"
        self._create_file_if_not_exists()

    def _create_file_if_not_exists(self):
        if not os.path.exists(self.file_path):
            # Initialize with empty data
            empty_data = [] 
            self._save(empty_data)
    
    def store(self, summary, clean_entities,dirty_entities, file_id, article, references, topic, hypothetical_questions, knowledge):
        data = { 
            "file_id": file_id,
            "article": article,
            "summary": summary,
            "clean_entities": clean_entities,
            "dirty_entities": dirty_entities,
            "references": references,
            "topics": topic,
            "hypothetical_questions": hypothetical_questions,
            "knowledge_triplets": knowledge,
            "timestamp": datetime.now().isoformat()
        }

        existing_data = self.load()
        existing_data.append(data)
        print(f"Storing data for file_id: {file_id}")  # Log storing action
        self._save(existing_data)

    def load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                return json.load(f)
        else:
            return []

    def _save(self, content):
        try:
            with open(self.file_path, "w") as f:
                json.dump(content, f)
            print(f"Successfully saved data to {self.file_path}")  # Log success message
        except Exception as e:
            print(f"Error saving data to {self.file_path}: {e}")  # Log error message  

def count_words(text):
    return len(text.split())

def build_system_prompt(prompt_type: str):
    # read from file "entity_dense_prompt.md"
    if prompt_type == "Enitity Dense":
        with open("entity_dense_prompt.md", "r") as f:
            system_prompt = f.read()
    if prompt_type == "SPR":
        with open("sparse_prime_representation.md", "r") as f:
            system_prompt = f.read()
    if prompt_type == "Get Entities":
        with open("get_entities.md", "r") as f:
            system_prompt = f.read()
    if prompt_type == "Get Topic":
        with open("get_topic.md", "r") as f:
            system_prompt = f.read()
    if prompt_type == "Get Hypothetical Questions":
        with open("get_hypothetical_questions.md", "r") as f:
            system_prompt = f.read()
    if prompt_type == "Get Knowledge":
        with open("get_knowlege_graph_triples.md", "r") as f:
            system_prompt = f.read()
    return f"{system_prompt}"

def parse_response(response):

    # Get the text content from the single completion 
    completion = response.choices[0]
    text = completion.message.content

    # Remove unnecessary newlines and whitespace    
    text = text.strip()  

    # Could add additional parsing logic here 

    return text



def generate_summary(text: str, summary_type: str, model: str = "gpt-3.5-turbo-0613", temp: float = 0.45, max_tokens: int = 800 ):
    client = instructor.patch(OpenAI(api_key=api_key))
    if not text:
        raise ValueError("Text cannot be empty")

    if temp < 0 or temp > 1:
       raise ValueError("Temperature should be between 0 and 1")
    
    try: 
        # summarization code
        if summary_type == "Entity Dense":
            #print(f"System Prompt: {build_system_prompt(prompt_type='Enitity Dense')}")
            response = client.chat.completions.create(
                model=model,
                temperature=temp,
                max_tokens=max_tokens,
                max_retries=3,
                messages=[
                    {"role": "system", "content": build_system_prompt(prompt_type="Enitity Dense")},
                    {"role": "user", "content": text}
                ],
            )
        if summary_type == "SPR":
            #print(f"System Prompt: {build_system_prompt(prompt_type='SPR')}")
            response = client.chat.completions.create(
                model=model,
                temperature=temp,
                max_tokens=max_tokens,
                max_retries=3,
                messages=[
                    {"role": "system", "content": build_system_prompt(prompt_type="SPR")},
                    {"role": "user", "content": text}
                ],
            )
        summary = parse_response(response)
    except Exception as e:
        print(f"Error in summarizing article: {e}\n Occured in generate_summary function")
        # Break out of the loop if there is an error
        return None
    
    if not summary:
        raise RuntimeError("Summary generation failed")

    return summary


def get_entity_dense_sumary(article, initial_summary, num_iterations=3):
    summary_chain = [initial_summary]
    
    all_entities_dict = {}
    clean_entities,  dirty_entities = get_entities(article)
    all_entities_dict["clean_entities"] = clean_entities
    all_entities_dict["dirty_entities"] = dirty_entities

    try:
        for _ in range(num_iterations):
            missing_entities = [entity for entity in clean_entities if entity not in summary_chain[-1]]
            condensed_entities = generate_summary(text=",".join(missing_entities), summary_type="SPR")
            request = build_sumary_request(article, summary_chain[-1], condensed_entities)
            new_summary = generate_summary(text=request, summary_type="Entity Dense")  
            summary_chain.append(new_summary)        
        return summary_chain[-1], all_entities_dict
    except Exception as e:
        print(f"Error in summarizing article: {e}\n Using last summary")
        # Break out of the loop if there is an error
        return summary_chain[-1], all_entities_dict
    

def get_entities(article: str, model="gpt-3.5-turbo-0613"):
    client = instructor.patch(OpenAI(api_key=api_key))

    if not article:
        raise ValueError("Article text cannot be empty")

    entities = []

    sentences = split_to_sentences(article)
        
    chunk_size = 5
    overlap = 1
    
    for i in range(0, len(sentences), chunk_size-overlap): 
        start = i
        end = i + chunk_size
        if end > len(sentences):
            end = len(sentences)
            
        chunk = sentences[start:end]
        chunk_text = ". ".join(chunk)
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                        {"role": "system", "content": build_system_prompt(prompt_type="Get Entities")},
                        {"role": "user", "content": chunk_text}
                    ],
                temperature=0.7
            )

            entities.extend(_parse_entities(response))
        except Exception as e:
            print(f"Error in extracting entities: {e}")
            # Break out of the loop if there is an error
            return None
        
    return clean_and_separate_entities(entities)
    

def _parse_entities(response):
    # Parses the generated response to extract a list of entity strings
    entities = [] 
    entity_text =  parse_response(response)
    #print(f'Entity text: {entity_text}')

    # Naive splitting on commas for example output 
    entities = [e.strip() for e in entity_text.split(",")] 
    entities = [e for e in entities if e]
    
    return entities


def build_knowledge_graph_request(article, clean_entities=None, dirty_entities=None, prev_knowledge=None):
        request = f"Article: {article}\n\n"
        if clean_entities:
            request += f"Clean Entities: {clean_entities}\n\n"
        if dirty_entities:
            request += f"Dirty Entities: {dirty_entities}\n\n"
        if prev_knowledge:
            request += f"Do Not Repeat Previous Knowledge: {prev_knowledge}\n\n"
        
        client = instructor.patch(OpenAI(api_key=api_key))
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo-0613",
                temperature=0.6,
                max_retries=3,
                messages=[
                    {"role": "system", "content": build_system_prompt(prompt_type="Get Knowledge")},
                    {"role": "user", "content": request}
                ],
            )
            knowledge = parse_response(response)
            return knowledge
        except Exception as e:
            print(f"Error in extracting knowledge: {e}")
            # Break out of the loop if there is an error
            raise ValueError("Error in extracting knowledge")


def build_sumary_request(article, prev_summary, missing_entities):

    request = f"Article: {article}\n\n"
    request += f"Previous Summary: {prev_summary}\n\n" 
    request += f"Missing Entities: {missing_entities}\n\n"
    return request

def split_to_sentences(text):
    # logic to split text into sentences 
    return re.split(r"[.!?]\s", text)

   
def get_article_chunks(article, chunk_size=800 ):
    total_words = count_words(article) 
    if total_words <= chunk_size:
        return [article]
    
    sentences = split_to_sentences(article)
    
    chunks = []
    current_chunk = []
    curr_len = 0
    
    for sentence in sentences:
        sentence_words = count_words(sentence)  
        if curr_len + sentence_words < chunk_size:
            # add sentence if under chunk size
            current_chunk.append(sentence)
            curr_len += sentence_words 
        else:
            # otherwise save chunk and reset
            chunks.append(" ".join(current_chunk)) 
            current_chunk = [sentence]
            curr_len = sentence_words
            
    if current_chunk:
        chunks.append(" ".join(current_chunk))
        
    return chunks
import re

def extract_references(file_path):

    with open(file_path) as f:
        text = f.read() 

    start_idx = text.find("## References")

    if start_idx >= 0:
        refs = text[start_idx:]
        refs = refs.replace("## References", "")
        return refs

    return ""

def request_topics(summary):
    client = instructor.patch(OpenAI(api_key=api_key))
    try:
        response = client.chat.completions.create(
        model="gpt-3.5-turbo-0613",
        temperature=0.4,
        max_retries=3,
        messages=[
            {"role": "system", "content": build_system_prompt(prompt_type="Get Topic")},
            {"role": "user", "content": summary}])
        topic = extract_topics_with_justification(parse_response(response))
    except Exception as e:
        print(f"Error in extracting topics: {e}")
        # Break out of the loop if there is an error
        return None
    return topic

def request_hypothetical_questions(summary):
    client = instructor.patch(OpenAI(api_key=api_key))
    try:
        response = client.chat.completions.create(
        model="gpt-3.5-turbo-0613",
        temperature=0.4,
        max_retries=3,
        messages=[
            {"role": "system", "content": build_system_prompt(prompt_type="Get Hypothetical Questions")},
            {"role": "user", "content": summary}])
        questions = extract_hypothetical_questions(parse_response(response))
        #questions = parse_response(response)
    except Exception as e:
        print(f"Error in extracting hypothetical questions: {e}")
        # Break out of the loop if there is an error
        return None
    return questions

def extract_info(summary):
    # NLP logic to extract topic and hypothetical questions 
    while True:
        topic = request_topics(summary)
        if topic:
            break
    while True:
        questions = request_hypothetical_questions(summary)
        if questions:
            break
    return topic, questions

def extract_knowledge(article, clean_entities, dirty_entities):
    # NLP logic to extract knowledge from the article
    knowledge = ""
    if not article:
        raise ValueError("Article text cannot be empty")

    try:
        clean_knowledge = build_knowledge_graph_request(article=article, clean_entities=clean_entities)
        knowledge += clean_knowledge
    except Exception as e:
        print(f"Error in extracting clean knowledge: {e}\n Trying again")
        clean_knowledge = build_knowledge_graph_request(article=article, clean_entities=clean_entities)
        knowledge += clean_knowledge
    try:
        dirty_knowledge = build_knowledge_graph_request(article=article, dirty_entities=dirty_entities)
        knowledge += dirty_knowledge
    except Exception as e:
        print(f"Error in extracting dirty knowledge: {e}\n Trying again")
        dirty_knowledge = build_knowledge_graph_request(article=article, dirty_entities=dirty_entities)
        knowledge += dirty_knowledge

    try:
        combined_knowledge = build_knowledge_graph_request(article=article, prev_knowledge=knowledge)
        knowledge += combined_knowledge
    except Exception as e:
        print(f"Error in extracting combined knowledge: {e}\n Trying again")
        combined_knowledge = build_knowledge_graph_request(article=article, prev_knowledge=knowledge)
        knowledge += combined_knowledge
    return clean_entity_relationships(knowledge)


import subprocess

def extract_references_from_pdf(pdf_path, output_path):
    # Construct the command
    command = f"pdfx -v '{pdf_path}' -o '{output_path}'"

    # Run the command
    try:
        subprocess.run(command, check=True, shell=True)
        print(f"References extracted successfully to {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

# Example usage
#pdf_path = "/path/to/your/pdf.pdf"
#output_path = "/path/to/output/file.txt"
#extract_references_from_pdf(pdf_path, output_path)
from PyPDF2 import PdfReader 

def pdf_to_text(pdf_path):
    # importing required modules 
    text = ""
    # creating a pdf reader object 
    reader = PdfReader(pdf_path)
    pages = reader.pages
    
    # printing number of pages in pdf file 
    #print(len(reader.pages)) 
    
    # getting a specific page from the pdf file 
    #page = reader.pages[0] 
    
    # extracting text from page 
    for page in pages:
        text += page.extract_text()
    if not text:
        raise ValueError("Text cannot be empty")
    return text


def Incrementally_Refine_Article_Summary(article_info):
    file_id = article_info["file_id"]
    file_path = article_info["file_path"]
    
    store = SummaryStore(file_id)
    if article_info["file_type"] == "pdf":
        # Extract references from PDF
        references_path = f"{OUTPUT_FOLDER}{file_id}.txt"
        extract_references_from_pdf(file_path, references_path)
        with open(references_path) as f:
            references = f.read()
    else:
        references = extract_references(file_path)  
    urls = extract_urls(references)
    if urls:
        # create dictionary of urls and references
        references = {"urls": urls, "references": references}
    #print(f"References: {references}")
    if article_info["file_type"] == "pdf":
        # Extract text from PDF
        article_text = pdf_to_text(file_path)
    else:
        with open(file_path) as f:
            article_text = f.read()
    
    article_chunks = get_article_chunks(article_text)

    try:
        chunk_num = 0
        for chunk in article_chunks:
            # Generate an initial summary for each chunk
            initial_summary = generate_summary(text=chunk, summary_type="SPR")
            
            # Generate a refined summary for each chunk
            refined_sumary, entities = get_entity_dense_sumary(chunk, initial_summary)

            # Extract Knowledge from the article and entities
            knowledge_triplets = extract_knowledge(chunk, clean_entities=entities["clean_entities"], dirty_entities=entities["dirty_entities"])

            # Extract the topic and hypothetical questions from the refined summary
            topic, questions = extract_info(refined_sumary)

            # Store the summary, entities, and citation
            chunk_name = f"Chunk # {chunk_num}.\n{chunk}"
            
            store.store(summary=refined_sumary, 
                        file_id=file_id, 
                        clean_entities=entities["clean_entities"],
                        dirty_entities=entities["dirty_entities"],
                        article=chunk_name, 
                        references=references, 
                        topic=topic, 
                        hypothetical_questions=questions,
                        knowledge=knowledge_triplets
                        )
            chunk_num += 1
        # return success
        return True

    except Exception as e: 
        print(f"Error summarizing {file_path}: {e}")
        return None


import codecs

def is_bibliography(file_path):

    with codecs.open(file_path, 'rb') as f:
        first_line = f.readline()
        if b'# Bibliography Recommendation Report:' in first_line:
            return True
    return False

def get_article_list(filetype="md"):
    articles = []
    
    for file_name in os.listdir(OUTPUT_FOLDER):
        file_path = os.path.join(OUTPUT_FOLDER, file_name)
        
        # Skip bibliography files
        if is_bibliography(file_path):
            continue
        if not file_name.endswith(filetype):
            continue
        else:
            if file_name.endswith(".md") or file_name.endswith(".mmd"):
                file_id = get_file_id(file_name)
                summary_file_path = os.path.join(OUTPUT_FOLDER, f"{file_id}.json")

                if not os.path.exists(summary_file_path):
                    info = {
                        "file_id": file_id, 
                        "file_path": file_path,
                        "file_type": filetype
                    }
                    articles.append(info)
            
            if file_name.endswith(".pdf"):
                file_id = get_file_id(file_name)
                summary_file_path = os.path.join(OUTPUT_FOLDER, f"{file_id}.json")

                if not os.path.exists(summary_file_path):
                    info = {
                        "file_id": file_id, 
                        "file_path": file_path,
                        "file_type": filetype
                    }
                    articles.append(info)

    return articles

def get_file_id(file_name):
    # Extract base name without extension
    return os.path.splitext(file_name)[0]



#OUTPUT_FOLDER = "/home/epas/Programming/ResearchAgentSwarm/Literature_Review/gpt_researcher_outputs/" 
OUTPUT_FOLDER = "/Users/tomriddle1/Documents/GitHub/gpt-researcher/outputs/"
#OUTPUT_FOLDER = "gpt_researcher_outputs/"
#OUTPUT_FOLDER = "Literature_Review/gpt_researcher_outputs/"
OUTPUT_FOLDER = "/home/epas/Programming/ResearchAgentSwarm/Literature_Review/chemical_structure_report/"
#OUTPUT_FOLDER = "/home/epas/Programming/gpt-researcher/outputs/" # mmd files
article_list = get_article_list(filetype="mmd")
if article_list:
    for article_info in article_list:
        print(f"Summarizing {article_info['file_path']}")
        success = Incrementally_Refine_Article_Summary(article_info)
        if success:
            print(f"Successfully summarized {article_info['file_path']}")
        else:
            print(f"Error summarizing {article_info['file_path']}")
else:
    print("No articles to summarize")
# open summary.json to see the results 



# %%


# %% [markdown]
# # Create ChatGPT Message Summary

# %%
def count_words(text):
    return len(text.split())

def analyze_file(file_path, output_file_path, document_name):
    try:
        with open(file_path, 'r') as file:
            lines = file.read().split('\n')

        with open(output_file_path, 'w') as output_file:
            current_message = ""
            message_started = False
            sender = ""
            message_number = 0

            for i, line in enumerate(lines):
                line = line.strip()
                if line.lower().startswith('user') or line.lower().startswith('chatgpt'):
                    if message_started:  # End of a message
                        message_number += 1
                        word_count = count_words(current_message.strip())
                        output_file.write(f"{sender} Line number {i}, Message number {message_number}, Document: {document_name}, (Word Count: {word_count}):\n{current_message}\n\n---\n\n")
                        current_message = ""
                    message_started = True
                    sender = "User" if line.lower().startswith('user') else "ChatGPT"
                    continue
                if message_started:
                    current_message += " " + line

            # Add the last message if it exists
            if current_message:
                message_number += 1
                word_count = count_words(current_message.strip())
                output_file.write(f"{sender} Last message, Document: {document_name}, (Word Count: {word_count}):\n{current_message}\n\n---\n\n")

    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Replace 'your_file.txt' with the path to your text file
# Replace 'output_messages.txt' with the path for the output file
# Add the document name (e.g., 'ChatGPT_history.txt')
file_path = 'ChatGPT_history.txt'
output_file_path = 'output_messages.txt'
document_name = 'ChatGPT_history'  # This is the document name without the extension
analyze_file(file_path, output_file_path, document_name)
print("Messages have been written to the output file.")




# %%
import json
import time
from datetime import datetime
from typing import List, Tuple, Dict


class MessageAnalysisStore:
    def __init__(self, output_file_path):
        self.output_file_path = output_file_path
        self._create_file_if_not_exists()

    def _create_file_if_not_exists(self):
        if not os.path.exists(self.output_file_path):
            empty_data = []
            self._save(empty_data)

    def store(self, analyzed_data):
        existing_data = self.load()
        existing_data.append(analyzed_data)
        self._save(existing_data)

    def load(self):
        if os.path.exists(self.output_file_path):
            with open(self.output_file_path, "r") as file:
                return json.load(file)
        else:
            return []

    def _save(self, content):
        try:
            with open(self.output_file_path, "w") as file:
                json.dump(content, file, indent=4)
            print(f"Successfully saved data to {self.output_file_path}")
        except Exception as e:
            print(f"Error saving data to {self.output_file_path}: {e}")

# Assuming the required classes and functions from your new code are already defined and imported
# like SummaryStore, generate_summary, get_entities, extract_knowledge, etc.

def extract_messages_with_citation(lines: List[str], sender_keyword: str) -> List[Tuple[str, str]]:
    """
    Extracts messages with citation from the given lines based on the sender keyword.
    """

    messages_with_citation = []
    current_message = ""
    message_started = False
    citation_info = ""
    for i, line in enumerate(lines):
        line = line.strip()
        if line.lower().startswith(sender_keyword):
            if message_started:
                # End of the current message, add it to the list
                messages_with_citation.append((current_message.strip(), citation_info))
                current_message = ""
            message_started = True
            citation_info = line  # Capture the line with sender info as citation
        elif message_started:
            current_message += " " + line

    # Add the last message if it exists
    if current_message:
        messages_with_citation.append((current_message.strip(), citation_info))

    return messages_with_citation

def analyze_conversation(message: str, citation: str, sender_keyword: str) -> Dict:
    """
    Analyzes a single conversation message, extracting and summarizing information.
    """
    try:
        # Generate an initial summary
        if sender_keyword == "ChatGPT":
            initial_summary = generate_summary(text=message, summary_type="Entity Dense")
        else:
            initial_summary = generate_summary(text=message, summary_type="SPR")

        # Extract entities and knowledge
        entities = get_entities(message)
        knowledge = extract_knowledge(message, entities["clean_entities"], entities["dirty_entities"])

        # Extract the topic and hypothetical questions from the summary
        topic, questions = extract_info(initial_summary)

        analyzed_data = {
            "id": citation,
            "sender": sender_keyword,
            "message": message,
            "topic": topic,
            "hypothetical_questions": questions,
            "clean_entities": entities["clean_entities"],
            "dirty_entities": entities["dirty_entities"],
            "summary": initial_summary,
            "knowledge": knowledge,
            "timestamp": datetime.now().isoformat()
        }
        return analyzed_data

    except Exception as e:
        raise Exception(f"An error occurred in analyzing conversation: {e}")

def extract_and_analyze_messages(file_path: str, output_file_path: str, sender_keyword: str, log_file_path: str):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    messages_with_citation = extract_messages_with_citation(lines, sender_keyword)
    store = MessageAnalysisStore(output_file_path)
    error_log = []

    for message, citation in messages_with_citation:
        try:
            analyzed_data = analyze_conversation(message, citation, sender_keyword)
            store.store(analyzed_data)
            time.sleep(15)  # Delay to avoid rate limiting
        except Exception as e:
            error_info = {"citation": citation, "error": str(e), "timestamp": datetime.now().isoformat()}
            # Appending to the error log
            error_log.append(error_info)
            with open(log_file_path, "a") as log_file:
                json.dump(error_info, log_file, indent=4)
                log_file.write("\n")
            continue

    print(f"Messages analysis completed. Data saved to {output_file_path}")
    if error_log:
        print(f"Errors logged to {log_file_path}")

# Example usage
file_path = 'output_messages.txt'
output_file_path_user = 'analyzed_user_messages.json'
log_file_path_user = 'error_log_user.json'
extract_and_analyze_messages(file_path, output_file_path_user, 'user', log_file_path_user)


# %%


# %% [markdown]
# # Neo4j Graph Database

# %%
!pip install neo4j

from neo4j import GraphDatabase

NEO4J_URI="bolt://:7687"
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="12345678"


driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

with driver:
    driver.verify_connectivity()


# %% [markdown]
# MATCH (n) 
# DETACH DELETE n
# 
# CREATE CONSTRAINT FOR ()-[r:RELATED_TO]-() REQUIRE r.id IS UNIQUE
# 
# // Shared Entities  
# MATCH (a1:ArticleID)-[:MENTIONS]->(e)<-[:MENTIONS]-(a2:ArticleID) 
# WHERE e:CleanEntity OR e:DirtyEntity
# WITH DISTINCT a1, a2, collect(e.name) AS shared 
# MERGE (a1)-[r:RELATED_TO {type:'Shared Entity'}]->(a2)
# ON CREATE SET r.entities = shared
# 
# // Shared Topics
# MATCH (a1)-[:HAS_TOPIC]->(t1)<-[:HAS_TOPIC]-(a2) 
# WITH a1, a2, split(t1.name, ' ') AS words1
# UNWIND words1 AS word1
# MATCH (a3)-[:HAS_TOPIC]->(t2)<-[:HAS_TOPIC]-(a4)
# WHERE word1 =~ '(?i).*?' + word1  
# WITH DISTINCT a1, a3, collect(word1) AS shared
# MERGE (a1)-[r:RELATED_TO {type:'Shared Topic Word'}]->(a3)
# ON CREATE SET r.words = shared
# 
# // Shared Subjects
# MATCH (a:ArticleID)-[:HAS_TRIPLET]->(s:Subject)<-[:HAS_TRIPLET]-(b:ArticleID)
# WHERE id(a) < id(b) 
# WITH DISTINCT a, b, collect(s.name) AS shared 
# MERGE (a)-[r:RELATED_TO {type:'Shared Subject'}]->(b)  
# ON CREATE SET r.subjects = shared
# 
# // Shared URLs
# MATCH (a1)-[:HAS_REFERENCE]->(r)<-[:HAS_REFERENCE]-(a2)
# WHERE r:Reference AND id(a1) < id(a2)  
# WITH DISTINCT a1, a2, collect(r.url) AS shared  
# MERGE (a1)-[r:RELATED_TO {type:'Shared URL'}]->(a2)
# ON CREATE SET r.urls = shared

# %%
import logging
import os
import json
import dateutil.parser  # You need to install the python-dateutil package
# 11226 13863

def escape_string(text):
    # Helper function to escape special characters in strings
    return text.replace("'", "\\'").replace('"', '\\"')

def create_or_update_article_with_chunks(session, file_id, chunk_content, chunk_index, timestamp):
    # Convert timestamp from string to Unix timestamp (seconds since epoch)
    try:
        timestamp_unix = dateutil.parser.parse(timestamp).timestamp()
    except Exception as e:
        logging.error(f"Error parsing timestamp: {timestamp}. Error: {e}")
        timestamp_unix = 0  # Default to 0 or some other value in case of parsing failure
    # Ensure ArticleID node exists (create if it doesn't)
    session.run(f"MERGE (articleID:ArticleID {{id: '{file_id}'}})")

    # Create or update the Article node and link it to ArticleID
    session.run(f"MATCH (articleID:ArticleID {{id: '{file_id}'}}) MERGE (article:Article) MERGE (articleID)-[:IDENTIFIES]->(article)")

    # Create a new Chunk node with a unique identifier, timestamp, and link it to ArticleID
    chunk_id = f"{file_id}_{chunk_index}"
    create_chunk_query = (
        f"MATCH (articleID:ArticleID {{id: '{file_id}'}}) "
        f"CREATE (chunk:Chunk {{id: '{chunk_id}', content: '{chunk_content}', timestamp: '{timestamp_unix}'}}) "
        f"CREATE (articleID)-[:HAS_CHUNK]->(chunk)"
    )
    session.run(create_chunk_query)

    # Link this chunk to the previous chunk if it's not the first one
    if chunk_index > 0:
        previous_chunk_id = f"{file_id}_{chunk_index - 1}"
        link_chunks_query = (
            f"MATCH (prevChunk:Chunk {{id: '{previous_chunk_id}'}}), (currChunk:Chunk {{id: '{chunk_id}'}}) "
            f"CREATE (prevChunk)-[:NEXT]->(currChunk)"
        )
        session.run(link_chunks_query)

# Functions to link nodes to ArticleID
def link_topic_to_article(session, file_id, topic_name, justification):
    query = (
        f"MATCH (articleID:ArticleID {{id: '{file_id}'}}) "
        f"MERGE (topic:Topic {{name: '{topic_name}', justification: '{justification}'}}) "
        f"MERGE (articleID)-[:HAS_TOPIC]->(topic)"
    )
    session.run(query)
def link_entity_to_article(session, file_id, entity_name, clean=True):
    entity_type = "CleanEntity" if clean else "DirtyEntity"
    # Don't add irrelevant entities: 
    if entity_name in ['Abstract Concepts:', 'References:', 'Key Phrases:', 'Keywords:', 'Entities:', 'Topics:', 'Concepts:', 'Final Output:', 'Introduction', 'Conclusion', 'Summary']:
        return
    query = (
        f"MATCH (articleID:ArticleID {{id: '{file_id}'}}) "
        f"MERGE (entity:{entity_type} {{name: '{entity_name}'}}) "
        f"MERGE (articleID)-[:MENTIONS]->(entity)"
    )
    session.run(query)
def link_question_to_article(session, file_id, question_content, question_type):
    query = (
        f"MATCH (articleID:ArticleID {{id: '{file_id}'}}) "
        f"MERGE (hq:HypotheticalQuestion {{content: '{question_content}', type: '{question_type}'}}) "
        f"MERGE (articleID)-[:HAS_QUESTION]->(hq)"
    )
    session.run(query)
def link_triplet_to_article(session, file_id, subject, target, relationship):
    query = (
        f"MATCH (articleID:ArticleID {{id: '{file_id}'}}) "
        f"MERGE (subj:Subject {{name: '{subject}'}}) "
        f"MERGE (targ:Target {{name: '{target}'}}) "
        f"MERGE (rel:Relationship {{type: '{relationship}'}}) "
        f"MERGE (subj)-[:HAS_RELATIONSHIP]->(rel)-[:TARGETS]->(targ) "
        f"MERGE (articleID)-[:HAS_TRIPLET]->(subj)"
    )
    session.run(query)
def link_summary_to_chunk(session, file_id, chunk_index, summary_content):
    # Unique identifier for the chunk
    chunk_id = f"{file_id}_{chunk_index}"

    # Link the summary to the corresponding chunk
    link_summary_query = (
        f"MATCH (chunk:Chunk {{id: '{chunk_id}'}}) "
        f"MERGE (summary:Summary {{content: '{summary_content}'}}) "
        f"MERGE (chunk)-[:HAS_SUMMARY]->(summary)"
    )
    session.run(link_summary_query)
def link_url_references_to_article(session, file_id, urls):
    for url in urls:
        escaped_url = escape_string(url)
        query = (
            f"MATCH (articleID:ArticleID {{id: '{file_id}'}}) "
            f"MERGE (ref:Reference {{url: '{escaped_url}'}}) "
            f"WITH articleID, ref "
            f"MERGE (articleID)-[:HAS_REFERENCE]->(ref)"
        )
        session.run(query)
def link_textual_references_to_article(session, file_id, textual_references):
    for reference in textual_references.split('\n'):  # Assuming each reference is on a new line
        if reference.strip():
            escaped_reference = escape_string(reference)
            query = (
                f"MATCH (articleID:ArticleID {{id: '{file_id}'}}) "
                f"MERGE (textRef:TextualReference {{text: '{escaped_reference}'}}) "
                f"WITH articleID, textRef "
                f"MERGE (articleID)-[:HAS_TEXTUAL_REFERENCE]->(textRef)"
            )
            session.run(query)

def process_knowledge_triplet(session, file_id, subject, target, relationship):
    # Constructing a query to check if the specific triplet combination already exists
    check_triplet_query = (
        f"MATCH (articleID:ArticleID {{id: '{file_id}'}})-[:HAS_TRIPLET]->"
        f"(subj:Subject {{name: '{subject}'}})-[:HAS_RELATIONSHIP]->"
        f"(rel:Relationship {{type: '{relationship}'}})-[:TARGETS]->"
        f"(targ:Target {{name: '{target}'}}) "
        f"RETURN subj, rel, targ"
    )
    if not session.run(check_triplet_query).single():
        # Linking the triplet only if it doesn't exist
        link_triplet_to_article(session, file_id, subject, target, relationship)
def process_json_file(file_path, session):
    with open(file_path) as file:
        data = json.load(file)

        # Group records by file_id
        grouped_records = {}
        for record in data:
            file_id = record['file_id']
            grouped_records.setdefault(file_id, []).append(record)

        for file_id, records in grouped_records.items():
            try:
                # Check if the ArticleID already exists
                check_query = f"MATCH (articleID:ArticleID {{id: '{file_id}'}}) RETURN articleID"
                result = session.run(check_query).single()
                if result:
                    logging.info(f"File ID {file_id} already exists in the database. Processing only new chunks.")
                else:
                    logging.info(f"File ID {file_id} does not exist. Processing all chunks.")

                for index, record in enumerate(records):
                    chunk_content = escape_string(record['article'])
                    timestamp = record.get('timestamp', '')
                    summary_content = escape_string(record['summary']) if "summary" in record else ""

                    # Process each chunk
                    process_record_with_chunks(session, file_id, chunk_content, index, timestamp, summary_content, record)

                logging.info(f"Successfully processed file: {file_path}")
            except Exception as e:
                logging.error(f"Failed to process file: {file_path}. Error: {e}")
                continue

def process_record_with_chunks(session, file_id, chunk_content, chunk_index, timestamp, summary_content, record):
    chunk_id = f"{file_id}_{chunk_index}"

    # Check and process each chunk and its summary
    if not session.run(f"MATCH (chunk:Chunk {{id: '{chunk_id}'}}) RETURN chunk").single():
        create_or_update_article_with_chunks(session, file_id, chunk_content, chunk_index, timestamp)
        if summary_content:
            link_summary_to_chunk(session, file_id, chunk_index, summary_content)

    # Process Topics
    for topic in record.get("topics", []):
        topic_name = escape_string(topic['topic'])
        if not session.run(f"MATCH (articleID:ArticleID {{id: '{file_id}'}})-[:HAS_TOPIC]->(topic:Topic {{name: '{topic_name}'}}) RETURN topic").single():
            justification = escape_string(topic.get('justification', ''))
            link_topic_to_article(session, file_id, topic_name, justification)

    # Process Entities (both clean and dirty)
    for clean, entities in [(True, record.get("clean_entities", [])), (False, record.get("dirty_entities", []))]:
        for entity in entities:
            entity_name = escape_string(entity)
            if entity_name.strip() and not session.run(f"MATCH (articleID:ArticleID {{id: '{file_id}'}})-[:MENTIONS]->(entity {{name: '{entity_name}'}}) RETURN entity").single():
                link_entity_to_article(session, file_id, entity_name, clean)

    # Process Hypothetical Questions
    for question in record.get("hypothetical_questions", []):
        question_content = escape_string(question['question'])
        if not session.run(f"MATCH (articleID:ArticleID {{id: '{file_id}'}})-[:HAS_QUESTION]->(hq:HypotheticalQuestion {{content: '{question_content}'}}) RETURN hq").single():
            question_type = escape_string(question.get('question_type', ''))
            link_question_to_article(session, file_id, question_content, question_type)

    # Process Knowledge Triplets
    for triplet in record.get("knowledge_triplets", []):
        subject = escape_string(triplet['subject'])
        target = escape_string(triplet['target'])
        relationship = escape_string(triplet['relationship'])
        process_knowledge_triplet(session, file_id, subject, target, relationship)

    # Process URL References
    if "references" in record and "urls" in record["references"]:
        for url in record["references"]["urls"]:
            escaped_url = escape_string(url)
            if not session.run(f"MATCH (articleID:ArticleID {{id: '{file_id}'}})-[:HAS_REFERENCE]->(ref:Reference {{url: '{escaped_url}'}}) RETURN ref").single():
                link_url_references_to_article(session, file_id, [url])

    # Process Textual References
    if "references" in record and "textual_references" in record["references"]:
        for reference in record["references"]["textual_references"].split('\n'):
            if reference.strip():
                escaped_reference = escape_string(reference)
                if not session.run(f"MATCH (articleID:ArticleID {{id: '{file_id}'}})-[:HAS_TEXTUAL_REFERENCE]->(textRef:TextualReference {{text: '{escaped_reference}'}}) RETURN textRef").single():
                    link_textual_references_to_article(session, file_id, [reference])

def add_jsons_to_neo4j(output_folder):
    with driver.session() as session:
        for file_name in os.listdir(output_folder):
            if file_name.endswith(".json"):
                file_path = os.path.join(output_folder, file_name)
                process_json_file(file_path, session)
                print(f"Successfully processed file: {file_path}")
    driver.close()

if __name__ == "__main__":
    output_folder4 = "/Users/tomriddle1/Documents/GitHub/ResearchAgentSwarm/Literature_Review/Chemical_Structure_json/"
    output_folder1 = "/home/epas/Programming/ResearchAgentSwarm/Literature_Review/Chemical_Structure_json/"
    output_folder2 = "/home/epas/Programming/gpt-researcher/outputs/"
    output_folder3 = "/home/epas/Programming/ResearchAgentSwarm/Literature_Review/gpt_researcher_outputs/"
    for output_folder in [output_folder1, output_folder2, output_folder3, output_folder4]:
        try:
            add_jsons_to_neo4j(output_folder)
        except Exception as e:
            print(f"Error adding jsons to Neo4j database: {e}")
            continue
    print("Successfully added data to Neo4j database.")

# %%
embedding = embeddings.embed_query("text")
print(f"Embedding for text: {embedding}\n With shape: {len(embedding)}")

# %%
from langchain.embeddings import HuggingFaceEmbeddings
from neo4j import GraphDatabase

# Configuration for HuggingFaceEmbeddings
model_name = "WhereIsAI/UAE-Large-V1"  # or another model of your choice
model_kwargs = {'device': 'mps'}  # use 'cuda' for GPU acceleration if available
embeddings = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs)

def LoadEmbedding(node_type, text_properties):
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
    with driver.session() as session:
        # Handle multiple properties (concatenation) for a single embedding
        if isinstance(text_properties, list) and len(text_properties) > 1:
            properties_str = " + ' ' + ".join([f"n.{prop}" for prop in text_properties])
            query = f"MATCH (n:{node_type}) WHERE n.embedding IS NULL RETURN id(n) AS id, {properties_str} AS text"
        else:
            text_property = text_properties[0]
            query = f"MATCH (n:{node_type}) WHERE n.embedding IS NULL RETURN id(n) AS id, n.{text_property} AS text"

        result = session.run(query)
        count = 0
        for record in result:
            id = record["id"]
            text = record["text"]

            # Generate the embedding
            embedding = embeddings.embed_query(text)
            print(f"Embedding for {node_type} with id {id}: With shape: {len(embedding)}")
            cypher = "MATCH (n) WHERE id(n) = $id SET n.embedding = $embedding"
            session.run(cypher, embedding=embedding, id=id)
            count += 1

        print(f"Processed {count} {node_type} nodes for property @{' and '.join(text_properties)}.")
    return count

# Example usages
LoadEmbedding("Chunk", ["content"])
LoadEmbedding("CleanEntity", ["name"])
LoadEmbedding("DirtyEntity", ["name"])
LoadEmbedding("Subject", ["name"])
LoadEmbedding("Target", ["name"])
LoadEmbedding("Relationship", ["type"])
LoadEmbedding("Topic", ["name", "justification"])  # Concatenating name and justification for topics
LoadEmbedding("HypotheticalQuestion", ["content"])


# %%
from neo4j import GraphDatabase

def create_indexes(uri, user, password):
    # Establish a connection to the Neo4j database
    driver = GraphDatabase.driver(uri, auth=(user, password))

    # Define Cypher queries for creating the indexes
    create_full_text_index_query = """
    CALL db.index.fulltext.createNodeIndex("textIndex", ["Chunk", "CleanEntity", "DirtyEntity", "HypotheticalQuestion"], ["content", "name"])
    """
    create_vector_index_query = """
    CALL db.index.vector.createNodeIndex("chunkVectorIndex", "Embedding", "embedding", 1024, "COSINE")
    """

    with driver.session() as session:
        # Create Full-Text Index#
        #session.run(create_full_text_index_query) # Neo.ClientError.Procedure.ProcedureNotFound
        #print("Full-text index created.")

        # Create Vector Index
        session.run(create_vector_index_query)
        print("Vector index created.")

    # Close the driver connection
    driver.close()

from neo4j import GraphDatabase

def modify_indexes(old_index_name, new_index_name, label, property, dimensions, similarity):
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
    with driver.session() as session:
        # Drop the old index
        session.run(f"DROP INDEX {old_index_name}")

        # Create the new vector index
        create_vector_index_query = f"""
        CALL db.index.vector.createNodeIndex("{new_index_name}", "{label}", "{property}", {dimensions}, "{similarity}")
        """
        session.run(create_vector_index_query)
        print(f"Vector index {new_index_name} created.")

    # Close the driver connection
    driver.close()

# Usage
uri = NEO4J_URI
user = NEO4J_USERNAME
password = NEO4J_PASSWORD
old_index_name = "chunkVectorIndex"  # Replace with the actual name of the index to drop
new_index_name = "chunkVectorIndex"  # Replace with your new index name
label = "Embedding"  # Replace with the appropriate label
property = "embedding"  # Replace with the correct property
dimensions = 1024
similarity = "COSINE"

#modify_indexes(old_index_name, new_index_name, label, property, dimensions, similarity)


create_indexes(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)


# %%
from langchain.embeddings import HuggingFaceEmbeddings

def generate_query_vector(text, model_name="WhereIsAI/UAE-Large-V1", model_kwargs={'device': 'mps'}):
    embeddings = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs)
    return embeddings.embed_query(text)


from neo4j import GraphDatabase

def query_similar_nodes(uri, user, password, vector_index_name, query_vector, top_k=10):
    driver = GraphDatabase.driver(uri, auth=(user, password))
    similar_nodes = []
    with driver.session() as session:
        query = f"""
        CALL db.index.vector.queryNodes('{vector_index_name}', {top_k}, $queryVector)
        YIELD node, score
        RETURN node, score
        """
        result = session.run(query, queryVector=query_vector)
        for record in result:
            node = record["node"]
            score = record["score"]
            similar_nodes.append((node, score))
    driver.close()
    return similar_nodes


query_text = "X-ray crystallography"
query_vector = generate_query_vector(query_text)
print(f"Query vector: {query_vector}\n With shape: {len(query_vector)}")
uri = NEO4J_URI
user = NEO4J_USERNAME
password = NEO4J_PASSWORD
vector_index_name = "chunkVectorIndex"  # Replace with your actual vector index name

similar_nodes = query_similar_nodes(uri, user, password, vector_index_name, query_vector)
for node, score in similar_nodes:
    print(node, score)


# %% [markdown]
# 

# %%
from neo4j import GraphDatabase

NEO4J_URI="bolt://:7687"
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="12345678"


driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

with driver:
    driver.verify_connectivity()

# %%
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings import OllamaEmbeddings, SentenceTransformerEmbeddings
from langchain.chat_models import ChatOpenAI, ChatOllama
from langchain.vectorstores.neo4j_vector import Neo4jVector
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from typing import List, Any
#from utils import BaseLogger
from langchain.chains import GraphCypherQAChain 
#model_name = "WhereIsAI/UAE-Large-V1" 
def load_embedding_model(embedding_model_name: str, config={}):
    if embedding_model_name == "ollama":
        embeddings = OllamaEmbeddings(
            base_url=config["ollama_base_url"], model="llama2"
        )
        dimension = 4096
        #logger.info("Embedding: Using Ollama")
    elif embedding_model_name == "openai":
        embeddings = OpenAIEmbeddings()
        dimension = 1536
        #logger.info("Embedding: Using OpenAI")
    elif embedding_model_name == "WhereIsAI/UAE-Large-V1":
        embeddings = HuggingFaceEmbeddings(
            model_name="WhereIsAI/UAE-Large-V1", cache_folder="Literature_Review/cache/"
        )
        dimension = 1024
        #logger.info("Embedding: Using HuggingFace")
    else:
        embeddings = SentenceTransformerEmbeddings(
            model_name="all-MiniLM-L6-v2", cache_folder="Literature_Review/cache/"
        )
        dimension = 384
        #logger.info("Embedding: Using SentenceTransformer")
    return embeddings, dimension


def load_llm(llm_name: str, config={}):
    if llm_name == "gpt-4":
        logger.info("LLM: Using GPT-4")
        return ChatOpenAI(temperature=0, model_name="gpt-4", streaming=True)
    elif llm_name == "gpt-3.5":
        logger.info("LLM: Using GPT-3.5")
        return ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", streaming=True)
    elif len(llm_name):
        logger.info(f"LLM: Using Ollama: {llm_name}")
        return ChatOllama(
            temperature=0,
            base_url=config["ollama_base_url"],
            model=llm_name,
            streaming=True,
            top_k=10,  # A higher value (100) will give more diverse answers, while a lower value (10) will be more conservative.
            top_p=0.3,  # Higher value (0.95) will lead to more diverse text, while a lower value (0.5) will generate more focused text.
            num_ctx=3072,  # Sets the size of the context window used to generate the next token.
        )
    logger.info("LLM: Using GPT-3.5")
    return ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", streaming=True)


def configure_llm_only_chain(llm):
    # LLM only response
    template = """
    You are a helpful assistant that helps with answering general questions.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    """
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = "{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    def generate_llm_output(
        user_input: str, callbacks: List[Any], prompt=chat_prompt
    ) -> str:
        answer = llm(
            prompt.format_prompt(
                text=user_input,
            ).to_messages(),
            callbacks=callbacks,
        ).content
        return {"answer": answer}

    return generate_llm_output


def configure_qa_rag_chain(llm, embeddings, embeddings_store_url, username, password):
    # RAG response
    general_system_template = """
    Use the following context to answer the question at the end.
    The context contains article summaries, related topics, and hypothetical questions.
    Make sure to rely on accurate information from the summaries and topics.
    If a particular article or topic in the context is useful, refer to it in your response.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    ----
    {summaries}
    ----
    Your response should be concise and based on the given context.
    """

    general_user_template = "Question:```{question}```"
    messages = [
        SystemMessagePromptTemplate.from_template(general_system_template),
        HumanMessagePromptTemplate.from_template(general_user_template),
    ]
    qa_prompt = ChatPromptTemplate.from_messages(messages)

    qa_chain = load_qa_with_sources_chain(
        llm,
        chain_type="stuff",
        prompt=qa_prompt,
    )

    # Vector + Knowledge Graph response
    kg = Neo4jVector.from_existing_index(
        embedding=embeddings,
        url=embeddings_store_url,
        username=username,
        password=password,
        database='neo4j',  # neo4j by default
        index_name="chunkVectorIndex",  # vector by default
        text_node_property="content",  # text by default
        retrieval_query="""
        WITH node AS questionEmb, score
        MATCH (questionEmb) <-[:HAS_EMBEDDING]- (article:Article)
        OPTIONAL MATCH (article)-[:HAS_SUMMARY]->(summary:Summary)
        OPTIONAL MATCH (article)-[:HAS_TOPIC]->(topic:Topic)
        RETURN '##Article ID: ' + article.id + '\n' 
            + '##Summary: ' + coalesce(summary.content, 'No summary available') + '\n'
            + '##Related Topics: ' + coalesce(topic.name, 'No topics available') AS text, 
            score AS similarity
        ORDER BY similarity DESC LIMIT 5
    """,
    )

    kg_qa = RetrievalQAWithSourcesChain(
        combine_documents_chain=qa_chain,
        retriever=kg.as_retriever(search_kwargs={"k": 2}),
        reduce_k_below_max_tokens=False,
        max_tokens_limit=3375,
    )
    return kg_qa

# ADDED
# >>>> Extended to support vector search over strucutured chunking

def configure_qa_structure_rag_chain(llm, embeddings, embeddings_store_url, username, password):
    # RAG response based on vector search and retrieval of structured chunks
    
    sample_query = """
    // 0 - prepare question and its embedding 
        MATCH (ch:Chunk) -[:HAS_EMBEDDING]-> (chemb) 
        WHERE ch.block_idx = 19
        WITH ch.sentences AS question, chemb.value AS qemb
        // 1 - search chunk vectors
        CALL db.index.vector.queryNodes($index_name, $k, qemb) YIELD node, score
        // 2 - retrieve connectd chunks, sections and documents
        WITH node AS answerEmb, score
        MATCH (answerEmb) <-[:HAS_EMBEDDING]- (answer) -[:HAS_PARENT*]-> (s:Section)
        WITH s, score LIMIT 1
        MATCH (d:Document) <-[*]- (s) <-[:HAS_PARENT*]- (chunk:Chunk)
        WITH d, s, chunk, score ORDER BY chunk.block_idx ASC
        // 3 - prepare results
        WITH d, collect(chunk) AS chunks, score
        RETURN {source: d.url, page: chunks[0].page_idx} AS metadata, 
            reduce(text = "", x IN chunks | text + x.sentences + '.') AS text, score;   
    """

    general_system_template = """
    You are an assistant providing detailed answers based on specific chunks of articles.
    Use the context provided to answer the question at the end.
    Ensure that the context is not altered and that your responses are based on the content of the chunks.
    If you don't know the answer, just say that you don't know.
    ----
    {summaries}
    ----
    Each answer should include reference to the relevant document and page, as indicated in the context metadata.
    """

    general_user_template = "Question:```{question}```"
    messages = [
        SystemMessagePromptTemplate.from_template(general_system_template),
        HumanMessagePromptTemplate.from_template(general_user_template),
    ]
    qa_prompt = ChatPromptTemplate.from_messages(messages)

    qa_chain = load_qa_with_sources_chain(
        llm,
        chain_type="stuff",
        prompt=qa_prompt,
    )

    # Vector + Knowledge Graph response
    kg = Neo4jVector.from_existing_index(
        embedding=embeddings,
        url=embeddings_store_url,
        username=username,
        password=password,
        database='neo4j',  # neo4j by default
        index_name="chunkVectorIndex",  # vector by default
        node_label="Embedding",  # embedding node label
        embedding_node_property="embedding",  # embedding value property
        text_node_property="content",  # text by default
        retrieval_query="""
        WITH node AS answerEmb, score
        MATCH (answerEmb) <-[:HAS_EMBEDDING]- (chunk:Chunk) -[:HAS_CHUNK]-> (article:Article)
        WITH article, chunk, score
        ORDER BY score DESC LIMIT 10
        MATCH (chunk)-[:NEXT]->(nextChunk:Chunk)
        WITH article, chunk, nextChunk, score
        RETURN '##Article ID: ' + article.id + '\n'
            + 'Relevant Chunk: ' + chunk.content + '\n'
            + 'Next Chunk: ' + nextChunk.content AS text, 
            score AS similarity
        LIMIT 3

    """,
    )

    kg_qa = RetrievalQAWithSourcesChain(
        combine_documents_chain=qa_chain,
        retriever=kg.as_retriever(search_kwargs={"k": 25}),
        reduce_k_below_max_tokens=False,
        max_tokens_limit=7000,      # gpt-4
    )
    return kg_qa

# %%
import os
#!pip install streamlit
import streamlit as st



# Rest of your code...

from streamlit.logger import get_logger
from langchain.callbacks.base import BaseCallbackHandler
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.graphs import Neo4jGraph
from dotenv import load_dotenv
#from utils import (
#    extract_title_and_question,
#    create_vector_index,
#)



# >>>> initialise - environemnt <<<< 

#load_dotenv(".env")
"""
url = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")
database = os.getenv("NEO4J_DATABASE")
ollama_base_url = os.getenv("OLLAMA_BASE_URL")
embedding_model_name = os.getenv("EMBEDDING_MODEL")
llm_name = os.getenv("LLM")
"""
url = NEO4J_URI
username = NEO4J_USERNAME
password = NEO4J_PASSWORD
database = "neo4j"
#ollama_base_url = "http://localhost:8000"
embedding_model_name = "WhereIsAI/UAE-Large-V1"
llm_name = "gpt-4"


# Remapping for Langchain Neo4j integration
# os.environ["NEO4J_URL"] = url


# >>>> initialise - services <<<< 

logger = get_logger(__name__)

neo4j_graph = Neo4jGraph(url=url, username=username, password=password, database=database)

embeddings, dimension = load_embedding_model(
    embedding_model_name)

llm = load_llm(llm_name)


# llm_chain: LLM only response
llm_chain = configure_llm_only_chain(llm)

# rag_chain: KG augmented response
rag_chain = configure_qa_structure_rag_chain(
    llm, embeddings, embeddings_store_url=url, username=username, password=password
)

# SKIPPED: create_vector_index(neo4j_graph, dimension)

# >>>> Class definition - StreamHander <<<< 

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)

# >>>> Streamlit UI <<<<

styl = f"""
<style>
    /* not great support for :has yet (hello FireFox), but using it for now */
    .element-container:has([aria-label="Select RAG mode"]) {{
      position: fixed;
      bottom: 33px;
      background: white;
      z-index: 101;
    }}
    .stChatFloatingInputContainer {{
        bottom: 20px;
    }}

    /* Generate question text area */
    textarea[aria-label="Description"] {{
        height: 200px;
    }}
</style>
"""
st.markdown(styl, unsafe_allow_html=True)
st.image("qna-logo.png", width=160) 

# >>>> UI interations <<<<

def chat_input():
    user_input = st.chat_input("What service questions can I help you resolve today?")

    if user_input:
        with st.chat_message("user"):
            st.write(user_input)
        with st.chat_message("assistant"):
            st.caption(f"RAG: {name}")
            stream_handler = StreamHandler(st.empty())

            # Call chain to generate answers
            result = output_function(
                {"question": user_input, "chat_history": []}, callbacks=[stream_handler]
            )["answer"]

            output = result

            st.session_state[f"user_input"].append(user_input)
            st.session_state[f"generated"].append(output)
            st.session_state[f"rag_mode"].append(name)


def display_chat():
    # Initialize session state keys if they do not exist
    #if "generated" not in st.session_state:
    #    st.session_state["generated"] = []
    if "user_input" not in st.session_state:
        st.session_state["user_input"] = []
    if "rag_mode" not in st.session_state:
        st.session_state["rag_mode"] = []

    # Now you can safely access st.session_state["generated"] and other keys



def mode_select() -> str:
    options = ["Disabled", "Enabled"]
    return st.radio("Select RAG mode", options, horizontal=True)

# >>>>> switch on/off RAG mode

name = mode_select()
if name == "LLM only" or name == "Disabled":
    output_function = llm_chain
elif name == "Vector + Graph" or name == "Enabled":
    output_function = rag_chain

"""
def generate_ticket():
    # Get high ranked questions
    records = neo4j_graph.query(
        "MATCH (q:Question) RETURN q.title AS title, q.body AS body ORDER BY q.score DESC LIMIT 3"
    )
    questions = []
    for i, question in enumerate(records, start=1):
        questions.append((question["title"], question["body"]))
    # Ask LLM to generate new question in the same style
    questions_prompt = ""
    for i, question in enumerate(questions, start=1):
        questions_prompt += f"{i}. {question[0]}\n"
        questions_prompt += f"{question[1]}\n\n"
        questions_prompt += "----\n\n"

    gen_system_template = f\"""
    You're an expert in formulating high quality questions. 
    Can you formulate a question in the same style, detail and tone as the following example questions?
    {questions_prompt}
    ---

    Don't make anything up, only use information in the following question.
    Return a title for the question, and the question post itself.

    Return example:
    ---
    Title: How do I use the Neo4j Python driver?
    Question: I'm trying to connect to Neo4j using the Python driver, but I'm getting an error.
    ---
    \"""
    # we need jinja2 since the questions themselves contain curly braces
    system_prompt = SystemMessagePromptTemplate.from_template(
        gen_system_template, template_format="jinja2"
    )
    q_prompt = st.session_state[f"user_input"][-1]
    chat_prompt = ChatPromptTemplate.from_messages(
        [
            system_prompt,
            SystemMessagePromptTemplate.from_template(
                \"""
                Respond in the following format or you will be unplugged.
                ---
                Title: New title
                Question: New question
                ---
                \"""
            ),
            HumanMessagePromptTemplate.from_template("{text}"),
        ]
    )
    llm_response = llm_chain(
        f"Here's the question to rewrite in the expected format: ```{q_prompt}```",
        [],
        chat_prompt,
    )
    new_title, new_question = extract_title_and_question(llm_response["answer"])
    return (new_title, new_question)


"""

def open_sidebar():
    st.session_state.open_sidebar = True


def close_sidebar():
    st.session_state.open_sidebar = False


if not "open_sidebar" in st.session_state:
    st.session_state.open_sidebar = False
"""
if st.session_state.open_sidebar:
    new_title, new_question = generate_ticket()
    with st.sidebar:
        st.title("Ticket draft")
        st.write("Auto generated draft ticket")
        st.text_input("Title", new_title)
        st.text_area("Description", new_question)
        st.button(
            "Submit to support team",
            type="primary",
            key="submit_ticket",
            on_click=close_sidebar,
        )
"""

# >>>> UI: show chat <<<<
display_chat()
chat_input()



# %%


# %%
!pip install TTS
!pip install speake3


# %%
!tts --list_models
!tts --text "Hello, how are you?" --model_name "tts_models/en/ljspeech/vits" --out_path "output.wav"


# %%
from calendar import c
from librosa import ex
from regex import E
import torch
from TTS.api import TTS
#!pip install PyPDF2
from PyPDF2 import PdfReader
import re
from torch import le 

import subprocess


def pdf_to_text(pdf_path):
    # importing required modules 
    text = ""
    # creating a pdf reader object 
    reader = PdfReader(pdf_path)
    pages = reader.pages
    
    # printing number of pages in pdf file 
    #print(len(reader.pages)) 
    
    # getting a specific page from the pdf file 
    #page = reader.pages[0] 
    
    chunk_idx =0
    # extracting text from page 
    for page in pages:
        text = page.extract_text()
        if chunk_idx <=9:
            cmd = f'tts --text "{text}" --model_name "tts_models/en/ljspeech/vits" --out_path AUDIO_OUTPUTS/page_0{chunk_idx}.wav'
        else:
            cmd = f'tts --text "{text}" --model_name "tts_models/en/ljspeech/vits" --out_path AUDIO_OUTPUTS/page_{chunk_idx}.wav'
        
        try:
            subprocess.run(cmd, check=True, shell=True)
            chunk_idx += 1
        except Exception as e:
            print(f"An error occurred: {e}")
            # try again but drop the last 5 sentences
            text = text.rsplit(".", 5)[0]
            if chunk_idx <=9:
                cmd = f'tts --text "{text}" --model_name "tts_models/en/ljspeech/vits" --out_path AUDIO_OUTPUTS/page_0{chunk_idx}.wav'
            else:
                cmd = f'tts --text "{text}" --model_name "tts_models/en/ljspeech/vits" --out_path AUDIO_OUTPUTS/page_{chunk_idx}.wav'
            try:
                subprocess.run(cmd, check=True, shell=True)
                chunk_idx += 1
            except Exception as e:
                # skip this chunk
                print(f"An error occurred: {e}")
                chunk_idx += 1
                continue

        

    if not text:
        raise ValueError("Text cannot be empty")
    return text

pdf = "/Users/tomriddle1/Documents/Dr_Bryan_Chemisty.pdf"
text = pdf_to_text(pdf)
print(len(text))
# Get device
#device = "cuda" if torch.cuda.is_available() else "cpu"

# List available 🐸TTS models
#print(TTS().list_models())

# Init TTS
#tts = TTS("tts_models/en/ljspeech/vits").to(device)

# Run TTS
# Text to speech to a file
#tts.tts_to_file(text="Hello world!", speaker_wav="my/cloning/audio.wav", language="en", file_path="output.wav")
# Init TTS with the target model name
#tts = TTS(model_name="tts_models/en/ljspeech/vits", progress_bar=True).to(device)

# Run TTS
#tts.tts_to_file(text=text, file_path="output.wav")



# %%
!pip install PyPDF2
from PyPDF2 import PdfReader
import re
from torch import le 

def pdf_to_text(pdf_path):
    # importing required modules 
    text = ""
    # creating a pdf reader object 
    reader = PdfReader(pdf_path)
    pages = reader.pages
    
    # printing number of pages in pdf file 
    #print(len(reader.pages)) 
    
    # getting a specific page from the pdf file 
    #page = reader.pages[0] 
    
    # extracting text from page 
    for page in pages:
        text += page.extract_text()
    if not text:
        raise ValueError("Text cannot be empty")
    return text
pdf = "/Users/tomriddle1/Documents/Dr_Bryan_Chemisty.pdf"
text = pdf_to_text(pdf)
print(len(text))
# Break text into chunks of 5000 words
def split_to_sentences(text):
    # logic to split text into sentences 
    return re.split(r"[.!?]\s", text)
text_chunks = split_to_sentences(text)
print(len(text_chunks))
!tts --text f"{text_chunks[0]}" --model_name "tts_models/en/ljspeech/vits" --out_path "output.wav"


# %%
!conda clean --packages -y

# %%



