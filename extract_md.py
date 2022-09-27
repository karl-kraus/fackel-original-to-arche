import glob
import os
import pandas as pd
from tqdm import tqdm
from acdh_tei_pyutils.tei import TeiReader

files = sorted(glob.glob('./data/*/*.xml'))

data = []
for x in tqdm(files, total=len(files)):
    f_name = os.path.split(x)[1]
    item = {
        'path': x,
        'f_name': f_name,
        'jg': f_name.split('-')[1],
        'nr': f_name.split('-')[2]
    }
    doc = TeiReader(x)
    try:
        page_date = "-".join(doc.any_xpath('.//PUBL_DATE//text()'))
    except IndexError:
        print(x)
        continue
    try:
        issue = doc.any_xpath('.//issue_head')[0]
    except IndexError:
        print(x)
        continue
    try:
         page_title = doc.any_xpath('.//DISP')[0]
    except IndexError:
        print(x)
        continue
    item["issue_title"] = " ".join([x[1] for x in issue.items()[:3]])
    item["page_title"] = page_title.text
    item["page_date"] = page_date
    data.append(item)
print(len(data))

df = pd.DataFrame(data)
df.to_csv('metadata.csv', index=False)