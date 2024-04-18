import streamlit as st
import phonenumbers
import folium
from streamlit_folium import folium_static
from phonenumbers import carrier

from opencage.geocoder import OpenCageGeocode
from location import get_location_from_phone_number


# Set up OpenCage API


def get_location_from_phone_number(phone_number):
    from phonenumbers import geocoder
    samNumber = phonenumbers.parse(phone_number)
    
    #st.write("hi")
    region = geocoder.description_for_number(samNumber,'en')
    service_provider = carrier.name_for_number(samNumber, "en")
    #st.write(region)
    api_key = '8d84206c5a29446787fef9be70275ebf'
    geocoder = OpenCageGeocode(api_key)
    query=str(region)
    results=geocoder.geocode(query)
  

    lat=results[0]['geometry']['lat']
    lng=results[0]['geometry']['lng']

    return lat,lng,region,service_provider
    

# Streamlit UI
st.title("  Phone Number Location Finder")
st.image("img.png", caption="")

phone_number = st.text_input("Enter the phone number (with country code, e.g., +123456789):")

if st.button("Find Location"):
    if phone_number:
        st.write(f"Searching location for phone number: {phone_number}")
        lat, lng, region,service_provider = get_location_from_phone_number(phone_number)
        if lat is not None and lng is not None:
            st.success(f"Location found: {region}")
            st.error(f"Service Provider: {service_provider}")
            my_map = folium.Map(location=[lat, lng], zoom_start=9)
            folium.Marker([lat, lng], popup=region).add_to(my_map)
            folium_static(my_map)
            st.warning("*****************THANK YOU!*******************")
        else:
            st.error("Failed to find location for the provided phone number.")
    else:
        st.warning("Please enter a phone number.")
