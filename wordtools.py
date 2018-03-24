def cleanword(word):
    out = ""
    for char in word:
        if char.isalpha():
            out = out + char
    return out

def has_dashdash(word):
    first_dash = False
    for char in word:
        if char != "-":
            first_dash = False
        elif char == "-" and first_dash == False:
            first_dash = True
        elif char == "-" and first_dash == True:
            first_dash = False # Desnecessário. Mas, se fôssemos contar a quantidade de "--" na string, seria necessário
            return True
    return False

def extract_words(string):
    def read_word(start_index):
        out = ""
        index = start_index
        while index < len(string):
            if not string[index].isalpha():
                return (out, index)
            out = out + string[index]
            index = index + 1
        return (out, index)
    
    out = []
    index = 0
    while index < len(string):
        if string[index].isalpha():
            res = read_word(index)
            out.append(res[0].lower())
            index = res[1] + 1
        else:
            index = index + 1
    return out

def wordcount(word, array):
    count = 0
    for each in array:
        if each == word:
            count = count + 1
    return count

def wordset(array):
    def remove_duplicates(arr):
        out = []
        index = 0
        while index < len(arr):
            if wordcount(arr[index], out) == 0:
                out.append(arr[index])
            index = index + 1
        return out
    
    def findmin(arr):
        min = arr[0]
        for elem in arr:
            min = elem if elem < min else min
        return min
    
    def sort(arr):
        out = []
        while len(arr) > 0:
            new = findmin(arr)
            arr.remove(new)
            out.append(new)
        return out
    
    return sort(remove_duplicates(array))

def longestword(array):
    if len(array) == 0:
        return 0
    max = len(array[0])
    index = 1
    while index < len(array):
        if len(array[index]) > max:
            max = len(array[index])
        index = index + 1
    return max