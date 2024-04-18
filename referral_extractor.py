from referral_data import ReferralData, LcReferralDataList
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate

class ReferralExtractor:    
    prompt = ChatPromptTemplate.from_messages([
    ("system", '''
      You are a medical specialist in oral surgery. You will be retrieving data from referral emails sent to your clinic.
      Here are some terms to know: 
      -Re = Regarding
      -Ext = extraction (when shown as eg. Ext 14 - This means quadrant 1, tooth #4) (4 quadrants total)
      -Local = Local anesthesia
      -IV sedation
      -Pt = Patient
      -8s = wisdom teeth
      -TMJ = Temporomandibular joints
      -C/S = Consult & surgery (usually a same day appointment)
      -Ortho = Orthognathic surgery 
      -All-On-Four = Full mouth implant procedure

      From the emails, you will extract the following information (in json format): 
      -referring_office (who the message is coming from)
      -doctor (who the message is sent to)
      -procedure: name of medical procedure
      -booking: a string either booked / call pt / Pt to call
      -xray : a string either taken / sent / needed / no xray
      -attachment: true or false
      -patient: name/phone of patient (null if absent)

      Remember the following rules : 
      1) when an attachment is present, it means the Xray is sent ; 
      2) when there is no attachment, the Xray is needed or no xray, depending on the context of this email ; 
      3) when a date is present in the email subject or body, the appointment is booked ; 
      4) when a date is not present in the subject or body, the appointment is either call pt or Pt to call, depending on the context of this email; 
      5) Use the doctor's name (if present) instead of the email for the doctor field ; 
      6) Use the referring office's name (if present) instead of the email for the referring_office field;
      7) Only extract relevant information from the text ;
      8) If you do not know the value of an attribute asked to extract, return null for the attribute's value.
     '''),
    ("user", '''
      Here is a list of emails from which to extract the information. Each email is in square brackets like [].
      Respond only with the json, no other words.
     {input}'
     ''')
    ])    
        
    
    def __init__(self, model, api_key):
        llm = ChatAnthropic(model=model, 
                            api_key=api_key, 
                            temperature=0, 
                            max_tokens=1024, 
                            default_headers={"anthropic-beta": "tools-2024-04-04"})
        self.chain = ReferralExtractor.prompt | llm.with_structured_output(schema=LcReferralDataList)

    # Extract referral data from emails
    def extract(self, emails) -> list[ReferralData]:
        referral_list = []        

        input = ' '.join([email.to_string() for email in emails])
        result = self.chain.invoke({"input" : input})

        # We make the hypothesis that the order of the emails in the input is the same as the order of the emails in the result
        for i in range(len(result.referrals)):
            ref = result.referrals[i]
            email = emails[i]
            referral = ReferralData(email_id=email.id,
                                    date_received=email.date, 
                                    referring_office=ref.referring_office, 
                                    doctor=ref.doctor, 
                                    procedure=ref.procedure, 
                                    booking=ref.booking, 
                                    xray=ref.xray, 
                                    attachment=ref.attachment, 
                                    patient=ref.patient)
            referral_list.append(referral)

        return referral_list
