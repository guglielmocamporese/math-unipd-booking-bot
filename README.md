# Minimal API for the COVID Booking System of the Offices at the UniPD Math Dep 

Currently for registering the presence at the math department you have to manually login into the math website and fill several forms EVERY day. In order to speedup this process, this project proposes a minimal interface of the COVID booking system of the math unipd website that you can use the simple API written in Python.

```
If you use the code of this repo and you find this project useful, please consider to give a star ⭐!
```

# Booking with the Telegram Bot
From Telegram search for `math-unipd-booking` and start using the bot!

### Example of Usage
```bash
/book --user math/username --pwd math/password --this_week
/check --user math/username --pwd math/password --tomorrow --arrival 9 --departure 18
/remove --user math/username --pwd math/password --office 702 --next_week
```


# Booking with the Python API
### Requirements
- You have to clone the repo:
```bash
# clone the repo
git clone https://github.com/guglielmocamporese/math-unipd-booking.git

# go the project folder
cd math-unipd-booking
```
- You have to use Python 3.x (specifially I used Python 3.7, but 3.x should be ok),
- You need the `selenium` package (this is a python package for interacting with web pages):
```bash
# install selenium
pip install selenium
```
- You have to have Chrome (for now the code supports only this web browser),
- You have to download `chromedriver` form [[here](https://chromedriver.chromium.org/downloads)] (search for the version compatible with your Chrome version), and move the extracted file into the project folder `math-unipd-booking`,
- Extend the permissions for the bash scripts:
```bash
# extend files permissions
chmod +x ./scripts/book ./scripts/check ./scripts/remove
```

### Example of Usage
```bash
# Book the office
./scripts/book # book the office 732 from 9:00 to 18:00, today
./scripts/book --office 702 --tomorrow # book the office 702 from 9:00 to 18:00, tomorrow
./scripts/book --next_week -ta 10 -td 19 # book the office 732 from 10:00 to 19:00, all the next week
./scripts/book --this_month # book the office 732 from 9:00 to 18:00, all this month

# Check reservations
./scripts/check --this_month # check all my reservations of this month in office 732

# Remove reservations
./scripts/remove --this_week # remove all my reservations of this week in office 732
```

Here all the input arguments that are supported:
```bash
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

# Contributing

### TODO
- [X] Implemented a Telegram Bot that handles bookings,
- [ ] Extend the code on different web browser other than Chrome,
- [ ] Add functionalities (booking statistics, ...)
