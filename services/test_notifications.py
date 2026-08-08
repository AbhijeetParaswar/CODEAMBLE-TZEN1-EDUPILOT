"""Interactive Notification Testing Tool

This script allows you to test all notification channels:
- Email (SendGrid)
- SMS (Twilio)
- Voice Call (Twilio Voice API)

Usage:
    python test_notifications.py
"""

import asyncio
import sys
import os
from typing import Dict, Any

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.notifications.email import EmailNotificationService
from app.notifications.sms import SMSNotificationService
from app.notifications.voice import VoiceNotificationService


class NotificationTester:
    """Interactive testing tool for all notification channels."""
    
    def __init__(self):
        self.email_service = EmailNotificationService()
        self.sms_service = SMSNotificationService()
        self.voice_service = VoiceNotificationService()
    
    def print_header(self, title: str):
        """Print formatted section header."""
        print("\n" + "=" * 60)
        print(f"  {title}")
        print("=" * 60)
    
    def print_result(self, result: Dict[str, Any]):
        """Print formatted test result."""
        if result.get('success'):
            print("\n✅ SUCCESS")
            for key, value in result.items():
                if key != 'success':
                    print(f"   {key}: {value}")
        else:
            print("\n❌ FAILED")
            print(f"   Error: {result.get('error', 'Unknown error')}")
    
    async def test_email(self):
        """Test email notification."""
        self.print_header("📧 EMAIL NOTIFICATION TEST")
        
        email = input("\nEnter recipient email (or press Enter for default test): ").strip()
        if not email:
            email = "test@example.com"
        
        subject = input("Enter subject (or press Enter for default): ").strip()
        if not subject:
            subject = "EduPilot Test Notification"
        
        message = input("Enter message body: ").strip()
        if not message:
            message = "This is a test notification from EduPilot platform."
        
        print(f"\n📤 Sending email to {email}...")
        
        result = await self.email_service.send(
            recipient=email,
            message={
                'subject': subject,
                'body': message,
                'html': f'<h2>EduPilot Notification</h2><p>{message}</p>'
            }
        )
        
        self.print_result(result)
    
    async def test_sms(self):
        """Test SMS notification."""
        self.print_header("📱 SMS NOTIFICATION TEST")
        
        phone = input("\nEnter recipient phone (E.164 format, e.g., +918975622777): ").strip()
        if not phone:
            print("❌ Phone number is required!")
            return
        
        message = input("Enter SMS message (max 160 chars): ").strip()
        if not message:
            message = "EduPilot: This is a test SMS notification. New scholarship deadline approaching!"
        
        urgent = input("Mark as urgent? (y/n, default: n): ").strip().lower() == 'y'
        
        print(f"\n📤 Sending SMS to {phone}...")
        
        result = await self.sms_service.send(
            recipient=phone,
            message={
                'body': message,
                'urgent': urgent
            }
        )
        
        self.print_result(result)
    
    async def test_voice(self):
        """Test voice call notification."""
        self.print_header("📞 VOICE CALL NOTIFICATION TEST")
        
        phone = input("\nEnter recipient phone (E.164 format, e.g., +918975622777): ").strip()
        if not phone:
            print("❌ Phone number is required!")
            return
        
        message = input("Enter message to be spoken (max 500 chars): ").strip()
        if not message:
            message = "Hello! This is a test call from EduPilot. You have a new scholarship opportunity with an approaching deadline. Please log in to your dashboard for details."
        
        print("\nVoice options:")
        print("1. alice (default, polite female)")
        print("2. man (male voice)")
        print("3. woman (female voice)")
        voice_choice = input("Select voice (1-3, default: 1): ").strip()
        
        voice_map = {
            '1': 'alice',
            '2': 'man',
            '3': 'woman'
        }
        voice = voice_map.get(voice_choice, 'alice')
        
        print("\nLanguage options:")
        print("1. en-US (English - US)")
        print("2. en-IN (English - India)")
        print("3. hi-IN (Hindi - India)")
        lang_choice = input("Select language (1-3, default: 1): ").strip()
        
        lang_map = {
            '1': 'en-US',
            '2': 'en-IN',
            '3': 'hi-IN'
        }
        language = lang_map.get(lang_choice, 'en-US')
        
        urgent = input("Mark as urgent? (y/n, default: n): ").strip().lower() == 'y'
        
        print(f"\n📤 Initiating voice call to {phone}...")
        print(f"   Voice: {voice}")
        print(f"   Language: {language}")
        
        result = await self.voice_service.send(
            recipient=phone,
            message={
                'body': message,
                'voice': voice,
                'language': language,
                'urgent': urgent
            }
        )
        
        self.print_result(result)
        
        # If successful and we have a real call_sid, offer to check status
        if result.get('success') and result.get('call_sid') and not result.get('call_sid').startswith('dev-'):
            check = input("\n🔍 Check call status? (y/n): ").strip().lower() == 'y'
            if check:
                await asyncio.sleep(2)  # Wait a bit for call to progress
                print("\n📊 Fetching call status...")
                status = await self.voice_service.get_call_status(result['call_sid'])
                self.print_result(status)
    
    async def test_all_channels(self):
        """Test all notification channels in sequence."""
        self.print_header("🚀 TEST ALL NOTIFICATION CHANNELS")
        
        phone = input("\nEnter your phone number (E.164 format, e.g., +918975622777): ").strip()
        email = input("Enter your email address: ").strip()
        
        if not phone or not email:
            print("❌ Both phone and email are required for this test!")
            return
        
        print("\n🔄 Testing all channels...")
        
        # Test Email
        print("\n1️⃣ Testing Email...")
        email_result = await self.email_service.send(
            recipient=email,
            message={
                'subject': 'EduPilot - Multi-Channel Test',
                'body': 'This is part of a multi-channel notification test from EduPilot.',
                'html': '<h2>EduPilot Multi-Channel Test</h2><p>You are receiving this as part of testing all notification channels.</p>'
            }
        )
        print(f"   Email: {'✅ SUCCESS' if email_result.get('success') else '❌ FAILED'}")
        
        await asyncio.sleep(1)
        
        # Test SMS
        print("\n2️⃣ Testing SMS...")
        sms_result = await self.sms_service.send(
            recipient=phone,
            message={
                'body': 'EduPilot multi-channel test: SMS notification working!',
                'urgent': False
            }
        )
        print(f"   SMS: {'✅ SUCCESS' if sms_result.get('success') else '❌ FAILED'}")
        
        await asyncio.sleep(2)
        
        # Test Voice
        print("\n3️⃣ Testing Voice Call...")
        voice_result = await self.voice_service.send(
            recipient=phone,
            message={
                'body': 'Hello! This is the final test of the EduPilot multi-channel notification system. Voice call notification is working successfully.',
                'voice': 'alice',
                'language': 'en-IN',
                'urgent': False
            }
        )
        print(f"   Voice: {'✅ SUCCESS' if voice_result.get('success') else '❌ FAILED'}")
        
        # Summary
        self.print_header("📊 TEST SUMMARY")
        print(f"\n✉️  Email:  {'✅ PASS' if email_result.get('success') else '❌ FAIL'}")
        print(f"📱 SMS:    {'✅ PASS' if sms_result.get('success') else '❌ FAIL'}")
        print(f"📞 Voice:  {'✅ PASS' if voice_result.get('success') else '❌ FAIL'}")
    
    async def run(self):
        """Main interactive loop."""
        print("\n" + "=" * 60)
        print("  🎓 EDUPILOT NOTIFICATION TESTING TOOL")
        print("=" * 60)
        print("\nThis tool allows you to test all notification channels.")
        print("Make sure your .env file has the correct credentials:")
        print("  - SENDGRID_API_KEY")
        print("  - TWILIO_ACCOUNT_SID")
        print("  - TWILIO_AUTH_TOKEN")
        print("  - TWILIO_FROM_PHONE")
        
        while True:
            print("\n" + "-" * 60)
            print("Select test to run:")
            print("  1. Test Email Notification")
            print("  2. Test SMS Notification")
            print("  3. Test Voice Call Notification")
            print("  4. Test ALL Channels (Email + SMS + Voice)")
            print("  5. Exit")
            print("-" * 60)
            
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == '1':
                await self.test_email()
            elif choice == '2':
                await self.test_sms()
            elif choice == '3':
                await self.test_voice()
            elif choice == '4':
                await self.test_all_channels()
            elif choice == '5':
                print("\n👋 Goodbye! Happy testing!")
                break
            else:
                print("❌ Invalid choice. Please select 1-5.")
            
            input("\n📝 Press Enter to continue...")


async def main():
    """Entry point for the testing tool."""
    tester = NotificationTester()
    await tester.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Testing interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
