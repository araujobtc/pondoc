from main import main
from tkinter import *
from tkinter import ttk

root = Tk()
root.title('PONDOC')
root.geometry('+400+200')
root.resizable(False, False)

window = ttk.Frame(root, padding=10)
window.grid()

column1 = ttk.Frame(window, padding=10)
column1.grid(column=0, row=0)


period = ttk.Label(column1, text='Periódicos').grid()
text1 = ttk.Label(column1, text='url:').grid(column=0, row=1)
urlp = StringVar()
textboxp = ttk.Entry(column1, textvariable=urlp, width=70).grid(column=1, row=1)

confer = ttk.Label(column1, text='Conferências').grid()
text2 = ttk.Label(column1, text='url:').grid(column=0, row=3)
urlc = StringVar()
textboxc= ttk.Entry(column1, textvariable=urlc, width=70).grid(column=1, row=3)

column2 = ttk.Frame(window, padding=10)
column2.grid(column=1, row=0)

advance = ttk.Button(column2, text='Avançar', command=lambda: main(urlp.get(), urlc.get()))
advance.grid()
cancel = ttk.Button(column2, text='Cancelar', command=root.destroy).grid()

root.mainloop()
