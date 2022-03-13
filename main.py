import corpus
import lm
from tkinter import *
from tkinter import Label, Button, filedialog, messagebox, ttk

welcome = "Welcome to Siobhan's Text Generator!" 
instructions1 = "Please select one or more text files (.txt) you would like to mimic."
instructions2 = "Please input the length of n-gram you'd like to use."
instructions3 = "How many texts would you like to generate?"
info1 = "Note: The generated text could be one word or more."
info2 = "(Please resize the window to see the Save and Close buttons if they are hidden.)"
instructions4 = "Upload another text file to calculate its perplexity against the training file(s)."
info3 = "Note: It might say (Not Responding) while processing Test Perplexity. Please wait."


root = Tk()
root.title("Siobhan's Text Generator")
Label(root, text=welcome).grid(row=0, columnspan=3)
Label(root, text=instructions1).grid(row=1, columnspan=3)

# Properties

root.lang = None
root.selection = ''
root.simple_generated = ''
root.greedy_generated = ''
root.beam_generated = ''
root.perplexity = 0
root.greedy_perplexity = 0
root.beam_perplexity = 0
root.test_text = ''
root.test_perplexity = 0

# Training tools

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

Label(root, text=instructions2).grid(row=4, columnspan=3)
n_input = Entry(root, border=5, width=5)
n_input.grid(row=5, column=0)

def trainlm():
    n = n_input.get()
    if int(n) <= 0:
        messagebox.showwarning("Ineligible Input", "Please enter a number greater than 0.")
    else:
        root.lang = lm.LanguageModel(int(n))
        tokens = corpus.tokenize(root.selection)
        root.lang.train(tokens)
        num = len(root.lang.token_list)
        num_tokens = f'The number of tokens is {num}'
        most_token = f'The most common word {root.lang.most_common_word()}'
        most_gram = f'The most common {n}-gram {root.lang.most_common_gram()}'
        most_word_gram = f'The most common {n}-gram starting with \'{root.lang.common_word}\' {root.lang.most_common_word_gram()}'
        Label(root, text=num_tokens).grid(row=6, columnspan=3)
        Label(root, text=most_token).grid(row=7, columnspan=3)
        Label(root, text=most_gram).grid(row=8, columnspan=3)
        Label(root, text=most_word_gram).grid(row=9, columnspan=3)

Button(root, text="Train and Display Information", command=trainlm, bg="#caced1").grid(row=5, column=1)

Label(root, text=instructions3).grid(row=10, columnspan=3)
Label(root, text=info1).grid(row=11, columnspan=3)
gen_input = Entry(root, border=5, width=5)
gen_input.grid(row=12, column=0)

# Generate Text functions

def generate():
    top = Toplevel()
    top.title("Generated Texts")
    top.geometry("800x400")
    Label(top, text=info2).pack()

    gen = gen_input.get()
    for i in range(int(gen)):
        lines = root.lang.generate()
        Label(top, text=lines, wraplength=750).pack()
        root.simple_generated += lines

    Button(top, text="Save to File", command=save_simple, bg="#caced1").pack(pady=10)
    Button(top, text="Close Window", command=top.destroy, bg="#caced1").pack(pady=10)

def greedy_generate():
    top = Toplevel()
    top.title("Greedy Texts")
    top.geometry("800x400")
    Label(top, text=info2).pack()

    gen = gen_input.get()
    for i in range(int(gen)):
        lines = root.lang.greedy_generate()
        Label(top, text=lines, wraplength=750).pack()
        root.greedy_generated += lines

    Button(top, text="Save to File", command=save_greedy, bg="#caced1").pack(pady=10)
    Button(top, text="Close Window", command=top.destroy, bg="#caced1").pack(pady=10)

def beam_generate():
    top = Toplevel()
    top.title("Beam Texts")
    top.geometry("800x400")
    Label(top, text=info2).pack()

    gen = gen_input.get()
    for i in range(int(gen)):
        lines = root.lang.beam_generate()
        Label(top, text=lines, wraplength=750).pack()
        root.beam_generated += lines

    Button(top, text="Save to File", command=save_beam, bg="#caced1").pack(pady=10)
    Button(top, text="Close Window", command=top.destroy, bg="#caced1").pack(pady=10)

# Save functions

def save_simple():
    root.save_file = filedialog.asksaveasfile(mode='w', filetypes=[("Text Document", "*.txt"), ("PDF", "*.pdf")])
    root.save_file.write(root.simple_generated)
    root.save_file.close()

def save_greedy():
    root.save_file = filedialog.asksaveasfile(mode='w', filetypes=[("Text Document", "*.txt"), ("PDF", "*.pdf")])
    root.save_file.write(root.greedy_generated)
    root.save_file.close()

def save_beam():
    root.save_file = filedialog.asksaveasfile(mode='w', filetypes=[("Text Document", "*.txt"), ("PDF", "*.pdf")])
    root.save_file.write(root.beam_generated)
    root.save_file.close()

# Perplexity functions

def simple_perplex():
    root.perplexity = root.lang.get_perplexity_score(root.simple_generated)
    Label(root, text=str(root.perplexity)).grid(row=13, column=2)

def greedy_perplex():
    root.greedy_perplexity = root.lang.get_perplexity_score(root.greedy_generated)
    Label(root, text=str(root.greedy_perplexity)).grid(row=14, column=2)

def beam_perplex():
    root.beam_perplexity = root.lang.get_perplexity_score(root.beam_generated)
    Label(root, text=str(root.beam_perplexity)).grid(row=15, column=2)

def test_perplex():
    root.test_perplexity = root.lang.get_test_perplexity(root.test_text)

    Label(root, text=str(root.test_perplexity)).grid(row=19, column=2)

# Generate Buttons

Button(root, text="Generate Simple Text", command=generate, bg="#caced1").grid(row=13, column=0, pady=10)
Button(root, text="Generate Greedy Text", command=greedy_generate, bg="#caced1").grid(row=14, column=0, pady=10)
Button(root, text="Generate Beam Text", command=beam_generate, bg="#caced1", width=17).grid(row=15, column=0, pady=10)

# Perplexity Buttons

Button(root, text="Caclulate Simple Perplexity", command=simple_perplex, bg="#caced1").grid(row=13, column=1, pady=10)
Button(root, text="Caclulate Greedy Perplexity", command=greedy_perplex, bg="#caced1").grid(row=14, column=1, pady=10)
Button(root, text="Caclulate Beam Perplexity", command=beam_perplex, bg="#caced1", width=21).grid(row=15, column=1, pady=10)

# Test Text Tools

Label(root, text=instructions4).grid(row=16, columnspan=3)

def get_file():
    root.file_path = filedialog.askopenfilenames(title="Select a text file or files", filetypes=[("text files", "*.txt")])
    for element in root.file_path:
        file = open(element, 'r')
        root.test_text += file.read()
        file.close()
    file_num = len(root.file_path)
    message = f'{file_num} file(s) uploaded successfully.'
    Label(root, text=message).grid(row=17, column=1)

Button(root, text="Browse", command=get_file, bg="#caced1").grid(row=17, column=0)

Label(root, text=info3).grid(row=18, columnspan=3)

Button(root, text="Caclulate Test Perplexity", command=test_perplex, bg="#caced1").grid(row=19, column=0)

# Close

Button(root, text="Close Program", command=exit, bg="#caced1").grid(row=20, columnspan=3)
root.mainloop()