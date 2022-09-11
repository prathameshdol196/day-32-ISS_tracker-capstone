import time
import requests
from datetime import datetime
import smtplib

MY_LAT = 0.00000  # Your latitude
MY_LONG = 0.00000  # Your longitude

my_email = "Sender Email Address"
password = "Sender Email Password"

def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")  # api that fatches the ISS live location
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    time.sleep(1)
    print(f"ISS LATITUDE {iss_latitude}")
    time.sleep(1)
    print(f"ISS LONGITUDE {iss_longitude}")
    time.sleep(1)
    print(f"My current location {MY_LAT, MY_LONG}")

    # Your position is within +5 or -5 degrees of the ISS position.
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True

def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour


while True:
    time.sleep(4)
    if is_iss_overhead() and is_night():
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(my_email, password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=my_email,
            msg="Subject:Look Up \n\nThe ISS is above your head"
        )
    time.sleep(1)
    print("project status running stay connected don't close program")
    print("A mail will be sent to you when ISS is closer to you, if it's night")
    print("\n")


