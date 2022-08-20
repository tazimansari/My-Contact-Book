from tkinter import *
from tkinter.ttk import *
from sqlite3 import *
from tkinter import messagebox
from tkinter import filedialog

class ManageContactsFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.style = Style()

        self.style.configure('TFrame', background = 'white')

        self.pack(side = TOP, fill = BOTH, expand = TRUE)

        self.con = connect('mycontacts.db')
        self.cur = self.con.cursor()
        self.photo_path = ""

        self.create_view_all_contacts_frame()

    def create_view_all_contacts_frame(self):
        self.view_all_contacts_frame = Frame(self)
        self.view_all_contacts_frame.place(relx=.5,rely=.5,anchor=CENTER)

        self.style.configure('TButton', font=(NONE, 15), width=20)

        self.add_new_contact_button = Button(self.view_all_contacts_frame,
        text="Add New Contact", command=self.add_new_contact_button_click)
        self.add_new_contact_button.grid(row=0, column=0, columnspan=2,
        sticky=E, pady=50)

        self.style.configure('TLabel', background='white', font=(NONE, 15))

        self.name_label = Label(self.view_all_contacts_frame,
        text = "Name:", width = 7)
        self.name_label.grid(row=1,column=0,pady=10,sticky=W)

        self.name_entry = Entry(self.view_all_contacts_frame,
        font = (NONE, 15), width = 65)
        self.name_entry.grid(row=1,column=1,sticky=W)
        self.name_entry.bind('<KeyRelease>', self.name_entry_key_released)

        self.style.configure('Treeview', font = (NONE, 14), rowheight = 25)
        self.style.configure('Treeview.Heading', font=(NONE, 15))

        self.contacts_treeview = Treeview(self.view_all_contacts_frame,
        columns=('name','phone_no','email_id','city'),show='headings')
        self.contacts_treeview.heading('name', text = "Name", anchor = W)
        self.contacts_treeview.heading('phone_no', text="Phone No", anchor = W)
        self.contacts_treeview.heading('email_id', text="Email Id", anchor = W)
        self.contacts_treeview.heading('city', text="City", anchor = W)
        self.contacts_treeview.column('name', width = 250)
        self.contacts_treeview.column('phone_no', width=200)
        self.contacts_treeview.column('email_id', width=250)
        self.contacts_treeview.column('city', width=100)
        self.contacts_treeview.grid(row=2,column=0,columnspan=2,pady=10)
        self.contacts_treeview.bind('<<TreeviewSelect>>',
        self.contacts_treeview_selection)

        self.cur.execute("select * from Contact")
        self.fill_contacts_treeview()

    def fill_contacts_treeview(self):
        for contact in self.contacts_treeview.get_children():
            self.contacts_treeview.delete(contact)

        contacts = self.cur.fetchall()
        for contact in contacts:
            self.contacts_treeview.insert("", END, values=contact)

    def name_entry_key_released(self, event):
        self.cur.execute("select * from Contact where name like ?", ('%' + self.name_entry.get() + '%',))
        self.fill_contacts_treeview()

    def contacts_treeview_selection(self, event):
        contact = self.contacts_treeview.item(
            self.contacts_treeview.selection()
        )['values']

        self.view_all_contacts_frame.destroy()
        self.create_update_delete_contact_frame(contact)

    def create_add_new_contact_frame(self):
        self.add_new_contact_frame = Frame(self)
        self.add_new_contact_frame.place(relx=.5, rely=.5, anchor=CENTER)

        self.style.configure('TLabel', background='white', font=(NONE, 15))

        self.name_label = Label(self.add_new_contact_frame, text="Name:")
        self.name_label.grid(row=0, column=0, sticky=W)

        self.name_entry = Entry(self.add_new_contact_frame,
        font=(NONE, 15), width=20)
        self.name_entry.grid(row=0, column=1, pady=10)

        self.phone_no_label = Label(self.add_new_contact_frame, text="Phone No:")
        self.phone_no_label.grid(row=1, column=0, sticky=W)

        self.phone_no_entry = Entry(self.add_new_contact_frame,
        font=(NONE, 15), width=20)
        self.phone_no_entry.grid(row=1, column=1, pady=10)

        self.email_id_label = Label(self.add_new_contact_frame, text="Email Id:")
        self.email_id_label.grid(row=2, column=0, sticky=W)

        self.email_id_entry = Entry(self.add_new_contact_frame,
        font=(NONE, 15), width=20)
        self.email_id_entry.grid(row=2, column=1, pady=10)

        self.city_label = Label(self.add_new_contact_frame, text="City:")
        self.city_label.grid(row=3, column=0, sticky=W)

        self.city_combobox = Combobox(self.add_new_contact_frame, font=(NONE, 15),
        width=18, values=('Greater Noida','Noida','Delhi','Gurgaon','Mumbai'),
        state='readonly')
        self.city_combobox.grid(row=3, column=1, pady=10)
        self.city_combobox.current(0)

        self.style.configure('TButton', font=(NONE, 15), width=20)

        self.add_button = Button(self.add_new_contact_frame, text="Add",
        command=self.add_button_click)
        self.add_button.grid(row=5, column=1, pady=10)

    def create_update_delete_contact_frame(self, contact):
        self.update_delete_contact_frame = Frame(self)
        self.update_delete_contact_frame.place(relx=.5, rely=.5, anchor=CENTER)

        self.style.configure('TLabel', background='white', font=(NONE, 15))

        self.name_label = Label(self.update_delete_contact_frame, text="Name:")
        self.name_label.grid(row=2, column=0, sticky=W)

        self.name_entry = Entry(self.update_delete_contact_frame, font=(NONE, 15),
        width=20)
        self.name_entry.grid(row=2, column=1, pady=10)
        self.name_entry.insert(END, contact[0])

        self.phone_no_label = Label(self.update_delete_contact_frame, text="Phone No:")
        self.phone_no_label.grid(row=3, column=0, sticky=W)

        self.phone_no_entry = Entry(self.update_delete_contact_frame, font=(NONE, 15),
        width=20)
        self.phone_no_entry.grid(row=3, column=1, pady=10)
        self.phone_no_entry.insert(END, contact[1])

        self.email_id_label = Label(self.update_delete_contact_frame, text="Email Id:")
        self.email_id_label.grid(row=4, column=0, sticky=W)

        self.email_id_entry = Entry(self.update_delete_contact_frame,
        font=(NONE, 15), width=20)
        self.email_id_entry.grid(row=4, column=1, pady=10)
        self.email_id_entry.insert(END, contact[2])
        self.old_email_id = contact[2]

        self.city_label = Label(self.update_delete_contact_frame,text="City:")
        self.city_label.grid(row=5, column=0, sticky=W)

        self.city_combobox = Combobox(self.update_delete_contact_frame, font=(NONE, 15),
        width=19, values=('Greater Noida', 'Noida', 'Delhi', 'Gurgaon', 'Mumbai'),
        state='readonly')
        self.city_combobox.grid(row=5, column=1, pady=10)
        self.city_combobox.set(contact[3])

        self.style.configure('TButton', font=(NONE, 15), width=20)

        self.update_button = Button(self.update_delete_contact_frame,
        text="Update", command = self.update_button_click)
        self.update_button.grid(row=6, column=1, pady=10)

        self.delete_button = Button(self.update_delete_contact_frame,
        text="Delete", command = self.delete_button_click)
        self.delete_button.grid(row=7, column=1, pady=10)

    def add_new_contact_button_click(self):
        self.view_all_contacts_frame.destroy()
        self.create_add_new_contact_frame()

    def add_button_click(self):
        self.cur.execute("select * from Contact where EmailId = ?", (self.email_id_entry.get(),))
        record = self.cur.fetchone()
        if record is None:
            self.cur.execute("insert into Contact values(?, ?, ?, ?)",
               (self.name_entry.get(),
                self.phone_no_entry.get(),
                self.email_id_entry.get(),
                self.city_combobox.get()))
            self.con.commit()
            messagebox.showinfo('Success Message',
            'Contact details are added successfully')
            self.add_new_contact_frame.destroy()
            self.create_view_all_contacts_frame()
        else:
            messagebox.showerror('Error Message',
            "User of email id" + self.email_id_entry.get() + " is already added")

    def update_button_click(self):
        self.cur.execute("update Contact set Name = ?, PhoneNo = ?, EmailId = ?, City = ? where EmailId = ?",
        (self.name_entry.get(), self.phone_no_entry.get(),
        self.email_id_entry.get(), self.city_combobox.get(), self.old_email_id))
        self.con.commit()
        messagebox.showinfo('Success Message', 'Contact details are updated successfully')
        self.update_delete_contact_frame.destroy()
        self.create_view_all_contacts_frame()

    def delete_button_click(self):
        if messagebox.askquestion('Confirmation Message',
        'Are you sure to delete?') == 'yes':
            self.cur.execute("delete from Contact where EmailId = ?",
            (self.old_email_id,))
            self.con.commit()
            messagebox.showinfo('Success Message',
            'Contact details are deleted successfully')
        self.update_delete_contact_frame.destroy()
        self.create_view_all_contacts_frame()
