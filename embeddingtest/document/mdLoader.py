"""langchain document 관련해서 db(markdownDB) 불러와서 
    document로 parse하는 과정 object로 생성. 
    
    need url_table, metadata.json """

import os
import uuid
import re
import pandas as pd
import numpy as np
import json

from langchain.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader
from langchain.text_splitter import TextSplitter
from langchain.schema.document import Document

from datetime import datetime

class BaseDBLoader:
    """markdownDB folder에서 불러온 다음에 폴더별로 내부에 있는 내용 Load해서 Split하고 저장함"""

    def __init__(self, path_db:str, path_metadata:str, path_url_table:str, text_splitter:TextSplitter, loader_cls=UnstructuredMarkdownLoader):
        #timecheck
        start_time = datetime.now()
        # textsplitter config
        self.text_splitter = text_splitter
        # loaderclass config
        self.loader_cls = loader_cls
        # md 파일 담고 있는 전체 디렉터리 경로
        self.path_db = path_db
        # metadata path
        self.path_metadata = path_metadata
        # url table path
        self.path_url_table = path_url_table
        # storage
        self.storage = []

        #timecheck
        end_time = datetime.now()
        print("initialize class takes", (end_time-start_time).total_seconds(), "seconds.")
        return

    def load(self, is_split=True, is_regex=True, show_progress=True, use_multithreading=True) -> list[Document]: ### mul 수정
        """ Get Directory Folder and documents -> parse, edit metadata -> langchain Document list. 
        
            args :
                is_split: whether split or not(text_splitter)
                is_regex: apply regex to edit document form. 
                show_progress: show progress -> from LangChain.
                use_multithreading: use multithread(cpu) -> from LangChain. """
        #timecheck
        start_time = datetime.now()
        # document pre-processing
        for db_folder in os.listdir(self.path_db):
            db_folder_abs = os.path.join(self.path_db, db_folder)
            directory_loader = DirectoryLoader(path=db_folder_abs, loader_cls=self.loader_cls, show_progress=show_progress, use_multithreading=use_multithreading)
            doc_list = directory_loader.load()

            if is_regex:
                doc_list = self._result_to_regex(doc_list)            
            if is_split:
                doc_list = self.text_splitter.split_documents(doc_list)
            self.storage.extend(doc_list)
        self.storage = self._process_document_metadata(self.storage)

        #timecheck
        end_time = datetime.now()
        print("loading Documents takes", (end_time-start_time).total_seconds(), "seconds.")
        
        return self.storage

    def _result_to_regex(self, doc_list:list[Document]) -> list[Document]:
        """regex splitter (Document)"""
        regex = '([^가-힣0-9a-zA-Z.,·•%↓()\s\\\])'
        result = []
        for document in doc_list:
            sub_str = re.sub(pattern=regex, repl="", string=document.page_content)
            document.page_content = sub_str
            result.append(document)
        return result

    ##### metadata edit methods
    def _read_tag_file(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    
    def _read_url_table(self, file_path):
        return pd.read_csv(file_path, header=0, index_col=0)

    def _replace_metadata(self, metafilename:str, replacer:dict={"_":" ", "•":"·"})->str:
        for key, value in replacer.items():
            metafilename = metafilename.replace(key, value)
        return metafilename

    def _strip_replace_text(self, s:str)->str:
        regex = '([^가-힣0-9a-zA-Z.,·•%↓()\s\\\])'
        # regex = "([^가-힣0-9a-zA-Z])"
        s = re.sub(pattern=regex, repl="", string=s)
        s = self._replace_metadata(metafilename=s, replacer={" ":"", '•':'·', 'Ⅰ':'', 'Ⅱ':'', "_":""})
        return s
    
    def _get_category_from_source(self, source:str)->str:
        """get category from Document object metadata['source'] and parse directory(for category use.)"""
        parsed_source = source.split("\\")
        dir_source = parsed_source[-2]
        return self._replace_metadata(dir_source)
    
    def _process_document_metadata(self, documents:list)->list:
        """get metadata edit internal methods and integrate all. """
        metadata_json = self._read_tag_file(self.path_metadata)
        url_table = self._read_url_table(self.path_url_table)

        for document in documents:
            #### get source from Document metadata
            meta_source = document.metadata["source"]
            meta_source_parsed = meta_source.split("\\")

            #### category
            document.metadata["category"] = self._get_category_from_source(meta_source)

            #### title
            meta_source_parsed_file_name = meta_source_parsed[-1]
            meta_source_parsed_get = meta_source_parsed_file_name[3:-3]
            result = self._replace_metadata(metafilename=meta_source_parsed_get)
            document.metadata["title"] = result
            
            #### tag
            title = document.page_content.split("\n")[0]
            title_parsed = self._strip_replace_text(title)
            document.metadata["tag"] = metadata_json[title_parsed]

            #### url
            result = url_table.loc[url_table["source"] == meta_source_parsed_file_name]["url"].values[0]

            if result is np.nan :
                document.metadata["url"] = ""
            else :
                document.metadata["url"] = result

        return documents
    
    ##### get corpus
    def get_corpus(self) -> dict:
        """self.storage가 존재한다면 dict로 결과 return함."""
        if not self.storage :
            raise ValueError("loader에 storage가 생성되지 않았습니다. load 함수를 실행하거나 storage를 확인하고 다시 실행하세요.")     
        return {str(uuid.uuid4()): doc.page_content for doc in self.storage}

##################################################################################################################################################

class TokenDBLoader(BaseDBLoader):
    """ 
        fix loading sequence

        before: document -> split -> extract title
        after: document -> title -> split 
    """

    def load(self, is_split=False, is_regex=False, show_progress=True, use_multithreading=True) -> list[Document]:
        """ Get Directory Folder and documents -> parse, edit metadata -> langchain Document list. 
        
            args :
                is_split: whether split or not(text_splitter)
                is_regex: apply regex to edit document form. 
                show_progress: show progress -> from LangChain.
                use_multithreading: use multithread(cpu) -> from LangChain. """
        #timecheck
        start_time = datetime.now()
        # document pre-processing
        for db_folder in os.listdir(self.path_db):
            db_folder_abs = os.path.join(self.path_db, db_folder)
            directory_loader = DirectoryLoader(path=db_folder_abs, loader_cls=self.loader_cls, show_progress=show_progress, use_multithreading=use_multithreading)
            doc_list = directory_loader.load()

            ## 여기에서 제목추출하고 보내는게 맞을듯... (제목 추출 순서 변경 완료..) 231215
            doc_list = self._process_document_metadata(doc_list)

            if is_regex:
                doc_list = self._result_to_regex(doc_list)            
            if is_split:
                doc_list = self.text_splitter.split_documents(doc_list)

            self.storage.extend(doc_list)

        #timecheck
        end_time = datetime.now()
        print("loading Documents takes", (end_time-start_time).total_seconds(), "seconds.")

        return self.storage

class TeamALoader(TokenDBLoader):
    def _strip_replace_text(self, s: str)->str:
        regex = '([^가-힣0-9a-zA-Z])'
        s = re.sub(pattern=regex, repl="", string=s)
        return s
    
class TeamBLoader(TokenDBLoader):
    """ Just Inherite BaseDBLoader. Recommand using this class for clarity. """