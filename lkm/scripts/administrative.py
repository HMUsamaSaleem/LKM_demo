from time import sleep
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from transformers import pipeline
df = pd.read_csv("C:/Users/PC/Desktop/pixeledge/lkm/dataset/inputfile/23oct.csv")
driver = webdriver.Firefox()
first_10_lines_list = []
for index, row in df.iterrows():
    url = row["SEC.gov URL"]
    driver.get(url)
    sleep(5)
    page_text = driver.find_element(By.TAG_NAME, 'body').text
    first_10_lines = page_text.splitlines()[:15]
    first_10_lines_list.append(first_10_lines)
driver.quit()
model_name = "deepset/roberta-base-squad2"
nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)
for i, lines in enumerate(first_10_lines_list):
    context = " ".join(lines)
    question = "what is the name of admministrative agent?"
    QA_input = {'question': question, 'context': context}
    result = nlp(QA_input)
    if result['score'] < 0.5:
        question = "Who is the administrative agent in this text?"
        QA_input = {'question': question, 'context': context}
        result = nlp(QA_input)
        df.loc[i, "Lead Arranger/Bookrunner"] = result['answer']
    if result['score'] < 0.5:
        question = "Who serves as the administrative agent?"
        QA_input = {'question': question, 'context': context}
        result = nlp(QA_input)
        df.loc[i, "Lead Arranger/Bookrunner"] = result['answer']
    if result['score'] < 0.5:
        question = "Who holds the position of administrative agent?"
        QA_input = {'question': question, 'context': context}
        result = nlp(QA_input)
        df.loc[i, "Lead Arranger/Bookrunner"] = result['answer']
    if result['score'] < 0.5:
        lines = str(lines)
        if "Administrative Agent" in lines:
            text_1 = lines.split('as Administrative Agent')
            Agent_name = re.findall(r'\b[A-Z][A-Z\s,]+\b', str(text_1[0]))
            df.loc[i, "Lead Arranger/Bookrunner"] = Agent_name[-1]
        elif "administrative agent" in lines:
            text_1 = lines.split('as administrative agent')
            Agent_name = re.findall(r'\b[A-Z][A-Z\s,]+\b', str(text_1[0]))
            df.loc[i, "Lead Arranger/Bookrunner"] = Agent_name[-1]
        elif "as agent" in lines:
            text_1 = lines.split('as agent')
            Agent_name = re.findall(r'\b[A-Z][A-Z\s,]+\b', str(text_1[0]))
            df.loc[i, "Lead Arranger/Bookrunner"] = Agent_name[-1]
        else:
            df.loc[i, "Lead Arranger/Bookrunner"] = None
print(df["Lead Arranger/Bookrunner"])
df.to_csv("C:/Users/PC/Desktop/pixeledge/lkm/dataset/outputfile1/23oct.csv")