import streamlit as st
import pandas as pd
import numpy as np
import os
import requests

st.set_page_config(
    layout="wide",
    page_title='Earthquake analysis',
    page_icon='🪙'
)



df_f = pd.read_csv('Eng Spare parts.csv')
csv_path = 'Eng Spare parts.csv'
page =  st.sidebar.radio('Select page', ['Utility area','Mechanical parts', 'Electrical parts',
                    'Pneumatic parts','GLATT','FETTE','FORKLIFT','LOTOTO'])
if 'df' not in st.session_state:
            st.session_state.df = pd.read_csv('Eng Spare parts.csv')
df_f = st.session_state.df
def update_quantity(row_index, quantity, operation):
    if operation == 'add':
        df_f.loc[row_index, 'Qty.'] += quantity
    elif operation == 'subtract':
        df_f.loc[row_index, 'Qty.'] -= quantity
    df_f.to_csv('data.csv', index=False)
    st.success(f"Quantity updated successfully! New Quantity: {df_f.loc[row_index, 'Qty.']}")
    st.session_state.update_button_clicked = True

def display_tab(tab_name):
    st.header(f'{tab_name} Tab')

    # تنسيق Select row number
    st.markdown("""
        <style>
        .custom-input label {
            font-size: 20px; 
            color: blue; 
        }
        .custom-input input {
            font-size: 18px;
            color: black;
            width: 10px; /* عرض مربع الإدخال */
        }
        </style>
        """, unsafe_allow_html=True)
    row_number = st.number_input(f'Select row number for {tab_name}:', min_value=0, max_value=len(df_f)-1, step=1, key=f'{tab_name}_row_number')

    # تنسيق الكتابة
    st.markdown(f"""
        <div style='font-size: 20px; color: green;'>Selected Item: {df_f.loc[row_number, 'Item description']}</div>
        <div style='font-size: 20px; color: green;'>Current Quantity: {df_f.loc[row_number, 'Qty.']}</div>
        """, unsafe_allow_html=True)
    
    # تنسيق Enter quantity
    st.markdown("""
        <style>
        .custom-quantity-input label {
            font-size: 20px; 
            color: red; 
        }
        .custom-quantity-input input {
            font-size: 18px;
            color: black;
            width: 10px; /* عرض مربع الإدخال */
        }
        </style>
        """, unsafe_allow_html=True)
    quantity = st.number_input(f'Enter quantity for {tab_name}:', min_value=0, step=1, key=f'{tab_name}_quantity')

    operation = st.radio(f'Choose operation for {tab_name}:', ('add', 'subtract'), key=f'{tab_name}_operation')

    if st.button(f'Update Quantity for {tab_name}', key=f'{tab_name}_update_button'):
        update_quantity(row_number, quantity, operation)
    csv = df_f.to_csv(index=False)



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

# Display a placeholder while loading data
        with st.spinner("Data loaded successfully!"):
            # Simulate loading data
            import time
            time.sleep(1)

        # Once data is loaded, display a message
        st.markdown("""
    <h2 style='text-align: center; font-size: 40px; color: red;'>
        Find your Mechanical parts
    </h2>
""", unsafe_allow_html=True)
        st.subheader('Select from these items')

        tab1, tab2 ,tab3, tab4,tab5, tab6 ,tab7, tab8 ,tab10, tab11 ,tab12, tab13, tab14  = st.tabs(['Bearing', 'Belts','Shaft','Spring',
        'leaflet rooler','Cam','Clutch','Oil _ grease','Chain','Gearbox','Door','Couplin','Wheel CASTOR'])


        with tab1:
            col1, col2, col3 = st.columns([30,3,13])
            with col1:
                peraing = df_f[df_f['Comments'] == 'Bearing'].sort_values(by='Comments')
                st.dataframe(peraing,width=2000)
                

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

        st.subheader('Inventory Management')
        col1, col2, col3 = st.columns([1,2,2])
        with col1:
                # عرض الداتا فري  
            row_number = st.number_input('Select row number:', min_value=0, max_value=len(df_f)-1, step=1)

    # عرض المعلومات عن الصف المختار
        
            
            item_style = """
    <style>
    .item-text {
        color: #FF5733;
        font-size: 24px;
    }
    .quantity-text {
        color: #33C3FF;
        font-size: 24px;
    }
    .custom-label {
    color: #000000;
    font-size: 20px;
    
}
    </style>
    """
    
    # Inject the custom CSS
            st.markdown(item_style, unsafe_allow_html=True)
        
        # Display the selected item and current quantity with custom styles
            st.markdown(f"<p class='item-text'>Selected Item: {df_f.loc[row_number, 'Item description']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='quantity-text'>Current Quantity: {df_f.loc[row_number, 'Qty.']}</p>", unsafe_allow_html=True)
        
                # Custom label for the number input
            st.markdown("<p class='custom-label'>Enter quantity to deduct:</p>", unsafe_allow_html=True)
                
                # Number input for deducting quantity
            deduct_quantity = st.number_input('', min_value=0, max_value=int(df_f.loc[row_number, 'Qty.']), step=1)

        # زر لتحديث الكمية
        if 'update_button_clicked' not in st.session_state:
            st.session_state.update_button_clicked = False
    
    # زر لتحديث الكمية
        if st.button('Update Quantity'):
            if not st.session_state.update_button_clicked:
    # خصم الكمية المحددة
                df_f.loc[row_number, 'Qty.'] -= deduct_quantity
                st.success(f'{deduct_quantity} units deducted from {df_f.loc[row_number, "Item description"]}.')
                
                # تحديث البيانات في ملف CSV
                df_f.to_csv(csv_path, index=False)
                
                # تحديد حالة الزر على أنه تم الضغط عليه
                st.session_state.update_button_clicked = True
                
                # إعادة تحميل البيانات من ملف CSV لتحديث العرض
                st.experimental_rerun()
    
    # إعادة تعيين حالة الزر عند إعادة تحميل الصفحة
       
        csv = df_f.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name='updated_inventory.csv',
            mime='text/csv',
        )
        with tab2:
            col1, col2, col3 = st.columns([30,3,13])
            with col1:
                Belts = df_f[df_f['Comments'] == 'Belts'].sort_values(by='Comments')
                st.dataframe(Belts,width=2000)
                    
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
                st.dataframe(Shaft)
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
                st.dataframe(Spring)
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
                st.dataframe(leaflet_rooler)
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
                st.dataframe(Cam)
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
                st.dataframe(Clutch)
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
                st.dataframe(Oil_grease)
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
                st.dataframe(Chain)
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
                st.dataframe(Gearbox)
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
                st.dataframe(Door)
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
                st.dataframe(Couplin)
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
                st.dataframe(Wheel_CASTOR)
            with col3:
                st.subheader('image  for  these  part')
                image32 = open('images/32.jpg', 'rb').read()
                st.image(image32, width=150)
                url = 'https://www.shoplinco.com/colson-polyurethane-heavy-duty-total-lock-swivel-caster-8-x-2-1000-lbs-cap/'
                st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
            

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

# Display a placeholder while loading data
        with st.spinner("Data loaded successfully!"):
            # Simulate loading data
            import time
            time.sleep(1)

            st.markdown("""
    <h2 style='text-align: center; font-size: 40px; color: red;'>
        Find your Electrical parts
    </h2>
""", unsafe_allow_html=True)
        st.subheader('Select from these items')
        
            
        
        tab1, tab2 ,tab3, tab4,tab5, tab6 ,tab7, tab8, tab9 ,tab10, tab11 ,tab12  = st.tabs(['Proximity','Sensor','Fiber sensor','Amplifier','Socket',
        'Selector','Button','Switch','Light','Fan','Cable','Fuse'])
        
        

        with tab1:
            col1, col2, col3 = st.columns([30,3,13])
            with col1:
                
                Proximity = df_f[df_f['Comments'] == 'Proximity'].sort_values(by='Comments')
                st.dataframe(Proximity)
                col4, col5, col6 = st.columns([3,1,2])
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
                st.dataframe(Sensor)
                col4, col5, col6 = st.columns([3,1,2])
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
                st.dataframe(Fiber_sensor)
                col4, col5, col6 = st.columns([3,1,2])
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
                st.dataframe(Amplifier)
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
                st.dataframe(Socket)
                col4, col5, col6 = st.columns([3,1,2])
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
                st.dataframe(Selector)
                col4, col5, col6 = st.columns([3,1,2])
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
                st.dataframe(Button)
                col4, col5, col6 = st.columns([3,1,2])
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
                st.dataframe(Switch)
                col4, col5, col6 = st.columns([3,1,2])
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
                st.dataframe(Light)
                col4, col5, col6 = st.columns([3,1,2])
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
                st.dataframe(Fan)
                col4, col5, col6 = st.columns([3,1,2])
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
                st.dataframe(Cable)
                col4, col5, col6 = st.columns([3,1,2])
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
                st.dataframe(Fuse)
                col4, col5, col6 = st.columns([3,1,2])
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
        
        tab13, tab14 ,tab15, tab16,tab17, tab18 ,tab19, tab20, tab21 ,tab22, tab23 ,tab24  = st.tabs(['Converter','Control','Conductor','Contactor','Controller',
        'Inverter','Relay','Jumper','Panel','Heater','Thermostate','Thermocouple'])

        with tab13:
            col1, col2, col3 = st.columns([30,3,13])
            with col1:
                Converter = df_f[df_f['Comments'] == 'Converter'].sort_values(by='Comments')
                st.dataframe(Converter)
                col16, col2, col31 = st.columns([3,.5,3])
                with col16:
                    display_tab('Converter')
            with col3:
                st.subheader('image  for  these  part')

                GLASS,CRAMIC  = st.tabs(['GLASS','CRAMIC'])
                with GLASS:
                    image77 = open('images/77.PNG', 'rb').read()
                    st.image(image77, width=150)
                    url = 'https://makerselectronics.com/product/fuse-1a-250v-t5x20mm'
                    st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
        with tab14:
            Control = df_f[df_f['Comments'] == 'Control'].sort_values(by='Comments')
            st.dataframe(Sensor)
            col4, col5, col6 = st.columns([3,1,2])
            with col4:
                display_tab('Control')
        with tab15:
            Conductor = df_f[df_f['Comments'] == 'Conductor'].sort_values(by='Comments')
            st.dataframe(Conductor)
            col4, col5, col6 = st.columns([3,1,2])
            with col4:
                display_tab('Conductor')
        with tab16:
            Contactor = df_f[df_f['Comments'] == 'Contactor'].sort_values(by='Comments')
            st.dataframe(Contactor)
            col4, col5, col6 = st.columns([3,1,2])
            with col4:
                display_tab('Contactor')
        with tab17:
            Controller = df_f[df_f['Comments'] == 'Controller'].sort_values(by='Comments')
            st.dataframe(Controller)
            col4, col5, col6 = st.columns([3,1,2])
            with col4:
                display_tab('Controller')
        with tab18:
            Inverter = df_f[df_f['Comments'] == 'Inverter'].sort_values(by='Comments')
            st.dataframe(Inverter)
            col4, col5, col6 = st.columns([3,1,2])
            with col4:
                display_tab('Inverter')
        with tab19:
            Relay = df_f[df_f['Comments'] == 'Relay'].sort_values(by='Comments')
            st.dataframe(Relay)
            col4, col5, col6 = st.columns([3,1,2])
            with col4:
                display_tab('Relay')
        with tab20:
            Jumper = df_f[df_f['Comments'] == 'Jumper'].sort_values(by='Comments')
            st.dataframe(Jumper)
            col4, col5, col6 = st.columns([3,1,2])
            with col4:
                display_tab('Jumper')
        with tab21:
            Panel = df_f[df_f['Comments'] == 'Panel'].sort_values(by='Comments')
            st.dataframe(Panel)
            col4, col5, col6 = st.columns([3,1,2])
            with col4:
                display_tab('Panel')
        with tab22:
            Heater = df_f[df_f['Comments'] == 'Heater'].sort_values(by='Comments')
            st.dataframe(Heater)
        with tab23:
            Thermostate = df_f[df_f['Comments'] == 'Thermostate'].sort_values(by='Comments')
            st.dataframe(Thermostate)
            col4, col5, col6 = st.columns([3,1,2])
            with col4:
                display_tab('Thermostate')
        with tab24:
            Thermocouple = df_f[df_f['Comments'] == 'Thermocouple'].sort_values(by='Comments')
            st.dataframe(Thermocouple)
            col4, col5, col6 = st.columns([3,1,2])
            with col4:
                display_tab('Thermocouple')

        st.header('Select from these items')
     
        tab25, tab26 ,tab27, tab28,tab29, tab30 ,tab31, tab32, tab33  = st.tabs(['Ups','Power strip','Power supply','Electricity','Electricity pin',
        'Feedback','Battery','Electronic board','Electronic buzzer'])

        with tab25:
            Ups = df_f[df_f['Comments'] == 'Ups'].sort_values(by='Comments')
            st.dataframe(Ups)
            col16, col2, col31 = st.columns([3,.5,3])
            with col16:
                display_tab('Ups')
                csv = df_f.to_csv(index=False)
                st.download_button(label="Download updated CSV", data=csv, file_name='updated_spare_parts.csv', mime='text/csv')
        with tab26:
            Power_strip = df_f[df_f['Comments'] == 'Power strip'].sort_values(by='Comments')
            st.dataframe(Power_strip)
            col16, col2, col31 = st.columns([3,.5,3])
            with col16:
                display_tab('Power_strip')
        with tab27:
            Power_supply = df_f[df_f['Comments'] == 'Power supply'].sort_values(by='Comments')
            st.dataframe(Power_supply)
            col16, col2, col31 = st.columns([3,.5,3])
            with col16:
                display_tab('Power_supply')
        with tab28:
            Electricity = df_f[df_f['Comments'] == 'Electricity'].sort_values(by='Comments')
            st.dataframe(Electricity)
            col16, col2, col31 = st.columns([3,.5,3])
            with col16:
                display_tab('Electricity')
        with tab29:
            Electricity_pin = df_f[df_f['Comments'] == 'Electricity pin'].sort_values(by='Comments')
            st.dataframe(Electricity_pin)
            col16, col2, col31 = st.columns([3,.5,3])
            with col16:
                display_tab('Electricity_pin')
        with tab30:
            Feedback = df_f[df_f['Comments'] == 'Feedback'].sort_values(by='Comments')
            st.dataframe(Feedback)
            col16, col2, col31 = st.columns([3,.5,3])
            with col16:
                display_tab('Feedback')
        with tab31:
            Battery = df_f[df_f['Comments'] == 'Battery'].sort_values(by='Comments')
            st.dataframe(Battery)
            col16, col2, col31 = st.columns([3,.5,3])
            with col16:
                display_tab('Battery')
        with tab32:
            Electronic_board = df_f[df_f['Comments'] == 'Electronic board'].sort_values(by='Comments')
            st.dataframe(Electronic_board)
            col16, col2, col31 = st.columns([3,.5,3])
            with col16:
                display_tab('Electronic_board')
        with tab33:
            Electronic_buzzer = df_f[df_f['Comments'] == 'Electronic buzzer'].sort_values(by='Comments')
            st.dataframe(Electronic_buzzer)
            col16, col2, col31 = st.columns([3,.5,3])
            with col16:
                display_tab('Electronic_buzzer')
    
    if __name__ == '__main__':

        main()


if page == 'Pneumatic parts': 
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

# Display a placeholder while loading data
        with st.spinner("Data loaded successfully!"):
            # Simulate loading data
            import time
            time.sleep(1)

        st.markdown("""
    <h2 style='text-align: center; font-size: 40px; color: red;'>
        Find your Pneumatic parts
    </h2>
""", unsafe_allow_html=True)
        st.subheader('Select from these items')
      
        tab1, tab2 ,tab3, tab4,tab5, tab6 ,tab7  = st.tabs(['Oil seal','Gasket','Gauge','Solenoid valve','Neumatic hose','Cylinder','Regulator'])

        with tab1:
            Oil_seal = df_f[df_f['Comments'] == 'Oil seal'].sort_values(by='Comments')
            st.dataframe(Oil_seal)
        with tab2:
            Gasket = df_f[df_f['Comments'] == 'Gasket'].sort_values(by='Comments')
            st.dataframe(Gasket)
        with tab3:
            Gauge = df_f[df_f['Comments'] == 'Gauge'].sort_values(by='Comments')
            st.dataframe(Gauge)
        with tab4:
            Solenoid_valve = df_f[df_f['Comments'] == 'Solenoid valve'].sort_values(by='Comments')
            st.dataframe(Solenoid_valve)
        with tab5:
            Neumatic_hose = df_f[df_f['Comments'] == 'Neumatic hose'].sort_values(by='Comments')
            st.dataframe(Neumatic_hose)
        with tab6:
            Cylinder = df_f[df_f['Comments'] == 'Cylinder'].sort_values(by='Comments')
            st.dataframe(Cylinder)
        with tab7:
            Regulator = df_f[df_f['Comments'] == 'Regulator'].sort_values(by='Comments')
            st.dataframe(Regulator)
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

# Display a placeholder while loading data
        with st.spinner("Data loaded successfully!"):
            # Simulate loading data
            import time
            time.sleep(1)

        st.markdown("""
    <h2 style='text-align: center; font-size: 40px; color: red;'>
        Find your FORKLIFT parts
    </h2>
""", unsafe_allow_html=True)
        st.subheader('Select from these items')
      
        tab1, tab2 ,tab3, tab4,tab5, tab6 ,tab7  = st.tabs(['Forklift wheel','Forklift switch','Forklift coolant','Forklift switch',
        'Forklift control','Forklift carbon','Forklift break'])

        with tab1:
            Forklift_wheel = df_f[df_f['Comments'] == 'Forklift wheel'].sort_values(by='Comments')
            st.dataframe(Forklift_wheel)
        with tab2:
            Forklift_switch = df_f[df_f['Comments'] == 'Forklift switch'].sort_values(by='Comments')
            st.dataframe(Forklift_switch)
        with tab3:
            Forklift_coolant = df_f[df_f['Comments'] == 'Forklift coolant'].sort_values(by='Comments')
            st.dataframe(Forklift_coolant)
        with tab4:
            Forklift_switch = df_f[df_f['Comments'] == 'Forklift switch'].sort_values(by='Comments')
            st.dataframe(Forklift_switch)
        with tab5:
            Forklift_control = df_f[df_f['Comments'] == 'Forklift control'].sort_values(by='Comments')
            st.dataframe(Forklift_control)
        with tab6:
            Forklift_carbon = df_f[df_f['Comments'] == 'Forklift carbon'].sort_values(by='Comments')
            st.dataframe(Forklift_carbon)
        with tab7:
            Forklift_break = df_f[df_f['Comments'] == 'Forklift break'].sort_values(by='Comments')
            st.dataframe(Forklift_break)
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

# Display a placeholder while loading data
        with st.spinner("Data loaded successfully!"):
            # Simulate loading data
            import time
            time.sleep(1)

        # Once data is loaded, display a message
      
        st.markdown("""
    <h2 style='text-align: center; font-size: 40px; color: red;'>
        Find your Utility parts
    </h2>
""", unsafe_allow_html=True)
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
                    st.dataframe(Conductivity_transmitter)
                   
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
                    st.dataframe(Flowmeter_controller)
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
                    st.dataframe(Flow_module)
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
                    st.dataframe(Flow_monitor)
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
                    st.dataframe(conductivity)
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
                    st.dataframe(STILMAS_SENSOR)
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
                    st.dataframe(Valve)
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
                    st.dataframe(test)
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
                    st.dataframe(pump)
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
                st.dataframe(Uv)
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
                st.dataframe(Ro)
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
                    st.dataframe(Fire_detector)
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
                    st.dataframe(Fire_valve)
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
                st.dataframe(AHU_Valve)
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
                    st.dataframe(Hepa_filter)
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
                    st.dataframe(High_filter)
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
                    st.dataframe(Pre_filter)
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
                    st.dataframe(Packfilter)
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
                    st.dataframe(Pump_filter)
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
                    st.dataframe(Emflon_filter)
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
                    st.dataframe(Filters_cartage)
                with col3:
                    st.subheader('image  for  these  part')
                    image56 = open('images/56.PNG', 'rb').read()
                    st.image(image56, width=150)
                    url = 'https://shop.pall.com/us/en/food-beverage/zidimmfdh4o'
                    st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                    
                  
            
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

# Display a placeholder while loading data
        with st.spinner("Data loaded successfully!"):
            # Simulate loading data
            import time
            time.sleep(1)
        
        st.markdown("""
    <h2 style='text-align: center; font-size: 40px; color: red;'>
        Find your LOTOTO parts
    </h2>
""", unsafe_allow_html=True)
        st.subheader('Select from these items')

        LOTOTO = df_f[df_f['Comments'] == 'Lototo'].sort_values(by='Comments')
        st.dataframe(LOTOTO)

    if __name__ == '__main__':

        main()
 

if page == 'GLATT': 
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

# Display a placeholder while loading data
        with st.spinner("Data loaded successfully!"):
            # Simulate loading data
            import time
            time.sleep(1)

        st.markdown("""
    <h2 style='text-align: center; font-size: 40px; color: red;'>
        Find your GLATT parts
    </h2>
""", unsafe_allow_html=True)
        st.subheader('Select from these items')
      
        tab1, tab2 ,tab3 = st.tabs(['Glatt nozzle','Glatt  switch','Glatt valve'])

        with tab1:
            Glatt_nozzle = df_f[df_f['Comments'] == 'Glatt nozzle'].sort_values(by='Comments')
            st.dataframe(Glatt_nozzle)
        with tab2:
            Glatt_switch = df_f[df_f['Comments'] == 'Glatt  switch'].sort_values(by='Comments')
            st.dataframe(Glatt_switch)
        with tab3:
            Glatt_valve = df_f[df_f['Comments'] == 'Glatt valve'].sort_values(by='Comments')
            st.dataframe(Glatt_valve)

    if __name__ == '__main__':

        main()


if page == 'FETTE':

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

# Display a placeholder while loading data
        with st.spinner("Data loaded successfully!"):
            # Simulate loading data
            import time
            time.sleep(1)

        st.markdown("""
    <h2 style='text-align: center; font-size: 40px; color: red;'>
        Find your FETTE parts
    </h2>
""", unsafe_allow_html=True)
        st.subheader('Select from these items')
        col1, col2, col3 = st.columns([5,.5, 2])
        with col1:
            FETTE = df_f[df_f['Comments'] == 'Fette'].sort_values(by='Comments')
            st.dataframe(FETTE)

        with col3:
            if st.button('image  for  these  part'):

                image = open('small_c3fd8f0984028bc7dafbe91cf808227543df0eec_450653_0001.jpg', 'rb').read()
                st.image(image,  width=150)
            
            # Redirect to a web page
                url = 'https://www.abf.store/s/en/bearings/STO12-INA/450653'
                st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')

    if __name__ == '__main__':

        main()

        
