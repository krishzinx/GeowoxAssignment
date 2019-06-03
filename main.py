# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 14:13:15 2019

@author: Krishna Hariramani
"""

from nltk.corpus import stopwords
import re
import inflect
import string
import pandas as pd
import sys


'''
@return: compiled pattern to recognise 1st, 2nd, 3rd, etc. in the string
'''
def compile_pattern_ordinals():
    #compile pattern 1st, 2nd, 3rd, 4th, etc.
    return re.compile("^(\d+)(st|nd|rd|th)$")


'''
@return: generate a list of stopwords for ennglish language
'''
def gen_stopwords_list():
    #create stopwords list for english language
    return set(stopwords.words('english'))


'''
@param address: street address with uppercase characters
@return: street address with lowercase characters
'''                      
def convert_to_lowercase(address):
    #convert all characters address to lowecase
    return address.lower()


'''
@param address: full street address
@param split_char: the character by which the address address will be splitted into a list
@return: list of words in an adress
'''
def split_string(address, split_char):
    #split address into list of words
    return address.split(split_char)


'''
@param word: word from which the trailing spaces are to be removed
@return: word without trailing spaces
'''
def strip_word(word):
    #remove trailing spaces, tabs, and newline characters
    return word.strip()


'''
@param word: word containing bad characters
@return: word with all bad characters removed
'''
def remove_badchars(word):
    #iterate over string to remove all bad characters and create new string without bad characters 
    return "".join(i for i in word if ord(i) < 128)


'''
@param word: word with punctuations
@return: word without punctuations
'''
def remove_punctuations(word):
    #iterate over string to remove all punctuations and create new string without punctuations
    return "".join(i for i in word if i not in string.punctuation)


'''
@param word: word to be checked in the stopwords lsit
@return: empty string if the input word is a stop word else the input word itself
'''
def remove_stop_words(word):
    #check whether word is a stopword or not
    if word in en_stops:
        #if word is a stopword then replace it by an empty string
        word = ''
    return word


'''
@param value: integer value
@return: ordinal value
'''
def int_to_ordinal(value):
    #initialise inflect engine
    p = inflect.engine()
    
    #convert integer value to string (1 to one)
    ordstr = p.number_to_words(value)
    
    #replace ',' and '-' to space
    ordstr = ordstr.replace('-', ' ')
    ordstr = ordstr.replace(',', '')
    
    #split string into a list of words separated by a space
    ordlist = ordstr.split(" ")
    
    #create list to which 'th' is to be added at end
    thlist = ['four', 'six', 'seven', 'nine', 'ten', 'eleven', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'hundred', 'thousand']
    
    #create list in which 'y' is to be replaced by 'ieth' at the end
    iethlist = ['twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
    
    #change last word in the converted string based on different test cases
    if ordlist[-1] == 'one':
        ordlist[-1] = 'first'
        
    if ordlist[-1] == 'two':
        ordlist[-1] = 'second'
    
    if ordlist[-1] == 'three':
        ordlist[-1] = 'third'
    
    if ordlist[-1] == 'five':
        ordlist[-1] = 'fifth'
    
    if ordlist[-1] == 'eight':
        ordlist[-1] = 'eighth'
    
    if ordlist[-1] == 'twelve':
        ordlist[-1] = 'twelfth'
    
    if ordlist[-1] in thlist:
        ordlist[-1] = ordlist[-1] + 'th'
    
    if ordlist[-1] in iethlist:
        ordlist[-1] = ordlist[-1].replace('y', 'ieth')
    
    ordval = ''
    
    for word in ordlist:
        ordval = ordval + word + ' '
    return ordval.strip()


'''
@param word: word containing 1st, 2nd, 3rd, etc.
@param myParam2: pattern to find in the word, in this case 1st, 2nd, etc.
@return: word with 1st, 2nd, etc. replaced to first, second, etc. 
'''
def convert_ordinals(word, pattern):
    #find pattern(1st, 2nd, 3rd, etc.) in a word
    matches = pattern.finditer(word)
    
    #convert found pattern to ordinal values (convert 22nd to twenty second)
    for match in matches:
        word = int_to_ordinal(match.group(1))
    return word


'''
@param word: first ocuurance of a word in the address or duplicate occuracnce of the word in the address
@param uniq: list containing first occurance of all words in an address
@return word: word itself if it is first ocuurance in an address else empty string
@return uniq: uniq list containing first occurance of a word
'''
def remove_duplicates(word, uniq):
    #if the word is a digit then it does not have to be unique
    if word.isdigit():
        return word, uniq
    
    #if the word is already present in the uniq list then it is a duplicate word, remove it
    if word in uniq:
        word = ''
    
    #if the word is not in the uniq list, then it is not a duplicate, append it to the unique list
    if word not in uniq:
        uniq.append(word)
    
    return word, uniq


'''
@param ad: final address string
@param word: word to be added in the string
@return: updated final address
'''
def edit_final_address(ad, word):
    #if word is not empty string then add it to the address
    if word:
        ad = ad + word + ' '
    return ad


'''
@param stad: unprocessed street address
@param en_stops: stopwords list for english
@param pattern: pattern to be looked in a string, in this case 1st, 2nd, 3rd, etc.
@return: pre-processed address
'''
def preprocess_address(st_ad, en_stops, pattern):
    
    #lowecase all chatacters in the address
    st_ad = convert_to_lowercase(st_ad)
    
    #split address by whitespace into a list of words
    split_st_ad = split_string(st_ad, " ")
    
    #create a list to identify unique words in the address to remove duplicates
    uniq = []

    #create a empty string to store address after text preprocessing 
    ad = ''
    
    #iterate over each word in address
    for word in split_st_ad:
        #remove trailing spaces, tabs and newlines from start or end of each word
        word = strip_word(word)

        #remove all badcharacters from each word
        word = remove_badchars(word)

        #remove all puctuations from each word
        word = remove_punctuations(word)

        #transform 1st, 2nd, 3rd to first, second, third
        word = convert_ordinals(word, pattern)

        #remove word if it is a stop word    
        word = remove_stop_words(word)

        #remove duplicates
        word, uniq = remove_duplicates(word, uniq)

        #if the word is not empty after preprocessing add it to the final address follow it with a space
        ad = edit_final_address(ad, word)
    
    #remove trailing spaces, tabs and newlines from start or end of the final preprocessed address
    ad = ad.strip()
    return ad

if __name__ == "__main__":
    #compile pattern to recognice 1st, 2nd, 3rd, 4th, etc. in a string
    pattern = compile_pattern_ordinals()
    
    #generate list of stop words in english
    en_stops = gen_stopwords_list()
    
    #read csv to pandas dataframe
    df = pd.read_csv(sys.argv[1])
    
    #apply preprocessing to address column and update address coulmn with new values 
    df['Address'] = df['Address'].apply(preprocess_address, args = [en_stops, pattern]) 
    
    #save dataframe to csv
    df.to_csv(sys.argv[2])