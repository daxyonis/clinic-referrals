class Email:
    def __init__(self, id, date, _from, to, subject, body, attachments=None):
        self.id = id
        self.date = date
        self._from = _from
        self.to = to        
        self.subject = subject
        self.body = body
        self.attachments = attachments

    @property
    def short_id(self):        
        if len(self.id) >= 5:
            return self.id[1:5]
        else:
            return self.id

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date,
            'from': self._from,
            'to': self.to,
            'subject': self.subject,            
            'body': self.body,
            'attachments': self.attachments            
        }
    
    def to_string(self):
        return f'[ ID={self.short_id}, FROM={self._from}, TO={self.to}, SUBJECT={self.subject}, BODY={self.body}, ATTACHMENT={self.attachments}]'