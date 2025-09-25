f = open("block_output.txt")
flines = f.readlines()

for elem in flines:
  if elem.startswith("Contains query average:"):
    eleml = elem.split(" ")
    print(eleml[-1].strip())

f.close()