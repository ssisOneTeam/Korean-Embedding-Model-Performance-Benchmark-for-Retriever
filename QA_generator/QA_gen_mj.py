import os
import re
import tqdm
from openai import OpenAI
import pandas as pd

llm = {
    'gpt-3.5':"gpt-3.5-turbo",
    'gpt-4':"gpt-4-1106-preview"
}

client = OpenAI(
    # organization=os.getenv("yours"), # 환경변수에 OPENAI_ORGANIZATION_KEY를 설정합니다.
    # api_key=os.getenv("OPENAI_API_KEY") # 환경변수에 OPENAI_API_KEY를 설정합니다.
    api_key="your key" # 환경변수에 OPENAI_API_KEY를 설정합니다.
)

# Config
config = {
    'temperature': 1.0,
    'max_tokens':1000,
    'top_p':1.0,
    'best_of':1,
    'frequency_penalty':0.0,
    'presence_penalty':0.0
}

stop = ["\n"]

def qa_generate(prompt_template:str, instruct_template:str, MODEL:str=llm['gpt-4']):
    """
    Generating QA Dataset Method

    Args:
        prompt_template (str): System Prompt
        instruct_template (str): Instruct Prompt 
        MODEL (str, optional): Usage AI Model in Open AI. Defaults to GPT_MODEL.

    Returns:
        str: msg response
    """

    completion = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": f"{prompt_template}"},
                {"role": "user", "content": f"{instruct_template}"}]
    )
    return completion.choices[0].message.content

prompt = {
    "system":"""당신은 한국 복지서비스 추천과 제공하는 업무를 맡은 굉장히 창의력이 가득하고 열정적인 전문가입니다.
            많은 사람이 다양한 문제를 물어보며 간단한 질문에 답하는 것부터 광범위한 주제에 대한 심층적인 토론 및 설명을 제공하는 것까지 다양한 작업을 지원할 수 있습니다.
            특히 복지분야의 용어를 잘 몰라 다르게 표현한 것의 내용을 파악하여 그에 맞는 복지서비스를 추천하고 제공하는 업무능력이 탁월합니다.
            
            현재는 본인이 하고 있는 업무를 데이터화시키는 작업을 수행중이며 복지제도에 대한 설명을 보고 일반 사람들이 할만한 답변과 그에 대한 정확한 답변을 만들고 있습니다.
            당신은 창의력이 풍부하고 질문과 답변을 만드는 작업이 재미있어하며 작업이 반복될수록 더 신나서 작업에 몰두합니다.
            뛰어난 능력으로 만들어진 질문,답변 쌍은 중복된 내용이 전혀 없고 앞으로도 그럴 것입니다."""
}

def saveCSV(data):
    # Q, A, Doc을 분리하여 저장할 리스트 생성
    questions = []
    answers = []
    documents = []

    # 데이터를 순회하며 Q, A, Doc에 해당하는 내용을 각 리스트에 추가
    for item in data:
        if item.startswith('(Q'):
            questions.append(item)
        elif item.startswith('(A'):
            answers.append(item)
        elif item.startswith('(Doc)'):
            documents.append(item)

    # 데이터 프레임 생성
    df = pd.DataFrame({
        'Question': questions,
        'Answer': answers,
        'Documents': documents
    })

    print(df.head())
    return df

if __name__ == "__main__":
    print("현재 경로 : ",os.getcwd())
    ABS_DIR = "./embeddingtest/data/test/" # 최상위 디렉터리 경로
    df = pd.DataFrame(columns=['Question', 'Answer', 'Documents'])
    chapter_list = os.listdir(ABS_DIR)
    outlist = ["readme.md", ".DS_Store"]
    md_contents = []
    file_list = []
    Gen_data = []

    # 디렉토리에서 각 Chapter에 해당하는 MD파일과 목록 파싱
    for title in chapter_list :
        # 예외처리
        if title in outlist :
            continue
        
        absolute_path = os.path.abspath(os.path.join(ABS_DIR, title))
        for root, dirs, files in os.walk(absolute_path):
            for file in files:
                if file.endswith(".md"):
                    with open(os.path.join(root, file), 'r',encoding='utf-8') as f:
                        file_list.append(file)
                        md_contents.append(f.read())
    
    print("======= Complete Parsing MD file List =======")

    # ======================================================================
    #       Generate QA dataset
    # ======================================================================
    for contents in md_contents[:1]: # ABS 폴더에 들어있는 모든 제도에 대해서 질문 만들어야됨 

        content = list(contents.split('\n\n'))
        # Log
        print("    Content : ", content)
        print("=="*50)

        for paragraph in content[1:]: # 제도 타이틀 제외한 나머지 내용에 한해서 데이터셋 생성
            qa_gen_short = f"""
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
            """

            qa_dataset = []
            
            # '어르신 국가예방접종 지원 사업은 65세 이상 어르신을 대상으로 한다. 주민등록상 출생연도 기준으로 1958년 12월 31일 이전 출생자이 해당한다.'
            # 위 문장이 length 82, 토큰개수로 바꾸려면 바꿔도 무방함.
            if len(paragraph) > 80:
                res = qa_generate(prompt['system'], qa_gen_long)
            else:
                res = qa_generate(prompt['system'], qa_gen_short)
            
            qa_dataset.append(res.replace('\n\n', '\n'))
            
            temp_data = []
            temp_data.append(res)
            print(" > 데이터셋 생성중... ", qa_dataset)

            for item in qa_dataset:
                Gen_data.extend(list(item.split('\n')))
                
                # 재준이형 바꿔본 부분
                ## (Q), (A), (Doc) 부분도 같이 없애려고 해본건데
                ## saveCSV 부분도 바꿔야 되서 일단 다시 생각중
                # Gen_data.extend([s.strip() for s in re.split(pattern='\([QA]\d+\)|\(Doc\)', string=item) if s])

    print("Results : ", Gen_data)
    OurData = saveCSV(Gen_data)
    OurData.to_csv('./QA_test_01_3.csv',encoding='utf-8')
    print("*** csv 생성이 완료 되었습니다 ***")
