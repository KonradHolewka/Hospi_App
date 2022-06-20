import psycopg2
from numpy import random
import datetime
import barcode
import plotdraw


#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# pobranie danych pacjenta
def patientcard_load(code):
    con, cur = polacz()

    command = "SELECT * FROM card_" + code
    cur.execute(command)
    # bierze wszystkie rekordy
    data = cur.fetchall()

    values = plotdraw.draw_plot(data)

    cur.close()
    con.close()
    return data, values

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# ewierzytelnianie
def authorization(log, pas):
    user = ''
    granted = 0

    con, cur = polacz()

    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    for r in rows:
        print (f"id {r[1]} name {r[2]}")
        if r[1] == log:
            if r[2] == pas:
                granted = 1
                user = r[0]

    # DODAĆ ERROR - BRAK SERWERA!! (psycopg2.OperationalError)
    cur.close()
    con.close()
    return granted, user

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# dodanie nowego pacjenta
def new_patient(name, surname, pesel, weight, height, sex, user_id):
    con, cur = polacz()

    # tworzenie nowego id pacjenta i sprawdzenie duplikatów
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

    # data rejestracji
    rdate_buf = datetime.datetime.now()
    registration_date = rdate_buf.strftime("%Y") + '-' + rdate_buf.strftime("%m") + '-' + rdate_buf.strftime("%d")

    # SQL insert
    command = "INSERT INTO patients (patient_id, name, surname, pesel, weight, height, registration_date, sex, user_id) \
              VALUES ('" + patient_id + "', '" + name + "', '" + surname + "', " + pesel + ", '" + weight + "', '" + \
                height + "', '" + registration_date + "', '" + sex + "', '" + user_id + "')"
    cur.execute(command)
    con.commit()

    # nowa tabela pacjenta
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

    # zamknięcie połaczenia
    cur.close()
    con.close()

    # nowy kod QR, zapisany w trajektorii /storage/emulated/0/Documents
    barcode.new_qr(patient_id)

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# dodanie nowego pomiaru
def add_measurement(temp, pulse, blood_pr,patient_id):
    con, cur = polacz()

    # data i czas rejestracji
    rdate_buf = datetime.datetime.now()
    registration_date = rdate_buf.strftime("%Y") + '-' + rdate_buf.strftime("%m") + '-' + rdate_buf.strftime("%d")
    registration_time = rdate_buf.strftime("%H") + ':' + rdate_buf.strftime("%M")

    # dzień rezydentury
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

    # zamknięcie połaczenia
    cur.close()
    con.close()
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# dane pacjenta do okna edycji
def get_pdata(patient_id):
    con, cur = polacz()

    # SELECT na danym pacjencie
    command = "SELECT * FROM patients WHERE patient_id = '" + patient_id + "'"
    cur.execute(command)
    data = cur.fetchone()
    print(data)
    # zamknięcie połaczenia
    cur.close()
    con.close()

    return data

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# nowe dane pacjenta
def edit_patient(name, surname, pesel, weight, height, sex, patient_id):
    con, cur = polacz()

    # formowanie zapytania
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

    # zamknięcie połaczenia
    cur.close()
    con.close()

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# usuwanie pomiaru
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

    # zamknięcie połaczenia
    cur.close()
    con.close()

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# edycja pojedynczego pomiaru
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

    # zamknięcie połaczenia
    cur.close()
    con.close()

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


# funkcja suplementacyjna, wprowadzic poprawne dane polaczenia!
def polacz():
    connection = psycopg2.connect(host="192.168.0.23", database="flucard_db", user="postgres", password="6938072")
    cursor = connection.cursor()
    return connection, cursor