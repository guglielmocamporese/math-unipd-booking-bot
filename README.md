# Minimal API for the COVID Booking System of the Offices at the UniPD Math Dep 

Currently for registering the presence at the math department you have to manually login into the math website, fill several forms EVERY day. In order to speedup this process and create an interface to the website that you can use the simple API written in Python.

### Requirements
- You have to clone the repo:
```console
# clone the repo
git clone https://github.com/guglielmocamporese/math-unipd-booking.git

# go the project folder
cd math-unipd-booking
```
- You have to use Python 3.x (specifially I used Python 3.7, but 3.x should be ok),
- You have to have Chrome (for now the code supports only this web browser),
- You have to download `chromedriver` form [[here](https://chromedriver.chromium.org/downloads)] (search for the version compatible with your Chrome version), and move the extracted file into the project folder `math-unipd-booking`,
- Extend the permissions for the bash scripts:
```console
chmod +x ./book ./check ./remove
```

### Example of Usage
```python
# Book the office
./book # book the office 732 from 9:00 to 18:00, today
./book --office 702 --tomorrow # book the office 702 from 9:00 to 18:00, tomorrow
./book --tomorrow -ta 10 -td 19 # book the office 732 from 10:00 to 19:00, tomorrow
./book --next_week # book the office 732 from 9:00 to 18:00, all the next week
./book --this_month # book the office 732 from 9:00 to 18:00, all this month

# Check reservations
./check --this_month # check all my reservations of this month in office 732

# Remove reservations
./remove --this_week # remove all my reservations of this week in office 732
```

### TODO
- Extend the code on different web browser other than Chrome,
- Add functionalities (booking statistics, ...)