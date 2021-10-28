import json
import tkinter as tk
from tkinter import ttk


class TodoModel:
    def __init__(self, data_file):
        self._data_file = data_file
        self._img = tk.PhotoImage(file="tick.png")

    def load(self, tree):
        try:
            with open(self._data_file, 'r') as f:
                todos = json.load(f)
            row_count = len(todos)
            index = 0
            while index <= row_count - 1:
                status, text = todos[index]
                if status:
                    tree.insert('', 'end', text=text, image=self._img)
                else:
                    tree.insert('', 'end', text=text)
                index += 1
        except Exception:
            pass

    def complete(self, tree):
        self.check_mark(tree, self._img)

    def incomplete(self, tree):
        self.check_mark(tree, '')

    def check_mark(self, tree, image_value):
        curItem = tree.focus()
        if curItem != '':
            to_do_text = tree.item(curItem, 'text')
            tree.item(curItem, text=to_do_text, image=image_value)
            self.unselect_item(tree, curItem, to_do_text)
            self.save(tree)

    def add_new_todo(self, entry, tree):
        new_todo = entry.get()
        if new_todo != '':
            tree.insert('', 'end', text=new_todo)
            entry.delete(0, 'end')
            self.save(tree)

    def save(self, tree):
        todos = []
        for each in tree.get_children():
            to_do_text = tree.item(each, 'text')
            if tree.item(each)['image'] == '':
                todos.append((False, to_do_text))
            else:
                todos.append((True, to_do_text))
        with open(self._data_file, 'w') as f:
            json.dump(todos, f)

    def delete_todo(self, tree):
        curItem = tree.focus()
        if curItem != '':
            tree.delete(curItem)
            self.save(tree)

    def unselect_item(self, tree, current_item, new_todo):
        todo_index = tree.index(current_item)
        if tree.item(current_item)['image'] == '':
            tree.insert('', todo_index, text=new_todo)
        else:
            tree.insert('', todo_index, text=new_todo, image=self._img)
        tree.delete(current_item)


class MainWindowView:
    def __init__(self, window):
        self.window = window
        self.window.geometry('236x405+300+300')
        self.window.title('To do')
        self._frame = tk.Frame(master=self.window, width=100, height=175, background='light grey')
        self.todos = ttk.Treeview(master=self._frame, show="tree", selectmode='none', height=7)
        self.todos.place(x=13, y=13)
        self._scrollbar = ttk.Scrollbar(self._frame, orient="vertical", command=self.todos.yview)
        self._scrollbar.place(x=217, y=13, height=143)
        self.todos.configure(yscrollcommand=self._scrollbar.set)
        self._frame.pack(fill='both')
        self.delete = tk.Button(master=self.window, text="Delete", width=10, background='light grey')
        self.delete.place(x=13, y=208)
        self.complete = tk.Button(master=self.window, text="Complete", width=10, background='light grey')
        self.complete.place(x=120, y=208)
        self.entry_box = tk.Entry(master=self.window, width=30)
        self.entry_box.place(x=13, y=257)
        self.add_todo = tk.Button(master=self.window, text="Add To do", width=25, background='light grey')
        self.add_todo.place(x=13, y=300)
        self.uncheck_todo = tk.Button(master=self.window, text="Uncheck To do", width=25, background='light grey')
        self.uncheck_todo.place(x=13, y=350)


class Controller:
    def __init__(self, window, data_file):
        self.window = window
        self.model = TodoModel(data_file)
        self.view = MainWindowView(window)
        self.model.load(self.view.todos)
        self.view.complete.bind("<Button-1>", self.complete_button)
        self.view.uncheck_todo.bind("<Button-1>", self.incomplete_button)
        self.view.delete.bind("<Button-1>", self.delete_button)
        self.view.add_todo.bind("<Button-1>", self.add_button)

    def complete_button(self, event):
        self.model.complete(self.view.todos)

    def incomplete_button(self, event):
        self.model.incomplete(self.view.todos)

    def delete_button(self, event):
        self.model.delete_todo(self.view.todos)

    def add_button(self, event):
        self.model.add_new_todo(self.view.entry_box, self.view.todos)


root = tk.Tk()
controller = Controller(root, 'data.db')
root.mainloop()
