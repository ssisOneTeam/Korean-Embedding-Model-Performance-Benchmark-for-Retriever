import torch # _device_check

from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings as STE
from langchain.embeddings import OpenAIEmbeddings
from settings import OPENAI_API_KEY
from datetime import datetime


class EmbeddingLoader:
    class SentenceTransformerEmbedding:
        def __init__(self, **kwargs) -> None:
            """ Embedding model setting. 
                
                args
                    model_name: model name or path(HuggingFaceEmbeddings)
                    encode_kwargs: encoding kwargs from SentenceTransformer model kwargs
            """
            kwargs.setdefault("model_kwargs", {'device': self._device_check()})
            self.kwargs = kwargs
            return
        
        def checktime(func):
            def wrapper(*args, **kwargs):
                start_time = datetime.now()
                result = func(*args, **kwargs)
                end_time = datetime.now()
                print(f"Function call {func.__name__} took {(end_time - start_time).total_seconds()}s to run.\n")
                return result
            return wrapper

        @checktime
        def load(self) -> STE:
            embedding = STE(**self.kwargs)
            print(f"embedding model in path <{embedding.model_name}> has been loaded successfully.")
            return embedding
        
        def _device_check(self) -> str: 
            ''' for check cuda availability '''
            if torch.cuda.is_available(): device = "cuda"
            elif torch.backends.mps.is_available(): device = "mps"
            else: device = "cpu"
            return device    
    
    class OpenAIEmbedding:
        def __init__(self) -> None:
            print("OpenAI Embedding has been activated.")
            self.embedding = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

        def checktime(func):
            def wrapper(*args, **kwargs):
                start_time = datetime.now()
                result = func(*args, **kwargs)
                end_time = datetime.now()
                print(f"Function call {func.__name__} took {(end_time - start_time).total_seconds()}s to run.\n")
                return result
            return wrapper

        @checktime
        def load(self):
            return self.embedding

## test
if __name__ == "__main__" :
    PATH_YOUR_EMBEDDING_MODEL = "PATH WHERE YOUR EMBEDDING MODEL IS"
    setup = EmbeddingLoader.SentenceTransformerEmbedding(model_name=PATH_YOUR_EMBEDDING_MODEL, encode_kwargs = {'normalize_embeddings': True})