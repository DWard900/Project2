from app import app

# Filter for Jinja to format datetime to Day, DD MM YYYY at HH:MM
@app.template_filter('formatdatetime_long')
def format_datetime_long(value, format="%A, %d %B %Y at %H:%M UTC"):
    if value is None:
        return ""
    return value.strftime(format)

# Filter for Jinja to format datetime to Day, DD MM YYYY
@app.template_filter('formatdatetime_short')
def format_datetime_short(value, format="%A, %d %B %Y"):
    if value is None:
        return ""
    return value.strftime(format)