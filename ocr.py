from pathlib import Path
import ast 
import re
from cell import days,times

extracted_text_path = Path("output/extracted_cells.txt")
output_path = Path("output")

with open(extracted_text_path) as f:
    content = f.read()

data = ast.literal_eval(content.strip())

records = []

for r , row in enumerate(data):
    day = row[0]

    for c , cell in enumerate(row[1:],start=1):
        cell = cell.strip()
        if not cell :
            continue

        lines = [l.strip() for l in cell.splitlines() if l.strip()]
        #print(f"{r}:{c}",lines)

        current_group = "ALL"
        for l in lines:
            x = re.search("G[1-3]:",l)
            if x:
                current_group = x.group()
            
            records.append({"day":days[r],"Time":times[c-1],"group":current_group,"text":l})

(output_path / "data.txt").write_text(str(records),"utf-8")
print(records)