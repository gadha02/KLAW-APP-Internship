import string

file = open("sample.txt", "r")
text = file.read()
text = text.translate(str.maketrans('', '', string.punctuation))

file.close()

words = text.split()
word_count = {}

for word in words:
    word = word.lower()
    if word in word_count:
        word_count[word] += 1
    else:
        word_count[word] = 1

for word, count in word_count.items():
    print(word, ":", count)
