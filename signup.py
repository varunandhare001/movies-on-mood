from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import pymysql
import smtplib


# function part

# def user_enter(event):
#     if usernameEntry.get()=='Username':
#         usernameEntry.delete(0,END)

# def password_enter(event):
#     if passwordEntry.get()=='password':
#         passwordEntry.delete(0,END)

def clear():
    emailEntry.delete(0, END)
    userEntry.delete(0, END)
    passwordEntry.delete(0, END)
    confirmEntry.delete(0, END)


def login_page():
    sign_window.destroy()
    import signin


def connect_database():
    if emailEntry.get() == '' or userEntry.get() == '' or passwordEntry.get() == '' or confirmEntry.get() == '':
        messagebox.showerror('Error', 'All fields are required')
    elif passwordEntry.get() != confirmEntry.get():
        messagebox.showerror('Error', 'Password Mismatch')
    else:
        try:
            con = pymysql.connect(host='localhost', user='root', password='ektejivan001')
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error', 'Database Connectivity issue, please try again later')
            return
        try:
            query = 'create database userdata'
            mycursor.execute(query)
            query = 'use userdata'
            mycursor.execute(query)
            query = 'create table data(id int auto_increment primary key not null, email varchar(50),username varchar(100),password varchar(20))'
            mycursor.execute(query)
        except:
            mycursor.execute('use userdata')
        query = 'select * from data where username=%s'
        mycursor.execute(query, (userEntry.get()))

        row = mycursor.fetchone()
        if row != None:
            messagebox.showerror('Error', 'Username Already exists')

        else:
            query = 'insert into data(email,username,password) values(%s,%s,%s)'
            mycursor.execute(query, (emailEntry.get(), userEntry.get(), passwordEntry.get()))
            con.commit()
            con.close()
            messagebox.showinfo('Success', 'Registration is successfull')
            clear()
            sign_window.destroy()
            import signin


# i have tried to send email function but because we can't give two commands to single button
# we will work on it later

def send_email():
    sender_email = "varunandhare314@gmail.com"
    sender_password = "Ektejivan@001"

    server = smtplib.SMTP('smtp.gmail.com', 587)

    server.starttls()

    server.login(sender_email, sender_password)

    print("login successful")

    emailEntry = emailEntry.get()

    server.sendmail(sender_email, emailEntry)

    print("msg sent")

    emailEntry.delete(0, END)


# import smtplib
# from email.mime.text import MIMEText

# # ... your existing code ...

# # Function to send a welcome email
# def send_welcome_email(email):
#     # Replace these values with your email configuration
#     smtp_server = 'your_smtp_server'
#     smtp_port = 587
#     smtp_username = 'your_username'
#     smtp_password = 'your_password'
#     sender_email = 'your_sender_email'

#     # Create the email message
#     subject = "Welcome to Movies on Mood!"
#     body = "Thank you for signing up on Movies on Mood. Enjoy exploring movies based on your mood!"
#     message = MIMEText(body)
#     message['Subject'] = subject
#     message['From'] = sender_email
#     message['To'] = email

#     # Connect to the SMTP server and send the email
#     with smtplib.SMTP(smtp_server, smtp_port) as server:
#         server.starttls()
#         server.login(smtp_username, smtp_password)
#         server.sendmail(sender_email, [email], message.as_string())

# # Modify your signup function to call send_welcome_email
# def signup():
#     # Your existing signup logic

#     # After successful registration, send a welcome email
#     send_welcome_email(user_email.get())

# # ... rest of your code ...

# gui part
sign_window = Tk()
sign_window.geometry('2560x1600')
sign_window.title('signin Page')

bg_image = Image.open('bg11.jpg')
bg_image = bg_image.resize((1660, 800))
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = Label(sign_window, image=bg_photo)
bg_label.pack(expand="true", fill="both")

heading = Label(sign_window, text='CREATE AN ACCOUNT', font=('Times Now Romen', 23, 'bold'), bg='ghost white',
                fg='gray17')
heading.place(x=585, y=124)

emailLabel = Label(text='Email', font=('Times now roman', 10, 'bold'), bg='ghost white', fg='gray17')
emailLabel.place(x=615, y=160)

emailEntry = Entry(width=25, font=('Times now roman', 10, 'bold'), bg='ghost white', fg='gray17')
emailEntry.place(x=615, y=182)

userLabel = Label(text='Username', font=('Times now roman', 10, 'bold'), bg='ghost white', fg='gray17')
userLabel.place(x=615, y=210)

userEntry = Entry(width=25, font=('Times now roman', 10, 'bold'), bg='ghost white', fg='gray17')
userEntry.place(x=615, y=235)

passwordLabel = Label(text='Password', font=('Times now roman', 10, 'bold'), bg='ghost white', fg='gray17')
passwordLabel.place(x=615, y=265)

passwordEntry = Entry(width=25, font=('Times now roman', 10, 'bold'), bg='ghost white', fg='gray17')
passwordEntry.place(x=615, y=290)

confirmLabel = Label(text='Confirm Password', font=('Times now roman', 10, 'bold'), bg='ghost white', fg='gray17')
confirmLabel.place(x=615, y=320)

confirmEntry = Entry(width=25, font=('Times now roman', 10, 'bold'), bg='ghost white', fg='gray17')
confirmEntry.place(x=615, y=345)
# usernameEntry=Entry(sign_window,font=('Times Now Romen',13,'bold'),bg='ghost white',fg='gray17')
# usernameEntry.place(x=927, y=170)
# usernameEntry.insert(0,'Username')

# usernameEntry.bind('<FocusIn>',user_enter)

# passwordEntry=Entry(sign_window,font=('Times Now Romen',13,'bold'),bg='ghost white',fg='gray17')
# passwordEntry.place(x=927, y=220)
# passwordEntry.insert(0,'password')

# passwordEntry.bind('<FocusIn>',password_enter)

# forgetButton=Button(sign_window,text='Forgot Password',bd=0,activebackground='ghost white',cursor='hand2',font=('times now roman',12,'bold'),bg='ghost white',fg='gray17',width=18)
# forgetButton.place(x=927,y=270)

signupButton = Button(sign_window, text='Sign Up', font=('Open Sans', 16, 'bold'), fg='gray17', bg='firebrick1',
                      cursor='hand2', width=14, command=connect_database)
signupButton.place(x=615, y=380)

# signupButton=Button(sign_window,text='Sign Up',font=('Open Sans',16,'bold'),fg='gray17',bg='firebrick1',cursor='hand2',width=14,command=send_email)
# signupButton.place(x=615,y=380)

alreadyLabel = Label(sign_window, text="already have an account?", font=('Times Now Romen', 16,), bg='ghost white',
                     fg='gray17')
alreadyLabel.place(x=615, y=422)

alreadyButton = Button(sign_window, text='Log in', font=('Open Sans', 14, 'bold underline'), fg='gray17',
                       bg='firebrick1', cursor='hand2', command=login_page)
alreadyButton.place(x=670, y=455)

sign_window.mainloop()
