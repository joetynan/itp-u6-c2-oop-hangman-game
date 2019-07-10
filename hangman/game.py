from .exceptions import *
import random

class GuessAttempt(object):
    def __init__(self, letter, hit=None, miss=None):
        self.letter = letter
        self.hit = hit
        self.miss = miss
        if self.hit != None and self.miss !=None:
            raise InvalidGuessAttempt()
        
    def is_hit(self):
        if self.hit:
            return True
        return False
    def is_miss(self):
        if self.miss:
            return True
        return False
    
    
    #is_hit, is_miss = true/false


class GuessWord(object):
    def __init__(self, answer):
        self.answer = answer
        self.masked = "*" * len(answer)
        if len(self.answer) <1:
            raise InvalidWordException("GAME REFUSING TO WORK")
        
    def perform_attempt(self,guess):
        if len(guess) > 1:
            raise InvalidGuessedLetterException("NO FUNNY BUSINESS")
        if type(guess) != str:
            raise InvalidGuessedLetterException("I SAID NO FUNNY BUSINESS")
        if guess.lower() in self.answer.lower():
            result = []
            guess = guess.lower()
            for index, letter in enumerate(self.answer):
                if letter.lower() == guess:
                    result.append(index)
            for location in result:
                self.masked = self.masked[:location] + guess + self.masked[location + 1:]
            return (GuessAttempt(guess,hit=True))
        else:
            return (GuessAttempt(guess,miss=True))
        

class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self,word_list = [], number_of_guesses=5):
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        self.words = word_list
        if not word_list:
            word_list = HangmanGame.WORD_LIST
        self.chosen_word = HangmanGame.select_random_word(word_list)
        self.word = GuessWord(self.chosen_word)
        self.game_over_flag = None
        
    def guess(self, guess):
        self.previous_guesses.append(guess.lower())
        guess_attempt = self.word.perform_attempt(guess)
        
        if self.game_over_flag == True:
            raise GameFinishedException("Win or lose, this game is OVER")
        if guess_attempt.is_miss() == True:
            self.remaining_misses -=1
            if self.remaining_misses == 0:
                self.game_over_flag = True
                raise GameLostException("Ha! Teh Loser si YUO!")
        if guess_attempt.is_hit() == True:
            if self.word.answer == self.word.masked:
                self.game_over_flag = True
                raise GameWonException("Take this moment and revel in victory")
        return self.word.perform_attempt(guess)
    
    @staticmethod
    def select_random_word(list_of_words=[]):
        if list_of_words == []:
            raise InvalidListOfWordsException()
        choice = random.choice(list_of_words)
        choice = choice.lower()
        return str(choice)
    
    
    def is_won(self):
        if self.word.answer == self.word.masked:
            return True
        else:
            return False
        
    def is_lost(self):
        if self.remaining_misses == 0 and self.word.answer is not self.word.masked:
            return True
        else:
            return False
        
    def is_finished(self):
        if self.game_over_flag == True:
            return True
        else:
            return False
    