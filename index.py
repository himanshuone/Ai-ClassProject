import streamlit as st
import requests
from amadeus import Client, ResponseError

# Amadeus API Configuration
AMADEUS_API_KEY = "OxtZ0Ag83s7KvtgXiSvAM6rmKCHxdbVW"
AMADEUS_API_SECRET = "ZhLFMRDCzpthzkOY"

# Initialize Amadeus Client
amadeus = Client(client_id=AMADEUS_API_KEY, client_secret=AMADEUS_API_SECRET)

# List of major Indian airports with their IATA codes
INDIAN_AIRPORTS = {
    "Delhi (DEL)": "DEL",
    "Mumbai (BOM)": "BOM",
    "Bangalore (BLR)": "BLR",
    "Hyderabad (HYD)": "HYD",
    "Chennai (MAA)": "MAA",
    "Kolkata (CCU)": "CCU",
    "Pune (PNQ)": "PNQ",
    "Ahmedabad (AMD)": "AMD",
    "Jaipur (JAI)": "JAI",
    "Goa (GOI)": "GOI"
}

# Function to fetch flight details from Amadeus API
def fetch_flight_details(origin, destination, date):
    try:
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origin,
            destinationLocationCode=destination,
            departureDate=date,
            adults=1,
            currencyCode="INR"
        )
        
        flights = response.data
        if not flights:
            return "No flight data found. Try a different date or route."
        
        flight_info_list = []
        for flight in flights[:5]:  # Display up to 5 flights
            airline = flight["validatingAirlineCodes"][0]
            flight_number = flight["itineraries"][0]["segments"][0]["carrierCode"] + flight["itineraries"][0]["segments"][0]["number"]
            departure_time = flight["itineraries"][0]["segments"][0]["departure"]["at"]
            arrival_time = flight["itineraries"][0]["segments"][0]["arrival"]["at"]
            price = flight["price"]["total"]
            
            flight_info_list.append(
                f"Flight {flight_number} by {airline}\nDeparture: {departure_time}\nArrival: {arrival_time}\nPrice: ₹{price}"
            )
        return "\n\n".join(flight_info_list)
    except ResponseError as error:
        return f"Error fetching flight data: {error}"

# Streamlit UI
def main():
    st.title("AI Flight Tracker (India) - Amadeus API")
    
    origin = st.selectbox("Select Origin Airport:", list(INDIAN_AIRPORTS.keys()))
    destination = st.selectbox("Select Destination Airport:", list(INDIAN_AIRPORTS.keys()))
    date = st.date_input("Select Travel Date:")
    
    if st.button("Check Flight Details"):
        origin_code = INDIAN_AIRPORTS[origin]
        destination_code = INDIAN_AIRPORTS[destination]
        flight_info = fetch_flight_details(origin_code, destination_code, str(date))
        st.write(flight_info)

if __name__ == "__main__":
    main()
