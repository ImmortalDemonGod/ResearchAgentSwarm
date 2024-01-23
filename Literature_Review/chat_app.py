from neo4j import GraphDatabase

NEO4J_URI="bolt://:7687"
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="12345678"


driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

with driver:
    driver.verify_connectivity()

from langchain.embeddings import HuggingFaceEmbeddings

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
            model_name="WhereIsAI/UAE-Large-V1"
        )
        dimension = 1024
        #logger.info("Embedding: Using HuggingFace")
    else:
        embeddings = SentenceTransformerEmbeddings(
            model_name="all-MiniLM-L6-v2"
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

