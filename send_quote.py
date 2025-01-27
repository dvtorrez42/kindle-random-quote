from utils import (
    read_env_to_dict,
    parse_clippings,
    select_random_quote,
    send_to_telegram
)

DOTENV_PATH = './.env'
env_variables = read_env_to_dict(DOTENV_PATH)

API_TOKEN = env_variables['API_TOKEN']
API_URL = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage"

def main():
    for chat_id in env_variables['CHAT_ID']:
        file_path = f"./{chat_id}-My Clippings.txt"
        quotes = parse_clippings(file_path)
        # * feature 1
        # TODO: Delete short version of the same quote
        # * feature 2
        # TODO: Create sqlite db to store data from quotes dictionary
        # TODO: Every time this runs it should check if there is a new quote, if so it should add it to the database
        # TODO: Random quote should be selected from the database
        message = select_random_quote(quotes)
        send_to_telegram(
                message=message,
                api_url=API_URL,
                chat_id=chat_id
                )
    
if __name__ == "__main__":
    main()