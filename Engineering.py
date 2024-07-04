import streamlit as st
import pandas as pd
import numpy as np
import os
import requests
from datetime import datetime
import json



st.set_page_config(
    layout="wide",
    page_title='Earthquake analysis',
    page_icon='🪙'
)



df_f = pd.read_csv('Eng Spare parts.csv')



def load_users():
    try:
        with open('users3.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "knhp322": {"password": "knhp322", "first_login": True, "name": "Shehab Ayman "},    # shehab
            "krxs742": {"password": "krxs742", "first_login": True, "name": "Mohamed Ashry"},    # ashry
            "kxsv748": {"password": "kxsv748", "first_login": True, "name": "Mohamed El masry"}, # el masry
            "kvwp553": {"password": "kvwp553", "first_login": True, "name": "sameh"},            # sameh
            "knfb489": {"password": "knfb489", "first_login": True, "name": "Yasser Hassan"},    # yasser
            "kjjd308": {"password": "kjjd308", "first_login": True, "name": "Kaleed "},          # kaleed
            "kibx268": {"password": "kibx268", "first_login": True, "name": "Zeinab Mobarak" }}  #Zinab

# حفظ بيانات المستخدمين إلى ملف JSON
def save_users(users3):
    with open('users3.json', 'w') as f:
        json.dump(users3, f)

users3 = load_users()

# دالة لتسجيل الدخول
def login(username, password):
    if username in users3 and users3[username]["password"] == password:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.first_login = users3[username]["first_login"]
    else:
        st.error("Incorrect username or password")

# دالة لتحديث كلمة المرور
def update_password(username, new_password):
    users3[username]["password"] = new_password
    users3[username]["first_login"] = False
    save_users(users3)
    st.session_state.first_login = False
    st.success("Password updated successfully!")

# دالة لإعادة تعيين كلمات المرور الافتراضية وتحديث الأسماء
def reset_passwords_and_update_usernames(new_usernames, new_password="password"):
    global users3
    users3 = {new_usernames[i]: {"password": new_password, "first_login": True} for i in range(len(new_usernames))}
    save_users(users3)

# دالة لتحديث الكمية
def update_quantity(row_index, quantity, operation, username):
    old_quantity = st.session_state.df.loc[row_index, 'Qty.']
    if operation == 'add':
        st.session_state.df.loc[row_index, 'Qty.'] += quantity
    elif operation == 'subtract':
        st.session_state.df.loc[row_index, 'Qty.'] -= quantity
    new_quantity = st.session_state.df.loc[row_index, 'Qty.']

    st.session_state.df.to_csv('Eng Spare parts.csv', index=False)
    st.success(f"Quantity updated successfully by {username}! New Quantity: {int(st.session_state.df.loc[row_index, 'Qty.'])}")

    log_entry = {
        'user': username,
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'item': st.session_state.df.loc[row_index, 'Item description'],
        'old_quantity': old_quantity,
        'new_quantity': new_quantity,
        'operation': operation
    }
    st.session_state.logs.append(log_entry)
    
    # حفظ السجلات إلى ملف CSV
    logs_df = pd.DataFrame(st.session_state.logs)
    logs_df.to_csv('logs.csv', index=False)



# عرض التبويبات
def display_tab(tab_name):
    st.header(f'{tab_name} Tab')
    row_number = st.number_input(f'Select row number for {tab_name}:', min_value=0, max_value=len(st.session_state.df)-1, step=1, key=f'{tab_name}_row_number')

    st.markdown(f"""
    <div style='font-size: 20px; color: blue;'>Selected Item: {st.session_state.df.loc[row_number, 'Item description']}</div>
    <div style='font-size: 20px; color: blue;'>Current Quantity: {int(st.session_state.df.loc[row_number, 'Qty.'])}</div>
    <div style='font-size: 20px; color: red;'>Location: {st.session_state.df.loc[row_number, 'Location']}</div>
    """, unsafe_allow_html=True)

    quantity = st.number_input(f'Enter quantity for {tab_name}:', min_value=0, step=1, key=f'{tab_name}_quantity')
    operation = st.radio(f'Choose operation for {tab_name}:', ('add', 'subtract'), key=f'{tab_name}_operation')

    if st.button('Update Quantity', key=f'{tab_name}_update_button'):
        update_quantity(row_number, quantity, operation, st.session_state.username)

# واجهة تسجيل الدخول
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.logs = []

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        st.button("Login")
        login(username, password)
else:
    if st.session_state.first_login:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.subheader("Change Password")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            st.button("Change Password")
            if st.button("Log in"):
                if new_password == confirm_password:
                    users3[st.session_state.username]['password'] = new_password
                    users3[st.session_state.username]['first_login'] = False
                    save_users(users3)
                    st.session_state.first_login = False
                    st.success("Password changed successfully!")
                else:
                    st.error("Passwords do not match")
    else:
        st.markdown(f"<div style='text-align: right; font-size: 20px; color: green;'> Login by : {users3[st.session_state.username]['name']}</div>", unsafe_allow_html=True)
        
        # قراءة البيانات
        if 'df' not in st.session_state:
            st.session_state.df = pd.read_csv('Eng Spare parts.csv')
        try:
            logs_df = pd.read_csv('logs.csv')
            st.session_state.logs = logs_df.to_dict('records')
        except FileNotFoundError:
            st.session_state.logs = []
            
        page =  st.sidebar.radio('Select page', ['Utility area','Mechanical parts', 'Electrical parts',
                        'Neumatic parts','FORKLIFT','LOTOTO','Add New Item & delete','View Logs'])
       
        
        if page == 'Mechanical parts':
            def main():
                
                st.markdown("""
            <style>
                /* Add your custom CSS styles here */
                .stProgress > div > div > div {
                    background-color: #FFD700; /* Change the color of the loading spinner */
                    border-radius: 50%; /* Make the loading spinner circular */
                }
            </style>
        """, unsafe_allow_html=True)
                with st.spinner("Data loaded successfully!"):
                    import time
                    time.sleep(1)
        
                
                col1, col2 = st.columns([2, 0.75])
                with col1:
                    st.markdown("""
                        <h2 style='text-align: center; font-size: 40px; color: red;'>
                            Find your Mechanical parts
                        </h2>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Retrieve or initialize search keyword from session state
                    search_keyword = st.session_state.get('search_keyword', '')
                    search_keyword = st.text_input("Enter keyword to search:", search_keyword)
                    search_button = st.button("Search")
                    search_option = 'All Columns'
                
                # Function to search in dataframe
                def search_in_dataframe(df_f, keyword, option):
                    if option == 'All Columns':
                        result = df_f[df_f.apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)]
                    else:
                        result = df_f[df_f[option].astype(str).str.contains(keyword, case=False)]
                    return result
                
                # Clear search keyword on page refresh
                if st.session_state.get('refreshed', False):
                    st.session_state.search_keyword = ''
                    st.session_state.refreshed = False
                
                # Perform search if button is clicked and keyword is not empty
                if search_button and search_keyword:
                    # Update session state with current search keyword
                    st.session_state.search_keyword = search_keyword
                    search_results = search_in_dataframe(df_f, search_keyword, search_option)
                    st.write(f"Search results for '{search_keyword}' in {search_option}:")
                    st.dataframe(search_results, width=1000, height=200)
                
                # Set refreshed state to clear search keyword on page refresh
                st.session_state.refreshed = True 
                        
                tab1, tab2 ,tab3, tab4,tab5, tab6 ,tab7, tab8 ,tab10, tab11 ,tab12, tab13, tab14  = st.tabs(['Bearing', 'Belts','Shaft','Spring',
                'leaflet rooler','Cam','Clutch','Oil _ grease','Chain','Gearbox','Door','Couplin','Wheel CASTOR'])
                
                with tab1:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        peraing = df_f[df_f['Comments'] == 'Bearing'].sort_values(by='Comments')
                        st.dataframe(peraing,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('peraing')
                            
                    with col3:
                        st.subheader('image  for  these  part')
                        SKF,ASAHI,INA,KBC,IKO,NTN,NB = st.tabs(['SKF','ASAHI','INA','IKO','KBC','NB','NTN'])
                        with SKF:
                            image1 = open('images/1.jpeg', 'rb').read()
                            st.image(image1, width=150)
                            url = 'https://www.skf.com/id/productinfo/productid-6001-2Z%2FC3'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        with ASAHI:
                            image2 = open('images/2.jpg', 'rb').read()
                            st.image(image2,  width=150)
                            url = 'https://th.misumi-ec.com/en/vona2/detail/221000612127/?HissuCode=JAF10'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        with INA:
                            image3 = open('images/3.jpg', 'rb').read()
                            st.image(image3, width=150)
                            url = 'https://www.abf.store/s/en/bearings/STO12-INA/450653'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        with IKO:
                            image4 = open('images/4.jpg', 'rb').read()
                            st.image(image4,  width=150)
                            url = 'https://www.acorn-ind.co.uk/p/iko/closed-type-linear-ball-bearings/lme122232n-iko/'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        with KBC:
                            image5 = open('images/5.jpg', 'rb').read()
                            st.image(image5,  width=150)
                            url = 'https://trimantec.com/products/kbc-bearings-radial-bearing-6004-d-6004-rs'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        with NTN:
                            image6 = open('images/6.png', 'rb').read()
                            st.image(image6,  width=150)
                            url = 'https://www.2rs.bg/en-gb/6004-llu-5k-ntn.html'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        with NB:
                            image7 = open('images/7.jpg', 'rb').read()
                            st.image(image7, caption='FETTE', width=150)
                            url = 'https://www.abf.store/s/en/bearings/6212-2NSE-NACHI/381266'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
        
                with tab2:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Belts = df_f[df_f['Comments'] == 'Belts'].sort_values(by='Comments')
                        st.dataframe(Belts,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Belts')
                    with col3:
                        st.subheader('image  for  these  part')
                        OPTIBELT ,FEC, timing_belt = st.tabs(['OPTIBELT','FEC','timing belt'])
                        with OPTIBELT:
                            image8 = open('images/8.jpg', 'rb').read()
                            st.image(image8, width=150)
                            url = 'https://www.optibelt.com/en/home/'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        with FEC:
                            image9 = open('images/9.jpg', 'rb').read()
                            st.image(image9, width=150)
                            url = 'https://www.fecconsulting.dk/en/timing-belts/megaflex-timing-belts/pu-timing-belts-t10-flex/t10-2550.html'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        with timing_belt:
                            image10 = open('images/10.jpg', 'rb').read()
                            st.image(image10, width=150)
                            url = 'https://www.konlidainc.com/gear/timing-belt.asp'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                   
        
                with tab3:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Shaft = df_f[df_f['Comments'] == 'Shaft'].sort_values(by='Comments')
                        st.dataframe(Shaft,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Shaft')
                    with col3:
                        st.subheader('image  for  these  part')
                        GRUNDFOS, uhlmann  = st.tabs(['GRUNDFOS','uhlmann'])
                        with GRUNDFOS:
                            image11 = open('images/11.jpeg', 'rb').read()
                            st.image(image11, width=150)
                            url = 'https://product-selection.grundfos.com/eg/products/service-partkit/spare-shaft-seal-96488302?pumpsystemid=2346046284&tab=variant-specifications'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        with uhlmann:
                            image12 = open('images/12.jpg', 'rb').read()
                            st.image(image12, width=150)
                            url = 'https://www.uhlmann.de/services/support-services/spare-parts/'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                    
        
                with tab4:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Spring = df_f[df_f['Comments'] == 'Spring'].sort_values(by='Comments')
                        st.dataframe(Spring,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Spring')
                    with col3:
                        st.subheader('image  for  these  part')
                        TENSION,PRESSURE  = st.tabs(['TENSION','PRESSURE'])
                        with TENSION:
                            image13 = open('images/13.jpg', 'rb').read()
                            st.image(image13, width=150)
                            url = 'https://www.sawane-spring.com/product/use/tension_spring_extension_spring.php'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        with PRESSURE:
                            image14 = open('images/14.jpg', 'rb').read()
                            st.image(image14, width=150)
                            url = 'https://metal-spring.com/'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
        
        
                with tab5:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        leaflet_rooler = df_f[df_f['Comments'] == 'Leaflet rooler'].sort_values(by='Comments')
                        st.dataframe(leaflet_rooler,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('leaflet_rooler')
                    with col3:
                        st.subheader('image  for  these  part')
                        Alumnum,rubber  = st.tabs(['Alumnum','rubber'])
                        with Alumnum:
                            image15 = open('images/15.jpg', 'rb').read()
                            st.image(image15, width=150)
                            url = 'https://www.jctprinting.com/'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        with rubber:
                            image16 = open('images/16.jpeg', 'rb').read()
                            st.image(image16, width=150)
                            url = 'https://www.jctprinting.com/'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                    
        
                with tab6:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Cam = df_f[df_f['Comments'] == 'Cam'].sort_values(by='Comments')
                        st.dataframe(Cam,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Cam')
                    with col3:
                        st.subheader('image  for  these  part')
                        Cam_SKF,Cam_INA,Cam_IKO  = st.tabs(['Cam_SKF','Cam_INA','Cam_IKO'])
                        with Cam_SKF:
                            image17 = open('images/17.jpg', 'rb').read()
                            st.image(image17, width=150)
                            url = 'https://www.skf.com/sg/products/rolling-bearings/track-rollers/cam-followers/productid-KR%2022'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        with Cam_INA:
                            image18 = open('images/18.jpg', 'rb').read()
                            st.image(image18, width=150)
                            url = 'https://www.abf.store/s/en/bearings/KR19-PP-A-NMT-INA/501413'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        with Cam_IKO:
                            image19 = open('images/19.jpg', 'rb').read()
                            st.image(image19, width=150)
                            url = 'https://www.acorn-ind.co.uk/p/iko/cam-followers/cr10-iko/'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                    
        
                with tab7:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Clutch = df_f[df_f['Comments'] == 'Clutch'].sort_values(by='Comments')
                        st.dataframe(Clutch,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Clutch')
                    with col3:
                        st.subheader('image  for  these  part')
                        Mechanical,Electrical   = st.tabs(['Mechanical','Electrical '])
                        with Mechanical:
                            image20 = open('images/20.jpg', 'rb').read()
                            st.image(image20, width=150)
                            url = 'https://www.psbearings.com/html_products/mzeu-series-cam-type-cam-clutch-346.html'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        with Electrical :
                            image21 = open('images/21.jpeg', 'rb').read()
                            st.image(image21, width=150)
                            url = 'https://peacosupport.com/electromagnetic-brake-6nm-400nm'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                    
        
                with tab8:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Oil_grease = df_f[df_f['Comments'] == 'Oil _ grease'].sort_values(by='Comments')
                        st.dataframe(Oil_grease,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Oil_grease')
                    with col3:
                        st.subheader('image  for  these  part')
                        HYDRAULIC,Gear   = st.tabs(['HYDRAULIC','Gear '])
                        with HYDRAULIC:
                            image22 = open('images/22.jpg', 'rb').read()
                            st.image(image22, width=150)
                            url = 'https://www.schaefferoil.com/h1-hydraulic-oil.html'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        with Gear :
                            image23 = open('images/23.jpg', 'rb').read()
                            st.image(image23, width=150)
                            url = 'https://stores.buy1oils.com/new-schaeffer-products/schaeffer-2009-supreme-open-gear-lube-37-lbs/'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                    
        
                with tab10:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Chain = df_f[df_f['Comments'] == 'Chain'].sort_values(by='Comments')
                        st.dataframe(Chain,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Chain')
                    with col3:
                        st.subheader('image  for  these  part')
                        image24 = open('images/24.jpg', 'rb').read()
                        st.image(image24, width=150)
                        url = 'https://www.uhlmann.de/services/support-services/spare-parts/'
                        st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                    
                    
                with tab11:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Gearbox = df_f[df_f['Comments'] == 'Gearbox'].sort_values(by='Comments')
                        st.dataframe(Gearbox,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Gearbox')
                    with col3:
                        st.subheader('image  for  these  part')
                        BEVEL,Nema   = st.tabs(['BEVEL','Nema '])
                        with BEVEL:
                            image25 = open('images/25.jpg', 'rb').read()
                            st.image(image25, width=150)
                            url = 'https://www.unimec.eu/en/products/bevel-gearboxes/110/RR.html'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        with Nema :
                            image26 = open('images/26.jpg', 'rb').read()
                            st.image(image26, width=150)
                            url = 'https://www.phidgets.com/?prodid=1082'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                    
        
                with tab12:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Door = df_f[df_f['Comments'] == 'Door'].sort_values(by='Comments')
                        st.dataframe(Door,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Door')
                    with col3:
                        st.subheader('image  for  these  part')
                        Dorma,Cam_Hydraulic,Handl  = st.tabs(['Dorma','Cam_Hydraulic','Handl'])
                        with Dorma:
                            image27 = open('images/27.jpg', 'rb').read()
                            st.image(image27, width=150)
                            url = 'https://doorcontrolsdirect.co.uk/door-closer-spare-parts/1043-dorma-g-n-slide-arm-channel'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        with Cam_Hydraulic:
                            image28 = open('images/28.jpg', 'rb').read()
                            st.image(image28, width=150)
                            url = 'https://www.dnd.com.tw/en/category/Door-Closer.html'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        with Handl:
                            image29 = open('images/29.jpg', 'rb').read()
                            st.image(image29, width=150)
                            url = 'https://www.handleking.co.uk/heavy-duty-door-handles-with-return-to-door-lever-grade-3'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                    
                    
                with tab13:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Couplin = df_f[df_f['Comments'] == 'Couplin'].sort_values(by='Comments')
                        st.dataframe(Couplin,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Couplin')
                    with col3:
                        st.subheader('image  for  these  part')
                        Flexible_Couplin, BoWex_Couplin   = st.tabs(['Flexible_Couplin','BoWex_Couplin '])
                        with Flexible_Couplin:
                            image30 = open('images/30.jpeg', 'rb').read()
                            st.image(image30, width=150)
                            url = 'https://www.ttco.com/encoders/ae087-10-10.html'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        with BoWex_Couplin :
                            image31 = open('images/31.jpg', 'rb').read()
                            st.image(image31, width=150)
                            url = 'https://www.ktr.com/no/products/bowex-curved-tooth-gear-couplings/'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                    
        
                with tab14:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Wheel_CASTOR = df_f[df_f['Comments'] == 'Swivel castor'].sort_values(by='Comments')
                        st.dataframe(Wheel_CASTOR,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Wheel CASTOR')
                    with col3:
                        st.subheader('image  for  these  part')
                        image32 = open('images/32.jpg', 'rb').read()
                        st.image(image32, width=150)
                        url = 'https://www.shoplinco.com/colson-polyurethane-heavy-duty-total-lock-swivel-caster-8-x-2-1000-lbs-cap/'
                        st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                csv = df_f.to_csv(index=False)
                st.download_button(label="Download updated CSV", data=csv, file_name='updated_spare_parts.csv', mime='text/csv')
                    
            if __name__ == '__main__':
        
                main()
    
        if page == 'Electrical parts': 
            def main():
                st.markdown("""
            <style>
                /* Add your custom CSS styles here */
                .stProgress > div > div > div {
                    background-color: #FFD700; /* Change the color of the loading spinner */
                    border-radius: 50%; /* Make the loading spinner circular */
                }
            </style>
        """, unsafe_allow_html=True)
                with st.spinner("Data loaded successfully!"):
                    # Simulate loading data
                    import time
                    time.sleep(1)
        
                col1, col2 = st.columns([2, 0.75])
                with col1:
                    st.markdown("""
                        <h2 style='text-align: center; font-size: 40px; color: red;'>
                            Find your Electrical parts
                        </h2>
                    """, unsafe_allow_html=True)
                
                with col2:
                    search_keyword = st.text_input("Enter keyword to search:")
                    search_button = st.button("Search")
                    search_option = 'All Columns'
                def search_in_dataframe(df_f, keyword, option):
                    if option == 'All Columns':
                        result = df_f[df_f.apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)]
                    else:
                        result = df_f[df_f[option].astype(str).str.contains(keyword, case=False)]
                    return result
                
                if search_button and search_keyword:
                    search_results = search_in_dataframe(df_f, search_keyword, search_option)
                    st.write(f"Search results for '{search_keyword}' in {search_option}:")
                    st.dataframe(search_results, width=700, height=200)
                
                    
                tab1, tab2 ,tab3, tab4,tab5, tab6 ,tab7, tab8, tab9 ,tab10, tab11 ,tab12  = st.tabs(['Proximity','Sensor','Fiber sensor','Amplifier','Socket',
                'Selector','Button','Switch','Light','Fan','Cable','Fuse'])
                
        
                with tab1:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Proximity = df_f[df_f['Comments'] == 'Proximity'].sort_values(by='Comments')
                        st.dataframe(Proximity,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Proximity')
                    with col3:
                        st.subheader('image  for  these  part')
                        BALLUFF,MICRO_DETECTORS,IFM  = st.tabs(['BALLUFF','MICRO_DETECTORS','IFM'])
                        with BALLUFF:
                            image57 = open('images/57.PNG', 'rb').read()
                            st.image(image57, width=150)
                            url = 'https://valinonline.com/products/dw-as-503-m30-002'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        with MICRO_DETECTORS:
                            image58= open('images/58.PNG', 'rb').read()
                            st.image(image58, width=150)
                            url = 'https://www.electricautomationnetwork.com/en/micro-detectors/am1-an-1a-micro-detectors-inductive-sensor-m12-shielded-no-npn-cable-2m-axial'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        with IFM:
                            image59 = open('images/59.PNG', 'rb').read()
                            st.image(image59, width=150)
                            url = 'https://www.ifm.com/in/en/product/IF5345'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                
                with tab2:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Sensor = df_f[df_f['Comments'] == 'Sensor'].sort_values(by='Comments')
                        st.dataframe(Sensor,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Sensor')
                    with col3:
                        st.subheader('image  for  these  part')
                        SICK,BAUMER,DATALOGIC  = st.tabs(['SICK','BAUMER','DATALOGIC'])
                        with SICK:
                            image60 = open('images/60.PNG', 'rb').read()
                            st.image(image60, width=150)
                            url = 'https://www.sick.com/be/en/catalog/products/detection-sensors/color-sensors/cs8/cs81-p1112/p/p138054'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        with BAUMER:
                            image61= open('images/61.PNG', 'rb').read()
                            st.image(image61, width=150)
                            url = 'https://www.kempstoncontrols.com/FPDK-10N5101-S35A/Baumer/sku/136377'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        with DATALOGIC:
                            image62 = open('images/62.PNG', 'rb').read()
                            st.image(image62, width=150)
                            url = 'https://www.electricautomationnetwork.com/en/datalogic/s41-photoelectric-sensors-datalogic-s41-2-c-p-950701010'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                            
                    
                with tab3:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Fiber_sensor = df_f[df_f['Comments'] == 'Fiber sensor'].sort_values(by='Comments')
                        st.dataframe(Fiber_sensor,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Fiber sensor')
                    with col3:
                        st.subheader('image  for  these  part')
                        image63 = open('images/63.PNG', 'rb').read()
                        st.image(image63, width=150)
                        url = 'https://www.wenglor.com/en/Sensors/Photoelectronic-Sensors/Fiber-Optic-Sensors/Fiber-Optic-Cable-Amplifiers/Fiber-optic-amplifier/p/UM55PA2'
                        st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        
            
                with tab4:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Amplifier = df_f[df_f['Comments'] == 'Amplifier'].sort_values(by='Comments')
                        st.dataframe(Amplifier,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Amplifier')
                    with col3:
                        st.subheader('image  for  these  part')
                        image64 = open('images/64.PNG', 'rb').read()
                        st.image(image64, width=150)
                        url = 'https://www.pepperl-fuchs.com/global/en/classid_6.htm?view=productdetails&prodid=95425'
                        st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        
                    
                with tab5:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        
                        Socket = df_f[df_f['Comments'] == 'Socket'].sort_values(by='Comments')
                        st.dataframe(Socket,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Socket')
                    with col3:
                        st.subheader('image  for  these  part')
                        image65 = open('images/65.PNG', 'rb').read()
                        st.image(image65, width=150)
                        url = 'https://ie.farnell.com/hirschmann/ca6ld/cir-connector-receptacle-6pos/dp/3611905'
                        st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        
                    
                with tab6:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Selector = df_f[df_f['Comments'] == 'Selector'].sort_values(by='Comments')
                        st.dataframe(Selector,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Selector')
                    with col3:
                        st.subheader('image  for  these  part')
                        image66 = open('images/66.PNG', 'rb').read()
                        st.image(image66, width=150)
                        url = 'https://www.se.com/eg/en/product/XA2ED33/selector-switch-%C3%B822-standard-handle-3-positions-2no/'
                        st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        
                    
                with tab7:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:   
                        Button = df_f[df_f['Comments'] == 'Button'].sort_values(by='Comments')
                        st.dataframe(Button,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Button')
                    with col3:
                        st.subheader('image  for  these  part')
                        image67= open('images/67.PNG', 'rb').read()
                        st.image(image67, width=150)
                        url = 'https://za.rs-online.com/web/p/push-button-heads/3308975/'
                        st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        
                    
                with tab8:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:   
                        Switch = df_f[df_f['Comments'] == 'Switch'].sort_values(by='Comments')
                        st.dataframe(Switch,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Switch')
                    with col3:
                        st.subheader('image  for  these  part')
                        SICK,MOUJEN,SCHNEIDER  = st.tabs(['SICK','MOUJEN','SCHNEIDER'])
                        with SICK:
                            image68 = open('images/68.PNG', 'rb').read()
                            st.image(image68, width=150)
                            url = 'https://www.sick.com/us/en/catalog/products/safety/safety-switches/re1/re11-sa03/p/p315664'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        with MOUJEN:
                            image69= open('images/69.PNG', 'rb').read()
                            st.image(image69, width=150)
                            url = 'https://www.moujenswitch.com/product/me-8108-m/'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        with SCHNEIDER:
                            image70 = open('images/70.PNG', 'rb').read()
                            st.image(image70, width=150)
                            url = 'https://www.se.com/th/en/all-products'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                            
                    
                with tab9:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Light = df_f[df_f['Comments'] == 'Light'].sort_values(by='Comments')
                        st.dataframe(Light,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Light')
                    with col3:
                        st.subheader('image  for  these  part')
                        Filux,LED_OUTLET  = st.tabs(['Filux','LED OUTLET'])
                        with Filux:
                            image71 = open('images/71.PNG', 'rb').read()
                            st.image(image71, width=150)
                            url = 'https://filux.com/en/t8-pro-led-tubes/-t8-led-tube-9w-60cm-cct-3000k-4000k-6500k-130lm-w-5-years-warranty-6350.html'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        with LED_OUTLET:
                            image72= open('images/72.PNG', 'rb').read()
                            st.image(image72, width=150)
                            url = 'https://www.ledoutletpr.com/products/flood-lamp-200w'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                            
                    
                with tab10:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Fan = df_f[df_f['Comments'] == 'Fan'].sort_values(by='Comments')
                        st.dataframe(Fan,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Fan')
                    with col3:
                        st.subheader('image  for  these  part')
                        image73= open('images/73.PNG', 'rb').read()
                        st.image(image73, width=150)
                        url = 'https://au.element14.com/multicomp/sf23080a-2083hsl-gn/fan-80mm-230vac-23cfm-31dba/dp/9606238'
                        st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        
                    
                with tab11:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:               
                        Cable = df_f[df_f['Comments'] == 'Cable'].sort_values(by='Comments')
                        st.dataframe(Cable,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Cable')
                    with col3:
                        st.subheader('image  for  these  part')
                        CONNECTION,CAT6_CABLE,FIBER_OPTIC  = st.tabs(['SICK','CAT6 CABLE','FIBER OPTIC'])
                        with CONNECTION:
                            image74 = open('images/74.PNG', 'rb').read()
                            st.image(image74, width=150)
                            url = 'https://asi.net.nz/category/Sensor-Leads-Connectors-Valve-Cables'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        with CAT6_CABLE:
                            image75= open('images/75.PNG', 'rb').read()
                            st.image(image75, width=150)
                            url = 'https://de.assmann.shop/en/Copper-Network-Technology/Network-Cables/Installation-Cables/ASSNET250-Cat-6-U-UTP-installation-cable-305-m-Eca.html'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        with FIBER_OPTIC:
                            image76 = open('images/76.PNG', 'rb').read()
                            st.image(image76, width=150)
                            url = 'https://www.wenglor.com/pt/Sensors/Sensores-optoelectronicos/Fiber-Optic-Sensors/Glass-Fiber-Optic-Cables/Glass-Fiber-Optic-Cable-Through-Beam-Mode/p/SLK2313'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                            
                    
                with tab12:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:       
                        Fuse = df_f[df_f['Comments'] == 'Fuse'].sort_values(by='Comments')
                        st.dataframe(Fuse,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Fuse')
                    with col3:
                        st.subheader('image  for  these  part')
                        GLASS,CRAMIC  = st.tabs(['GLASS','CRAMIC'])
                        with GLASS:
                            image77 = open('images/77.PNG', 'rb').read()
                            st.image(image77, width=150)
                            url = 'https://makerselectronics.com/product/fuse-1a-250v-t5x20mm'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        with CRAMIC:
                            image78= open('images/78.PNG', 'rb').read()
                            st.image(image78, width=150)
                            url = 'https://witonics.com/products/siba-ceramic-fuse-6-3x32mm-time-delay-t200ma-7006565-0-200'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                   
        
                st.header('Select from these items')
                
                tab13, tab14 ,tab15, tab16,tab17, tab18 ,tab19, tab20, tab21 , tab23 ,tab24  = st.tabs(['Converter','Control','Conductor','Contactor','Controller',
                'Inverter','Relay','Jumper','Panel','Thermostate','Thermocouple'])
        
                with tab13:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Converter = df_f[df_f['Comments'] == 'Converter'].sort_values(by='Comments')
                        st.dataframe(Converter,width=2000)
                        col16, col2, col31 = st.columns([2,1,2])
                        with col16:
                            display_tab('Converter')
                    with col3:
                        st.subheader('image  for  these  part')
                        image90 = open('images/90.PNG', 'rb').read()
                        st.image(image90, width=150)
                        url = 'https://www.pepperl-fuchs.com/great_britain/en/classid_1830.htm?view=productdetails&prodid=48337'
                        st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                            
                            
                with tab14:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Control = df_f[df_f['Comments'] == 'Control'].sort_values(by='Comments')
                        st.dataframe(Control,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Control')
                    with col3:
                        st.subheader('image  for  these  part')
                        UHLMANN ,SCHNEIDER,SIEMENS  = st.tabs(['UHLMANN ','SCHNEIDER','SIEMENS'])
                        with UHLMANN :
                            image79 = open('images/79.PNG', 'rb').read()
                            st.image(image79, width=150)
                            url = 'https://industrie-24-de.myshopify.com/products/uhlmann-tsg4-v05-thyistor-steuergerat?shpxid=44aab6e7-988c-4f35-b98e-18acaff4cfee'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        with SCHNEIDER:
                            image80= open('images/80.PNG', 'rb').read()
                            st.image(image80, width=150)
                            url = 'https://eshop.se.com/ae/nfc-3-phase-monitoring-relay-harmony-8a-2co-multifunction-208a-480v-ac-rmnf22tb30.html'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        with SIEMENS:
                            image81 = open('images/81.PNG', 'rb').read()
                            st.image(image81, width=150)
                            url = 'https://www.lemu.dk/en/catalog/products/simatic-s7-1500f-cpu-1516f-3-pndp-central-processing-unit-with-15-mb-work-memory-for-program-and-5-mb-for-data/7889231828'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        
                with tab15:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Conductor = df_f[df_f['Comments'] == 'Conductor'].sort_values(by='Comments')
                        st.dataframe(Conductor,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Conductor')
                    with col3:
                        st.subheader('image  for  these  part')
                        image82 = open('images/82.PNG', 'rb').read()
                        st.image(image82, width=150)
                        url = 'https://www.wago.com/global/rail-mount-terminal-blocks/2-conductor-ground-terminal-block/p/280-907'
                        st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        
                with tab16:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Contactor = df_f[df_f['Comments'] == 'Contactor'].sort_values(by='Comments')
                        st.dataframe(Contactor,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Contactor')
                    with col3:
                        st.subheader('image  for  these  part')
                        NHP ,SCHNEIDER = st.tabs(['NHP ','SCHNEIDER'])
                        with NHP :
                            image83 = open('images/83.PNG', 'rb').read()
                            st.image(image83, width=150)
                            url = 'https://www.nhp.com.au/product/ca79e1024vdc'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        with SCHNEIDER:
                            image84= open('images/84.PNG', 'rb').read()
                            st.image(image84, width=150)
                            url = 'https://www.se.com/eg/en/product/LC1D18B7/tesys-d-contactor-3p3-no-ac3-440-v-18-a-24-v-ac-coil/'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        
                with tab17:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Controller = df_f[df_f['Comments'] == 'Controller'].sort_values(by='Comments')
                        st.dataframe(Controller,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Controller')
                    with col3:
                        st.subheader('image  for  these  part')
                        image85 = open('images/85.PNG', 'rb').read()
                        st.image(image85, width=150)
                        url = 'https://www.se.com/in/en/product/TM262M35MESS8T/motion-controller-modicon-m262-3ns-per-instruction-24-axes-ethernet-sercos/'
                        st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        
                with tab18:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Inverter = df_f[df_f['Comments'] == 'Inverter'].sort_values(by='Comments')
                        st.dataframe(Inverter,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Inverter')
                    with col3:
                        st.subheader('image  for  these  part')
                        image86 = open('images/86.PNG', 'rb').read()
                        st.image(image86, width=150)
                        url = 'https://www.se.com/in/en/product-range/7654-conext-xw/#overview'
                        st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        
                with tab19:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:               
                        Relay = df_f[df_f['Comments'] == 'Relay'].sort_values(by='Comments')
                        st.dataframe(Relay,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Relay')
                    with col3:
                        st.subheader('image  for  these  part')
                        relay,solid_relay,PILZ_relay  = st.tabs(['relay','solid relay','PILZ relay'])
                        with relay:
                            image87 = open('images/87.PNG', 'rb').read()
                            st.image(image87, width=150)
                            url = 'https://www.se.com/in/en/product/RPM31F7/power-plugin-relay-15-a-3-co-120-v-ac/'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        with solid_relay:
                            image88= open('images/88.PNG', 'rb').read()
                            st.image(image88, width=150)
                            url = 'https://www.se.com/eg/en/product/SSP3A225BDT/solid-state-relay-panelinput-432vdc-output-48530vac-25athermal-interface/'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        with PILZ_relay:
                            image89 = open('images/89.PNG', 'rb').read()
                            st.image(image89, width=150)
                            url = 'https://www.pilz.com/en-IE/eshop/Small-controllers-PNOZmulti/Safety-systems-PNOZmulti-Classic/PNOZmulti-I-O-modules/PNOZmulti-safe-I-O-modules/c/0010100203701880G2'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        
                with tab20:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Jumper = df_f[df_f['Comments'] == 'Jumper'].sort_values(by='Comments')
                        st.dataframe(Jumper,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Jumper')
                    with col3:
                        st.subheader('image  for  these  part')
                        image91 = open('images/91.PNG', 'rb').read()
                        st.image(image91, width=150)
                        url = 'https://www.wago.com/us/protection-devices/push-in-type-jumper-bar/p/859-408'
                        st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                with tab21:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Panel = df_f[df_f['Comments'] == 'Panel'].sort_values(by='Comments')
                        st.dataframe(Panel,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Panel')
                    with col3:
                        st.subheader('image  for  these  part')
                        GUK,Laetus  = st.tabs(['GUK','Laetus'])
                        with GUK:
                            image93 = open('images/93.PNG', 'rb').read()
                            st.image(image93, width=150)
                            url = 'https://www.guk-vijuk.net/folding-machines/packaging-line-leaflet-folders-feeders/rs-21070-roll-fed-folder.html'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        with Laetus:
                            image92= open('images/92.PNG', 'rb').read()
                            st.image(image92, width=150)
                            url = 'https://permasale.de/GUK-folding-machine-FA-35-2-SVA-VAR'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        
                        
                with tab23:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Thermostate = df_f[df_f['Comments'] == 'Thermostate'].sort_values(by='Comments')
                        st.dataframe(Thermostate,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Thermostate')
                    with col3:
                        st.subheader('image  for  these  part')
                        JUMO, GLATT  = st.tabs(['JUMO','GLATT'])
                        with JUMO:
                            image94 = open('images/94.PNG', 'rb').read()
                            st.image(image94, width=150)
                            url = 'https://www.ebay.co.uk/itm/255381109138'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        with GLATT:
                            image95= open('images/95.PNG', 'rb').read()
                            st.image(image95, width=150)
                            url = 'https://www.directindustry.com/prod/acs-control-system-gmbh/product-37041-2485593.html'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        
                with tab24:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Thermocouple = df_f[df_f['Comments'] == 'Thermocouple'].sort_values(by='Comments')
                        st.dataframe(Thermocouple,width=2000)
                        col16, col2, col31 = st.columns([2,1,2])
                        with col16:
                            display_tab('Thermocouple')
                    with col3:
                        st.subheader('image  for  these  part')
                        image96 = open('images/96.PNG', 'rb').read()
                        st.image(image96, width=150)
                        st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        
        
                st.header('Select from these items')
                tab25 ,tab26, tab27, tab28 ,tab29, tab30, tab31  = st.tabs(['Ups','Power_supply','Electricity',
                'Feedback','Battery','Electronic_board','Electronic_buzzer'])
        
                
        
                with tab25:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Ups = df_f[df_f['Comments'] == 'Ups'].sort_values(by='Comments')
                        st.dataframe(Ups,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Ups')
                    with col3:
                        st.subheader('image  for  these  part')
                        battery_UPS, QUINT_UPS  = st.tabs(['battery UPS','QUINT UPS'])
                        with battery_UPS:
                            image97 = open('images/97.PNG', 'rb').read()
                            st.image(image97, width=150)
                            url = 'https://plc-direct.com/products/2320319'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        with QUINT_UPS:
                            image98= open('images/98.PNG', 'rb').read()
                            st.image(image98, width=150)
                            url = 'https://www.phoenixcontact.com/en-us/products/uninterruptible-power-supply-quint-ups-24dc-24dc20-2320238'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                       
                        
                with tab26:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Power_supply = df_f[df_f['Comments'] == 'Power supply'].sort_values(by='Comments')
                        st.dataframe(Power_supply,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Power_supply')
                    with col3:
                        st.subheader('image  for  these  part')
                        SIEMENS, OMRON  = st.tabs(['SIEMENS','OMRON'])
                        with SIEMENS:
                            image99 = open('images/99.PNG', 'rb').read()
                            st.image(image99, width=150)
                            url = 'https://www.siemens.com/global/en/products/automation/power-supply/special-design.html'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        with OMRON:
                            image100= open('images/100.PNG', 'rb').read()
                            st.image(image100, width=150)
                            url = 'https://www.indiamart.com/proddetail/s8vk-t24024-omron-smps-power-supply-25938847955.html'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        
                with tab27:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Electricity = df_f[df_f['Comments'] == 'Electricity'].sort_values(by='Comments')
                        st.dataframe( Electricity,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Electricity')
                    with col3:
                        st.subheader('image  for  these  part')
                        END_PLATE, INSERT_CRIMP  = st.tabs(['END PLATE','INSERT CRIMP'])
                        with END_PLATE:
                            image101 = open('images/101.PNG', 'rb').read()
                            st.image(image101, width=150)
                            url = 'https://www.wago.com/global/rail-mount-terminal-blocks/end-and-intermediate-plate/p/2000-1392'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        with INSERT_CRIMP:
                            image102= open('images/102.PNG', 'rb').read()
                            st.image(image102, width=150)
                            url = 'https://www.elecbee.com/en-57967-hee-46-pin-female-insert-crimp-terminal'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        
                        
                with tab28:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Feedback = df_f[df_f['Comments'] == 'Feedback'].sort_values(by='Comments')
                        st.dataframe(Feedback,width=2000)
                        col16, col2, col31 = st.columns([2,1,2])
                        with col16:
                            display_tab('Feedback')
                    with col3:
                        st.subheader('image  for  these  part')
                        image103 = open('images/103.PNG', 'rb').read()
                        st.image(image103, width=150)
                        url = 'https://www.kempstoncontrols.co.uk/SRS50-HWA0-K21/Sick/sku/411694'
                        st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
        
                
                with tab29:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Battery = df_f[df_f['Comments'] == 'Battery'].sort_values(by='Comments')
                        st.dataframe( Battery,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Battery')
                    with col3:
                        st.subheader('image  for  these  part')
                        Battery_module,  Battery  = st.tabs(['Battery module',' Battery'])
                        with Battery_module:
                            image104 = open('images/104.PNG', 'rb').read()
                            st.image(image104, width=150)
                            url = 'https://www.electricautomationnetwork.com/en/siemens/6ep4135-0gb00-0ay0-6ep41350gb000ay0-siemens-sitop-ups1100-battery-module-with-service-free-sealed-lead-batter'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        with  Battery:
                            image105= open('images/105.PNG', 'rb').read()
                            st.image(image105, width=150)
                            url = 'https://free-electronic.com/product/ultracell-battery-ul2-2-12-sealed-lead-acid-battery-12v2-2a/'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        
                with tab30:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Electronic_board  = df_f[df_f['Comments'] == 'Electronic board'].sort_values(by='Comments')
                        st.dataframe(Electronic_board ,width=2000)
                        col16, col2, col31 = st.columns([2,1,2])
                        with col16:
                            display_tab('Electronic_board')
                    with col3:
                        st.subheader('image  for  these  part')
                        image106 = open('images/106.PNG', 'rb').read()
                        st.image(image106, width=150)
                        url = 'https://fares-pcb.com/product-category/fares-products/interface-cards-and-modules/'
                        st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        
                with tab31:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Electronic_buzzer  = df_f[df_f['Comments'] == 'Electronic buzzer'].sort_values(by='Comments')
                        st.dataframe(Electronic_buzzer,width=2000 )
                        col16, col2, col31 = st.columns([2,1,2])
                        with col16:
                            display_tab('Electronic_buzzer')
                    with col3:
                        st.subheader('image  for  these  part')
                        image107 = open('images/107.PNG', 'rb').read()
                        st.image(image107, width=150)
                        url = 'https://electroshope.com/product/panel-buzzer-24vdc-cbz-10dc'
                        st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                csv = st.session_state.df.to_csv(index=False)
                st.download_button(label="Download updated CSV", data=csv, file_name='updated_spare_parts.csv', mime='text/csv')
        
            
            if __name__ == '__main__':
        
                main()
    
    
        if page == 'Neumatic parts': 
            def main():
                st.markdown("""
            <style>
                /* Add your custom CSS styles here */
                .stProgress > div > div > div {
                    background-color: #FFD700; /* Change the color of the loading spinner */
                    border-radius: 50%; /* Make the loading spinner circular */
                }
            </style>
        """, unsafe_allow_html=True)
                with st.spinner("Data loaded successfully!"):
                    import time
                    time.sleep(1)
        
                col1, col2 = st.columns([2, 0.75])
                with col1:
                    st.markdown("""
                        <h2 style='text-align: center; font-size: 40px; color: red;'>
                            Find your Neumatic parts
                        </h2>
                    """, unsafe_allow_html=True)
                
                with col2:
                    search_keyword = st.text_input("Enter keyword to search:")
                    search_button = st.button("Search")
                    search_option = 'All Columns'
                def search_in_dataframe(df_f, keyword, option):
                    if option == 'All Columns':
                        result = df_f[df_f.apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)]
                    else:
                        result = df_f[df_f[option].astype(str).str.contains(keyword, case=False)]
                    return result
            
                if search_button and search_keyword:
                    search_results = search_in_dataframe(df_f, search_keyword, search_option)
                    st.write(f"Search results for '{search_keyword}' in {search_option}:")
                    st.dataframe(search_results, width=700, height=200)
                st.subheader('Select from these items')
              
                tab1, tab2 ,tab3, tab4,tab5, tab6 ,tab7  = st.tabs(['Oil seal','Gasket','Gauge','Solenoid valve','Neumatic hose','Cylinder','Regulator'])
        
                with tab1:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Oil_seal = df_f[df_f['Comments'] == 'Oil seal'].sort_values(by='Comments')
                        st.dataframe(Oil_seal,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Oil_seal')
                    with col3:
                        st.subheader('image  for  these  part')
                        O_RING ,OIL_SEAL, MECHANICAL_SEAL = st.tabs(['O RING','OIL SEAL','Mechanical SEAL'])
                        with O_RING:
                            image108 = open('images/108.PNG', 'rb').read()
                            st.image(image108, width=150)
                            url = 'https://shop.gottwald-hydraulik.com/en/sealing-technology/static-seals/o-rings/'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                            
                        with OIL_SEAL:
                            image109 = open('images/109.PNG', 'rb').read()
                            st.image(image109, width=150)
                            url = 'https://shop.gottwald-hydraulik.com/en/sealing-technology/rotary-seals/simmerrings-radial-shaft-seals/'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                            
                        with MECHANICAL_SEAL:
                            image110 = open('images/110.PNG', 'rb').read()
                            st.image(image110, width=150)
                            url = 'https://mechanical-seal.pro/eng/tortsevye-uplotneniya/r-109_r-8u/ushch-lnyuvach-mekhan-chniy-r-8u-11-8-car-sic-viton-304-pg/'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        
                with tab2:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Gasket = df_f[df_f['Comments'] == 'Gasket'].sort_values(by='Comments')
                        st.dataframe(Gasket,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Gasket')
                    with col3:
                        st.subheader('image  for  these  part')
                        Silicone ,Viton, Teflon,Valve_Seat = st.tabs(['Silicone','Viton','Teflon','Valve Seat'])
                        with Silicone:
                            image111 = open('images/111.PNG', 'rb').read()
                            st.image(image111, width=200)
                            url = 'https://www.brewerygaskets.com/1-5-red-silicone-tri-clamp-gasket/'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                            
                        with Viton:
                            image112 = open('images/112.PNG', 'rb').read()
                            st.image(image112, width=200)
                            url = 'https://www.brewerygaskets.com/2-white-viton-tri-clamp-gasket/'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                            
                        with Teflon:
                            image113 = open('images/113.PNG', 'rb').read()
                            st.image(image113, width=200)
                            url = 'https://www.brewerygaskets.com/1-5-white-teflon-100-virgin-ptfe-tri-clamp-gasket/'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                            
                        with Valve_Seat:
                            image114 = open('images/114.PNG', 'rb').read()
                            st.image(image114, width=200)
                            url = 'https://www.brewerygaskets.com/tassalini-butterfly-valve-seat-1-1-2-orange-silicone-oem-style/'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        
                with tab3:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Gauge = df_f[df_f['Comments'] == 'Gauge'].sort_values(by='Comments')
                        st.dataframe(Gauge,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Gauge')
                    with col3:
                        st.subheader('image  for  these  part')
                        Vacuum_Gauge , Differential_pressure = st.tabs(['Vacuum Gauge','Differential pressure'])
                        with Vacuum_Gauge:
                            image115 = open('images/115.PNG', 'rb').read()
                            st.image(image115, width=200)
                            url = 'https://shop.prmfiltration.com/products/30-0-in-hg-vacuum-gauge-35-3'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                            
                        with Differential_pressure:
                            image116 = open('images/116.PNG', 'rb').read()
                            st.image(image116, width=200)
                            url = 'https://shop.prmfiltration.com/collections/differential-pressure-gauges/products/differential-pressure-gauge-0-0-25-inches-of-water'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        
                with tab4:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Solenoid_valve = df_f[df_f['Comments'] == 'Solenoid valve'].sort_values(by='Comments')
                        st.dataframe(Solenoid_valve,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Solenoid_valve')
                    with col3:
                        st.subheader('image  for  these  part')
                        Non_Return_Valve  , PNEUMATIC_VALVE ,Solenoid_Valve = st.tabs(['Non Return Valve ','PNEUMATIC VALVE','Solenoid Valve'])
                        with Non_Return_Valve:
                            image117 = open('images/117.PNG', 'rb').read()
                            st.image(image117, width=150)
                            url = 'https://tameson.com/products/617-12-012-g1-2inch-brass-relief-valve-2-12-bar-29-174-psi'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                            
                        with PNEUMATIC_VALVE:
                            image118 = open('images/118.PNG', 'rb').read()
                            st.image(image118, width=200)
                            url = 'https://www.electricsolenoidvalves.com/1-8-3-way-2-position-pneumatic-solenoid-valve/'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                            
                        with Solenoid_Valve:
                            image119 = open('images/119.PNG', 'rb').read()
                            st.image(image119, width=200)
                            url = 'https://www.electricsolenoidvalves.com/1-2-stainless-steel-steam-solenoid-valve/'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        
                with tab5:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Neumatic_hose = df_f[df_f['Comments'] == 'Neumatic hose'].sort_values(by='Comments')
                        st.dataframe(Neumatic_hose,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Neumatic_hose')
                    with col3:
                        st.subheader('image  for  these  part')
                        PVC_hose  , pneumatic_hose  = st.tabs(['PVC hose ','pneumatic hose'])
                        with PVC_hose:
                            image120 = open('images/120.PNG', 'rb').read()
                            st.image(image120, width=200)
                            url = 'https://www.camthorne.co.uk/product/clear-braided-pvc-hose/'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                            
                        with pneumatic_hose:
                            image121 = open('images/121.PNG', 'rb').read()
                            st.image(image121, width=200)
                            url = 'https://hpcontrol.eu/przewod-waz-pneumatyczny-poliuretanowy-pu-8-5-mm-50mb-niebieski.html'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        
                with tab6:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Cylinder = df_f[df_f['Comments'] == 'Cylinder'].sort_values(by='Comments')
                        st.dataframe(Cylinder,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Cylinder')
                    with col3:
                        st.subheader('image  for  these  part')
                        RODLESS_CYLINDER ,VDMA_CYLINDER, PNEUMATIC_CYLINDER = st.tabs(['RODLESS CYLINDER','VDMA CYLINDER','PNEUMATIC CYLINDER'])
                        with RODLESS_CYLINDER:
                            image122 = open('images/122.PNG', 'rb').read()
                            st.image(image122, width=200)
                            url = 'https://www.disumtec.com/en/pneumatic-cylinders/50170028-rodless-cylinder.html'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                            
                        with VDMA_CYLINDER:
                            image123 = open('images/123.PNG', 'rb').read()
                            st.image(image123, width=200)
                            url = 'https://www.disumtec.com/en/pneumatic-cylinders/50040026-cnomo-pcn-cylinder.html'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                            
                        with PNEUMATIC_CYLINDER:
                            image124 = open('images/124.PNG', 'rb').read()
                            st.image(image124, width=200)
                            url = 'https://www.disumtec.com/en/pneumatic-cylinders/50010004-pneumatic-cylinder-iso-6432.html'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                with tab7:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Regulator = df_f[df_f['Comments'] == 'Regulator'].sort_values(by='Comments')
                        st.dataframe(Regulator,width=900)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Regulator')
                    with col3:
                        st.subheader('image  for  these  part')
                        image125= open('images/125.PNG', 'rb').read()
                        st.image(image125, width=150)
                        url = 'https://www.disumtec.com/en/compressed-air-filter-regulators/32030008-22543-compressed-air-filter-regulator.html?mot_tcid=16c9b4d0-9039-43d1-bbd9-0c536a6fe56e#/thread-1_4'
                        st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                csv = df_f.to_csv(index=False)
                st.download_button(label="Download updated CSV", data=csv, file_name='updated_spare_parts.csv', mime='text/csv')
                
            if __name__ == '__main__':
        
                main()
        
        
        if page == 'FORKLIFT': 
            def main():
                st.markdown("""
            <style>
                /* Add your custom CSS styles here */
                .stProgress > div > div > div {
                    background-color: #FFD700; /* Change the color of the loading spinner */
                    border-radius: 50%; /* Make the loading spinner circular */
                }
            </style>
        """, unsafe_allow_html=True)
                
                with st.spinner("Data loaded successfully!"):
                    import time
                    time.sleep(1)
        
                col1, col2 = st.columns([2, 0.75])         
                with col1:
                    st.markdown("""
                        <h2 style='text-align: center; font-size: 40px; color: red;'>
                            Find your Forklift parts
                        </h2>
                    """, unsafe_allow_html=True)
                
                with col2:
                    search_keyword = st.text_input("Enter keyword to search:")
                    search_button = st.button("Search")
                    search_option = 'All Columns'
                def search_in_dataframe(df_f, keyword, option):
                    if option == 'All Columns':
                        result = df_f[df_f.apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)]
                    else:
                        result = df_f[df_f[option].astype(str).str.contains(keyword, case=False)]
                    return result
                
                if search_button and search_keyword:
                    search_results = search_in_dataframe(df_f, search_keyword, search_option)
                    st.write(f"Search results for '{search_keyword}' in {search_option}:")
                    st.dataframe(search_results, width=700, height=200)
                    
                st.subheader('Select from these items')
              
                tab1, tab2 ,tab3, tab5, tab6 ,tab7  = st.tabs(['Forklift wheel','Forklift switch','Forklift coolant',
                'Forklift control','Forklift carbon','Forklift break'])
        
                with tab1:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Forklift_wheel = df_f[df_f['Comments'] == 'Forklift wheel'].sort_values(by='Comments')
                        st.dataframe(Forklift_wheel,width=900)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Forklift_wheel')
                    with col3:
                        st.subheader('image  for  these  part')
                        image126= open('images/126.PNG', 'rb').read()
                        st.image(image126, width=200)
                        url = 'https://directparts.eu/still/4974-230x70-82-45-drive-wheel-vulkollan-still-4359920-10009.html'
                        st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        
                with tab2:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Forklift_switch = df_f[df_f['Comments'] == 'Forklift switch'].sort_values(by='Comments')
                        st.dataframe(Forklift_switch,width=900)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Forklift_switch')
                    with col3:
                        st.subheader('image  for  these  part')
                        image127= open('images/127.PNG', 'rb').read()
                        st.image(image127, width=200)
                        url = 'https://directparts.eu/linde/5144-microswitch-linde-7915497021-10906.html'
                        st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        
                with tab3:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Forklift_coolant = df_f[df_f['Comments'] == 'Forklift coolant'].sort_values(by='Comments')
                        st.dataframe(Forklift_coolant,width=900)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Forklift_coolant')
                    with col3:
                        st.subheader('image  for  these  part')
                        image128= open('images/128.PNG', 'rb').read()
                        st.image(image128, width=200)
                        url = 'https://www.gsistore.com/products/york-013-03344-000-glycol-coolant'
                        st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        
                with tab5:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Forklift_control = df_f[df_f['Comments'] == 'Forklift control'].sort_values(by='Comments')
                        st.dataframe(Forklift_control,width=900)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Forklift_control')
                    with col3:
                        st.subheader('image  for  these  part')
                        image129= open('images/129.PNG', 'rb').read()
                        st.image(image129, width=200)
                        url = 'https://directparts.eu/still/5482-contactor-iskra-12088.html'
                        st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        
                with tab6:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Forklift_carbon = df_f[df_f['Comments'] == 'Forklift carbon'].sort_values(by='Comments')
                        st.dataframe(Forklift_carbon,width=900)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Forklift_carbon')
                    with col3:
                        st.subheader('image  for  these  part')
                        image130= open('images/130.PNG', 'rb').read()
                        st.image(image130, width=200)
                        url = 'https://directparts.eu/linde/5096-carbon-brush-4457096-10663.html'
                        st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        
                with tab7:
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Forklift_break = df_f[df_f['Comments'] == 'Forklift break'].sort_values(by='Comments')
                        st.dataframe(Forklift_break,width=900)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Forklift_break')
                    with col3:
                        st.subheader('image  for  these  part')
                        image131= open('images/131.PNG', 'rb').read()
                        st.image(image131, width=200)
                        url = 'https://directparts.eu/linde/5122-brake-shoe-108116.html'
                        st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                csv = df_f.to_csv(index=False)
                st.download_button(label="Download updated CSV", data=csv, file_name='updated_spare_parts.csv', mime='text/csv')
            if __name__ == '__main__':
        
                main()
        
        
        if page == 'Utility area':
            
            def main():
                
                st.markdown("""
            <style>
                /* Add your custom CSS styles here */
                .stProgress > div > div > div {
                    background-color: #FFD700; /* Change the color of the loading spinner */
                    border-radius: 50%; /* Make the loading spinner circular */
                }
            </style>
        """, unsafe_allow_html=True)
                
                with st.spinner("Data loaded successfully!"):
                    import time
                    time.sleep(1)
        
                col1, col2 = st.columns([2, 0.75])
                with col1:
                    st.markdown("""
                        <h2 style='text-align: center; font-size: 40px; color: red;'>
                            Find your Utility parts
                        </h2>
                    """, unsafe_allow_html=True)
                
                with col2:
                    search_keyword = st.text_input("Enter keyword to search:")
                    search_button = st.button("Search")
                    search_option = 'All Columns'
                def search_in_dataframe(df_f, keyword, option):
                    if option == 'All Columns':
                        result = df_f[df_f.apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)]
                    else:
                        result = df_f[df_f[option].astype(str).str.contains(keyword, case=False)]
                    return result
                    
                if search_button and search_keyword:
                    search_results = search_in_dataframe(df_f, search_keyword, search_option)
                    st.write(f"Search results for '{search_keyword}' in {search_option}:")
                    st.dataframe(search_results, width=700, height=200)
              
                col1, col2, col3 = st.columns([1,2,2])
                with col1:
                    select_col = st.selectbox('Select page:', ['Water Station','Fire Fighting','Filters', 'AHU'], key='select_page')
            
                    st.markdown("""
                        <style>
                        .stSelectbox label {
                            font-size: 20px; 
                            color: blue; 
                        }
                        </style>
                    """, unsafe_allow_html=True)
                    st.subheader('Select from these items')
                            
                if select_col == 'Water Station':    
                    tab1, tab2 ,tab3, tab4,tab5, tab6 ,tab8, tab9 ,tab10, tab12,tab13 = st.tabs(['Conductivity transmitter','Flowmeter controller','Flow module',
                        'Flow monitor','conductivity','Stilmas sensor','Valve','test','pump','Uv','Ro'])
                    
                    with tab1:
                        col1, col2, col3 = st.columns([30,3,13])
                        with col1:
                            Conductivity_transmitter = df_f[df_f['Comments'] == 'Conductivity transmitter'].sort_values(by='Comments')
                            st.dataframe(Conductivity_transmitter,width=2000)
                            col4, col5, col6 = st.columns([2,1,2])
                            with col4:
                                display_tab('Conductivity_transmitter')
                        with col3:
                            st.subheader('image  for  these  part')
                            image33 = open('images/33.jpg', 'rb').read()
                            st.image(image33, width=100)
                            url = 'https://www.endress.com/en/field-instruments-overview/liquid-analysis-product-overview/conductivity-transmitter-clm223?t.tabId=product-overview'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                            
                          
                    with tab2:
                        col1, col2, col3 = st.columns([30,3,13])
                        with col1:
                            Flowmeter_controller = df_f[df_f['Comments'] == 'Flowmeter controller'].sort_values(by='Comments')
                            st.dataframe(Flowmeter_controller,width=2000)
                            col4, col5, col6 = st.columns([2,1,2])
                            with col4:
                                display_tab('Flowmeter_controller')
                        with col3:
                            st.subheader('image  for  these  part')
                            image34= open('images/34.PNG', 'rb').read()
                            st.image(image34, width=150)
                            url = 'https://www.burkert.com/en/type/8035'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                            
                        
                    with tab3:
                        col1, col2, col3 = st.columns([30,3,13])
                        with col1:
                            Flow_module = df_f[df_f['Comments'] == 'Flow module'].sort_values(by='Comments')
                            st.dataframe(Flow_module,width=2000)
                            col4, col5, col6 = st.columns([2,1,2])
                            with col4:
                                display_tab('Flow_module')
                        with col3:
                            st.subheader('image  for  these  part')
                            image35= open('images/35.PNG', 'rb').read()
                            st.image(image35, width=150)
                            url = 'https://www.burkert.com/en/type/SE32'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                            
                        
                    with tab4:
                        col1, col2, col3 = st.columns([30,3,13])
                        with col1:
                            Flow_monitor = df_f[df_f['Comments'] == 'Flow monitor sensor'].sort_values(by='Comments')
                            st.dataframe(Flow_monitor,width=2000)
                            col4, col5, col6 = st.columns([2,1,2])
                            with col4:
                                display_tab('Flow_monitor')
                        with col3:
                            st.subheader('image  for  these  part')
                            image36= open('images/36.PNG', 'rb').read()
                            st.image(image36, width=150)
                            url = 'https://www.ifm.com/de/en/product/SI1000'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                            
                        
                    with tab5:
                        col1, col2, col3 = st.columns([30,3,13])
                        with col1:
                            conductivity = df_f[df_f['Comments'] == 'Water conductivity'].sort_values(by='Comments')
                            st.dataframe(conductivity,width=2000)
                            col4, col5, col6 = st.columns([2,1,2])
                            with col4:
                                display_tab('conductivity')
                        with col3:
                            st.subheader('image  for  these  part')
                            image37= open('images/37.PNG', 'rb').read()
                            st.image(image37, width=150)
                            url = 'https://www.directindustry.com/prod/emerson-automation-solutions-rosemount/product-36718-949557.html'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                            
                        
                    with tab6:
                        col1, col2, col3 = st.columns([30,3,13])
                        with col1:
                            STILMAS_SENSOR = df_f[df_f['Comments'] == 'Stilmas sensor'].sort_values(by='Comments')
                            st.dataframe(STILMAS_SENSOR,width=2000)
                            col4, col5, col6 = st.columns([2,1,2])
                            with col4:
                                display_tab('STILMAS_SENSOR')
                        with col3:
                            st.subheader('image  for  these  part')
                            image38= open('images/38.PNG', 'rb').read()
                            st.image(image38, width=150)
                            url = 'https://www.ifm.com/my/en/product/TR7432'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                            
                        
                    with tab8:
                        col1, col2, col3 = st.columns([30,3,13])
                        with col1:
                            Valve = df_f[df_f['Comments'] == 'Water valve'].sort_values(by='Comments')
                            st.dataframe(Valve,width=2000)
                            col4, col5, col6 = st.columns([2,1,2])
                            with col4:
                                display_tab('Valve')
                        with col3:
                            st.subheader('image  for  these  part')
                            pressure_transmitter, Angle_Valve   = st.tabs(['pressure_transmitter','Angle_Valve '])
                            with pressure_transmitter:
                                image39 = open('images/39.PNG', 'rb').read()
                                st.image(image39, width=150)
                                url = 'https://www.endress.com/en/field-instruments-overview/pressure/pressure-transmitter-cerabar-pmp71b?t.tabId=product-overview'
                                st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                            with Angle_Valve :
                                image40 = open('images/40.PNG', 'rb').read()
                                st.image(image40, width=150)
                                url = 'https://tameson.co.uk/products/al2a-spp-100-b-16-g1inch-ptfe-16bar-nc-angle-seat-valve-stainless-steel-brass'
                                st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        
                    with tab9:
                        col1, col2, col3 = st.columns([30,3,13])
                        with col1:
                            test = df_f[df_f['Comments'] == 'Water test '].sort_values(by='Comments')
                            st.dataframe(test,width=2000)
                            col4, col5, col6 = st.columns([2,1,2])
                            with col4:
                                display_tab('test')
                        with col3:
                            st.subheader('image  for  these  part')
                            PHOTOMETERS, Colorimetric = st.tabs(['PHOTOMETERS','Colorimetric'])
                            with PHOTOMETERS:
                                image42 = open('images/42.PNG', 'rb').read()
                                st.image(image42, width=150)
                                url = 'https://www.hannaservice.eu/water/environmental/photometers'
                                st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                            with Colorimetric:
                                image41 = open('images/41.PNG', 'rb').read()
                                st.image(image41, width=150)
                                url = 'https://www.hannaservice.eu/total-hardness-colorimetric-reagents-hi93735-0-product'
                                st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                                
                        
                    with tab10:
                        col1, col2, col3 = st.columns([30,3,13])
                        with col1:
                            pump = df_f[df_f['Comments'] == 'Water pump'].sort_values(by='Comments')
                            st.dataframe(pump,width=2000)
                            col4, col5, col6 = st.columns([2,1,2])
                            with col4:
                                display_tab('pump')
                        with col3:
                            st.subheader('image  for  these  part')
                            LOBE_PUMP,WHEEL_PUMP = st.tabs(['LOBE PUMP','WHEEL PUMP'])
                            with LOBE_PUMP:
                                image43 = open('images/43.jpg', 'rb').read()
                                st.image(image43, width=150)
                                url = 'https://www.chinastainlesssteelpump.com/Stainless-Steel-rotary-lobe-Pumps/Rotary-Lobe-Pumps-for-Chocolate.html'
                                st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                            with WHEEL_PUMP:
                                image44 = open('images/44.jpg', 'rb').read()
                                st.image(image44, width=150)
                                url = 'https://www.flowpumps.de/product-page/peripheral-pump-pe50brt'
                                st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
        
                    with tab12:
                        col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Uv = df_f[df_f['Comments'] == 'Water uv'].sort_values(by='Comments')
                        st.dataframe(Uv,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Uv')
                    with col3:
                        st.subheader('image  for  these  part')
                        image45 = open('images/45.jpeg', 'rb').read()
                        st.image(image45, width=150)
                        url = 'https://pureaqua.com/viqua-sterilight-uv/'
                        st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        
                        
                    with tab13:
                        col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        Ro = df_f[df_f['Comments'] == 'Water ro'].sort_values(by='Comments')
                        st.dataframe(Ro,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('Ro')
                    with col3:
                        st.subheader('image  for  these  part')
                        image46 = open('images/46.jpeg', 'rb').read()
                        st.image(image46, width=150)
                        url = 'https://www.hongtekfiltration.com/RO-membrane-elements/XLP-Series-RO-membrane-elements.html'
                        st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        
                        
                        
                elif select_col == 'Fire Fighting':
                    
                    Fire_detector, Fire_valve = st.tabs(['Fire_detector','Fire_valve'])
                    with Fire_detector:
                        col1, col2, col3 = st.columns([30,3,13])
                        with col1:
                            Fire_detector = df_f[df_f['Comments'] == 'Fire detector'].sort_values(by='Comments')
                            st.dataframe(Fire_detector,width=2000)
                            col4, col5, col6 = st.columns([2,1,2])
                            with col4:
                                display_tab('Fire_detector')
                        with col3:
                            st.subheader('image  for  these  part')
                            image47 = open('images/47.PNG', 'rb').read()
                            st.image(image47, width=150)
                            url = 'https://www.royal.ps/en/sanitary-ware/products/fire-fighting-system/water-flow-detector'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        
        
                    with Fire_valve:
                        col1, col2, col3 = st.columns([30,3,13])
                        with col1:
                            Fire_valve = df_f[df_f['Comments'] == 'Fire valve'].sort_values(by='Comments')
                            st.dataframe(Fire_valve,width=2000)
                            col4, col5, col6 = st.columns([2,1,2])
                            with col4:
                                display_tab('Fire_valve')
                        with col3:
                            st.subheader('image  for  these  part')
                            image48 = open('images/48.PNG', 'rb').read()
                            st.image(image48, width=150)
                            url = 'https://www.giacomini.com/product/A56'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                        
        
                elif select_col == 'AHU':
                    col1, col2, col3 = st.columns([30,3,13])
                    with col1:
                        AHU_Valve = df_f[df_f['Comments'] == 'Valve ahu'].sort_values(by='Comments')
                        st.dataframe(AHU_Valve,width=2000)
                        col4, col5, col6 = st.columns([2,1,2])
                        with col4:
                            display_tab('AHU_Valve')
                    with col3:
                        st.subheader('image  for  these  part')
                        image49 = open('images/49.PNG', 'rb').read()
                        st.image(image49, width=150)
                        url = 'https://www.indiamart.com/proddetail/butterfly-valve-22160377997.html'
                        st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
        
                elif select_col == 'Filters':
        
                    tab1, tab2 ,tab3, tab4, tab5, tab6 ,tab7  = st.tabs(['Hepa filter','High filter','Pre filter','Pack filter','Pump filter','Emflon filter','Filters cartage'])
        
                    with tab1:
                        col1, col2, col3 = st.columns([30,3,13])
                        with col1:
                            Hepa_filter = df_f[df_f['Comments'] == 'Hepa filter'].sort_values(by='Comments')
                            st.dataframe(Hepa_filter,width=2000)
                            col4, col5, col6 = st.columns([2,1,2])
                            with col4:
                                display_tab('Hepa_filter')
                        with col3:
                            st.subheader('image  for  these  part')
                            image50 = open('images/50.PNG', 'rb').read()
                            st.image(image50, width=150)
                            url = 'https://www.indiamart.com/proddetail/hepa-filters-13677374133.html'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
        
                        
                    with tab2:
                        col1, col2, col3 = st.columns([30,3,13])
                        with col1:
                            High_filter = df_f[df_f['Comments'] == 'High filter'].sort_values(by='Comments')
                            st.dataframe(High_filter,width=2000)
                            col4, col5, col6 = st.columns([2,1,2])
                            with col4:
                                display_tab('High_filter')
                        with col3:
                            st.subheader('image  for  these  part')
                            image51 = open('images/51.PNG', 'rb').read()
                            st.image(image51, width=150)
                            url = 'https://www.indiamart.com/proddetail/hepa-filters-13677374133.html'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
        
                        
                    with tab3:
                        col1, col2, col3 = st.columns([30,3,13])
                        with col1:
                            Pre_filter = df_f[df_f['Comments'] == 'Pre-filter'].sort_values(by='Comments')
                            st.dataframe(Pre_filter,width=2000)
                            col4, col5, col6 = st.columns([2,1,2])
                            with col4:
                                display_tab('Pre_filter')
                        with col3:
                            st.subheader('image  for  these  part')
                            image52 = open('images/52.PNG', 'rb').read()
                            st.image(image52, width=150)
                            url = 'https://dir.indiamart.com/pune/pre-filter.html?enqformpdp=1'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
        
                        
                    with tab4:
                        col1, col2, col3 = st.columns([30,3,13])
                        with col1:
                            Packfilter = df_f[df_f['Comments'] == 'Packfilter'].sort_values(by='Comments')
                            st.dataframe(Packfilter,width=2000)
                            col4, col5, col6 = st.columns([2,1,2])
                            with col4:
                                display_tab('Pack_filter')
                        with col3:
                            st.subheader('image  for  these  part')
                            image53 = open('images/53.PNG', 'rb').read()
                            st.image(image53, width=150)
                            url = 'https://hepafiltersales.com/products/80085-01499-19-7-8x21-1-2x1-air-filter-12-pack'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
        
                        
                    with tab5:
                        col1, col2, col3 = st.columns([30,3,13])
                        with col1:
                            Pump_filter = df_f[df_f['Comments'] == 'Pump filter'].sort_values(by='Comments')
                            st.dataframe(Pump_filter,width=2000)
                            col4, col5, col6 = st.columns([2,1,2])
                            with col4:
                                display_tab('Pump_filter')
                        with col3:
                            st.subheader('image  for  these  part')
                            image55 = open('images/55.PNG', 'rb').read()
                            st.image(image55, width=150)
                            url = 'https://www.buschvacuum.com/in/en/products/spare-parts-and-accessories/spare-parts/inlet-filters/'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
        
                        
                    with tab6:
                        col1, col2, col3 = st.columns([30,3,13])
                        with col1:
                            Emflon_filter = df_f[df_f['Comments'] == 'Emflon filter'].sort_values(by='Comments')
                            st.dataframe(Emflon_filter,width=2000)
                            col4, col5, col6 = st.columns([2,1,2])
                            with col4:
                                display_tab('Emflon_filter')
                        with col3:
                            st.subheader('image  for  these  part')
                            image54 = open('images/54.PNG', 'rb').read()
                            st.image(image54, width=150)
                            url = 'https://shop.pall.com/us/en/food-beverage/cannabis/zidMCY2230PFRWH4?CategoryName=filter-cartridges&CatalogID=products'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
        
                        
                    with tab7:
                        col1, col2, col3 = st.columns([30,3,13])
                        with col1:
                            Filters_cartage = df_f[df_f['Comments'] == 'Filters cartage'].sort_values(by='Comments')
                            st.dataframe(Filters_cartage,width=2000)
                            col4, col5, col6 = st.columns([2,1,2])
                            with col4:
                                display_tab('Filters_cartage')
                        with col3:
                            st.subheader('image  for  these  part')
                            image56 = open('images/56.PNG', 'rb').read()
                            st.image(image56, width=150)
                            url = 'https://shop.pall.com/us/en/food-beverage/zidimmfdh4o'
                            st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                csv = df_f.to_csv(index=False)
                st.download_button(label="Download updated CSV", data=csv, file_name='updated_spare_parts.csv', mime='text/csv')   
                            
                          
                    
            if __name__ == '__main__':
        
                main()
        
        
        if page == 'LOTOTO':
            
            def main():
                st.markdown("""
            <style>
                /* Add your custom CSS styles here */
                .stProgress > div > div > div {
                    background-color: #FFD700; /* Change the color of the loading spinner */
                    border-radius: 50%; /* Make the loading spinner circular */
                }
            </style>
        """, unsafe_allow_html=True)
                with st.spinner("Data loaded successfully!"):
                    import time
                    time.sleep(1)
                    
                col1, col2 = st.columns([2, 0.5])
                with col1:
                    st.markdown("""
                        <h2 style='text-align: center; font-size: 40px; color: red;'>
                            Find your LOTOTO parts
                        </h2>
                    """, unsafe_allow_html=True)
                    
                with col2:
                    search_keyword = st.text_input("Enter keyword to search:")
                    search_button = st.button("Search")
                    search_option = 'All Columns'
                def search_in_dataframe(df_f, keyword, option):
                    if option == 'All Columns':
                        result = df_f[df_f.apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)]
                    else:
                        result = df_f[df_f[option].astype(str).str.contains(keyword, case=False)]
                    return result
                    
                if search_button and search_keyword:
                    search_results = search_in_dataframe(df_f, search_keyword, search_option)
                    st.write(f"Search results for '{search_keyword}' in {search_option}:")
                    st.dataframe(search_results, width=700, height=200)
        
                col1, col2, col3 = st.columns([30,3,13])
                with col1:
                    LOTOTO = df_f[df_f['Comments'] == 'Lototo'].sort_values(by='Comments')
                    st.dataframe(LOTOTO,width=1000)
                    col4, col5, col6 = st.columns([2,1,2])
                    with col4:
                        display_tab('LOTOTO')
                with col3:
                    st.subheader('image  for  these  part')
                    BOX ,GROUP_LOCK   = st.tabs(['BOX','GROUP LOCK'])
                    with BOX:
                        image132 = open('images/132.PNG', 'rb').read()
                        st.image(image132, width=200)
                        url = 'https://www.lockeylock.com/13-locks-portable-metal-group-lock-box-lk02-2-product/'
                        st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                    with GROUP_LOCK:
                        image133= open('images/133.PNG', 'rb').read()
                        st.image(image133, width=200)
                        url = 'https://www.lockeylock.com/factory-directly-loto-tools-combined-safety-lockout-tagout-station-kit-lg12-lockey-product/'
                        st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                csv = df_f.to_csv(index=False)
                st.download_button(label="Download updated CSV", data=csv, file_name='updated_spare_parts.csv', mime='text/csv')        
          
        
            if __name__ == '__main__':
        
                main()
        
        if page == 'Add New Item & delete':
        
            try:
                df_f = pd.read_csv('Eng Spare parts.csv')
            except FileNotFoundError:
                df_f = pd.DataFrame(columns=['Item description', 'Qty.','Part #','Manufacturer','Location','Comments'])
            
            # Function to add new item
            def add_new_item(item_description, quantity, Part, Manufacturer, Location, Comments):
                global df_f  # Define df_f as global variable
                new_row = {'Item description': item_description, 'Qty.': quantity, 'Part #': Part, 'Manufacturer': Manufacturer, 'Location': Location, 'Comments': Comments}
                df_f = df_f.append(new_row, ignore_index=True)
                df_f.to_csv('Eng Spare parts.csv', index=False)
                st.success(f"New item '{item_description}' added successfully with quantity {quantity}!")
                
            def delete_item(row_index):
                global df_f
                item_description = df_f.loc[row_index, 'Item description']
                df_f = df_f.drop(index=row_index).reset_index(drop=True)
                df_f.to_csv('Eng Spare parts.csv', index=False)
                st.warning(f"Item '{item_description}' at row {row_index} deleted successfully!")
            
            # Streamlit app
            def main():
                global df_f
                col1, col2, col3 = st.columns([1, 3, 1])
                with col2:  # Define df_f as global variable
                    st.title('Add New Item')
                
                    # User inputs
                    item_description = st.text_input('Enter item description:')
                    quantity = st.number_input('Enter quantity:', min_value=0, step=1)
                    Part = st.text_input('Enter Part NO:')
                    Manufacturer = st.text_input('Enter item Manufacturer:')
                    Location = st.text_input('Enter item Location:')
                    Comments = st.text_input('Enter item Comments:')
    
                    # Button to add new item
                    if st.button('Add Item'):
                        if not item_description or not Part or not Manufacturer or not Location or not Comments:
                            st.error("Please fill in all the fields.")
                        else:
                            add_new_item(item_description, quantity, Part, Manufacturer, Location, Comments)
                            st.write('## Updated Items')
                            st.dataframe(df_f)
                    
                    st.write('## Delete Item')
                    row_index = st.number_input('Enter row number to delete:', max_value=len(df_f)-1, step=1)
                    
                    # Button to delete item
                    if st.button('Delete Item', key='delete_item'):
                        delete_item(row_index)
                        st.write('## Updated Items')
                        st.dataframe(df_f)
            
            if __name__ == '__main__':
                
                main()
    
        elif page == 'View Logs':
            def main():
                st.header('User Activity Logs')
                if st.session_state.logs:
                    logs_df = pd.DataFrame(st.session_state.logs)
                    st.dataframe(logs_df)
                    
                    if st.button('Clear Logs'):
                        st.session_state.logs = []
                        try:
                            os.remove('logs.csv')
                        except FileNotFoundError:
                            pass
                        st.success("Logs cleared successfully!")
                else:
                    st.write("No logs available.")
    
            if __name__ == '__main__':
                
                main()
     




    
 


        
