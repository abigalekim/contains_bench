file = "../exp5_pct.txt"
f = open(file, "r")
f_lines = f.readlines()

time_list = []
for fl in f_lines:
  if fl.startswith("Contains query average:"):
    print(fl.split(" ")[3].strip())

f.close()