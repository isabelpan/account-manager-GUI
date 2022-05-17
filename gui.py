from asyncore import file_dispatcher
from tkinter import *
from os import path
# from venv import create 
from PIL import ImageTk, Image
from tkinter import ttk 
import random 
import json
import csv 
import tkinter.messagebox
import time
from customer_classes import Customer

# open JSON file
file_handle = open('customers.json')

accounts = json.load(file_handle)

with open('customers.json') as fp:
    data = json.load(fp)

file_handle.close()


#  -------------------------------- LOGIN PAGE -------------------------------
def main():
    global name_entry, number_entry, login_button, error_lbl, name, number, logout_button, login_frame
    try: 
        account_frame.place_forget()
        createAccount_frame.place_forget()
        order_frame.place_forget()
        pastOrders_frame.place_forget()
        feedback_frame.place_forget()
    except NameError as e: 
        print(f'{e}')

    window.title('Mochi Fresh Account Login')
    window.config(menu = 0)

    login_frame.pack()
    login_frame.place(anchor='center', x = 350, y = 350)

    instruction_lbl = Label(login_frame, text = "Please login to view your loyalty points or to place an order!", bg = '#9CAF88', font = ('Acta Display', 18), fg = 'white')
    instruction_lbl.place(x = 10, y = 10)

    name = Label(login_frame, text = "Name", fg = 'white', bg = '#9CAF88', font = ('Acta Display',22))
    name.place(x = 30, y = 60)

    name = StringVar()
    name.set('')
    name_entry = Entry(login_frame, textvariable = name, justify = CENTER, width = 30, bg = '#b5bda5')
    name_entry.place(x=210, y= 60 )

    number = Label(login_frame, text = "Phone Number", fg = 'white', bg = '#9CAF88', font = ('Acta Display', 21))
    number.place(x = 30, y = 100)

    number = IntVar()
    number.set('')
    number_entry = Entry(login_frame, textvariable = number, justify = CENTER, width = 30, bg = '#b5bda5')
    number_entry.place(x=210, y = 100)
    number_entry.config(state = NORMAL)

    login_button = Button(login_frame, text = 'Login', font = ('Acta Display', 18, 'bold'), padx = 3, command = account_manager, width = 10, bg = 'white', fg = '#9CAF88', borderwidth=1)
    login_button.place(x = 353, y = 150)
    login_button.config(state = NORMAL)

    noAccount_lbl = Label(login_frame, text = "Don't have an account yet?", font = ('Acta Display', 12, 'bold'), bg = '#b5bda5', fg = 'white')
    noAccount_lbl.place(x = 10, y = 235)
    
    createAccount_button = Button(login_frame, text = 'Create a New Account', command = newAccount_form, font = ('Acta Display', 12, 'bold'), width = 16, bg = 'white', fg = '#9CAF88', borderwidth = 0, padx = 3)
    createAccount_button.place(x = 20, y = 265)

    error_lbl = Label(login_frame, text = '', font = ('Acta Display', 10), fg = 'white', bg ='#9CAF88')
    error_lbl.place(x = 30, y = 140)

# < "LOGIN" BUTTON >
def login_onclick(customerName):
    global error_lbl, customerNum

    customerName = str(name.get())
    try:
        customerNum = str(number.get())
    except TclError as e:
        number.set('')
        print(e)

    if customerNum not in accounts:
        error_lbl.config(text = "Customer info was not found. Please try again.")
        name.set("")
        number.set("")
    else:
        if accounts[customerName["Phone Number"]] == customerNum:
            account_manager(customerName)
        else: 
            error_lbl.config(text = "The name or number does not match our records. Please try again.")
            name.set("")
            number.set("")

# Account Manager Screen (after login)
def account_manager():
    global account_frame

    login_frame.place_forget()
    order_frame.place_forget()
    feedback_frame.place_forget()
    createAccount_frame.place_forget()
    pastOrders_frame.place_forget()
    account_frame.place_forget()

    window.title('Account Manager - Mochi Fresh')
    window.config(menu = menubar)
    
    account_frame.pack()
    account_frame.place(x = 350, y = 350, anchor = 'center')

    greeting_lbl = Label(account_frame, text = "Welcome!", font = ('Acta Display', 19, 'bold'), fg = 'white', bg = '#9CAF88')
    greeting_lbl.place(x = 200, y = 10)
    # greetingName_lbl = Label(account_frame, text = f"{accounts[customer]['Name']}", font = ('Acta Display', 19, 'bold'), fg = 'white', bg = '#b5bda5')
    # greetingName_lbl.place(x = 295, y = 10)

    createOrder_button = Button(account_frame, text = 'View Menu/Order Here', command = order_onclick, bg = '#b5bda5', fg = '#9CAF88', width = 18, height = 2, borderwidth = 1, font = ('Acta Display', 16, 'bold'))
    createOrder_button.place(x = 70, y = 380)
    
    pastOrder_button = Button(account_frame, text = 'View Past Orders', bg = '#E9CDD0', command = pastOrders_onclick, fg = '#9CAF88', width = 15, height = 2, borderwidth = 1, font = ('Acta Display', 16, 'bold'))
    pastOrder_button.place(x = 350, y = 380)

    # loyalty message
    loyalty_lbl = Label(account_frame, text = 'Mochi Fresh Loyalty Points', font = ('Acta Display', 16, 'underline'), fg = 'black', bg = '#b5bda5')
    loyalty_lbl.place(x = 25, y = 60)
    pts_lbl = Label(account_frame, text = '- $1 spent = 2 points\n- 100 points = 1 free drink', font = ('Acta Display', 14), padx = 12, pady = 5, justify = LEFT, fg = 'black', bg = '#b5bda5')
    pts_lbl.place(x = 25, y = 86)
    
    # drink of the day
    drinkOfDay_frame = Frame(account_frame, width = 280, height = 250, borderwidth = 1, relief = GROOVE, bg = '#e5bcbb')
    drinkOfDay_frame.place(x=300, y = 50)

    drinkOfDay_lbl = Label(drinkOfDay_frame, text = 'Drink of the Day', font = ('Acta Display', 18, 'bold'), bg = '#e5bcbb', fg = 'black')
    drinkOfDay_lbl.place(x = 72.5, y = 7)

    drinkOfDay = random.randint(1, 3)

    if drinkOfDay == 1:
        drink_lbl1 = Label(drinkOfDay_frame, text = 'Matcha Milk Tea', bg = '#E9CDD0', fg = 'black', font = ('Acta Display', 17, 'bold'))
        drink_lbl1.place(x = 80, y = 215)

        img = Image.open('matchaMilkTea.png')
        new_width = 110
        new_height = 170
        img101= img.resize((new_width, new_height), Image.ANTIALIAS)
        logo = ImageTk.PhotoImage(img101)
        logo_label = Label(drinkOfDay_frame, image = logo )
        logo_label.image = logo
        logo_label.place(x = 95, y = 35)

    elif drinkOfDay == 2:
        drink_lbl2 = Label(drinkOfDay_frame, text = 'Thai Milk Tea', bg = '#E9CDD0', fg = 'black', font = ('Acta Display', 17, 'bold'))
        drink_lbl2.place(x = 87, y = 215)

        img2 = Image.open('thaiMilkTea.png')
        new_width = 120
        new_height = 180
        img202 = img2.resize((new_width, new_height), Image.ANTIALIAS)
        logo = ImageTk.PhotoImage(img202)
        logo_label = Label(drinkOfDay_frame, image = logo)
        logo_label.image = logo
        logo_label.place(x = 87, y = 35)
    
    elif drinkOfDay == 3:
        drink_lbl3 = Label(drinkOfDay_frame, text = 'Brown Sugar Milk Tea', bg = '#E9CDD0', fg = 'black', font = ('Acta Display', 17, 'bold'))
        drink_lbl3.place(x = 55, y = 215)

        img3 = Image.open('brownSugarMilkTea.png')
        new_width = 120
        new_height = 180
        img303 = img3.resize((new_width, new_height), Image.ANTIALIAS)
        logo = ImageTk.PhotoImage(img303)
        logo_label = Label(drinkOfDay_frame, image = logo)
        logo_label.image = logo
        logo_label.place(x = 87, y = 35)

    def customer_points():
        global numOfPts, total, pts_progressbar

        numOfPts = accounts[customerName]["Points"]
        print(numOfPts)
        total = 100
        print(numOfPts)
    
        if numOfPts == 100:
            pts_progressbar = numOfPts/total
            print(f"You have {pts_progressbar}/100 points. Claim your free drink!")
        elif numOfPts > 0 + numOfPts < 100:
            pts_progressbar = numOfPts/total
            difference = total - numOfPts
            print(f"You currently have {pts_progressbar} points.\n{difference} points left before you can claim your free drink")

    progress_lbl = Label(account_frame, text = '42 / 100 points', fg = 'black', bg = '#9caf88', font = ('Acta Display', 16))
    progress_lbl.place(x = 80, y = 172)

    progress = ttk.Progressbar(account_frame, orient = 'horizontal', length = 200, max = 1, mode = 'indeterminate')
    progress.place(x = 20, y = 200)
    progress.step(customer_points)
    progress.pack(expand = True)

    

    

# Login > Account Manager
def pastOrders_onclick():
    # function that displays the orders upon clicking the button 
    def display_orders():
        global pastOrders
        pastOrders = list(filter(None, pastOrders))
        accounts[customerName]['Past Orders'] = pastOrders

        pastOrderString = ''.join(str(order) for order in pastOrders)

        if not path.isfile('pastOrders.csv'):
            with open('pastOrders.csv', 'w') as fp:
                data = csv.writer(fp)
                data.writerow(['Name', 'Phone Number', 'Past Orders'])

        with open('pastOrders.csv', 'a') as fp:
            data = csv.writer(fp)
            data.writerow([name, number, pastOrderString])

        with open('pastOrders.csv', 'w') as fp:
            reader = csv.reader(fp)

            r = 0
            for col in reader:
                c = 0
                for row in col:
                    display_lbl = Label(past_frame, text = row, relief = GROOVE, height = 300, width = 200)
                    display_lbl.grid(row = r, column = c)
                    c += 1
                r += 1 

    try:
        login_frame.place_forget()
        menu_frame.place_forget()
        order_frame.place_forget()
        account_frame.place_forget()
        createAccount_frame.place_forget()
    except NameError as e:
        print(f'Error handled, see details below: \n{e}')

    window.title('Past Orders - Mochi Fresh')

    pastOrders_frame.place(x = 350, y = 350, anchor = 'center')

    pastOrders_lbl = Label(pastOrders_frame, text = "Past Orders", fg = 'black', bg = '#9CAF88', justify = CENTER, font = ('Acta Display', 19, 'bold'))
    pastOrders_lbl.place(x = 225, y = 5)

    back_button = Button(pastOrders_frame, text = 'Back to Account Manager', bg = 'white', fg = 'black', font = ('Acta Display', 10, 'bold'), command = back )
    back_button.place (x = 430, y = 425)

    # frame that displays the user's csv file of past orders
    past_frame = Frame(pastOrders_frame, width = 560, height = 385, bg = '#b5bda5', borderwidth = 1, relief = GROOVE)
    past_frame.place(x = 20, y = 40)

    display_orders

# "Past Orders" page -> Account Manager       
def back():
    account_manager()


# Login > Account Manager > View Menu/Submit Order Page
def order_onclick(): 
    global order_frame, menu_frame, checkvar1, checkvar2, checkvar3, checkvar4, checkvar5, checkvar6, checkvar7, checkvar8, c1, c2, c3, c4, c5, c6, c7, c8

    account_frame.place_forget()
    login_frame.place_forget()
    createAccount_frame.place_forget()
    feedback_frame.place_forget()
    pastOrders_frame.place_forget()

    window.title('Menu/Order Here - Mochi Fresh')
    window.config(menu = menubar)

    checkvar1 = IntVar()
    checkvar2 = IntVar()
    checkvar3 = IntVar()
    checkvar4 = IntVar()
    checkvar5 = IntVar()
    checkvar6 = IntVar()
    checkvar7 = IntVar()
    checkvar8 = IntVar()

    # order_frame.pack()
    order_frame.place(anchor = 'center', x = 330, y = 350)
    
    order_lbl = Label(order_frame, text = "Mochi Fresh Menu", fg = 'black', bg = '#9CAF88', justify = CENTER, font = ('Acta Display', 19, 'bold'))
    order_lbl.place(x = 220, y = 10)

    # frame for users to choose what to add to their
    menu_frame = Frame(order_frame, width = 560, height = 400, bg = '#b5bda5', borderwidth = 1, relief = GROOVE)
    menu_frame.place(x = 20, y = 40)

    # _lbl = Label(order_frame, text = "*All drinks are medium-sized and come with boba as the topping!*", fg = 'black', bg = '#E9CDD0', font = ('Acta Display', 15, 'bold'))
    
    menu_lbl = Label(menu_frame, text = 'Milk Teas', fg= 'white', bg = '#b5bda5', font = ('Acta Display', 18, 'bold'))
    menu_lbl.place(x = 10, y = 20)

    c1 = Checkbutton(menu_frame, text = 'Signature Milk Tea', fg = 'black', bg = '#b5bda5', onvalue = 1, offvalue = 0, variable = checkvar1)
    c1.place(x = 40, y = 60)
    c2 = Checkbutton(menu_frame, text = 'Coffee Milk Tea', fg = 'black', bg = '#b5bda5', onvalue = 2, offvalue = 0, variable = checkvar2)
    c2.place(x = 40, y = 80)
    c3 = Checkbutton(menu_frame, text = 'Real Taro Milk Tea', fg = 'black', bg = '#b5bda5', onvalue = 3, offvalue = 0, variable = checkvar3)
    c3.place(x = 40, y = 100)

    menu_lbl2 = Label(menu_frame, text = 'Fruit Teas', fg= 'white', bg = '#b5bda5', font = ('Acta Display', 18, 'bold'))
    menu_lbl2.place(x = 10, y = 150)
    c4 = Checkbutton(menu_frame, text = 'Signature Fruit Tea', fg = 'black', bg = '#b5bda5', onvalue = 4, offvalue = 0, variable = checkvar4)
    c4.place(x = 40, y = 180)
    c5 = Checkbutton(menu_frame, text = 'Peach Oolong Tea', fg = 'black', bg = '#b5bda5', onvalue = 5, offvalue = 0, variable = checkvar5)
    c5.place(x = 40, y = 205)

    menu_lbl3 = Label(menu_frame, text = 'Smoothies', fg= 'white', bg = '#b5bda5', font = ('Acta Display', 18, 'bold'))
    menu_lbl3.place(x = 10, y = 240)
    c6 = Checkbutton(menu_frame, text = 'Mango Smoothie', fg = 'black', bg = '#b5bda5', onvalue = 6, offvalue = 0, variable = checkvar6)
    c6.place(x = 40, y = 275)
    c7 = Checkbutton(menu_frame, text = 'Watermelon Smoothie', fg = 'black', bg = '#b5bda5', onvalue = 7, offvalue = 0, variable = checkvar7)
    c7.place(x = 40, y = 295)

    menu_lbl4 = Label(menu_frame, text = 'Special Items', fg = 'white', bg = '#b5bda5', font = ('Acta Display', 18, 'bold'))
    menu_lbl4.place(x = 300, y = 120)
    c8 = Checkbutton(menu_frame, text = 'Drink of the Day', fg = 'black', bg = '#b5bda5', onvalue = 8, offvalue = 0, variable = checkvar8)
    c8.place(x = 330, y = 150)

    submitOrder_button = Button(menu_frame, text = 'Submit Order', command = feedback_screen, bg = '#b5bda5', fg = 'black', font = ('Acta Display', 17))
    submitOrder_button.place(x = 400, y = 350)

    orderSelected = accounts[customerName]['Past Orders']
    if 1 in orderSelected:
        c1.select()
    if 2 in orderSelected:
        c2.select()
    if 3 in orderSelected:
        c3.select()
    if 4 in orderSelected:
        c4.select()
    if 5 in orderSelected:
        c5.select()
    if 6 in orderSelected:
        c6.select()

# Logic for after the "Submit Order" button is clicked
def submitOrder_onclick():
    global orders

    # orderSelected = accounts[customerName]['Past Orders']
    # if 1 in orderSelected:
    #     c1.select()
    # if 2 in orderSelected:
    #     c2.select()
    # if 3 in orderSelected:
    #     c3.select()
    # if 4 in orderSelected:
    #     c4.select()
    # if 5 in orderSelected:
    #     c5.select()
    # if 6 in orderSelected:
    #     c6.select()
    
    orders = [checkvar1.get(), checkvar2.get(), checkvar3.get(), checkvar4.get(), checkvar5.get(), checkvar6.get(), checkvar7.get(), checkvar8.get()]
    orders = list(filter(None, orders))

    if not path.isfile('pastOrders.csv'):
        with open('pastOrders.csv', 'w') as fp: 
            data = csv.writer(fp)
            data.writerow(['Name', 'Number', 'Orders'])
    
    orderString = ' '.join(str(order) for order in orders)

    with open('pastOrders.csv', 'a', newline = '') as fp:
        data = csv.writer(fp)
        data.writerow([name.get(), number.get(), orderString])

    feedback_screen()

# Login > Account Manager > View Menu/Submit Order > Feedback
def feedback_screen():
    global feedback_frame, feedback

    menu_frame.place_forget()
    order_frame.place_forget()
    login_frame.place_forget()

    window.title('Order Submitted! - Mochi Fresh')

    feedback_frame.place(anchor = 'center', x = 350, y = 350)

    orderConfirmation_lbl = Label(feedback_frame, text = 'Your order has been submitted! Please see the cashier to pay.', bg = '#e5bcbb', fg = 'black', font = ('Acta Display', 16, 'bold'))
    orderConfirmation_lbl.place(x = 20, y = 20)

    feedback = Label(feedback_frame, text = "We value your feedback. Leave us a review on Yelp!☺", bg = '#b5bda5', fg = 'black', font = ('Acta Display', 16))
    feedback.place(x = 75, y = 90)

    feedback_entry = Entry(feedback_frame, textvariable = feedback, relief = GROOVE, bg = '#b5bda5', borderwidth = 1, height = 100, width = 200)
    feedback_entry.pack()
    # feedback_entry.place(x = 120, y = 200)

# "Create Account" Button > Create Account Form
def newAccount_form():
    global createAccount_frame

    login_frame.place_forget()
    logout_button.place_forget()

    window.config(menu = 0)

    window.title('Creating a New User Account - Mochi Fresh')

    createAccount_frame.pack()
    createAccount_frame.place(x = 350, y = 350, anchor = 'center')

    instructions_lbl = Label(createAccount_frame, text = 'Please enter your name and a phone number to create an account!', bg = '#9CAF88', font = ('Acta Display', 16), fg = 'white')
    instructions_lbl.place(x = 10, y = 10)

    name = Label(createAccount_frame, text = "Name", fg = 'white', bg = '#9CAF88', font = ('Acta Display',21))
    name.place(x = 30, y = 60)

    name = StringVar()
    name.set('')
    name_entry = Entry(createAccount_frame, textvariable = name, justify = CENTER, width = 30, bg = '#b5bda5')
    name_entry.place(x= 210, y = 60)

    number = Label(createAccount_frame, text = "Phone Number", fg = 'white', bg = '#9CAF88', font = ('Acta Display', 21))
    number.place(x = 30, y = 100)

    number = IntVar()
    number.set('')
    number_entry = Entry(createAccount_frame, textvariable = number, justify = CENTER, width = 30, bg = '#b5bda5')
    number_entry.place(x=210, y = 100)

    createAccount_button = Button(createAccount_frame, text = 'Create Account', font = ('Acta Display', 18, 'bold'), padx = 3, command = createAccount_onclick, bg = 'white', fg = '#9CAF88', borderwidth=1)
    createAccount_button.place(x = 220, y = 150)

    backMain_button = Button(createAccount_frame, text = "Back", bg = 'white', fg = '#9CAF88', font = ('Acta Display', 18, 'bold'), padx = 3, command = main)
    backMain_button.place(x = 220, y = 200)

# 'Create a New Account' PAGE > Create Account Button 
def createAccount_onclick():
    global accounts, customerName, customerNum   
    customerNum = float(number.get())
    customerName = name.get()
    
    print(len(customerName))
    print(len(customerNum))

    if customerName in accounts:
        tkinter.messagebox.showinfo("This name/phone number already exists in our records. Please try logging in.")
        name.set('')
    else:
        if customerName != " ":
            print('Hi!')

            if customerNum >= 10:
                print('Bye!')
                randomPts = random.randint(1, 100)

                new_customer = Customer(customerName, customerNum, randomPts)
                print("New Customer Data:")
                print(new_customer)

                accounts[customerName] = dict()
                accounts[customerName]['Name'] = str(customerName).capitalize()
                accounts[customerName]['Phone Number'] = str(customerNum)
                accounts[customerName]['Points'] = randomPts

                with open('customers.json', 'w', newline = "") as file_handle:
                    json.dump(accounts, file_handle) 

                main()

                tkinter.messagebox.showinfo("New account created!", "Please log in to view your account or to place an order.")

            else: 
                tkinter.messagebox.showinfo("ERROR", "Phone numbers should be 10 digits long and entered in this format: 0000000000")
                number.set('')
        else: 
            tkinter.messagebox.showinfo("ERROR", "The name entered can be a nickname, username, etc")
            name.set('')


#  ------------------------------------LOGOUT BUTTON ONCLICK (back to login page)------------------------------
def logout_onclick():
    try:
        account_frame.place_forget()
        pastOrders_frame.place_forget()
        createAccount_frame.place_forget()
        order_frame.place_forget()
        menu_frame.place_forget()
        feedback_frame.place_forget()
    except NameError as e:
        print("")

    window.config(menu = 0)
    name.set('')
    number.set('')
    logout_button.place_forget()

    main()

    tkinter.messagebox.showinfo("Successfully logged out", 'See you next time!')

# # Back to Account Manager page
# def back():
#     login_frame.place_forget()
#     createAccount_frame.place_forget()
#     account_frame.place_forget()
#     feedback_frame.place_forget()
#     pastOrders_frame.place_forget()
#     order_frame.place_forget()

#     account_manager(customer)

# --------------------------------------GUI SETUP-------------------------------------------------
window = Tk()
window.geometry('700x700')
window.title('Login - Mochi Fresh')
window.config(bg = '#b5bda5')

# stationary frame for welcome msg + greeting variables
mainframe = Frame(window, width=400, height=200, bg = '#9CAF88', relief = GROOVE, borderwidth = 2)
mainframe.pack()
mainframe.place(anchor='center', x = 350, y = 80)

welcome_message = Label(mainframe, text = "Mochi Fresh", anchor = 'w', pady = 1, bg = '#9CAF88', fg = 'white', font = ('Trivia Serif', 24, 'bold'))
welcome_message.place(x = 125, y = 30)
welcome_message.pack()
greeting = Label(mainframe, text = "Arizona's Best Homemade Boba Milk Tea", fg = '#b5bda5', font = ('Acta Display', 20, 'bold'))
greeting.place(x = 1, y = 60)
greeting.pack()

menubar = Menu(window)

account_menu = Menu(menubar) 
menubar.add_cascade(label = 'Account', menu = account_menu)
account_menu.add_command(label = 'Account Manager', command = account_manager)
account_menu.add_separator() # horizontal bar
account_menu.add_command(label = 'Logout', command = logout_onclick)

order_menu = Menu(window)
menubar.add_cascade(label = 'Orders', menu = order_menu)
order_menu.add_command(label = 'Order History', command = pastOrders_onclick)
order_menu.add_command(label = 'Submit a New Order', command = order_onclick)

help_ = Menu(menubar)
menubar.add_cascade(label = 'Help', menu = help_)

# login frame
login_frame = Frame(window, width = 520, height = 300, bg = '#9CAF88', relief = GROOVE, borderwidth = 1)

# account manager frame
account_frame = Frame(window, width = 600, height = 450, bg = '#9CAF88', relief = GROOVE, borderwidth = 1)

# frame for users creating a new account
createAccount_frame = Frame(window, width = 520, height = 300, bg = '#9CAF88', relief = GROOVE, borderwidth = 1)

# frame for users to submit their order
order_frame = Frame(window, height = 450, width = 600, bg = '#9CAF88', relief = GROOVE, borderwidth = 1)

# frame after users submit their order and are given an option to leave feedback
feedback_frame = Frame(window, width = 520, height = 300, bg = '#9CAF88', relief = GROOVE, borderwidth = 1)

# # frame for users to view their previous orders
pastOrders_frame = Frame(window, width = 600, height = 450, bg = '#9CAF88', relief = GROOVE, borderwidth = 1)

main() 

# backToMain_button = Button(window, text = 'Back to Account Manager', command = account_manager, bg = '#b5bda5', fg = 'black', font = ('Acta Display', 10, 'bold'), width = 25)
# backToMain_button.place(x = 400, y = 430)

logout_button = Button(window, text = 'Logout', command = logout_onclick, bg = '#b5bda5', fg = 'black', font = ('Acta Display', 10, 'bold'), width = 5)
logout_button.place(x = 505, y = 600)

exit_button = Button(window, text = 'Exit', command = window.quit, bg = '#b5bda5', fg = 'black', font = ('Acta Display', 10, 'bold'), width = 5)
exit_button.place(x = 565, y = 600)


window.mainloop()
