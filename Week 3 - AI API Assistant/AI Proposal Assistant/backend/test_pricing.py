
from backend.pricing import calculate_project_price


# Temporary test profile.
# These are test values, not your actual pricing settings.
test_profile = {
    "currency": "KES",
    "daily_rate": 3500,
    "minimum_project_fee": 10000,
    "working_hours_per_day": 8,
    "payment_terms": "50% upfront, 50% on completion",
    "delivery_buffer_multiplier": 1.5
}


result = calculate_project_price(
    estimated_days=5,
    overrides=test_profile
)

print("\nPROJECT PRICING TEST")
print("====================")
print(f"Currency: {result['currency']}")
print(f"Estimated days: {result['estimated_days']}")
print(f"Proposed delivery days: {result['delivery_days']}")
print(f"Daily rate: {result['daily_rate']}")
print(f"Minimum fee: {result['minimum_project_fee']}")
print(f"Final quotation: {result['currency']} {result['final_price']}")
print(f"Payment terms: {result['payment_terms']}")
