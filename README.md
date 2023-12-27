# Korean-Embedding-Model-Performance-Benchmark-for-Retriever
Korean Sentence Embedding Model Performance Benchmark for RAG System

## Ⅰ. 개요

#### **1. 실험목표**
  > 한국어 임베딩 모델에 Domain Adaptation을 진행함과 동시에 하이퍼파라미터 조정에 따라 Retriever 성능변화가 얼마나 일어나는지 실험하고자한다.

#### **2. 실험배경**

- 기존 프로젝트의 후속실험으로 자세한 내용은 아래 항목을 참고할 것.  
  - [SSiS TeamA - Ask-for-Welfare Service](https://github.com/ash-hun/Ask-for-Welfare)  
  - [SSiS TeamB - Advanced Semantic Search Engine](https://github.com/SSiS-TeamB/RAG)  
    
- Domain Adaptation과 RAG
  - 공통적으로 복지 도메인에 특화된 RAG System을 구축하고자 함.
   
  - 범용 Korean Embedding Model을 복지 도메인에 특화되게 DAPT(Domain Adaptation)을 적용하였음.
    - 한국어 Embedding Model 중 AVG Score가 가장 높은 `KoSimCSE-RoBERTa-multitask` Model 사용  

  - DAPT와 RAG System에서의 상관관계 개선 필요성 발견  
    - Retriever 결과의 미흡함 확인
    - 더 나은 성과를 위해 추가적인 실험(=DAPT, Algorithm, etc..)과 비교 분석 필요

#### 3. 실험환경
- 기획
   - [복지로](https://www.bokjiro.go.kr/ssis-tbu/index.do)에서 오픈소스로 공개된 `2023 나에게 힘이되는 복지서비스` pdf 책자를 이용해 추가적인 데이터셋을 생성하여 실험을 진행
   - `KoSimCSE-RoBERTa-multitask`을 사용했으나 타 임베딩 모델과의 성능비교가 필요
   - 특정 하이퍼파라미터 조합에 따라 추가적인 성능개선이 가능성 확보

- 사용 라이브러리


      $ pip install -r requirement.txt


## Ⅱ. 가정
  위 내용을 통해 기존 프로젝트에서 적용된 방식은 근거와 실험절차가 충분치 않으며 이를 보강할 수 있는 후속작업이 필요하다.  
  즉, **임베딩 모델의 기본성능이 높으면 높을수록 DAPT를 진행했을시 더 높은 성능을 보일것**이라는 가정을 세우고 이를 증명하기 위한 실험을 진행하려고 한다. 

## Ⅲ. 방법

#### 1. 데이터셋 생성
  1. 생성방식
  2. 비용산정

#### 2. 성능비교
  1. 고성능의 Retriever 결과도출을 위한 다양한 한국어 문장 임베딩 모델들에 대한 성능비교 (HitRate)
    1. 다양한 한국어 문장 임베딩 모델 리스트업
      - 모델 선정이유/근거
      - 평가지표 선정이유/근거
    2. Retriever 성능평가 진행
      - 성능평가 방식 선정
      - 성능평가 진행
    3. 기존 모델(=KoSimCSE-RoBERTa-multitask)과의 Performance Benchmarking 진행
      
  2. 가장 높은 성능을 가지는 모델에 대하여 하이퍼파라미터 조정 진행
    1. 하이퍼파라미터 선정
    2. 하이퍼파라미터 튜닝후 성능평가 진행
      - 성능평가 방식 선정 (전수조사, GridsearchCV, etc… )
      - 성능평가 진행

  3. RAG System 적용

## Ⅳ. 실험결과 (※ 전/후 결과비교가 중요)
  1. Embedding Model 비교/선정  
  2. Retreiver 성능측정  
    1. Embedding Model 교체 전/후 Retriever 성능비교  
    2. BM25, Re-Rank, Filtering 적용 전/후 Retriever 성능비교  
  3. 최종 실험결과 도출  

## Ⅴ. 컨트리뷰터

<table align="center">
  <tr>
    <td align="center">
      <a href="https://github.com/PangPangGod">
        <img src="https://github.com/PangPangGod.png" width="100px;" alt="송준호"/><br />
        <sub><b>송준호</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/ash-hun">
        <img src="https://github.com/ash-hun.png" width="100px;" alt="최재훈"/><br />
        <sub><b>최재훈</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/MoonHeesun">
        <img src="https://github.com/MoonHeesun.png" width="100px;" alt="문희선"/><br />
        <sub><b>문희선</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/Noveled">
        <img src="https://github.com/Noveled.png" width="100px;" alt="김민식"/><br />
        <sub><b>김민식</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/myeongjun1007">
        <img src="https://github.com/myeongjun1007.png" width="100px;" alt="현명준"/><br />
        <sub><b>현명준</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/kha-jaejun">
        <img src="https://github.com/kha-jaejun.png" width="100px;" alt="가재준"/><br />
        <sub><b>가재준</b></sub>
      </a>
    </td>
  </tr>
</table>

### Ⅵ. 참고자료
  1. 참조한 자료 목록
