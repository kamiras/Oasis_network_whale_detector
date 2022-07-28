# Oasis Network Whale Detector

The reason of this project is to analyze **in live** the Oasis Network Blockchain to find the most valuable transactions and report it instantly. This could help to the community and investors to find the behaviour of the network daily.

This project was made by kamiras. Feel free to use, change and ask everything that you want.

## Features

**Monitoring of the Oasis Network Blockchain**

- Every second the script checks 2 times the Blockchain with the staking.Transfer method, which is the quivalent of a transaction.

**API's**

- Twitter API
- Coinbase API
- Kucoin API
- oasisscan API

**Automated Tweets**

- The bot tweets transactions over **60000 dollars** by default.
- Every 24 Hours the bot tweets a rank of the 3 highest transactions of the Network (22:00 EU).

**Weekly Chart**

- Each Saturday at 20:00 pm the bot posts a tweet with the **Top 10 Validators of the Network.**

**Database and example.py**

- 1 Database
- 1 Table
- 4 Columns

example.py: As the name says it is an example that you could follow to create the database. Rather than doing an .sql script I chose to do it with python for its simplicity.

## What do you consider a whale transaction?

- We consider a whale a transaction that overpasses the 1,200,000 ROSE. ~60k USD (14/07/2022). This number will be increased eventually.


## Installation

```
pip install -r .\requirements.txt
```

## Usage

Execute the **whale.py**

```
python3 whale.py
```   
