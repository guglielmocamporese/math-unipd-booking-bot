# Minimal API for the COVID Booking System of the Offices at the UniPD Math Dep 

Currently for registering the presence at the math department you have to manually login into the math website and fill several forms EVERY day. In order to speedup this process, this project proposes a minimal interface of the COVID booking system of the math unipd website that you can use the simple API written in Python.

If you use the code of this repo and you find this project useful, please consider to give a star ⭐!

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
```console
# Book the office
./book # book the office 732 from 9:00 to 18:00, today
./book --office 702 --tomorrow # book the office 702 from 9:00 to 18:00, tomorrow
./book --next_week -ta 10 -td 19 # book the office 732 from 10:00 to 19:00, all the next week
./book --this_month # book the office 732 from 9:00 to 18:00, all this month

# Check reservations
./check --this_month # check all my reservations of this month in office 732

# Remove reservations
./remove --this_week # remove all my reservations of this week in office 732
```

Here all the input arguments that are supported:
```console
  -h, --help            show this help message and exit
  --mode {book,check,remove}
                        Year of the booking.
  --year {2020,2021,2022}, -y {2020,2021,2022}
                        Year of the booking.
  --month {1,2,3,4,5,6,7,8,9,10,11,12}, -m {1,2,3,4,5,6,7,8,9,10,11,12}
                        Month number of the booking.
  --day DAY, -d DAY     Day of the booking.
  --arrival {7,8,9,10,11,12,13,14,15,16,17,18}, -ta {7,8,9,10,11,12,13,14,15,16,17,18}
                        Time of arrival (h) of the booking.
  --departure {8,9,10,11,12,13,14,15,16,17,18,19}, -td {8,9,10,11,12,13,14,15,16,17,18,19}
                        Time of departure (h) of the booking.
  --office OFFICE, -o OFFICE
                        Office number.
  --guests GUESTS, -g GUESTS
                        Guests names (optional).
  --today               Use today as the time reference.
  --tomorrow            Use tomorrow as the time reference.
  --this_week           Use this week as the time reference.
  --next_week           Use next week as the time reference.
  --this_month          Use this month as the time reference.
  --next_month          Use next month as the time reference.
```

### TODO
- Extend the code on different web browser other than Chrome,
- Add functionalities (booking statistics, ...)
