# Initialize basic variables
beginWord = ""
endWord = ""
Dict = []
DictNodes = []
DictRef = []

# Input handling
with open('../data/input/inputPS14.txt', 'r') as input_file:
    lines = input_file.readlines()
    for i in lines:
        linelist = i.strip('\n').split('=')
        if linelist[0].strip(' ') == 'beginWord':
            beginWord = linelist[1].strip(' ')
        if linelist[0].strip(' ') == 'endWord':
            endWord = linelist[1].strip(' ')
        if linelist[0].strip(' ') == 'Dict':
            for x in linelist[1].split(','):
                Dict.append(x.strip(' '))

# print(beginWord)
# print(endWord)
# print(Dict)

# Adding the start and end words to the graph if not present
if beginWord not in Dict:
    Dict.append(beginWord)
if endWord not in Dict:
    Dict.append(endWord)
