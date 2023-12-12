# How to use QA_gen.py

### 설명
0. `api-key`를 `os` 모듈을 통해 불러들이게 해놓았으나 임의로 매핑해주시면 됩니다. (해당 변수에 잘 들어가기만 하면 됩니다.)
1. `ABS_DIR` 경로 확인 (상대경로로 매핑해놓았으나 개별환경의 경우 한번 더 확인해주세요.)
2. `outlist` 확인
    - 해당 경로에 각 Chapter별 MD파일외 다른 파일이 있다면 삭제하거나 `outlist`에 기입해주세요.
3. `for contents in md_contents[:1]: ...`부분을 보면 임시로 1개 제도에 대해서만 테스트 되게끔 해놓았습니다. 실제 생성을 돌릴땐 해당 부분을 수정하여 전체가 돌아가게끔 해주세요.
4. 주요변수설명
    - `md_contents` : 각 제도별로 마크다운 내용이 들어갑니다.
    - `file_list` : 모든 파일 명이 들어가있는 파일리스트입니다.
    - `Gen_data` : 생성된 데이터가 Question, Answer, Documents별로 들어갑니다. 단, [[Q, A, Doc], [Q, A, Doc], [Q, A, Doc], ...]의 형태가 아니고 [Q, A, Doc, Q, A, Doc, Q, A, Doc, Q, A, Doc, Q, A, Doc, ..]의 형태입니다.

    이후 `saveCSV()`에서 형태를 고려하여 Dataframe으로 변환하게 해두었으니 최종적으로 데이터셋을 추출했을 때 정상적으로 들어가는지 확인만 해주시면 됩니다.

### 실행
    $ python QA_gen.py

### 비고

- 이전에 실행할 때보다 gpt-4 호출이 느립니다. 요부분은 왜 그런지 모르겠네요. openai api쪽 문제인거 같아요.
- 테스트 실행 결과 (동일 경로 OurData.csv 참조)
