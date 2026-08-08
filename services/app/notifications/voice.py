"""Voice Call Notification Service (Twilio Voice)

This module provides voice call notification delivery service using Twilio Voice API.
It includes phone number validation, Text-to-Speech (TTS) message delivery, and call tracking.

Satisfies Requirements: 12.1, 12.2, 12.3, 12.4, 12.5
"""

import logging
import re
from typing import Dict, Any, Optional
from datetime import datetime

from app.notifications.service import NotificationService
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class VoiceNotificationService(NotificationService):
    """Voice call delivery service using Twilio Voice API with TTS.
    
    **Validates: Requirements 12.1, 12.2, 12.3, 12.4, 12.5**
    """
    
    PHONE_REGEX = r'^\+?[1-9]\d{7,14}$'  # E.164 phone format validation
    
    def __init__(self, account_sid: Optional[str] = None, auth_token: Optional[str] = None, from_phone: Optional[str] = None):
        self.account_sid = account_sid or getattr(settings, 'twilio_account_sid', None)
        self.auth_token = auth_token or getattr(settings, 'twilio_auth_token', None)
        self.from_phone = from_phone or getattr(settings, 'twilio_from_phone', '+15005550006')

    async def validate_recipient(self, recipient: str) -> bool:
        """Validate recipient phone number in E.164 format."""
        if not recipient or not isinstance(recipient, str):
            return False
        clean = recipient.strip().replace(' ', '').replace('-', '')
        return bool(re.match(self.PHONE_REGEX, clean))

    def sanitize_tts_message(self, text: str, max_length: int = 500) -> str:
        """Sanitize and truncate message for Text-to-Speech (TTS).
        
        Args:
            text: Message text to be spoken
            max_length: Maximum character length (default 500)
        
        Returns:
            Sanitized message suitable for TTS
        """
        if not text:
            return ""
        
        # Remove special characters that might cause TTS issues
        clean_text = re.sub(r'[<>{}[\]\\]', '', text)
        
        if len(clean_text) <= max_length:
            return clean_text
        return clean_text[:max_length - 20] + ". Message truncated."

    async def send(self, recipient: str, message: Dict[str, Any]) -> Dict[str, Any]:
        """Initiate voice call with TTS message.
        
        Args:
            recipient: Target phone number in E.164 format
            message: Dict containing:
                - 'body': Message text to be spoken via TTS
                - 'voice': Optional voice type ('man', 'woman', 'alice' - default: 'alice')
                - 'language': Optional language code (default: 'en-US')
                - 'urgent': Optional urgent flag for priority handling
        
        Returns:
            Dict with success status, call_sid, and metadata
        """
        if not await self.validate_recipient(recipient):
            return {
                'success': False,
                'error': f'Invalid phone number format: {recipient}',
                'status_code': 400
            }
        
        body = self.sanitize_tts_message(message.get('body', ''))
        voice = message.get('voice', 'alice')  # Options: 'man', 'woman', 'alice'
        language = message.get('language', 'en-US')
        urgent = message.get('urgent', False)
        
        if not body:
            return {
                'success': False,
                'error': 'Message body is required for voice calls',
                'status_code': 400
            }
        
        try:
            if self.account_sid and self.auth_token:
                # Real Twilio Voice API call
                from twilio.rest import Client
                
                client = Client(self.account_sid, self.auth_token)
                
                # Create TwiML for Text-to-Speech
                twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="{voice}" language="{language}">{body}</Say>
    <Pause length="1"/>
    <Say voice="{voice}" language="{language}">This message is from EduPilot. Thank you.</Say>
</Response>"""
                
                logger.info(f"Initiating voice call via Twilio to {recipient} (urgent={urgent})")
                
                call = client.calls.create(
                    to=recipient,
                    from_=self.from_phone,
                    twiml=twiml,
                    status_callback_method='POST',
                    status_callback_event=['initiated', 'ringing', 'answered', 'completed']
                )
                
                return {
                    'success': True,
                    'call_sid': call.sid,
                    'recipient': recipient,
                    'provider': 'twilio_voice',
                    'status': call.status,
                    'direction': call.direction,
                    'from_phone': self.from_phone,
                    'voice': voice,
                    'language': language,
                    'message_length': len(body),
                    'timestamp': datetime.utcnow().isoformat()
                }
            else:
                # Development mock mode
                logger.info(f"[DEV] Voice call simulated to {recipient}")
                logger.info(f"[DEV] TTS Message: {body}")
                logger.info(f"[DEV] Voice: {voice}, Language: {language}")
                
                return {
                    'success': True,
                    'call_sid': f"dev-call-{int(datetime.utcnow().timestamp())}",
                    'recipient': recipient,
                    'provider': 'development_mock',
                    'status': 'simulated',
                    'voice': voice,
                    'language': language,
                    'message_length': len(body),
                    'timestamp': datetime.utcnow().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Voice call failed for {recipient}: {e}")
            return {
                'success': False,
                'error': str(e),
                'recipient': recipient
            }

    async def get_call_status(self, call_sid: str) -> Dict[str, Any]:
        """Retrieve status of a voice call.
        
        Args:
            call_sid: Twilio Call SID
        
        Returns:
            Dict with call status information
        """
        try:
            if self.account_sid and self.auth_token:
                from twilio.rest import Client
                
                client = Client(self.account_sid, self.auth_token)
                call = client.calls(call_sid).fetch()
                
                return {
                    'success': True,
                    'call_sid': call.sid,
                    'status': call.status,
                    'duration': call.duration,
                    'price': call.price,
                    'price_unit': call.price_unit,
                    'direction': call.direction,
                    'from': call.from_,
                    'to': call.to
                }
            else:
                return {
                    'success': True,
                    'call_sid': call_sid,
                    'status': 'mock_mode',
                    'message': 'Call status check only available with Twilio credentials'
                }
        except Exception as e:
            logger.error(f"Failed to fetch call status for {call_sid}: {e}")
            return {
                'success': False,
                'error': str(e)
            }
