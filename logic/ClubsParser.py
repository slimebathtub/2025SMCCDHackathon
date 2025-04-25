import os
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from .TimeHandler import time_handler as th

CACHE_PATH = "cache/clubs_cache.csv"
CSM_CLUBS_URL = "https://collegeofsanmateo.edu/clubs/activegroups.asp"

def fetch_active_clubs() -> pd.DataFrame:
    headers = {"User-Agent": "ClubCrawler/1.0"}
    resp = requests.get(CSM_CLUBS_URL, headers=headers)
    resp.raise_for_status()
    time.sleep(1)

    soup  = BeautifulSoup(resp.text, "html.parser")
    table = soup.find("table")

    records = []
    for row in table.find_all("tr")[1:]:
        cols = row.find_all("td")
        # preserve newlines
        raw_name     = cols[0].get_text("\n", strip=True)
        raw_advisors = cols[1].get_text("\n", strip=True)
        raw_meetings = cols[2].get_text("\n", strip=True)
        records.append({
            "name":     raw_name,
            "advisors": raw_advisors,
            "meetings": raw_meetings,
        })

    df = pd.DataFrame.from_records(records, columns=["name","advisors","meetings"])
    df.to_csv(CACHE_PATH, index=False)
    return df

def load_clubs(force_refresh=False) -> pd.DataFrame:
    if os.path.exists(CACHE_PATH) and not force_refresh:
        return pd.read_csv(CACHE_PATH)
    return fetch_active_clubs()

def clubs_parser():
    df = load_clubs()

    df["advisors"]      = df["advisors"].astype(object)
    df["advisors_email"] = df["advisors"].copy().astype(object)
    df["meetings"]      = df["meetings"].astype(object)
    df["days"]  = df["meetings"].astype(object)
    df["location"] = df["meetings"].astype(object)
    df["time"] = df["meetings"].astype(object)

    for i, row in df.iterrows():
        # 1) truncate the club name as before
        raw_name = row["name"]
        n1 = raw_name.find("(")
        n2 = raw_name.find("Club")
        n2 = -1 if n2 == -1 else n2 + len("Club")
        cuts = [x for x in (n1, n2) if x != -1]
        end  = min(cuts) if cuts else len(raw_name)
        df.at[i, "name"] = raw_name[:end].strip()

       
        advisor_lines = [ln.strip() for ln in row["advisors"].split("\n") if ln.strip()]
      
        names, emails = [], []
        days, time, location = [], [], []
        for j in range(1, len(advisor_lines), 2):
            nm = advisor_lines[j]
            em = advisor_lines[j+1]
            # ensure the 'edu' suffix
            if not em.endswith("edu"):
                em += "edu"
            names.append(nm)
            emails.append(em)

        df.at[i, "advisors"]       = names
        df.at[i, "advisors_email"] = emails

        # 3) split meetings into lines (or leave as list)
        meets = [ln.strip() for ln in row["meetings"].split("\n") if ln.strip()]
        meets = meets[1:] #drop headers
        df.at[i, "meetings"] = meets
        
        expanded = []
        
    for _, row in df.iterrows():
        base = {
            "name":            row["name"],
            "advisors":        row["advisors"],
            "advisors_email":  row["advisors_email"],
        }
        meets = row["meetings"]
        # assume len(meets) == 3 * p
        for k in range(0, len(meets), 3):
            meets[k+2] = meets[k+2].replace(",", " at")
            meets[k+2] = meets[k+2].replace("Room ", "")
            expanded.append({
                **base,
                "day":      meets[k],
                "time":     meets[k+1].replace(" to ", " - "),
                "location": meets[k+2].replace("Building", "Bldg")
            })

    # 5) Build the final DataFrame
    final_df = pd.DataFrame(expanded, columns=[
        "name", "advisors", "advisors_email", "day", "time", "location"
    ])
        

    df.drop(columns=["meetings"])
    return th(final_df)


def main():
    parsed = clubs_parser()
    print(parsed)
    
    # and to inspect emails:
    # for lst in parsed["advisor_email"]:
    #     print(lst)
    
    

# example usage
if __name__ == "__main__":
    main()
