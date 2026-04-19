def get_age_group(age: int):
    if age <= 12:
        return "child"
    elif age <= 19:
        return "teenager"
    elif age <= 59:
        return "adult"
    else:
        return "senior"


def get_top_country(country_data):
    if not country_data:
        return None
    return max(country_data, key=lambda x: x["probability"])