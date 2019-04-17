from tkinter import *
import backend


class Note(Tk):

    def __init__(self, *args, **kwargs):

        Tk.__init__(self, *args, **kwargs)
        self.container = Frame(self)

        self.container.pack(side="top", fill="both", expand = True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.display(StartPage)

    def display(self,cont):
        frame = cont(self.container,self)
        frame.grid(row=0, column=0, sticky="nsew")


class StartPage(Frame):

    note_idx = []

    def __init__(self, parent, controller):
        Frame.__init__(self,parent)

        StartPage.note_idx = []

        def on_configure(event):
            all_notes_canvas.configure(scrollregion=all_notes_canvas.bbox('all'))

        all_notes_surface = Frame(self,relief='groove',bd=2)
        all_notes_surface.place(relx=0,rely=0,relheight=1,relwidth=1)

        title_frame = Frame(all_notes_surface,bg='orange',relief='groove',bd=2)
        title_frame.place(relx=0,rely=0,relwidth=1,relheight=0.2)

        title = Label(title_frame, text='My Notes', font=('verdana',24,'bold'),bg="orange")
        title.place(relx=0.4,rely=0,relwidth=0.2,relheight=1)

        add_new = Button(title_frame,text='Add New')
        add_new.configure(command=lambda: controller.display(PageOne))
        add_new.place(relx=0.9,rely=0,relwidth=0.1,relheight=0.3)

        all_notes_canvas = Canvas(all_notes_surface,relief='groove',bd=2)
        all_notes_canvas.place(relx=0,rely=0.2,relwidth=1,relheight=0.8)

        frame = Frame(all_notes_canvas)
        frame.bind('<Configure>', on_configure)

        all_notes_canvas.create_window(0, 0, window=frame)

        scrolly = Scrollbar(all_notes_surface, command=all_notes_canvas.yview,bg='black')
        scrolly.place(relx=1, rely=0.2, relheight=0.8, anchor='ne')
        all_notes_canvas.configure(yscrollcommand=scrolly.set)


        query = 'SELECT title,created,id FROM note;'

        all_data = backend.execute_query(query)

        frames_to_detail = []


        def callback(event):
            index = None
            if event.widget in frames_to_detail:
                index = frames_to_detail.index(event.widget)

            self.note_id = all_data[index][2]

            StartPage.note_idx.append(self.note_id)

            return controller.display(PageOne)


        if all_data:

            for i,data in enumerate(all_data):

                single_note_frame = Frame(frame,relief='groove',bd=2)
                single_note_frame.configure(bg='grey',height=75,width=800)
                note_title = Label(single_note_frame,text='{}'.format(data[0]),anchor='w')
                note_title.configure(font=('verdana',20),bg='grey',padx=20)
                note_title.place(relx=0,rely=0.2,relwidth=0.5,relheight=0.6)

                note_created = Label(single_note_frame,text='{}'.format(data[1]),anchor='e')
                note_created.configure(font=('verdana',10),bg='grey',padx=20)
                note_created.place(relx=0.75,rely=0.02,relwidth=0.25,relheight=0.6)

                single_note_frame.pack()

                frames_to_detail.append(single_note_frame)

                single_note_frame.bind("<Button-1>", callback)


class PageOne(StartPage,Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        query = 'SELECT title,description FROM note WHERE id={};'

        # print(all_data)
        self.configure(bg='orange')

        note_title = Label(self,text='Title :',font=("Verdana", 18,"bold"),bg='orange')
        note_title.place(relx=0,rely=0.1,relheight=0.08,relwidth=0.18)

        title_input = StringVar()
        note_title_entry = Entry(self, textvariable = title_input)
        note_title_entry.place(relx=0.2,rely=0.1,relheight=0.08,relwidth=0.7)


        description = Label(self,text='Description :',font=("Verdana", 18,"bold"),bg='orange')
        description.place(relx=0,rely=0.25,relheight=0.08,relwidth=0.18)

        desc_input = StringVar()
        description_text = Text(self,height=2, width=30,bd=2, relief='sunken')
        description_text.place(relx=0.2,rely=0.25,relheight=0.4,relwidth=0.7)

        try:
            all_data = backend.execute_query_1(query.format(StartPage.note_idx[0]))

            if all_data:
                note_title_entry.insert(0, all_data[0])
                description_text.insert(END, all_data[1])
        except:
            all_data = None

        def delete_notex():
            if all_data:
                query = 'DELETE FROM note WHERE id={}'.format(StartPage.note_idx[0])
                backend.delete_note(query)
            return controller.display(StartPage)

        def save_or_update():


            try:

                if not all_data:

                    query = "INSERT INTO note (title,description) VALUES('{}','{}');"

                    backend.store_note(query.format(title_input.get(),description_text.get('1.0', END)))
                    print('DATA STORED.....')

                else:
                    query = "UPDATE note SET title = '{}', description = '{}' WHERE  id = {};"

                    # UPDATE `members` SET `full_names` = 'Janet Smith Jones', `physical_address` = 'Melrose 123' WHERE `membership_number` = 2;
                    backend.update_note(query.format(title_input.get(),description_text.get('1.0', END),StartPage.note_idx[0]))
                    print('DATA UPDATED.....')

            except Exception as err:print(err)

            return controller.display(StartPage)

        back_btn = Button(self,text='Back')
        back_btn.configure(command=lambda: controller.display(StartPage))
        back_btn.place(relx=0.05, rely=0.85, relwidth=0.1,relheight=0.1)

        save_btn = Button(self,text='Save')
        save_btn.configure(command=save_or_update)
        save_btn.place(relx=0.65, rely=0.85, relwidth=0.1,relheight=0.1)

        delete_btn = Button(self,text='Delete')
        delete_btn.configure(command=delete_notex)
        delete_btn.place(relx=0.8, rely=0.85, relwidth=0.1,relheight=0.1)


def main():

    app = Note()
    app.title("My Notes")
    app.geometry("800x480")
    app.resizable(False,False)

    app.mainloop()


if __name__=="__main__":main()
