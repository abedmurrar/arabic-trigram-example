from tkinter import *
import re
from nltk.util import ngrams
from glob import glob
import os


class AutocompleteEntry(Entry):
    def __init__(self, lista, *args, **kwargs):
        Entry.__init__(self, *args, **kwargs)
        self.lista = lista
        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = StringVar()

        self.var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)

        self.lb_up = False

    def changed(self, name, index, mode):
        if self.var.get() == '':
            self.lb.destroy()
            self.lb_up = False
        else:
            words = self.comparison()
            if words:
                if not self.lb_up:
                    self.lb = Listbox()
                    self.lb.bind("<Double-Button-1>", self.selection)
                    self.lb.bind("<Right>", self.selection)
                    self.lb.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
                    self.lb_up = True

                self.lb.delete(0, END)
                for w in words:
                    self.lb.insert(END, w)
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False

    def selection(self, event):

        if self.lb_up:
            self.var.set(self.var.get() + ' ' + self.lb.get(ACTIVE))
            self.lb.destroy()
            self.lb_up = False
            self.icursor(END)
            self.changed(None, None, None)

    def up(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':
                self.lb.selection_clear(first=index)
                index = str(int(index) - 1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def down(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != END:
                self.lb.selection_clear(first=index)
                index = str(int(index) + 1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def comparison(self):
        last_word = self.var.get().split(" ")[-1]
        words = []
        for arr in self.lista:
            for gram in arr:
                if last_word in gram and gram.index(last_word) < 2:
                    words.append(gram[gram.index(last_word) + 1])
        return list(dict.fromkeys(words))
        # return [w for w in self.lista if re.match(pattern, w)]


if __name__ == '__main__':
    trigrams = []
    GRAMS = 3
    aleph_to_yaa_regex = '[\u0621-\u064A]'
    arabic_letters_sequence = aleph_to_yaa_regex + '+'

    files = glob(os.path.join(os.getcwd(), 'data', '*.txt'))
    for file in files:
        cur_file = open(file)
        arabic_words_tokens = re.findall(arabic_letters_sequence, cur_file.read())
        trigrams.append(list(ngrams(arabic_words_tokens, GRAMS)))

    root = Tk()

    entry = AutocompleteEntry(trigrams, root)
    entry.grid(row=0, column=0)
    Button(text='nothing').grid(row=1, column=0)
    Button(text='nothing').grid(row=2, column=0)
    Button(text='nothing').grid(row=3, column=0)

    root.mainloop()
