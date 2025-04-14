from flask import Blueprint, request, render_template
from datetime import datetime, timedelta
from models.history import History
from db import db


blp = Blueprint("calculate_age", __name__)


def parse_birth_datetime(birthdate_str, birthtime_str):
    """Parse and validate birth date and time strings."""
    if not birthdate_str:
        raise ValueError("Birthdate is required")
    dt_str = f"{birthdate_str} {birthtime_str}"
    return datetime.strptime(dt_str, "%Y-%m-%d %H:%M")


def calculate_years_months_and_days(birth_datetime, now):
    """Calculate complete years, months and days of age."""
    years = now.year - birth_datetime.year
    months = now.month - birth_datetime.month
    days = now.day - birth_datetime.day

    # Adjust years and months if needed
    if now.month < birth_datetime.month or (
        now.month == birth_datetime.month and now.day < birth_datetime.day
    ):
        years -= 1
        months += 12

    # Adjust months and days if needed
    if days < 0:
        # Get the last day of the previous month
        if months == 0:
            months = 11
            years -= 1
        else:
            months -= 1
        # Calculate days remaining in the last month
        last_month = now.replace(day=1) - timedelta(days=1)
        days = last_month.day + days

    return years, months, days


def calculate_remaining_time(birth_datetime, now, years, months, days):
    """Calculate remaining hours, minutes, and seconds."""
    # Calculate reference date for remaining time
    try:
        next_month = birth_datetime.month + months
        ref_month = (
            next_month if next_month <= 12 else (next_month % 12 or 12)
        )
        reference_date = birth_datetime.replace(
            year=birth_datetime.year + years,
            month=ref_month,
            day=birth_datetime.day + days
        )
    except ValueError:
        # Handle case where the day might be invalid for the target month
        next_month = birth_datetime.month + months + 1
        ref_month = (
            next_month if next_month <= 12 else (next_month % 12 or 12)
        )
        next_month = birth_datetime.replace(
            year=birth_datetime.year + years,
            month=ref_month
        )
        reference_date = next_month - timedelta(days=1)

    time_diff = now - reference_date

    # Calculate hours, minutes and seconds
    total_seconds = int(time_diff.total_seconds())
    hours = (total_seconds // 3600) % 24
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    return hours, minutes, seconds


def format_detailed_age(years, months, days, hours, minutes, seconds):
    """Format the detailed age string."""
    def plural(num, unit):
        return f"{num} {unit}{'s' if num != 1 else ''}"

    detailed_age_parts = []
    if years > 0:
        detailed_age_parts.append(plural(years, "year"))
    if months > 0:
        detailed_age_parts.append(plural(months, "month"))
    if days > 0:
        detailed_age_parts.append(plural(days, "day"))
    if hours > 0:
        detailed_age_parts.append(plural(hours, "hour"))
    if minutes > 0:
        detailed_age_parts.append(plural(minutes, "minute"))
    if seconds > 0:
        detailed_age_parts.append(plural(seconds, "second"))

    if not detailed_age_parts:
        return "0 seconds"

    if len(detailed_age_parts) == 1:
        return detailed_age_parts[0]

    return (
        ", ".join(detailed_age_parts[:-1])
        + " and "
        + detailed_age_parts[-1]
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
    """Calculate age based on birthdate and time."""
    # Default to 09:00 if not provided
    birthdate_str = request.form.get("birthdate")
    birthtime_str = request.form.get("birthtime", "09:00")

    try:
        birth_datetime = parse_birth_datetime(birthdate_str, birthtime_str)
        now = datetime.now()

        # Calculate main components
        years, months, days = calculate_years_months_and_days(
            birth_datetime, now
        )
        hours, minutes, seconds = calculate_remaining_time(
            birth_datetime, now, years, months, days
        )

        # Format detailed age string
        detailed_age = format_detailed_age(
            years, months, days, hours, minutes, seconds
        )

        # Calculate other representations
        age_data = calculate_total_units(birth_datetime, now, years, months)
        age_data["detailed_age"] = detailed_age
        age_data["days"] = days  # Add days to the age data

        # Save calculation to history
        save_to_history(None, age_data)

        # Get context from base route logic to show history
        context = db.session.execute(
            db.select(History).order_by(History.id.desc()).limit(10)
        ).scalars()
        age_data["context"] = context

        return render_template("base.html", **age_data)
    except ValueError as e:
        # Get context even when there's an error
        context = db.session.execute(
            db.select(History).order_by(History.id.desc()).limit(10)
        ).scalars()
        error_msg = (
            "Invalid date/time format. "
            "Use YYYY-MM-DD for date and HH:MM for time. "
            f"{str(e)}"
        )
        return render_template(
            "base.html",
            error=error_msg,
            context=context,
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
