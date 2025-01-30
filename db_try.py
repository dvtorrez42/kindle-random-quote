from sqlmodel import SQLModel, Field, Session, create_engine, select
import os

# Step 1: Define the database model
class Quotes(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str 
    author: str
    position: str
    date_added: str
    quote: str
    
def create_db_and_tables(db_path: str = "prueba.db"):
    """Create database and table if they don't exist"""
    engine = create_engine(f"sqlite:///{db_path}")
    if not os.path.exists(db_path):
        SQLModel.metadata.create_all(engine)
    else:
        return engine

def add_quote_if_not_exists(session:Session, data_dict:dict):
    """
    Add a quote to the database if it doesn't exists.
    Returns True if quote was added, False if it already existed.
    """
    # Check if quote already exists
    statement = select(Quotes).where(Quotes.quote == data_dict["quote"])
    existing_quote = session.exec(statement).first()
    
    if existing_quote is None:
        # Quote doen't exist, add it
        quote = Quotes(**data_dict)
        session.add(quote)
        session.commit()
        session.refresh(quote)
        return True
    else:
        return False
    
    # Create database and engine
engine = create_db_and_tables(db_path="quotes.db")


data_dict_list = [
    {
        "title": "mi amiga bolufi",
        "author": "elena nito",
        "position": "8888 to 4444",
        "date_added": "el 4 del 20 de 1990",
        "quote": "tu eres mi amiga bolufi por siempre"
    },
    {
        "title": "Wisdom of Life",
        "author": "Albert Einstein",
        "position": "Physicist",
        "date_added": "15th March 1955",
        "quote": "Life is like riding a bicycle. To keep your balance, you must keep moving."
    },
    {
        "title": "Dream Big",
        "author": "Walt Disney",
        "position": "Entrepreneur & Animator",
        "date_added": "1st January 1950",
        "quote": "All our dreams can come true if we have the courage to pursue them."
    },
    {
        "title": "CAca",
        "author": "Walt Disney",
        "position": "dañlskjdfioe",
        "date_added": "1st January 1950",
        "quote": "cahuayos."
    }
]

# Try to add the quote
with Session(engine) as session:
    
    for data_dict in data_dict_list:
        was_added = add_quote_if_not_exists(session, data_dict)
        if was_added:
            print("Quote added successfully.")
        else:
            print("Quote already exists in the database.")

################
    

