
# from sqlalchemy import Column, Integer, String, Boolean, JSON, DateTime, Float, ForeignKey, event
# from sqlalchemy.sql import func
# from sqlalchemy.orm import Session
# from sqlalchemy.inspection import inspect as sql_inspect
# from app.database import Base

# from datetime import datetime, date
# from decimal import Decimal

# def model_to_dict(obj):
#     """Convert SQLAlchemy model to dictionary"""
#     result = {}
#     for column in sql_inspect(obj).mapper.column_attrs:
#         value = getattr(obj, column.key)
        
#         if isinstance(value, (datetime, date)):
#             value = value.isoformat()
#         elif isinstance(value, Decimal):
#             value = float(value)
        
#         result[column.key] = value
    
#     return result


# def get_changed_fields_from_history(obj):
#     insp = sql_inspect(obj)
#     before_data = {}
#     after_data = {}
    
#     for attr in insp.mapper.column_attrs:
#         hist = insp.attrs[attr.key].history
        
#         if hist.has_changes():
#             # get old value (deleted)
#             old_value = hist.deleted[0] if hist.deleted else None
            
#             # get new value (added)
#             new_value = hist.added[0] if hist.added else None
            
#             # convert datetime/date to string
#             if isinstance(old_value, (datetime, date)):
#                 old_value = old_value.isoformat()
#             # convert old value to string if it's a datetime/date or Decimal
#             elif isinstance(old_value, Decimal):
#                 old_value = float(old_value)
                
#             # convert new value to string if it's a datetime/date or Decimal
#             if isinstance(new_value, (datetime, date)):
#                 new_value = new_value.isoformat()
#             # convert new value to string if it's a datetime/date or Decimal
#             elif isinstance(new_value, Decimal):
#                 new_value = float(new_value)
            
#             before_data[attr.key] = old_value
#             after_data[attr.key] = new_value
    
#     return before_data, after_data

# class AuditLog(Base):
#     __tablename__ = "audit_logs"
    
#     id = Column(Integer, primary_key=True)
#     table_name = Column(String, nullable=False)
#     record_id = Column(Integer, nullable=False)
#     action = Column(String, nullable=False)
    
#     before_data = Column(JSON, nullable=True)
#     after_data = Column(JSON, nullable=True)
    
#     performed_by = Column(Integer, nullable=False)
    
#     created_at = Column(DateTime, server_default=func.now())

# class AuditableBase(Base):
#     __abstract__ = True

# @event.listens_for(Session, "after_flush")
# def after_flush(session, flush_context):
#     user_id = session.info.get("user_id")
#     if user_id is None:
#         return
    
#     # Track NEW objects (CREATE)
#     for obj in session.new:
#         if isinstance(obj, AuditableBase) and hasattr(obj, 'id') and obj.id is not None:
#             table_name = obj.__tablename__
#             after_data = model_to_dict(obj)
#             audit = AuditLog(
#                 table_name=table_name,
#                 record_id=obj.id,
#                 action="CREATE",
#                 before_data=None,
#                 after_data=after_data,
#                 performed_by=user_id
#             )
            
#             session.add(audit)


#     for obj in session.dirty:
#         if isinstance(obj, AuditableBase):
#             table_name = obj.__tablename__
            
#             # Skip audit_logs table itself
#             if table_name == "audit_logs":
#                 continue

#             before_data, after_data = get_changed_fields_from_history(obj)

#             if before_data:
#                 audit = AuditLog(
#                     table_name=table_name,
#                     record_id=obj.id,
#                     action="UPDATE",
#                     before_data=before_data,
#                     after_data=after_data,
#                     performed_by=user_id
#                 )
                
#                 session.add(audit)

#     for obj in session.deleted:
#         if isinstance(obj, AuditableBase):
#             table_name = obj.__tablename__
             
#             before_data = model_to_dict(obj)
            
#             audit = AuditLog(
#                 table_name=table_name,
#                 record_id=obj.id,
#                 action="DELETE",
#                 before_data=before_data,
#                 after_data=None,
#                 performed_by=user_id
#             )
            
#             session.add(audit)

# class User(Base):
#     """User table - not auditable"""
#     __tablename__ = "users"
    
#     id = Column(Integer, primary_key=True)
#     email = Column(String, unique=True, nullable=False)
#     password = Column(String, nullable=False)
#     role = Column(String, nullable=False)
    
#     created_at = Column(DateTime, server_default=func.now())


# class Loan(AuditableBase):
#     # Loan table - automatically audited
#     __tablename__ = "loans"
    
#     id = Column(Integer, primary_key=True)
    
#     customer_name = Column(String, nullable=False)
#     loan_amount = Column(Float, nullable=False)
#     tenure_months = Column(Integer, nullable=False)
#     interest_rate = Column(Float, nullable=True)
#     status = Column(String, default="pending")
    
#     created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
#     approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
#     created_at = Column(DateTime, server_default=func.now())
#     approved_at = Column(DateTime, nullable=True)

# class ActivityLog(Base):
#     __tablename__ = "activity_logs"

#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, nullable=True)
#     action = Column(String, nullable=False)
#     entity = Column(String, nullable=True)
#     entity_id = Column(Integer, nullable=True)
#     method = Column(String, nullable=False)
#     endpoint = Column(String, nullable=False)
#     ip_address = Column(String, nullable=True)
#     status = Column(String, default="SUCCESS")
#     status_code = Column(Integer, nullable=True) 
#     extra_data = Column(JSON, nullable=True)
#     created_at = Column(DateTime, server_default=func.now())
    

# class Payment(Base):
#     __tablename__ = "payments"

#     id = Column(Integer, primary_key=True)
  

#     amount = Column(Float, nullable=False)
#     payment_mode = Column(String, nullable=False)  # CASH / UPI / CARD
#     status = Column(String, default="PENDING")     # PENDING / SUCCESS / FAILED

#     created_at = Column(DateTime, server_default=func.now())

