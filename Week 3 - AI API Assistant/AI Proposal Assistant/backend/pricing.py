
import json
import math
from decimal import Decimal
from pathlib import Path


PROFILE_FILE = Path(__file__).resolve().parent / "pricing_profile.json"


def load_pricing_profile(overrides=None):
    """
    Load the default pricing profile.
    Allow individual projects to override its settings.
    """

    with open(PROFILE_FILE, "r", encoding="utf-8") as file:
        profile = json.load(file)

    if overrides:
        profile.update(overrides)

    required_fields = [
        "currency",
        "daily_rate",
        "minimum_project_fee",
        "working_hours_per_day",
        "payment_terms",
        "delivery_buffer_multiplier"
    ]

    missing = [
        field for field in required_fields
        if profile.get(field) is None
    ]

    if missing:
        raise ValueError(
            f"Missing pricing profile settings: {', '.join(missing)}"
        )

    return profile


def calculate_project_price(estimated_days, overrides=None):
    """
    Calculate project pricing and proposed delivery duration.
    """

    if estimated_days <= 0:
        raise ValueError("Estimated working days must be positive.")

    profile = load_pricing_profile(overrides)

    daily_rate = Decimal(str(profile["daily_rate"]))
    minimum_fee = Decimal(str(profile["minimum_project_fee"]))

    estimated_cost = daily_rate * Decimal(str(estimated_days))
    final_price = max(estimated_cost, minimum_fee)

    buffer_multiplier = float(profile["delivery_buffer_multiplier"])

    if buffer_multiplier < 1:
        raise ValueError("Delivery buffer multiplier must be at least 1.")

    delivery_days = math.ceil(estimated_days * buffer_multiplier)

    return {
        "currency": profile["currency"],
        "estimated_days": estimated_days,
        "delivery_days": delivery_days,
        "daily_rate": daily_rate,
        "minimum_project_fee": minimum_fee,
        "final_price": final_price,
        "payment_terms": profile["payment_terms"]
    }