import ast 
from collections import defaultdict



with open("output/data.txt") as f:
    content = f.read()


records = ast.literal_eval(content.strip())

# group records by their 'group' value
schedule_by_group = defaultdict(list)

for record in records:
    group_name = record["group"]
    schedule_by_group[group_name].append(record)
print(records[0])

