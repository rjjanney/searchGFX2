import Tkinter, Tkconstants, tkFileDialog

class TkFileDialogExample(Tkinter.Frame):

    def __init__(self, root):

        Tkinter.Frame.__init__(self, root)
        button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}
        Tkinter.Button(self, text='asksaveasfilename', command=self.asksaveasfilename).pack(**button_opt)

        self.file_opt = options = {}
        options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
        options['initialfile'] = 'myfile.txt'
        options['parent'] = root

    def asksaveasfilename(self):
        filename = tkFileDialog.asksaveasfilename(**self.file_opt)

        if filename:
            return open(filename, 'w')

if __name__=='__main__':
    root = Tkinter.Tk()
    TkFileDialogExample(root).pack()
    root.mainloop()