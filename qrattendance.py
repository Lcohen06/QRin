"""
File: qrattendance.py
------------------
NOTE: Built by Luc Cohen, Western School of Technology and Environmental Science
Built for Western Tech Club attendance
"""

# QR READING:
import cv2

# QR GENERATING:
import qrcode

# DATE FORMATTING
import datetime

# FILE MANAGEMENT
import json

# Email
from email.message import EmailMessage
import ssl
import smtplib
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# IMG
from PIL import Image

# GUI
from QRin import *


# import webbrowser - open web


def scan_in():
    vid_cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    while True:
        _, img = vid_cap.read()
        data, bbox, _ = detector.detectAndDecode(img)
        if data:
            a = data
            break
        cv2.imshow("Attendance Scanner", img)
        if cv2.waitKey(1) == ord("q"):
            break
    vid_cap.release()
    cv2.destroyAllWindows()
    return a


def add_name(name):
    with open('allnames.txt', 'r+') as f:
        f_contents = f.read()
        if name.lower() not in f_contents.lower():
            generated = qrcode.make(name)
            generated.show()
            f.write(name + ', ')
            folder = r"C:/Users/lucco/Downloads/tennis_atten/qrs"
            generated.save(folder + r'/' + f"{name}.png", )
            return

            # img = Image.open(f"{name}.png") ^
            # img.show() ^

        else:
            print("Unacceptable name. Name already in system.")


def check_in():
    with open('record.json', 'r+') as rec:
        record = json.load(rec)
        name = scan_in()
        date = datetime.datetime.now()
        date = date.strftime('%x')
        if date not in record:
            record[date] = []
        if name not in record[date]:
            record[date].append(name)
        else:
            print("You have already checked in!")
        with open('record.json', 'w') as write:
            json.dump(record, write)


def check_attendance():
    choice = input("Select: Single day or entire? (D/E) ")
    if choice.lower() == 'd':
        with open('record.json') as f:
            record = json.load(f)
            print(record[datetime.datetime.now().strftime('%x')])
    elif choice.lower() == 'e':
        with open('record.json') as f:
            record = json.load(f)
            print(record)


def search_attendance():
    choice = input("Select: Single day or entire? (D/E) ")
    name = input("Enter a name to search: ")
    if choice.lower() == 'd':
        with open('record.json') as f:
            record = json.load(f)
            present = name in record[datetime.datetime.now().strftime('%x')]
            if present:
                print(f"{name} is marked present today.")
            else:
                print(f"{name} is marked absent today.")
    elif choice.lower() == 'e':
        with open('record.json') as f:
            record = json.load(f)
            count_present = 0
            days = []
            for day in record:
                if name in record[day]:
                    count_present += 1
                    days.append(day)
            print(f"{name} was marked present a total of {count_present} times.")
            print("Days present:")
            print(days)


def email():
    with open('record.json') as f:
        record = json.load(f)
    item_count_max = 0
    for item in record.values():
        if len(item) > item_count_max:
            item_count_max = len(item)
    for item in record.values():
        for i in range(item_count_max - len(item)):
            item.append('')
    df = pd.DataFrame.from_dict(record)
    df.to_csv(r'attendance.csv', index = False, header=True)
    email_sender = 'qrinbotv1.0@gmail.com'
    email_password = 'ghcctbyrmrvayqgq'
    verify = True
    while verify:
        email_receiver = input("Enter an email to send attendance: \n")
        ensure = input(f"Is this email correct?: {email_receiver}? (Y/N) ")
        if ensure.lower() == 'y':
            verify = False
    subject = 'QRin Automated Attendance Delivery'
    # body = f'''
    # Attached below is a complete copy of the QRin attendance record.
    #
    # Sent from QRin automated attendance
    # '''
    em = MIMEMultipart()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    file = "attendance.csv"
    attachment = open(file, 'rb')
    obj = MIMEBase('application', 'octet-stream')
    obj.set_payload(attachment.read())
    encoders.encode_base64(obj)
    obj.add_header('Content-Disposition', "attachment; filename= " + file)
    em.attach(obj)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())


def main():
    import winsound
    import os
    from colorama import init, Fore, Back
    import shutil
    import time
    init()
    print(Fore.GREEN + Back.BLACK)
    columns = shutil.get_terminal_size().columns

    def clearconsole():
        command = 'clear'
        if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
            command = 'cls'
        os.system(command)

    clearconsole()
    for i in range(6):
        clearconsole()
        dots = ['...', '.', '..', '...', '.', '..']
        print(" #####   ######                  #     #    #           ###  ".center(columns))
        print("#     #  #     #  #  #    #      #     #   ##          #   # ".center(columns))
        print("#     #  #     #  #  ##   #      #     #  # #         #     #".center(columns))
        print("#     #  ######   #  # #  #      #     #    #         #     #".center(columns))
        print("#   # #  #   #    #  #  # #       #   #     #    ###  #     #".center(columns))
        print("#    #   #    #   #  #   ##        # #      #    ###   #   # ".center(columns))
        print(" #### #  #     #  #  #    #         #     #####  ###    ###  ".center(columns))
        print(("Welcome" + dots[i]).center(columns))
        time.sleep(1)

    # Main Menu
    winsound.PlaySound("boot.wav", winsound.SND_FILENAME)
    menu_options = {
        1: 'Scan In',
        2: 'Add Name',
        3: 'Check Attendance',
        4: 'Search Attendance',
        5: 'Email Record',
        6: 'Exit',
    }
    print("Loading dependencies...")
    files = os.listdir( )
    for file in files:
        print(file)
        time.sleep(0.2)
    print("Gathering record file...")
    time.sleep(0.3)
    print("Loading content...")
    time.sleep(0.5)
    print("Initializing modules...")
    modules = ['cv2', 'qrcode', 'datetime', 'json', 'PIL', 'webbrowser']
    for module in modules:
        print(module)
        time.sleep(0.1)
    print('Initializing email server...')
    protocols = ['ssl', 'smtplib', 'pandas', 'email.mime.multipart', 'email.mime.base', 'email.mime.text', 'encoders']
    for protocol in protocols:
        print(protocol)
        time.sleep(0.1)
    while True:
        clearconsole()
        print("*QRin version 1.0 -- Made by Luc Cohen*")
        print("------ Menu ------")
        for key in menu_options.keys():
            print(key, '--', menu_options[key])
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number...')
            input("Press enter to acknowledge...")

        if option == 1:
            check_in()
            input("Press enter to continue...")
        elif option == 2:
            print("INSTRUCTIONS: Add a name and press enter. A QR code will appear.")
            print("Take a picture on your phone to keep.")
            print("The QR code will act like a sign-in badge. Use your QR image to scan in.")
            verify = True
            while verify:
                name = input("Please enter a name to add: ")
                ensure = input(f"Are you sure you want to add name {name}? (Y/N) ")
                if ensure.lower() == 'y':
                    verify = False
            add_name(name)
            input("Press enter to continue...")
        elif option == 3:
            check_attendance()
            input("Press enter to continue...")
        elif option == 4:
            search_attendance()
            input("Press enter to continue...")
        elif option == 5:
            from getpass import getpass
            user = 'LMC060'
            password = 'Vwup*238'
            passtrue = True
            failcount = 0
            while passtrue:
                clearconsole()
                print("Secure QRin Login Shell: ")
                userinp = getpass("User: ")
                passinp = getpass("Password: ")
                if failcount == 2:
                    print("Authentication failed! Exiting...")
                    exit()
                if userinp == user and passinp == password:
                    passtrue = False
                else:
                    failcount += 1
            clearconsole()
            email()
        elif option == 6:
            print('Exiting...')
            exit()
        else:
            print('Invalid option. Please enter a number between 1 and 6.')


if __name__ == '__main__':
    main()
