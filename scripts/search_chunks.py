import sys
from app.database import SessionLocal
from app.models import FileChunk

def search_chunks(keyword:str):
    db = SessionLocal()
    try:
        results = (db.query(FileChunk).filter(FileChunk.chunk_text.ilike(f"%{keyword}%")).limit(5).all())
        if results is None:
            print(f"No matches found for {keyword}")
            return
        print(f"Found {len(results)} matching chunks\n")
        for result in results:
            print("=" * 60)
            print(f"File Path: {result.file_path}")
            print(f"Line Range: {result.end_line - result.start_line}")
            print()
            print(result.chunk_text[:500])
            print()
    finally:
        db.close()
        
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python -m scripts.search_chunks "keyword"')
        sys.exit(1)

    search_chunks(sys.argv[1])