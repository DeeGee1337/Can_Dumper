import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(14, 10))
sns.heatmap(bitflips_df, cmap="YlGnBu", annot=True, fmt="d", annot_kws={"size": 8}, linewidths=0.5, linecolor='gray')
plt.title("Heatmap of Bitflips per ID across CAN Dumps", fontsize=16)
plt.xlabel("CAN Dumps", fontsize=12)
plt.ylabel("Message IDs", fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10, rotation=0)
plt.savefig("bitflips_heatmap.png")
plt.show()
