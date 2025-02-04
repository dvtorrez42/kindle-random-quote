from utils import (
    read_env_to_dict,
    parse_clippings,
    #select_random_quote,
    send_to_telegram
)

from db_utils import (
    #Quotes,
    Session,
    create_db_and_tables,
    add_quote_if_not_exists,
    get_random_quote
)

DOTENV_PATH = './.env'
env_variables = read_env_to_dict(DOTENV_PATH)

API_TOKEN = env_variables['API_TOKEN']
API_URL = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage"

def main():
    
    # Create database and engine
    engine = create_db_and_tables(db_path="quotes.db")
    
    for chat_id in env_variables['CHAT_ID']:
        file_path = f"./{chat_id}-My Clippings.txt"
        quotes_dict_list = parse_clippings(file_path, chat_id)
        # * feature 1
        # TODO: Delete short version of the same quote
        
        # Try to add the quote
        with Session(engine) as session:
            for quotes_dict in quotes_dict_list:
                was_added = add_quote_if_not_exists(session, quotes_dict)
                if was_added:
                    print(f"Quote from '{quotes_dict['title']}' by {quotes_dict['author']} added successfully.")
                else:
                    continue 
                
        random_quote = get_random_quote(engine)
        
        message = (  
            f'>{random_quote["quote"]} \n\n'
            f'\\- {random_quote["author"]} \n\n'
            f'*Libro*: _"{random_quote["title"]}"_ \n\n'
            f'Subrayada el {random_quote["date_added"]} \n'
        )
        
        send_to_telegram(
                message=message,
                api_url=API_URL,
                chat_id=chat_id
                )
    
if __name__ == "__main__":
    main()