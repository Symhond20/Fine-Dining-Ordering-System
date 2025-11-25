from tkinter import *
from datetime import datetime
import customtkinter as ctk
from tkinter import ttk, messagebox
from backend_reservation import TableManager, ReservationManager

ctk.set_appearance_mode("light")

class ReservationPage:
    def __init__(self, root):
        self.root = root
        self.table_manager = TableManager()
        self.reservation_manager = ReservationManager()
        
        # Main Frames
        self.page_header_frame = Frame(self.root, bg=  "#3c5070")
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

        self.order_frame = Frame(self.table_view_frame, width= 440, height= 700, bg= "white", highlightbackground= "gray", highlightthickness= 2)
        self.order_frame.pack_propagate(False)
        self.order_frame.pack(anchor= "w", pady= 30)

        self.reservation_header = Frame(self.reservation_view_frame)
        self.reservation_header.pack(fill= X, anchor= "e")

        self.reservation_frame = Frame(self.reservation_view_frame)
        self.reservation_frame.pack()

        # Contents
        Label(self.page_header_frame, text= "Make a Reservation", font= ("Times", 27, "bold"), bg=  "#3c5070", fg= "#f5f0e9").pack(side= LEFT)

        # Gets the current date
        date_today = datetime.now().strftime("%A, %d %B %Y")
        time_todaye = datetime.now().strftime("%I:%M %p")

        Label(self.page_header_frame, text= date_today, font= ("Times", 12), bg=  "#3c5070", fg= "#f5f0e9").pack(anchor= "e")
        Label(self.page_header_frame, text= time_todaye, font= ("Times", 11), bg=  "#3c5070", fg= "#f5f0e9").pack(anchor= "e")

        # Form Section
        Label(self.form_frame, text= "Full Name:", font= ("Times", 11)).pack(anchor= "w")
        self.name_entry = ctk.CTkEntry(self.form_frame, width= 260, corner_radius= 3)
        self.name_entry.pack(anchor= "w", pady= (0, 25))

        Label(self.form_frame, text= "Contact Number:", font= ("Times", 11)).pack(anchor= "w")
        self.contact_entry = ctk.CTkEntry(self.form_frame, width= 260, corner_radius= 3)
        self.contact_entry.pack(anchor= "w", pady= (0, 25))

        Label(self.form_frame, text= "Selected Date (YYYY-MM-DD):", font= ("Times", 11)).pack(anchor= "w")
        self.date_entry = ctk.CTkEntry(self.form_frame, width= 260, corner_radius= 3)
        self.date_entry.pack(anchor= "w", pady= (0, 25))

        Label(self.form_frame, text= "Selected Time (HH:MM AM/PM):", font= ("Times", 11)).pack(anchor= "w")
        self.time_entry = ctk.CTkEntry(self.form_frame, width= 260, corner_radius= 3)
        self.time_entry.pack(anchor= "w", pady= (0, 25))

        Label(self.form_frame, text= "Guest Count:", font= ("Times", 11)).pack(anchor= "w")
        self.guest_count_entry = ctk.CTkEntry(self.form_frame, width= 260, corner_radius= 3)
        self.guest_count_entry.pack(anchor= "w", pady= (0, 25))

        Label(self.form_frame, text= "Special Instructions:", font= ("Times", 11)).pack(anchor= "w")
        self.notes_entry = ctk.CTkTextbox(self.form_frame, width= 260, corner_radius= 3,  border_width= 2)
        self.notes_entry.pack(anchor= "w", pady= (0, 25))

        self.cancel_btn = Button(self.form_frame, text= "Cancel", height= 1, width= 20, relief= RIDGE, command= self.clearForm)
        self.cancel_btn.pack(anchor= "w")

        Label(self.table_header, text= "Selected Table:", font= ("Times", 11)).pack(side= LEFT, anchor= "w", pady= (0, 5))
        self.table_entry = ctk.CTkEntry(self.table_header, width= 40, corner_radius= 3)
        self.table_entry.pack(side= LEFT, anchor= "w", pady= (0, 7), padx= 10)

         # Calls the Table View
        self.creatTableTree(self.table_frame)

        # Table frame buttons
        self.all_btn = Button(self.table_header, text= "Show Tables", height= 1, width= 10, relief= RAISED, command= self.showAll)
        self.all_btn.pack(side= RIGHT, pady= (0, 5), padx= (10, 15))

        self.filtered_btn = Button(self.table_header, text= "Filter Tables", height= 1, width= 10, relief= RAISED, command= self.showFiltered)
        self.filtered_btn.pack(side= RIGHT, pady= (0, 5), padx= 10)

        self.add_icon = PhotoImage(file="icons/add.png")

        # Advanced Order Button
        Label(self.order_frame, text= "Advanced Order", font= ("Times", 12), bg= "white").pack(pady= 10)
        self.advanced_order_btn = Button(self.order_frame, image= self.add_icon, text= "Advanced Order", relief= RAISED, compound= "left", padx= 5, pady= 5,
                                         command= self.orderWindow)
        self.advanced_order_btn.pack(side= BOTTOM, anchor= "e", padx= 10, pady= 10)
        
        # Advanced Order Items
        self.order_summary = None
        self.view_order_mode = False

        Label(self.reservation_header, text= "Reservation Made Today", font= ("Times", 12)).pack(anchor= "w", pady= (0, 12))
        
        # Calls the Reservation view
        self.createReservationTree(self.reservation_frame)

        self.table_tree.bind("<<TreeviewSelect>>", self.selectedRow)

        self.add_btn = Button(self.reservation_view_frame, text= "Add Reservation", height= 1, width= 20, relief= RAISED, command= self.submitReservation)
        self.add_btn.pack(anchor= "e", pady= (25, 0))

        # Uses the curreny date
        self.showAll()
        self.showCurrentReservations()

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

        self.table_tree.column("#0", width= 140)
        self.table_tree.column("Capacity", width= 90)
        self.table_tree.column("Status", width= 90)
        self.table_tree.column("Time", width= 100, anchor= "center")
        self.table_tree.pack(side= LEFT, fill= BOTH, expand= TRUE)

        scrollbar = ttk.Scrollbar(parent, orient= "vertical", command= self.table_tree.yview)
        self.table_tree.config(yscrollcommand= scrollbar.set)
        scrollbar.pack(side= RIGHT, fill= Y)     

    def createReservationTree(self, parent):
        self.reservation_tree = ttk.Treeview(parent, columns= ("Selected Time", "Table Number", "Guest Count", "Reservation Status"), show= "headings", height= 27) 
        self.reservation_tree.heading("Selected Time", text= "Selected Time")
        self.reservation_tree.heading("Table Number", text= "Table Number")
        self.reservation_tree.heading("Guest Count", text= "Guest Count")
        self.reservation_tree.heading("Reservation Status", text= "Reservation Status")

        self.reservation_tree.column("Selected Time", width= 140, anchor= "center")
        self.reservation_tree.column("Table Number", width= 120, anchor= "center")
        self.reservation_tree.column("Guest Count", width= 100, anchor= "center")
        self.reservation_tree.column("Reservation Status", width= 140, anchor= "center")
        self.reservation_tree.pack(side= LEFT, fill= BOTH, expand= TRUE, anchor= "center")

        scrollbar = ttk.Scrollbar(parent, orient= "vertical", command= self.reservation_tree.yview)
        self.reservation_tree.config(yscrollcommand= scrollbar.set)
        scrollbar.pack(side= RIGHT, fill= Y)     

    def selectedRow(self, event):
        selected_data = self.table_tree.selection()
        if not selected_data:
            return
        
        item = selected_data[0]

        for child in self.table_tree.get_children():
            if child != selected_data:
                self.table_tree.item(child, open= FALSE)
        
        if self.table_tree.get_children(item):
            self.table_tree.item(item, open= TRUE)
            table_number = self.table_tree.item(item, "text")
            self.table_entry.configure(state= "normal")
            self.table_entry.delete(0, 'end')
            self.table_entry.insert(0, table_number)
            self.table_entry.configure(state= "readonly")
        else:
            self.table_tree.selection_remove(item)

    def showAll(self, date=None):
        for item in self.table_tree.get_children():
            self.table_tree.delete(item)

        if date is None:
            formatted_date = datetime.now().strftime("%Y-%m-%d")
            view = self.table_manager.viewAll(formatted_date)
        else:
            view = self.table_manager.viewAll(date)
        
        for id, table_number, capacity, status, time, description in view:
            if time:
                try:
                    formatted_time = datetime.strptime(str(time), "%H:%M:%S")
                    display_time = formatted_time.strftime("%I:%M %p").lstrip("0")
                except Exception:
                    display_time = str(time)
            else:
                display_time = "-"
            
            status_display = "reserved" if time else "available"
            parent = self.table_tree.insert("", END, iid= str(id), text= table_number, values= (capacity, status_display, display_time))
            self.table_tree.insert(parent, END, text= description, values= ("","",""))

    def showFiltered(self):
        try:
            date = self.date_entry.get().strip()
            guest = self.guest_count_entry.get()
            
            if not date and not guest:
                messagebox.showwarning("No Input Error", "Please enter date and guest count.")
                return
            if not guest:
                messagebox.showwarning("Input Error", "Please enter guest count (number).")
                return
            if not date:
                messagebox.showwarning("Input Error", "Please enter a date.")
                return
         
            guest_count_int = int(guest)
            if guest_count_int <= 0:
                messagebox.showwarning("Input Error", "Please enter valid input guest count (no zero and negative number).")
                return
            datetime.strptime(date, "%Y-%m-%d")
                
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter valid date format (YYYY-MM-DD) and guest count (number)")
            return
        
        for item in self.table_tree.get_children():
            self.table_tree.delete(item)

        filtered_data = self.table_manager.viewFilteredTable(date, guest_count_int)

        for table_id, table_num, capacity, description, status, time in filtered_data:
            if time:
                try:
                    formatted_time = datetime.strptime(str(time), "%H:%M:%S")
                    display_time = formatted_time.strftime("%I:%M %p").lstrip("0")
                except Exception:
                    display_time = str(time)
            else:
                display_time = "-"

            status_display = "reserved" if time else "available"
            parent = self.table_tree.insert("", "end", iid= str(table_id), text= table_num, values= (capacity, status_display, display_time))
            self.table_tree.insert(parent, "end", text= f" Description: {description}", values= ("", "", ""))

    def submitReservation(self):
        name = self.name_entry.get().title() 
        contact = self.contact_entry.get()
        date = self.date_entry.get()
        time = self.time_entry.get()
        guest_count = self.guest_count_entry.get()
        notes = self.notes_entry.get("1.0", "end").strip()
        table_number = self.table_entry.get()

        if not name or not contact or not date or not time or not guest_count or not table_number:
            messagebox.showwarning("Input Error", "Please fill up required entries.")
            return
        try:
            guest_count_int = int(guest_count)
            if guest_count_int <= 0:
                messagebox.showwarning("Input Error", "Please enter valid input guest count (no zero and negative number).")
                return
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter valid guest count.")
            return

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Invalid Date Format", "Plaese enter a valid date format YYYY-MM-DD.") 
            return
        
        try:
            datetime.strptime(time, "%H:%M %p")
        except ValueError:
            messagebox.showwarning("Invalid Time Format", "Plaese enter a valid time format HH:MM AM/PM.") 
            return
        
        result = self.reservation_manager.addReservation(name, contact, date, time, guest_count, notes, table_number)

        if result == "success":
            messagebox.showinfo("Success", "Reservation is successfully added.")
            self.table_tree.selection_remove(self.table_tree.selection())
            self.clearForm()
            self.showAll()
            self.showCurrentReservations()
        elif result == 'empty_fields':
            messagebox.showwarning("Input Error", "Fill in all required fields.")
        elif result == "already_exists":
            messagebox.showerror('Duplicate Error', "A reservtion with the same details already exists.")
        else:
            messagebox.showerror("Error", "An unexpected error occurred.")
        
    def showCurrentReservations(self):
        for item in self.reservation_tree.get_children():
            self.reservation_tree.delete(item)

        reservations = self.reservation_manager.viewAll()

        for time, table_num, guest_count, status  in reservations:
            if time:
                try:
                    formatted_time = datetime.strptime(str(time), "%H:%M:%S")
                    display_time = formatted_time.strftime("%I:%M %p").lstrip("0")
                except Exception:
                    display_time = str(time)
            else:
                display_time = "N/A"
            
            self.reservation_tree.insert("", "end", values=(display_time, table_num, guest_count, status))