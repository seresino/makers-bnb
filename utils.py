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