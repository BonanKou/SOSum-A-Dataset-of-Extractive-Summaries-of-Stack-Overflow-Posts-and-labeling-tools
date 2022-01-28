from re import T
from tarfile import PAX_FIELDS
from tkinter import *
from turtle import width
import pandas as pd
import tkinter.font as font
from ast import literal_eval
from tkinter.filedialog import askopenfilename
import functools
import regex

LOG_LINE_NUM = 0
button_color = "#c1c1c1"
border_color = "#f1f1f1"
selected_color = "#ffef61"

class ScrollableFrame(Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = Canvas(self)
        scrollbar = Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

class MY_GUI():
    def __init__(self,root):
        self.root = root
        self.START = False
        self.INDEX = 0

    def setText(self, widget, text):
        try:
            widget.delete("1.0","end")      
        except:
            pass
        widget.insert("1.0", text)

    def prev_callback(self):
        if self.INDEX != 0 and self.START:
            self.INDEX = self.INDEX - 1
            self.refresh()

    def next_callback(self):
        if self.INDEX != self.df.shape[0] and self.START:
            self.INDEX = self.INDEX + 1
            self.refresh()
    
    def start(self, df, questionIds, postIds, scores, question_bodies, answer_bodies, tags, truth):
        self.START = True
        for i in range(df.shape[0]):
            if truth[i] == "Empty":
                break
        self.INDEX = i
        self.refresh()

    def concat(self, a):
        result = ""
        for i in a:
            result += i + " "
        return result[:-1]

    def makeUrl(self, a):
        return "https://stackoverflow.com/a/" + a

    def populateTags(self):
        allTags = self.df["tags"][self.INDEX][1:-1].split("><")
        for widget in self.tags.winfo_children():
            widget.destroy()
        for i in allTags:
            temp = Label(self.tags, 
                    text=i, 
                    border=1,
                    relief=GROOVE,
                    width=len(i),
                    height=1, font=("Helvetica", 10),
                    background="#ff9893"
                    )
            temp.pack(side=LEFT, anchor='n', padx=10, pady = 2)

    def count(self):
        count = 0
        for i in range(self.df.shape[0]):
            if self.df["truth"][i] in ["Empty"]:
                count += 1
        return count
    
    def toString(self, a):
        result = "["
        for i in a:
            result += str(i) + ","
        if result != "[":
            result = result[:-1] + "]"
        else:
            result = result + "]"
        return result

    def clickText(self, event, temp):
        text = temp.get("1.0",END)
        id = int(text.split(":")[0])

        if temp["bg"] == "#e8f6ff":
            temp.config(background="#fcd9ff")
        else:
            temp.config(background="#e8f6ff")
        
        current = self.df.loc[self.INDEX, 'truth']
        if current != "Empty":
            next = literal_eval(current)
            if id not in next:
                next.append(id)
            else:
                next.remove(id)
            self.df.loc[self.INDEX, 'truth'] = self.toString(next)
        else:
            self.df.loc[self.INDEX, 'truth'] = "[" + str(id) + "]"
        self.refresh()

    def selected(self, a):
        if self.df["truth"][self.INDEX] != "Empty":
            try:
                select = literal_eval(self.df["truth"][self.INDEX])
            except: 
                self.df.loc[self.INDEX, "truth"] = "[]"
                select = literal_eval(self.df["truth"][self.INDEX])
            return a in select
        else:
            return False

    def populateAnswer(self):
        for widget in self.hope.winfo_children():
            widget.destroy()
        for index, i in enumerate(literal_eval(self.df["post_body"][self.INDEX])):
            if self.selected(index):
                temp_color = selected_color
            else:
                temp_color = "#e8f6ff"

            temp = Text(self.hope, 
                    border=1,
                    relief=GROOVE,
                    width=77,
                    height=int(len(i) / 50) + 1,
                    background=temp_color, font=("Helvetica", 12), name=str(index)
                    )
            
            temp.grid(row = index, column = 0, pady=2)
            self.setText(temp, str(index) + ": " + i)
            self.color_tag(temp, str(index) + ": " + i)
            temp.config(state=DISABLED)
            temp.tag_add("index", "1.0", "1.{}".format(2+len(str(index))))
            temp.tag_config("index", foreground="red")
            temp.bind("<Button-1>", functools.partial(self.clickText, temp=temp))

    def color_tag(self, widget, text):
        pass
        # for j, k in [(m.start(0), m.end(0)) for m in regex.finditer(r'<code>.+?</code>', text)]:
        #     widget.tag_add("code", "1.{}".format(j), "1.{}".format(k))
        #     widget.tag_config("code", background="#00ab2e")

    def refresh(self):
        if (self.df["truth"][self.INDEX]) == "[]":
            self.skip.configure(bg="#98fac8")
            self.skip.configure(text="Skipped")
        else:
            self.skip.configure(bg=button_color)
            self.skip.configure(text="Skip")
        question = literal_eval(self.df["question_body"][self.INDEX])
        self.setText(self.question_title, question[0])
        self.setText(self.question_body, self.concat(question[1:]))

        self.color_tag(self.question_body, self.concat(question[1:]))

        answer = literal_eval(self.df["post_body"][self.INDEX])
        self.setText(self.question_id, self.makeUrl(str(self.df["post_id"][self.INDEX])))
        # self.setText(self.post_id, "Post Id: " + str(self.df["post_id"][self.INDEX]))
        self.setText(self.score, str(self.df["score"][self.INDEX]))
        self.populateTags()
        self.setText(self.total, str(self.df.shape[0]))
        # self.setText(self.current, "At {}".format(self.INDEX))
        count = self.count()
        self.setText(self.finished, "{}".format(self.df.shape[0]-count))
        self.populateAnswer()
        self.df.to_csv(self.name, index=False)
        

    def populate(self, name):
        try:
            self.df = pd.read_csv(name)
            questionIds = self.df["question_id"]
            postIds = self.df["post_id"]
            scores = self.df["score"]
            question_bodies = self.df["question_body"]
            answer_bodies = self.df["post_body"]
            truth = self.df["truth"]
            tags = self.df["tags"]
            self.start(self.df, questionIds, postIds, scores, question_bodies, answer_bodies, tags, truth)
        except:
            self.setText(self.question_body, '''Wrong file! Please make sure an CSV file is provided with following columns: 
                \n(1) question_id \n(2) answer_id \n(3) score \n(4) question_body \n(5) answer_body \n(6) tags \n(7) truth''')
            self.question_body.tag_add("error", "1.0", "end")
            self.question_body.tag_config("error", foreground="red")


    def addfile_callback(self):
        self.name = askopenfilename()
        # self.setText(self.filename, self.name)
        self.populate(self.name)

    def skip_callback(self):
        if self.START:
            self.df.loc[self.INDEX, "truth"] = "[]"
            self.INDEX += 1
            self.refresh()

    def set_init_window(self):
        myFont = font.Font(family="Helvetica", size=10)
        main_frame = Frame(self.root, border=3)
        main_frame.grid()
        self.root.geometry('+250+30')

        left = Frame(main_frame)
        right = Frame(main_frame)

        question_info = Frame(left,
                border=1,
                width = 50,
                height= 15,
                background=border_color,
        )

        files = Frame(left,
            border = 1,
            width = 1,
            height = 65,
            background = border_color
        )

        # TODO
        self.question_body = Text(question_info,
                border=1,
                width = 84,
                height= 29,
                background="white",font=("Helvetica", 11)
        )

        self.basics = Frame(question_info,
                border=1,
                width = 40,
                height= 5,
                background=border_color,
        )

        self.question_title_container = Frame(self.basics)
        self.question_title_description = Label(self.question_title_container, text="Question title: ", height=1, font = "Helvetica 10 bold")
        self.question_title = Text(self.question_title_container,
            height=2,
            width = 49,font=("Helvetica", 12)
        )


        self.answer_general = Frame(right,
                border=1,
                width = 40,
                height=43,
                background=border_color,)

        self.general = Frame(files,
            background=border_color,
            width = 20      
        )
        # self.answer_general.grid_rowconfigure(0, weight=1)
        self.metadata = Frame(self.answer_general, height=2, width = 30,)
        self.url_description = Label(self.metadata, text="Post URL: ", width=8, font= "Helvetica 10 bold")
        self.question_id = Text(self.metadata, height=2, width=30)
        # self.post_id = Text(self.metadata, height=2, width=17)
        self.score_description = Label(self.metadata, text="Score: ", width=6, font= "Helvetica 10 bold")
        self.score = Text(self.metadata, height=2, width=11)

        self.tag_container = Frame(self.basics,border=1,
                width = 70,
                height= 65,
                background=border_color,
        )

        self.tag_description = Label(self.tag_container, text="Question tags: ", width=11, font="Helvetica 10 bold")

        # TODO
        self.tags = Frame(self.tag_container,
                border=1,
                width = 443,
                height= 30,
                background = "white",
        )

        self.metadata.grid(column = 0, row = 0, padx=(12, 0), sticky="w")
        self.question_title_container.grid(column =0, row = 0, sticky= "w", padx=(1,0))
        self.question_title_description.grid(column = 0, row = 0, padx = (4, 0), pady = 2, columnspan= 1, sticky="w")
        self.question_title.grid(column = 1, row = 0, padx = 0, pady = 2, columnspan=1, sticky="w")
        self.url_description.grid(column = 0, row = 0)
        self.question_id.grid(column = 1, row = 0, padx= 0, pady= 2, sticky=W)
        # self.post_id.grid(column = 2, row = 0, padx= (0, 2), pady= 2, sticky=W)
        self.score_description.grid(column = 2, row = 0)
        self.score.grid(column = 3, row = 0, pady= 2, sticky=W)
        self.tag_container.grid(column = 0, row = 2, padx = 5, pady = 2, columnspan=3, sticky='w')
        self.tag_description.grid(column = 0, row = 0, padx = 2)
        self.tags.grid(column = 1, row = 0, padx=(0, 0), sticky="w")



        # self.filename = Text(files,
        #     border=1,
        #     width = 30,
        #     height= 2,
        #     background="white",
        # )

        addfile = Button(files,
            border=1,
            width = 10,
            height= 1,
            background=button_color,
            relief=GROOVE,
            font=("Helvetica", 10),
            text = "Select file",
            command = self.addfile_callback
        )

        # self.filename.grid(column = 0, row = 0, padx=(20, 45))
        addfile.grid(column = 0, row = 0, sticky="w", padx = (8, 0))
        self.total_description = Label(self.general, text="Total posts: ", width=11, height = 1, font="Helvetica 10 bold")
        self.total = Text(self.general, width=5, height=1, font=("Helvetica", 10), background="white")
        self.finished_description = Label(self.general, text="You have labeled: ", height = 1, width=15, font="Helvetica 10 bold")
        self.finished = Text(self.general, width=5, height = 1, font=("Helvetica", 10), background="white")
        self.post_body = Frame(self.answer_general,
                border=1,
                width = 420,
                height= 600,
                background=border_color,
        )

        # TODO
        canvas=Canvas(self.post_body,bg='#FFFFFF',width=700,height=500) #,scrollregion=(0,0,300,300))
        vbar=Scrollbar(self.post_body,orient=VERTICAL)
        vbar.pack(side=RIGHT,fill=Y)
        vbar.config(command=canvas.yview)
        # TODO
        canvas.config(width=700,height=500)
        canvas.config(yscrollcommand=vbar.set)
        canvas.pack(side=LEFT,expand=True,fill=BOTH)

        self.general.grid(column=1, row=0, sticky="w")
        self.total.grid(column=1, row=0)
        self.total_description.grid(column = 0, row = 0)
        self.finished_description.grid(column=2, row = 0)
        # self.current.grid(coumn=1, row=0, padx=10)
        self.finished.grid(column=3, row=0)
        self.post_body.grid(column = 0, row = 1, padx=10)

        self.hope = Frame(canvas, background="white")
        self.hope.grid()
        self.hope.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.hope, anchor="nw")
        canvas.configure(yscrollcommand=vbar.set)

        buttons = Frame(right,
                border = 1,
                width = 40,
                height = 10,
                # relief=GROOVE,
                background=border_color,
        )

        prev = Button(buttons, 
                height = 2,
                background=button_color,
                width = 10,
                text= "Previous",
                font=("Helvetica", 14),
                command = self.prev_callback
        )

        next = Button(buttons, 
                height = 2,
                width = 10,
                background=button_color,
                text = "Next",
                font=("Helvetica", 14),
                command = self.next_callback
        )

        self.skip = Button(buttons, 
                height = 2,
                background=button_color,
                width = 10,
                text= "Skip",
                font=("Helvetica", 14),
                command = self.skip_callback
        )

        self.skip.grid(row = 0, column = 2, pady = (10, 0)) #, padx=(20, 30))

        files.grid(row = 0, column = 0, sticky='nsew')
        prev.grid(row = 0, column = 0, pady=(10, 0), padx=(0, 30))
        next.grid(row = 0, column = 1, pady=(10, 0), padx=(0, 30))

        left.grid(row = 0, column = 0)
        right.grid(row = 0, column = 1)
        # TODO
        self.question_body.grid(row=1, column=0, padx=(8, 0))
        self.basics.grid(row=0, column=0, sticky="w")
        question_info.grid(row=1, column=0)
        self.answer_general.grid(row=0, column = 0, sticky=N) 
        # TODO
        buttons.grid(row=1, column = 0, sticky="w", padx=(150,0)) 
        self.tags.pack_propagate(0)
        self.post_body.grid_propagate(False)
        files.pack_propagate(0)

def gui_start():
    root = Tk()
    root.title('SO post labeler')
    ZMJ_PORTAL = MY_GUI(root)
    ZMJ_PORTAL.set_init_window()
    root.mainloop()


gui_start()