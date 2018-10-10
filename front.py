from tkinter import *
from tkinter import font as tkFont
from back import insert_team, remove_team, insert_worker, remove_worker, insert_product, \
    remove_product, insert_issue, team_names, worker_names, product_names, \
    relate_all, login_check


class Ticket_Management_System(Tk):
    # Main class for the system

    def __init__(self, *args, **kwargs):
        # Function for intializing all the views

        Tk.__init__(self, *args, **kwargs)
        self.title_font = tkFont.Font(
            family='Helvetica', size=18, weight="bold", slant="italic")

        # Stacking of multiple frames on top of each other
        # the one visible will be raised on top
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # All the classes whose view is to be shown
        self.classes = (login_view, issues_view, GUI_team_edit, GUI_team_input, GUI_team_remove, GUI_worker_edit,
                        GUI_worker_input, GUI_worker_remove, GUI_product_edit, GUI_product_input, GUI_product_remove, GUI_issue_input)
        self.frames = {}
        for F in self.classes:
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("login_view")  # First frame to be shown

    def show_frame(self, page_name):
        # Function to raise the requested frame to the top
        frame = self.frames[page_name]
        frame.tkraise()


class login_view(Frame):
    # Login view class of the app

    def __init__(self, parent, controller):
        # Function for initializing the components of the view
        Frame.__init__(self, parent)
        self.controller = controller

        self.current_row = 0  # Set the current row count of the view

        # Username Field
        self.username_label = Label(self, text='Username: ')
        self.username_label.grid(row=self.current_row, column=0)
        self.username_text = StringVar()
        self.username_entry = Entry(
            self, textvariable=self.username_text, width=60)
        self.username_entry.grid(row=self.current_row, column=1, sticky='we')
        self.current_row += 1

        # Password field
        self.password_label = Label(self, text='Password: ')
        self.password_label.grid(row=self.current_row, column=0)
        self.password_text = StringVar()
        self.password_entry = Entry(
            self, textvariable=self.password_text, show='*', width=60)
        self.password_entry.grid(row=self.current_row, column=1, sticky='we')
        self.current_row += 1

        # Query status
        self.querystatus = Label(self, text='')
        self.querystatus.grid(row=self.current_row, column=0, columnspan=2)
        self.current_row += 1

        # Button for login action
        self.button = Button(
            self, text="Login", command=lambda: self.login())
        self.button.grid(row=self.current_row, column=0)
        self.current_row += 1

    def login(self):
        # Function to pass on the username and password to the login function
        response = login_check(self.username_text.get(),
                               self.password_text.get())
        if response:
            self.controller.show_frame('issues_view')
        else:
            self.querystatus.configure(text='Incorrect login')


class issues_view(Frame):
    # Issues view of the app

    def __init__(self, parent, controller):
        # Function to initialize the components of the view
        Frame.__init__(self, parent)
        self.controller = controller
        self.initUI(parent, controller)

    def initUI(self, parent, controller):
        # Function to initialize the various frames

        # Frame one declaration
        self.frame_one = Frame(self, parent)
        self.frame_one.grid(row=0, column=0)

        # Frame two declaration
        self.frame_two = Frame(self, parent)
        self.frame_two.grid(row=1, column=0)

        # Canvas decalaration
        self.canvas = Canvas(self.frame_two)

        # List frame declaration
        self.list_frame = Frame(self.canvas)

        # Scrollbar declaration
        self.scrolllib = Scrollbar(
            parent, orient='vertical', command=self.canvas.yview)
        self.scrolllib.grid(row=0, column=1, sticky='nsew')
        self.canvas['yscrollcommand'] = self.scrolllib.set

        # Canvas window creation
        self.canvas.create_window((0, 0), window=self.list_frame, anchor='nw')

        # Binding of the scrolling function to the frame
        self.list_frame.bind('<Configure>', self.Auxscrollfunction)

        self.canvas.pack(side='left')

        # Frame three declaration
        self.frame_three = Frame(parent)
        self.frame_three.grid(row=0, column=0)

        # Column labels
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

        # Button declarations
        self.button_team = Button(self.frame_one, text="Edit Teams",
                             command=lambda: controller.show_frame("GUI_team_edit"))
        self.button_worker = Button(
            self.frame_one, text="Edit Workers", command=lambda: controller.show_frame("GUI_worker_edit"))
        self.button_product = Button(
            self.frame_one, text="Edit Products", command=lambda: controller.show_frame("GUI_product_edit"))
        self.button_issue = Button(
            self.frame_one, text="Add Issues", command=lambda: controller.show_frame("GUI_issue_input"))
        self.button_refresh = Button(
            self.frame_one, text='Refesh', command=self.populate)

        # Button positioning
        self.button_team.grid(row=0, column=0, sticky='w')
        self.button_worker.grid(row=0, column=1)
        self.button_product.grid(row=0, column=2)
        self.button_issue.grid(row=0, column=3)
        self.button_refresh.grid(row=0, column=4)

    def populate(self):
        # Function to populate the list view
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
        # Function for the scrolling of the canvas
        self.canvas.configure(scrollregion=self.canvas.bbox(
            'all'), width=1080, height=150)


class GUI_team_edit(Frame):
    # Team editing options view of the app

    def __init__(self, parent, controller):
        # Function to initialize the components of the view
        Frame.__init__(self, parent)
        self.controller = controller

        self.current_row = 0  # Set the current row count of the view

        # Buttons declaration
        self.button_input = Button(
            self, text='Add teams', command=lambda: controller.show_frame('GUI_team_input'))
        self.button_delete = Button(
            self, text='Remove teams', command=lambda: controller.show_frame('GUI_team_remove'))
        self.button_back = Button(
            self, text='Back', command=lambda: controller.show_frame('issues_view'))

        # Buttons positioning
        self.button_input.pack()
        self.button_delete.pack()
        self.button_back.pack(side='left')


class GUI_worker_edit(Frame):
    # Worker editing options of the app

    def __init__(self, parent, controller):
        # Function for initaializing the components of the view
        Frame.__init__(self, parent)
        self.controller = controller

        # Set the current row count of the view  # Set the current row count of the view
        self.current_row = 0

        # Buttons declaration
        self.button_input = Button(
            self, text='Add workers', command=lambda: controller.show_frame('GUI_worker_input'))
        self.button_delete = Button(
            self, text='Remove workers', command=lambda: controller.show_frame('GUI_worker_remove'))
        self.button_back = Button(
            self, text='Back', command=lambda: controller.show_frame('issues_view'))

        # Buttons positioning
        self.button_input.pack()
        self.button_delete.pack()
        self.button_back.pack(side='left')


class GUI_product_edit(Frame):
    # Product editing options of the app

    def __init__(self, parent, controller):
        # Function for initialzing the components of the view
        Frame.__init__(self, parent)
        self.controller = controller

        self.current_row = 0  # Set the current row count of the view

        # Button declaration
        self.button_input = Button(
            self, text='Add products', command=lambda: controller.show_frame('GUI_product_input'))
        self.button_delete = Button(
            self, text='Remove products', command=lambda: controller.show_frame('GUI_product_remove'))
        self.button_back = Button(
            self, text='Back', command=lambda: controller.show_frame('issues_view'))

        # Button positioning
        self.button_input.pack()
        self.button_delete.pack()
        self.button_back.pack(side='left')


class GUI_team_input(Frame):
    # Team input view for the app

    def __init__(self, parent, controller):
        # Function for initializing the components of the app
        Frame.__init__(self, parent)
        self.controller = controller

        self.current_row = 0  # Set the current row count of the view

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

        # Button declaration
        self.button = Button(self, text='Back',
                        command=lambda: controller.show_frame("GUI_team_edit"))
        self.button_save = Button(self, text='Insert team', command=self.send_query)

        # Button positioning
        self.button_save.grid(row=self.current_row, column=0)
        self.button.grid(row=self.current_row, column=1)
        self.current_row += 1

    def send_query(self):
        # Function to pass on the details for insertion of the team
        team_name = self.team_text.get()
        response = insert_team(team_name)
        self.querystatus.configure(text=response)


class GUI_team_remove(Frame):
    # Team removal view of the app

    def __init__(self, parent, controller):
        # Function for initializing the components of the app
        Frame.__init__(self, parent)
        self.controller = controller

        self.current_row = 0  # Set the current row count of the view

        # Team selection menu
        self.team_label = Label(self, text="Team: ")
        self.team_label.grid(row=self.current_row, column=0)
        self.team_text = StringVar(self)
        self.team_text.set('Choose a team')
        self.team_options = OptionMenu(
            self, self.team_text, *self.get_options())
        self.team_options.grid(row=self.current_row, column=1)
        self.team_refresh = Button(
            self, text='Refresh', command=self.update_team_option)  # Button for resfreshing the option menu
        self.team_refresh.grid(row=self.current_row, column=2)
        self.current_row += 1

        # Query status
        self.querystatus = Label(self, text='')
        self.querystatus.grid(row=self.current_row, column=0, columnspan=2)
        self.current_row += 1

        # Button declaration
        self.button_back = Button(self, text='Back',
                             command=lambda: controller.show_frame("GUI_team_edit"))
        self.button_remove = Button(self, text='Remove team',
                               command=self.send_query)

        # Button positioning
        self.button_back.grid(row=self.current_row, column=0)
        self.button_remove.grid(row=self.current_row, column=1)
        self.current_row += 1

    def get_options(self):
        # Function to get the names of the existing teans
        return team_names()

    def update_team_option(self):
        # Function to update the option menu
        menu = self.team_options['menu']
        menu.delete(0, 'end')
        for value in team_names():
            menu.add_command(
                label=value, command=lambda v=value: self.team_text.set(v))

    def send_query(self):
        # Function to pass on the values for removal of the teams
        team_name = self.team_text.get()
        response = remove_team(team_name)
        self.querystatus.configure(text=response)


class GUI_worker_input(Frame):
    # Worker input view of the app

    def __init__(self, parent, controller):
        # Function to initialize the components of the app
        Frame.__init__(self, parent)
        self.controller = controller

        self.current_row = 0  # Set the current row count of the view

        # Worker Name field
        self.worker_label = Label(self, text="Worker Name: ")
        self.worker_label.grid(row=self.current_row, column=0)
        self.worker_text = StringVar()
        self.worker_entry = Entry(self, textvariable=self.worker_text)
        self.worker_entry.grid(row=self.current_row, column=1)
        self.current_row += 1

        # Team selection field
        self.team_label = Label(self, text="Team: ")
        self.team_label.grid(row=self.current_row, column=0)
        self.variable = StringVar(self)
        self.variable.set('Choose a team')
        self.team_options = OptionMenu(
            self, self.variable, *self.get_options())
        self.team_options.grid(row=self.current_row, column=1)
        self.team_refresh = Button(
            self, text='Refresh', command=self.update_team_option)  # Buttion to refresh the options for the menu
        self.team_refresh.grid(row=self.current_row, column=2)
        self.current_row += 1

        # Query status
        self.querystatus = Label(self, text='')
        self.querystatus.grid(row=self.current_row, column=0, columnspan=2)
        self.current_row += 1

        # Button declaration
        self.button = Button(self, text='Back',
                        command=lambda: controller.show_frame("GUI_worker_edit"))
        self.button_save = Button(self, text='Insert worker',
                             command=self.send_query)

        # Button positioning
        self.button_save.grid(row=self.current_row, column=1)
        self.button.grid(row=self.current_row, column=0)
        self.current_row += 1

    def get_options(self):
        # Function to get the team names
        return team_names()

    def update_team_option(self):
        # Function to update the OptionMenu
        menu = self.team_options['menu']
        menu.delete(0, 'end')
        for value in team_names():
            menu.add_command(
                label=value, command=lambda v=value: self.team_text.set(v))

    def send_query(self):
        # Function to pass on the values for adding the workers
        worker_name = self.worker_text.get()
        team = self.variable.get()
        response = insert_worker(worker_name, team)
        self.querystatus.configure(text=response)


class GUI_worker_remove(Frame):
    # Worker removal view of the app

    def __init__(self, parent, controller):
        # Function to initialize the components of the view
        Frame.__init__(self, parent)
        self.controller = controller

        self.current_row = 0  # Set the current row count of the view

        # Team selection menu
        self.team_label = Label(self, text="Team: ")
        self.team_label.grid(row=self.current_row, column=0)
        self.team_text = StringVar(self)
        self.team_text.set(self.get_team_options()[0])
        self.team_options = OptionMenu(
            self, self.team_text, *self.get_team_options())
        self.team_options.grid(row=self.current_row, column=1)
        self.current_row += 1

        # Worker selection menu
        self.worker_label = Label(self, text="Worker: ")
        self.worker_label.grid(row=self.current_row, column=0)
        self.worker_text = StringVar(self)
        self.worker_text.set('Choose a worker')
        self.worker_options = OptionMenu(
            self, self.worker_text, *self.get_worker_options())
        self.worker_options.grid(row=self.current_row, column=1)
        self.worker_refresh = Button(
            self, text='Refresh', command=self.update_worker_option)
        self.worker_refresh.grid(row=self.current_row, column=2)
        self.current_row += 1

        # Query status
        self.querystatus = Label(self, text='')
        self.querystatus.grid(row=self.current_row, column=0, columnspan=2)
        self.current_row += 1

        # Button declaration
        self.button_back = Button(self, text='Back',
                             command=lambda: controller.show_frame("GUI_worker_edit"))
        self.button_remove = Button(self, text='Remove worker',
                               command=self.send_query)

        # Button positioning
        self.button_back.grid(row=self.current_row, column=0)
        self.button_remove.grid(row=self.current_row, column=1)
        self.current_row += 1

    def get_team_options(self):
        # Function to get the team names
        return team_names()

    def get_worker_options(self):
        # Function to get the worker names
        return worker_names(self.team_text.get())

    def update_worker_option(self):
        # Function to update the OptionMenu
        menu = self.worker_options['menu']
        menu.delete(0, 'end')
        for value in worker_names(self.team_text.get()):
            menu.add_command(
                label=value, command=lambda v=value: self.worker_text.set(v))

    def send_query(self):
        # Function to pass on the values needed to remove the workers
        worker_name = self.worker_text.get()
        team_name = self.team_text.get()
        response = remove_worker(worker_name, team_name)
        self.querystatus.configure(text=response)


class GUI_product_input(Frame):
    # Product insertion view of the app

    def __init__(self, parent, controller):
        # Function to initialize the components of the view
        Frame.__init__(self, parent)
        self.controller = controller

        self.current_row = 0  # Set the current row count of the view

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

        # Button declaration
        self.button = Button(self, text='Back',
                        command=lambda: controller.show_frame("GUI_product_edit"))
        self.button_save = Button(self, text='Insert product',
                             command=self.send_query)

        # Button postioning
        self.button_save.grid(row=self.current_row, column=0)
        self.button.grid(row=self.current_row, column=1)
        self.current_row += 1

    def send_query(self):
        # Function to pass on the values needed to insert the product
        product_name = self.product_text.get()
        response = insert_product(product_name)
        self.querystatus.configure(text=response)


class GUI_product_remove(Frame):
    # Product removal view of the app

    def __init__(self, parent, controller):
        # Function to initialize the components of the app
        Frame.__init__(self, parent)
        self.controller = controller

        self.current_row = 0  # Set the current row count of the view

        # Produt selection menu
        self.product_label = Label(self, text="Product: ")
        self.product_label.grid(row=self.current_row, column=0)
        self.product_text = StringVar(self)
        self.product_text.set('Choose a product')
        self.product_options = OptionMenu(
            self, self.product_text, *self.get_options())
        self.product_options.grid(row=self.current_row, column=1)
        self.product_refresh = Button(
            self, text='Refresh', command=self.update_product_option)
        self.product_refresh.grid(row=self.current_row, column=2)
        self.current_row += 1

        # Query status
        self.querystatus = Label(self, text='')
        self.querystatus.grid(row=self.current_row, column=0, columnspan=2)
        self.current_row += 1

        # Button declaration
        self.button_back = Button(self, text='Back',
                             command=lambda: controller.show_frame("GUI_product_edit"))
        self.button_remove = Button(self, text='Remove product',
                               command=self.send_query)

        # Button positioning
        self.button_back.grid(row=self.current_row, column=0)
        self.button_remove.grid(row=self.current_row, column=1)
        self.current_row += 1

    def get_options(self):
        # Function to get the product names
        return product_names()

    def update_product_option(self):
        # Function to update the OptionMenu
        menu = self.product_options['menu']
        menu.delete(0, 'end')
        for value in product_names():
            menu.add_command(
                label=value, command=lambda v=value: self.product_text.set(v))

    def send_query(self):
        # Function to pass on the values for product removal
        product_name = self.product_text.get()
        response = remove_product(product_name)
        self.querystatus.configure(text=response)


class GUI_issue_input(Frame):
    # Issue input view of the app

    def __init__(self, parent, controller):
        # Function to initialize the components of the view
        Frame.__init__(self, parent)
        self.controller = controller

        self.current_row = 0  # Set the current row count of the view

        # Issue type selection menu
        self.issue_label = Label(self, text="Issue Type: ")
        self.issue_label.grid(row=self.current_row, column=0)
        self.issue_options = ['Suggestion', 'Complaint', 'Request']
        self.issue_text = StringVar()
        self.issue_options = OptionMenu(
            self, self.issue_text, *self.issue_options)
        self.issue_options.grid(row=self.current_row, column=1)
        self.current_row += 1

        # Team selection menu
        self.team_label = Label(self, text="Team: ")
        self.team_label.grid(row=self.current_row, column=0)
        self.team_text = StringVar(self)
        self.team_text.set(self.get_team_options()[0])
        self.team_options = OptionMenu(
            self, self.team_text, *self.get_team_options())
        self.team_options.grid(row=self.current_row, column=1)
        self.current_row += 1

        # Worker selection menu
        self.worker_label = Label(self, text="Team: ")
        self.worker_label.grid(row=self.current_row, column=0)
        self.worker_text = StringVar(self)
        self.worker_text.set('Choose a worker')
        self.worker_options = OptionMenu(
            self, self.worker_text, *self.get_worker_options())
        self.worker_options.grid(row=self.current_row, column=1)
        self.current_row += 1

        # Product selection menu
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

        # Issue Priority selection menu
        self.priority_label = Label(self, text="Issue priority: ")
        self.priority_label.grid(row=self.current_row, column=0)
        self.priority_text = StringVar(self)
        self.priority_option = [1, 2, 3]
        self.priority_text.set('Select priority')
        self.priority_options = OptionMenu(
            self, self.priority_text, *self.priority_option)
        self.priority_options.grid(row=self.current_row, column=1)
        self.current_row += 1

        # Issue Severity selection menu
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

        # Button declaration
        self.worker_refresh = Button(
            self, text='Refresh', command=self.update_options)
        self.button = Button(self, text='Back',
                        command=lambda: controller.show_frame("issues_view"))
        self.button_save = Button(self, text='Insert issue',
                             command=self.send_query)

        # Button positioning
        self.button_save.grid(row=self.current_row, column=0)
        self.button.grid(row=self.current_row, column=1)
        self.worker_refresh.grid(row=self.current_row, column=2)
        self.current_row += 1

    def get_team_options(self):
        # Function to get the team names
        return team_names()

    def get_worker_options(self):
        # Function to get the worker names according to the tean
        return worker_names(self.team_text.get())

    def get_product_options(self):
        # Function to get the product names
        return product_names()

    def update_options(self):
        # FUnction to update the OptionMenus
        menu = self.team_options['menu']
        menu.delete(0, 'end')
        for value in team_names():
            menu.add_command(
                label=value, command=lambda v=value: self.team_text.set(v))

        menu = self.worker_options['menu']
        menu.delete(0, 'end')
        for value in worker_names(self.team_text.get()):
            menu.add_command(
                label=value, command=lambda v=value: self.worker_text.set(v))

        menu = self.product_options['menu']
        menu.delete(0, 'end')
        for value in product_names():
            menu.add_command(
                label=value, command=lambda v=value: self.product_text.set(v))

    def send_query(self):
        # Function to pass on the values required for issue insertion
        team = self.team_text.get()
        worker = self.worker_text.get()
        product = self.product_text.get()
        issue_type = self.issue_text.get()
        issue_desc = self.desc_text.get()
        issue_priority = self.priority_text.get()
        issue_severity = self.severity_text.get()
        response = insert_issue(team, worker, product, issue_type,
                                issue_desc, issue_priority, issue_severity)
        self.querystatus.configure(text=response)


def main():
    # Main function of the app
    window = Ticket_Management_System()
    window.wm_title("Ticket Managemnt System")
    window.mainloop()


if __name__ == "__main__":
    main()
