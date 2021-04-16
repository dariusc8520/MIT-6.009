# NO ADDITIONAL IMPORTS!
import doctest
from typing import Type
from text_tokenize import tokenize_sentences


class Trie:
    def __init__(self, key_type):
        self.key_type = key_type
        self.children = {}
        self.value = None

    def __setitem__(self, key, value):
        """
        Add a key with the given value to the trie, or reassign the associated
        value if it is already present in the trie.  Assume that key is an
        immutable ordered sequence.  Raise a TypeError if the given key is of
        the wrong type.
        """
        if type(key) != self.key_type:
            raise TypeError

        current_Trie = self
        for i in range(len(key)):
            prefix = key[i]
            if self.key_type == tuple:
                prefix = (prefix,)
            if prefix not in current_Trie.children:
                current_Trie.children[prefix] = Trie(self.key_type)
            current_Trie = current_Trie.children[prefix]
            if i == len(key)-1:
                current_Trie.value = value

    def __getitem__(self, key):
        """
        Return the value for the specified prefix.  If the given key is not in
        the trie, raise a KeyError.  If the given key is of the wrong type,
        raise a TypeError.
        """
        if type(key) == Trie:
            raise KeyError
        elif type(key) != self.key_type:
            raise TypeError
        
        current_Trie = self
        for i in range(len(key)):
            prefix = key[i]
            if self.key_type == tuple:
                prefix = (prefix,)
            if prefix in current_Trie.children:
                current_Trie = current_Trie.children[prefix]
            else:
                raise KeyError

        if current_Trie.value != None:
            return current_Trie.value
        else:
            raise KeyError


    def __delitem__(self, key):
        """
        Delete the given key from the trie if it exists. If the given key is not in
        the trie, raise a KeyError.  If the given key is of the wrong type,
        raise a TypeError.
        """
        if type(key) != self.key_type:
            raise TypeError
        else:
            if len(key)<1:
                raise KeyError

        current_Trie = self
        for i in range(len(key)):
            prefix = key[i]
            if self.key_type == tuple:
                prefix = (prefix,)
            if prefix in current_Trie.children:
                current_Trie = current_Trie.children[prefix]
                if i == len(key)-1 and current_Trie.value == None:
                    raise KeyError
            else:
                raise KeyError
        current_Trie.value = None

    def __contains__(self, key):
        """
        Is key a key in the trie? return True or False.
        """
        current_Trie = self
        for i in range(len(key)):
            prefix = key[i]
            if self.key_type == tuple:
                prefix = (prefix,)
            if prefix in current_Trie.children:
                current_Trie = current_Trie.children[prefix]
            else:
                return False
        if current_Trie.value != None:
            return True
        else:
            return False

    def __iter__(self):
        """
        Generator of (key, value) pairs for all keys/values in this trie and
        its children.  Must be a generator!
        """
        if self.children:
            for child in self.children:
                sub_Trie = self.children[child]
                value = sub_Trie.value
                if value != None:
                    yield (child,value)
                for sub_child in sub_Trie:
                    yield (child + sub_child[0], sub_child[1])

def make_word_trie(text):
    """
    Given a piece of text as a single string, create a Trie whose keys are the
    words in the text, and whose values are the number of times the associated
    word appears in the text
    """
    new_text = tokenize_sentences(text) #creates a list of strings
    word_trie = Trie(str) 
    for sentence in new_text: #ex of sentence: 'how shall i ever repay you'
        word = ''
        for i in range(len(sentence)): #counter to detect last element
            letter = sentence[i]
            if letter != ' ': #Updates word for letters and not spaces
                word = word+letter
            if letter == ' ' or i == len(sentence)-1: #full word
                if word not in word_trie: #Initializes if it doesn't exist
                    word_trie[word] = 1
                else: #Updates the count
                    word_trie[word] += 1
                word = '' #Resets if the count has been updated for the word
    return word_trie

def make_phrase_trie(text):
    """
    Given a piece of text as a single string, create a Trie whose keys are the
    sentences in the text (as tuples of individual words) and whose values are
    the number of times the associated sentence appears in the text.
    """
    new_text = tokenize_sentences(text) #creates a list of strings
    phrase_trie = Trie(tuple)
    for sentence in new_text:
        words_in_sentence = []
        word = ''
        for i in range(len(sentence)): #counter to detect last element
            letter = sentence[i]
            if letter != ' ': #Updates word for letters and not spaces
                word = word+letter
            if letter == ' ' or i == len(sentence)-1: #full word
                words_in_sentence.append(word)
                word = '' #Resets if the count has been updated for the word
        words_in_sentence = tuple(words_in_sentence)
        if words_in_sentence not in phrase_trie: #Updates phrase trie for the sentence
            phrase_trie[words_in_sentence] = 1
        else:
            phrase_trie[words_in_sentence] += 1
    return phrase_trie


def autocomplete(trie, prefix, max_count=None):
    """
    Return the list of the most-frequently occurring elements that start with
    the given prefix.  Include only the top max_count elements if max_count is
    specified, otherwise return all.

    Raise a TypeError if the given prefix is of an inappropriate type for the
    trie.
    """
    if type(prefix) != trie.key_type:
        raise TypeError

    current_Trie = trie
    for i in range(len(prefix)): #Gets to trie of prefix
        letter = prefix[i]
        if type(prefix) == tuple:
            letter = (letter,)
        if letter in current_Trie.children:
            current_Trie = current_Trie.children[letter]
        else: #prefix not in trie
            return []

    #At trie of prefix
    occuring_keys = {}
    if current_Trie.value != None: #Case of prefix being a word
        occuring_keys[prefix] = current_Trie.value
    for key, val in current_Trie: #Adds all words with prefix
        occuring_keys[prefix+key] = val

    most_frequent_keys = sorted(occuring_keys.keys(),key=occuring_keys.get,reverse=True) #Sort highest to lowest by value
    if max_count == None:
        return most_frequent_keys #returns all if max_count not specified
    else:
        return most_frequent_keys[:max_count] 

def autocorrect(trie, prefix, max_count=None):
    """
    Return the list of the most-frequent words that start with prefix or that
    are valid words that differ from prefix by a small edit.  Include up to
    max_count elements from the autocompletion.  If autocompletion produces
    fewer than max_count elements, include the most-frequently-occurring valid
    edits of the given word as well, up to max_count total elements.
    """
    # >>> autocorrect(t, "bar", 3)
    # ['bar', 'bark', 'bat']
    def edit(trie,prefix):
        '''
        Returns a list of all possible edits
        Edits include single character delection, insertion, replacement and two character transpose
        '''
        possible_edits = {}
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        for i in range(len(prefix)+1): #Single character deletion and two character transpose
            if i < len(prefix)-1: #Prevents i outside index range
                first_letter = prefix[i]
                second_letter = prefix[i+1]
                word = prefix[0:i] + second_letter + first_letter + prefix[i+2:] #Two Character transpose
                if word in trie: 
                    possible_edits.update({word:trie[word]})
            word = prefix[0:i]+prefix[i+1:] #Single Character deletion
            if word in trie: 
                possible_edits.update({word:trie[word]})
            for j in range(len(alphabet)): #Single character insertion and replacement
                word = prefix[0:i]+alphabet[j]+prefix[i:] #Single Character Insertion
                if word in trie:
                    possible_edits.update({word:trie[word]})
                word = prefix[0:i]+alphabet[j]+prefix[i+1:] #Single Character Replacement
                if word in trie:
                    possible_edits.update({word:trie[word]})
        return possible_edits

    autocomplete_list = autocomplete(trie,prefix,max_count)
    possible_edits = edit(trie,prefix)
    if max_count != None:
        C = max_count-len(autocomplete_list)
        if C > 0:
            most_frequent_possible_edits = sorted(possible_edits.keys(),key=possible_edits.get,reverse=True) #Sort highest to lowest by value
            return autocomplete_list + most_frequent_possible_edits[:C]
        else:
            return autocomplete_list
    else:
        return list(set(autocomplete_list + list(possible_edits.keys()))) #Removes doubles

def pattern_filter(pattern):
    '''
    Removes repeating '*'s in a pattern sequence
    '''
    filtered_pattern = ''
    for i in range(len(pattern)):
        if i < len(pattern)-1:
            if pattern[i] == '*' and pattern[i+1] == '*':
                pass
            elif i > 0:
                if pattern[i-1] != '*' and pattern[i] == '*' and pattern[i+1] != '*':
                    pass
                else:
                    filtered_pattern = filtered_pattern + pattern[i]
            else:
                filtered_pattern = filtered_pattern + pattern[i]
        else:
            filtered_pattern = filtered_pattern + pattern[i]
    return filtered_pattern

def word_filter(trie, pattern,first = True):
    """
    Return list of (word, freq) for all words in trie that match pattern.
    pattern is a string, interpreted as explained below:
         * matches any sequence of zero or more characters,
         ? matches any single character,
         otherwise char in pattern char must equal char in word.
    """
    if len(pattern) == 0:
        if trie.value != None:
            return [('',trie.value)]
        else:
            return []
    result = []
    if first:
        pattern = pattern_filter(pattern)
        initial_pattern = pattern[0]
        remaining_pattern = pattern[1:]
        first = False
        if initial_pattern == "*":
            result = result + [(word[0],word[1]) for word in word_filter(trie,remaining_pattern,first)]
    else:
        initial_pattern = pattern[0]
        remaining_pattern = pattern[1:]

    if initial_pattern == '?':
        for child in trie.children:
            result = result + [(child + word[0],word[1]) for word in word_filter(trie.children[child],remaining_pattern,first)]
    elif initial_pattern == '*':
        if trie.value != None and len(pattern) == 1:
            result = result + [('',trie.value)]
        for child in trie.children:
            result = result + [(child + word[0],word[1]) for word in word_filter(trie.children[child],remaining_pattern,first)]
            result = result + [(child + word[0],word[1]) for word in word_filter(trie.children[child],pattern,first)]
    else:
        for child in trie.children:
            if child in initial_pattern:
                result = result + [(child + word[0],word[1]) for word in word_filter(trie.children[child],remaining_pattern,first)]
    return list(set(result))



# you can include test cases of your own in the block below.
if __name__ == '__main__':
    doctest.testmod()
    #Initiatlize
    t = Trie(str)
    #set item
    t['bat'] = 7 #prefix is word
    t['ba'] = 8 #Deletion
    t['pat'] = 10 #Replacement
    t['abat'] = 4 #Insertion
    t['abt'] = 3 #Transpose
    t['d'] = 2
    t['batter'] = 20
    print(t.children)
    print(t.children['a'].children)
    print(t.children['b'].children)
    print(t.children['b'].children['a'].children)
    print(t.children['b'].children['a'].children['t'])
    print(t.children['b'].children['a'].children['t'].value)
    #get item
    print('get item',t['bat'])
    #print(t[1])
    #del item
    # del [t['bat']]
    # print('del item')
    print(t.children['b'].children['a'].children['t'].value)
    #print(t['bat'])
    #contains item
    print('ba' in t)
    #iter items
    print([key for key,val in t])
    #print('edits',edit(t,'bat'))
    #word filter
    print('word filter', word_filter(t,'bat*'))
    print('pattern filter', pattern_filter('*?*?*?*'))