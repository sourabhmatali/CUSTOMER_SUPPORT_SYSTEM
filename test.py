from config.config_loader import load_config #here we are testing / here taking from config----->config_loader.py----->load_config()[method]

config=load_config() #here initializing the load_config()

collection_name = config["astra_db"]["collection_name"] #here we can fetch /they are like key & value pair ,here "astra_db" is key & "collection_name" is value
embedding_model_name = config["embedding_model"]["model_name"]#here we can fetch /they are like key & value pair ,here "embedding_model" is key & "model_name" is value
top_k = config["retriever"]["top_k"]#here we can fetch /they are like key & value pair ,here "retriever" is a key & "top_k"  is value

print(collection_name)
print(embedding_model_name)
print(top_k)