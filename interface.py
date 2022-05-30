from main import main
from tkinter import *
from tkinter import ttk

def interface():
    root = Tk()
    root.title('PONDOC')
    root.geometry('+150+100')
    root.resizable(False, False)

    window = ttk.Frame(root, padding=10)
    window.grid()
    # column 1
    column1 = ttk.Frame(window, padding=10)
    column1.grid(column=0, row=0)

    t1 = ttk.Label(column1, text='Ano:').grid(column=0, row=0)

    ano = StringVar()
    ano.set(2021)   #default
    anoMenu = OptionMenu(column1, ano, *range(2017, 2022))
    anoMenu.grid(column=1, row=0)

    # column 2
    column2 = ttk.Frame(window, padding=10)
    column2.grid(column=1, row=0)

    advance = ttk.Button(column2, text='Avançar', command=lambda: [main(ano.get()), window.destroy()])
    advance.grid()
    cancel = ttk.Button(column2, text='Cancelar', command=root.destroy).grid()

    root.mainloop()


interface()