import ast
from collections import defaultdict
import matplotlib.pyplot as plt

with open("output/data.txt", encoding="utf-8") as f:
    records = ast.literal_eval(f.read().strip())

# clean the strings (they may still contain \n)
for r in records:
    r["day"] = r["day"].strip()
    r["Time"] = r["Time"].strip()
    r["text"] = " ".join(r["text"].split())

# keep the order in which days and times first appear
DAYS = list(dict.fromkeys(r["day"] for r in records))
TIMES = list(dict.fromkeys(r["Time"] for r in records))

# records that belong to every group (courses)
SHARED = {"ALL", "", None}

groups = sorted({r["group"] for r in records if r["group"] not in SHARED})

def build_grid(group_records):
    """{(day, time): [text lines]} for one group."""
    grid = defaultdict(list)
    for r in group_records:
        grid[(r["day"], r["Time"])].append(r["text"])
    return grid

def schedule_per_group(save=False):
    shared_records = [r for r in records if r["group"] in SHARED]

    for g in groups:
        own = [r for r in records if r["group"] == g]
        grid = build_grid(own + shared_records)

        table_data = [
            ["\n".join(grid.get((day, t), [])) for t in TIMES]
            for day in DAYS
        ]

        fig, ax = plt.subplots(figsize=(18, 8))
        ax.axis("off")
        table = ax.table(
            cellText=table_data,
            rowLabels=DAYS,
            colLabels=TIMES,
            loc="center",
            cellLoc="center",
        )
        table.auto_set_font_size(False)
        table.set_fontsize(7)
        table.scale(1, 6)
        ax.set_title(f"Schedule - {g}", fontsize=14, pad=20)

        if save:
            fig.savefig(f"output/schedule_{g}.png", dpi=200, bbox_inches="tight")
        plt.show()

schedule_per_group(save=True)