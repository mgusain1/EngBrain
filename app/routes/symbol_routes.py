from fastapi import APIRouter, HTTPException, Query
from app.database import SessionLocal
from app.models import CodeSymbol, Repo

router = APIRouter(prefix="/repos")

@router.get("/{repo_id}/symbols")
def get_repo_symbols(repo_id: int, symbol_type:str|None=None, file_path:str|None=None, limit: int= Query(default=100,ge=1,le=500)):
    db = SessionLocal()

    try:
        repo = db.query(Repo).filter(Repo.id == repo_id).first()

        if repo is None:
            raise HTTPException(
                status_code=404,
                detail="Repo not found."
            )
            
        query = db.query(CodeSymbol).filter(CodeSymbol.repo_id==repo_id)
        
        if symbol_type is not None:
            query = query.filter(CodeSymbol.symbol_type==symbol_type)
            
        if file_path is not None:
            query = query.filter(CodeSymbol.file_path==file_path)
            
        total_count = query.count()
        
        symbols = (
           query.order_by(CodeSymbol.file_path.asc(),CodeSymbol.start_line.asc()).limit(limit).all()
        )

        result = []

        for symbol in symbols:
            result.append({
                "id": symbol.id,
                "repo_id": symbol.repo_id,
                "file_id": symbol.file_id,
                "file_path": symbol.file_path,
                "symbol_type": symbol.symbol_type,
                "symbol_name": symbol.symbol_name,
                "parent_name": symbol.parent_name,
                "start_line": symbol.start_line,
                "end_line": symbol.end_line,
                "docstring": symbol.docstring
            })

        return {
            "repo_id": repo_id,
            "repo_name": repo.name,
            "total_symbol_returned": total_count,
            "returned_symbols_count": len(result),
            "limit":limit,
            "symbols": result
        }

    finally:
        db.close()