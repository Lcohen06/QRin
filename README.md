# QRin V1.0
QRin V1.0 attendance based system. A streamlined, intuitive system for digital club attendance and attendance management. 
Utilizes qrcode creation and decoding as well as local file databases to store daily attendance records. Email functionality
designed and executed using SMTP protocol client and EMAIL.MIME framework for file attachment.
Designed for club use at Western School of Technology and Environmental Science. 
> *Copywrite 2022 Luc Cohen*

## INSTALLATION:
 - Initialize a **local** powershell shell

 - Download project, install required modules: cv2, qrcode, smtplib, Colorama, datetime, json, PIL using the command below:
     - ```$ python -m pip install qrcode opencv-contrib-python pillow pandas colorama smtplib json matplotlib```
 
 - Run the following command:
     - ```py ./qrattendance.py```
