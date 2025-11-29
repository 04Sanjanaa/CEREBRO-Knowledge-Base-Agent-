"""
Calendar Service - Google Calendar Integration
Provides access to company events and holiday schedule
"""

import os
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta

class CalendarService:
    def __init__(self, credentials_path=None):
        """Initialize Google Calendar service"""
        self.credentials_path = credentials_path or os.getenv('GOOGLE_CALENDAR_CREDS')
        self.service = None
        self.enabled = False
        
        if self.credentials_path and os.path.exists(self.credentials_path):
            try:
                self._authenticate()
                self.enabled = True
            except Exception as e:
                print(f"Calendar service initialization failed: {e}")
    
    def _authenticate(self):
        """Authenticate with Google Calendar"""
        try:
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path,
                scopes=['https://www.googleapis.com/auth/calendar.readonly']
            )
            self.service = build('calendar', 'v3', credentials=credentials)
        except Exception as e:
            raise Exception(f"Failed to authenticate with Google Calendar: {e}")
    
    def get_upcoming_events(self, calendar_id='primary', days=30):
        """
        Get upcoming company events
        Args:
            calendar_id: Google Calendar ID
            days: Number of days to look ahead
        Returns:
            List of upcoming events
        """
        if not self.enabled or not self.service:
            return {
                'success': False,
                'error': 'Calendar service not configured',
                'events': []
            }
        
        try:
            now = datetime.utcnow()
            future = now + timedelta(days=days)
            
            events_result = self.service.events().list(
                calendarId=calendar_id,
                timeMin=now.isoformat() + 'Z',
                timeMax=future.isoformat() + 'Z',
                maxResults=10,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            formatted_events = []
            for event in events:
                formatted_events.append({
                    'title': event.get('summary', 'Untitled'),
                    'start': event.get('start', {}).get('dateTime', event.get('start', {}).get('date')),
                    'end': event.get('end', {}).get('dateTime', event.get('end', {}).get('date')),
                    'description': event.get('description', ''),
                    'location': event.get('location', '')
                })
            
            return {
                'success': True,
                'events': formatted_events,
                'count': len(formatted_events)
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to fetch events: {str(e)}',
                'events': []
            }
    
    def get_company_holidays(self, year=None):
        """
        Get company holidays
        Returns:
            List of holidays
        """
        if not year:
            year = datetime.now().year
        
        # Mock holidays data - in production, fetch from calendar
        holidays = [
            {'date': f'{year}-01-01', 'name': 'New Year Day'},
            {'date': f'{year}-05-01', 'name': 'Labour Day'},
            {'date': f'{year}-12-25', 'name': 'Christmas Day'},
        ]
        
        return {
            'success': True,
            'holidays': holidays,
            'year': year
        }


# Initialize default service
calendar_service = CalendarService()
