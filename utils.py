import os
from dotenv import load_dotenv
from twilio.rest import Client
from datetime import datetime, timedelta
from lib.booking import *
from lib.availability import *

"""
Check that new availability does not overlap with any existing available date ranges for that listing
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
Check if requested booking falls within one of the available date ranges for that listing
"""

def check_requested_booking_availability(availabilities, requested_start_date, requested_end_date):
    for availability in availabilities:
        start_date = availability.start_date
        end_date = availability.end_date

        if (start_date <= requested_start_date <= end_date) and (start_date <= requested_end_date <= end_date):
            return True
    
    return False

"""
Send sms to owner of a listing when there property has been requested
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
Send sms to requesting user when there request has been dealt with (approved, denied etc)
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

"""
If a booking status is accepted, remove the dates of the booking from the availability table
"""

def remove_availability(booking):
    booking_dates = [booking.start_date + timedelta(days=i) for i in range((booking.end_date - booking.start_date).days + 1)]
    availabilities = Availability.select().where(Availability.listing_id == booking.listing_id)

    for availability in availabilities:
        availability_dates = [availability.start_date + timedelta(days=i) for i in range((availability.end_date - availability.start_date).days + 1)]
        new_availability_dates = [date for date in availability_dates if date not in booking_dates]

        if new_availability_dates:
            new_availabilities = split_dates_on_gap(new_availability_dates)
            Availability.create(
                listing_id=booking.listing_id,
                start_date=new_availabilities[0][0],
                end_date=new_availabilities[0][-1],
                available=True
            )

            if len(new_availabilities) > 1:
                Availability.create(
                    listing_id=booking.listing_id,
                    start_date=new_availabilities[1][0],
                    end_date=new_availabilities[1][-1],
                    available=True
                )

        availability.delete_instance()

"""
Split a list of dates into consecutive lists based on a gap threshold.
"""

def split_dates_on_gap(date_list, gap_threshold=timedelta(days=1)):
    consecutive_lists = []
    current_consecutive_list = [date_list[0]]

    for i in range(1, len(date_list)):
        current_date = date_list[i]
        prev_date = date_list[i - 1]

        if (current_date - prev_date) <= gap_threshold:
            current_consecutive_list.append(current_date)
        else:
            consecutive_lists.append(current_consecutive_list)
            current_consecutive_list = [current_date]

    consecutive_lists.append(current_consecutive_list)
    return consecutive_lists
