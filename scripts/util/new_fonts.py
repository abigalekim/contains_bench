import matplotlib.font_manager as fm

# List ALL fonts
all_fonts = sorted(set([f.name for f in fm.fontManager.ttflist]))

# Filter for likely candidates
libertine = [f for f in all_fonts if 'liber' in f.lower() or 'biol' in f.lower()]
print("Libertine-related fonts:", libertine)

# Or save all to a file to search
with open('all_fonts.txt', 'w') as f:
    f.write('\n'.join(all_fonts))
print("All fonts written to all_fonts.txt")