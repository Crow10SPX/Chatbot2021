from os import name
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pyttsx3
import json
import spacy
nlp = spacy.load("en_core_web_sm")

menu = {
    "entree" :
            {
                "quiche lorraine" : 5.00,
                "cheese souffle" : 8.00,
                "flamiche" : 6.00
            },
    "main" :
            {
                "duck a l'orange" : 18.00,
                "chicken dijon" : 23.00,
                "croque madame" : 15.00 
            },
    "dessert" :
            {
                "crepes" : 12.00,
                "creme brulee" : 10.00,
                "macarons" : 8.00
            },
    "side" :
            {
                "pommes frites" : 6.00,
                "truffade" : 5.00                    
            }
    }

class Frenchbot:

    def initVoice(self):
        self.__engine = pyttsx3.init()
        self.__voices = self.__engine.getProperty('voices')
        self.__vix = 1 
        self.__voice = self.__voices[self.__vix].id
        self.__engine.setProperty('voice', self.__voice)
        self.__engine.setProperty('rate', 400) 
        self.__engine.setProperty('volume', 2.0)
        
    def say(self, words):
        self.__engine.say(words)
        self.__engine.runAndWait()
        
    def __init__(self):
        self.jsonMenu = self.returnMenu()["menu"]
        self.__fileName = "orders.json"
        self.orderDict = {}
        self.mainFunction = ["previous","order","menu","exit"]
        self.choice = ["yes", "no"]
        self.initVoice()
        self.startUp()
        try:
            with open(self.__fileName, 'r') as f:
                self.__orders = json.load(f)
        except FileNotFoundError:
            self.__orders = {}
        self.getOrdersFromFile()
        
    def startUp(self):
        print("Welcome to Frenchbot!")
        self.say("Welcome to French bot!")
        self.getNameSpacy()
        self.getMainFunction()
        
    def storeOrdersToFile(self):
        with open(self.__fileName, 'w') as f:
            json.dump(self.__orders, f)
            
    def getOrdersFromFile(self):
        try:
            with open(self.__fileName, 'r') as f:
                self.__orders = json.load(f)
        except FileNotFoundError:
            self.__orders = {}
            
    def displayOrdersForCust(self, name):
        orderList = self.__orders[self.name]
        print(f"Customer: {self.name.title()} :")
        for order in orderList:
            print(f"Order Number: {order}:")
            for dish in orderList[order]:
                print(f"> {dish.title():15s} ${self.getPrice(dish)}")
        print()
        
    def displayOrders(self, name=""):
        print("Order History")
        if self.__orders:
            if name:
                self.displayOrdersForCust(name)
            else:
                for name in self.__orders:
                    self.displayOrdersForCust(name)
        else:
            print("No Orders found")
            
    def insertOrder(self, name, choices):

        try:
            with open("orders.json", 'r') as f:
                self.orders1 = json.load(f)
        except FileNotFoundError:
            self.orders1 = {}

            
        if name in list(self.orders1.keys()):
            orderList = self.orders1[name]
            nextOrder = len(orderList) + 1
        else:
            orderList = {}
            nextOrder = 1
        orderList[nextOrder] = choices
        self.orders1[name] = orderList
        with open("orders.json", 'w+') as f:
            json.dump(self.orders1, f)
        print(f"Order Saved for {name} {self.orders1}")
        exit()

    def returnFoodItems(self):
        finalList = []
        for category in self.jsonMenu:
            for food in self.jsonMenu[category]:
                finalList.append(food)
        return finalList

    def returnFoodPrices(self):
        finalList = []
        for category in self.jsonMenu:
            for food in self.jsonMenu[category]:
                finalList.append(self.jsonMenu[category][food])
        return finalList

    def returnMenu(self):
        try:
            with open("menu.json", 'r') as f:
                self.menu = json.load(f)
        except FileNotFoundError:
            self.menu = {}
        return self.menu
    
    def getPrice(self, dish):
        mealPrice = []
        if dish in self.returnFoodItems():
            return self.returnFoodPrices()[self.returnFoodItems().index(dish)]
                 
    def getMeal(self, name):
        choices = []
        while True:
            courseList = list(menu.keys())
            self.say("From what course would you like to order from? ")
            getCourse = input("From what course would you like to order from? ")
            (match, confidence) = process.extractOne(getCourse, courseList)
            if match in courseList and confidence >= 60:
                mealList = list(menu[match].keys())
                mealDict = menu[match]
                self.say(f"Choose one of the following meals, {' or '.join(mealList)} ")
                mealChoice = input(f"Choose one of the following meals, {' or '.join(mealList)}: ")
                (match, confidence) = process.extractOne(mealChoice, mealList)
                if match in mealList and confidence >=60:
                    mealPrice = mealDict[match]
                    self.say(f'So you want {match}? That costs {int(mealPrice)} dollars')
                    choice = input(f'So you want {match}? That costs ${mealPrice}: ')
                    (choice, confidence) = process.extractOne(choice, self.choice)
                    if choice == 'yes' and confidence >= 60:
                        self.orderDict[match] = mealPrice
                        orderLen = len(list(self.orderDict.keys()))
                        self.say(f'Excellent choice, {self.name}')
                        print(f'Excellent choice, {self.name}')
                        self.say("Would you like to continue ordering, please keep in mind you must order a minimum of 3 dishes")
                        getNextOrder = input("Would you like to continue ordering? Please keep in mind you must order a minimum of 3 dishes: ")
                        (match, confidence) = process.extractOne(getNextOrder, self.choice)
                        if match == 'yes' and confidence >= 60:
                            self.getMeal(name)
                        elif match == 'no' and confidence >= 60:  
                            if orderLen < 3:
                                self.say(f'{self.name.title()}, you have ordered less than 3 dishes, knowing this would you like to continue? This will cancel your order')
                                finishOrder = input(f'{self.name.title()}, you have ordered less than 3 dishes, knowing this would you like to continue? This will cancel your order: ') 
                                (match, confidence) = process.extractOne(finishOrder, self.choice)
                                if match == "yes" and confidence >= 60:
                                    self.exitTask()
                                    break
                                elif match == 'no' and confidence >= 60:
                                    self.getMeal()
                            else:
                                choices.append(self.orderDict)
                                print(self.orderDict)
                                self.insertOrder(name, choice)
                    (match, confidence) = process.extractOne(choice, self.choice)                
                    if match == 'no' and confidence >= 60:
                        self.say("No problem, would you like to restart your order")
                        reOrder = input("No problem, would you like to restart your order? ") 
                        (match, confidence) = process.extractOne(reOrder, self.choice)
                        if match == 'yes' and confidence >= 60:
                            self.getMeal(name)
                        if match == 'no' and confidence >= 60:
                            self.exitTask()
                            break 
            else:
                self.say("Not a valid choice")
                print("Not a valid choice.")
            return mealPrice
            
                      
        
                        
    def printMenu(self):
            json_file = open("menu.json", encoding="utf-8")
            file = json.load(json_file)
            json_file.close()
            self.__jsonMenu = file["menu"]      
            for category in self.__jsonMenu:
                print (f"-------{category.title()}-------")
                for menuItem in self.__jsonMenu[category]:
                    print (menuItem.title()+':', '$' +str(self.__jsonMenu[category][menuItem]))
                print(" ")
        
    def getNameSpacy(self, speech="What is your name? "):
        while True:
            self.say("What is your name?")
            getProper = input(speech)
            name = []
            doc = nlp(getProper.title()+" And")
            for token in doc:
                if token.pos_ in ["PROPN"]:
                    name.append(token.text)
            name = " ".join(name)
            self.say(f"So {name} is your name?")
            justifyName = input(f"So {name} is your name? ")
            (match, confidence) = process.extractOne(justifyName, self.choice)
            if match == 'yes' and confidence >=60:
                self.say(f"Nice to meet you {name}")
                print(f"Nice to meet you {name}")
                break
            elif match == 'no' and confidence >=60:
                self.say("My apologies")
                print("My apologies")
                continue
            else:
                self.say("i dont understand what you mean, please try again")
            return name
        self.name = name
        

    def getMenu(self):
        self.say("You would like to see the menu?")
        getMenu = input("You would like to see the menu? ")
        (match, confidence) = process.extractOne(getMenu, self.choice)
        if match == 'yes' and confidence >=60:
            self.say('Here is the menu')
            self.printMenu()
        elif match == 'no' and confidence >=60:
            self.say("No problem ")
            print("No problem")
        else:
            self.say("Im not sure what you mean, please enter yes or no to answer the question")
            print("Im not sure what you mean, please enter yes or no to answer the question")
            
    def getOrder(self):
        self.say("You would like to order?")
        getOrder = input("You would like to order? ")
        (match, confidence) = process.extractOne(getOrder, self.choice)
        if match == 'yes' and confidence >=60:
            self.say("Here is a menu to assist you in your order. Take as long as you like")
            print("Here is a menu to assist you in your order. Take as long as you like.")                    
            self.printMenu() 
            self.getMeal(self.name)         
        elif match == 'no' and confidence >=60:
            self.say("No problem monsieur")
            print("No problem monsieur")
        else:
            self.say("Im not sure what you mean, please enter yes or no to answer the question")
            print("Im not sure what you mean, please enter yes or no to answer the question")
            
        
    def getPreOrder(self):
        self.say("You would like to see previous orders?")
        seePreOrders = input("You would like to see previous orders? ")
        (match, confidence) = process.extractOne(seePreOrders, self.choice)
        if match == 'yes' and confidence >=60:
            self.getOrdersFromFile()
            self.displayOrders(name)
        elif match == 'no' and confidence >=60:
            self.say(f"No problem, {self.name}")
            print(f"No problem, {self.name}")
            
            
    def exitTask(self):
        self.say(f"Thankyou for ordering with French bot today {self.name} please do come again in the future!")
        print(f"Thankyou for ordering with Frenchbot today {self.name} please do come again in the future!")
        

    def getMainFunction(self):
        self.say("Here are the options")
        print("Options:")
        self.say("Would you like to see previous orders?")
        print("- See Previous Orders")
        self.say("Make an order")
        print("- Make an Order")
        self.say("see the menu")
        print("- See the Menu")
        self.say("or exit")
        print("- Exit")
        while True:
            self.say("What would you like to do?")
            entry = input("What would you like to do? ")
            (choice, confidence) = process.extractOne(entry, self.mainFunction)
            if choice == 'order' and confidence>=70:
                self.getOrder()
            elif choice == 'menu' and confidence>=70:
                self.getMenu()
            elif choice == 'previous' and confidence>=70:
                self.getPreOrder()
            elif choice == 'exit' and confidence>=70:
                self.exitTask()
                break
            else:
                self.say("I dont understand what you mean, please try again")
                print("I dont understand what you mean, please try again")

                
def main():
    test = Frenchbot()

if __name__ == "__main__":
    main()
