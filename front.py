from tkinter import *
from tkinter import font as tkFont
from back import insert_team, insert_worker, insert_product, insert_issue, team_names, product_names, relate_all


class Ticket_Management_System(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title_font = tkFont.Font(
            family='Helvetica', size=18, weight="bold", slant="italic")

        # stacking of multiple frames on top of each other
        # the one visible will be raised on top
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (GUI_team_input, GUI_worker_input, GUI_product_input, GUI_issue_input, issues_view):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("issues_view")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class GUI_team_input(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.current_row = 0

        # Query Panel
        # Worker Name field
        self.team_label = Label(self, text="Team Name: ")
        self.team_label.grid(row=self.current_row, column=0)
        self.team_text = StringVar()
        self.team_entry = Entry(self, textvariable=self.team_text)
        self.team_entry.grid(row=self.current_row, column=1)
        self.current_row += 1

        # Query status
        self.querystatus = Label(self, text='')
        self.querystatus.grid(row=self.current_row, column=0, columnspan=2)
        self.current_row += 1

        button = Button(self, text='Back',
                        command=lambda: controller.show_frame("issues_view"))
        button_save = Button(self, text='Insert team', command=self.send_query)

        button_save.grid(row=self.current_row, column=0)
        button.grid(row=self.current_row, column=1)
        self.current_row += 1

    def send_query(self):
        team_name = self.team_text.get()
        response = insert_team(team_name)
        self.querystatus.configure(text=response)


class GUI_worker_input(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.current_row = 0

        # Query Panel
        # Worker Name field
        self.worker_label = Label(self, text="Worker Name: ")
        self.worker_label.grid(row=self.current_row, column=0)
        self.worker_text = StringVar()
        self.worker_entry = Entry(self, textvariable=self.worker_text)
        self.worker_entry.grid(row=self.current_row, column=1)
        self.current_row += 1

        # Team ID field
        self.team_label = Label(self, text="Team: ")
        self.team_label.grid(row=self.current_row, column=0)
        self.variable = StringVar(self)
        self.variable.set('Choose a team')
        self.team_options = OptionMenu(
            self, self.variable, *self.get_options())
        self.team_options.grid(row=self.current_row, column=1)
        self.current_row += 1

        # Query status
        self.querystatus = Label(self, text='')
        self.querystatus.grid(row=self.current_row, column=0, columnspan=2)
        self.current_row += 1

        button = Button(self, text='Back',
                        command=lambda: controller.show_frame("issues_view"))
        button_save = Button(self, text='Insert worker',
                             command=self.send_query)

        button_save.grid(row=self.current_row, column=0)
        button.grid(row=self.current_row, column=1)
        self.current_row += 1

    def get_options(self):
        return team_names()

    def send_query(self):
        worker_name = self.worker_text.get()
        team = self.variable.get()
        response = insert_worker(worker_name, team)
        self.querystatus.configure(text=response)


class GUI_product_input(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.current_row = 0

        # Query Panel
        # Worker Name field
        self.product_label = Label(self, text="Product Name: ")
        self.product_label.grid(row=self.current_row, column=0)
        self.product_text = StringVar()
        self.product_entry = Entry(self, textvariable=self.product_text)
        self.product_entry.grid(row=self.current_row, column=1)
        self.current_row += 1

        # Query status
        self.querystatus = Label(self, text='')
        self.querystatus.grid(row=self.current_row, column=0, columnspan=2)
        self.current_row += 1

        button = Button(self, text='Back',
                        command=lambda: controller.show_frame("issues_view"))
        button_save = Button(self, text='Insert product',
                             command=self.send_query)

        button_save.grid(row=self.current_row, column=0)
        button.grid(row=self.current_row, column=1)
        self.current_row += 1

    def send_query(self):
        product_name = self.product_text.get()
        response = insert_product(product_name)
        self.querystatus.configure(text=response)


class GUI_issue_input(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.current_row = 0

        # Query Panel
        # Issue type field
        self.issue_label = Label(self, text="Issue Type: ")
        self.issue_label.grid(row=self.current_row, column=0)
        self.issue_options = ['Suggestion', 'Complaint', 'Request']
        self.issue_text = StringVar()
        self.issue_options = OptionMenu(
            self, self.issue_text, *self.issue_options)
        self.issue_options.grid(row=self.current_row, column=1)
        self.current_row += 1

        # Team ID field
        self.team_label = Label(self, text="Team: ")
        self.team_label.grid(row=self.current_row, column=0)
        self.team_text = StringVar(self)
        self.team_text.set('Choose a team')
        self.team_options = OptionMenu(
            self, self.team_text, *self.get_team_options())
        self.team_options.grid(row=self.current_row, column=1)
        self.current_row += 1

        # Product ID field
        self.product_label = Label(self, text="Product: ")
        self.product_label.grid(row=self.current_row, column=0)
        self.product_text = StringVar(self)
        self.product_text.set('Choose a product')
        self.product_options = OptionMenu(
            self, self.product_text, *self.get_product_options())
        self.product_options.grid(row=self.current_row, column=1)
        self.current_row += 1

        # Issue Description field
        self.desc_label = Label(self, text="Issue Description: ")
        self.desc_label.grid(row=self.current_row, column=0)
        self.desc_text = StringVar()
        self.desc_entry = Entry(self, textvariable=self.desc_text, width=60)
        self.desc_entry.grid(row=self.current_row, column=1, sticky='we')
        self.current_row += 1

        # Issue Priority field
        self.priority_label = Label(self, text="Issue priority: ")
        self.priority_label.grid(row=self.current_row, column=0)
        self.priority_text = StringVar(self)
        self.priority_option = [1, 2, 3]
        self.priority_text.set('Select priority')
        self.priority_options = OptionMenu(
            self, self.priority_text, *self.priority_option)
        self.priority_options.grid(row=self.current_row, column=1)
        self.current_row += 1

        # Issue Severity field
        self.severity_label = Label(self, text="Issue Severity: ")
        self.severity_label.grid(row=self.current_row, column=0)
        self.severity_text = StringVar(self)
        self.severity_option = [1, 2, 3]
        self.severity_text.set('Select severity')
        self.severity_options = OptionMenu(
            self, self.severity_text, *self.severity_option)
        self.severity_options.grid(row=self.current_row, column=1)
        self.current_row += 1

        # Query status
        self.querystatus = Label(self, text='')
        self.querystatus.grid(row=self.current_row, column=0, columnspan=2)
        self.current_row += 1

        button = Button(self, text='Back',
                        command=lambda: controller.show_frame("issues_view"))
        button_save = Button(self, text='Insert issue',
                             command=self.send_query)

        button_save.grid(row=self.current_row, column=0)
        button.grid(row=self.current_row, column=1)
        self.current_row += 1

    def get_team_options(self):
        return team_names()

    def get_product_options(self):
        return product_names()

    def send_query(self):
        team = self.team_text.get()
        product = self.product_text.get()
        issue_type = self.issue_text.get()
        issue_desc = self.desc_text.get()
        issue_priority = self.priority_text.get()
        issue_severity = self.severity_text.get()
        response = insert_issue(team, product, issue_type,
                                issue_desc, issue_priority, issue_severity)
        self.querystatus.configure(text=response)


class issues_view(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.initUI(parent, controller)

    def initUI(self, parent, controller):
        self.frame_one = Frame(self, parent)
        self.frame_one.grid(row=0, column=0)

        self.frame_two = Frame(self, parent)
        self.frame_two.grid(row=1, column=0)

        self.canvas = Canvas(self.frame_two)
        self.list_frame = Frame(self.canvas)
        self.scrolllib = Scrollbar(
            parent, orient='vertical', command=self.canvas.yview)
        self.scrolllib.grid(row=0, column=1, sticky='nsew')
        self.canvas['yscrollcommand'] = self.scrolllib.set

        self.canvas.create_window((0, 0), window=self.list_frame, anchor='nw')
        self.list_frame.bind('<Configure>', self.Auxscrollfunction)

        self.canvas.pack(side='left')
        self.frame_three = Frame(parent)
        self.frame_three.grid(row=0, column=0)

        self.product_name = Label(
        self.list_frame, text='Product Name', font='Helvetica 10 bold', width=20, wraplength=50)
        self.product_name.grid(row=0, column=0)
        self.issue_type = Label(self.list_frame, text='Issue Type',
                                font='Helvetica 10 bold', width=20, wraplength=50)
        self.issue_type.grid(row=0, column=1)
        self.issue_description = Label(
            self.list_frame, text='Issue Description', font='Helvetica 10 bold', width=50, wraplength=75)
        self.issue_description.grid(row=0, column=2)
        self.issue_priority = Label(
            self.list_frame, text='Issue Priority', font='Helvetica 10 bold', width=8, wraplength=50)
        self.issue_priority.grid(row=0, column=3)
        self.issue_severity = Label(
            self.list_frame, text='Issue Severity', font='Helvetica 10 bold', width=8, wraplength=70)
        self.issue_severity.grid(row=0, column=4)
        self.issue_impact = Label(
            self.list_frame, text='Issue Impact', font='Helvetica 10 bold', width=8, wraplength=50)
        self.issue_impact.grid(row=0, column=5)
        self.worker_name = Label(
            self.list_frame, text='Worker Name', font='Helvetica 10 bold', width=6, wraplength=50)
        self.worker_name.grid(row=0, column=6)
        self.team_name = Label(
            self.list_frame, text="Team Name", font='Helvetica 10 bold', width=7, wraplength=50)
        self.team_name.grid(row=0, column=7)
        self.populate()
        button_team = Button(self.frame_one, text="Add Teams",
                             command=lambda: controller.show_frame("GUI_team_input"))
        button_worker = Button(
            self.frame_one, text="Add Workers", command=lambda: controller.show_frame("GUI_worker_input"))
        button_product = Button(
            self.frame_one, text="Add Products", command=lambda: controller.show_frame("GUI_product_input"))
        button_issue = Button(
            self.frame_one, text="Add Issues", command=lambda: controller.show_frame("GUI_issue_input"))
        button_team.grid(row=0, column=0, sticky='w')
        button_worker.grid(row=0, column=1)
        button_product.grid(row=0, column=2)
        button_issue.grid(row=0, column=3)

    def populate(self):
        data = relate_all()
        for index, dat in enumerate(data):
            Label(self.list_frame, text=dat[0]).grid(row=index + 1, column=0)
            Label(self.list_frame, text=dat[1]).grid(row=index + 1, column=1)
            Label(self.list_frame, text=dat[2]).grid(row=index + 1, column=2)
            Label(self.list_frame, text=dat[3]).grid(row=index + 1, column=3)
            Label(self.list_frame, text=dat[4]).grid(row=index + 1, column=4)
            Label(self.list_frame, text=dat[5]).grid(row=index + 1, column=5)
            Label(self.list_frame, text=dat[6]).grid(row=index + 1, column=6)
            Label(self.list_frame, text=dat[7]).grid(row=index + 1, column=7)

    def Auxscrollfunction(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox(
            'all'), width=1080, height=150)


def main():
    window = Ticket_Management_System()
    window.wm_title("Ticket Managemnt System")
    window.mainloop()


if __name__ == "__main__":
    main()
