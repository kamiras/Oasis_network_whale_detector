# Oasis Network Whale Detector

This project was made by kamiras. Feel free to use, change and ask everything that you want.

## Features

**Monitoring of the Oasis Network Blockchain**

- Every second the script checks 2 times the Blockchain with the staking.Transfer method, which is the quivalent of a transaction.

**API's**

- Twitter API
- Coinbase API
- oasisscan API

**Automated Tweets**

- The bot tweets transactions over 100000 dollars by default.
- Every 24 Hours the bot tweets a rank of the 3 highest transactions of the Network (22:00 EU).

**Database**

- 1 Databse
- 1 Table
- 3 Columns

## Installation

```
pip install -r .\requirements.txt
```

## Usage

Execute the **whale.py**

```
python3 whale.py
```   
