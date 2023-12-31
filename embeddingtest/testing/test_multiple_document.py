from document.mdLoader import BaseDBLoader, TeamALoader
import os

# 현재 파일의 절대 경로
current_file_path = os.path.abspath(__file__)
# 현재 파일이 위치한 디렉토리의 경로
current_directory = os.path.dirname(current_file_path)

path_db = os.path.join(current_directory, "data/teamA")
path_metadata = os.path.join(current_directory, "document/meta_team_a.json")
path_url_table = os.path.join(current_directory, "document/url_table_team_a.csv")

loader = TeamALoader(path_db=path_db, path_metadata=path_metadata, path_url_table=path_url_table)
documents = loader.load(is_split=False, is_regex=False)

## document 실행 확인, main 경로로 빼면 실행 잘 됨.
print(documents[0])