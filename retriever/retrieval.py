import os
from langchain_astradb import AstraDBVectorStore
from typing import List
from langchain_core.documents import Document
from config.config_loader import load_config
from utils.model_loader import ModelLoader
from dotenv import load_dotenv

class Retriever:
    
    def __init__(self):#these are because whenever we are going to create object ,those things will be automatically initialized
        self.model_loader=ModelLoader() #ModelLoader is a class inside model_loader.py to load all the llm,embeddin
        self.config=load_config() #it is function inside config--->config_loader.py
        self._load_env_variables() #for loading all the environment variables
        self.vstore = None
        self.retriever = None
    
    def _load_env_variables(self):
         
        load_dotenv() #loading the environment varaible
         
        required_vars = ["GOOGLE_API_KEY", "ASTRA_DB_API_ENDPOINT", "ASTRA_DB_APPLICATION_TOKEN", "ASTRA_DB_KEYSPACE"] #here all the required varaibles means API keys 
        
        missing_vars = [var for var in required_vars if os.getenv(var) is None] #here iterating over the required_vars
        
        if missing_vars: #if any api key is missing it will raise Error
            raise EnvironmentError(f"Missing environment variables: {missing_vars}")

        self.google_api_key = os.getenv("GOOGLE_API_KEY")  #here getting api key from os.getenv
        self.db_api_endpoint = os.getenv("ASTRA_DB_API_ENDPOINT")#here getting api key from os.getenv
        self.db_application_token = os.getenv("ASTRA_DB_APPLICATION_TOKEN")#here getting api key from os.getenv
        self.db_keyspace = os.getenv("ASTRA_DB_KEYSPACE")#here getting api key from os.getenv
        
    
    def load_retriever(self):
        if not self.vstore: #if nothing inside the vstore 
            collection_name = self.config["astra_db"]["collection_name"] #here we need collection name
            
            self.vstore = AstraDBVectorStore( #here again not creating VDB again ,here just loading the VDB
                embedding= self.model_loader.load_embeddings(),
                collection_name=collection_name,
                api_endpoint=self.db_api_endpoint,
                token=self.db_application_token,
                namespace=self.db_keyspace,
            )
        if not self.retriever:#if there is nothing inside the retriver
            top_k = self.config["retriever"]["top_k"] if "retriever" in self.config else 3 #here we are taking from config.yaml ,if k value is not mentioned it will take as 3
            retriever = self.vstore.as_retriever(search_kwargs={"k": top_k})#converting VDB as a retriver
            print("Retriever loaded successfully.")
            return retriever #returning the retriver
   

    #to test the retriver we are writing below function 
    def call_retriever(self,query:str)-> List[Document]: #here we are passing query it will return the list of document
        retriever=self.load_retriever() #here loading the load_retriever() function
        output=retriever.invoke(query) #here passing the query
        return output
        
    
if __name__=='__main__': #we use to execute this file as a stand alone module
    retriever_obj = Retriever() #here initializing the class
    user_query = "Can you suggest good budget laptops?" #initializing the query
    results = retriever_obj.call_retriever(user_query) #passing the query to retriever

    for idx, doc in enumerate(results, 1): #here printing results page.content & result.metadata
        print(f"Result {idx}: {doc.page_content}\nMetadata: {doc.metadata}\n")