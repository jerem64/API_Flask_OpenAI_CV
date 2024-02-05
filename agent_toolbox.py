# agent_tool_box.py
from langchain.agents import Tool
from flask import session
from config import Config
import json

from datetime import datetime, timedelta

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from google.oauth2.credentials import Credentials

import random
import uuid


class AgentToolBox:
    def __init__(self):
        self.init_GoogleCalendar()

        self.tools = []
        self.tools.append(
            Tool(
                name='send_Google_calendar_invitation',
                func=self.send_GoogleCalendar_invitation,
                description='''Useful for when you need to send a google calendar meeting invitation to Jérémy chassin.
                
                Parameters:
                - If the user provides his email address, put it in user_email. The default value is null.
                - If the user provides a meeting time, format it to the YYYY-MM-DD HH:MM:SS format and put in meeting_date. The default value is null.
                - If the user provides his name, put it in user_name. The default value is null.
                Structure the data as a python dictionary.
                
                Note: If a parameter is not provided, the default value will be used (null).
                
                Example:
                {
                    "user_name": null,          # Leave null if not specified
                    "meeting_date": null,       # Leave null if not specified
                    "user_email": null          # Leave null if not specified
                }'''
            )
        )

        #self.tools.append(
            #Tool(
                #name='complete_Google_calendar_invitation_informations',
                #func=self.complete_Google_calendar_invitation_informations,
                #description='''Useful for when you receive a name, a meeting time or an email address. 
                #If the user provide his email adress, put it in user_email.
                #"If the user provide a meeting time, format it to the YYYY-MM-DD HH:MM:SS format and put in meeting_date.
                #If the user provide his name, put it in user_name.
                #Structure the data as a python dictionary and do not fill missing values.'''
            #)
        #)

        self.tools.append(
            Tool(
	            name='play_chifumi',
                func=self.play_chifumi,
                description='''Useful for when you need to play chifumi (rock, paper, scissors).
                User must provide a choice that will go in player_choice.'''
            )
        )

    # Tool to send google calendar meeting to me
    def play_chifumi(self, player_choice=None):
        choices = ["rock", "paper", "scissors"]
        agent_choice = random.choice(choices)

        if player_choice == agent_choice:
            return f"{player_choice} versus {agent_choice}, it's a tie!"
        elif ((player_choice == "rock" and agent_choice == "scissors") or
              (player_choice == "paper" and agent_choice == "rock") or
              (player_choice == "scissors" and agent_choice == "paper")):
            return f"{player_choice} versus {agent_choice}, you win!"
        else:
            return f"{player_choice} versus {agent_choice}, I win!"
        
    # Tool to send google calendar meeting to me
    def send_GoogleCalendar_invitation(self, data=None, need_additional_info=True):
        """Tool method to create an Event in Google Calendar.
        """
        try:
            data_dict = json.loads(data)

            # Extract values from the dictionary
            user_email = data_dict.get('user_email', '')
            user_name = data_dict.get('user_name', '')
            meeting_date = data_dict.get('meeting_date', '')

            meeting_result = 'Google Calendar invitation cannot be created, please provide: '

            # Check and store user email
            if not user_email and not 'user_email' in session:
                meeting_result = meeting_result + 'email adress, '
            elif user_email:
                session['user_email'] = user_email
        
            # Check and store user fullname
            if not user_name and not 'user_name' in session or user_name == 'Jérémy Chassin':
                meeting_result = meeting_result + 'full name, '
            elif user_name:
                session['user_name'] = user_name
        
            # Check and store meeting time
            if not meeting_date and not 'meeting_date' in session:
                meeting_result = meeting_result + 'meeting time, '
            elif meeting_date:
                session['meeting_date'] = meeting_date
        
            if 'user_email' in session and 'user_name' in session and 'meeting_date' in session:
                need_additional_info = False
                # Parse meeting_date to get start and end time
                meeting_datetime = datetime.strptime(session['meeting_date'], '%Y-%m-%d %H:%M:%S')
                end_datetime = meeting_datetime + timedelta(hours=1)  # Assuming the meeting lasts 1 hour

                # Define event details
                event = {
                    'summary': f"Meeting with {session['user_name']}",
                    'start': {
                        'dateTime': meeting_datetime.strftime('%Y-%m-%dT%H:%M:%S'),
                        'timeZone': 'UTC'
                    },
                    'end': {
                        'dateTime': end_datetime.strftime('%Y-%m-%dT%H:%M:%S'),
                        'timeZone': 'UTC'
                    },
                    'attendees': [
                        {'email': user_email},
                        {'email': Config.GOOGLE_CALENDAR_CLIENT_EMAIL}
                    ],
                    'conferenceData': {
                        'createRequest': {
                            'requestId': str(uuid.uuid4()),
                        },
                    },
                }

                # Call the Calendar API to create the event
                event = self.googleCalendar_service.events().insert(calendarId=Config.GOOGLE_CALENDAR_CLIENT_EMAIL, body=event).execute()

                # Format the meeting time and attendees for the return statement
                formatted_meeting_time = f'{meeting_datetime:%Y-%m-%d %H:%M:%S} to {end_datetime:%H:%M:%S} (UTC)'
                formatted_attendees = ', '.join([attendee['email'] for attendee in event['attendees']])

                meeting_result = f'Google Calendar invitation created. Event ID: {event["id"]}\nMeeting Time: {formatted_meeting_time}\nAttendees: {formatted_attendees}'

            return meeting_result, need_additional_info
        except Exception as error:
            return error
    
    
    def complete_Google_calendar_invitation_informations(self, data=None):
        """Tool method to complete a Google Calendar event informations.
        """
        meeting_result = self.send_GoogleCalendar_invitation(data=data)

        return meeting_result

    def init_GoogleCalendar(self):
        try:
            with open('credentials.json', 'r') as f:
                credentials_data = json.load(f)
                credentials = Credentials.from_authorized_user_info(credentials_data)
           
            # Use the credentials to build the Calendar service
            self.googleCalendar_service = build('calendar', 'v3', credentials=credentials)

        except Exception as error:
            print(f"An error occurred: {error}")