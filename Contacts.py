import sys
import mysql.connector
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

win_size = "400x300+100+100"

#Check if connected to MySQL or not
def isconnected()	:
	try	:
		mydb = mysql.connector.connect	(
			host = "localhost",
			user = 'root',
			password = '1234',
		)
	
		if mydb.is_connected()	:
			return("✅ Connected to MYSQL database successfully!", True, mydb)

	except mysql.connector.Error as err	:
		return (f"⚠ Error: {err}", False, None)
	
def print_records(tree, result_label, records)	:
	for i in tree.get_children():
		tree.delete(i)

	if not records:
		result_label.config(text="No contact found", bg = 'aquamarine')
	else:
		result_label.config(text=f"{len(records)} result(s) found")
		for row in records:
			tree.insert("", "end", values=row)
		
def add_contact(mydb)	:
	add_win = Toplevel(gui)
	add_win.title("Add contact")
	add_win.geometry(win_size)
	add_win.config(bg = 'lightgreen')
	
	Label(add_win, text = "Name: ", bg = 'lightgreen').grid(row = 0, column = 0, pady = 10)
	name_entry = Entry(add_win)
	name_entry.grid(row = 0, column = 1, pady = 10)
	
	Label(add_win, text = "Contact Number: ", bg = 'lightgreen').grid(row = 1, column = 0, pady = 10)
	contact_entry = Entry(add_win)
	contact_entry.grid(row = 1, column = 1, pady = 10)
	
	Label(add_win, text = "Email: ", bg = 'lightgreen').grid(row = 2, column = 0, pady = 10)
	email_entry = Entry(add_win)
	email_entry.grid(row = 2, column = 1, pady = 10)
	
	Label(add_win, text = "Address: ", bg = 'lightgreen').grid(row = 3, column = 0, pady = 10)
	address_entry = Entry(add_win)
	address_entry.grid(row = 3, column = 1, pady = 10)
	
	def save_contact():
		try	:
			name = name_entry.get().strip()
			contact = int(contact_entry.get().strip())
			email = email_entry.get().strip()
			address = address_entry.get().strip()
			
			if not mydb.is_connected()	:
				mydb.reconnect()
			
			cursor = mydb.cursor()
	
			cursor.execute("INSERT INTO contact (Name, Number, Email, Address) VALUES(%s, %s, %s, %s);", (name, contact, email, address))
			mydb.commit()
			add_win.destroy()
			messagebox.showinfo("Success!", "✅ Contact saved successfully!")
		
		except Exception as e	:
			Label(add_win, text = f"❌ Error: {e}", fg = "red", font = ("Arial", 12), wraplength = 300, justify = "center").place(relx = 0.5, rely = 0.5, anchor = "center").pack()
		
	Button(add_win, text = "Save contact", width = 20, bg = 'green', command = save_contact).grid(row = 4, column = 0, pady = 10)

def view_contact(mydb)	:
	try	: 
		if not mydb.is_connected()	:
			mydb.reconnect(attempt = 3, delay = 2)
		
		cursor = mydb.cursor()
		cursor.execute("SELECT * FROM contact ORDER BY Name ASC;")
		
		records = cursor.fetchall()
		
		if not records	:
			messagebox.showinfo("Contact record", "No contact found")
			return
		
		view_win = Toplevel(gui)
		view_win.title("Contact List")
		view_win.geometry("1100x400")
		view_win.config(bg = 'lightpink')
		
		cols = ("Name", "Number", "Email", "Address")
		tree = ttk.Treeview(view_win, columns = cols, show = "headings")
		
		for col in cols	:
			tree.heading(col, text = col)
			tree.column(col, width = 250)
			
		for row in records	:
			tree.insert("", "end", values = row)
		
		tree.pack(fill = "both", expand = True)
		
	except mysql.connector.Error as e	:
		messagebox.showerror("Database error:", str(e))
		
def search(mydb)	:
	def search_name(cursor)	:
		search_n = Toplevel(search_win)
		search_n.title("Search by Name")
		search_n.geometry(win_size)
		search_n.config(bg = 'lavender')

		Label(search_n, text="Enter name", bg = 'lavender').grid(row=0, column=0, pady=10)
		name_entry = Entry(search_n)
		name_entry.grid(row=0, column=1, pady=10)

		result_label = Label(search_n, text="")
		result_label.grid(row=1, column=0, columnspan=2, pady=10)

		tree = ttk.Treeview(search_n, columns=("Name", "Number", "Email", "Address"), show="headings")
		for col in ("Name", "Number", "Email", "Address"):
			tree.heading(col, text=col)
			tree.column(col, width=120)
		tree.grid(row=3, column=0, columnspan=2, pady=10)

		def do_search():
			name = name_entry.get().strip()
			if not name:
				result_label.config(text="⚠ Please enter a name")
				return

			cursor.execute("SELECT * FROM contact WHERE Name = %s", (name,))
			records = cursor.fetchall()

			print_records(tree, result_label, records)
	
		Button(search_n, text="Search", width = 20, bg = 'lightgreen', command = do_search).grid(row=2, column=0, columnspan=2, pady=10)
		
	def search_contact(cursor)	:
		search_c = Toplevel(search_win)
		search_c.title("Search by Contact")
		search_c.geometry(win_size)
		search_c.config(bg = 'palegreen')

		Label(search_c, text="Enter contact", bg = 'palegreen').grid(row=0, column=0, pady=10)
		contact_entry = Entry(search_c)
		contact_entry.grid(row=0, column=1, pady=10)

		result_label = Label(search_c, text="")
		result_label.grid(row=1, column=0, columnspan=2, pady=10)

		tree = ttk.Treeview(search_c, columns=("Name", "Number", "Email", "Address"), show="headings")
		for col in ("Name", "Number", "Email", "Address"):
			tree.heading(col, text=col)
			tree.column(col, width=120)
		tree.grid(row=3, column=0, columnspan=2, pady=10)

		def do_search():
			contact = int(contact_entry.get().strip())
			if not contact:
				result_label.config(text="⚠ Please enter a contact number")
				return

			cursor.execute("SELECT * FROM contact WHERE Number = %s", (contact,))
			records = cursor.fetchall()

			print_records(tree, result_label, records)
	
		Button(search_c, text="Search", width = 20, bg = 'lightgreen', command = do_search).grid(row=2, column=0, columnspan=2, pady=10)
		
			
	def search_email(cursor)	:
		search_e = Toplevel(search_win)
		search_e.title("Search by Email")
		search_e.geometry(win_size)
		search_e.config(bg = 'wheat')

		Label(search_e, text="Enter email", bg = 'wheat').grid(row=0, column=0, pady=10)
		email_entry = Entry(search_e)
		email_entry.grid(row=0, column=1, pady=10)

		result_label = Label(search_e, text="")
		result_label.grid(row=1, column=0, columnspan=2, pady=10)

		tree = ttk.Treeview(search_e, columns=("Name", "Number", "Email", "Address"), show="headings")
		for col in ("Name", "Number", "Email", "Address"):
			tree.heading(col, text=col)
			tree.column(col, width=120)
		tree.grid(row=3, column=0, columnspan=2, pady=10)

		def do_search():
			email = email_entry.get().strip()
			if not email:
				result_label.config(text="⚠ Please enter an email")
				return

			cursor.execute("SELECT * FROM contact WHERE Email = %s", (email,))
			records = cursor.fetchall()

			print_records(tree, result_label, records)
	
		Button(search_e, text="Search", width = 20, bg = 'lightgreen', command = do_search).grid(row=2, column=0, columnspan=2, pady=10)
			
			
	def search_address(cursor)	:
		search_a = Toplevel(search_win)
		search_a.title("Search by Address")
		search_a.geometry(win_size)
		search_a.config(bg = 'plum')

		Label(search_a, text="Enter address", bg = 'plum').grid(row=0, column=0, pady=10)
		address_entry = Entry(search_a)
		address_entry.grid(row=0, column=1, pady=10)

		result_label = Label(search_a, text="")
		result_label.grid(row=1, column=0, columnspan=2, pady=10)

		tree = ttk.Treeview(search_a, columns=("Name", "Number", "Email", "Address"), show="headings")
		for col in ("Name", "Number", "Email", "Address"):
			tree.heading(col, text=col)
			tree.column(col, width=120)
		tree.grid(row=3, column=0, columnspan=2, pady=10)

		def do_search():
			address = address_entry.get().strip()
			if not address:
				result_label.config(text="⚠ Please enter an address")
				return

			cursor.execute("SELECT * FROM contact WHERE address LIKE %s",(f"%{address}%",))

			records = cursor.fetchall()

			print_records(tree, result_label, records)
	
		Button(search_a, text="Search", width = 20, bg = 'lightgreen', command=do_search).grid(row=2, column=0, columnspan=2, pady=10)
			
	try	:
	
		if not mydb.is_connected()	:
			mydb.reconnect()
		
		cursor = mydb.cursor()	
		
	except mysql.connector.Error as e	:
		messagebox.showerror("Database error: {e}")
		return
		
	search_win = Toplevel(gui)
	search_win.title("Search Contact")
	search_win.geometry(win_size)
	search_win.config(bg = 'thistle')
	
	name = Button(search_win, text = "Name", width = 20, bg = 'salmon', command = lambda: search_name(cursor))
	name.pack(pady = 10)
	
	contact = Button(search_win, text = "Contact", width = 20, bg = 'mediumseagreen', command = lambda: search_contact(cursor))
	contact.pack(pady = 10)
	
	email = Button(search_win, text = "E-mail", width = 20, bg = 'cornflowerblue', command = lambda: search_email(cursor))
	email.pack(pady = 10)
	
	address = Button(search_win, text = "Address", width = 20, bg = 'orchid', command = lambda: search_address(cursor))
	address.pack(pady = 10)
	
def update_contact(mydb)	:
	def update_name(cursor)	:
		update_n = Toplevel(gui)
		update_n.title("Update by Name")
		update_n.geometry(win_size)
		update_n.config(bg = 'lavender')
		
		Label(update_n, text = "Enter the current name", bg = 'lavender').grid(row = 0, column = 0, pady = 10)
		curr_name = Entry(update_n)
		curr_name.grid(row = 0, column = 1, pady = 10)
		
		Label(update_n, text = "Enter the updated name", bg = 'lavender').grid(row = 1, column = 0, pady = 10)
		updated_name = Entry(update_n)
		updated_name.grid(row = 1, column = 1, pady = 10)
		
		def update()	:
			curr_Name = curr_name.get().strip()
			updated_Name = updated_name.get().strip()
			
			if not curr_Name or not updated_Name	:
				messagebox.showerror("Input Error:", "Both fields are required")
				return
			
			cursor.execute("UPDATE contact SET Name = %s WHERE Name = %s", (updated_Name, curr_Name,))
			
			mydb.commit()
			messagebox.showinfo("Success", f"Updated '{curr_Name}' to '{updated_Name}'")
			update_n.destroy()

		Button(update_n, text = "Update", width = 20, bg = 'yellow', command = update).grid(row = 2, column = 0, pady = 10)
		
	def update_contact(cursor)	:
		update_c = Toplevel(gui)
		update_c.title("Update by contact")
		update_c.geometry(win_size)
		update_c.config(bg = 'peachpuff')
		
		Label(update_c, text = "Enter the current contact", bg = 'peachpuff').grid(row = 0, column = 0, pady = 10)
		curr_contact = Entry(update_c)
		curr_contact.grid(row = 0, column = 1, pady = 10)
		
		Label(update_c, text = "Enter the updated contact", bg = 'peachpuff').grid(row = 1, column = 0, pady = 10)
		updated_contact = Entry(update_c)
		updated_contact.grid(row = 1, column = 1, pady = 10)
		
		def update()	:
			curr_Contact = int(curr_contact.get().strip())
			updated_Contact = int(updated_contact.get().strip())
			
			if not curr_contact or not updated_contact	:
				messagebox.showerror("Input Error:", "Both fields are required")
				return
			
			cursor.execute("UPDATE contact SET number = %s WHERE number = %s", (updated_Contact, curr_Contact,))
			
			mydb.commit()
			messagebox.showinfo("Success", f"Updated '{curr_Contact}' to '{updated_Contact}'")
			update_c.destroy()

		Button(update_c, text = "Update", width = 20, bg = 'yellow', command = update).grid(row = 2, column = 0, pady = 10)
		
	def update_email(cursor)	:
		update_e = Toplevel(gui)
		update_e.title("Update by email")
		update_e.geometry(win_size)
		update_e.config(bg = 'honeydew')
		
		Label(update_e, text = "Enter the current email", bg = 'honeydew').grid(row = 0, column = 0, pady = 10)
		curr_email = Entry(update_e)
		curr_email.grid(row = 0, column = 1, pady = 10)
		
		Label(update_e, text = "Enter the updated email", bg = 'honeydew').grid(row = 1, column = 0, pady = 10)
		updated_email = Entry(update_e)
		updated_email.grid(row = 1, column = 1, pady = 10)
		
		def update()	:
			curr_Email = curr_email.get().strip()
			updated_Email = updated_email.get().strip()
			
			if not curr_Email or not updated_Email	:
				messagebox.showerror("Input Error:", "Both fields are required")
				return
			
			cursor.execute("UPDATE contact SET email = %s WHERE email = %s", (updated_Email, curr_Email,))
			
			mydb.commit()
			messagebox.showinfo("Success", f"Updated '{curr_Email}' to '{updated_Email}'")
			update_e.destroy()

		Button(update_e, text = "Update", width = 20, bg = 'yellow', command = update).grid(row = 2, column = 0, pady = 10)
		
	def update_address(cursor)	:
		update_a = Toplevel(gui)
		update_a.title("Update by email")
		update_a.geometry(win_size)
		update_a.config(bg = 'mistyrose')
		
		Label(update_a, text = "Enter the current email", bg = 'mistyrose').grid(row = 0, column = 0, pady = 10)
		curr_address = Entry(update_a)
		curr_address.grid(row = 0, column = 1, pady = 10)
		
		Label(update_a, text = "Enter the updated address", bg = 'mistyrose').grid(row = 1, column = 0, pady = 10)
		updated_address = Entry(update_a)
		updated_address.grid(row = 1, column = 1, pady = 10)
		
		def update()	:
			curr_Address = curr_address.get().strip()
			updated_Address = updated_address.get().strip()
			
			if not curr_Address or not updated_Address	:
				messagebox.showerror("Input Error:", "Both fields are required")
				return
			
			cursor.execute("UPDATE contact SET address = %s WHERE address = %s", (updated_Address, curr_Address,))
			
			mydb.commit()
			messagebox.showinfo("Success", f"Updated '{curr_Address}' to '{updated_Address}'")
			update_a.destroy()

		Button(update_a, text = "Update", width = 20, bg = 'yellow', command = update).grid(row = 2, column = 0, pady = 10)
		
	try	:
		if not mydb.is_connected()	:
			mydb.reconnect(attempt = 3, delay = 2)
			
		cursor = mydb.cursor()
		
	except mysql.connector.Error as e:
		messagebox.showerror("Database error: {e}")
		
	update_win = Toplevel(gui)
	update_win.title("Update Contact")
	update_win.geometry(win_size)
	update_win.config(bg = 'khaki')
	
	Button(update_win, text = "Name", width = 20, bg = 'salmon', command = lambda: update_name(cursor)).pack(pady = 10)
	
	Button(update_win, text = "Contact", width = 20, bg = 'mediumseagreen', command = lambda: update_contact(cursor)).pack(pady = 10)
	
	Button(update_win, text = "Email", width = 20, bg = 'cornflowerblue', command = lambda: update_email(cursor)).pack(pady = 10)
	
	Button(update_win, text = "Address", width = 20, bg = 'orchid', command = lambda: update_address(cursor)).pack(pady = 10)
	
def delete_number(mydb)	:
	def delete_name(cursor)	:
		delete_n = Toplevel(delete_win)
		delete_n.title("Delete by Name")
		delete_n.geometry(win_size)
		delete_n.config(bg = 'gold')
		
		Label(delete_n, text = "Enter name you want to delete", bg = 'gold').grid(row = 0, column = 0, pady = 10)
		name_entry = Entry(delete_n)
		name_entry.grid(row = 0, column = 1, pady = 10)
		
		def del_n()	:
			name = name_entry.get().strip()
			
			if not name	:
				messagebox.showerror("Input Error", "Field is required!")
				return
			
			cursor.execute("DELETE FROM contact WHERE Name = %s;", (name,))
			
			mydb.commit()
			messagebox.showinfo("Deleted contact with name ", (f"{name}"))
			delete_win.destroy()
			
		Button(delete_n, text = "Delete", width = 20, bg = 'orange', command = del_n).grid(row = 1, column = 1, pady = 10)
		
	def delete_contact(cursor)	:
		delete_c = Toplevel(delete_win)
		delete_c.title("Delete by contact")
		delete_c.geometry(win_size)
		delete_c.config(bg = 'lightcyan')
		
		Label(delete_c, text = "Enter contact you want to delete", bg = 'lightcyan').grid(row = 0, column = 0, pady = 10)
		contact_entry = Entry(delete_c)
		contact_entry.grid(row = 0, column = 1, pady = 10)
		
		def del_c()	:
			contact = contact_entry.get().strip()
			
			if not contact	:
				messagebox.showerror("Input Error", "Field is required!")
				return
			
			cursor.execute("DELETE FROM contact WHERE number = %s;", (contact,))
			
			mydb.commit()
			messagebox.showinfo("Deleted contact with contact ", (f"{contact}"))
			delete_win.destroy()
			
		Button(delete_c, text = "Delete", width = 20, bg = 'orange', command = del_c).grid(row = 1, column = 1, pady = 10)
		
	def delete_email(cursor)	:
		delete_e = Toplevel(delete_win)
		delete_e.title("Delete by email")
		delete_e.geometry(win_size)
		delete_e.config(bg = 'bisque')
		
		Label(delete_e, text = "Enter email you want to delete", bg = 'bisque').grid(row = 0, column = 0, pady = 10)
		email_entry = Entry(delete_e)
		email_entry.grid(row = 0, column = 1, pady = 10)
		
		def del_e()	:
			email = email_entry.get().strip()
			
			if not email	:
				messagebox.showerror("Input Error", "Field is required!")
				return
			
			cursor.execute("DELETE FROM contact WHERE email = %s;", (email,))
			
			mydb.commit()
			messagebox.showinfo("Deleted email with email ", (f"{email}"))
			delete_win.destroy()
			
		Button(delete_e, text = "Delete", width = 20, bg = 'orange', command = del_e).grid(row = 1, column = 1, pady = 10)
		
	def delete_address(cursor)	:
		delete_a = Toplevel(delete_win)
		delete_a.title("Delete by address")
		delete_a.geometry(win_size)
		delete_a.config(bg = 'navajowhite')
		
		Label(delete_a, text = "Enter address you want to delete", bg = 'navajowhite').grid(row = 0, column = 0, pady = 10)
		address_entry = Entry(delete_a)
		address_entry.grid(row = 0, column = 1, pady = 10)
		
		def del_a()	:
			address = address_entry.get().strip()
			
			if not address	:
				messagebox.showerror("Input Error", "Field is required!")
				return
			
			cursor.execute("DELETE FROM contact WHERE address LIKE %s;", (f"%address%",))
			
			mydb.commit()
			messagebox.showinfo("Deleted address with address ", (f"{address}"))
			delete_win.destroy()
			
		Button(delete_a, text = "Delete", width = 20, bg = 'orange', command = del_a).grid(row = 1, column = 1, pady = 10)
		
	try	:
		if mydb.is_connected	:
			mydb.reconnect()
			
		mydb.database = 'Contact'
		cursor = mydb.cursor()
		
	except mysql.connector.Error as e:
		messagebox.showerror("Database error: {e}")
		
	delete_win = Toplevel(gui)
	delete_win.title("Delete Contact")
	delete_win.geometry(win_size)
	delete_win.config(bg = 'lightcoral')
	
	Button(delete_win, text = "Name", width = 20, bg = 'salmon', command = lambda: delete_name(cursor)).pack(pady = 10)
	
	Button(delete_win, text = "Contact", width = 20, bg = 'mediumseagreen', command = lambda: delete_contact(cursor)).pack(pady = 10)
	
	Button(delete_win, text = "Email", width = 20, bg = 'cornflowerblue', command = lambda: delete_email(cursor)).pack(pady = 10)
	
	Button(delete_win, text = "Address", width = 20, bg = 'orchid', command = lambda: delete_address(cursor)).pack(pady = 10)
			
def exit_app(cursorObject, mydb)	:
	cursorObject.close()
	mydb.close()
	gui.destroy()
			
#GUI
gui = Tk()

gui.title("Contacts")
gui.state("zoomed")
gui.config(bg = 'lightblue')

status_label = Label(gui, text = "Connecting...", font = ("Arial", 14), bg = 'lightblue')
status_label.pack(padx = 50, pady = 10)

status_msg, status_bool, mydb = isconnected()
status_label.config(text = status_msg)

if status_bool	:
	#Create object
	cursorObject = mydb.cursor()

	#Create database and table if not exists
	cursorObject.execute('CREATE DATABASE IF NOT EXISTS Contact;')
		
	mydb.database = 'Contact'
	cursorObject.execute("CREATE TABLE IF NOT EXISTS contact (name varchar(255), number bigint UNIQUE, email varchar(255), address varchar(255));")

	welcome = Label(gui, text = "Welcome user!\n", bg = 'lightblue')
	welcome.pack(padx = 50, pady = 10)
		
	add = Button(gui, text = "Add Contact", width = 20, bg = 'lightgreen', command = lambda: add_contact(mydb))
	add.pack(padx = 50, pady = 10)

	view = Button(gui, text = "View Contact", width = 20, bg = 'lightpink', command = lambda: view_contact(mydb))
	view.pack(padx = 50, pady = 10)

	search_c = Button(gui, text = "Search Contact", width = 20, bg = 'thistle', command = lambda: search(mydb))
	search_c.pack(padx = 50, pady = 10)
	
	update = Button(gui, text = "Update Contact", width = 20, bg = 'khaki', command = lambda: update_contact(mydb))
	update.pack(padx = 50, pady = 10)

	delete_num = Button(gui, text = "Delete Contact", width = 20, bg = 'lightcoral', command = lambda: delete_number(mydb))
	delete_num.pack(padx = 50, pady = 10)

	exit = Button(gui, text = "Exit", width = 20, bg = 'red', command = lambda: exit_app(cursorObject, mydb))
	exit.pack(padx = 50, pady = 10)

	gui.mainloop()

else	:
	Label(gui, text = "Exiting because connection to MySQL is not exist\nTry again later", anchor = "center", justify = "center", bg = 'lightblue').pack()
	
	# Close after 3 seconds
	gui.after(3000, lambda: (gui.destroy(), sys.exit()))

	gui.mainloop()