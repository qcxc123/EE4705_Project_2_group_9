# This Python file was written by Qian Ci

import json
from pathlib import Path

data = Path('Psychology.txt').read_text(encoding="utf-8").split('\n\n\n')
output = []
for i in range(1, len(data)):
    qn_data = data[i].split('\n')
    if qn_data[0] == '':
        continue

    qn = qn_data[0]
    distractor = []
    for j in range(1,len(qn_data)):
        if qn_data[j][0]=='0':
            distractor.append(qn_data[j][2:])
        else:
            corr_ans = qn_data[j][2:]
    dict = {"question":qn,"correct_answer":corr_ans}

    for k in range(len(distractor)):
        dict["distractor"+str(k+1)] = distractor[k]
    output.append(dict)

with open('psychology.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=4)