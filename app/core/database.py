from sqlmodel import create_engine, Session, SQLModel
import os

DATABASE_URL = 'sqlite:///./ade.db'

engine = create_engine(
    DATABASE_URL, 
    echo=False, 
    connect_args={'check_same_thread': False}
)

def create_db_and_tables():
    from app.domain.models.base import BaseModel
    from app.domain.models.repository import Repository
    from app.domain.models.change_event import ChangeEvent
    
    print('🔧 Creating database tables...')
    SQLModel.metadata.create_all(engine)
    
    db_path = os.path.abspath('ade.db')
    print('✅ SQLite Database initialized successfully!')
    print(f'📍 Database file: {db_path}')
    
    if os.path.exists('ade.db'):
        print(f'✅ File exists! Size: {os.path.getsize('ade.db')} bytes')
    else:
        print('❌ File not found!')

def get_session():
    with Session(engine) as session:
        yield session
