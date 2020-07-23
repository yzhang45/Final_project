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
        elif self.op == '/':
            return first / second
        elif self.op == '+':
            return first + second
        elif self.op == '-':
            return first - second
        else:
            return "Error"

    # Define the __repr__ method and return string
    def __repr__(self):
        return str(self.op)


# Create the Hint class
class Hint(object):
    numbers = []
    operations = []

    # Create an init constructor
    def __init__(self):
        pass

    # Evaluate the result of hint
    def evaluate(self):
        if len(self.numbers) > 0:
            result = self.numbers[0]
            for i in range(1, len(self.numbers)):
                assert i > 0
                first = result
                second = self.numbers[i]
                operator = self.operations[i - 1]

                # Recursive call
                result = operator.evaluate(first, second)
            return result
        else:
            return False

    # Create the repr representation for this Hint
    def __repr__(self):
        strResult = str(self.numbers[0])
        for i in range(1, len(self.numbers)):
            operator = self.operations[i - 1].op
            number = self.numbers[i]
            strResult += "" + operator + "" + str(number)
        return strResult


# Find a hint and evaluate an expression for 24 point
# Define verify function
def verify():
    # To get the expression entered by user
    exp = str(expr.get())

    # Extract operator, number separately from expression
    operatorList = re.findall('[() * / + - ]', exp)
    numberList = []
    numberList = re.findall(r'\d+', exp)

    # Only 4 numbers are allowed, store in allowed list
    numbersAllowed = []
    for i in range(len(cardValues)):
        numbersAllowed.append(cardValues[i] % 13 + 1)

    # Compare numbers in expression with allowed
    for i in range(len(numberList)):
        if eval(numberList[i]) not in numbersAllowed:
            tkinter.messagebox.showinfo("Incorrect", "You have to use the four cards shown!")
            return

    # Evaluate the expression, handle exception and write expression into the file
    try:
        result = eval(exp)
        if result == 24:
            file = open("result.txt", "w")
            file.write("You got it! The Correct result of the expression is : " + str(exp))
            file.close()
            tkinter.messagebox.showinfo("Correct", "You got it!")
            return

        else:
            tkinter.messagebox.showinfo("Incorrect", exp + " is not 24")
            return

    except SyntaxError:
        print("Oops! That was no valid expression.  Try again...")


# Define getCards function
def getCards():
    # Choose four random cards
    for i in range(4):
        cardValues[i] = random.randrange(1, 52)


# Set the images of selected 4 cards
def setImages():
    for i in range(4):
        labelList[i]["image"] = imageList[cardValues[i]]


# Select the new set of cards and display their image
def reset():
    getCards()
    setImages()
    HintVar.set("Hint to be displayed here")
    expr.set("")


# Create getHint function, try all permutations of operators and numbers
def getHint():
    cards = []
    for i in range(len(cardValues)):
        cards.append(cardValues[i] % 13 + 1)

    # Define constant name for Operators
    mul = Operator('*')
    div = Operator('/')
    add = Operator('+')
    sub = Operator('-')
    operators = [mul, div, add, sub]
    currentHint = Hint()

    # Try all permutations of 4 cards in list
    for number in permutations(cards):
        for operation in product(operators, repeat=3):
            # Construct a new current hint for testing
            currentHint.numbers = number
            currentHint.operations = operation
            if currentHint.evaluate() == 24:
                HintVar.set(currentHint)
                return

    # No hint can be found
    HintVar.set("Could not find a hint. Refresh.")


# Create a window and set the tile
window = Tk()
window.title("24 point card game")
label = Label(window, text=" Welcome to 24 Point card game ", fg='purple')
label.pack()

# Create a canvas and add it to the window
width = 500
height = 3
canvas = Canvas(window, width=width, height=height)
canvas.pack()

# Create a frame and add it to the window
frame = Frame(window)
frame.pack()

# Add two buttons, an entry to frame
Button(frame, text="Find a hint:", command=getHint).pack(side=LEFT)
HintVar = StringVar()
HintVar.set("Hint to be displayed here")
hintEntry = Entry(frame, textvariable=HintVar, justify=RIGHT, width=27).pack(side=LEFT)
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
getCards()  # Choose four random cards

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
Label(frame1, text="Enter an expression:", fg="blue").pack(side=LEFT)
expr = StringVar()
entry = Entry(frame1, textvariable=expr, justify=RIGHT, width=20).pack(side=LEFT)
Button(frame1, text="Verify", command=verify).pack(side=LEFT)

# Create an event loop
window.mainloop()

