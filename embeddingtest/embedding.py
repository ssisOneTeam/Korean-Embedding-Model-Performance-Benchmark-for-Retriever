import os
import torch

from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings as STE
from langchain.embeddings import OpenAIEmbeddings
from settings import OPENAI_API_KEY

from sentence_transformers import SentenceTransformer

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

        def load(self) -> STE:
            embedding = STE(**self.kwargs)
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
            return

        def load(self):
            return self.embedding

## test
if __name__ == "__main__" :
    # setup = EmbeddingLoader(from_default_template=False, model_name="workspace/dadt_epoch2_kha_tok", encode_kwargs = {'normalize_embeddings': True}).load()
    setup = EmbeddingLoader(model_name="workspace/dadt_epoch2_kha_tok", encode_kwargs = {'normalize_embeddings': True})