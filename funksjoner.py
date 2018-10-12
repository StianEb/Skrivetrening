##
# FUNKSJONER - alle funksjoner er laget etter "black box" - prinsipp.
# De henter ingen 'skjulte' variabler fra f.eks. root, og kaller ikke på noen prosedyrer.
# Deres eneste funksjon (hah!) er å utlede en returverdi fra parametrene.
#
# De henter imidlertid noen verdier fra konstanter.py.
#

import random
import konstanter

def generateWeights(incompleteDictionary, completeKeyList, defaultValue=0.5):
    '''incompleteDictionary.keys() should be a subset of completeKeyList.
Returns a list of the same length as completeList. Each position contains the
values from the dictionary when possible, otherwise defaultValue.'''
    
    weights = []
    keysFromDict = incompleteDictionary.keys()
    for element in completeKeyList:
        if element in keysFromDict:
            weights.append(incompleteDictionary[element])
        else:
            weights.append(defaultValue)
            
    return weights

def generateWord(length, weights, mode="small"):
    '''Generates a word of given length, heavily favoring alternation between consonants and vowels
while also favoring individual letters relative to each other according to the given weights'''

    allVowels = konstanter.charsByCategory["vowels"]
    allConsonants = konstanter.charsByCategory["consonants"]
    previousLetter = ' ' #pretend / assume the previous letter was space
    newWord = ''
    
    for letter in range(length):

        # Set 7% chance for vowel after vowel, 85% chance for vowel after non-vowel
        if previousLetter.lower() in allVowels:
            vowelBias = 0.07
        else:
            vowelBias = 0.85

        #let 30% of new words start with a vowel
        if previousLetter == ' ':
            vowelBias = 0.3

        # If we're generating a random text focusing on non-Shift characters only..
        if mode == "small":
            
            #decide whether we're generating a vowel next
            writeVowel = random.randint(1,100)/100 < vowelBias

            #If we're writing a vowel, then pick a vowel. Randomness informed by the given weights.
            if writeVowel:
                vowelWeights = [weights[2], weights[6], weights[7], weights[8], weights[10]]
                newLetter = random.choices(allVowels, weights=vowelWeights)[0]

            #Let's ignore punctuation for now - if not wovel, then consonant.
            else:
                consonantWeights = weights[:2] + weights[3:6] + weights[9:10] + weights[11:19] + weights[20:27]
                newLetter = random.choices(allConsonants, weights=consonantWeights)[0]

        else:

            writeVowel = random.choice(range(100))/100 < vowelBias

            #Note that the lists of shift and non-Shift characters are not entirely equivalent. See smallKeyValues and bigKeyValues in konstanter.
            if writeVowel:
                vowelWeights = [weights[5], weights[9], weights[10], weights[11], weights[13]]
                newLetter = random.choices(allVowels, weights=vowelWeights)[0]
                if previousLetter == ' ':
                    newLetter = newLetter.upper()

            else:
                consonantWeights = weights[3:5] + weights[6:9] + weights[12:13] + weights[14:29]
                newLetter = random.choices(allConsonants, weights=consonantWeights)[0]
                if previousLetter == ' ':
                    newLetter = newLetter.upper()

        previousLetter = newLetter
        newWord += newLetter

    return newWord

def trimKeylog(acceptedChars, originalList):
    '''Returns a version of the originalList (keylog) that only contains entries on the characters specified in acceptedChars'''

    newList = []
    for session in originalList:
        adoptSession = False
        for entry in session:
            if entry[0] in acceptedChars:
                if adoptSession == False:
                    newList.append([])
                    adoptSession = True
                newList[-1].append(entry)
    return newList

def filterPostShift(keylog):
    '''Returns a modified version of the keylog, where entries after Shift entries are removed
(unless they're errors, which are preserved)'''

    newlog = []
    afterShift = True #this is usually true for the first key entry of a session
    for session in keylog:
        newlog.append([])
        for entry in session:
            if entry[2]:
                if not afterShift:
                    newlog[-1].append(entry)
                if entry[0] in konstanter.bigKeyValues:
                    afterShift = True
                else:
                    afterShift = False
            else: #If it's an error or a session identifier:
                newlog[-1].append(entry)
    return newlog

def calculateDistributedAverages(avDe):
    '''Redistributes the values of a dictionary to fit between 0.0 and 1.0, preserving proportion'''
    
    lowestDelay = 5000
    highestDelay = 0
    for item in avDe.values():
        if item[0] < lowestDelay:
            lowestDelay = item[0]
        if item[0] > highestDelay:
            highestDelay = item[0]
            
    difference = highestDelay - lowestDelay
    wAverages = {}
    
    for letter in avDe:
        wAverages[letter] = (avDe[letter][0] - lowestDelay) / difference

    return wAverages

def calculateAverageDelays(log):
    '''Gathers all of the non-error entries from all sessions of the provided keylog in a dictionary
where the keys are the distinct letters present in the log and the values are their average values'''
    
    averages = {}
    for session in log:
        for entry in session:
            if entry[2]: #let's not take errors into the calculation
                if entry[0] in averages:
                    oldAverage = averages[entry[0]]
                    weight = oldAverage[1]
                    newaverage = (entry[1] + oldAverage[0] * weight)/(weight+1)
                    averages[entry[0]] = [newaverage, weight+1]
                else:
                    averages[entry[0]] = [entry[1],1]
    return averages

def generateTrainingText(distributedAverageDelays, numberOfWords, mode="small"):

    #Figure out how heavily to favor each letter
    charList = konstanter.bigKeyValues if mode == "big" else konstanter.smallKeyValues
    weights = generateWeights(distributedAverageDelays, charList, defaultValue=0.3)

    customText = ""
    for word in range(numberOfWords):
        wordLength = random.randint(3,6)
        newWord = generateWord(wordLength, weights, mode=mode)
        customText += newWord
        customText += " "
    customText = customText[:-1] #remove the last space

    return customText

def numberOfSessions(log, titles='nope', returnFilteredLog=False):
    '''Returns the number of sessions in log. If a list of titles is provided, returns the number
of sessions with those titles. If returnFilteredLog is True, returns the filtered log instead'''
    
    if titles != 'nope':
        filteredLog = []
        for session in log:
            if session[0][0] in titles:
                filteredLog.append(session)
        if returnFilteredLog:
            return filteredLog
        else:
            return len(filteredLog)

    else:
        return len(log)
