from datetime import datetime, date
from decimal import Decimal
from sqlalchemy.inspection import inspect as sql_inspect

def model_to_dict(obj) -> dict:
    """
    Convert SQLAlchemy/SQLModel instance to dictionary.
    
    Handles serialization of datetime, date, and Decimal types.
    
    Args:
        obj: SQLAlchemy model instance.
        
    Returns:
        dict: Dictionary representation of the model.
    """
    result = {}
    for column in sql_inspect(obj).mapper.column_attrs:
        value = getattr(obj, column.key)

        if isinstance(value, (datetime, date)):
            value = value.isoformat()
        elif isinstance(value, Decimal):
            value = float(value)

        result[column.key] = value
    return result


def get_changed_fields_from_history(obj) -> tuple[dict, dict]:
    """
    Inspects SQLAlchemy history to find changed fields.
    
    Args:
        obj: SQLAlchemy model instance.
        
    Returns:
        tuple[dict, dict]: (before_data, after_data) containing only changed fields.
    """
    insp = sql_inspect(obj)
    before_data = {}
    after_data = {}

    for attr in insp.mapper.column_attrs:
        hist = insp.attrs[attr.key].history

        if hist.has_changes():
            # get old value (deleted)
            old_value = hist.deleted[0] if hist.deleted else None
            # get new value (added)
            new_value = hist.added[0] if hist.added else None

            # convert datetime/date to string
            if isinstance(old_value, (datetime, date)):
                old_value = old_value.isoformat()
            elif isinstance(old_value, Decimal):
                old_value = float(old_value)

            if isinstance(new_value, (datetime, date)):
                new_value = new_value.isoformat()
            elif isinstance(new_value, Decimal):
                new_value = float(new_value)

            before_data[attr.key] = old_value
            after_data[attr.key] = new_value

    return before_data, after_data
