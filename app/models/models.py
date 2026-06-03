from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, BigInteger, JSON, Index, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class Portfolio(Base):
    __tablename__ = 'portfolios'
    __table_args__ = (
        UniqueConstraint('owner', 'name', name='uq_portfolio_owner_name'),
    )
    id = Column(BigInteger, primary_key=True)
    owner = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    trades = relationship('Trade', back_populates='portfolio', cascade='all, delete-orphan')

class Trade(Base):
    __tablename__ = 'trades'
    __table_args__ = (
        Index('idx_trades_portfolio_id', 'portfolio_id'),
        Index('idx_trades_ticker_time', 'ticker', 'trade_time'),
    )
    id = Column(BigInteger, primary_key=True)
    portfolio_id = Column(BigInteger, ForeignKey('portfolios.id', ondelete='CASCADE'), nullable=False)
    ticker = Column(String(16), nullable=False)
    side = Column(String(8), nullable=False)
    amount = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    trade_time = Column(DateTime, nullable=False)
    status = Column(String(16), nullable=False)
    portfolio = relationship('Portfolio', back_populates='trades')
    audit_logs = relationship('AuditLog', back_populates='trade', cascade='all, delete-orphan')

class MarketData(Base):
    __tablename__ = 'market_data'
    __table_args__ = (
        Index('idx_market_data_ticker_time', 'ticker', 'trade_time'),
    )
    id = Column(BigInteger, primary_key=True)
    ticker = Column(String(16), nullable=False)
    trade_time = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    extra_json = Column(JSON)

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    __table_args__ = (
        Index('idx_audit_logs_trade_id_time', 'trade_id', 'log_timestamp'),
    )
    id = Column(BigInteger, primary_key=True)
    trade_id = Column(BigInteger, ForeignKey('trades.id', ondelete='CASCADE'), nullable=False)
    event_type = Column(String(32), nullable=False)
    event_data = Column(JSON, nullable=False)
    log_timestamp = Column(DateTime, nullable=False)
    trade = relationship('Trade', back_populates='audit_logs')