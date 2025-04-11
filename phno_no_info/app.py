from flask import Flask, render_template, request
import phonenumbers
from phonenumbers import timezone, geocoder, carrier
from geopy.geocoders import Nominatim

# Initialize Flask app and geolocator
app = Flask(__name__)
geolocator = Nominatim(user_agent="geoapi")

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        number = request.form.get('phone_number')  # Get the inputted phone number
        try:
            # Parsing string to the Phone number
            phoneNumber = phonenumbers.parse(number)

            # Getting timezone
            timeZones = timezone.time_zones_for_number(phoneNumber)

            # Getting geolocation (country or city)
            geolocation = geocoder.description_for_number(phoneNumber, "en")

            # Getting geographic region code (e.g., IN, US, GB)
            region_code = phonenumbers.region_code_for_number(phoneNumber)

            # Getting service provider
            service = carrier.name_for_number(phoneNumber, "en")

            # Fetching latitude and longitude using geopy
            latitude = longitude = None
            if geolocation:
                location = geolocator.geocode(geolocation)
                if location:
                    latitude = location.latitude
                    longitude = location.longitude

            return render_template('index.html', timeZones=timeZones, geolocation=geolocation, region_code=region_code,
                                   service=service, latitude=latitude, longitude=longitude, number=number)

        except phonenumbers.phonenumberutil.NumberParseException:
            return render_template('index.html', error="Invalid phone number format. Please try again.")

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)