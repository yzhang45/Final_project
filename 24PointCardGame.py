from tkinter import *
from itertools import permutations
from itertools import product
import random
import re
import tkinter.messagebox


# Create the Operator class
class Operator(object):
    # Define a variable for operator
    def __init__(self, op):
        self.op = op

    # Define the evaluate method and return the value on two given arguments
    def evaluate(self, first, second):
        if self.op == '*':
            return first * second
        elif self.op == '+':
            return first + second
        elif self.op == '-':
            return first - second
        elif self.op == '/':
            return float(first / second)
        else:
            return "Error"

    # Create the String method and return representation of operand
    def __str__(self):
        return str(self.op)


# Create the Solution class
class Solution(object):
    numbers = []
    operations = []

    # Constructor, do nothing
    def __init__(self):
        pass

    # Evaluate the result of this Solution
    def evaluate(self):
        if len(self.numbers) > 0:
            result = self.numbers[0]
            for i in range(1, len(self.numbers)):
                first = result
                second = self.numbers[i]
                operator = self.operations[i - 1]

                # Recursive call
                result = operator.evaluate(first, second)
            return result
        else:
            return False

    # Return string representation of this Solution
    def __str__(self):
        strResult = str(self.numbers[0])
        for i in range(1, len(self.numbers)):
            operator = self.operations[i - 1].op
            number = self.numbers[i]
            strResult += "" + operator + "" + str(number)
        return strResult


# Find a solution and evaluate an expression for 24 point
# Define verify method
def verify():
    # To get the expression entered by user
    exp = str(exprs.get())

    # Extract operator, number separately from expression
    operatorList = re.findall('[+ - /* // () ]', exp)
    numberList = []
    numberList = re.findall(r'\d+', exp)

    # Only 4 numbers are allowed, populate allowed list
    numbersAllowed = []
    for i in range(len(cardValues)):
        numbersAllowed.append(cardValues[i] % 13 + 1)

    for i in range(len(numberList)):
        # Compare numbers in expression with allowed
        if eval(numberList[i]) not in numbersAllowed:
            tkinter.messagebox.showinfo("Incorrect", "You have to use the four cards shown.")
            return

    # Evaluate the expression
    result = eval(exp)
    if result == 24:
        tkinter.messagebox.showinfo("Correct", "You got it.")
        return
    else:
        tkinter.messagebox.showinfo("Incorrect", exp + " is not 24")
        return


# Define getCards method
def getCards():
    # Choose four random cards
    for i in range(4):
        cardValues[i] = random.randint(1, 52)


# Set the images of selected 4 cards
def setImages():
    for i in range(4):
        labelList[i]["image"] = imageList[cardValues[i]]


# Select the new set of cards and display their image
def reset():
    getCards()
    setImages()
    SolVar.set("Solution to be displayed here")
    exprs.set("")


# Create getSolution method, try all permutations of operators and numbers
def getSolution():
    cards = []
    for i in range(len(cardValues)):
        cards.append(cardValues[i] % 13 + 1)

    # Define constant name for Operators
    MUL = Operator('*')
    ADD = Operator('+')
    SUB = Operator('-')
    DIV = Operator('/')
    OPS = [MUL, ADD, SUB, DIV]
    crntSol = Solution()

    solution = StringVar()

    # Try all permutations of 4 cards in list
    for number in permutations(cards):
        for operation in product(OPS, repeat=3):

            # Construct a new current solution for testing
            crntSol.numbers = number
            crntSol.operations = operation
            if crntSol.evaluate() == 24:
                # Put solution in variable for entry box
                SolVar.set(crntSol)
                return
    # No solution can be found
    SolVar.set("Could not find a solution. Refresh.")


# Create a window and set the tile
window = Tk()
window.title("24 point card game")

# Create a canvas and add it to the window
width = 300
height = 5
canvas = Canvas(window, width=width, height=height)
canvas.pack()

# Create a frame and add it to the window
frame = Frame(window)
frame.pack()

# Add two buttons, an entry to frame
Button(frame, text="Find a solution:", command=getSolution).pack(side=LEFT)
SolVar = StringVar()
SolVar.set("Solution to be displayed here")
solEntry = Entry(frame, textvariable=SolVar, justify=RIGHT, width=27).pack(side=LEFT)
Button(frame, text="Refresh", command=reset).pack(side=LEFT)

# Store all images for 52 cards
imageList = []
for i in range(1, 53):
    imageList.append(PhotoImage(file="image/card/" + str(i) + ".gif"))

# Create another frame and add it to window
frame1 = Frame(window)
frame1.pack()

labelList = []  # A list of four labels
cardValues = 4 * [0]  # Main list of card values

# Display selected four cards
for i in range(4):
    labelList.append(Label(frame1, image=imageList[cardValues[i]]))
    labelList[i].pack(side=LEFT)

# Set the images of selected four cards
setImages()

# Create a new frame and add it to window
frame1 = Frame(window)
frame1.pack()

# Add labels, entry and buttons to frame
Label(frame1, text="Enter an expression:").pack(side=LEFT)
exprs = StringVar()
entry = Entry(frame1, textvariable=exprs, justify=RIGHT, width=20).pack(side=LEFT)
Button(frame1, text="Verify", command=verify).pack(side=LEFT)

# Create an event loop
window.mainloop()

#
# class DeckOfCardsGUI:
#     def __init__(self):
#         window = Tk()  # Create a window
#         window.title("Pick Four Cards Randomly")  # Set title
#
#         self.imageList = []  # Store images for cards
#         for i in range(1, 53):
#             self.imageList.append(PhotoImage(file="image/card/"
#                                                   + str(i) + ".gif"))
#
#         frame = Frame(window)  # Hold four labels for cards
#         frame.pack()
#
#         self.labelList = []  # A list of four labels
#         for i in range(4):
#             self.labelList.append(Label(frame,
#                                         image=self.imageList[i]))
#             self.labelList[i].pack(side=LEFT)
#
#         Button(window, text="Shuffle",
#                command=self.shuffle).pack()
#
#         window.mainloop()  # Create an event loop
#
#     # Choose four random cards
#     def shuffle(self):
#         random.shuffle(self.imageList)
#         for i in range(4):
#             self.labelList[i]["image"] = self.imageList[i]
#
#
# DeckOfCardsGUI()  # Create GUI
