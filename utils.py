import os
from dotenv import load_dotenv
from twilio.rest import Client

"""
check that new availability does not overlap with any existing available date ranges for that listing
"""

def check_availability_overlap(availabilities, new_start_date, new_end_date):
    for availability in availabilities:
        existing_start_date = availability.start_date
        existing_end_date = availability.end_date

        if (
            (existing_start_date <= new_start_date <= existing_end_date) or
            (existing_start_date <= new_end_date <= existing_end_date) or
            (new_start_date <= existing_start_date and new_end_date >= existing_end_date)
        ):
            return True
    return False

"""
check if requested booking falls within one of the available date ranges for that listing
"""

def check_requested_booking_availability(availabilities, requested_start_date, requested_end_date):
    for availability in availabilities:
        start_date = availability.start_date
        end_date = availability.end_date

        if requested_start_date <= end_date and requested_end_date >= start_date:
            return True
    
    return False

"""
send sms to owner of a listing when there property has been requested
"""

def send_request_sms(twilio_num, recipitent_num, message):
    load_dotenv()
    client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
    message = client.messages.create(
        body = message,
        from_ = twilio_num,
        to = recipitent_num
    )
    return None

"""
send sms to requesting user when there request has been dealt with (approved, denied etc)
"""

def send_request_outcome_sms(twilio_num, recipitent_num, message):
    load_dotenv()
    client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
    message = client.messages.create(
        body = message,
        from_ = twilio_num,
        to = recipitent_num
    )
    return None