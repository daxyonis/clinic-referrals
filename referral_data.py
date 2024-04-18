from typing import Optional, List, Any
from pydantic import BaseModel, Field

class LcReferralData(BaseModel):
    """ Information about a referral  """
    email_id: Any = Field(description="The id of the email")
    referring_office: Optional[str] = Field(default=None, description="Name of the referring office (who the message is coming from)")
    doctor: Optional[str] = Field(default=None, description="Name of the doctor (who the message is sent to)")
    procedure: Optional[str] = Field(default=None, description="Name of the medical procedure")
    booking: Optional[str] = Field(default=None, description="Booking status, either booked / call pt / Pt to call")
    xray: Optional[str] = Field(default=None, description="Xray status, either taken / sent / needed / no xray")
    attachment: Optional[bool] = Field(default=None, description="Attachment status")
    patient: Optional[str]= Field(default=None, description="Patient name or phone number")

class LcReferralDataList(BaseModel):
    """ Extracted data about all referrals """
    referrals: List[LcReferralData]

class ReferralData:
    def __init__(self, email_id, date_received, referring_office, doctor, procedure, booking, xray, attachment, patient):
        self.email_id = email_id
        self.date_received = date_received
        self.referring_office = referring_office
        self.doctor = doctor
        self.procedure = procedure
        self.booking = booking
        self.xray = xray
        self.attachment = attachment
        self.patient = patient       

    def to_dict(self):
        return {
            'email_id': self.email_id,
            'date_received': self.date_received,
            'referring_office': self.referring_office,
            'doctor': self.doctor,
            'procedure': self.procedure,
            'booking': self.booking,
            'xray': self.xray,
            'attachment': self.attachment,
            'patient': self.patient
        }