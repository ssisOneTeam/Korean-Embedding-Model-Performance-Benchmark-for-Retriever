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
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.document import Document

from datetime import datetime

class BaseDBLoader:
    """markdownDB folder에서 불러온 다음에 폴더별로 내부에 있는 내용 Load해서 Split하고 저장함"""

    def __init__(self, path_db: str, loader_cls=UnstructuredMarkdownLoader):
        #timecheck
        start_time = datetime.now()
        # textsplitter config
        self.text_splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", " ", ""],
            chunk_size=200,
            chunk_overlap=10,
            is_separator_regex=False,
        )

        # loaderclass config
        self.loader_cls = loader_cls
        # md 파일 담고 있는 전체 디렉터리 경로
        self.path_db = path_db
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
                doc_list = self.__result_to_regex(doc_list)            
            if is_split:
                doc_list = self.text_splitter.split_documents(doc_list)
            self.storage.extend(doc_list)
        
############################################################## 11-27 metadata edit
        # metadata edit
        self.storage = self.__process_document_metadata(self.storage)

        #timecheck
        end_time = datetime.now()
        print("loading Documents takes", (end_time-start_time).total_seconds(), "seconds.")

        return self.storage

    def __result_to_regex(self, doc_list:list[Document]) -> list[Document]:
        """regex splitter (Document)"""
        regex = '([^가-힣0-9a-zA-Z.,·•%↓()\s\\\])'
        result = []
        for document in doc_list:
            sub_str = re.sub(pattern=regex, repl="", string=document.page_content)
            document.page_content = sub_str
            result.append(document)
        return result

    ##### metadata edit methods
    def __read_tag_file(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    
    def __read_url_table(self, file_path):
        return pd.read_csv(file_path, header=0, index_col=0)

    def __replace_metadata(self, metafilename:str, replacer:dict={"_":" ", "•":"·"})->str:
        for key, value in replacer.items():
            metafilename = metafilename.replace(key, value)
        return metafilename

    def __strip_replace_text(self, s: str)->str:
        regex = '([^가-힣0-9a-zA-Z.,·•%↓()\s\\\])'
        s = re.sub(pattern=regex, repl="", string=s)
        s = self.__replace_metadata(metafilename=s, replacer={" ":"", '•':'·', 'Ⅰ':'', 'Ⅱ':'', "_":""})
        return s
    
    def __process_document_metadata(self, documents:list)->list:
        """get metadata edit internal methods and integrate all. """
        metadata_json = self.__read_tag_file("document/metadata.json")
        url_table = self.__read_url_table("document/url_table.csv")

        for document in documents:
            #### title
            meta_source = document.metadata["source"]
            meta_source_parsed = meta_source.split("\\")[-1]
            meta_source_parsed_get = meta_source_parsed[3:-3]

            result = self.__replace_metadata(metafilename=meta_source_parsed_get)
            document.metadata["title"] = result
            
            #### tag
            title = document.page_content.split("\n")[0]
            title_parsed = self.__strip_replace_text(title)
            document.metadata["tag"] = metadata_json[title_parsed]

            #### url
            result = url_table.loc[url_table["source"] == meta_source_parsed]["url"].values[0]

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