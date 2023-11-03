import pandas as pd
input_file = pd.read_excel("C:/Users/PC/Desktop/pixeledge/lkm/dataset/inputfile/prostprocessed_output_result_1.xlsx")
df = input_file
# Convert the `Title Name` column to string
df['Title Name'] = df['Title Name'].astype(str)
# Filter the DataFrame to only include rows where the Amendment Number column is already None
df_filtered = df[df['Amendment number'].isnull()]
# Iterate over the filtered DataFrame and update the Amendment Number column
for i, row in df_filtered.iterrows():
    if row['Title Name'].split(" ")[0] == "AMENDMENT" and row['Title Name'].split(" ")[-1] == "AGREEMENT":
        df.loc[i, "Amendment number"] = None
    elif row['Title Name'].split(" ")[0] == "CREDIT" and row['Title Name'].split(" ")[-1] == "AGREEMENT":
        df.loc[i, "Amendment number"] =None
    else:
        df.loc[i, "Amendment number"] = 1
# Save the updated file as an output
df.to_excel('C:/Users/PC/Desktop/pixeledge/lkm/dataset/outputfile/output.xlsx', index=False)