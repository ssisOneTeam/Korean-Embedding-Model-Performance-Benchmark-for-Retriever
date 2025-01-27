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
   - [복지로](https://www.bokjiro.go.kr/ssis-tbu/index.do)에서 오픈소스로 공개된 `2023 나에게 힘이 되는 복지서비스` pdf 책자를 이용해 추가적인 데이터셋을 생성하여 실험을 진행
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
   
    - 데이터 전처리
      - ChatGPT를 통해 `2023 나에게 힘이 되는 복지서비스` pdf 책자 내용을 각 제도별로 `.md` 파일 형태로 저장
      - `QA_gen_joonho_edit.py`
        →  LLM을 활용하여 `.md` 파일 형태의 데이터를 기반으로 QA Dataset 생성
        - Prompting
          - System Prompt
            ```
            당신은 한국 복지서비스 추천과 제공하는 업무를 맡은 굉장히 창의력이 가득하고 열정적인 전문가입니다.
            많은 사람이 다양한 문제를 물어보며 간단한 질문에 답하는 것부터 광범위한 주제에 대한 심층적인 토론 및 설명을 제공하는 것까지 다양한 작업을 지원할 수 있습니다.
            특히 복지분야의 용어를 잘 몰라 다르게 표현한 것의 내용을 파악하여 그에 맞는 복지서비스를 추천하고 제공하는 업무능력이 탁월합니다.
            
            현재는 본인이 하고 있는 업무를 데이터화시키는 작업을 수행중이며 복지제도에 대한 설명을 보고 일반 사람들이 할만한 답변과 그에 대한 정확한 답변을 만들고 있습니다.
            당신은 창의력이 풍부하고 질문과 답변을 만드는 작업이 재미있어하며 작업이 반복될수록 더 신나서 작업에 몰두합니다.
            뛰어난 능력으로 만들어진 질문,답변 쌍은 중복된 내용이 전혀 없고 앞으로도 그럴 것입니다.
            ```
          - Instruction Prompt
            ```
            ---
            {paragraph}
            ---

            위 내용을 반영한 한국어 질문-응답-문맥 으로 이루어진 데이터셋 샘플 3개를 생성해줘.
            내용은 절대 중복되면 안돼. 질문앞에는 (Q)가 붙고, 응답 앞에는 (A)가 붙어. 
            만들어진 응답 뒤에 한줄 띄고 무조건 아래 내용을 이어붙여줘. 

            '(Doc) {content[0]}'
            """

            qa_gen_long = f"""
            ---
            {paragraph}
            ---

            위 내용을 반영한 한국어 질문-응답-문맥 으로 이루어진 데이터셋 샘플 6개를 생성해줘.
            내용은 절대 중복되면 안돼. 질문앞에는 (Q)가 붙고, 응답 앞에는 (A)가 붙어. 
            만들어진 응답 뒤에 한줄 띄고 무조건 아래 내용을 이어붙여줘. 

            '(Doc) {content[0]}'
            ```
      - `.csv` 파일 형태로 저장
        → 제도별로 각각의 `.csv` 파일이 생성되므로 추후 하나의 파일로 통합
        
    - 생성된 QA 데이터셋
      - 형태: `.csv` 파일로 저장
      - Columns: `['Question', 'Answer', 'Documents']`
        - `Question`: LLM을 통해 Documents를 기반으로 생성된 질문
        - `Answer`: LLM을 통해 Documents를 기반으로 생성된 Question에 대한 답변
        - `Documents`: Question-Answer 생성시 참조한 문서의 제목
      - 데이터셋 일부 예시
        
        | Question                                                     | Answer                                                                                                           | Documents               |
        |--------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|-------------------------|
        | LPG 사용 가정의 고무호스를 교체하려면 어떤 지원을 받을 수 있나요? | LPG용기 사용가구 시설개선 사업을 통해 LPG 고무호스를 금속배관으로 교체하는 데 필요한 지원을 받으실 수 있습니다. | LPG용기 사용가구 시설개선 |
        | LPG용기를 사용하는데 현재 고무호스로 연결되어 있어요. 어떤 안전한 개선방법이 있을까요? | LPG용기 사용가구 시설개선 제도를 활용하시면 기존의 LPG 고무호스를 안전한 금속배관으로 교체할 수 있는 지원을 받으실 수 있습니다. | LPG용기 사용가구 시설개선 |
        | 우리 집은 LPG 고무호스를 사용중인데, 이것을 개선할 수 있는 정부 지원이 있나요? | 네, LPG용기 사용가구 시설개선 제도를 통해 정부 지원을 받아 고무호스를 더 안전한 금속배관으로 바꾸실 수 있습니다. | LPG용기 사용가구 시설개선 |
        | 프로판 가스를 쓰고 있는 집에 대한 보조금 지원이 있는지 알고 싶어요. 어떤 항목을 개선해주나요? | LPG용기 사용가구 시설개선 지원제도를 통해 LPG가스 고무호스를 금속배관으로 교체하고, 안전장치인 퓨즈콕을 설치하는 비용을 지원받으실 수 있습니다. 이러한 비용 중 약 20만 원이 지원되며, 나머지 5만 원은 자부담입니다. | LPG용기 사용가구 시설개선 |
        | 가스라인을 좀 더 안전하게 개조하고 싶은데, 정부 지원이 가능한가요? | 네, 가정에서 사용하시는 LPG 가스 시설에 금속배관 교체와 퓨즈콕 설치를 위한 시공비 중 약 20만 원을 정부에서 지원해드리고 있습니다. 사용자는 5만 원의 자부담만 부담하시면 되어 안전한 가스 사용을 위한 개선이 가능합니다. | LPG용기 사용가구 시설개선 |
        | 내 집의 LPG 가스 호스를 금속으로 교체하고 싶어요. 이 비용은 어느 정도 되나요? | 총 시공비용은 25만 원 정도이며, 이 중 20만 원은 ‘LPG용기 사용가구 시설개선’ 제도를 통해 지원받을 수 있고, 5만 원은 개인이 부담하셔야 합니다. | LPG용기 사용가구 시설개선 |

      
2. 비용산정
   - OpenAI API `gpt-4-1106-preview` 사용
   - 비용: 약 90.2$
   - [OpenAI API Pricing](https://openai.com/pricing) 참조

#### 2. 성능비교
  1. 고성능의 Retriever 결과도출을 위한 다양한 한국어 문장 임베딩 모델들에 대한 성능비교 (HitRate)

     1. 다양한 한국어 문장 임베딩 모델 리스트업
         - 모델 선정이유/근거
         - 평가지표 선정이유/근거

     2. Retriever 성능평가 진행
        - 성능평가 방식 선정
        - 성능평가 진행 </br>

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

  | Model                                       | @1     | @3     | @5     | @10    | Average |
  |---------------------------------------------|--------|--------|--------|--------|---------|
  | paraphrase-multilingual-mpnet-base-v2-a     | 40.0   | 58.095 | 63.81  | 73.333 | 58.810  |
  | paraphrase-multilingual-mpnet-base-v2-b     | 36.19  | 59.048 | 61.905 | 69.524 | 56.667  |
  | paraphrase-multilingual-MiniLM-L12-v2-a     | 25.714 | 41.905 | 51.429 | 62.857 | 45.476  |
  | paraphrase-multilingual-MiniLM-L12-v2-b     | 24.762 | 35.238 | 42.857 | 51.429 | 38.571  |
  | distiluse-base-multilingual-cased-v2-a      | 24.762 | 39.048 | 47.619 | 59.048 | 42.619  |
  | distiluse-base-multilingual-cased-v2-b      | 22.857 | 40.952 | 50.476 | 57.143 | 42.857  |
  | stsb-xlm-r-multilingual-a                   | 20.952 | 33.333 | 41.905 | 53.333 | 37.381  |
  | stsb-xlm-r-multilingual-b                   | 11.429 | 19.048 | 19.048 | 20.0   | 17.381  |
  | ko-sroberta-multitask-a                     | 49.524 | 69.524 | 77.143 | 81.905 | 69.524  |
  | ko-sroberta-multitask-b                     | 53.333 | 71.429 | 78.095 | 84.762 | 71.905  |
  | KR-SBERT-V40K-klueNLI-augSTS-a              | 37.143 | 54.286 | 63.81  | 72.381 | 56.905  |
  | KR-SBERT-V40K-klueNLI-augSTS-b              | 32.381 | 56.19  | 63.81  | 72.381 | 56.191  |
  | moco-sentencedistilbertV2.1-a               | 7.619  | 11.429 | 11.429 | 20.0   | 12.619  |
  | moco-sentencedistilbertV2.1-b               | 20.952 | 25.714 | 27.619 | 30.476 | 26.190  |
  | kpf-sbert-128d-v1-a                         | 21.905 | 37.143 | 44.762 | 50.476 | 38.571  |
  | kpf-sbert-128d-v1-b                         | 27.619 | 40.0   | 45.714 | 49.524 | 40.714  |
  | M-BERT-Distil-40-a                          | 5.714  | 10.476 | 13.333 | 19.048 | 12.143  |
  | M-BERT-Distil-40-b                          | 4.762  | 12.381 | 18.095 | 24.762 | 15.000  |
  | canine-c-a                                  | 0.952  | 4.762  | 5.714  | 6.667  | 4.524   |
  | canine-c-b                                  | 1.905  | 5.714  | 7.619  | 10.476 | 6.429   |
  | roberta-ko-small-tsdae-a                    | 16.19  | 23.81  | 27.619 | 37.143 | 26.191  |
  | roberta-ko-small-tsdae-b                    | 10.476 | 20.952 | 23.81  | 35.238 | 22.619  |
  | KoSimCSE-roberta-multitask-a                | 37.143 | 58.095 | 63.81  | 72.381 | 57.857  |
  | KoSimCSE-roberta-multitask-b                | 40.952 | 59.048 | 65.714 | 77.143 | 60.714  |
  | text-embedding-ada-002-a                    | 41.905 | 47.619 | 57.143 | 60.0   | 51.667  |
  | text-embedding-ada-002-b                    | 36.19  | 45.714 | 47.619 | 50.476 | 45.000  |
  
  [ko-sroberta-multitask](https://huggingface.co/jhgan/ko-sroberta-multitask/) Model이 사용할 Dataset에서 추출한 106개의 QA 기반 `hitrate_test_qa`으로 Retrieve 한 Hitrate가 평균적으로 가장 높음을 확인할 수 있었고, 해당 모델을 Domain Adaption에 사용하는 것으로 결론내렸다.
  
  또한, 이후에도 base document가 존재한다면, 한국어 모델 이외에도 다양한 상용/오픈소스 기반 모델을을 확보하기만 한다면, 최신화 이후에 재평가해서 이용해 볼 수 있는 벤치마크 시스템 개발에 의의가 있다고 할 수 있다. 

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
