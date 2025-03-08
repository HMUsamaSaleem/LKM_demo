from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import re
from time import sleep
df = pd.read_csv("C:/Users/PC/Desktop/pixeledge/lkm/dataset/inputfile/23oct.csv")
driver = webdriver.Firefox()
first_10_lines_list = []
for index, row in df.iterrows():
    url = row["SEC.gov URL"]
    driver.get(url)
    sleep(5)
    page_text = driver.find_element(By.TAG_NAME, 'body').text.lower()
    first_10_lines = page_text.splitlines()[:15]
    first_10_lines_list.append(first_10_lines)
driver.quit()
pattern_first_tenth = r"(?:^|\s)(first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth)(?:\samendment)?"
pattern_amendment_no = r"\s*?amendment\s*no\.?\s*(\d+)"
for line in first_10_lines_list:
    line = str(line)
    match_first_tenth = re.search(pattern_first_tenth, line)
    match_amendment_no = re.search(pattern_amendment_no, line)
        
    if match_first_tenth:
        amendment_name = match_first_tenth.group(1) 
        if amendment_name:
            amendment_number = {
                    "first": "1",
                    "second": "2",
                    "third": "3",
                    "fourth": "4",
                    "fifth": "5",
                    "sixth": "6",
                    "seventh": "7",
                    "eighth": "8",
                    "ninth": "9",
                    "tenth": "10"
                }.get(amendment_name)
            if amendment_number:
                df.at[index, "Amendment number"] = amendment_number
                break 
    elif match_amendment_no:
        amendment_number = match_amendment_no.group(1)
        df.at[index, "Amendment number"] = amendment_number
        break
    else:
        df.at[index, "Amendment number"] = None
print(df["Amendment number"])
df.to_csv("C:/Users/PC/Desktop/LKM_demo/lkm/dataset/outputfile/OUtput.csv")