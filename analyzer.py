import os
import json
import pandas as pd
import numpy  as np
from matplotlib import pyplot as  plt

print(*[filename.split(".")[0] for filename in os.listdir("./opinions")],sep="\n")
product_code = input("Please enter product code: ")

opinions = pd.read_json(f"./opinions/{product_code}.json")

stats = {
    # 'opinions_count': len(opinions),
    # 'opinions_count': int(opinions.id.count()),
    'opinions_count': opinions.shape[0],
    # 'pros_count': int(opinions.pros_en.count()),
    'pros_count': int(opinions.pros.astype(bool).sum()),
    # 'cons_count': int(opinions.cons_en.count()),
    'cons_count': int(opinions.cons.astype(bool).sum()),
    'average_score': opinions.stars.mean().round(2)
}
if not os.path.exists("./plots"):
    os.mkdir("./plots")
stars = opinions.stars.value_counts().reindex(list(np.arange(0.5,5.5,0.5)), fill_value=0)
stars.plot.bar(color='lightskyblue')
for index, value in enumerate(stars):
    plt.text(index,value+1,str(value), ha='center')
plt.ylim([0,max(stars.values)*1.1])
plt.xticks(rotation=0)
plt.grid(axis='y',which='major')
plt.xlabel("Number of stars")
plt.ylabel("Number of opinions")
plt.title("Stars freqiencies")
plt.savefig(f"./plots/{product_code}_stars.png")
plt.close()
stats['stars'] = stars.to_dict()
recommendations = opinions.recommendation.value_counts(dropna=False).reindex([True, False, np.nan])
recommendations.plot.pie(
    label = "",
    labels = ["Positive", "Negative", "Neutral"],
    colors = ['forestgreen', 'crimson', 'lightskyblue'],
    autopct = lambda p: '{:.1f}%'.format(round(p)) if p > 0 else ''
)
plt.title("Recommendations share")
plt.savefig(f"./plots/{product_code}_rcmds.png")
plt.close()
stats['recommendations'] = recommendations.to_dict()
if not os.path.exists("./stats"):
    os.mkdir("./stats")
with open(f"./stats/{product_code}.json", "w", encoding="UTF-8") as jf:
    json.dump(stats, jf, indent=4, ensure_ascii=False)

