#from wordleinfo.py import alphatest
import numpy as np
import pandas as pd
import random as rd
import math

all_Words = pd.read_excel(r'C:\Users\spenc\Downloads\WordleWords.xlsx')
ongoing_Words =  pd.read_excel(r'C:\Users\spenc\Downloads\WordleWords.xlsx')

def validGuess(guess):                                          #Function for validation of word user entered.
    test = guess in all_Words.values
    return test

def userGuess():                                                #Function for user input of a 5 letter word. 
    word = input("Please enter a 5 letter word:")               
    word = word.lower()
    validation = validGuess(word)                               #Checks that the user input was a valid (5 letter / A-Z Characters only) guess

    while not validation:                                       #If user entry is not valid this loop forces user to enter a valid guess before proceeding,
        word = input("Please enter a valid 5 letter word:")
        word = word.lower()
        validation = validGuess(word)
    
    return (word)                                               #Returns the user's guess 
  

def randomWord():                                               #Function for randomly choosing a word from the list of possible words.
    maxValue = all_Words.shape[0] - 1                           #Determines the range of numbers which are valid guesses
    choice = rd.randint(0, maxValue)                            #randomly selects an integer 
    randWord = all_Words.loc[choice][0]
    return (randWord)

def checkWordWinner(correctWord, userWord):                     #Function used for checking if the word is correct.
    if correctWord == userWord:
        return True


def checkForGreen(correctWord, userWord):                       #Function cycles through each letter and determines if it is correct and in the correct place. 
    solution = ""
    for x in range(0,len(correctWord)):                         #Cycles through each letter in the Solution
            if correctWord[x] == userWord[x]:                   #If the characters in a position match appends a "G" - Correct and in Correct place
                solution = solution + "G"
            else:                                               #If the characters in a specific position do not match appends a " " 
                solution = solution + " "                   
    
    solution = checkForYellow(solution, correctWord, userWord)  #Calls function to pass through and check to see if letters are correct but in the incorrect place.  
    return solution

def checkForYellow(tempSolution, correctWord, userWord):        #Cycles through each letter to determine if correct and in incorrect place. 
    solution = ""
    for y in range(0, len(tempSolution)):                       #Loops through the string of "G" - Correct and in correct place 
        if tempSolution[y] == "G":                              #Logic to check if the character was already determined to be correct
            solution = solution + "G"
        else:                                                   #If the character wasn't correct and in the correct place then we check for other possibilities
            for z in range(0, len(correctWord)):                #Loops through each character in the correct word 
                if userWord[y] == correctWord[z]:               #If statement which determines if there is a match 
                    if tempSolution[z] != "G":                  #Check to see if that character was already accounted for. If it wasn't then we appened "Y" - Correct and incorrect place
                        solution = solution + "Y"
                        break
                if z == 4:                                      #If no matches are found and we reach the final character we append a "B" - not in word
                    solution = solution + "B"    

    return solution                                             #Return the complete string containing the evaluation information. 
    
def possibleSolutions(userWord, results):                       #loop through list of possible guesses. 
    global ongoing_Words
    dropChecker = 0
    for i in range(len(ongoing_Words)):                         #loop through list of possible guesses.
        dropChecker = 0
        for x in range(0,len(results)):                         #loops through the results (G = Green / Correct and in correct location. Y = Correct and incorrect location. B = Incorrect)
            if results[x] == "G":
                if ongoing_Words.loc[i]["Word"][x] != userWord[x]:
                    ongoing_Words.drop([i], inplace = True)
                    
                    break
                    
            elif results[x] == "B":                             #Handles the incorrect letter in a guess. 
                doubleCheck = doubleLetterCheck(userWord[x], userWord, results) #calls function to check if there is a double letter.  "True" means there is a repeated letter. 
                if not doubleCheck:
                    for y in range(0, len(ongoing_Words.loc[i]["Word"])):       #loop through characters in each possible word
                        if ongoing_Words.loc[i]["Word"][y] == userWord[x]:
                            ongoing_Words.drop([i], inplace = True)
                            dropChecker = 1                                     #Used to get out of looping through the variable results    
                            break                                               #Break to Get out of looping through characters in each entry in the ongoing list dataframe
                    if dropChecker == 1:
                        dropChecker = 0
                        break                                                   #Break to get out of looping through each character in the results string. 
                else:                                                           #Handling dropping if there is a double letter.
                    if userWord[x] == ongoing_Words.loc[i]["Word"][x]:          #Checks to see if the double letter matches the specific location in the word.  
                        ongoing_Words.drop([i], inplace = True)                 #Drops the word as a possible guess. 
                        break 
            
            else:                                               #Handling the "Y" condition of information
                yCheck = 0
                for z in range(0,len(ongoing_Words.loc[i]["Word"])):
                    if ongoing_Words.loc[i]["Word"][z] == userWord[z] and results[z] != "G":
                        yCheck = 0
                        break 
                    if ongoing_Words.loc[i]["Word"][z] == userWord[x] and results[x] != "G":
                        yCheck = 1
                        break  


                if yCheck == 0:                                 #Checking if we found a match for a "Y" result.  0 means no match found. 1 Means match found.     
                    ongoing_Words.drop([i], inplace = True)     
                    break                                       #Break to exit for loop on line 78 as the line would already be dropped. 
                    
                                                                #check to see if the word could be a solution.
                                                                #if the word can't be a solution - drop the line in the dataframe and decrement the loop 
    ongoing_Words = ongoing_Words.reset_index()
    ongoing_Words = ongoing_Words.drop(["index"], axis=1)                   

def evalProb():                                                 #Function for determining the letter frequency in the remaining valid words
    alphabet = [['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q', 'r','s','t','u','v','w','x','y','z'], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
    percentages = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

    for i in range(len(ongoing_Words)):                         #Loops through each word in the remaining possible words and prints it prior to evaluating character information
        print(ongoing_Words.loc[i][0])                          
        for x in range(len(ongoing_Words.loc[i][0])):           #Loops through each character in the word in order to determine the number of each character
            tempLetter = ongoing_Words.loc[i][0][x]             
            for z in range(len(alphabet[0])):                   #Increments the corresponding later in the list "alphabet" 
            
                if alphabet[0][z] == tempLetter:
                
                    alphabet[1][z] = alphabet[1][z] + 1
                
                    break

    for i in range (len(alphabet[0])):                          #Loops through each letter in order to calculate the percentage of words each letter is in. 
        if len(ongoing_Words) == 0:                             #Error checking - if a word was removed in error this prevents dividing by zero. 
            print("Error - A Word was incorrectly removed")
        else:    
            if alphabet[1][i] >= len(ongoing_Words):            #If statement for words with double letters to prevent overvaluing their prioritization, primarily if we've already found that one instance is in a word. 
                percentages[0][i] = math.trunc((alphabet[1][i] - len(ongoing_Words)) / len(ongoing_Words) * 10000)/100
            else:
                percentages[0][i] = math.trunc(alphabet[1][i] / len(ongoing_Words) * 10000)/100         #Divides the number of occurrences of a letter by the number of words to get a percentage.
    alphabet += percentages                                     #Appending the percentages list to the alphabet list 
    for i in range(len(alphabet[0])):                           #Loops through the list "alphabet" and prints each letter (with at least 1 occurrence), the number of occurrences, and the percentage of words. 
        if (alphabet[1][i] > 0):
        
            print(alphabet[0][i], " ", alphabet[1][i], " ", alphabet[2][i])
    
    print("Number of possible words remaining is:", len(ongoing_Words))
    evalWordsProb(alphabet)
    

#Work In progress - evalWordsProb function will be used to more easily evaluate each order and assign a score based on the number of occurrences of each character in the remaining guesses 
#


def evalWordsProb(alphabet):                                    
    wordPercentages = []
    for x in range (len(ongoing_Words)):
        score = 0
        for y in range (0, len(ongoing_Words.loc[x]["Word"])):
            for z in range (0, len(alphabet[0])):
                if alphabet[0][z] == ongoing_Words.loc[x]["Word"][y]:
                    score = score + alphabet[2][z]
                    break
        #print(ongoing_Words.loc[x]["Word"])
        #print(score)
        wordPercentages.append(score)
    #print(wordPercentages)    



def doubleLetterCheck(letter, checkWord, results):              #Function to check for double letters.  This will be used to prevent words from being removed incorrectly. 
    counter = 0
    double = False                                              #Boolean variable used as a check for if the word contains a double letter 
    for i in range(0, len(checkWord)):                          #Looping through each character in the passed word. 
        if letter == checkWord[i]:
            if results[i] == "Y" or results [i] == "G":
                counter += 1
    
    if counter > 0:                                             #If there is at least one occurrence of a double letter the variable "double" is set to "True" to prevent incorrectly removing words
        double = True                                           
    return double

        
                

def userResults():                                              #Function for receiving user input for the results  
    result = input("Please input your Wordle Results - 'B' for Wrong, 'Y' for Yellow, and 'G' for Green: ")
    result = result.upper()                                     
    validation = resultsValidation(result)                      #Function to call and check if the user input is only valid (BYG) characters
    while not validation:                                       #Loop that forces the user to input a valid (5 characters and only B, Y, or G) input
        result = input("Please input your valid Wordle Results - 'B' for Wrong, 'Y' for Yellow, and 'G' for Green: ")
        result = result.upper()                                 
        validation = resultsValidation(result)
    
    return result

def resultsValidation(userResults):                             #Function for validating results to ensure they are entered in the correct format
    validation = True
    userSet = set(userResults)                                  #Creates a set of characters based on what the user entered
    validLetters = set('BGY')                                   #Defines the set of valid characters
    if len(userResults) != 5:                                   #If statement to ensure that exactly five characters are entered
        validation = False  
    if not userSet.issubset(validLetters):                      #Compares the set of letters in the user entered results to the set of allowed results.
        validation = False                                      #If the user entered invalid results the variable "validation" is set to false to force the user to reenter results.

    return validation

def checkResultsWinner(results):                                #Function for checking if you have the correct word based on results
    if results == "GGGGG":
        return True

choice = input("To simulate Wordle type 1. To help with Wordle of the day type 2: ")        #Prompt for User to simulate Wordle or to assist with wordle of the day

if choice == "1":                                               #If logic for when the user selects to simulate wordle. 

    winner = randomWord()                                       #Calls the function randomWord to choose a randomly selected word
    
    guesses = 0                                                 #Counter to track the number of guesses used

    while guesses < 6:                                          #Loop that increments the number of guesses and sets the limit at 6 guesses
        wordGuess = userGuess()                                 #Gets the user entered word 

        result = checkForGreen(winner, wordGuess)               #Compares the user entered word to the randomly selected word to get the results.  
        guesses = guesses + 1                                   #Increments the number of guesses

        if checkWordWinner(winner, wordGuess) is True:          #Checks if the word is correct and displays the winning message if its correct.
            result = "Congrats"
            break

        print(result)
        if result != "Congrats":                                #If the word is not correct displays additional information and statistics.
            possibleSolutions(wordGuess, result)                #Evaluates, edits, and then prints the remaining possible guesses
            evalProb()                                          #Evaluates and then displays information for individual characters
            print("You are on your ", guesses+1, " guess.")     #Displays what guess the user is on. 


        
   


elif choice == "2":                                             #If logic for when the user selects assistance with the wordle of the day. 
    guesses = 0                                                 #Counter to track the number of guesses used
    while guesses < 6:                                          #Loop that increments the number of guesses and sets the limit at 6 guesses
        wordGuess = userGuess()                                 #Gets the user entered word 
        results = userResults()                                 #Gets the user entered result
             
        guesses = guesses + 1                                   #Increments the number of guesses used

        if checkResultsWinner(results) is True:                 #Checks to see the word was correctly guess - "GGGGG" being the winning result
            results = "Congrats"            
            break                            


        if results != "Congrats":                               #If the word is not correct displays additional information and statistics.
            possibleSolutions(wordGuess, results)               #Evaluates, edits, and then prints the remaining possible guesses
            evalProb()                                          #Evaluates and then displays information for individual characters
            print("You are on your ", guesses+1, " guess.")     #Displays what guess the user is on. 

