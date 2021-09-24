def row_to_dict(row):
    return dict((col, getattr(row, col)) for col in row.__table__.columns.keys())
