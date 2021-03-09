from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pyttsx3

name = ''
validoptions = ["pizza","menu","order","exit","ice cream","soup"]
yes = ["yes","maybe","ok","indeed"]

class Frenchbot:
    
    def __init__(self):
        self.initVoice()
        print("Welcome to Frenchbot!")
        self.say("Welcome to French bot!")
        self.askName()
        self.askInput()

    def initVoice(self):

        self.__engine = pyttsx3.init()
        self.__voices = self.__engine.getProperty('voices')
        self.__vix = 1  
        self.__voice = self.__voices[self.__vix].id
        self.__engine.setProperty('voice', self.__voice)
        self.__engine.setProperty('rate', 250)
        self.__engine.setProperty('volume', 2.0)

    def say(self, words):
        self.__engine.say(words)
        self.__engine.runAndWait()
    
    def askName(self, prompt="What name would you like to order under? "):
        while True:
            self.say(prompt)
            words = input(prompt)
            name = words
            if prompt == '':
                print("You must enter your name. Try again.")
                break
            elif prompt == True:
                self.say(f"So {name} is your name? ")
                justifyName = input(f"So {name} is your name? ")
            if justifyName.lower().strip()[0] == 'n':
                break
            (match, confidence) = process.extractOne(justifyName, yes)
            if confidence > 60 and match in justifyName:
                self.say(f"Nice to meet you {name}!")
                print(f"Nice to meet you {name}!")
                break
            else:
                break
                
            
    def askInput(self):
        self.say("What would you like to do?")
        question = input("What would you like to do? ")
        (match, confidence) = process.extractOne(question, validoptions)
        if 'menu' in question:
            self.say(f'You would like to see the menu? ')
            fuzz = input(f'You would like to see the menu? ')
        if fuzz.lower().strip()[0] == 'y':
            self.say("Menu To be Decided")
            print("Menu TBD")


def main():
    test = Frenchbot()

if __name__ == "__main__":
    main()