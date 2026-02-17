#!/usr/bin/env python3
import smtplib
import argparse
import json
import sys
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def load_config(config_path):
    """安全讀取 config.json"""
    print(f"📂 Loading config: {config_path}")
    
    # ✅ 檢查檔案存在
    if not os.path.exists(config_path):
        print(f"❌ Error: Config file not found: {config_path}")
        print("📁 Current directory:")
        print(os.listdir('.'))
        sys.exit(1)
    
    # ✅ 檢查檔案大小
    if os.path.getsize(config_path) == 0:
        print(f"❌ Error: Config file is empty: {config_path}")
        sys.exit(1)
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"✅ Config loaded: {len(config)} keys")
        return config
    except json.JSONDecodeError as e:
        print(f"❌ JSON parse error: {e}")
        print("📄 First 200 chars:")
        with open(config_path, 'r', encoding='utf-8') as f:
            print(f.read(200))
        sys.exit(1)
    except Exception as e:
        print(f"❌ Load config failed: {e}")
        sys.exit(1)

def send_email(config, dry_run=False):
    print(f"📧 From: {config['gmail_email']}")
    print(f"📨 To: {config['to_email']}")
    print(f"👥 BCC: {len(config['bcc_list'])}")
    
    if dry_run:
        print("🧪 DRY RUN - No email sent")
        return True
    
    # 檢查必要欄位
    required = ['gmail_email', 'app_password', 'to_email']
    for key in required:
        if key not in config:
            print(f"❌ Missing required config: {key}")
            return False
    print(config['app_password'],config['gmail_email'])
    msg = MIMEMultipart()
    msg['From'] = config['gmail_email']
    msg['To'] = config['to_email']
    msg['Subject'] = config.get('subject', 'No Subject')
    
    html_body = MIMEText(config.get('html_content', 'Test email'), 'html')
    msg.attach(html_body)
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(config['gmail_email'], config['app_password'])
        
        server.sendmail(
            config['gmail_email'], 
            [config['to_email']] + config['bcc_list'],
            msg.as_string()
        )
        server.quit()
        print("✅ Email sent successfully!")
        return True
    except Exception as e:
        print(f"❌ Send failed: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="🚀 Gmail Batch Sender")
    parser.add_argument('--config', required=True, help='Path to config.json')
    parser.add_argument('--dry-run', action='store_true', help='Test mode')
    args = parser.parse_args()
    
    print(f"🎯 Starting: python DailySender.py --config {args.config} {'--dry-run' if args.dry_run else ''}")
    
    config = load_config(args.config)
    success = send_email(config, args.dry_run)
    
    status = "✅ SUCCESS" if success else "❌ FAILED"
    print(f"{status} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
