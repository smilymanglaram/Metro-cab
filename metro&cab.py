import streamlit as st
import qrcode
from io import BytesIO
import uuid
from PIL import Image
import base64


def generate_qr(data):
    qr=qrcode.QRCode(version=1,box_size=10,border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img=qr.make_image(fill_color="black",back_color="white")
    return img

#streamlit ui
st.set_page_config(page_title="Metro Ticket Booking system with QR code + Auto voice")
stations=["Miyapur","Ameerpet","JNTU","LB Nagar"]
name=st.text_input("Passenger Name")
source=st.selectbox("source station",stations)
destination=st.selectbox("destination station",stations)
no_tickets=st.number_input("No of Tickets", min_value=1,value=1)
price_per_ticket=30
cab_charge=100
total_amount=no_tickets*price_per_ticket
st.info(f"Total Amount:(total_amount)")
st.subheader("Do you need a Cab?")
cab_required = st.radio("", ["NO", "YES"], horizontal=True)

drop_location = ""


if cab_required == "YES":
    drop_location = st.text_input("Enter Drop Location")
    
    
metro_amount = no_tickets * price_per_ticket
total_amount = metro_amount + cab_charge

st.info(f" Total Amount: ₹{total_amount}")


#booking button
if st.button("Book Ticket"):
    if name.strip() =="":
        st.error("Please Enter the Passenger name:")
    elif source == destination:
        st.error("source and destination cannot be same")
    elif cab_required == "YES" and drop_location.strip() == "":
        st.error("Please enter drop location")
    else:
        booking_id= str(uuid.uuid4()) [:8]
        

        qr_data = (
            f"Booking ID: {booking_id}\n"
            f"Name: {name}\n"
            f"From: {source}\n"
            f"To: {destination}\n"
            f"no_tickets: {no_tickets}\n"
            f"Cab: {cab_required}\n"
            f"Drop: {drop_location if cab_required == 'YES' else 'N/A'}\n"
            f"Total Amount: ₹{total_amount}"
        )

        

        qr_img=generate_qr(qr_data)

        buf= BytesIO()
        qr_img.save(buf, format="PNG")
        qr_bytes = buf.getvalue()

        st.success("Ticket Booked Successfully")


        st.write("###Ticket Details")
        st.write(f"**Booking ID:** {booking_id}")
        st.write(f"**Passenger:** {name}")
        st.write(f"**From:** {source}")
        st.write(f"**To:** {destination}")
        st.write(f"**no_tickets:** {no_tickets}")
        

        if cab_required == "YES":
            st.write("**Cab Booked**")
            st.write(f"**Drop Location:** {drop_location}")
        else:
            st.write("**Metro Ticket Only**")

        
        st.write(f"**Amount Paid:** {total_amount}")
        
        st.image(qr_bytes, width=250)

