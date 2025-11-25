from tkinter import *
import customtkinter as ctk
from tkinter import messagebox, ttk
from backend_menu import MenuCreation  
from datetime import datetime

menu = MenuCreation()

class MenuGui:
    def __init__(self, root):
        self.root = root

        # Main frames
        self.header_frame = Frame(self.root)
        self.header_frame.pack(fill= X, anchor= "n", pady= 10, padx= 25)

        self.form_frame = Frame(self.root)
        self.form_frame.pack(side=LEFT, anchor="n", padx=25)

        Label(self.header_frame, text="Menu Management", font=("Times", 30, "bold")).pack(side=LEFT)

        current_date = datetime.now().strftime("%A, %d %B %Y")
        current_time = datetime.now().strftime("%I:%M %p")

        Label(self.header_frame, text=current_time, font=("Times", 12)).pack(side=RIGHT, padx=(0, 20))
        Label(self.header_frame, text=current_date, font=("Times", 12)).pack(side=RIGHT, padx=15)

        # Form Section
        Label(self.form_frame, text="Dish name:", font=("Times", 12)).pack(anchor="w")
        self.name_entry = ctk.CTkEntry(self.form_frame,placeholder_text="Enter name...", width=260)  
        self.name_entry.pack(anchor="n", pady=(0, 25))

        Label(self.form_frame, text="Description:", font=("Times", 9)).pack(anchor="w")
        self.desc_entry = ctk.CTkTextbox(self.form_frame, width= 260,height= 100, corner_radius= 3,
                                          border_width= 2)
        self.desc_entry.pack(anchor= "w", pady= (0, 25))

        Label(self.form_frame, text="Price:", font=("Times", 12)).pack(anchor="w")
        self.price_entry = ctk.CTkEntry(self.form_frame,placeholder_text="Enter price...", width=260)
        self.price_entry.pack(anchor="n", pady=(0, 25))

        
        Label(self.form_frame, text="Cuisine:", font=("Times", 12)).pack(anchor="w")
        cuisines = menu.get_cuisines()
        if isinstance(cuisines, str):
            messagebox.showerror("Error", cuisines)
            cuisine_names = ["No cuisines available"]   #placeholder  when no cuisines can be loaded
        else:
            cuisine_names = []
            for c in cuisines:
                cuisine_names.append(c[1])
        self.cuisine_combo = ttk.Combobox(self.form_frame, values=cuisine_names, width=27,state="readonly")
        self.cuisine_combo.pack(anchor="w", pady=5)

        # Category Dropdown
        Label(self.form_frame, text="Category:", font=("Times", 12)).pack(anchor="w")
        categories = menu.get_categories()
        if isinstance(categories, str):
            messagebox.showerror("Error", categories)
            cat_names = ["No Category availlable"]  
        else:
            cat_names = []
            for cat in categories:
                cat_names.append(cat[1])
        self.cat_combo = ttk.Combobox(self.form_frame, values=cat_names, width=27,state="readonly")
        self.cat_combo.pack(anchor="w", pady=5)

        Label(self.form_frame, text="Preparation Time (minutes):").pack(anchor="w", pady=5)
        self.prep_entry = ctk.CTkEntry(self.form_frame,placeholder_text="Enter prepartion time...", width=260)
        self.prep_entry.pack(anchor="w", pady=5)
    
        # Add and cancel btn
        self.btn1 = Button(self.form_frame, text="Add", width=10, command=self.add_meal)
        self.btn1.pack(side='left', padx=5, pady=20)
        self.btn2 = Button(self.form_frame, text="Cancel", width=10, command=self.clear_form)
        self.btn2.pack(side='right', padx=5, pady=20)

        # Top frame for Update and Delete buttons
        top_frame = Frame(self.root)
        top_frame.pack(pady=10, anchor='e')
        self.btn3 = Button(top_frame, text="Update", width=10, command=self.open_update_window)
        self.btn3.pack(side='left', padx=5)
        self.btn4 = Button(top_frame, text="Delete", width=10, command=self.delete_meal)
        self.btn4.pack(side='left', padx=5)


        # Filter by Category
        filter_frame = Frame(self.root)
        filter_frame.pack(pady=5, anchor='w', padx=10)
        Label(filter_frame, text="Filter by Category:").pack(side='left', padx=5)

        category_names_filter = ["All"]
        cat_ids = [None]

        if not isinstance(categories, str):
             for cat_id, cat_name in categories:
                category_names_filter.append(cat_name)
                cat_ids.append(cat_id)

        self.cat_combo_filter = ttk.Combobox(filter_frame, values=category_names_filter, state="readonly", width=20)
        self.cat_combo_filter.set("All")
        self.cat_combo_filter.pack(side='left', padx=5)
        self.cat_combo_filter.bind("<<ComboboxSelected>>", self.filter_menu)

        self.creatTableTree()

    def creatTableTree(self):
        
        self.table_frame = Frame(self.root)
        self.table_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=5, pady=10)

        # Tree view
        columns = ("ID", "Name", "Price", "Availability", "Preparation Time", "Category", "Cuisine")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", height=20)
        self.tree.pack(side=LEFT, fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        #Headings
        for col in columns:
            self.tree.heading(col, text=col)
            if col == "Name":
                self.tree.column(col, width=150, anchor="w")
            elif col == "Price" or col == "Availability":
                self.tree.column(col, width=100, anchor="center")
            else:
                self.tree.column(col, width=120, anchor="center")

        self.tree.tag_configure("description", foreground="gray", font=("Times", 10, "italic"), background="#d71010")
        self.tree.bind("<Double-1>", self.toggle_description)
        self.load_menu()
        

    def load_menu(self, course_id=None):
    # Clear existing rows
        for item in self.tree.get_children():
            self.tree.delete(item)

        meals = menu.display(course_id=course_id)
        if isinstance(meals, str):
            messagebox.showerror("Error", meals)
            return

        for meal in meals:
            meal_id, name, description, price, availability, prep_time, cuisine_name, category_name = meal
            avail_text = "Available" if availability else "Not Available"

            # Parent row (main info)
            parent_item = self.tree.insert(
                "", "end",
                iid=f"meal_{meal_id}",
                values=(meal_id, name, f"₱{price:.2f}", avail_text, f"{prep_time} mins", category_name, cuisine_name),
                open=False
            )

            # Child row for description (hidden initially)
            self.tree.insert(
                parent_item, "end",
                values=(description,),  # only description
                tags=("description",)
            )


    def toggle_description(self, event):
        # Get the clicked row
        row_id = self.tree.identify_row(event.y)
        if not row_id:
            return
            # Only toggle parent rows
        if self.tree.parent(row_id):
            row_id = self.tree.parent(row_id)
        is_open = self.tree.item(row_id, "open")
        self.tree.item(row_id, open=not is_open)

        # Filter
    def filter_menu(self, event=None):
        selected_category_name = self.cat_combo_filter.get()
        if selected_category_name == "All":
            selected_category_id = None
        else: 
            all_categories = menu.get_categories()
            selected_category_id = None
            
            for category in all_categories:
                if len(category) >= 2 and category[1] == selected_category_name:
                    selected_category_id = category[0]
                    break
    
        self.load_menu(selected_category_id)




    def add_meal(self):
        name = self.name_entry.get().strip()
        description = self.desc_entry.get("1.0", "end").strip() 
        price = self.price_entry.get().strip()
        cuisine_name = self.cuisine_combo.get()
        cat_name = self.cat_combo.get()
        avail = self.avail_combo.get()
        prep = self.prep_entry.get().strip()

        if not name or not price or not cuisine_name or not cat_name:
            messagebox.showerror("Error", "Name, Price, Cuisine, and Category are required.")
            return

        try:
            price = float(price)
            prep = int(prep) if prep else 0
            avail_bool = True
            # Get cuisine ID
            cuisines = menu.get_cuisines()
            cuisine_id = None
            for c in cuisines:
                if c[1] == cuisine_name:
                    cuisine_id = c[0]
                    break
            # Get category ID
            categories = menu.get_categories()
            cat_id = None
            for cat in categories:
                if cat[1] == cat_name:
                    cat_id = cat[0]
                    break
            if cuisine_id is None or cat_id is None:
                messagebox.showerror("Error", "Invalid cuisine or category.")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid price or prep time.")
            return

        result = menu.add_meal(name, description, price, cuisine_id, cat_id, avail_bool, prep)
        messagebox.showinfo("Result", result)
        self.load_menu()  
        self.clear_form()

    def open_update_window(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a meal to update.")
            return

        item_id = selected[0]
        parent_id = self.tree.parent(item_id)
        if parent_id:
            item_id = parent_id

        values = self.tree.item(item_id)['values']

        # Create popup window
        update_win = Toplevel(self.root)
        update_win.title("Update Meal")
        update_win.geometry("300x200")

        Label(update_win, text=f"Updating: {values[1]}", font=("Times", 14, "bold")).pack(pady=(10, 5))
        # Price
        Label(update_win, text="Price:").pack(anchor="w", padx=10, pady=(10,0))
        price_entry = ctk.CTkEntry(update_win, width=200)
        price_entry.pack(padx=10, pady=5)
        price_entry.insert(0, str(values[2]).replace("₱", ""))

        # Availability
        Label(update_win, text="Availability:").pack(anchor="w", padx=10, pady=(10,0))
        avail_combo = ttk.Combobox(update_win, values=["Available", "Not Available"], state="readonly", width=20)
        avail_combo.pack(padx=10, pady=5)
        avail_combo.set(values[3])

        # Save button
        def save_update():
            new_price = price_entry.get().strip()
            new_avail = avail_combo.get()
            if not new_price:
                messagebox.showerror("Error", "Price is required.")
                return
            try:
                new_price = float(new_price)
                avail_bool = new_avail == "Available"
            except ValueError:
                messagebox.showerror("Error", "Invalid price.")
                return

            # Call backend update
            result = menu.update(values[0], new_price, avail_bool)
            messagebox.showinfo("Result", result)
            update_win.destroy()  # close the popup
        self.load_menu()
        Button(update_win, text="Save", width=10, command=save_update).pack(pady=15)



    def delete_meal(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a meal to delete.")
            return

        item = self.tree.item(selected[0])
        meal_id = item['values'][0]

        if messagebox.askyesno("Confirm", f"Delete meal ID {meal_id}?"):
            result = menu.delete(meal_id)
            messagebox.showinfo("Result", result)
            self.load_menu()



    def clear_form(self):
    # Clear CTkEntry fields
        self.name_entry.delete(0, END)
        self.price_entry.delete(0, END)
        self.prep_entry.delete(0, END)
        
        # Clear CTkTextbox
        self.desc_entry.delete("1.0", "end")
        
        # Reset comboboxes
        self.cuisine_combo.set("")
        self.cat_combo.set("")
        
       