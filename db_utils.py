from sqlmodel import SQLModel, Field, Session, create_engine, select
import os
import random

# Step 1: Define the database model
class Quotes(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    lectore: str
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
    
    
def get_random_quote(engine):
    """
    Retrieves a random quote from the database.

    Args:
        engine: SQLModel database engine instance

    Returns:
        dict: Dictionary containing quote data if found, None if no quotes exist
    """
    with Session(engine) as session:
        # Get min and max ID
        min_id = session.exec(select(Quotes.id).order_by(Quotes.id).limit(1)).one_or_none()
        max_id = session.exec(select(Quotes.id).order_by(Quotes.id.desc()).limit(1)).one_or_none()
        
        if min_id is None or max_id is None:
            return None  # No records in the table
        
        while True:
            ids = list(range(1, max_id + 1))
            random_id = random.choices(ids, weights=ids, k=1)[0]
            # random_id = random.randint(min_id, max_id)
            stmt = select(Quotes).where(Quotes.id == random_id)
            quote = session.exec(stmt).first()
            
            if quote:
                return quote.model_dump()  # Found a valid row, return it
