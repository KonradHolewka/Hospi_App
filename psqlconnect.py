import psycopg2
from numpy import random
import datetime
import barcode
import plotdraw


#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# patient data loading
def patientcard_load(code):
    con, cur = polacz()

    command = "SELECT * FROM card_" + code
    cur.execute(command)
    # takes all measurement records
    data = cur.fetchall()
    values = plotdraw.draw_plot(data)

    cur.close()
    con.close()
    return data, values

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# log-in authorization function
def authorization(log, pas):
    user = ''
    name = ''
    surname = ''
    granted = 0

    con, cur = polacz()

    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    print("Registered physicians in the database:")
    for r in rows:
        print(f"login {r[1]} password {r[2]} name {r[3]} surname {r[4]}")
        if r[1] == log:
            if r[2] == pas:
                granted = 1
                user = r[0]
                name = r[3]
                surname = r[4]

    # ADD THE ERROR - SERVER MISSING!! (psycopg2.OperationalError)
    cur.close()
    con.close()
    return granted, user, name, surname

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# patient addition
def new_patient(name, surname, pesel, weight, height, sex, user_id):
    con, cur = polacz()

    # new id creation & searching for duplicates
    while True:
        patient_id = str(random.randint(99999999))
        while True:
            if len(patient_id) < 8:
                patient_id = '0' + patient_id
            else:
                break
        print("ID PACJENTA: " + patient_id)
        command = "SELECT * FROM patients WHERE patient_id = '" + patient_id + "'"
        cur.execute(command)
        id_check = cur.fetchone()
        if id_check == None:
            break

    # registration date
    rdate_buf = datetime.datetime.now()
    registration_date = rdate_buf.strftime("%Y") + '-' + rdate_buf.strftime("%m") + '-' + rdate_buf.strftime("%d")

    # SQL insert
    command = "INSERT INTO patients (patient_id, name, surname, pesel, weight, height, registration_date, sex, user_id) \
              VALUES ('" + patient_id + "', '" + name + "', '" + surname + "', " + pesel + ", '" + weight + "', '" + \
                height + "', '" + registration_date + "', '" + sex + "', '" + user_id + "')"
    cur.execute(command)
    con.commit()

    # creating a new table for the patient
    command = "CREATE TABLE card_" + patient_id + " (\
    measure_id serial NOT NULL, \
    date date NOT NULL, \
    \"time\" time without time zone NOT NULL, \
    day_of_residence numeric(4,0) NOT NULL, \
    blood_pressure character varying(7) COLLATE pg_catalog.\"default\" NOT NULL, \
    temperature numeric(4,1) NOT NULL, \
    pulse numeric(3,0) NOT NULL, \
    CONSTRAINT card_" + patient_id + "_pkey PRIMARY KEY (measure_id))"
    cur.execute(command)
    con.commit()

    # connection closure
    cur.close()
    con.close()

    # new QC code, saved at the path /storage/emulated/0/Documents on Android
    barcode.new_qr(patient_id)

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# new measurement addition
def add_measurement(temp, pulse, blood_pr,patient_id):
    con, cur = polacz()

    # registration date&time
    rdate_buf = datetime.datetime.now()
    registration_date = rdate_buf.strftime("%Y") + '-' + rdate_buf.strftime("%m") + '-' + rdate_buf.strftime("%d")
    registration_time = rdate_buf.strftime("%H") + ':' + rdate_buf.strftime("%M")

    # day of residency (counted from the day of registration)
    command = "SELECT registration_date FROM patients WHERE patient_id = '" + patient_id + "'"
    cur.execute(command)
    fdate = cur.fetchone()[0]
    ldate = datetime.date(int(rdate_buf.strftime("%Y")), int(rdate_buf.strftime("%m")), int(rdate_buf.strftime("%d")))
    delta = ldate - fdate
    day_of_residence = str(delta.days + 1)

    # SQL insert
    command = "INSERT INTO card_" + patient_id + " (date, time, day_of_residence, blood_pressure, temperature, pulse) \
                VALUES ('" + registration_date + "', '" + registration_time + "', " + day_of_residence + ", '" + \
                blood_pr + "', " + temp + ", " + pulse + ")"
    cur.execute(command)
    con.commit()

    # connection closure
    cur.close()
    con.close()
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# get patient's data for edition
def get_pdata(patient_id):
    con, cur = polacz()

    # fetching the patient's data
    command = "SELECT * FROM patients WHERE patient_id = '" + patient_id + "'"
    cur.execute(command)
    data = cur.fetchone()
    print(data)

    # connection closure
    cur.close()
    con.close()

    return data

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# editing patient's data
def edit_patient(name, surname, pesel, weight, height, sex, patient_id):
    con, cur = polacz()

    # SQL query formulation
    command = "UPDATE patients SET "
    if name != "":
        buf = "name = '" + name + "', "
        command += buf
    if surname != "":
        command += "surname = '" + surname + "', "
    if pesel != "":
        command += "pesel = " + pesel + ", "
    if weight != "":
        command += "weight = '" + weight + "', "
    if height != "":
        command += "height = '" + height + "', "
    if sex != "":
        command += "sex = '" + surname + "', "
    command = command[:-2]
    command += " WHERE patient_id = '" + patient_id + "'"
    cur.execute(command)
    con.commit()

    # connection closure
    cur.close()
    con.close()

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# measurement deletion
def delete_record(index, patient_id):
    con, cur = polacz()

    if len(index) == 15:
        command = "DELETE FROM card_" + patient_id + " WHERE day_of_residence = " + index[4] + " AND time = '" + index[7:15] + "'"
    elif len(index) == 16:
        command = "DELETE FROM card_" + patient_id + " WHERE day_of_residence = " + index[4:6] + " AND time = '" + index[
                                                                                                                 8:16] + "'"
    elif len(index) == 17:
        command = "DELETE FROM card_" + patient_id + " WHERE day_of_residence = " + index[4:7] + " AND time = '" + index[9:17] + "'"
    else:
        command = "DELETE FROM card_" + patient_id + " WHERE day_of_residence = " + index[4:8] + " AND time = '" + index[10:18] + "'"


    cur.execute(command)
    con.commit()

    # connection closure
    cur.close()
    con.close()

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# measurement edition
def edit_measurement(temp, pulse, bpressure, patient_id, index):
    con, cur = polacz()

    # SQL insert
    if len(index) == 15:
        command = "UPDATE card_" + patient_id + " SET blood_pressure = '" + bpressure + "', temperature = " + temp + ", \
                            pulse = " + pulse + " WHERE day_of_residence = " + index[4] + " AND time = '" + index[
                                                                                                            7:15] + "'"
    elif len(index) == 16:
        command = "UPDATE card_" + patient_id + " SET blood_pressure = '" + bpressure + "', temperature = " + temp + ", \
                            pulse = " + pulse + " WHERE day_of_residence = " + index[4:6] + " AND time = '" + index[
                                                                                                            8:16] + "'"
    elif len(index) == 17:
        command = "UPDATE card_" + patient_id + " SET blood_pressure = '" + bpressure + "', temperature = " + temp + ", \
                            pulse = " + pulse + " WHERE day_of_residence = " + index[4:7] + " AND time = '" + index[
                                                                                                            9:17] + "'"
    else:
        command = command = "UPDATE card_" + patient_id + " SET blood_pressure = '" + bpressure + "', temperature = " + \
                            temp + ", pulse = " + pulse + " WHERE day_of_residence = " + index[4:8] + " AND time = '" + \
                            index[10:18] + "'"

    cur.execute(command)
    con.commit()

    # connection closure
    cur.close()
    con.close()

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


# connection to the database, insert appropriate connection features!
def polacz():
    connection = psycopg2.connect(host="abul.db.elephantsql.com", database="nxuliape", user="nxuliape", password="c5FT1S6m-3Cn_RRYChx40mXjFDb-uvKN")
    cursor = connection.cursor()
    return connection, cursor
