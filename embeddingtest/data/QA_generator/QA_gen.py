import os
import tqdm
from openai import OpenAI
import pandas as pd

llm = {
    'gpt-3.5':"gpt-3.5-turbo",
    'gpt-4':"gpt-4-1106-preview"
}

client = OpenAI(
    organization=os.getenv("OPENAI_ORGARNIZATION_KEY"), # 환경변수에 OPENAI_ORGANIZATION_KEY를 설정합니다.
    api_key=os.getenv("OPENAI_API_KEY") # 환경변수에 OPENAI_API_KEY를 설정합니다.
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

if __name__ == "__main__":
    ABS_DIR = "../teamA/" # 최상위 디렉터리 경로
    df = pd.DataFrame(columns=['Question', 'Answer', 'Documents'])
    chapter_list = os.listdir(ABS_DIR)
    outlist = ["readme.md", ".DS_Store"]
    md_contents = []
    file_list = []
    test_data = []

    for title in chapter_list :
        # 예외처리
        if title in outlist :
            continue
        
        absolute_path = os.path.abspath(os.path.join(ABS_DIR, title))
        for root, dirs, files in os.walk(absolute_path):
            for file in files:
                if file.endswith(".md"):
                    with open(os.path.join(root, file), 'r') as f:
                        file_list.append(file)
                        md_contents.append(f.read())
    
    print("======= Complete Parsing MD file List =======")

    # ======================================================================
    #       Generate QA dataset
    # ======================================================================
    for content in sorted(md_contents)[:1]:
        qa_gen = f"""
        ---
        {content}
        ---

        위 내용을 반영한 한국어 질문-응답-문맥 으로 이루어진 데이터셋 샘플 10개를 생성해줘.
        내용은 절대 중복되면 안돼. 질문앞에는 (Q)가 붙고, 응답 앞에는 (A)가 붙어. 
        만들어진 응답 뒤에 한줄 띄고 무조건 아래 내용을 이어붙여줘. 제도명은 위 내용의 제목을 사용하면 돼.

        '(Doc) 제도명'
        """

        qa_dataset = []
        
        res = qa_generate(prompt['system'], qa_gen)
        qa_dataset.append(res.replace('\n\n', '\n'))
        
        temp_data = []
        temp_data.append(res)
        print(qa_dataset)

        for item in qa_dataset:
            test_data.extend(list(item.split('\n')))
    print(test_data)


    # 다른방식으로 사용했던 프롬프트 혹시 몰라 냅둬요~
    # qa_gen_2 = f"""
    #         ---
    #         {content}
    #         ---

    #         위 내용을 '본문'이라고 할게. 이제부터 본문을 반영한 한국어 데이터셋 샘플을 10개 생성할거야.
    #         데이터셋은 아래 구조에 따라 만들어야 해.
    #         - Context : 본문의 제목
    #         - Question : 본문의 내용과 관련된 질문, 내용이 중복되면 절대 안돼.
    #         - Answer : Question에 해당하는 정답
    #         - Answer_start : Context에서 Answer가 시작하는 위치인덱스

    #         위 구조를 갖춘 데이터셋을 만들되 중복되는 내용없이 데이터셋을 10개 생성해줘.
    #         전체 형태는 아래처럼 만들면 돼.
    #         "context": ,
    #         "question": ,
    #         "answer":  ,
    #         "answer_start": 
    #         위의 4개가 딕셔너리 형태로 하고, 10개의 데이터셋이 하나의 리스트로 묶으면 돼.
    #         """