from tkinter import * 
from reservation_page import ReservationPage
from menu_gui import MenuGui

window = Tk()
window.geometry("1700x800")
window.title("Restaurant Ordering System")

class SidebarMenu:
    def __init__(self, root):
        self.root = root
        
        # Loads Icon: handles the error
        try:
            self.dashboard_icon = PhotoImage(file="icons/dashboard.png")
            self.order_icon = PhotoImage(file="icons/order.png")
            self.reservation_icon = PhotoImage(file="icons/reservation.png")
            self.report_icon = PhotoImage(file="icons/report.png")
            self.foodMenu_icon = PhotoImage(file="icons/menu-food.png")
            self.logout_icon = PhotoImage(file="icons/logout.png")
        except Exception as e:
            print(f"Warning: Icon loading failed: {e}")
            self.dashboard_icon = None
            self.order_icon = None
            self.reservation_icon = None
            self.report_icon = None
            self.foodMenu_icon = None
            self.logout_icon = None

        # Main frames
        self.sidebar_frame = Frame(self.root, bg='#D9D9D9')
        self.sidebar_frame.pack(side= LEFT, fill= Y)

        self.page_frame = Frame(self.root, bg='#D9D9D9')
        self.page_frame.pack(side= LEFT, fill= Y, padx= 30, pady= 10, anchor= "center")

        #try:
            #HomePage(self.page_frame)
        #except Exception as e:
            #print(f"Error: Loading HomaPage: {e}")

        # Side bar buttons
        self.dashboard_btn = Button(self.sidebar_frame, image=self.dashboard_icon, text="Home Page", 
                                    font=('Helvetica', 10), bd= 0, bg="#DADADA",
                                    compound="left", anchor= "w", padx= 20,
                                    command=self.homePage)
        self.dashboard_btn.pack(fill=X, pady=(170, 50))

        self.customer_btn = Button(self.sidebar_frame, image=self.dashboard_icon, text="Customer", 
                                   font=('Helvetica', 10), bd= 0, bg="#DADADA",
                                   compound="left", anchor= "w", padx= 20,
                                   command=self.customerPage)
        self.customer_btn.pack(fill=X, pady=(0, 50))

        # Reservation buttons main frame
        self.reservation_btn_frame = Frame(self.sidebar_frame, bg="#DADADA")
        self.reservation_btn_frame.pack(fill=X, anchor="w")

        # Reservation subframe (hidden)
        self.reservation_btn_subframe = Frame(self.reservation_btn_frame, bg="#DADADA")

        self.reservation_btn = Button(self.reservation_btn_frame, image=self.reservation_icon, text="Reservation", 
                                      font=('Helvetica', 10), bd=0, bg="#DADADA",
                                      compound="left", anchor="w", padx=20, 
                                      command=self.reservationOnClick)
        self.reservation_btn.pack(fill=X, anchor= 'w')

        # Reservation button sub buttons (make and view reservation)
        self.make_reservation_btn = Button(self.reservation_btn_subframe, text="Make Reservation", 
                                           font=('Helvetica', 10), bd=0, bg="#DADADA",
                                           command=self.addReservationPage)
        self.make_reservation_btn.pack(fill=X, pady=(5, 10))

        self.view_reservation_btn = Button(self.reservation_btn_subframe, text="View Reservations", 
                                           font=('Helvetica', 10), bd=0, bg="#DADADA",
                                           command=self.viewReservationPage)  # Fixed typo: removed extra space
        self.view_reservation_btn.pack(fill=X, pady=(0, 20))

        # Order buttons main frame
        self.order_btn_frame = Frame(self.sidebar_frame, bg="#DADADA")
        self.order_btn_frame.pack(fill=X, anchor="w")

        # Order button subframe (hidden)
        self.order_btn_subframe = Frame(self.order_btn_frame, bg="#DADADA")

        self.order_btn = Button(self.order_btn_frame, image=self.order_icon, text="Order", 
                                font=('Helvetica', 10), bd=0, bg="#DADADA",
                                compound="left", anchor="w", padx= 20, 
                                command=self.orderOnClick)
        self.order_btn.pack(fill=X, anchor= "w", pady= (50, 0))

        # Order button sub buttons (view order and payment & billing)
        self.view_order_btn = Button(self.order_btn_subframe, text="View Orders", 
                                     font=('Helvetica', 10), bd=0, bg="#DADADA", 
                                     command= self.viewOrdersPage)
        self.view_order_btn.pack(fill=X, pady=(5, 10))

        self.billing_btn = Button(self.order_btn_subframe, text="Payment & Billing", 
                                  font=('Helvetica', 10), bd=0, bg="#DADADA",
                                  command= self.paymentPage)
        self.billing_btn.pack(fill=X, pady=(0, 10))
        
        # Continuation of sidebar buttons
        self.menu_btn = Button(self.sidebar_frame, image=self.foodMenu_icon, text="Menu", 
                               font=('Helvetica', 10), bd=0, bg="#DADADA",
                               compound= "left", anchor= "w", padx= 20, 
                               command=self.menuPage)
        self.menu_btn.pack(fill=X, pady= 50)

        report_btn = Button(self.sidebar_frame, image=self.report_icon, text="Report", 
                            font=('Helvetica', 10), bd=0, bg="#DADADA",
                            compound= "left", anchor= "w", padx= 20, 
                            command=self.reportPage)
        report_btn.pack(fill=X, pady=(0, 50))

    def homePage(self):
        for widgets in self.page_frame.winfo_children():
            widgets.destroy()

        #try:
            #HomePage(self.page_frame)
        #except Exception as e:
            #print(f"Error: Loading HomaPage: {e}")

    def customerPage(self):
        for widgets in self.page_frame.winfo_children():
            widgets.destroy()
        
        #try:
            #CustomerPage(self.page_frame)
        #except Exception as e:
            #print(f"Error: Loading HomaPage: {e}")

    def reservationOnClick(self):
        if self.order_btn_subframe.winfo_viewable():
            self.order_btn_subframe.pack_forget()
            self.order_btn.pack_configure(pady=(50, 0))
            self.menu_btn.pack_configure(pady=50)
        
        if self.reservation_btn_subframe.winfo_viewable():
            self.reservation_btn_subframe.pack_forget()
            self.order_btn.pack_configure(pady=(50, 0))
        else:
            self.reservation_btn_subframe.pack(fill=X, pady=(5, 0))
            self.order_btn.pack_configure(pady=0)
    
    def addReservationPage(self):
        for widgets in self.page_frame.winfo_children():
            widgets.destroy()
        try:
            ReservationPage(self.page_frame)
        except Exception as e:
            print(f"Error: Loading HomaPage: {e}")

    def viewReservationPage(self):
        for widgets in self.page_frame.winfo_children():
            widgets.destroy()

        #try:
            #ViewReservationPage(self.page_frame)
        #except Exception as e:
            #print(f"Error: Loading HomaPage: {e}")
    
    def orderOnClick(self):
        if self.reservation_btn_subframe.winfo_viewable():
            self.reservation_btn_subframe.pack_forget()
            self.order_btn.pack_configure(pady=(50, 0))
        
        if self.order_btn_subframe.winfo_viewable():
            self.order_btn_subframe.pack_forget()  
            self.order_btn.pack_configure(pady=(50, 0))
            self.menu_btn.pack_configure(pady=50)
        else:
            self.order_btn_subframe.pack(fill=X, pady=(5, 10))  
            self.menu_btn.pack_configure(pady=(0, 50))

    def viewOrdersPage(self):
        for widgets in self.page_frame.winfo_children():
            widgets.destroy()

        #try:
            #OrderPage(self.page_frame)
        #except Exception as e:
            #print(f"Error: Loading HomaPage: {e}")

    def paymentPage(self):
        for widgets in self.page_frame.winfo_children():
            widgets.destroy()

        Label(self.page_frame, text= "Payment & Billing").pack()

    def menuPage(self):
        for widgets in self.page_frame.winfo_children():
            widgets.destroy()

        try:
            MenuGui(self.page_frame)
        except Exception as e:
            print(f"Error: Loading HomePage: {e}")


    def reportPage(self):
        for widgets in self.page_frame.winfo_children():
            widgets.destroy()

        Label(self.page_frame, text= "Reports").pack()

sidebar = SidebarMenu(window)
window.mainloop()