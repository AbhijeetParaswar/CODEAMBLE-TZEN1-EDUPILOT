"""Quick Non-Interactive Notification Test

This script automatically tests all notification channels without user interaction.
Perfect for quick testing before demos.

Usage:
    python test_all_now.py
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.notifications.email import EmailNotificationService
from app.notifications.sms import SMSNotificationService
from app.notifications.voice import VoiceNotificationService


# Test configuration - UPDATE THESE WITH YOUR DETAILS
TEST_EMAIL = "abhijeetparaswar56@gmail.com"
TEST_PHONE = "+918975622777"


async def test_all_notifications():
    """Test all notification channels automatically."""
    
    print("=" * 70)
    print("  🎓 EDUPILOT - QUICK NOTIFICATION TEST")
    print("=" * 70)
    print(f"\n📧 Email: {TEST_EMAIL}")
    print(f"📱 Phone: {TEST_PHONE}")
    print("\n" + "=" * 70)
    
    # Initialize services
    email_service = EmailNotificationService()
    sms_service = SMSNotificationService()
    voice_service = VoiceNotificationService()
    
    results = {
        'email': None,
        'sms': None,
        'voice': None
    }
    
    # Test Email
    print("\n📧 Testing Email Notification...")
    print("-" * 70)
    try:
        email_result = await email_service.send(
            recipient=TEST_EMAIL,
            message={
                'subject': 'EduPilot - Quick Test Notification',
                'body': 'This is an automated test of the email notification system.',
                'html': '''
                <div style="font-family: Arial, sans-serif; padding: 20px;">
                    <h2 style="color: #4F46E5;">EduPilot Notification Test</h2>
                    <p>This is an automated test of the email notification system.</p>
                    <p><strong>Status:</strong> Email notification is working correctly! ✅</p>
                    <hr style="margin: 20px 0;">
                    <p style="color: #666; font-size: 12px;">
                        This is a test message from EduPilot platform.
                    </p>
                </div>
                '''
            }
        )
        results['email'] = email_result
        if email_result.get('success'):
            print(f"✅ Email sent successfully!")
            print(f"   Message ID: {email_result.get('message_id', 'N/A')}")
        else:
            print(f"❌ Email failed: {email_result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"❌ Email exception: {e}")
        results['email'] = {'success': False, 'error': str(e)}
    
    # Wait between tests
    await asyncio.sleep(2)
    
    # Test SMS
    print("\n📱 Testing SMS Notification...")
    print("-" * 70)
    try:
        sms_result = await sms_service.send(
            recipient=TEST_PHONE,
            message={
                'body': 'EduPilot Quick Test: SMS notification working! New scholarship deadline approaching. Check dashboard for details.',
                'urgent': False
            }
        )
        results['sms'] = sms_result
        if sms_result.get('success'):
            print(f"✅ SMS sent successfully!")
            print(f"   Message SID: {sms_result.get('message_sid', 'N/A')}")
        else:
            print(f"❌ SMS failed: {sms_result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"❌ SMS exception: {e}")
        results['sms'] = {'success': False, 'error': str(e)}
    
    # Wait between tests
    await asyncio.sleep(2)
    
    # Test Voice
    print("\n📞 Testing Voice Call Notification...")
    print("-" * 70)
    try:
        voice_result = await voice_service.send(
            recipient=TEST_PHONE,
            message={
                'body': '''Hello! This is an automated test of the EduPilot voice notification system. 
                You have received this call to verify that voice notifications are working correctly. 
                The scholarship deadline reminder system is operational. 
                Please check your EduPilot dashboard for more details. Thank you!''',
                'voice': 'alice',
                'language': 'en-IN',
                'urgent': False
            }
        )
        results['voice'] = voice_result
        if voice_result.get('success'):
            print(f"✅ Voice call initiated successfully!")
            print(f"   Call SID: {voice_result.get('call_sid', 'N/A')}")
            print(f"   Status: {voice_result.get('status', 'N/A')}")
            print(f"\n   📞 Your phone should be ringing now...")
        else:
            print(f"❌ Voice call failed: {voice_result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"❌ Voice exception: {e}")
        results['voice'] = {'success': False, 'error': str(e)}
    
    # Summary
    print("\n" + "=" * 70)
    print("  📊 TEST SUMMARY")
    print("=" * 70)
    
    email_status = "✅ PASS" if results.get('email', {}).get('success') else "❌ FAIL"
    sms_status = "✅ PASS" if results.get('sms', {}).get('success') else "❌ FAIL"
    voice_status = "✅ PASS" if results.get('voice', {}).get('success') else "❌ FAIL"
    
    print(f"\n📧 Email:  {email_status}")
    print(f"📱 SMS:    {sms_status}")
    print(f"📞 Voice:  {voice_status}")
    
    # Overall result
    all_passed = all([
        results.get('email', {}).get('success'),
        results.get('sms', {}).get('success'),
        results.get('voice', {}).get('success')
    ])
    
    print("\n" + "=" * 70)
    if all_passed:
        print("  🎉 ALL TESTS PASSED!")
        print("  All notification channels are working correctly.")
    else:
        print("  ⚠️  SOME TESTS FAILED")
        print("  Check the results above for details.")
    print("=" * 70)
    
    # Detailed error information
    if not all_passed:
        print("\n📋 Error Details:")
        print("-" * 70)
        for channel, result in results.items():
            if result and not result.get('success'):
                print(f"\n{channel.upper()}:")
                print(f"  Error: {result.get('error', 'Unknown error')}")
    
    print("\n")
    return results


async def main():
    """Entry point."""
    try:
        print("\n🚀 Starting quick notification test...")
        print("⏱️  This will take about 10-15 seconds...\n")
        
        await test_all_notifications()
        
        print("✅ Test completed!\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user.")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
