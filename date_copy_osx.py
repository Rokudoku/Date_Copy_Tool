#!/usr/bin/env python3
"""
=== Date Copy Tool ===
A tool that copies a specified date to clipboard so that it can be pasted. 

By pressing the 'Today' button or using its hotkey, the current date is 
copied to  clipboard so it may be pasted. This is a similar case with the 
'Yesterday' and 'Tomorrow' buttons.

The format is: <date number> <abbreviated month> <4 digit year>
        e.g. 23 Dec 2016

===========================
By Jerome Probst 
December 2016/January 2017
===========================
"""

import tkinter as tk
from tkinter import ttk
import sys, subprocess


class MainApp(tk.Frame):
    """
    The parent window.
    Interacts with other sections as classes to make things cleaner and 
    easier to manage if doing more than just the date buttons.
    """

    def __init__(self, parent):
        """
        Sets up self as the mainframe under root and manages all the
        subframes and menu.
        """

        ttk.Frame.__init__(self, parent)
        self.parent = parent

        self.dates = Dates(self)
        self.dates.pack()

        self.menubar = Menubar(self)

        self.grid(row=0, column=0, sticky="nsew")

class Dates(tk.Frame):
    """ 
    "Yesterday", "Today" and "Tomorrow" buttons assigned to (1, 2, 3) 
    that copy their respective dates to the clipboard.
    """
    
    def __init__(self, parent):
        """Sets up self as the frame 'Dates'"""

        ttk.Frame.__init__(self, parent)
        self.parent = parent

        self.create_buttons()
        self.set_keybinds()

    def create_buttons(self):
        """Creates the "Yesterday", "Today" and "Tomorrow" buttons"""

        self.s = ttk.Style()

        self.s.configure("date.TButton", padding=35, width=14)

        self.yesterday_btn = ttk.Button(self, text="Yesterday (1)", 
                        style="date.TButton", 
                        command=lambda: self.copy_date(1))

        self.today_btn = ttk.Button(self, text="Today (2)",
                        style="date.TButton", 
                        command=lambda: self.copy_date(2))

        self.tomorrow_btn = ttk.Button(self, text="Tomorrow (3)",
                        style="date.TButton", 
                        command=lambda: self.copy_date(3))

        self.yesterday_btn.pack()
        self.today_btn.pack()
        self.tomorrow_btn.pack()

    def set_keybinds(self):
        """
        Sets up the buttons to correspond to 1,2,3. Gets passed the button
        number so copy_date knows what to do.
        """
        # Note: seems keybinds must be done at root (self.parent.parent)"""
        self.parent.parent.bind("1", lambda x: self.copy_date(1))
        self.parent.parent.bind("2", lambda x: self.copy_date(2))
        self.parent.parent.bind("3", lambda x: self.copy_date(3))

    def copy_date(self, option):
        """
        Clears clipboard and depending on option, gives the correct date.
        Uses the inbuilt date program/command.
        Also sets focus on the associated button so user knows what they
        pressed.
        """
        self.parent.clipboard_clear()

        if option == 1:
            self.yesterday_btn.focus()
            cmd = 'date -v-1d +"%d %b %Y"'
        elif option == 2:
            self.today_btn.focus()
            cmd = 'date +"%d %b %Y"'
        elif option == 3:
            self.tomorrow_btn.focus()
            cmd = 'date -v+1d +"%d %b %Y"'
        else:
            sys.stderr.write('copy_date was called with an invalid arg')
            sys.exit(1)
        
        self.output = subprocess.check_output(cmd, shell=True)
        #check_output returns a byte string e.g. b'dd mm yyyy\n'
        #decoded to get rid of the b and quotes and ignored newline
        self.output = self.output.decode("utf-8")[:-1]

        if self.parent.menubar.trailing_check.get():
            self.output += ' '

        if self.parent.menubar.leading_check.get():
            self.output = ' ' + self.output

        self.parent.clipboard_append(self.output)

class Menubar(tk.Toplevel):
    """
    The menubar. 
    Actually a Toplevel window, much like the other classes are Frames.
    """

    def __init__(self, parent):
        """
        Uses the init method of Toplevel to make self a Toplevel window.
        Its parent is the mainframe so it can easily communicate with the
        mainframe attributes and change things such as button size.
        """

        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.menubar = tk.Menu(self)

        #intentionally leaving out below (see method comments for details)
        #self.apple_menu()
        
        self['menu'] = self.menubar

        #removes dotted line tearoff option on win32 and x11
        self.parent.parent.option_add('*tearOff', tk.FALSE)

        self.file_menu()
        self.options_menu()
        self.help_menu()

        #this is to remove a second window that shows up
        #it's possible I did something wrong with the setup of the menubar
        #but this removes it pretty easily with seemingly no drawback
        self.withdraw()

    def apple_menu(self):
        """
        OS X specific menu to avoid the default Python menu showing 
        'About Python'. The Python menu (the application binary) CAN be 
        changed by renaming or making a copy of the binary used to run
        the script.
        For now I'm just going to leave this entire apple menu out because
        I think it's fine and I'm not sure how this would work when
        converted to a standalone executable. The main intention is a 
        Windows exe anyway.
        """
        self.appmenu = tk.Menu(self.menubar, name='apple')
        self.menubar.add_cascade(menu=appmenu)
        self.appmenu.add_command(label='About Copy Date Tool')
        self.appmenu.add_separator()

    def file_menu(self):
        """
        The 'File' menubar.
        Contains 'About' and 'Quit' with a seperator in between.
        """

        self.filemenu = tk.Menu(self.menubar)
        self.menubar.add_cascade(menu=self.filemenu, label='File')

        self.filemenu.add_command(label='About')
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Quit', command=self.close_window)

    def close_window(self):
        """Basically root.destroy() to close the program."""
        self.parent.parent.destroy()

    def options_menu(self):
        """
        The 'Options' menubar.
        Contains the 'Size' submenu which determines size of the buttons.
        """

        self.optionsmenu = tk.Menu(self.menubar)
        self.menubar.add_cascade(menu=self.optionsmenu, label='Options')

        self.size = self.size_submenu()
        self.spacing = self.spacing_submenu()

    def size_submenu(self):
        """
        Submenu inside 'Options'. Contains 'Small', 'Medium' and 'Large'.
        These options change the size of the buttons.
        The default is 'Medium'
        """

        self.sizemenu = tk.Menu(self.optionsmenu)
        self.optionsmenu.add_cascade(menu=self.sizemenu, label='Size')

        self.button_size = tk.StringVar()
        self.sizemenu.add_radiobutton(label='Small', 
                                command=lambda:self.change_button_size(10),
                                variable=self.button_size, value='Small')
        self.sizemenu.add_radiobutton(label='Medium', 
                                command=lambda:self.change_button_size(30),
                                variable=self.button_size, value='Medium')
        self.sizemenu.add_radiobutton(label='Large', 
                                command=lambda:self.change_button_size(50),
                                variable=self.button_size, value='Large')
        self.button_size.set('Medium')

    def change_button_size(self, size):
        """
        Changes the button size by accessing the dates created in mainframe
        """
        self.parent.dates.yesterday_btn.configure(padding=size)
        self.parent.dates.today_btn.configure(padding=size)
        self.parent.dates.tomorrow_btn.configure(padding=size)

    def spacing_submenu(self):
        """
        Submenu inside 'Options'. Allows for trailing or leading space in
        the date that is copied to clipboard. They are either on or off.
        Default is both off.
        """

        self.spacingmenu = tk.Menu(self.optionsmenu)
        self.optionsmenu.add_cascade(menu=self.spacingmenu, label='Spacing')

        self.leading_check = tk.BooleanVar()
        self.spacingmenu.add_checkbutton(label='Leading Space', 
                                    variable=self.leading_check,
                                    onvalue=True, offvalue=False)

        self.trailing_check = tk.BooleanVar()
        self.spacingmenu.add_checkbutton(label='Trailing Space',
                                    variable=self.trailing_check,
                                    onvalue=True, offvalue=False)

        ### These Bool values are used when creating the actual output.
        ### (Dates.copy_date)

    def help_menu(self):
        """
        The 'Help' menubar. Contains 'Instructions'.
        """
        self.helpmenu = tk.Menu(self.menubar)
        self.menubar.add_cascade(menu=self.helpmenu, label='Help')

        self.helpmenu.add_command(label='Instructions')

root = tk.Tk()

root.title("Date Copy Tool")

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

app = MainApp(root)

root.mainloop()