# Minimal API for the COVID Booking System of the Offices at the UniPD Math Dep 

Currently for registering the presence at the math department you have to manually login into the math website and fill several forms EVERY day. In order to speedup this process, this project proposes a minimal interface of the COVID booking system of the math unipd website that you can use the simple API written in Python.

```
If you use the code of this repo and you find this project useful, 
please consider to give a star ⭐!
```

# Using the Telegram Bot
From Telegram search for `math-unipd-booking` and start using the bot!

### Example of Usage
```bash
# start the bot, see main commands
/start

# book registration
/book --user math_username --pwd math_password --this_week

# check registration
/check --user math_username --pwd math_password --tomorrow --arrival 9 --departure 18

# remove registration
/remove --user math_username --pwd math_password --office 702 --next_week
```

### Main commands
`/book`, `/check`, `/remove`

### Main Params
`--user`, `--pwd`, `--today` `--tomorrow`, `--this_week`, `--next_week`, `--this_month`, `--next_month`, `--arrival`, `--departure`, `--office`, `--guests`, `--month`, `--year`

<details>
<summary>Contributing to the Math-Unipd-Booking Python API</summary>

### Requirements
- You have to clone the repo:
```bash
# clone the repo
git clone https://github.com/guglielmocamporese/math-unipd-booking-bot.git

# go the project folder
cd math-unipd-booking-bot
```
- You have to use Python 3.x (specifially I used Python 3.7, but 3.x should be ok),
- You need the `lxml`, `pandas` and `python-telegram-bot` packages installed,
- You need to extend the permissions for the bash scripts:
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
usage: ['--help'] [-h] [--mode {book,check,remove}] [--year {2020,2021,2022}]
                  [--month {1,2,3,4,5,6,7,8,9,10,11,12}] [--day DAY]
                  [--arrival {7,8,9,10,11,12,13,14,15,16,17,18}]
                  [--departure {8,9,10,11,12,13,14,15,16,17,18,19}]
                  [--office OFFICE] [--guests GUESTS] [--today] [--tomorrow]
                  [--this_week] [--next_week] [--this_month] [--next_month]
                  [--user USER] [--pwd PWD]

optional arguments:
  -h, --help            show this help message and exit
  --mode {book,check,remove}
                        Year of the booking.
  --year {2020,2021,2022}
                        Year of the booking.
  --month {1,2,3,4,5,6,7,8,9,10,11,12}
                        Month number of the booking.
  --day DAY             Day of the booking.
  --arrival {7,8,9,10,11,12,13,14,15,16,17,18}
                        Time of arrival (h) of the booking.
  --departure {8,9,10,11,12,13,14,15,16,17,18,19}
                        Time of departure (h) of the booking.
  --office OFFICE       Office number.
  --guests GUESTS       Guests names (optional).
  --today               Use today as the time reference.
  --tomorrow            Use tomorrow as the time reference.
  --this_week           Use this week as the time reference.
  --next_week           Use next week as the time reference.
  --this_month          Use this month as the time reference.
  --next_month          Use next month as the time reference.
  --user USER           Math username.
  --pwd PWD             Math password.
```


### TODO
- [X] Implemented a Telegram Bot that handles bookings,
- [ ] Implemented a Slack Bot that handles bookings,
- [ ] Extend the code on different web browser other than Chrome,
- [ ] Add functionalities (booking statistics, ...)
</details>

