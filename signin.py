from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import pymysql
import subprocess
import sys


# function part

def forget_pass():
    global bgpic, window

    def change_password():
        entered_username = usernameEntry.get().strip()  # Remove any leading/trailing whitespaces
        # print(f"Entered Username: {entered_username}")

        if entered_username == '' or newpassEntry.get() == '' or confirmpassEntry.get() == '':
            messagebox.showerror('Error', 'All fields are required', parent=window)
        elif newpassEntry.get() != confirmpassEntry.get():
            messagebox.showerror('Error', 'Password is not matching', parent=window)
        else:
            con = pymysql.connect(host='localhost', user='root', password='ektejivan001', database='userdata')
            mycursor = con.cursor()
            query = 'select * from data where username=%s COLLATE utf8mb4_general_ci'
            mycursor.execute(query, (entered_username,))
            row = mycursor.fetchone()
            # print(f"Retrieved Row: {row}")
            if row == None:
                messagebox.showerror('Error', 'Incorrect Username', parent=window)
            else:
                query = 'update data set password=%s where username=%s'
                mycursor.execute(query, (newpassEntry.get(), entered_username))
                con.commit()
                con.close()
                messagebox.showinfo('Success', 'Password is reset, please login with new password', parent=window)
                window.destroy()

    window = Toplevel()
    window.title('change password')

    # bgpic = ImageTk.PhotoImage(file='bg11.jpg')

    bg_image = Image.open('bg11.jpg')
    bg_image = bg_image.resize((1660, 800))
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = Label(window, image=bg_photo)
    bg_label.pack(expand="true", fill="both")

    # bgLabel = Label(window, image=bgpic)
    # bgLabel.grid()

    heading = Label(window, text='Reset Password', font=('Times Now Romen', 20, 'bold'), bg='ghost white', fg='gray17')
    heading.place(x=630, y=125)

    userLabel = Label(window, text='Username', font=('Times Now Romen', 16,), bg='ghost white', fg='gray17')
    userLabel.place(x=615, y=162)

    usernameEntry = Entry(window, font=('Times Now Romen', 13, 'bold'), bg='ghost white', fg='gray17')
    usernameEntry.place(x=615, y=195)

    newpassLabel = Label(window, text='New Password', font=('Times Now Romen', 16,), bg='ghost white', fg='gray17')
    newpassLabel.place(x=615, y=231)

    newpassEntry = Entry(window, font=('Times Now Romen', 13, 'bold'), bg='ghost white', fg='gray17')
    newpassEntry.place(x=615, y=265)

    confirmpassLabel = Label(window, text='Confirm password', font=('Times Now Romen', 16,), bg='ghost white',
                             fg='gray17')
    confirmpassLabel.place(x=615, y=300)

    confirmpassEntry = Entry(window, font=('Times Now Romen', 13, 'bold'), bg='ghost white', fg='gray17')
    confirmpassEntry.place(x=615, y=335)

    submitButton = Button(window, text='Submit', font=('Open Sans', 16, 'bold'), fg='gray17', bg='firebrick1',
                          cursor='hand2', width=14, command=change_password)
    submitButton.place(x=615, y=380)

    window.mainloop()


def user_enter(event):
    if usernameEntry.get() == 'Username':
        usernameEntry.delete(0, END)


def password_enter(event):
    if passwordEntry.get() == 'password':
        passwordEntry.delete(0, END)


def signup_page():
    login_window.destroy()
    import signup


def main_page():
    if usernameEntry.get() == '' or passwordEntry.get() == '':
        messagebox.showerror('Error', 'All Fields Are Required')

    else:
        try:
            con = pymysql.connect(host='localhost', user='root', password='ektejivan001')
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error', 'Connection is not established Try again')
            return
        query = 'use userdata'
        mycursor.execute(query)
        query = 'select * from data where username=%s and password=%s'
        mycursor.execute(query, (usernameEntry.get(), passwordEntry.get()))
        row = mycursor.fetchone()
        if row == None:
            messagebox.showerror('Error', 'Invalid username or password')
        else:
            # messagebox.showinfo('Welcome','Login is succesful')
            # Run main.py using subprocess
            login_window.destroy()

            subprocess.run([sys.executable, '/Users/varunandhare/PycharmProjects/PythonProject/PythonProject/main.py'])

        # gui part


login_window = Tk()
login_window.geometry('2560x1600')
login_window.title('Login Page')

bg_image = Image.open('bg11.jpg')
bg_image = bg_image.resize((1500, 800))
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = Label(login_window, image=bg_photo)
bg_label.pack(expand="true", fill="both")

# ocean_blue = "#0077cc"

heading = Label(login_window, text='USER LOGIN', font=('Times Now Romen', 28, 'bold'), bg='ghost white', fg='gray17')
heading.place(x=630, y=125)

usernameEntry = Entry(login_window, font=('Times Now Romen', 13, 'bold'), bg='ghost white', fg='gray17')
usernameEntry.place(x=615, y=180)
usernameEntry.insert(0, 'Username')

usernameEntry.bind('<FocusIn>', user_enter)

passwordEntry = Entry(login_window, font=('Times Now Romen', 13, 'bold'), bg='ghost white', fg='gray17')
passwordEntry.place(x=615, y=230)
passwordEntry.insert(0, 'password')

passwordEntry.bind('<FocusIn>', password_enter)

# root = Tk()
bgpic = None
forgetButton = Button(login_window, text='Forgot Password', bd=0, activebackground='gray17', cursor='hand2',
                      font=('times now roman', 12, 'bold'), bg='ghost white', fg='gray17', width=18,
                      command=forget_pass)
forgetButton.place(x=615, y=280)

loginButton = Button(login_window, text='Login', font=('Open Sans', 16, 'bold'), fg='gray17', bg='ghost white',
                     cursor='hand2', width=14, command=main_page)
loginButton.place(x=615, y=330)

signupLabel = Label(login_window, text="don't have an account?", font=('Times Now Romen', 18,), bg='ghost white',
                    fg='gray17')
signupLabel.place(x=615, y=385)

newaccountButton = Button(login_window, text='Create new one', font=('Open Sans', 14, 'bold underline'), fg='gray17',
                          bg='firebrick1', cursor='hand2', command=signup_page)
newaccountButton.place(x=640, y=430)

login_window.mainloop()
