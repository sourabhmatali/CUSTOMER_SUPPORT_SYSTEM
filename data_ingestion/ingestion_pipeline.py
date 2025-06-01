import os
import pandas as pd
from dotenv import load_dotenv
from typing import List, Tuple #we have imported List,Tuple
from langchain_core.documents import Document #for converting data into document objects 
from langchain_astradb import AstraDBVectorStore #imported VDB
from utils.model_loader import ModelLoader #from utils folder, model_loader file loading ModelLoader function[for loading embedding model and llm ]
from config.config_loader import load_config #from config folder ,config_loader file loading load_config function

class DataIngestion: #this class is to ingest data inside the database
    """
    Class to handle data transformation and ingestion into AstraDB vector store.
    """

    def __init__(self):
        """
        Initialize environment variables, embedding model, and set CSV file path.
        """
        print("Initializing DataIngestion pipeline...")
        self.model_loader=ModelLoader() #here creating object of the ModelLoader
        self._load_env_variables() #loading the environment varaible/ here underscore first like ( _load_env_variables() ) this means private method 
        self.csv_path = self._get_csv_path() #initializing path of csv 
        self.product_data = self._load_csv() #reading the csv
        self.config=load_config() #it is config.yaml

    def _load_env_variables(self):
        """
        Load and validate required environment variables.
        """
        load_dotenv() #loading the environment varaible
        
        required_vars = ["GOOGLE_API_KEY", "ASTRA_DB_API_ENDPOINT", "ASTRA_DB_APPLICATION_TOKEN", "ASTRA_DB_KEYSPACE"] #here all the required varaibles means API keys 
        
        missing_vars = [var for var in required_vars if os.getenv(var) is None] #here iterating over the required_vars
        if missing_vars: #if any api key is missing it will raise Error
            raise EnvironmentError(f"Missing environment variables: {missing_vars}")
        
        self.google_api_key = os.getenv("GOOGLE_API_KEY") #here getting api key from os.getenv
        self.db_api_endpoint = os.getenv("ASTRA_DB_API_ENDPOINT")#here getting api key from os.getenv
        self.db_application_token = os.getenv("ASTRA_DB_APPLICATION_TOKEN")#here getting api key from os.getenv
        self.db_keyspace = os.getenv("ASTRA_DB_KEYSPACE")#here getting api key from os.getenv

       

    def _get_csv_path(self):#this func to get the csv file
        """
        Get path to the CSV file located inside 'data' folder.
        """
        current_dir = os.getcwd() #here fetching the current directory
        csv_path = os.path.join(current_dir, 'data', 'flipkart_product_review.csv') #here inside current directory we have data folder inside that we have file named flipkart_product_review.csv

        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found at: {csv_path}")

        return csv_path

    def _load_csv(self):
        """
        Load product data from CSV.
        """
        df = pd.read_csv(self.csv_path) #first reading the csv
        expected_columns = {'product_title', 'rating', 'summary', 'review'} #these are the imp columns inside csv

        if not expected_columns.issubset(set(df.columns)): #if the required columns are not there it wiill raise the error
            raise ValueError(f"CSV must contain columns: {expected_columns}")

        return df #it will return the df

    def transform_data(self):#here from csv converting into document object
        """
        Transform product data into list of LangChain Document objects.
        """
        product_list = [] #it is a empty list

        for _, row in self.product_data.iterrows(): #here iterating over rows,index
            product_entry = { #here it is dictonary keeping in form of key & value 
                "product_name": row['product_title'], #here changing name giving "product_name" from row named 'product_title'
                "product_rating": row['rating'],#here changing name giving "product_rating" from row named 'rating'
                "product_summary": row['summary'],#here changing name giving "product_summary" from row named 'summary'
                "product_review": row['review']#here changing name giving "product_review" from row named 'review'
            }
            product_list.append(product_entry) #here appending in the list/this product_list we are storing inside vector DB

        documents = [] #here empty list is initialized
        for entry in product_list: #here iterating over the product list
            metadata = { #metadata is a variable whis is a dictonary/here keeping all the columns, except "product_review" in metadata
                "product_name": entry["product_name"],
                "product_rating": entry["product_rating"],
                "product_summary": entry["product_summary"]
            }
            #basically Document conatins both pagecontent and metadata
            doc = Document(page_content=entry["product_review"], metadata=metadata) #here passing both  pagecontent and metadata inside the document
            documents.append(doc) #here appending inside the empty list

        print(f"Transformed {len(documents)} documents.")
        return documents #basically this documents are going to be stored in VDB

    def store_in_vector_db(self, documents: List[Document]):
        """
        Store documents into AstraDB vector store.
        """
        collection_name=self.config["astra_db"]["collection_name"]#fetching collection name from config.yaml
        vstore = AstraDBVectorStore( #here initializing the VDB,object name is vstore
            embedding= self.model_loader.load_embeddings(), #here initializing embedding model /this one is in model_loader.py
            collection_name=collection_name, #collection_name taken from config.yaml where we have initialized
            api_endpoint=self.db_api_endpoint, #here api_endpoint , astradb
            token=self.db_application_token, #here astra db application token,astradb
            namespace=self.db_keyspace, #here astra db name space,astradb
        )

        inserted_ids = vstore.add_documents(documents) #here storing the documents into VDB
        print(f"Successfully inserted {len(inserted_ids)} documents into AstraDB.")
        return vstore, inserted_ids #here returning vstore, inserted_ids

    def run_pipeline(self):
        """
        Run the full data ingestion pipeline: transform data and store into vector DB.
        """
        documents = self.transform_data() #fistly we are transforming the data using transform_data function
        vstore, inserted_ids = self.store_in_vector_db(documents)#storing inside the VDB

        # Optionally do a quick search
        query = "Can you tell me the low budget headphone?" #here passing the query to check 
        results = vstore.similarity_search(query) #here passing query ti vstore and doing similarity_search

        print(f"\nSample search results for query: '{query}'")
        for res in results: #it will show result's page content and metadata
            print(f"Content: {res.page_content}\nMetadata: {res.metadata}\n")

# Run if this file is executed directly
if __name__ == "__main__":
    ingestion = DataIngestion() #here initializing the class 
    ingestion.run_pipeline() #here running the pipeline