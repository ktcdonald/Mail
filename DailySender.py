import argparse
import json
from datetime import datetime

def load_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def dry_run_test(config):
    """模擬發送，不真發"""
    print(f"🧪 DRY RUN MODE")
    print(f"📅 Date: {config['date']} (Day {config['day_num']}/{config['total_day']})")
    print(f"📧 From: {config['gmail_email']}")
    print(f"📨 To: {config['to_email']}")
    print(f"👥 BCC: {len(config['bcc_list'])} recipients")
    print(f"📄 Subject: {config['subject'][:50]}...")
    print(f"✅ Batch size: {config['batch_size']}")
    print(f"🕐 Simulated send time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True, help='Path to config.json')
    parser.add_argument('--dry-run', action='store_true', help='Test without sending')
    args = parser.parse_args()
    
    config = load_config(args.config)
    
    if args.dry_run:
        success = dry_run_test(config)
        print("✅ Test PASSED!")
    else:
        print("🚀 Real send mode (implement your SMTP logic)")
