from tkinter import*
import pickle

Restore = []
can_Save = False
phone_numbers_save_index = 0

def error_window(prompt):
    error = Toplevel()
    error.geometry("350x100")
    error.title("Error")
    error_message = Label(error, text="Error!")
    error_prompt = Label(error, text=prompt)
    exit_btn = Button(error, text="Exit", width=20, height=30, command= lambda: error.destroy())
    error_message.pack(side=TOP)
    error_prompt.pack(side=TOP, pady=10)
    exit_btn.pack(side=TOP, pady=0)

#Checks for valid entry (only spaces and atleast one text + name cant be already entered before)
def check_validity(name, number):

    if not(unchanged()):
        if len(name)>0 and len(number)>8:
            if any(x.isalpha() for x in name) and not(any(x.isdigit() for x in name)) == True:
                for i in range(len(PhoneBook_info)):
                    if name == PhoneBook_info[i][0] and number == PhoneBook_info[i][1]:
                        error_window("Name is already in list or is on file.")
                        return False
                return True
            else:
                error_window("No numbers in name. Atleast one letter in name.")
        else:
            error_window("Name and/or number are not long enough!")

#Clear text in: country, city, street and number
def clear_OtherInfo():
    name_label.configure(text=" ")
    country_entry.delete(0, END)
    city_entry.delete(0, END)
    street_entry.delete(0, END)
    number_entry.delete(0, END)


#Clear text in: Name and Password
def clear_MainInfo():
    name_entry.delete(0, END)
    phone_entry.delete(0, END)

#Checks if entry boxes are blank
def canSave():

    global can_Save
    if can_Save:
        return True
    else:
        return False

def show():
    intro_frame.destroy()
    enter_btn.destroy()
    quit_btn.destroy()
    phone_book.lower()
    
def button_press(button):
    
    global can_Save
    name = str(name_var.get())
    number = str(phone_var.get())

    if button == "enter":
        show()
    
    #Compares seleteced item in listbox with item in list and when found, both are deleted
    elif button == "delete":
        break_all = False
        can_Save = False
        for i in range(len(PhoneBook_info)):

            if break_all==True:
                break
            elif phone_book.curselection() and phone_book.get(ACTIVE) == (PhoneBook_info[i][0], ":", PhoneBook_info[i][1]): 
                Restore.append(PhoneBook_info[i])
                PhoneBook_info.pop(i)
                phone_book.delete(ACTIVE)
                clear_MainInfo()
                clear_OtherInfo()
                break_all=True
                break
        
    #Adds a new list each time to the Phone Book list and adds the name and number seperately to the added list as well as N/A for
    #the ocuntry, city, street and number
    elif button == "add":
 
        if check_validity(name, number): 
            phone_book.insert(0,(name,":", number))
            PhoneBook_info.append([])
            PhoneBook_info[len(PhoneBook_info)-1].append(name)
            PhoneBook_info[len(PhoneBook_info)-1].append(number)

            for i in range(4):
                PhoneBook_info[len(PhoneBook_info)-1].append("N/A")
                
        name_entry.delete(0, END)
        phone_entry.delete(0, END)
                
    #Deletes the items in listobx, sorts the Phone Book info list and reprint listbox with sorted list
    elif button == "sort_up":
        PhoneBook_info.sort()
        phone_book.delete(0, END)
        for i in range(len(PhoneBook_info)):
            phone_book.insert(END, (PhoneBook_info[i][0], ":", PhoneBook_info[i][1]))
            if len(PhoneBook_info[i]) > 6:
                phone_book.itemconfig(END, {'bg':'red'})


    elif button == "sort_down":
        PhoneBook_info.sort()
        phone_book.delete(0, END)
        for i in range(len(PhoneBook_info)):
            phone_book.insert(0, (PhoneBook_info[i][0], ":", PhoneBook_info[i][1]))
            if len(PhoneBook_info[i]) > 6:
                phone_book.itemconfig(0, {'bg':'red'})

def favourite():
    global phone_numbers_save_index
    global can_Save
    clear_OtherInfo()
    clear_MainInfo()
    can_Save = False
    
    if len(PhoneBook_info[phone_numbers_save_index])> 6: #> 6 means that it is a favourited item as it has 5 indexes in it which means you are unfavourting it
        PhoneBook_info[phone_numbers_save_index].pop(6)
        phone_book.itemconfig(ACTIVE, {'bg':'white'})
    else:
        PhoneBook_info[phone_numbers_save_index].append("Favourite") #< 6 means that it is not a favourited item as it has only 4 indexes in it which means you are favourting it
        phone_book.itemconfig(ACTIVE, {'bg':'red'})


#Inserts the phone book lists indexes into the listbox
def load():
    global PhoneBook_info
    PhoneBook_info = []
    PhoneBook_info = pickle.load(open("PhoneBook_Info", "rb"))

    for i in range(len(PhoneBook_info)):
        phone_book.insert(END, (PhoneBook_info[i][0], ":", PhoneBook_info[i][1]))
        if len(PhoneBook_info[i]) > 6:
            phone_book.itemconfig(END, {'bg':'red'})
    
#Thorugh a for loop, whatever is entered into the find entry box is compared to the phonebook list name
#and when found, scrolls to that selection in the listbox and selects it
def find():
    for i in range(len(PhoneBook_info)):
        if find_Entry.get() == PhoneBook_info[i][0]:
            found1 = PhoneBook_info[i][0]
            found2 = PhoneBook_info[i][1]
            find_Entry.delete(0, END)
            break
    
    for j in range(len(PhoneBook_info)):
        if (found1, ":", found2) == phone_book.get(j):
            phone_book.select_set(j)
            phone_book.yview(j)
            break

def listbox_click(event):

    global phone_numbers_save_index
    global can_Save 


    #Compares the listbox selection with the PhoneBook info list and finds the correct index
    #the previous info of all entry boxes are deleted
    #enters the name part of the index into the name entry and number part into the number part as well as all other parts
    for i in range(len(PhoneBook_info)):
        if phone_book.get(ACTIVE) == (PhoneBook_info[i][0], ":", PhoneBook_info[i][1]):
            can_Save = True
            phone_numbers_save_index = i
            clear_MainInfo()
            clear_OtherInfo()
            name_entry.insert(END, PhoneBook_info[i][0])
            phone_entry.insert(END, PhoneBook_info[i][1])
            name_label.configure(text=PhoneBook_info[i][0])

            country_entry.insert(END, PhoneBook_info[i][2])
            city_entry.insert(END, PhoneBook_info[i][3])
            street_entry.insert(END, PhoneBook_info[i][4])
            number_entry.insert(END, PhoneBook_info[i][5])

#Whenever something is deleted, it goes into the restore list and when the button is pressed
#if what is wanting to be restored actually was deleted, it is added to the phonebook inf list
#and inserted into the listbox
def restore():
    
    for i in range(len(Restore)):
        if str(restore_Entry.get()) == Restore[i][0]:
            PhoneBook_info.append(Restore[i])
            phone_book.insert(END, (Restore[i][0], ":", Restore[i][1]))
            Restore.pop(i)
            restore_Entry.delete(0, END)
            break

#When save is pressed, if whatever is in the differnet entry boxes is the same as
#what was originally in them (unchanged), returns true (prevents error box from
#coming up)
def unchanged():
    if len(PhoneBook_info)>0:
        if str(name_entry.get()) == PhoneBook_info[phone_numbers_save_index][0]:
            if str(phone_entry.get()) == PhoneBook_info[phone_numbers_save_index][1]:
               return True

def save():

    global phone_numbers_save_index
    global can_Save
    name = str(name_entry.get())
    number = str(phone_entry.get())

    if canSave():
        #PhoneBook info list is changed according to the entry boxes and in turn the list box is adjusted
        if check_validity(name, number):
            PhoneBook_info[phone_numbers_save_index][0] = name
            PhoneBook_info[phone_numbers_save_index][1] = number
            phone_book.insert(ACTIVE, (name, ":", number))
            phone_book.delete(ACTIVE)
            name_entry.delete(0, END)
            phone_entry.delete(0, END)

        PhoneBook_info[phone_numbers_save_index][2]=str(country_var.get())
        PhoneBook_info[phone_numbers_save_index][3]=str(city_var.get())
        PhoneBook_info[phone_numbers_save_index][4]=str(street_var.get())
        PhoneBook_info[phone_numbers_save_index][5]=str(number_var.get())

        pickle.dump(PhoneBook_info, open("PhoneBook_Info", "wb"))
            
        clear_OtherInfo()
        clear_MainInfo()
        can_Save = False
    else:
        pickle.dump(PhoneBook_info, open("PhoneBook_Info", "wb"))

def hide():
    restore_btn.lower()
    find_btn.lower()
    sortup_btn.lower()
    sortdown_btn.lower()
    restore_Entry.lower()
    find_Entry.lower()
    phone_book.lower()
    scrollbar.lower()
    name_entry.lower()
    phone_entry.lower()
    add_btn.lower()
    delete_btn.lower()
    save_btn.lower()
    favourite_btn.lower()
  
#-------------------Initiating Window---------------------------#        
root=Tk()

root.geometry("480x365")
root.resizable(width=False, height=False)
root.title("PhoneBook")
screen_width = root.winfo_width()
screen_height = root.winfo_height()

name_var=StringVar()
phone_var=StringVar()
country_var = StringVar()
city_var = StringVar()
street_var = StringVar()
number_var = StringVar()

find_var = StringVar()

#------------------Frames----------------------------------------#
bottomright_frame = Frame(root, bg="white", height=220, width=200)
topright_frame = Frame(root,height=100, width=150)
topmiddle_frame = Frame(root, height=200, width=250)
intro_frame = Frame(root, height=screen_height, width=screen_width, bg="white")

#------------------Making Window-------------------------------#
label_name=Label(topmiddle_frame, text="Name", font="halvetica")
label_phone=Label(topmiddle_frame, text="Phone", font="halvetica")

name_entry = Entry(topmiddle_frame, textvariable=name_var, bd=3, width=35)
phone_entry = Entry(topmiddle_frame, textvariable=phone_var, bd=3, width=35)

add_btn = Button(topmiddle_frame, text="Add", bd=3, width=5, command = lambda: button_press("add"))
delete_btn = Button(topmiddle_frame, text="Delete", bd=3, command = lambda: button_press("delete"))
save_btn = Button(topmiddle_frame, text="Save", bd=3, width=5, command = save)
favourite_btn = Button(topmiddle_frame, text="★/☆", bd=3, width=5, command = favourite)
sortup_btn=Button(root, text="↑↑", width=4, command = lambda: button_press("sort_up"))
sortdown_btn=Button(root, text="↓↓", width=4, command = lambda: button_press("sort_down"))

phone_book=Listbox(root, width=35, height=12)
phone_book.bind('<Double-Button-1>', listbox_click)
scrollbar = Scrollbar(root, orient=VERTICAL)

name_label=Label(bottomright_frame, text="N/A", bg="white")
country_label=Label(bottomright_frame, text="Country", bg="white")
country_entry=Entry(bottomright_frame, textvariable=country_var, bd=3, relief="raised", width=23, bg="white")
city_label=Label(bottomright_frame, text="City", bg="white")
city_entry=Entry(bottomright_frame, textvariable=city_var, bd=3, relief="raised", width=23, bg="white")
street_label=Label(bottomright_frame, text="Street", bg="white")
street_entry=Entry(bottomright_frame, textvariable=street_var, bd=3, relief="raised", width=23, bg="white")
number_label=Label(bottomright_frame, text="Number", bg="white")
number_entry=Entry(bottomright_frame, textvariable=number_var, bd=3, relief="raised", width=23, bg="white")


find_btn = Button(root, text="Find", command=find, width=7)
find_Entry = Entry(root, bd=3, width=15, textvariable=find_var)
restore_btn = Button(root, text="Restore", command = restore)
restore_Entry = Entry(root, bd=3, width=15)

enter_btn = Button(root, text="Enter", bg="white", width=10, command = lambda: button_press("enter"))
quit_btn = Button(root, text="Quit", bg="white", width=10, command = lambda: root.destroy())

logo = PhotoImage(file="Tackle Organization Logo - Small.png")
panel = Label(topright_frame, image=logo)

title = PhotoImage(file = "Title page.png")
title_page = Label(intro_frame, image=title).pack()

#------------Binding Scroll Wheel to Phonebook List------------#
phone_book.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=phone_book.yview)


#------------------Putting Everything on the Screen------------#
bottomright_frame.grid(row=1, column=2)
bottomright_frame.pack_propagate(0)
topmiddle_frame.grid(row=0, column=1)
topright_frame.grid(row=0, column=2)
panel.grid(sticky=W)

label_name.grid(row=0, column=0)
label_phone.grid(row=1, column=0)

name_entry.grid(row=0, column=1)
phone_entry.grid(row=1, column=1)

favourite_btn.grid(row=2, column=1, sticky=E, padx=55)
add_btn.grid(row=2, column=1, sticky=W, padx=0)
delete_btn.grid(row=2, column=1, sticky=W, padx=55)
save_btn.grid(row=2, column=1, sticky=E)
sortup_btn.grid(row=1, column=1, padx= 6, sticky=NW)
sortdown_btn.grid(row=1, column=1, padx= 6,sticky=SW)

phone_book.grid(row=1, column=1, sticky=N+S+E)
scrollbar.grid(row=1, column=1, sticky=N+S+E)

name_label.pack(side=TOP)
number_entry.pack(side=BOTTOM, anchor=W, padx=2)
number_label.pack(side=BOTTOM, anchor=W, pady=2)
street_entry.pack(side=BOTTOM, anchor=W, pady=2)
street_label.pack(side=BOTTOM, anchor=W, pady=2)
city_entry.pack(side=BOTTOM, anchor=W, padx=5)
city_label.pack(side=BOTTOM, anchor=W, padx=5)
country_entry.pack(side=BOTTOM, anchor=W, padx=5, pady=2)
country_label.pack(side=BOTTOM, anchor=W, padx=5, pady=2)

find_btn.grid(row=2, column=1, sticky=E, pady = 6, padx=15)
find_Entry.grid(row=2, column=1, sticky=E, pady = 8, padx=85)
restore_btn.grid(row=2, column=2, sticky=E, padx=0, pady=6)
restore_Entry.grid(row=2, column=2, sticky=W, padx=40, pady=8)

root.update()

load()
intro_frame.place(x=0, y=0)
enter_btn.place(x=round((root.winfo_width())/2, 1) - 40, y=round((root.winfo_height())/2, 1))
quit_btn.place(x=round((root.winfo_width())/2, 1) - 40, y=round((root.winfo_height())/2 + 70, 1))
hide()

root.mainloop()

