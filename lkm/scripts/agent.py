import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
df = pd.read_excel("C:/Users/PC/Desktop/pixeledge/lkm/dataset/inputfile/prostprocessed_output_result_3.xlsx")
# Create a list to store the first 10 lines from each webpage
driver = webdriver.Firefox()
keyword1 = "Administrative Agent"
for index, row in df.iterrows():
    url = row["SEC.gov URL"]
    try:
        driver.get(url)
        sleep(5)  # Wait for the page to load (you can adjust the sleep time as needed)
    
        # Get the text from the entire webpage
        page_text = driver.find_element(By.TAG_NAME, 'body').text

        # Split the text into lines and select the first 10 lines
        first_10_lines = page_text.splitlines()[:10]
        for lines in first_10_lines:
            for line in lines:
                if keyword1 in line:
                    # Find the index of the line with the keyword
                    ind = lines.index(line)
                    # Print lines from the beginning up to the line with the keyword
                    for i in range(ind + 1):
                        print(lines[i])
            print("######################################################################################################")
                else:
                    print(None)
    except:
        continue
driver.quit()

            