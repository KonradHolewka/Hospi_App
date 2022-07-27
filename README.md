# Hospi_App
Hospi_App is a project of a mobile application used for registering patients' temperature chart in a hospital.

Project characteristics:
 - application works with a relational database consisting of two main tables -> one is dedicated for registered physicians, their logins, passwords & their personal data and the other one stores registered patients with their personal data,
 - each patient has a separate table on the server, containing their observation record -> body temperature, pulse, blood pressure & date/time of the measurement,
 - each patient owns a unique QR code -> the QR code includes the patient's ID, with which the patient is searched on the server,
 - the patient's observation record is visualized as a chart -> the y-axis displays the values of the measurements, while the x-axis are the timestamps of each measurement.

Technologies used in the project:
 - Python 3.7,
 - PostgreSQL 13.1 (relational database management system) -> https://www.postgresql.org/,
 - Kivy 2.1.0 (an open-source, cross-platform framework for python) -> https://kivy.org/#home.

Python libraries included in the project:
 - Pyzbar v0.1.9 -> https://pypi.org/project/pyzbar/,
 - Psycopg2 v2.8.6 -> https://pypi.org/project/psycopg2/,
 - OpenCV v4.6.0 -> https://pypi.org/project/opencv-python/,
 - Matplotlib v3.5.1 -> https://pypi.org/project/matplotlib/,
 - PyQRCode v1.2.1 -> https://pypi.org/project/PyQRCode/,
 - NumPy v1.21.5 -> https://numpy.org/.

Database hosting website -> https://www.elephantsql.com/

Current functionalities:
 - log-in and registration of physicians' accounts on the server,
 - setting up the connection to the database hosted online,
 - patient registration (including patient's name & surname, national ID code, weight, height & sex) & initialization of his/her observation record,
 - edition of patient's personal data,
 - generation of patient-specific QR code (.png format),
 - QR code scan for patient identification, that opens his/her current record, 
 - visualization of the patient's current observation record,
 - implementation of new data (including current body temperature, pulse & blood pressure), record deletion & update in case any errors appear,
 - patient deletion from the server.

In order to log-in as one of the physicians, please use the following:
 - login: macrac
 - password: racmac123

Development plans:
 - implementation of a build compatible with Android smartphones (not tested yet, currently works 100% as a desktop app),
 - corrected exception handling,
 - patient's data & blood pressure displayed on their card,
 - timestamp fix,
 - GUI improvement.

Current app version: v0.1.1
