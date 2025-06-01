import os #importing the os 
from dotenv import load_dotenv #importing load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings #importing embeddings from google 
from langchain_google_genai import ChatGoogleGenerativeAI #importing llm from google 
from config.config_loader import load_config #here from config folder from config_loader file we are loading load_config function
from langchain_groq import ChatGroq
class ModelLoader:
    """
    A utility class to load embedding models and LLM models.
    """
    def __init__(self): #this is init method 
        load_dotenv()  #first loading the environment variable
        self._validate_env() #validing the env function 
        self.config=load_config()

    def _validate_env(self):
        """
        Validate necessary environment variables.
        """
        required_vars = ["GOOGLE_API_KEY","GROQ_API_KEY"] #storing GOOGLE_API_KEY inside variable    required_vars
        self.groq_api_key=os.getenv("GROQ_API_KEY")

        missing_vars = [var for var in required_vars if not os.getenv(var)] #here iterating over the    required_vars 
        if missing_vars: #if GOOGLE_API_KEY is not in the env ,it will raise the error 
            raise EnvironmentError(f"Missing environment variables: {missing_vars}")

    def load_embeddings(self):
        """
        Load and return the embedding model.
        """
        print("Loading Embedding model")
        model_name=self.config["embedding_model"]["model_name"] #here we are taking & loading  the embedding model which we stored inside the config.yaml in form of key & value 
        return GoogleGenerativeAIEmbeddings(model=model_name) #here we are passing to  GoogleGenerativeAIEmbeddings class

    def load_llm(self):
        """
        Load and return the LLM model.
        """
        print("LLM loading...")
        model_name=self.config["llm"]["model_name"] #here also we are taking & loading the llm model  which we stored inside the config.yaml in form of key & value 
        gemini_model=ChatGroq(model=model_name,api_key=self.groq_api_key) ##here we are passing to ChatGoogleGenerativeAI   class
        
        return gemini_model  # Placeholder for future LLM loading
