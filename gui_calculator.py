from tkinter import *

root = Tk()
root.title("GUI Practice: Calculator")

# Create input field
inpt = Entry(root, border=5)
inpt.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
# inpt.insert(0, "Enter a number") [puts default text into the field]

# Define Button Functions
def button_click(num):
    current = inpt.get()
    inpt.delete(0, END)
    inpt.insert(0, str(current) + str(num))

def button_clear():
    inpt.delete(0, END)

def button_addition():
    first_num = inpt.get()
    global f_num
    global oper
    oper = 'addition' 
    f_num = int(first_num)
    inpt.delete(0, END)

def button_subtract():
    first_num = inpt.get()
    global f_num
    global oper
    oper = 'subtraction' 
    f_num = int(first_num)
    inpt.delete(0, END)

def button_multiply():
    first_num = inpt.get()
    global f_num
    global oper
    oper = 'multiplication' 
    f_num = int(first_num)
    inpt.delete(0, END)

def button_divide():
    first_num = inpt.get()
    global f_num
    global oper
    oper = 'division' 
    f_num = int(first_num)
    inpt.delete(0, END)

def button_equal():
    second_num = inpt.get()
    inpt.delete(0, END)
    if oper == 'addition':
        inpt.insert(0, f_num + int(second_num))
    if oper == 'subtraction':
        inpt.insert(0, f_num - int(second_num))
    if oper == 'multiplication':
        inpt.insert(0, f_num * int(second_num))
    if oper == 'division':
        inpt.insert(0, f_num / int(second_num))

# Define Buttons
#command=root.destroy closes the window
button1 = Button(root, text="1", padx=40, command=lambda: button_click(1))
button2 = Button(root, text="2", padx=40, command=lambda: button_click(2))
button3 = Button(root, text="3", padx=40, command=lambda: button_click(3))
button4 = Button(root, text="4", padx=40, command=lambda: button_click(4))
button5 = Button(root, text="5", padx=40, command=lambda: button_click(5))
button6 = Button(root, text="6", padx=40, command=lambda: button_click(6))
button7 = Button(root, text="7", padx=40, command=lambda: button_click(7))
button8 = Button(root, text="8", padx=40, command=lambda: button_click(8))
button9 = Button(root, text="9", padx=40, command=lambda: button_click(9))
button0 = Button(root, text="0", padx=40, command=lambda: button_click(0))

button_add = Button(root, text="+", padx=40, command=button_addition)
button_eq = Button(root, text="=", padx=91, command=button_equal, bg="#33adff")
button_clr = Button(root, text="Clear", padx=79, command=button_clear)

button_sub = Button(root, text="-", padx=40, command=button_subtract)
button_mul = Button(root, text="x", padx=40, command=button_multiply)
button_div = Button(root, text="/", padx=40, command=button_divide)

# Show buttons on screen
button1.grid(row=3, column=0)
button2.grid(row=3, column=1)
button3.grid(row=3, column=2)

button4.grid(row=2, column=0)
button5.grid(row=2, column=1)
button6.grid(row=2, column=2)

button7.grid(row=1, column=0)
button8.grid(row=1, column=1)
button9.grid(row=1, column=2)

button0.grid(row=4, column=0)
button_add.grid(row=4, column=1)
button_sub.grid(row=4, column=2)

button_clr.grid(row=6, column=1, columnspan=2)
button_eq.grid(row=5, column=1, columnspan=2)

button_mul.grid(row=5, column=0)
button_div.grid(row=6, column=0)

root.mainloop()