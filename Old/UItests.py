from tkinter import *
from tkinter import ttk


class TestWindow:
    def __init__(self):
        self.root = Tk()  # start tkinter
        self.root.title = 'Testing UI components'
        self.root_frame = ttk.Frame(self.root)

        #styles
        style = ttk.Style()
        style.configure('Border.TButton', foreground='red',border=4,padding=2)
        style.configure('Border.TFrame', background='black', padding=4, border=4)
        style.configure('Border2.TFrame', background='black', padding=10)

        # notebook example
        self.notebook = ttk.Notebook(self.root_frame)
        self.tab_1 = ttk.Frame(self.notebook)
        self.tab_1['style'] = 'Border.TFrame'
        self.tab_1['padding'] = (1,1,1,1)
        self.tab_2 = ttk.Frame(self.notebook)
        self.tab_2['style'] = 'Border2.TFrame'
        button = ttk.Button(self.tab_1, text='button', command=self.make_window)
        button['style'] = 'Border.TButton'
        self.notebook.add(self.tab_1, text='tab1')
        self.notebook.add(self.tab_2, text='tab2')
        button.grid()
        self.notebook.grid()

        # menubar example
        menu_bar = Menu(self.root)
        menu_file = Menu(menu_bar)
        menu_edit = Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='Open', command = self.no_command)
        menu_bar.add_cascade(menu=menu_edit, label='Edit')
        # a cascading submenu
        menu_edit_list = Menu(menu_edit)
        menu_edit.add_cascade(menu=menu_edit_list, label='Edit sub menu')
        # add a checkbutton
        check = BooleanVar()
        menu_edit_list.add_checkbutton(label='Check', variable=check, onvalue=True, offvalue=False)
        # add a radio button
        radio = StringVar()
        menu_file.add_radiobutton(label='Opt1', variable=radio, value='Option 1')
        menu_file.add_radiobutton(label='Opt2', variable=radio, value='Option 2')
        # this activates the menu
        self.root['menu'] = menu_bar

        self.root_frame.grid()
        self.root.mainloop()


    def no_command(self):
        print('nothing')

    def make_window(self):
        print('window make')
        new_window = Tk()


TestWindow()
