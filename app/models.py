from sqlalchemy import Column, Integer, String,Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Repo(Base):
    __tablename__ = "repos"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    path = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    files = relationship("RepoFile", back_populates="repo", cascade="all, delete-orphan")
    
class RepoFile(Base):
    __tablename__ = "repo_files"
    id = Column(Integer, primary_key=True, index=True)
    repo_id = Column(Integer, ForeignKey("repos.id"), nullable=False)
    file_path = Column(String, nullable=False)
    file_type = Column(String, nullable=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    repo = relationship("Repo", back_populates="files")
    chunks = relationship("FileChunk", back_populates="file", cascade="all, delete-orphan")
    
class FileChunk(Base):
    __tablename__ = "file_chunks"
    id = Column(Integer, primary_key=True, index=True)
    repo_id = Column(Integer, ForeignKey("repos.id"), nullable=False)
    file_id = Column(Integer, ForeignKey("repo_files.id"), nullable=False)
    file_path = Column(String, nullable=False)
    chunk_text = Column(Text, nullable=False)
    start_line = Column(Integer, nullable=True)
    end_line = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    file = relationship("RepoFile", back_populates="chunks")
    
class QueryLog(Base):
    __tablename__ = "query_logs"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, nullable=False)
    repo_id = Column(Integer, nullable=True)
    query_type = Column(String, nullable=False)  # ask or runbook
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=True)
    sources_returned = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
class EventLog(Base):
    __tablename__ = "event_logs"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, nullable=True)
    event_type = Column(String, nullable=False)
    repo_input = Column(Text, nullable=True)
    repo_id = Column(Integer, nullable=True)
    status = Column(String, nullable=True)
    message = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    
class CodeSymbol(Base):
    __tablename__ = "code_symbols"

    id = Column(Integer, primary_key=True, index=True)

    repo_id = Column(Integer, ForeignKey("repos.id"), nullable=False)
    file_id = Column(Integer, ForeignKey("repo_files.id"), nullable=False)

    file_path = Column(String, nullable=False)

    symbol_type = Column(String, nullable=False)
    symbol_name = Column(String, nullable=False)
    parent_name = Column(String, nullable=True)

    start_line = Column(Integer, nullable=True)
    end_line = Column(Integer, nullable=True)

    docstring = Column(Text, nullable=True)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)