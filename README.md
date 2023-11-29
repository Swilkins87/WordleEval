# WordleEval
Personal Project Using Python to create a wordle clone and then use it to provide analysis, statistics, and evaluations / recommendations.  WORK IN PROGRESS

Scope / Goal: To provide evaluation and recommendations for guesses in the popular game "Wordle" with a focus on "Hard Mode"

Wordle is a game where users enter a 5 letter word and receive clues about the position of each character and if it is in the word in the following ways:
    - Green / "G" means that the character is in the word and in the correct position.
    - Yellow / "Y" means that the character is in the word but in the incorrect position.
    - Black / "B" means that the character is not in the word.

Users have six guesses to attempt to guess the correct word.  
Hard-Mode is a variation where the user must use any correct (Green / Yellow) characters they have found in all future guesses rather than using a combination of words to determine all of the correct characters used in the word. 

Upload on 11/29/2023:
Contains the wordle text based clone that can either simulate wordle (primarily for testing purposes) or assist with the daily wordle with a focus on hard mode(all correctly guessed characters must be included). 
Uses a list of all the valid guesses in wordle to:
      1) Check for and only allow users to enter valid guesses
      2) After each guess a list of words not yet eliminated is provided.
          a) This list is distinct from the valid guesses so words already eliminated could be guessed again if desired. 
      3) Using the list of remaining possible solutions some simple evaluation of each letter in the alphabet is performed and presented
          a) Number of occurrences for each character
          b) Percentage of words with each character

Current to do:
      1) Evaluation of each remaining word guess and include some information about the strength of guessing that word next.
      2) Replayability - Create a simple loop so that once a game is finished the user can decided to play again(and what version they want to play) or exit rather than automatically exiting at the conclusion of one game.
      3) Address a very rare and specific edge case where a word is not removed because of double letters (IE SPOON when we know that there is one, and only one, "O")
          a) This issue came up to prevent removing words incorrectly when a double letter when one letter was correct and one was incorrect. 
