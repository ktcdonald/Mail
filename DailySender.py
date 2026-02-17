#!/usr/bin/env python3
import smtplib
import argparse
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def load_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def send_email(config, dry_run=False):
    if dry_run:
        print("🧪 DRY RUN MODE")
        print(f"📧 From: {config['gmail_email']}")
        print(f"📨 To: {config['to_email']}")
        print(f"👥 BCC: {len(config['bcc_list'])}")
        print(f"📄 Subject: {config['subject']}")
        return True
    
    # 真實發送
    msg = MimeMultipart()
    msg['From'] = config['gmail_email']
    msg['To'] = config['to_email']
    msg['Subject'] = config['subject']
    
    # HTML 內容
    html_body = MimeText(config['html_content'], 'html')
    msg.attach(html_body)
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(config['gmail_email'], config['app_password'])
        
        server.sendmail(config['gmail_email'], 
                       [config['to_email']] + config['bcc_list'],
                       msg.as_string())
        server.quit()
        print("✅ Email sent successfully!")
        return True
    except Exception as e:
        print(f"❌ Send failed: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gmail Batch Sender")
    parser.add_argument('--config', required=True)
    parser.add_argument('--dry-run', action='store_true', default=False)
    args = parser.parse_args()
    
    config = load_config(args.config)
    success = send_email(config, args.dry_run)
    print(f"{'✅' if success else '❌'} Mission {'completed (dry)' if args.dry_run else 'completed'}!")
