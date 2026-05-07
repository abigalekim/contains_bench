import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

# ===== CONFIG =====
CSV_PATH  = "../csv/real_world.csv"
FONT_PATH = "/Users/abigale/code/fonts/LinLibertineOTF_5.3.0_2012_07_02/LinBiolinum_R.otf"
# ==================

custom_font = fm.FontEntry(fname=FONT_PATH, name="Linux Biolinum")
fm.fontManager.ttflist.insert(0, custom_font)

plt.style.use('seaborn-v0_8-paper')
plt.rcParams['font.family'] = "serif"
plt.rcParams.update({
    "axes.labelsize": 14,
    "legend.fontsize": 14,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "axes.titlesize": 14,
    "grid.alpha": 0.3,
    "text.usetex": False
})

color_set = ['#f77189', '#dc8932', '#ae9d31', '#77ab31', '#33b07a', '#36ada4',
             '#38a9c5', '#6e9bf4', '#cc7af4', '#f565cc']

mapping = {
    'facebook comments': 'FB Comments',
    'facebook posts':    'FB Posts',
    'reddit comments':   'Reddit',
    'twitter posts':     'Twitter',
    'amazon reviews':    'Amazon',
    'yelp reviews':      'Yelp',
    'github':            'GitHub',
    'common urls':       'URLs'
}

df = pd.read_csv(CSV_PATH)
df['formal_label'] = df['datasets'].str.lower().str.strip().map(mapping).fillna(df['datasets'])

fig, ax = plt.subplots(figsize=(10, 5))

x = np.arange(len(df))
width = 0.35

ax.bar(x - width / 2, df['het'].values,    width, label='Heterogeneous',
       color=color_set[0], edgecolor='black', linewidth=0.5)
ax.bar(x + width / 2, df['libcudf'].values, width, label='libcudf 25.10',
       color=color_set[1], edgecolor='black', linewidth=0.5)

ax.set_ylabel('Execution Time (ms)')
ax.set_xticks(x)
ax.set_xticklabels(df['formal_label'], rotation=30, ha='right')
ax.grid(axis='y', linestyle='--')
ax.legend(frameon=True, loc='upper left')

plt.tight_layout()
plt.savefig('realworld.pdf', dpi=300, bbox_inches='tight')
plt.close()
print("Generated: realworld.pdf")