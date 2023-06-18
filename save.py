import chromadb
from chromadb.config import Settings
from time import time
from uuid import uuid4

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as infile:
        return infile.read()

if __name__ == '__main__':
    def main():
        # instantiate ChromaDB
        persist_directory = "chromadb"
        chroma_client = chromadb.Client(Settings(persist_directory=persist_directory,chroma_db_impl="duckdb+parquet",))
        collection = chroma_client.get_or_create_collection(name="knowledge_base")

        # Update the knowledge base
        print('\n\nUpdating KB...')
        save_knowledge = open_file('save_kb.txt')
        if collection.count() == 0:
            # yay first KB!
            article = save_knowledge
            new_id = str(uuid4())
            collection.add(documents=[article],ids=[new_id])
        else:
            results = collection.query(query_texts=[save_knowledge], n_results=1)
            kb_id = results['ids'][0][0]
            article = save_knowledge
            
            # Expand current KB
            collection.update(ids=[kb_id],documents=[article])
            print('############################################')
            print(article)
            print('############################################')
        chroma_client.persist()
main()