import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

# ===== CONFIG =====
CSV_PCT   = "../csv/exp4_pct_short_strings.csv"
CSV_LEN   = "../csv/exp4_length_long_strings.csv"
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


# ===== GRAPH 1: % Short Strings — Het vs. libcudf =====
df_pct = pd.read_csv(CSV_PCT)
df_pct['x_label'] = df_pct['pct_short_strings'].apply(lambda v: f"{v}%")

fig, ax = plt.subplots(figsize=(10, 5))

x = np.arange(len(df_pct))
width = 0.35

ax.bar(x - width / 2, df_pct['het'].values,    width, label='Heterogeneous',
       color=color_set[0], edgecolor='black', linewidth=0.5)
ax.bar(x + width / 2, df_pct['libcudf'].values, width, label='libcudf 25.10',
       color=color_set[1], edgecolor='black', linewidth=0.5)

ax.set_xlabel('% Short Strings')
ax.set_ylabel('Execution Time (ms)')
ax.set_xticks(x)
ax.set_xticklabels(df_pct['x_label'], rotation=40, ha='right')
ax.grid(axis='y', linestyle='--')
ax.legend(frameon=True, loc='upper left')

plt.tight_layout()
plt.savefig('exp4_pct_short_strings.pdf', dpi=300, bbox_inches='tight')
plt.close()
print("Generated: exp4_pct_short_strings.pdf")


# ===== GRAPH 2: Length of Long Strings — Het vs. libcudf =====
df_len = pd.read_csv(CSV_LEN)
df_len['x_label'] = df_len['length of long string'].apply(lambda v: str(int(v)))

fig, ax = plt.subplots(figsize=(10, 5))

x = np.arange(len(df_len))

ax.bar(x - width / 2, df_len['het'].values,    width, label='Heterogeneous',
       color=color_set[0], edgecolor='black', linewidth=0.5)
ax.bar(x + width / 2, df_len['libcudf'].values, width, label='libcudf 25.10',
       color=color_set[1], edgecolor='black', linewidth=0.5)

ax.set_xlabel('Length of Long String (chars)')
ax.set_ylabel('Execution Time (ms)')
ax.set_xticks(x)
ax.set_xticklabels(df_len['x_label'], rotation=40, ha='right')
ax.grid(axis='y', linestyle='--')
ax.legend(frameon=True, loc='upper left')

plt.tight_layout()
plt.savefig('exp4_length_long_strings.pdf', dpi=300, bbox_inches='tight')
plt.close()
print("Generated: exp4_length_long_strings.pdf")

print("\n✓ Done!")
print("  - exp4_pct_short_strings.pdf")
print("  - exp4_length_long_strings.pdf")