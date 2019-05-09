import re
from collections import defaultdict
from numpy.random import choice
from functools import reduce

# text = 'Spider-man. Spider-man. Does whatever a spider can. Spins a web, any size. Catches thieves, just like flies. Look out, here comes the Spider-man.'
text = ''
with open('spiderman', 'r') as file:
    text = file.read()

t_split = re.split('(\n)| ', text)
t_split = list(filter(lambda x: x != None, t_split))

'''
str : list[list[str, int]] mapping
'''
model = defaultdict(lambda: None)
first_words = defaultdict(lambda: 0)

def add(word, next):
    next_words = model[word]
    if next_words:
        next_word = list(map(lambda x : x[0], next_words))
        print(next_words)
        print(next_word)
        if next in next_words:
            for pair in next_words:
                if pair[0] == next:
                    pair[1] += 1
        else:
            next_words.append([next, 1])
        # print(next_word)
        # if next_word:
        #     next_word[0][1] += 1
        # else:
        #     next_words.append([next, 1])
        # print(next_word)
    else:
        model[word] = [[next, 1]]

    if word == '\n':
        first_words[next] += 1

for i, word in enumerate(t_split[:-1]):
    add(word, t_split[i + 1])
# for key, value in model.items():
#     print(key, value)
first_words_total = sum(first_words.values())
#getting the dictionary values and converitng it into a list in one line. Probably should split it for visibility. It looks like a row of asses
generated = ''
while generated == '\n' or generated == '':
    first_word = choice(list(first_words.keys()), size=1, p=list(map( lambda x: x/first_words_total, list(first_words.values()))))
    generated = first_word[0]

counter = 25

while (counter > 0):
    latest = re.split('(\n)| ', generated)
    latest = list(filter(lambda x: x != None and x != '', latest))
    latest = latest[-1]
    choices = model[latest]
    next_words = list(map(lambda x: x[0], choices))
    frequency = list(map(lambda x: x[1], choices))
    total_next_words = sum(frequency)
    p = list(map(lambda x: x / total_next_words, frequency))
    next_word = choice(next_words, size=1, p=p)[0]
    generated += f' {next_word}'

    if '\n' == next_word:
        counter -= 1

print(generated)