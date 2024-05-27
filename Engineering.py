import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    layout="wide",
    page_title='Earthquake analysis',
    page_icon='🪙'
)


df_f = pd.read_csv('Eng Spare parts.csv')









page =  st.sidebar.radio('Select page', ['Utility area','Mechanical parts', 'Electrical parts',
                    'Pneumatic parts','GLATT','FETTE','FORKLIFT','LOTOTO'])



if page == 'Mechanical parts':
    def main():

        st.title('Find your mechanical parts')

        tab1, tab2 ,tab3, tab4,tab5, tab6 ,tab7, tab8, tab9 ,tab10, tab11 ,tab12, tab13, tab14  = st.tabs(['Bearing', 'Belts','Shaft','Spring',
        'leaflet rooler','Cam','Clutch','Oil _ grease','Bearing_yoke','Chain','Gearbox','Door','Couplin','Wheel CASTOR'])


        with tab1:
            col1, col2, col3 = st.columns([30,3,13])
            with col1:
                peraing = df_f[df_f['Comments'] == 'Bearing'].sort_values(by='Comments')
                st.dataframe(peraing,width=2000)
            with col3:
                st.subheader('image  for  these  part')

                SKF,ASAHI,INA,KBC,IKO,NTN,NB = st.tabs(['SKF','ASAHI','INA','IKO','KBC','NB','NTN'])

                with SKF:
                    image1 = open('1.jpeg', 'rb').read()
                    st.image(image1, width=200)
                    url = 'https://www.skf.com/id/productinfo/productid-6001-2Z%2FC3'
                    st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                with ASAHI:
                    image2 = open('2.jpg', 'rb').read()
                    st.image(image2,  width=200)
                    
                    url = 'https://th.misumi-ec.com/en/vona2/detail/221000612127/?HissuCode=JAF10'
                    st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                with INA:
                    image3 = open('3.jpg', 'rb').read()
                    st.image(image3, width=200)
                    
                    url = 'https://www.abf.store/s/en/bearings/STO12-INA/450653'
                    st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                with IKO:
                    image4 = open('4.jpg', 'rb').read()
                    st.image(image4,  width=200)
                    
                    url = 'https://www.acorn-ind.co.uk/p/iko/closed-type-linear-ball-bearings/lme122232n-iko/'
                    st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                with KBC:
                    image5 = open('5.jpg', 'rb').read()
                    st.image(image5,  width=200)
                    
                    url = 'https://trimantec.com/products/kbc-bearings-radial-bearing-6004-d-6004-rs'
                    st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                with NTN:
                    image6 = open('6.png', 'rb').read()
                    st.image(image6,  width=200)
                    
                    url = 'https://www.2rs.bg/en-gb/6004-llu-5k-ntn.html'
                    st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                with NB:
                    image7 = open('7.jpg', 'rb').read()
                    st.image(image7, width=200)
                    
                    url = 'https://www.abf.store/s/en/bearings/6212-2NSE-NACHI/381266'
                    st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
        with tab2:
            col1, col2, col3 = st.columns([30,3,13])
            with col1:
                Belts = df_f[df_f['Comments'] == 'Belts'].sort_values(by='Comments')
                st.dataframe(Belts,width=2000)
            with col3:
                st.subheader('image  for  these  part')

                SKF2,ASAHI2 = st.tabs(['SKF2','ASAHI2'])

                with SKF2:
                    image1 = open('1.jpeg', 'rb').read()
                    st.image(image1, width=200)
                    url = 'https://www.skf.com/id/productinfo/productid-6001-2Z%2FC3'
                    st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
                with ASAHI2:
                    image2 = open('2.jpg', 'rb').read()
                    st.image(image2,  width=200)
                    
                    url = 'https://th.misumi-ec.com/en/vona2/detail/221000612127/?HissuCode=JAF10'
                    st.components.v1.html(f'<a href="{url}" target="_blank" style="background-color: #FFD700;">Go to Web Page</a>')
            

        with tab3:
            Shaft = df_f[df_f['Comments'] == 'Shaft'].sort_values(by='Comments')
            st.dataframe(Shaft)

        with tab4:
            Spring = df_f[df_f['Comments'] == 'Spring'].sort_values(by='Comments')
            st.dataframe(Spring)

        with tab5:
            leaflet_rooler = df_f[df_f['Comments'] == 'Leaflet rooler'].sort_values(by='Comments')
            st.dataframe(leaflet_rooler)

        with tab6:
            Cam = df_f[df_f['Comments'] == 'Cam'].sort_values(by='Comments')
            st.dataframe(Cam)

        with tab7:
            Clutch = df_f[df_f['Comments'] == 'Clutch'].sort_values(by='Comments')
            st.dataframe(Clutch)

        with tab8:
            Oil_grease = df_f[df_f['Comments'] == 'Oil _ grease'].sort_values(by='Comments')
            st.dataframe(Oil_grease)

        with tab9:
            BEARING_YOKE = df_f[df_f['Comments'] == 'Bearing  yoke'].sort_values(by='Comments')
            st.dataframe(BEARING_YOKE)

        with tab10:
            Chain = df_f[df_f['Comments'] == 'Chain'].sort_values(by='Comments')
            st.dataframe(Chain)
            
        with tab11:
            Gearbox = df_f[df_f['Comments'] == 'Gearbox'].sort_values(by='Comments')
            st.dataframe(Gearbox)

        with tab12:
            Door = df_f[df_f['Comments'] == 'Door'].sort_values(by='Comments')
            st.dataframe(Door)
            
        with tab13:
            Couplin = df_f[df_f['Comments'] == 'Couplin'].sort_values(by='Comments')
            st.dataframe(Couplin)

        with tab14:
            Wheel_CASTOR = df_f[df_f['Comments'] == 'Swivel castor'].sort_values(by='Comments')
            st.dataframe(Wheel_CASTOR)

    if __name__ == '__main__':

        main()

if page == 'Electrical parts': 
    def main():

        st.title('Find your Electrical parts')
        st.header('Select from these items')
        
        tab1, tab2 ,tab3, tab4,tab5, tab6 ,tab7, tab8, tab9 ,tab10, tab11 ,tab12  = st.tabs(['Proximity','Sensor','Fiber sensor','Amplifier','Socket',
        'Selector','Button','Switch','Light','Fan','Cable','Fuse'])

        with tab1:
            col1, col2, col3 = st.columns([6,0.5,6])
            with col1:
                Proximity = df_f[df_f['Comments'] == 'Proximity'].sort_values(by='Comments')
                st.dataframe(Proximity)
            
        with tab2:
            Sensor = df_f[df_f['Comments'] == 'Sensor'].sort_values(by='Comments')
            st.dataframe(Sensor)
        with tab3:
            Fiber_sensor = df_f[df_f['Comments'] == 'Fiber sensor'].sort_values(by='Comments')
            st.dataframe(Fiber_sensor)
        with tab4:
            Amplifier = df_f[df_f['Comments'] == 'Amplifier'].sort_values(by='Comments')
            st.dataframe(Amplifier)
        with tab5:
            Socket = df_f[df_f['Comments'] == 'Socket'].sort_values(by='Comments')
            st.dataframe(Socket)
        with tab6:
            Selector = df_f[df_f['Comments'] == 'Selector'].sort_values(by='Comments')
            st.dataframe(Selector)
        with tab7:
            Button = df_f[df_f['Comments'] == 'Button'].sort_values(by='Comments')
            st.dataframe(Button)
        with tab8:
            Switch = df_f[df_f['Comments'] == 'Switch'].sort_values(by='Comments')
            st.dataframe(Switch)
        with tab9:
            Light = df_f[df_f['Comments'] == 'Light'].sort_values(by='Comments')
            st.dataframe(Light)
        with tab10:
            Fan = df_f[df_f['Comments'] == 'Fan'].sort_values(by='Comments')
            st.dataframe(Fan)
        with tab11:
            Cable = df_f[df_f['Comments'] == 'Cable'].sort_values(by='Comments')
            st.dataframe(Cable)
        with tab12:
            Fuse = df_f[df_f['Comments'] == 'Fuse'].sort_values(by='Comments')
            st.dataframe(Fuse)

        st.header('Select from these items')

        tab13, tab14 ,tab15, tab16,tab17, tab18 ,tab19, tab20, tab21 ,tab22, tab23 ,tab24  = st.tabs(['Converter','Control','Conductor','Contactor','Controller',
        'Inverter','Relay','Jumper','Panel','Heater','Thermostate','Thermocouple'])

        with tab13:
            Converter = df_f[df_f['Comments'] == 'Converter'].sort_values(by='Comments')
            st.dataframe(Converter)
        with tab14:
            Control = df_f[df_f['Comments'] == 'Control'].sort_values(by='Comments')
            st.dataframe(Sensor)
        with tab15:
            Conductor = df_f[df_f['Comments'] == 'Conductor'].sort_values(by='Comments')
            st.dataframe(Conductor)
        with tab16:
            Contactor = df_f[df_f['Comments'] == 'Contactor'].sort_values(by='Comments')
            st.dataframe(Contactor)
        with tab17:
            Controller = df_f[df_f['Comments'] == 'Controller'].sort_values(by='Comments')
            st.dataframe(Controller)
        with tab18:
            Inverter = df_f[df_f['Comments'] == 'Inverter'].sort_values(by='Comments')
            st.dataframe(Inverter)
        with tab19:
            Relay = df_f[df_f['Comments'] == 'Relay'].sort_values(by='Comments')
            st.dataframe(Relay)
        with tab20:
            Jumper = df_f[df_f['Comments'] == 'Jumper'].sort_values(by='Comments')
            st.dataframe(Jumper)
        with tab21:
            Panel = df_f[df_f['Comments'] == 'Panel'].sort_values(by='Comments')
            st.dataframe(Panel)
        with tab22:
            Heater = df_f[df_f['Comments'] == 'Heater'].sort_values(by='Comments')
            st.dataframe(Heater)
        with tab23:
            Thermostate = df_f[df_f['Comments'] == 'Thermostate'].sort_values(by='Comments')
            st.dataframe(Thermostate)
        with tab24:
            Thermocouple = df_f[df_f['Comments'] == 'Thermocouple'].sort_values(by='Comments')
            st.dataframe(Thermocouple)

        st.header('Select from these items')

        tab25, tab26 ,tab27, tab28,tab29, tab30 ,tab31, tab32, tab33  = st.tabs(['Ups','Power strip','Power supply','Electricity','Electricity pin',
        'Feedback','Battery','Electronic board','Electronic buzzer'])

        with tab25:
            Ups = df_f[df_f['Comments'] == 'Ups'].sort_values(by='Comments')
            st.dataframe(Ups)
        with tab26:
            Power_strip = df_f[df_f['Comments'] == 'Power strip'].sort_values(by='Comments')
            st.dataframe(Power_strip)
        with tab27:
            Power_supply = df_f[df_f['Comments'] == 'Power supply'].sort_values(by='Comments')
            st.dataframe(Power_supply)
        with tab28:
            Electricity = df_f[df_f['Comments'] == 'Electricity'].sort_values(by='Comments')
            st.dataframe(Electricity)
        with tab29:
            Electricity_pin = df_f[df_f['Comments'] == 'Electricity pin'].sort_values(by='Comments')
            st.dataframe(Electricity_pin)
        with tab30:
            Feedback = df_f[df_f['Comments'] == 'Feedback'].sort_values(by='Comments')
            st.dataframe(Feedback)
        with tab31:
            Battery = df_f[df_f['Comments'] == 'Battery'].sort_values(by='Comments')
            st.dataframe(Battery)
        with tab32:
            Electronic_board = df_f[df_f['Comments'] == 'Electronic board'].sort_values(by='Comments')
            st.dataframe(Electronic_board)
        with tab33:
            Electronic_buzzer = df_f[df_f['Comments'] == 'Electronic buzzer'].sort_values(by='Comments')
            st.dataframe(Electronic_buzzer)
            tab1, tab2 ,tab3, tab4,tab5, tab6 ,tab7, tab8, tab9 ,tab10, tab11 ,tab12  = st.tabs(['Proximity','Sensor','Fiber sensor','Amplifier','Socket',
        'Selector','Button','Switch','Light','Fan','Cable','Fuse'])


    if __name__ == '__main__':

        main()


if page == 'Pneumatic parts': 
    def main():

        st.title('Find your Pneumatic parts')
        st.header('Select from these items')
      
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

        st.title('Find your FORKLIFT parts')
        st.header('Select from these items')
      
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
        
        st.title('Find your Utility parts')

        select_col = st.selectbox('Select page', ['Water Station','Fire Fighting', 'AHU','Filters'])

        if select_col == 'Water Station':

            tab1, tab2 ,tab3, tab4,tab5, tab6 ,tab7 , tab8, tab9 ,tab10, tab11 ,tab12,tab13 = st.tabs(['Conductivity transmitter','Flowmeter controller','Flow module',
            'Flow monitor','conductivity','Stilmas sensor','intermediate','Valve','test','pump','heater','Uv','Ro'])
            
            with tab1:
                Conductivity_transmitter = df_f[df_f['Comments'] == 'Conductivity transmitter'].sort_values(by='Comments')
                st.dataframe(Conductivity_transmitter)
            with tab2:
                Flowmeter_controller = df_f[df_f['Comments'] == 'Flowmeter controller'].sort_values(by='Comments')
                st.dataframe(Flowmeter_controller)
            with tab3:
                Flow_module = df_f[df_f['Comments'] == 'Flow module'].sort_values(by='Comments')
                st.dataframe(Flow_module)
            with tab4:
                Flow_monitor = df_f[df_f['Comments'] == 'Flow monitor sensor'].sort_values(by='Comments')
                st.dataframe(Flow_monitor)
            with tab5:
                conductivity = df_f[df_f['Comments'] == 'Water conductivity'].sort_values(by='Comments')
                st.dataframe(conductivity)
            with tab6:
                STILMAS_SENSOR = df_f[df_f['Comments'] == 'Stilmas sensor'].sort_values(by='Comments')
                st.dataframe(STILMAS_SENSOR)
            with tab7:
                intermediate = df_f[df_f['Comments'] == 'Water intermediate'].sort_values(by='Comments')
                st.dataframe(intermediate)
            with tab8:
                Valve = df_f[df_f['Comments'] == 'Water valve'].sort_values(by='Comments')
                st.dataframe(Valve)
            with tab9:
                test = df_f[df_f['Comments'] == 'Water test '].sort_values(by='Comments')
                st.dataframe(test)
            with tab10:
                pump = df_f[df_f['Comments'] == 'Water pump'].sort_values(by='Comments')
                st.dataframe(pump)
            with tab11:
                heater = df_f[df_f['Comments'] == 'Water heater'].sort_values(by='Comments')
                st.dataframe(heater)
            with tab12:
                Uv = df_f[df_f['Comments'] == 'Water uv'].sort_values(by='Comments')
                st.dataframe(Uv)
            with tab13:
                Ro = df_f[df_f['Comments'] == 'Water ro'].sort_values(by='Comments')
                st.dataframe(Ro)
                
        elif select_col == 'Fire Fighting':
            
            tab1, tab2 = st.tabs(['Fire detector','Fire valve'])
            with tab1:
                Fire_detector = df_f[df_f['Comments'] == 'Fire detector'].sort_values(by='Comments')
                st.dataframe(Fire_detector)

            with tab2:
                Fire_valve = df_f[df_f['Comments'] == 'Fire valve'].sort_values(by='Comments')
                st.dataframe(Fire_valve)

        elif select_col == 'AHU':

            AHU_Valve = df_f[df_f['Comments'] == 'Valve ahu'].sort_values(by='Comments')
            st.dataframe(AHU_Valve)

        elif select_col == 'Filters':


            tab1, tab2 ,tab3, tab4, tab5, tab6 ,tab7  = st.tabs(['Hepa filter','High filter','Pre filter','Pack filter','Pump filter','Emflon filter','Filters cartage'])

            with tab1:
                Hepa_filter = df_f[df_f['Comments'] == 'Hepa filter'].sort_values(by='Comments')
                st.dataframe(Hepa_filter)
            with tab2:
                High_filter = df_f[df_f['Comments'] == 'High filter'].sort_values(by='Comments')
                st.dataframe(High_filter)
            with tab3:
                Pre_filter = df_f[df_f['Comments'] == 'Pre-filter'].sort_values(by='Comments')
                st.dataframe(Pre_filter)
            with tab4:
                Packfilter = df_f[df_f['Comments'] == 'Packfilter'].sort_values(by='Comments')
                st.dataframe(Packfilter)
            with tab5:
                Pump_filter = df_f[df_f['Comments'] == 'Pump filter'].sort_values(by='Comments')
                st.dataframe(Pump_filter)
            with tab6:
                Emflon_filter = df_f[df_f['Comments'] == 'Emflon filter'].sort_values(by='Comments')
                st.dataframe(Emflon_filter)
            with tab7:
                Filters_cartage = df_f[df_f['Comments'] == 'Filters cartage'].sort_values(by='Comments')
                st.dataframe(Filters_cartage)
            
    if __name__ == '__main__':

        main()


if page == 'LOTOTO':
    
    def main():
        
        st.title('Find your LOTOTO parts')

        LOTOTO = df_f[df_f['Comments'] == 'Lototo'].sort_values(by='Comments')
        st.dataframe(LOTOTO)

    if __name__ == '__main__':

        main()
 

if page == 'GLATT': 
    def main():

        st.title('Find your GLATT parts')
        st.header('Select from these items')
      
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

        st.title('Find your FETTE parts')
        col1, col2, col3 = st.columns([5,.5, 2])
        with col1:
            FETTE = df_f[df_f['Comments'] == 'Fette'].sort_values(by='Comments')
            st.dataframe(FETTE)

    if __name__ == '__main__':

        main()

        
