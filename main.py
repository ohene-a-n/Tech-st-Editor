import tkinter as tk
from tkinter import filedialog
import re
import os

class TextEditor:
    
        
    def __init__(self):
        
        # Declaring Window Class
        class Window:
            
            def __init__(self, title: str, dimensions: str):
        
                self.window = tk.Tk()
                self.window.title(title)
                self.window.geometry(dimensions)
       
        # Delcaring ToolBar Class
        class Toolbar:
            
            def __init__(self, master, texteditor):
                
                
                self.texteditor = texteditor
                self.body = tk.Frame(master)
                self.body.pack(side=tk.TOP, fill=tk.X)
        
                # Drop Menu for toolbar
                # File Menu
                self.file_options = ["File", "New", "Open", "Save", "Exit"]
                self.selected_file_option = tk.StringVar()
                self.selected_file_option.set(self.file_options[0])
        
                self.file_menu = tk.OptionMenu(self.body, self.selected_file_option, *self.file_options[1:], command=self.file_menu_select)
                self.file_menu.pack(side=tk.LEFT)
                
                #Edit Menu
                self.edit_options = ["Edit", "Cut", "Copy", "Paste", "Undo"]
                self.selected_edit_option = tk.StringVar()
                self.selected_edit_option.set(self.edit_options[0])
        
                self.edit_menu = tk.OptionMenu(self.body, self.selected_edit_option, *self.edit_options[1:], command=self.edit_menu_select)
                self.edit_menu.pack(side=tk.LEFT)

                # Tools Menu
                self.tools_options = ["Tools", "Search", "Find & Replace"]
                self.selected_tools_option = tk.StringVar()
                self.selected_tools_option.set(self.tools_options[0])
                
                self.tools_menu = tk.OptionMenu(self.body, self.selected_tools_option, *self.tools_options[1:], command=self.tools_menu_select)
                self.tools_menu.pack(side=tk.LEFT)
                
            def file_menu_select(self, event):
                
                command = self.selected_file_option.get()
                self.selected_file_option.set(self.file_options[0])
                self.texteditor.decider(command)
                
                
            def edit_menu_select(self, event):
                
                command = self.selected_edit_option.get()
                self.selected_edit_option.set(self.edit_options[0])
                self.texteditor.decider(command)
                
            def tools_menu_select(self, event):
               
                command = self.selected_tools_option.get()
                self.selected_tools_option.set(self.tools_options[0])
                self.texteditor.decider(command)
        
        # Declaring Textbox Class
        class Textbox:
            
            def __init__(self, master):
                
                self.textbox = tk.Text(master, undo=True)
                self.textbox.pack(expand=True, fill='both')
        
        # Declaring bottom InfoBar Class
        class InfoBar:
            
            def __init__(self, master, info, height: int, bg: str):
                
                self.infolabel = tk.Label(master, textvariable=info, height=height, bg=bg)
                self.infolabel.pack(side=tk.BOTTOM, fill=tk.X)
                
        class SearchWidget:
            
            def __init__(self, master, texteditor):
                
                self.master = master
                self.texteditor = texteditor
                self.entry = tk.Entry(master)
                
                self.search_button = tk.Button(master, text='Search', command=self.search)
                self.toggle_button = tk.Button(master, text='Toggle', command=self.toggle)
            
            def search(self):
                
                search_value = self.entry.get()
                self.texteditor.search(search_value)
            
            def toggle(self):
                
                if self.entry.winfo_manager():
                    self.entry.pack_forget()
                    self.search_button.pack_forget()
                    self.toggle_button.pack_forget()
                    self.master.tag_remove('found', '1.0', tk.END)
        
        class FindReplaceWidget:
            
            def __init__(self, master, texteditor):
            
                self.master = master
                self.texteditor = texteditor
                
                self.find_entry = tk.Entry(master)
                
                self.find_button = tk.Button(master, text='Find', command=self.find)
                
                self.replace_entry = tk.Entry(master)
                
                self.replace_button = tk.Button(master, text='Replace', command=self.replace)
                
                self.toggle_button = tk.Button(master, text='Toggle', command=self.toggle)
            
            def find(self):
                
                search_value = self.find_entry.get()
                self.texteditor.search(search_value)
            
            def replace(self):
                
                search_value = self.find_entry.get()
                replace_value = self.replace_entry.get()
                self.texteditor.search(search_value, replace=True, replace_value=replace_value)
                
            def toggle(self):
                
                if self.find_entry.winfo_manager():
                    self.find_entry.pack_forget()
                    self.find_button.pack_forget()
                    self.replace_entry.pack_forget()
                    self.replace_button.pack_forget()
                    self.toggle_button.pack_forget()
                    self.master.tag_remove('found', '1.0', tk.END)
                
                                    
        # File name
        self.filename = None
        
        # Initializing Window
        self.Twindow = Window("Tech-st Editor", "900x400")
        self.Twindow.window.bind('<KeyRelease>', lambda event: self.update_info())
        
        # Inializing Toolbar
        self.Ttoolbar = Toolbar(self.Twindow.window, self)
        
        # Initializing Textbox and binding methods to key-handling
        self.Ttextbox = Textbox(self.Twindow.window)
        self.Ttextbox.textbox.bind('<Control-z>', self.undo_change)
        
        # Information for Information Bar at the bottom
        self.info = tk.StringVar()
        self.info.set('Lines: 0 Words: 0 Characters: 0')
        
        # Initializing InfoBar 
        self.Tinfobar = InfoBar(self.Twindow.window, self.info, 1, 'lightgrey')

        
        #Initializing Search Widget
        self.SearchWidget = SearchWidget(self.Ttextbox.textbox, self)

        #Initializing Find and Replace Widget
        self.FindReplaceWidget = FindReplaceWidget(self.Ttextbox.textbox, self)

        # Blast Off!!
        self.Twindow.window.mainloop()
    
    def copy_highlighted_text(self):
        
        try:
            highlighted_text = self.Ttextbox.textbox.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.Twindow.window.clipboard_clear()
            self.Twindow.window.clipboard_append(highlighted_text)
        except Exception:
            pass
            
    def cut_highlighted_text(self):
        
        try:
            highlighted_text = self.Ttextbox.textbox.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.Twindow.window.clipboard_clear()
            self.Twindow.window.clipboard_append(highlighted_text)
            self.Ttextbox.textbox.delete(tk.SEL_FIRST, tk.SEL_LAST)
        except Exception:
            pass
    
    def paste_text(self):
        
        index_of_cursor = self.Ttextbox.textbox.index(tk.INSERT)
        self.Ttextbox.textbox.insert(index_of_cursor, self.Twindow.window.clipboard_get())
    
    def undo_change(self, event=None):
        
        try:
            self.Ttextbox.textbox.edit_undo()
        except Exception:
            pass
            
    def open_file(self):
    
        home_directory = os.path.expanduser('~')    
    
        file_path = filedialog.askopenfilename(initialdir=home_directory,
                                               title='Open File',
                                               filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')],
                                               defaultextension='.txt')
        
        if file_path:
        
            self.filename = os.path.basename(file_path)
            self.update_window_title()
        
            with open(file_path, 'r') as file:
                
                content = file.read()
                self.Ttextbox.textbox.delete(1.0, tk.END)
                self.Ttextbox.textbox.insert(1.0, content)
    
    def save_file(self):
        
        home_directory = os.path.expanduser('~')
        
        file_path = filedialog.asksaveasfilename(initialdir=home_directory,
                                                 title='Save File',
                                                 filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')],
                                                 defaultextension='.txt')
        
        if file_path:
            
            self.filename = os.path.basename(file_path)
            self.update_window_title()
            
            with open(file_path, 'w') as file:
                
                file.write(self.Ttextbox.textbox.get(1.0, tk.END))
        
    def update_info(self):
        
        content = self.Ttextbox.textbox.get(1.0, tk.END)
        characters = len(content) - 1
        lines = content.count('\n') if characters else 0
        words = len(re.findall(r'\b\w+\b', content))
        
        self.info.set(f'Lines: {lines} Words: {words} Characters: {characters}')
    
    def exit_program(self): 
        
      self.Twindow.window.quit()
      self.Twindow.window.destroy()
    
    def show_search_widgets(self):
        
        self.SearchWidget.entry.pack()
        self.SearchWidget.search_button.pack()
        self.SearchWidget.toggle_button.pack()
        
    def show_findandreplace_widget(self):
        
        self.FindReplaceWidget.find_entry.pack()
        self.FindReplaceWidget.find_button.pack()
        self.FindReplaceWidget.replace_entry.pack()
        self.FindReplaceWidget.replace_button.pack()
        self.FindReplaceWidget.toggle_button.pack()
        
    
    def update_window_title(self):
        
        if self.filename:
            
            self.Twindow.window.title(f'{self.filename} - Tech-st Editor')
            
        else:
            
            self.Twindow.window.title('Untitled - Tech-st Editor')
    
    def search(self, search_value, replace=False, replace_value=None):
         
        if search_value:
            
            self.Ttextbox.textbox.tag_remove('found', '1.0', tk.END)
            
            index = '1.0' 
            
            while True:
            
                    index = self.Ttextbox.textbox.search(search_value, index, tk.END, nocase=True)
                    
                    if not index:
                        
                        break
                    
                    end = f'{index}+{len(search_value)}c'
                    
                    if replace and replace_value:
                        
                        self.Ttextbox.textbox.delete(index, end)
                        self.Ttextbox.textbox.insert(index, replace_value)
                        end = f'{index}+{len(replace_value)}c'      
              
                    self.Ttextbox.textbox.tag_add('found', index, end)
                    
                    index = end
        
            self.Ttextbox.textbox.tag_config('found', background='lightgreen')
        
        
    def new_file(self):
        
        self.filename = None
        self.update_window_title()
        
        self.Ttextbox.textbox.delete(1.0, tk.END)
    
    # Routes various commands to the right function
    def decider(self, command: str):
        
        if command == 'Copy':
            self.copy_highlighted_text()
        elif command == 'Cut':
            self.cut_highlighted_text()
        elif command == 'Paste':
            self.paste_text()
        elif command == 'Undo':
            self.undo_change()
        elif command == 'Open':
            self.open_file()
        elif command == 'Save':
            self.save_file()
        elif command == 'Exit':
            self.exit_program()
        elif command == "Search":
            self.show_search_widgets()    
        elif command == 'Find & Replace':
            self.show_findandreplace_widget()
        if command == 'New':
            self.new_file()

if __name__ == "__main__":
    
    mytexteditor = TextEditor()