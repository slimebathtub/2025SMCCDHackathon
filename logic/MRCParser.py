import pandas as pd
import sqlite3

''' This script is meant to parse the MRC (Math Resource Center) tutoring schedule
    into a .db file that will be then displayed in the website
    
    The linear_search function is used to find the first occurrence of a key in a
    specific column or row. So that it can be adapted to other schedule formats as
    well. After that I just find the table limits by the "CLOSED" and "HOURS" keywords.
'''

MRC_URL = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vRK33wM-yaF-svgS2vuzaSO_YP-Uh_NeZRP5MVRMIlp9tcOQIvcJRQLbpjhOyd0U73ou_IaW-l9G2Hm"
    "/pub?gid=105984831&single=true&output=csv"
)

#pandas indexing: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html
# most crucial : #df.iloc[y1:y2, x1:x2] # y1:y2 = rows, x1:x2 = columns

SOURCE_DF = pd.read_csv(MRC_URL)

def linear_search(key="CLOSED", start_index=0, axis="col"):
    global SOURCE_DF
    
    if axis not in ["row", "col"]:
        raise ValueError("type must be 'row' or 'col'")
    
    local_df = SOURCE_DF.T.copy() if axis == "row" else SOURCE_DF.copy()
    
   
    arr = local_df.iloc[:, start_index].astype(str) 
    mask = arr.str.contains(key, case=False, na=False) 
    first_pos = next((pos for pos, hit in enumerate(mask) if hit), None)
    
    return first_pos

# relevant table : (finds w gonna find)
# (0,y1) - (x2,y1) 
# (0,y2) - (x2,y2)
# for each column, we may stop at (x,y) if y + 1 == "CLOSED", provided 0 <= y <= y2   
# for example, Friday might finish earlier than other weekdays, so we need to check for that

def main():
    global SOURCE_DF
    # 1. Find y1, y2, and x2, note x1 = 0
    y1 = linear_search("HOURS", start_index=0, axis="col")
    y2 = linear_search("CLOSED", start_index=3, axis="col")
    x2 = linear_search("CLOSED", start_index=y1+1, axis="row")
   
    # 2. Build and clean up header
    df = SOURCE_DF.iloc[y1:y2, 0:x2]    
    df = df.reset_index(drop=True) 
    df.columns = df.iloc[0].str.split().str[0]
    df = df.iloc[1:].reset_index(drop=True)

    # 3. Merge the first two columns and drop the second
    col1, col2 = df.columns[:2]
    df[col1] = df[col1].astype(str).str.cat(df[col2].astype(str), sep=" - ")
    df = df.drop(columns=col2)

    # 4. Combine every three rows by joining non‐null strings with “ | ”
    combined_rows = []
    for i in range(0, df.shape[0], 3):  # the excel has gaps of 3
        row1 = df.iloc[i + 0].tolist() if i + 0 < len(df) else []
        row2 = df.iloc[i + 1].tolist() if i + 1 < len(df) else []
        row3 = df.iloc[i + 2].tolist() if i + 2 < len(df) else []
        
        combined_row = [row1[0]]  # keep first column as is, dropping rows 2 & 3
        for j in range(1, df.shape[1]):
            triplet = map(str,[row1[j], row2[j], row3[j]])
            
             # join only those not equal to "nan" or empty, and don't repeat "CLOSED"
            if str(row1[j]).strip().upper() == "CLOSED":
               combined_row.append(row1[j])
            else:
                combined_row.append(
                    " | ".join(
                        filter(lambda x: x and x != "nan", triplet)
                    )
                )
            
        combined_rows.append(combined_row)
           
    df = pd.DataFrame(combined_rows, columns=df.columns)
    
    
    
    # 5. Export to SQLite database
    conn = sqlite3.connect("mrc_week_data.db")  # Creates a SQLite database file
    df.to_sql("mrc_week_schedule", conn, if_exists="replace", index=False)
    conn.close()

    print("Data exported to week_data.db successfully!")
    
    print(df) #-- uncomment to see the dataframe in the console


if __name__ == "__main__":
    main()
