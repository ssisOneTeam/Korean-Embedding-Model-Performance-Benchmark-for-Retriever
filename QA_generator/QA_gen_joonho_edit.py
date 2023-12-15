import os
import re
import tqdm
from openai import OpenAI
import pandas as pd

from settings import OPENAI_API_KEY

llm = {
    'gpt-3.5':"gpt-3.5-turbo",
    'gpt-4':"gpt-4-1106-preview"
}

client = OpenAI(
    api_key=OPENAI_API_KEY
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
    questions = []
    answers = []
    documents = []

    if len(data) % 3:
        print("데이터 형식 오류가 발생했습니다!")
        return
    
    for i in range(0, len(data), 3):
        questions.append(data[i])
        answers.append(data[i+1])
        documents.append(data[i+2])

    df = pd.DataFrame({
        'Question': questions,
        'Answer': answers,
        'Documents': documents
    })

    return df

if __name__ == "__main__":
    print("현재 경로 : ",os.getcwd())
    ABS_DIR = "../embeddingtest/data/test/"
    df = pd.DataFrame(columns=['Question', 'Answer', 'Documents'])
    chapter_list = os.listdir(ABS_DIR)
    outlist = ["readme.md", ".DS_Store"]
    md_contents = []
    file_list = []
    Gen_data = []
    items = []

    temp_gen_dir = 'temp_gen'
    backup_dir = os.path.join(temp_gen_dir, 'backup')

    if not os.path.exists(temp_gen_dir):
        os.makedirs(temp_gen_dir)
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    for title in chapter_list:
        if title in outlist:
            continue
        
        absolute_path = os.path.abspath(os.path.join(ABS_DIR, title))
        for root, dirs, files in os.walk(absolute_path):
            for file in files:
                if file.endswith(".md"):
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        file_list.append(file)
                        md_contents.append(f.read())

    print("MD 파일 파싱 완료")

    for title_of_file, contents in zip(file_list, md_contents):
        content = list(contents.split('\n\n'))

        for paragraph in content[1:]:
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
            
            if len(paragraph) > 80:
                res = qa_generate(prompt['system'], qa_gen_long)
            else:
                res = qa_generate(prompt['system'], qa_gen_short)
            
            qa_dataset.append(res.replace('\n\n', '\n'))

            for item in qa_dataset:
                Gen_data.extend([s.strip() for s in re.split(pattern='\([QA]\d*\)|\(Doc\)', string=item) if s])
                items.append(item)

            csv_file_name = f"temp_gen/{title_of_file.split('.')[0]}.csv"
            txt_file_name = f"temp_gen/backup/backup_{title_of_file.split('.')[0]}.txt"

            backup = "\n\n".join(items)
            text_to_save = backup

            with open(txt_file_name, mode='a+', encoding="utf-8", ) as txtfile:
                txtfile.write(text_to_save + '\n')

            try:
                OurData = saveCSV(Gen_data)
                if not os.path.exists(csv_file_name):
                    OurData.to_csv(csv_file_name, mode='w', encoding='utf-8', index=False)
                else:
                    OurData.to_csv(csv_file_name, mode='a', encoding='utf-8', index=False, header=False)

                print(f"*** Data:{title_of_file} -> csv 생성 완료 ***")
            except Exception as e:
                print(f"CSV 저장 중 오류 발생: {e}")

            Gen_data = []
            items = []
