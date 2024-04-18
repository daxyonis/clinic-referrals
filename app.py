from flask import Flask, render_template
from email_loader import EmailLoader
from referral_extractor import ReferralExtractor
import os

app = Flask(__name__)

@app.route("/")
def home():    
    return render_template('index.html')


@app.route("/api/emails")
def emails():
    email_loader = EmailLoader(os.environ.get('IMAP_SERVER'), os.environ.get('IMAP_USERNAME'), os.environ.get('IMAP_PASSWORD'))
    email_list = email_loader.load_emails()    
    referral_extractor = ReferralExtractor(os.environ.get('ANTHROPIC_MODEL'), os.environ.get('ANTHROPIC_API_KEY'))
    referral_list = referral_extractor.extract(email_list)
    email_dicts = [email.to_dict() for email in email_list]
    referral_dicts = [referral.to_dict() for referral in referral_list]
    return {'emails': email_dicts, 'referrals': referral_dicts}        


if __name__ == '__main__':
    app.run(debug=True)

