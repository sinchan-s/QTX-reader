from tkinter import filedialog
from tkinter import *

win = Tk()
filename = filedialog.asksaveasfilename(initialdir='/',
                                        title='Save File',
                                        filetypes=(('Text Files', 'txt.*'),
                                                   ('All Files', '*.*')))
textContent = "I'm the text in the file"
myfile = open(filename, "w+")
myfile.write(textContent)
# to test
print("File saved as ", filename)

win.mainloop()