# Korean-Embedding-Model-Performance-Benchmark-for-Retriever
Korean Sentence Embedding Model Performance Benchmark for RAG

## 목표 : 한국어 임베딩 모델에 대한 성능 벤치마킹

### 실험한 배경
`pip install -r requirement.txt`

### 배경
  1. 기존에 사용한 한국어 임베딩 모델의 경우 AVG Score가 가장 높은 KoSimCSE-RoBERTa-multitask를 사용함.
     
### 가정
  1. 우리의 가정 : 한국어 임베딩 모델에 대한 하이퍼 파라미터 조합에 따라 Retriever가 더 잘 되나 안되나
     
### 방법
  1. 다양한 모델을 실험해보고 그중 가장 좋은 모델을 선정 (hitrate로 평가)
      1. (Model list)
      2.  왜 요런 Model List 를 만들었는지? (이유 : 왜 모든 모델들이 다 SBERT 기반 모델들인지?)
      3.  hitrate를 평가지표로 사용한 이유? 근거
  2. 하이퍼 파라미터 조합
      1. 어떤 하이퍼 파라미터 조정할거고
      2. 각 하이퍼 파라미터 어느 범위내에서 조정할거고
      3. 어떻게 조정할거다. (전수조사 or GridsearchCV, etc… )
### 실험결과
    1. 테이블형태로 보여주는게 GOAT
    2.  실험 01 결과
    3.  실험 02 결과
    4.  최종 결과

### 참고자료
    1. 참조한 자료 목록
