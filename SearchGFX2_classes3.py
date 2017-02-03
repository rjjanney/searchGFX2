#!/usr/bin/env python

'''
Program to search a text file of directory listings.
Python version = 2.7
*** based on tt070.py from thinking in python ***
'''


import re
import Tkinter as tkt
import tkFileDialog
import subprocess
import ConfigParser

# CONSTANTS --------------------------------------------------------

config = ConfigParser.ConfigParser()
config.readfp(open('config.cfg'))

# The location of the text file to search
# FILE_LOCATION = "/Users/206098175/Projects/lists/_FileList.txt"
FILE_LOCATION = config.get('SOURCES', 'FILE_LOCATION')
ROOT = config.get('SOURCES', 'ROOT')

# Class and function definitions -----------------------------------

# This converts the search strings to regex patterns


def convert_patterns(patterns):
    results = []
    results.append(re.compile(patterns[0] +
                              ".*(" + myapp.endings +
                              ")$", re.IGNORECASE))

    if patterns[1] != "":  # Second search field non-empty
        if myapp.and_or_state.get() == 1:  # if OR, just make
                                        # results[0] the OR regex pattern
            results = [(re.compile("(" + patterns[0] +
                                   "|" + patterns[1] + ").*(" +
                                   myapp.endings + ")$", re.IGNORECASE)), 0]
        else:
            results.append(re.compile(patterns[1], re.IGNORECASE))

    else:
        results.append(0)
    return results


# Finds and compiles the results of the regex search.
def apply_pattern_to_file(files_list, pattern):
    search_listed = []
    directory = None
    # for each file in files
    for line in files_list:

        # assign directory line and eliminate it from search
        if line.startswith("/"):
            directory = line.replace(":\n", "")
            continue
        # for each pattern
        if pattern.search(line):
            search_listed.append([directory, line[:-1]])
    # print search_listed
    return search_listed

# Finds and compiles the results of the regex search.


def apply_pattern_to_list(files_list, pattern):
    search_listed = []
    # for each file in files
    for line in files_list:

        if pattern.search(line[1]):
            search_listed.append(line)
    # print search_listed
    return search_listed


def make_list(search_results):
    local_output_list = []

    item = [0, 0, 0]
    for item in search_results:
        # for filename highlighting, holds last line index, eventually
        if item[0] is None:
            item[0] = ROOT
        if myapp.search_root not in item[0]:
            continue

        local_output_list.append(item[0] + "/" + item[1] + "\n")

    return local_output_list


def searcher_submit(search_term1, search_term2, operation):
    output_results = []

    if search_term1 != "":  # check to see if anything was entered
                            # in search box 1, if not, skip search

        # ENABLES EDITING IN RESULT WINDOW
        myapp.results_window.config(state=tkt.NORMAL)
        myapp.results_window.tag_config("file", foreground="blue")

        search_terms = [search_term1, search_term2]

        # make search_terms into regex patterns
        outer_patterns = convert_patterns(search_terms)

        with open(FILE_LOCATION, 'r') as file_list:
            search_output = apply_pattern_to_file(file_list, outer_patterns[0])
            output_list = search_output

        if outer_patterns[1]:
            # if operation == 1:  # if OR 1, search full file list with each
            # term, then merge the results using set() to eiminate dupes
            #     with open(FILE_LOCATION, 'r') as file_list:
            #         second_output_list = apply_pattern_to_file(file_list,
            # outer_patterns[1])
            #         output_results = or_this_list_list(output_list,
            # second_output_list)

            # else:
            search_output_second = apply_pattern_to_list(output_list,
                                                         outer_patterns[1])
            second_output_list = search_output_second

            if operation == 0:  # if AND, only include line_2nds that are
                                # in output_list
                for line_2nd in second_output_list:
                    if line_2nd in output_list:
                        output_results.append(line_2nd)

            elif operation == 2:    # if NOT 2, compare and eliminate from
                                    # 1 all that are the same as 2
                output_results = output_list
                for line_2nd in second_output_list:
                    if line_2nd in output_list:
                        output_results.remove(line_2nd)
        else:
            output_results = output_list

        output_final = make_list(output_results)
        send_to_window(output_final)

    myapp.line_index += len(output_final)
    myapp.filecount.config(text="Files Found: %d" % (myapp.line_index - 1),
                           fg="black")
    myapp.cleared = False

    # DISABLES EDITING IN RESULT WINDOW
    myapp.results_window.config(state=tkt.DISABLED)


def send_to_window(output):

    for ind_x, line in enumerate(output):
        myapp.results_window.insert(tkt.END, line)
        #  _____ crazy way of highlighting file names in results window
        filename_end = str(ind_x + myapp.line_index) + "." + str(len(line))
        filename_begin = str(ind_x + myapp.line_index) + "." +\
            str((int(filename_end.split(".")[-1]) - len(line.split("/")[-1])))
        myapp.results_window.tag_add("file", filename_begin, filename_end)

    myapp.results_window.see(tkt.END)

# def or_this_list_list(output_list, second_output_list): # OLD OR method
#     directories_list = []
#     files_list = []

#     for item in output_list:
#         directories_list.append("####".join(item))
#     for item2 in second_output_list:
#         directories_list.append("####".join(item2))
#     files_deduped_unsplit = list(set(directories_list))

#     for item3 in files_deduped_unsplit:
#         files_list.append(item3.split("####"))

#     return files_list


class MyApp:
    def __init__(self, parent):
        self.myParent = parent
        parent.bind('<Return>', self.return_funct)
        parent.title("Search GFX2")
        # POSSIBLE way of decorating the whole app:
        # parent.wm_attributes("-alpha", 0.8)

        # ______ INITIALIZE VARIABLES _________
        self.and_or_state = tkt.IntVar()
        self.anyState = tkt.IntVar()
        self.jpgState = tkt.IntVar()
        self.movState = tkt.IntVar()
        self.tgaState = tkt.IntVar()
        self.wavState = tkt.IntVar()
        self.docState = tkt.IntVar()
        self.c4dState = tkt.IntVar()
        self.psdState = tkt.IntVar()
        self.aeState = tkt.IntVar()
        self.search_root = tkt.StringVar()
        self.search_root = ROOT
        self.line_index = 1
        self.endings = tkt.StringVar()
        self.endings = ""
        self.endings_list = []
        self.sep = "|"

        # ________ THE WIDGETS __________________
        self.frame1 = tkt.Frame(parent)
        self.frame2 = tkt.Frame(parent)
        self.frame2a = tkt.Frame(parent)
        self.frame3 = tkt.Frame(parent)
        self.frame4 = tkt.Frame(parent, padx=10, pady=6)
        self.frame5 = tkt.Frame(parent, padx=10, pady=6)
        self.tl_frm = tkt.Frame(self.frame1)
        self.tr_frm = tkt.Frame(self.frame1)

        self.label = tkt.Label(self.tl_frm, text="Enter search term(s):")
        self.ent = tkt.Entry(self.tl_frm)
        self.ao_frm = tkt.Frame(self.tr_frm)
        self.and_button = tkt.Radiobutton(self.ao_frm,
                                          variable=self.and_or_state,
                                          value=0, text='AND')
        self.or_button = tkt.Radiobutton(self.ao_frm,
                                         variable=self.and_or_state,
                                         value=1, text='OR')
        self.not_button = tkt.Radiobutton(self.ao_frm,
                                          variable=self.and_or_state,
                                          value=2, text="NOT")
        self.ent2 = tkt.Entry(self.tr_frm)

        self.btn = tkt.Button(self.tr_frm, text="Search",
                              command=self.search_funct)

        # ________ 9 Filetype Buttons ____________

        self.filetype_frame = tkt.LabelFrame(self.frame2)
        self.anyButton = tkt.Checkbutton(self.filetype_frame,
                                         text="all", variable=self.anyState,
                                         command=self.anyButton_command,
                                         justify=tkt.LEFT, padx=5)
        self.anyButton.select()
        self.jpgButton = tkt.Checkbutton(self.filetype_frame,
                                         text=".jpg", variable=self.jpgState,
                                         command=self.jpgButton_command,
                                         justify=tkt.LEFT, padx=5)
        self.movButton = tkt.Checkbutton(self.filetype_frame,
                                         text=".mov", variable=self.movState,
                                         command=self.movButton_command,
                                         justify=tkt.LEFT, padx=5)
        self.tgaButton = tkt.Checkbutton(self.filetype_frame, text=".tga",
                                         variable=self.tgaState,
                                         command=self.tgaButton_command,
                                         justify=tkt.LEFT, padx=5)
        self.wavButton = tkt.Checkbutton(self.filetype_frame, text=".wav",
                                         variable=self.wavState,
                                         command=self.wavButton_command,
                                         justify=tkt.LEFT, padx=5)
        self.docButton = tkt.Checkbutton(self.filetype_frame, text=".doc",
                                         variable=self.docState,
                                         command=self.docButton_command,
                                         justify=tkt.LEFT, padx=5)
        self.c4dButton = tkt.Checkbutton(self.filetype_frame, text=".c4d",
                                         variable=self.c4dState,
                                         command=self.c4dButton_command,
                                         justify=tkt.LEFT, padx=5)
        self.psdButton = tkt.Checkbutton(self.filetype_frame, text=".psd",
                                         variable=self.psdState,
                                         command=self.psdButton_command,
                                         justify=tkt.LEFT, padx=5)
        self.aeButton = tkt.Checkbutton(self.filetype_frame, text=".ae",
                                        variable=self.aeState,
                                        command=self.aeButton_command,
                                        justify=tkt.LEFT, padx=5)

        self.dirBtn = tkt.Button(self.frame2a, text="Choose Directory",
                                 command=self.dirBtn_command)
        self.dirLbl = tkt.Label(self.frame2a, text="Searching in: " +
                                self.search_root)

        # __________ RESULTS Window ________________

        self.scrollbar = tkt.Scrollbar(self.frame4)
        self.results_window = tkt.Text(self.frame4, relief=tkt.GROOVE, bd=1,
                                       yscrollcommand=self.scrollbar.set)
        self.filecount = tkt.Label(self.frame5, text="Files Found: 0",
                                   fg="black")
        self.clear_button = tkt.Button(self.tr_frm, text="Clear Result Box",
                                       command=self.clear_button_command)

        # ___________ LAYOUT _________________

        self.frame5.pack(side=tkt.BOTTOM, fill=tkt.X)
        self.frame4.pack(side=tkt.BOTTOM, expand=tkt.YES, fill=tkt.BOTH)
        self.frame2a.pack(side=tkt.BOTTOM, expand=tkt.YES, fill=tkt.BOTH)
        self.frame1.pack(side=tkt.LEFT, padx=10)
        self.frame2.pack(side=tkt.LEFT, expand=tkt.YES, fill=tkt.BOTH)
        self.frame3.pack(side=tkt.LEFT, expand=tkt.YES, fill=tkt.BOTH)

        self.tl_frm.pack(side=tkt.LEFT)
        self.label.pack(side=tkt.LEFT)
        self.ent.pack(side=tkt.LEFT)
        self.tr_frm.pack(side=tkt.RIGHT)
        self.ao_frm.configure(padx=4)
        self.ao_frm.pack(side=tkt.LEFT)
        self.and_button.pack(side=tkt.LEFT)
        self.or_button.pack(side=tkt.LEFT)
        self.not_button.pack(side=tkt.RIGHT)
        self.ent2.pack(side=tkt.LEFT)

        self.filetype_frame.pack(side=tkt.LEFT, expand=tkt.YES, padx=10)
        self.anyButton.pack(side=tkt.LEFT)
        self.jpgButton.pack(side=tkt.LEFT)
        self.movButton.pack(side=tkt.LEFT)
        self.tgaButton.pack(side=tkt.LEFT)
        self.wavButton.pack(side=tkt.LEFT)
        self.docButton.pack(side=tkt.LEFT)
        self.c4dButton.pack(side=tkt.LEFT)
        self.psdButton.pack(side=tkt.LEFT)
        self.aeButton.pack(side=tkt.LEFT)
        self.dirLbl.pack(side=tkt.LEFT, fill=tkt.X, padx=10)
        self.dirBtn.pack(side=tkt.LEFT, expand=tkt.NO, padx=10)

        self.btn.pack(side=tkt.LEFT)

        self.scrollbar.pack(side=tkt.RIGHT, fill=tkt.Y)
        self.results_window.pack(side=tkt.TOP, expand=tkt.YES, fill=tkt.BOTH)
        self.results_window.bind('<Button-1>', self.select_line)

        self.filecount.pack(side=tkt.LEFT, fill=tkt.X)
        self.clear_button.pack(side=tkt.LEFT)
        self.scrollbar.config(command=self.results_window.yview)

        self.end_buttons = {"jpg": (self.jpgState, self.jpgButton, "jpg|jpeg"),
                            "mov": (self.movState, self.movButton, "mov|mxf"),
                            "tga": (self.tgaState, self.tgaButton, "tga"),
                            "wav": (self.wavState, self.wavButton,
                                    "wav|aif|aiff|mp3|ogg"),
                            "doc": (self.docState, self.docButton,
                                    "doc|docx|txt|rtf|pdf"),
                            "c4d": (self.c4dState, self.c4dButton,
                                    "c4d|obj|mb|mel"),
                            "psd": (self.psdState, self.psdButton, "psd"),
                            "ae":  (self.aeState,  self.aeButton,  "ae|aep")
                            }

    # _________ BINDINGS __________________________

    def return_funct(self, event=None):
        self.search_funct()

    def search_funct(self, event=None):
        # SEARCHING NOTIFICATION
        self.filecount.config(text="SEARCHING...", fg="red")
        self.filecount.update_idletasks()

        for val in self.end_buttons.viewvalues():
            if val[0].get():
                self.endings_list.append(val[2])
        self.endings = self.sep.join(self.endings_list)
        # for testing
        # print self.endings
        searcher_submit(self.ent.get(), self.ent2.get(),
                        self.and_or_state.get())
        self.endings_list = []

    def select_line(self, event):
        # get index of text under mouse position in text widget
        index = self.results_window.index("@%s,%s" % (event.x, event.y))
        # select that whole line and assign it to file_loc
        file_loc = self.results_window.get("%s linestart" % index,
                                           "%s lineend" % index)
        # pop open finder window containing file, if line contains any info
        if file_loc != "":
            subprocess.call(["open", "-R", file_loc])

    def checkButtonsStates(self):
        on_off = []
        for val in self.end_buttons.viewvalues():
            on_off.append(val[0].get())
        if 1 in on_off:
            pass
        else:
            self.anyButton.toggle()
            self.endings = ""

    def anyButton_command(self):
        for val in self.end_buttons.viewvalues():
            val[1].deselect()
        self.anyButton.select()
        self.endings = ""

    def jpgButton_command(self):
        if self.jpgState.get():
            self.anyButton.deselect()
        else:
            self.checkButtonsStates()

    def movButton_command(self):
        if self.movState.get():
            self.anyButton.deselect()
        else:
            self.checkButtonsStates()

    def tgaButton_command(self):
        if self.tgaState.get():
            self.anyButton.deselect()
        else:
            self.checkButtonsStates()

    def wavButton_command(self):
        if self.wavState.get():
            self.anyButton.deselect()
        else:
            self.checkButtonsStates()

    def docButton_command(self):
        if self.docState.get():
            self.anyButton.deselect()
        else:
            self.checkButtonsStates()

    def c4dButton_command(self):
        if self.c4dState.get():
            self.anyButton.deselect()
        else:
            self.checkButtonsStates()

    def psdButton_command(self):
        if self.psdState.get():
            self.anyButton.deselect()
        else:
            self.checkButtonsStates()

    def aeButton_command(self):
        if self.aeState.get():
            self.anyButton.deselect()
        else:
            self.checkButtonsStates()

    def dirBtn_command(self):
        """
        Pop up file directory choose dialog box
        Passes chosen directory into the object
        """
        self.search_root = tkFileDialog.askdirectory(initialdir=ROOT)
        self.dirLbl.config(text="Searching in: " + self.search_root)

    def clear_button_command(self):
        # ENABLES EDITING IN RESULT WINDOW
        self.results_window.config(state=tkt.NORMAL)
        self.results_window.delete(1.0, tkt.END)
        self.line_index = 1
        # DISABLES EDITING IN RESULT WINDOW
        self.results_window.config(state=tkt.DISABLED)
        self.filecount.config(text="Files Found: 0")


if __name__ == '__main__':
    root = tkt.Tk()
    myapp = MyApp(root)
    root.mainloop()
