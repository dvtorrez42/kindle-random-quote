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
        message = select_random_quote(quotes)
        send_to_telegram(
                message=message,
                api_url=API_URL,
                chat_id=chat_id
                )
    
if __name__ == "__main__":
    main()