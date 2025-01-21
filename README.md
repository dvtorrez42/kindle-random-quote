# Random Quote from Kindle Bot

**Description**

`send_quote.py` reads and parses kindle clippings, selects one at random and sends it via a the Telegram Bot API.
Messages can be sent to as many `CHAT_ID`s as present in the `.env` file like so:
```
API_TOKEN=<Bot's API Token>

CHAT_ID=<CHAT_ID_1> # Person 1
CHAT_ID=<CHAT_ID_2> # Person 2
CHAT_ID=<CHAT_ID_N> # Person n
```

**Requires**:

1. Telegram bot and it's API token (in a `.env` file).
2. Telegram Chat ID's to send the quotes to (in a `.env` file).
3. "My Clippings.txt" file from Kindle renamed like so: `<CHAT_ID_N>-My Clippings.txt`