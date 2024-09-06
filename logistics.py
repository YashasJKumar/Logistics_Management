
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

def get_response():

    load_dotenv()

    # Load the CSV file
    file_loader = CSVLoader("../merged_data.csv")
    file_content = file_loader.load()

    # Use a larger chunk size or custom logic to ensure full content is loaded without truncation
    splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=0)
    docs = splitter.split_documents(documents=file_content)

    # Load embedding model and create vector store
    embedding_model = OllamaEmbeddings(model="nomic-embed-text:latest")
    vectors = FAISS.from_documents(embedding=embedding_model, documents=docs)

    # Define the prompt template
    prompt_template = ChatPromptTemplate.from_template(
        """Answer the following question based on the provided context, source, destination & your knowledge.
        Think step by step before providing the detailed answer.
        I am a lorry driver. I have customer data, before their delivery deadlines, you should provide me
        the most optimal path for delivering all products & I must incur minimum running costs.
        <context> 
        {context} 
        </context> 
        Question: {input}
        Answer step by step, showing how I should travel to pick up all products from their respective locations
        and deliver them to their destination locations. Ensure that you cover everyone and provide the total 
        distance of the path.Be descriptive.
        """
    )

    # Initialize the LLM
    llm = ChatGroq(
        groq_api_key=os.getenv('GROQ_API_KEY'),
        model_name='Mixtral-8x7b-32768',
        temperature=0
    )

    # Create document chain with full context handling
    document_chain = create_stuff_documents_chain(llm=llm, prompt=prompt_template)

    retriever = vectors.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    prompt = "Optimize & provide the best path.Don't miss any delivery."
    result = retrieval_chain.invoke({'input': prompt})
    with open("./answer.txt", "w") as f:
        f.write(result['answer'])

