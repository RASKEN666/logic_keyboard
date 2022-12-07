from tkinter import *

def copy_text(event=None):
    try:
        len(entry_box.selection_get())
    except:
        return
    selection = entry_box.selection_get()
    entry_box.clipboard_clear()
    entry_box.clipboard_append(selection)
    
def is_selected():
    try:
        len(entry_box.selection_get())
    except:
        return False
    return True

def click1(letter='', logop=''):
    entry_box.config(state=NORMAL)
    if not log_shift_on:
        if case_shift_on or len(letter+logop)>2:
            char = letter
        else:
            char=letter.lower()
    else:
        char = logop
    
    if is_selected():
        entry_box.delete(SEL_FIRST, SEL_LAST)

    entry_box.insert(entry_box.index('insert'), char)
    entry_box.config(state=DISABLED)

def multi_key_press(event):
    if event.keycode == 219:
        pressed = "´"
        logop ='≥'
    else:
        pressed = "¨"
        logop ='~'

    click1(pressed, logop)

def shift_key_press(event):
    if case_shift_on == False:
        shift_case()
    print("Shift is being pressed")
        
def shift_release(event):
    if case_shift_on==True:
        shift_case()
    print("Shift was released")

def shift_case():
    global case_shift_on
    if case_shift_on:
        case_shift_on = False
        case_shift['background']="SystemButtonFace"
    else:
        case_shift_on = True
        case_shift['background']="Dark Grey"

def shift_type():
    global log_shift_on
    if log_shift_on:
        log_shift_on = False
        log_shift['background']="SystemButtonFace"
    else:
        log_shift_on = True
        log_shift['background']="Dark Grey"

def back_space():
    entry_box.config(state = NORMAL)
    if is_selected():
        entry_box.delete(SEL_FIRST, SEL_LAST)
    else:
        entry_box.delete(entry_box.index('insert - 1 chars'), entry_box.index('insert'))
    entry_box.config(state = DISABLED)

shift_key_pressed = False
log_shift_on = False
case_shift_on = False

window = Tk()
window.title("Logic Keyboard Layout")
window.configure(background="grey")

window.grid_rowconfigure(0, weight=3)
window.grid_columnconfigure(0, weight=3)

### Frames ################
entry_frame = Frame(window, background="grey", bd=1, relief="sunken")
buttons_frame = Frame(window, background="darkgray", bd=1, relief="sunken")

entry_frame.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
buttons_frame.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)

entry_box = Text(entry_frame, width=77, height = 25, background="white", font="Terminal 15")
entry_box.grid(row=3, padx=0, columnspan=1, rowspan=25, sticky='nsew')
entry_box.insert(END,"Tip: Toggle Type-Shift with Ctrl + Shift")

entry_box.focus_set()

### Keys #####################
qwerty = [
'1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '+', '´','', 
'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'Å', '¨', "'", 
'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ö', 'Ä', '','',
'','Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '-']

logops = [
'!', '(', ')', '[', ']', '{', '}', '⊢',  '<', '>', '≤', '≥','',""
'→', '↔', '¬', '⊤', '∃', '∪', '⊂', '⊃', '∈', '∋', '∅', '~', '⋆', 
'∧', '∨', '⊻', '⊥', '∀', '∩', '⊆', '⊇', '∉', '∌','','','', 
'','⇒','⇔', '⇏', '⇎', '∴', '∵','⊕', '⊙',';',':','_',]

nordic_keys = {
    'plus': "+", 
    'aring': "å", 
    'quoteright': "'", 
    'odiaeresis': "ö", 
    'adiaeresis': "ä", 
    'comma': ",", 
    'period': ".", 
    'minus': "-", 
    }

### Char-Buttons #####################

charbuttons = {}

for pos, char in enumerate(qwerty):
    logop = logops[pos]
    _row, _column = pos//13, pos - pos//13*13 
    
    if char!='':
        charbuttons[char] = Button(buttons_frame, text=f"{char}\n{logop}", width=5, font="Terminal 15", command = lambda char = char, logop = logop: click1(char, logop))
        charbuttons[char].grid(row=_row, column = _column)

        if char.isalpha() and char not in "ÖÄÅöäå" or char.isnumeric():
            window.bind(f'{char}', charbuttons[char]['command'])
            window.bind(f'{char.lower()}', charbuttons[char]['command'])

for keysym in nordic_keys:
    window.bind(f'<{keysym}>', charbuttons[nordic_keys[keysym].upper()]['command'])

linebreak   =   Button(buttons_frame, text="line-\nbreak", width=5, font="Terminal 15", command = lambda : click1("\n", "\n"))
backspace   =   Button(buttons_frame, text="back-\nspace", width=5, font="Terminal 15", command = back_space)
case_shift  =   Button(buttons_frame, text="case-\nshift", width=5, font="Terminal 15", command = shift_case)
log_shift   =   Button(buttons_frame, text="type-\nshift", width=5, font="Terminal 15", command = shift_type)
space       =   Button(buttons_frame, text="space\n", width=5, font="Terminal 15", command = lambda : click1(" ", " "))
copy_btn    =   Button(buttons_frame, text="copy\n", width=5, font="Terminal 15", command = copy_text)
paste_btn   =   Button(buttons_frame, text="paste\n", width=5, font="Terminal 15", command = lambda : click1(window.clipboard_get(), window.clipboard_get()))

backspace.grid(row=0, column=12)
linebreak.grid(row=2, column = 11, columnspan=2, sticky='nsew')
case_shift.grid(row=3,)
log_shift.grid(row=4,)
space.grid(row=4, column = 3, columnspan=6, sticky='nsew')
copy_btn.grid(row=4, column = 12)
paste_btn.grid(row=4, column = 11)

### Binds #####################

window.bind('<BackSpace>', backspace['command'])
window.bind('<Return>', linebreak['command'])
window.bind('<space>', space['command'])
window.bind('<Control-Shift_L>', log_shift['command'])
window.bind('<Control-c>', copy_text)
window.bind('<Control-v>', paste_btn['command'])
window.bind("<Multi_key>", multi_key_press)

window.bind('<Shift_L>', shift_key_press)
window.bind('<KeyRelease-Shift_L>', shift_release)

window.mainloop()
