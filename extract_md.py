import glob
import os
import pandas as pd
from tqdm import tqdm
from acdh_tei_pyutils.tei import TeiReader

from config import MASTER_DF, OUT_DIR
from utils import fix_date

os.makedirs(OUT_DIR, exist_ok=True)
files = sorted(glob.glob("./data/*/*.xml"))

data = []
for x in tqdm(files, total=len(files)):
    f_name = os.path.split(x)[1]
    item = {
        "path": x,
        "f_name": f_name,
        "jg": f"{f_name.split('-')[1]}",
        "nr": f"{f_name.split('-')[2].split('_')[0]}",
    }
    doc = TeiReader(x)
    try:
        page_date = "-".join(doc.any_xpath(".//PUBL_DATE//text()"))
    except IndexError:
        print(x)
        continue
    try:
        issue = doc.any_xpath(".//issue_head")[0]
    except IndexError:
        print(x)
        continue
    try:
        page_title = doc.any_xpath(".//DISP")[0]
    except IndexError:
        print(x)
        continue
    item["issue_title"] = " ".join([x[1] for x in issue.items()[:3]])
    item["page_title"] = page_title.text
    item["page_date"] = fix_date(page_date)
    item["word_count"] = len(doc.any_xpath(".//w"))
    data.append(item)
print(len(data))

df = pd.DataFrame(data)
df.to_csv(MASTER_DF, index=False)
