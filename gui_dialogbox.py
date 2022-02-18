from tkinter import *
from tkinter import Label, Button, messagebox

from matplotlib.pyplot import text

root = Tk()
root.title("Learning about dialog boxes")

start_info = Label(text="Welcome to this little practice project for GUI!")
start_info.grid(row=0, column=0, columnspan=3)

def pop_info():
    messagebox.showinfo("Infobox", "Here is some info")

# messagebox can showinfo -> ok, 
# showwarning -> ok, 
# showerror -> ok, 
# askquestion -> yes / no, 
# askokcancel -> 1 / 0, 
# askyesno -> 1 / 0

def pop_yn():
    response = messagebox.askyesno("Yes or No?", "Would you like to save your progress?")
    if response == 1:
        Label(root, text="You clicked yes.").grid(row=2, column=0)
    else:
        Label(root, text="You clicked no.").grid(row=2, column=0)

info_popup = Button(root, text="Info", command=pop_info)
info_popup.grid(row=1, column=0, padx=50)

yn_popup = Button(root, text="Save", command=pop_yn)
yn_popup.grid(row=1, column=1, padx=50)

exit = Button(root, text="Exit", command=exit)
exit.grid(row=1, column=2, padx=50)

root.mainloop()