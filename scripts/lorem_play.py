from lorem_text import lorem

wl = 3000

for i in range(0,10):
  word = lorem.words(wl)
  print(len(word))