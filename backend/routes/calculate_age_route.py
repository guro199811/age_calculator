from flask import Blueprint, request, render_template
from datetime import datetime

from models.history import History
from db import db


blp = Blueprint("calculate_age", __name__)


def parse_birth_datetime(birthdate_str, birthtime_str):
    """Parse and validate birth date and time strings."""
    if not birthdate_str:
        raise ValueError("Birthdate is required")
    return datetime.strptime(f"{birthdate_str} {birthtime_str}", "%Y-%m-%d %H:%M")


def calculate_years_and_months(birth_datetime, now):
    """Calculate complete years and months of age."""
    years = now.year - birth_datetime.year
    months = now.month - birth_datetime.month

    # Adjust years and months if needed
    if now.month < birth_datetime.month or (
        now.month == birth_datetime.month and now.day < birth_datetime.day
    ):
        years -= 1
        months += 12

    # Adjust months if day of month needs rollover
    if now.day < birth_datetime.day:
        months -= 1
        if months < 0:
            months += 12
            years -= 1

    return years, months


def calculate_remaining_time(birth_datetime, now, years, months):
    """Calculate remaining hours, minutes, and seconds."""
    # Calculate reference date for remaining time
    reference_date = birth_datetime.replace(
        year=now.year - years,
        month=now.month - months if now.month > months else now.month + (12 - months),
    )
    time_diff = now - reference_date

    # Calculate hours, minutes and seconds
    total_seconds = int(time_diff.total_seconds())
    hours = (total_seconds // 3600) % 24  # Only remaining hours after complete days
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    return hours, minutes, seconds


def format_detailed_age(years, months, hours, minutes, seconds):
    """Format the detailed age string."""
    detailed_age_parts = []
    if years > 0:
        detailed_age_parts.append(f"{years} year{'s' if years != 1 else ''}")
    if months > 0:
        detailed_age_parts.append(f"{months} month{'s' if months != 1 else ''}")
    if hours > 0:
        detailed_age_parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        detailed_age_parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0:
        detailed_age_parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")

    return (
        ", ".join(detailed_age_parts[:-1])
        + (" and " if len(detailed_age_parts) > 1 else "")
        + detailed_age_parts[-1]
        if detailed_age_parts
        else "0 seconds"
    )


def calculate_total_units(birth_datetime, now, years, months):
    """Calculate age in various units."""
    total_days = (now - birth_datetime).days
    total_seconds = int((now - birth_datetime).total_seconds())

    return {
        "age": years,
        "months": months,
        "age_in_days": total_days,
        "age_in_weeks": total_days // 7,
        "age_in_months": (years * 12) + months,
        "age_in_hours": total_days * 24,
        "age_in_minutes": total_days * 24 * 60,
        "age_in_seconds": total_seconds,
    }


@blp.route("/calculate_age", methods=["POST"])
def calculate_age():
    """
    Calculate the age of a person based on their birthdate and time.
    :return: Rendered template with detailed age calculations
    """
    birthdate_str = request.form.get("birthdate")
    birthtime_str = request.form.get("birthtime", "09:00")  # Default to 09:00 if not provided

    try:
        birth_datetime = parse_birth_datetime(birthdate_str, birthtime_str)
        now = datetime.now()

        # Calculate main components
        years, months = calculate_years_and_months(birth_datetime, now)
        hours, minutes, seconds = calculate_remaining_time(birth_datetime, now, years, months)
        
        # Format detailed age string
        detailed_age = format_detailed_age(years, months, hours, minutes, seconds)

        # Calculate other representations
        age_data = calculate_total_units(birth_datetime, now, years, months)
        age_data["detailed_age"] = detailed_age

        # Save calculation to history
        save_to_history(None, age_data)

        return render_template("base.html", **age_data)
    except ValueError:
        return render_template(
            "base.html",
            error="Invalid date/time format. Use YYYY-MM-DD for date and HH:MM for time.",
        )


def save_to_history(country, data):
    """
    Save the calculation to the history database.
    :param country: The country of the person
    :param data: The data to save
    """
    try:
        history = History(country=country, data=data)
        db.session.add(history)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error saving to history: {e}")
        return False
