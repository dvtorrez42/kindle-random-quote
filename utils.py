import re
import random
import requests

def read_env_to_dict(file_path):
    """
    Reads a .env file and converts its contents into a dictionary.

    Parses the file line by line, removing comments and whitespace, and processes
    key-value pairs. Handles duplicate keys by storing their values in a list.

    Args:
        file_path (str): The path to the .env file to be read.

    Returns:
        dict: A dictionary containing key-value pairs from the .env file.
              If a key appears multiple times, its values are stored in a list.

    Example:
        Given a `.env` file with the following content:
            ```
            KEY1=value1
            KEY2=value2 # This is a comment
            KEY3="value3"
            KEY1=value4
            ```

        The function will return:
            {
                "KEY1": ["value1", "value4"],
                "KEY2": "value2",
                "KEY3": "value3"
            }
    """
    env_dict = {}
    with open(file_path, 'r') as file:
        for line in file:
            # Remove comments and whitespace
            line = line.split('#')[0].strip()
            if '=' in line:
                key, value = line.split('=', 1)
                # Remove quotes around the value if they exist
                value = value.strip("'").strip('"')
                if key in env_dict:
                    if not isinstance(env_dict[key], list):
                        env_dict[key] = [env_dict[key]]
                    env_dict[key].append(value)
                else:
                    env_dict[key] = value
    return env_dict

def clean_text_4_markdown(dirty_text):
    """
    Cleans a given text for safe use in Telegram's MarkdownV2 by escaping special characters.
    
    Args:
        dirty_text (str): The input text that may contain characters requiring escaping for Markdown compatibility.
    
    Return:
        str: The cleaned text with special Markdown character escaped.
        
    Example:
        >>> clean_text_4_markdown("_Markdown_ text with *special* characters!")
        '\\_Markdown\\_ text with \\*special\\* characters!'
    """
    # Characters to escape
    chars_to_escape = r"_\*\[\]\(\)~`>#\+\-=|{}\.\!"
    
    # Escape each character
    dirty_text = dirty_text.strip().lstrip('\ufeff')
    cleaned_text = re.sub(f"([{re.escape(chars_to_escape)}])", r"\\\1", dirty_text)
    return cleaned_text

def parse_clippings(file_path, chat_id):
    """
    Parses a Kindle clippings file and extracts quotes along with their metadata.

    This function reads the content of a Kindle clippings file, splits it into individual entries, 
    and uses regular expressions to extract relevant data such as the book title, author, 
    position, date added, and the quote itself. The extracted data is returned as a list of dictionaries.

    Args:
        file_path (str): The path to the Kindle clippings file.

    Returns:
        list: A list of dictionaries, where each dictionary contains the following keys:
            - 'title' (str): The title of the book.
            - 'author' (str): The author of the book.
            - 'position' (str): The position in the book where the quote is located.
            - 'date_added' (str): The date the quote was added.
            - 'quote' (str): The actual text of the quote.

    Example:
        Given a clippings file with the following entry:
            ```
            Book Title (Author Name)
            - Your Highlight on page 5 | position 100-101 | Added on Tuesday, January 1, 2023

            This is a sample quote.
            ==========
            ```

        The function will return:
            [
                {
                    'title': 'Book Title',
                    'author': 'Author Name',
                    'position': '100-101',
                    'date_added': 'Tuesday, January 1, 2023',
                    'quote': 'This is a sample quote.'
                }
            ]
    """
    
    chat_id_dict = {
        "831778701": "Dani",
        "6214991004": "Pau",
        "971556400": "Fecho"
    }
    
    # Initialize an empty list to stores parsed quotes
    parsed_data = []
    
    with open(file_path, 'r', encoding='utf-8-sig') as file:  # Handle BOM
        # Read the file and split by '==========='
        entries = file.read().split('==========')
        
        for entry in entries:
            
            # Use regex to parse each quote entry
            match = re.search(r"(.*?) \((.*?)\)\n- .*posición (\d+(-\d+)?) \| Añadido el (.*?)\n\n(.*)", entry, re.DOTALL)
            if match:
                title = clean_text_4_markdown(match.group(1))
                author = clean_text_4_markdown(match.group(2))
                position = clean_text_4_markdown(match.group(3))
                date_added = clean_text_4_markdown(match.group(5))
                quote = clean_text_4_markdown(match.group(6))
                
                parsed_data.append({
                    'lectore': chat_id_dict[chat_id],
                    'title': title,
                    'author': author,
                    'position': position,
                    'date_added': date_added,
                    'quote': quote
                })
    return parsed_data

def send_to_telegram(message, api_url, chat_id):
    """
    Sends a message to a Telegram chat using the Telegram Bot API.

    This function posts a message to a specified Telegram chat by sending a request 
    to the Telegram Bot API. The message is formatted using MarkdownV2.

    Args:
        message (str): The message to send, formatted in MarkdownV2.
        api_url (str): The Telegram Bot API URL, typically in the format 
                       `https://api.telegram.org/bot<token>/sendMessage`.
        chat_id (str or int): The unique identifier for the target chat or 
                              username of the target channel (prefixed with `@`).

    Returns:
        None

    Raises:
        Exception: If an error occurs during the HTTP request, the exception is caught 
                   and printed to the console.

    Example:
        send_to_telegram(
            message="Hello, Telegram!",
            api_url="https://api.telegram.org/bot<your_token>/sendMessage",
            chat_id="123456789"
        )
    """
    try:
        response = requests.post(api_url, json={'chat_id':chat_id, 'text':message, 'parse_mode':'MarkdownV2'})
        print(response.text)
    except Exception as e:
        print(e)