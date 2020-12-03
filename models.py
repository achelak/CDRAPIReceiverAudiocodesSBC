from app import db, session, Base





class CDR_Model(Base):
    __tablename__ = 'cdr_test_alchemy'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Local_Time = db.Column(db.String(250))
    CDR_Type = db.Column(db.Integer)
    IP_Group_Name = db.Column(db.String(250))
    IP_Profile_Name = db.Column(db.String(250))
    Call_ID = db.Column(db.String(250))
    Session_ID = db.Column(db.String(250))
    Setup_Time = db.Column(db.String(250))
    Connect_Time = db.Column(db.String(250))
    Release_Time = db.Column(db.String(250))
    Call_Duration = db.Column(db.Integer)
    Endpoint_Type = db.Column(db.String(250))
    Call_Originated = db.Column(db.String(250))
    Source_URI= db.Column(db.String(250))
    Destination_URI = db.Column(db.String(250))
    Termination_Side = db.Column(db.String(250))
    Termination_Reason = db.Column(db.String(250))
    SIP_Termination_Reason = db.Column(db.String(250))
    SIP_Termination_Description = db.Column(db.String(250))
