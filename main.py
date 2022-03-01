import corpus
import lm
from tkinter import *
from tkinter import Label, Button, filedialog

welcome = "Welcome to Siobhan's Text Generator!" 
instructions1 = "Please select one or more text files (.txt) you would like to mimic."
instructions2 = "Please input the length of n-gram you'd like to use."
instructions3 = "How many texts would you like to generate?"
information3 = "Note: The text could be one word or a whole paragraph."

root = Tk()
root.title("Siobhan's Text Generator")
Label(root, text=welcome).grid(row=0, columnspan=2)
Label(root, text=instructions1).grid(row=1, columnspan=2)

root.selection = ''
root.to_be_saved = ''
root.lang = None
root.perplexity = 0

def get_file():
    root.file_path = filedialog.askopenfilenames(title="Select a text file or files", filetypes=[("text files", "*.txt")])
    for element in root.file_path:
        file = open(element, 'r')
        root.selection += file.read()
        file.close()
    file_num = len(root.file_path)
    message = f'{file_num} file(s) uploaded successfully.'
    Label(root, text=message).grid(row=2, column=1)

Button(root, text="Browse", command=get_file, bg="#caced1").grid(row=2, column=0)

Label(root, text=instructions2).grid(row=4, columnspan=2)
n_input = Entry(root, border=5)
n_input.grid(row=5, column=0)

def trainlm():
    n = n_input.get()
    root.lang = lm.LanguageModel(int(n))
    tokens = corpus.tokenize(root.selection)
    root.lang.train(tokens)
    num = len(root.lang.token_list)
    num_tokens = f'The number of tokens is {num}'
    most_token = f'The most common word {root.lang.most_common_word()}'
    most_gram = f'The most common {n}-gram {root.lang.most_common_gram()}'
    most_word_gram = f'The most common {n}-gram starting with \'{root.lang.common_word}\' {root.lang.most_common_word_gram()}'
    Label(root, text=num_tokens).grid(row=6, columnspan=2)
    Label(root, text=most_token).grid(row=7, columnspan=2)
    Label(root, text=most_gram).grid(row=8, columnspan=2)
    Label(root, text=most_word_gram).grid(row=9, columnspan=2)

Button(root, text="Train and Display Info", command=trainlm, bg="#caced1").grid(row=5, column=1)

Label(root, text=instructions3).grid(row=10, columnspan=2)
Label(root, text=information3).grid(row=11, columnspan=2)
gen_input = Entry(root, border=5)
gen_input.grid(row=12, column=0)

def generate():
    top = Toplevel()
    top.title("Generated Texts")
    #top.geometry("800x800")
    gen = gen_input.get()
    for i in range(int(gen)):
        lines = root.lang.generate()
        Label(top, text=lines, wraplength=750).pack()
        root.to_be_saved += lines

    Button(top, text="Save to File", command=save, bg="#caced1").pack()
    Button(top, text="Close Window", command=top.destroy, bg="#caced1").pack()

def save():
    root.save_file = filedialog.asksaveasfile(mode='w', filetypes=[("Text Document", "*.txt"), ("PDF", "*.pdf")])
    root.save_file.write(root.to_be_saved)
    root.save_file.close()

def perplex():
    root.perplexity = root.lang.get_perplexity_score(root.to_be_saved)
    Label(root, text=str(root.perplexity)).grid(row=13, column=1)
    
Button(root, text="Generate Text", command=generate, bg="#caced1").grid(row=12, column=1)

Button(root, text="Caclulate Perplexity", command=perplex, bg="#caced1").grid(row=13, column=0)

Button(root, text="Close Program", command=exit, bg="#caced1").grid(row=14, columnspan=2)

root.mainloop()