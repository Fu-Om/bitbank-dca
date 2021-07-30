# DCA scripts for bitbank

### Description

An automatic DCA script for bitbank. Change the parameters to fit your needs.

A `log.csv` file will be created.

### How to run.

Create virtual env.

```
# from top dir
python3 -m venv .env
.env/bin/activate
pip install -r requirements.txt
# `deactivate` to quit virtualenv 
```

Create a file named `script/settings.py`. Example is given as `script/settings_example.py`.

### DO NOT UPLOAD settings.py (CREDENTIALS) !

Run with cron.

```
crontab -e
# add the following line to execute daily at 6 am. 
# m h  dom mon dow   command 
6 * * * path/to/run.sh 
```

### Parameters

- dca.py

```
# In the main function
unit = 5000  # unit of rounding order
"""
e.g. When the current price is 4,502,000 order will be at 4500000.
The current price is 45070000 order will be at 45050000.
When divisible by unit, the order will be 2,000 less than the current price.
"""
dca_amount = 3000  # jpy to buy for each day
log_file_path = pathlib.Path.home() / 'Devel/bitbank-dca/log.csv'  # log file path
```

