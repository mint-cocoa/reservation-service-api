from sqlalchemy.orm import Session
#

#def get_db():
#    db = SessionLocal()
#    try:
#        yield db
#    finally:
#        db.close()



#def get_specific_facilities(db, facility_ids):
#    return db.query(Facility).filter(Facility.id.in_(facility_ids)).all()