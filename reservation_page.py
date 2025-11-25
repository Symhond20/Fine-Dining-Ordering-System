from tkinter import *
from datetime import datetime
import customtkinter as ctk
from tkinter import ttk

ctk.set_appearance_mode("light")

class ReservationPage:
    def __init__(self, root):
        self.root = root

        # Main Frames
        self.page_header_frame = Frame(self.root)
        self.page_header_frame.pack(fill= X, anchor= "n", pady= 10, padx= 25)

        self.form_frame = Frame(self.root)
        self.form_frame.pack(side= LEFT, anchor= "n", padx= 25)

        self.table_view_frame = Frame(self.root)
        self.table_view_frame.pack(side= LEFT, anchor= "n", padx= 10)

        self.reservation_view_frame = Frame(self.root)
        self.reservation_view_frame.pack(side= LEFT, anchor= "n", padx= 10)

        # Sub Frames
        self.table_header = Frame(self.table_view_frame)
        self.table_header.pack(fill= X, anchor= "e")

        self.table_frame = Frame(self.table_view_frame)
        self.table_frame.pack()

        self.order_frame = Frame(self.table_view_frame, width= 440, height= 700, bg= "white",
                                 highlightbackground= "gray", highlightthickness= 2)
        self.order_frame.pack_propagate(False)
        self.order_frame.pack(anchor= "w", pady= 30)

        self.reservation_header = Frame(self.reservation_view_frame)
        self.reservation_header.pack(fill= X, anchor= "e")

        self.reservation_frame = Frame(self.reservation_view_frame)
        self.reservation_frame.pack()

        # Contents
        Label(self.page_header_frame, text= "Make a Reservation", font= ("Times", 27, "bold")).pack(side= LEFT)

        # Gets the current date
        date_today = datetime.now().strftime("%A, %d %B %Y")
        time_todaye = datetime.now().strftime("%I:%M %p")

        Label(self.page_header_frame, text= date_today, font= ("Times", 12)).pack(anchor= "e")
        Label(self.page_header_frame, text= time_todaye, font= ("Times", 11)).pack(anchor= "e")

        # Form Section
        Label(self.form_frame, text= "Full Name:", font= ("Times", 11)).pack(anchor= "w")
        self.name_entry = ctk.CTkEntry(self.form_frame, width= 260, corner_radius= 3)
        self.name_entry.pack(anchor= "w", pady= (0, 25))

        Label(self.form_frame, text= "Contact Number:", font= ("Times", 11)).pack(anchor= "w")
        self.contact_entry = ctk.CTkEntry(self.form_frame, width= 260, corner_radius= 3)
        self.contact_entry.pack(anchor= "w", pady= (0, 25))

        Label(self.form_frame, text= "Selected Date:", font= ("Times", 11)).pack(anchor= "w")
        self.date_entry = ctk.CTkEntry(self.form_frame, width= 260, corner_radius= 3)
        self.date_entry.pack(anchor= "w", pady= (0, 25))

        Label(self.form_frame, text= "Selected Time:", font= ("Times", 11)).pack(anchor= "w")
        self.time_entry = ctk.CTkEntry(self.form_frame, width= 260, corner_radius= 3)
        self.time_entry.pack(anchor= "w", pady= (0, 25))

        Label(self.form_frame, text= "Guest Count:", font= ("Times", 11)).pack(anchor= "w")
        self.guest_count_entry = ctk.CTkEntry(self.form_frame, width= 260, corner_radius= 3)
        self.guest_count_entry.pack(anchor= "w", pady= (0, 25))

        Label(self.form_frame, text= "Special Instructions:", font= ("Times", 11)).pack(anchor= "w")
        self.notes_entry = ctk.CTkTextbox(self.form_frame, width= 260, corner_radius= 3,
                                          border_width= 2)
        self.notes_entry.pack(anchor= "w", pady= (0, 25))

        self.cancel_btn = Button(self.form_frame, text= "Cancel",
                                 relief= RIDGE, height= 2, width= 20,
                                 command= self.clearForm)
        self.cancel_btn.pack(anchor= "w")

        # Calls the Table View
        Label(self.table_header, text= "Selected Table:", font= ("Times", 11)).pack(side= LEFT, anchor= "w", pady= (0, 5))
        self.table_entry = ctk.CTkEntry(self.table_header, width= 40, corner_radius= 3)
        self.table_entry.pack(side= LEFT, anchor= "w", pady= (0, 7), padx= 10)

        self.creatTableTree(self.table_frame)

        # Table buttons
        self.all_btn = Button(self.table_header, text= "All Tables",
                              relief= RIDGE, height= 1, width= 10)
        self.all_btn.pack(side= RIGHT, pady= (0, 5), padx= (10, 15))

        self.filtered_btn = Button(self.table_header, text= "Match Tables", 
                                   relief= RIDGE, height= 1, width= 10)
        self.filtered_btn.pack(side= RIGHT, pady= (0, 5), padx= 10)

        self.add_icon = PhotoImage(file="icons/add.png")

        # Advanced Order Button
        Label(self.order_frame, text= "Advanced Order", font= ("Times", 12), bg= "white").pack(pady= 10)
        self.advanced_order_btn = Button(self.order_frame, image= self.add_icon, text= "Advanced Order", 
                                         relief= RIDGE,
                                         compound= "left", padx= 5, pady= 5,
                                         command= self.orderWindow)
        self.advanced_order_btn.pack(side= BOTTOM, anchor= "e", padx= 10, pady= 10)
        
        # Advanced Order Items
        self.order_summary = None
        self.view_order_mode = False

        # Calls the Reservation view
        Label(self.reservation_header, text= "Reservation Made Today", font= ("Times", 12)).pack(anchor= "w", pady= (0, 12))
        self.createReservationTree(self.reservation_frame)

        self.add_btn = Button(self.reservation_view_frame, text= "Add Reservation",
                              relief= RIDGE, height= 2, width= 20)
        self.add_btn.pack(anchor= "e", pady= (25, 0))

    def orderWindow(self):
        self.order_window = Toplevel(self.root)
        self.order_window.geometry("400x300")
        self.order_window.title("Advanced Order")
    
    def clearForm(self):
        self.name_entry.delete(0, END)
        self.contact_entry.delete(0, END)
        self.date_entry.delete(0, END)
        self.time_entry.delete(0, END)
        self.guest_count_entry.delete(0, END)
        self.notes_entry.delete("1.0", END)
    
    def creatTableTree(self, parent):
        self.table_tree = ttk.Treeview(parent, columns= ("Capacity", "Status", "Time"), show= "tree headings", height= 20)
        self.table_tree.heading("#0", text= "Table Number")
        self.table_tree.heading("Capacity", text= "Capacity")
        self.table_tree.heading("Status", text= "Status")
        self.table_tree.heading("Time", text= "Time")

        self.table_tree.column("#0", width= 100)
        self.table_tree.column("Capacity", width= 100)
        self.table_tree.column("Status", width= 100)
        self.table_tree.column("Time", width= 130)
        self.table_tree.pack(side= LEFT, fill= BOTH, expand= TRUE)

        scrollbar = ttk.Scrollbar(parent, orient= "vertical", command= self.table_tree.yview)
        self.table_tree.config(yscrollcommand= scrollbar.set)
        scrollbar.pack(side= RIGHT, fill= Y)     

    def createReservationTree(self, parent):
        self.reservation_tree = ttk.Treeview(parent, columns= ("Table Number", "Capacity", "Status"), show= "tree headings", height= 27) 
        self.reservation_tree.heading("#0", text= "Time")
        self.reservation_tree.heading("Table Number", text= "Table Number")
        self.reservation_tree.heading("Capacity", text= "Capacity")
        self.reservation_tree.heading("Status", text= "Status")

        self.reservation_tree.column("#0", width= 140)
        self.reservation_tree.column("Table Number", width= 120)
        self.reservation_tree.column("Capacity", width= 100)
        self.reservation_tree.column("Status", width= 140)
        self.reservation_tree.pack(side= LEFT, fill= BOTH, expand= TRUE)

        scrollbar = ttk.Scrollbar(parent, orient= "vertical", command= self.reservation_tree.yview)
        self.reservation_tree.config(yscrollcommand= scrollbar.set)
        scrollbar.pack(side= RIGHT, fill= Y)     
