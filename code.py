from tkinter import *
from PIL import ImageTk, Image
import random
import tkinter.messagebox
import threading

window = Tk()
window.title("ATM")
window.resizable(False, False)

# --- Session Timeout ---
timeout_seconds = 30
last_action = [None]  # Use list for mutability in nested functions

def reset_timeout():
    last_action[0] = window.after_cancel(last_action[0]) if last_action[0] else None
    last_action[0] = window.after(timeout_seconds * 1000, reset_to_welcome)

def reset_to_welcome():
    global atmIdText, pinText
    atmIdText = ""
    pinText = ""
    atmIdFieldKey.set("")
    pinFieldKey.set("")
    goToPage0()

def user_action():
    reset_timeout()

# Field keys
atmIdFieldKey = StringVar()
pinFieldKey = StringVar()

# Variables for fields
atmIdText = ""
pinText = ""

# Correct id and pin
correctAtmId = '2020'
correctPin = '6344'

# To keep track of the SCREENS
screenNumber = 0

# Number list
normalList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
shuffledList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]

# A global variable to use everywhere
globalList = normalList

# --- Disable keyboard input for Entry fields ---
def block_typing(event):
    return "break"

# Functions of ENTER button
def pressEnter():
    user_action()
    if(screenNumber==0):
        goToPage1()
    elif(screenNumber==1):
        goToPage2()
    elif(screenNumber==2):
        goToPage3()
    elif(screenNumber==3):
        window.destroy()

# For creating color and number table
class Table:
    def __init__(self, page):
        global globalList
        random.shuffle(shuffledList)
        if(screenNumber==1):
            globalList = normalList
        elif(screenNumber==2):
            globalList = shuffledList
        # take the data
        color_choices = ['Red', 'Dark Green', 'Blue', 'Yellow', 'Brown', 'Orange', 'Purple', 'Grey', 'Pink', 'Light Green']
        random.shuffle(color_choices)
        lst = list(zip(color_choices, globalList, [img1,img2,img3,img4,img5,img6,img7,img8,img9,img10]))
        newFrame = Frame(page, bg='Light blue')
        newFrame.grid(columnspan=5)
        for i in range(2):
            for j in range(10):
                bgColor = lst[j][0]
                lstimg = lst[j][2]
                if(i==0):
                    e = Label(newFrame, height=45, width=45, image=lstimg, bg=bgColor)
                    e.grid(row=i, column=j)
                else:
                    e = Text(newFrame, height=2, width=5, fg='Black', font=('Ariel', 10), padx=8, pady=4, bg=bgColor)
                    e.grid(row=i, column=j)
                    e.insert(END, lst[j][1])

# For INTEGER buttons
def pressButton(num):
    global atmIdText, pinText
    user_action()
    if screenNumber == 1:
        atmIdText = atmIdText + str(num)
        atmIdFieldKey.set(atmIdText)
    elif screenNumber == 2:
        pinText = pinText + str(num)
        pinFieldKey.set(pinText)

# For CLEAR button
def clearAll():
    global atmIdText, pinText
    user_action()
    if screenNumber == 1:
        atmIdText = ""
        atmIdFieldKey.set(atmIdText)
    elif screenNumber == 2:
        pinText = ""
        pinFieldKey.set(pinText)

# For BACKSPACE button
def clearOne():
    global atmIdText, pinText
    user_action()
    if screenNumber == 1:
        atmIdText = atmIdText[:-1]
        atmIdFieldKey.set(atmIdText)
    elif screenNumber == 2:
        pinText = pinText[:-1]
        pinFieldKey.set(pinText)

# Main frame
mainFrame = Frame(window, bg='#D4D4D3')
mainFrame.grid(columnspan=5)

def goToPage3():
    global globalPageKey, screenNumber
    globalPageKey.destroy()
    screenNumber = 3
    finalText = ''
    if ((atmIdText == correctAtmId) and (pinText == correctPin)):
        finalText = 'Thank You'
    else:
        finalText = 'Failed'
    page3 = LabelFrame(mainFrame, bg='Light blue')
    page3.grid(columnspan=5, ipadx=270, ipady=110, padx=10, pady=10)
    globalPageKey = page3
    finalTextLabel = Label(page3, text=finalText, font=('Courier', 20), bg='Light blue')
    finalTextLabel.place(relx=0.5, rely=0.35, anchor='center')
    def retry():
        global atmIdText, pinText
        page3.destroy()
        atmIdText = ""
        atmIdFieldKey.set(atmIdText)
        pinText = ""
        pinFieldKey.set(pinText)
        goToPage1()
    if ((atmIdText == correctAtmId) and (pinText == correctPin)):
        exitButton = Button(page3, text='Exit', bg='White', height=2, width=8, command=window.destroy)
        exitButton.place(relx=0.5, rely=0.65, anchor='center')
    else:
        retryButton = Button(page3, text='Retry', bg='white', height=2, width=8,command=lambda:retry())
        retryButton.place(relx=0.4, rely=0.65, anchor='center')
        exitButton = Button(page3, text='Exit', bg='White', height=2, width=8, command=window.destroy)
        exitButton.place(relx=0.6, rely=0.65, anchor='center')
    reset_timeout()

def goToPage2():
    global globalPageKey, screenNumber
    globalPageKey.destroy()
    screenNumber = 2
    page2 = LabelFrame(mainFrame, bg='Light blue')
    page2.grid(columnspan=5, ipady=60, padx=10, pady=10)
    globalPageKey = page2
    pin = Label(page2, text="PIN", bg='Light blue', font=('Arial', 14, 'bold'))
    pin.place(relx=0.4, rely=0.6, anchor='center')
    pinField = Entry(page2, textvariable=pinFieldKey, font=('Arial', 14))
    pinField.place(relx=0.6, rely=0.6, anchor='center')
    pinField.bind('<Key>', block_typing)
    pinSubmit = Button(page2, text='Submit', bg='White', height=2, width=10, command=lambda: goToPage3())
    pinSubmit.place(relx=0.5, rely=0.85, anchor='center')
    instr = Label(page2, text='For your security, the keypad is randomized.\nUse only the on-screen buttons.', bg='Light blue', fg='red', font=('Arial', 10, 'italic'))
    instr.place(relx=0.5, rely=0.2, anchor='center')
    p2 = Table(page2)
    reset_timeout()

def goToPage1():
    global globalPageKey, screenNumber
    globalPageKey.destroy()
    screenNumber = 1
    page1 = LabelFrame(mainFrame, bg='Light blue')
    page1.grid(columnspan=5, ipady=60, padx=10, pady=10)
    globalPageKey = page1
    atmId = Label(page1, text="ATM ID", bg='Light blue', font=('Arial', 14, 'bold'))
    atmId.place(relx=0.4, rely=0.6, anchor='center')
    atmIdField = Entry(page1, textvariable=atmIdFieldKey, font=('Arial', 14))
    atmIdField.place(relx=0.6, rely=0.6, anchor='center')
    atmIdField.bind('<Key>', block_typing)
    atmIdSubmit = Button(page1, text='Next', bg='White', height=2, width=10, command=lambda: goToPage2())
    atmIdSubmit.place(relx=0.5, rely=0.85, anchor='center')
    instr = Label(page1, text='Enter your ATM ID using only the on-screen buttons.', bg='Light blue', fg='red', font=('Arial', 10, 'italic'))
    instr.place(relx=0.5, rely=0.2, anchor='center')
    p1 = Table(page1)
    reset_timeout()

def goToPage0():
    global globalPageKey, screenNumber
    try:
        globalPageKey.destroy()
    except:
        pass
    screenNumber = 0
    page0 = LabelFrame(mainFrame, bg='Light blue')
    page0.grid(columnspan=5, ipadx=270, ipady=110, padx=10, pady=10)
    globalPageKey = page0
    welcomeText = Label(page0, text='Welcome to Personal Bank atm', font=('Courier', 20), bg='Light blue')
    welcomeText.place(relx=0.5, rely=0.35, anchor='center')
    nextbutton = Button(page0, text='Next', bg='White', height=2, width=10, command=lambda: goToPage1())
    nextbutton.place(relx=0.5, rely=0.65, anchor='center')
    reset_timeout()

# Assigning a global page to access each page from anywhere
goToPage0()

# Full frame for buttons
bottomFrame = Frame(window, bg='#D4D4D3')
bottomFrame.grid(columnspan=5, ipadx=140)

# Frame for fixed buttons
buttonsFrame = LabelFrame(bottomFrame, bg='#AAA9A8')
buttonsFrame.grid(columnspan=5, padx=10, pady=10, sticky='')
bottomFrame.grid_rowconfigure(0, weight=1)
bottomFrame.grid_columnconfigure(0, weight=1)

# Button shapes
img1 = ImageTk.PhotoImage(Image.open("btn1.png"))
img2 = ImageTk.PhotoImage(Image.open("btn2.png"))
img3 = ImageTk.PhotoImage(Image.open("btn3.png"))
img4 = ImageTk.PhotoImage(Image.open("btn4.png"))
img5 = ImageTk.PhotoImage(Image.open("btn5.png"))
img6 = ImageTk.PhotoImage(Image.open("btn6.png"))
img7 = ImageTk.PhotoImage(Image.open("btn7.png"))
img8 = ImageTk.PhotoImage(Image.open("btn8.png"))
img9 = ImageTk.PhotoImage(Image.open("btn9.png"))
img10 = ImageTk.PhotoImage(Image.open("btn10.png"))

# Fixed buttons
button1 = Button(buttonsFrame, image=img1, fg='Black', bg='Black', command=lambda: pressButton(globalList[0]), height=40, width=40)
button1.grid(row=1, column=0, padx=5, pady=5)
button2 = Button(buttonsFrame, image=img2, fg='Black', bg='Black', command=lambda: pressButton(globalList[1]), height=40, width=40)
button2.grid(row=1, column=1, padx=5, pady=5)
button3 = Button(buttonsFrame, image=img3, fg='Black', bg='Black', command=lambda: pressButton(globalList[2]), height=40, width=40)
button3.grid(row=1, column=2, padx=5, pady=5)
button4 = Button(buttonsFrame, image=img4, fg='Black', bg='Black', command=lambda: pressButton(globalList[3]), height=40, width=40)
button4.grid(row=2, column=0, padx=5, pady=5)
button5 = Button(buttonsFrame, image=img5, fg='Black', bg='Black', command=lambda: pressButton(globalList[4]), height=40, width=40)
button5.grid(row=2, column=1, padx=5, pady=5)
button6 = Button(buttonsFrame, image=img6, fg='Black', bg='Black', command=lambda: pressButton(globalList[5]), height=40, width=40)
button6.grid(row=2, column=2, padx=5, pady=5)
button7 = Button(buttonsFrame, image=img7, fg='Black', bg='Black', command=lambda: pressButton(globalList[6]), height=40, width=40)
button7.grid(row=3, column=0, padx=5, pady=5)
button8 = Button(buttonsFrame, image=img8, fg='Black', bg='Black', command=lambda: pressButton(globalList[7]), height=40, width=40)
button8.grid(row=3, column=1, padx=5, pady=5)
button9 = Button(buttonsFrame, image=img9, fg='Black', bg='Black', command=lambda: pressButton(globalList[8]), height=40, width=40)
button9.grid(row=3, column=2, padx=5, pady=5)
button0 = Button(buttonsFrame, image=img10, fg='Black', bg='Black', command=lambda: pressButton(globalList[9]), height=40, width=40)
button0.grid(row=4, column=1, padx=5, pady=5)
backspace = Button(buttonsFrame, text='BACKSPACE', fg='Black', bg='Light grey', command=lambda: clearOne(), height=2, width=10)
backspace.grid(row=1, column=4, padx=5, pady=5)
clear = Button(buttonsFrame, text='CLEAR', fg='Black', bg='Light grey', command=lambda: clearAll(), height=2, width=10)
clear.grid(row=2, column=4, padx=5, pady=5)
enter = Button(buttonsFrame, text='ENTER', fg='Black', bg='Light grey', command=lambda: pressEnter(), height=2, width=10)
enter.grid(row=3, column=4, padx=5, pady=5)

# To open the screen
window.mainloop()