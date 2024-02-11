# importing required modules//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
from tkinter import *
from tkinter import filedialog
import customtkinter
from PIL import ImageTk, Image
from fpdf import FPDF
import datetime
import sqlite3
import os
from aphyt import omron
import socket
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#creating Tkinter theme and opening window***********************************************************

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green


app = customtkinter.CTk()  # MAIN WINDOW, creating cutstom tkinter window
app.geometry("600x440")
app.title('DPL Caliberation')

#*****************************************************************************************************


#////////////////////////////////    ------------------------LOGIN WINDOW------------------------   ////////////////////////////////////////////////////////////////////////////

# Function - Window Construction - Login window**********************************************************************************************************************

img1 = ImageTk.PhotoImage(Image.open("img_unsplash2.jpg")) # the image in the background of the login window
Login_l1 = customtkinter.CTkLabel(master=app, image=img1)
Login_l1.pack()

# creating custom frame
Login_main_frame = customtkinter.CTkFrame(master=Login_l1, width=320, height=360, corner_radius=15)
Login_main_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

Login_l2 = customtkinter.CTkLabel(master=Login_main_frame,text='DPL CALIBRATION',font=('Century Gothic', 20,'bold'))
Login_l2.place(x=70, y=40)

Login_entry1 = customtkinter.CTkEntry(master=Login_main_frame, width=220, placeholder_text='Username')
Login_entry1.place(x=50, y=110)

Login_entry2 = customtkinter.CTkEntry(master=Login_main_frame, width=220, placeholder_text='Password', show="*")
Login_entry2.place(x=50, y=165)

Login_button = customtkinter.CTkButton(master=Login_main_frame, width=220, text="Login", command=lambda: login_button_function(Login_entry1.get(),Login_entry2.get()), corner_radius=6)
Login_button.place(x=50, y=220)

Login_copyright = customtkinter.CTkLabel(master=Login_main_frame,text='@ For Development Assistant - Chamath Sandaru',font=('Century Gothic',10))
Login_copyright.place(x=50, y=300)

Login_copyright_2 = customtkinter.CTkLabel(master=Login_main_frame,text='chamathac99@gmail.com',font=('Century Gothic',10))
Login_copyright_2.place(x=85, y=320)

#end of - Function - Window Construction - Login window*************************************************************************************************************

# Function - execution of the logging Button***********************************************

def login_button_function(para1,para2):

   if para1=="admin" and para2=="Colombo1":
     Home_page()

   else:
     Login_Failed_Window()

# end 0f - Function for execution of the logging Button*************************************

# Function - Window Construction - Login Failed Pop up window**********************************************************************************************

def Login_Failed_Window():
  win_log_fail = customtkinter.CTk()
  win_log_fail.geometry("320x200")
  win_log_fail.title('Login Failed')

  Login_Failed_l1 = customtkinter.CTkLabel(master=win_log_fail, text="Incorrect Credentials !", font=('Century Gothic', 17))
  Login_Failed_l1.place(x=80, y=20)

  # img2 = customtkinter.CTkImage(Image.open("Google__G__Logo.svg.webp").resize((20, 20), Image.LANCZOS))

  Login_Failed_Exit_button = customtkinter.CTkButton(master=win_log_fail, width=220, text="Exit Software", command=lambda: Close_all(win_log_fail, app),corner_radius=6)
  Login_Failed_Exit_button.place(x=50, y=70)
  Login_Failed_Try_button = customtkinter.CTkButton(master=win_log_fail, width=220, text="Try again", command=lambda: win_log_fail.destroy(),corner_radius=6)
  Login_Failed_Try_button.place(x=50, y=120)
  win_log_fail.mainloop()

def Close_all(win1,win2):
  win1.destroy()
  win2.destroy()

# end of - Function - Window Construction - Login Failed Pop up window**************************************************************************************


#///////////////////////////////////////////////   ------------------------end of -LOGIN WINDOW------------------------   ///////////////////////////////////////////////////////////////////



#//////////////////////////////////////    ------------------------HOME WINDOW------------------------   ////////////////////////////////////////////////////////////////////////////



x= datetime.datetime.now()
date=str(x.year)+'-'+str(x.month)+'-'+str(x.day) #present date
next_cal_date=str(x.year+1)+'-'+str(x.month)+'-'+str(x.day) # addding one to the present year since the next caliberation date comes after a year

range_init = 6
Calib_entry_list=[] # [[raw1 value, raw2 value,......],[raw1 value, raw2 value,......],[],[],[],[],[],[]]
Calib_read_button_list=[]
master_guage_calib_values =[]

start_temp=40.00
end_temp=90.00
Serial_read_plot_permission=True
port_names = []
selected_from_location_window=[['','','',''],['','','',''],['','','',''],['','','',''],['','','',''],['','','',''],['','','','']] #['plant','place','equipment no','accuracy']
Plant_Loc_Equip_object_list=[]

selected_accuracy=''

Reference_number=''
Work_order_number=''
Equipment_number=''
Serial_value=0.00
plc_read_permission=TRUE
Location_button_no=1
Active_Window=app
authorization_password='Colombo10'
probe_type=1
mean_sensor_error=0
cooling_bool=0



def Home_page ():
    # destroy current window and creating new one
  customtkinter.set_default_color_theme("dark-blue")
  global Active_Window
  global range_init
  global start_temp
  global end_temp

  Active_Window.destroy()

  win_Home = customtkinter.CTk()
  win_Home.geometry("1280x810")
  win_Home.title('Home')

  Active_Window = win_Home


  Home_main_frame = customtkinter.CTkFrame(master=win_Home, width=1280, height=810, corner_radius=15)
  Home_main_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
  range_start_init = 40
  # Controls inside the Sensor Value frame *****************************************************************************************************************


  def Calib_frame_func(val_range):

    global Calib_entry_list
    global Calib_read_button_list
    Calib_entry_list=[] # otherwise if run several in a one opening of the software, all ebtries in all the rounds will be appended
    Calib_read_button_list=[]

    Home_calib_frame = customtkinter.CTkFrame(master=Home_main_frame, width=980, height=255, corner_radius=15)
    Home_calib_frame.place(x=50, y=30)

    Home_calib_l = customtkinter.CTkLabel(master=Home_main_frame, text="Sensor Values", font=('Century Gothic', 12))
    Home_calib_l.place(x=50, y=2)


    Y = 8

    for channels in range(0,8):
      X = 50
      if channels==0:
        channel_no='Mast'
      else:
        channel_no="Ch"+str(channels)
      Calib_entry_one_channel_list=[]

      label_name = customtkinter.CTkLabel(master=Home_calib_frame, text=channel_no, font=('Century Gothic', 12))
      label_name.place(x=20, y=Y)

      for i in range(0,val_range):

        entry_name = customtkinter.CTkEntry(master=Home_calib_frame, width=((900/val_range)*(0.7)), placeholder_text='0.0')
        Calib_entry_one_channel_list.append(entry_name)
        entry_name.place(x=X, y=Y)
        X+=((900/val_range))

      Y+=30
      Calib_entry_list.append(Calib_entry_one_channel_list)

  Calib_frame_func(range_init)

  Range_selection_drop = customtkinter.CTkOptionMenu(master=Home_main_frame,values=['200', '100','400'])
  Range_selection_drop.place(x=1070, y=30)

  customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

  PLC_Read_Start_Button = customtkinter.CTkButton(master=Home_main_frame, width=80, text="Start PLC",corner_radius=6,command=lambda:Read_button_function())
  PLC_Read_Start_Button.place(x=1060, y=70)

  PLC_Read_Pause_Button = customtkinter.CTkButton(master=Home_main_frame, width=80, text="Pause PLC", corner_radius=6,command=lambda: Pause_button_function())
  PLC_Read_Pause_Button.place(x=1150, y=70)

  PLC_Read_Stop_Button = customtkinter.CTkButton(master=Home_main_frame, width=120, text="Stop and Refresh",corner_radius=6, command=lambda: Stop_and_refresh_Plc_function())
  PLC_Read_Stop_Button.place(x=1085, y=105)

  customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

  def Pause_button_function():
    global plc_read_permission
    plc_read_permission = FALSE

  def Stop_and_refresh_Plc_function():
    global plc_read_permission
    plc_read_permission=FALSE

    for raws in Calib_entry_list:
      for columns in raws:
        columns.delete(0, END)
        columns.insert(0, '0.0')

  def Read_button_function():
    global plc_read_permission
    global cooling_bool
    cooling_bool=0

    plc_read_permission =TRUE #Otherwise if stop and try to start again, permission will be Flase and won't read plc values
    comparison_variable=0
    ref_column=0

    try:
      # Create a socket object
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

      # Set a timeout for the connection attempt (in seconds)
      sock.settimeout(2)

      # Attempt to connect to the PLC
      result = sock.connect_ex(('192.168.250.1', 44818))

      # Check the connection result
      if result == 0:
        print(f"PLC at {'192.168.250.1'}:{44818} is connected.")
      else:
        print(f"PLC at {'192.168.250.1'}:{44818} is not connected.")
        Print_Error_Window("Connection Failed with PLC", win_Home)
        exit()

        # Close the socket
      sock.close()

    except socket.error as e:
      print(f"An error occurred while connecting to the PLC: {str(e)}")


    while(plc_read_permission):

      try:

        if comparison_variable>=(float(master_guage_calib_values[-1])+1): #if the last value should be 110, then this line active after the reading exceeds 111
          cooling_bool=1
        if cooling_bool and comparison_variable<(float(master_guage_calib_values[0])):
          cooling_bool=0
          break
          print("Caliberation Done")

        eip_instance = omron.n_series.NSeriesThreadDispatcher()
        eip_instance.connect_explicit('192.168.250.1')
        eip_instance.register_session()
        eip_instance.update_variable_dictionary()

        global probe_type

        if Range_selection_drop.get() == '100':
          probe_type = 100 / 10
        elif Range_selection_drop.get() == '200':
          probe_type = 200 / 10
        elif Range_selection_drop.get() == '400':
          probe_type = 400 / 10


        # prbe_type is a float variable that changes with the value of the Range_selection_drop..probe_type=float(Range_selection_drop.get())/10
        channels_values_list = [eip_instance.read_variable('J01_Ch1_RdAI') / probe_type,eip_instance.read_variable('J01_Ch2_RdAI') / probe_type,eip_instance.read_variable('J01_Ch3_RdAI') / probe_type,
                                eip_instance.read_variable('J01_Ch4_RdAI') / probe_type,eip_instance.read_variable('J01_Ch5_RdAI') / probe_type,eip_instance.read_variable('J01_Ch6_RdAI') / probe_type,
                                eip_instance.read_variable('J01_Ch7_RdAI') / probe_type,eip_instance.read_variable('J01_Ch8_RdAI') / probe_type]

        #comparison_variable += 1
        comparison_variable = channels_values_list[0]

        if cooling_bool==0:
          for value in range(0, len(master_guage_calib_values)):

            #if comparison_variable <= float(master_guage_calib_values[len(master_guage_calib_values) - value - 1]):

            if (channels_values_list[0] <= float(master_guage_calib_values[len(master_guage_calib_values) - value - 1])+0.5)  :
              ref_column = len(master_guage_calib_values) - value - 1

        if cooling_bool==1:
          for value in range(0, len(master_guage_calib_values)):

            # if comparison_variable >= float(master_guage_calib_values[len(master_guage_calib_values) - value - 1]):

            if (channels_values_list[0] >= float(master_guage_calib_values[value])):
              ref_column = value


        for list_index in range(0,len(channels_values_list)):

            Calib_entry_list[list_index][ref_column].delete(0, END)
            Calib_entry_list[list_index][ref_column].insert(0, channels_values_list[list_index])


        eip_instance.close_explicit()
        win_Home.update()

      except :
        Print_Error_Window("Connection Failed with PLC", win_Home)
        break
    else:
      pass

  Report_details_frame = customtkinter.CTkFrame(master=Home_main_frame, width=1195, height=95, corner_radius=15)
  Report_details_frame.place(x=50, y=708)

  Report_Channel_no_lable = customtkinter.CTkLabel(master=Report_details_frame, width=100, text='Choose Channel: ',anchor='w')
  Report_Channel_no_lable.place(x=30, y=25)

  Channels_drop = customtkinter.CTkOptionMenu(master=Report_details_frame, values=['Channel 1','Channel 2','Channel 3','Channel 4','Channel 5','Channel 6','Channel 7',])
  Channels_drop.place(x=150, y=25)

  Report_Reference_no_lable = customtkinter.CTkLabel(master=Report_details_frame, width=100, text='Reference No: ', anchor='w')
  Report_Reference_no_lable.place(x=320, y=10)

  Report_Reference_no_entry = customtkinter.CTkEntry(master=Report_details_frame, width=180, placeholder_text='DPL/QAP/15/D7')
  Report_Reference_no_entry.place(x=440, y=15)

  Report_Work_no_lable = customtkinter.CTkLabel(master=Report_details_frame, width=100, text='Work Order No: ',anchor='w')
  Report_Work_no_lable.place(x=320, y=50)

  Report_Work_no_entry = customtkinter.CTkEntry(master=Report_details_frame, width=180,placeholder_text='4000006273')
  Report_Work_no_entry.place(x=440, y=50)

  Report_Ammend_no_lable = customtkinter.CTkLabel(master=Report_details_frame, width=100, text='Ammendment No: ',anchor='w')
  Report_Ammend_no_lable.place(x=650, y=15)

  Report_Ammend_no_entry = customtkinter.CTkEntry(master=Report_details_frame, width=180)
  Report_Ammend_no_entry.place(x=770, y=15)
  Report_Ammend_no_entry.insert(0,"00")

  Report_Ammend_date_lable = customtkinter.CTkLabel(master=Report_details_frame, width=100, text='Ammendment Date: ',
                                                    anchor='w')
  Report_Ammend_date_lable.place(x=650, y=50)

  Report_Ammend_date_entry = customtkinter.CTkEntry(master=Report_details_frame, width=180)
  Report_Ammend_date_entry.place(x=770, y=50)
  Report_Ammend_date_entry.insert(0, "2018-09-14")



  # Test_report(Ref_No,test_temp,test_med,work_ord_no,equip_no,ser_no,location,Manufacturer,range_st,range_end,uom,accuracy)

  customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

  Test_Report_button = customtkinter.CTkButton(master=Report_details_frame, width=60, text="Get Test Report",corner_radius=6,command=lambda: Test_report(Report_Reference_no_entry.get(),Home_required_Entry_Temp_test.get(),Home_required_Entry_Calib_medium.get(),Report_Work_no_entry.get(),Home_required_Entry_ser_no.get(),Home_required_Entry_Manufacturer.get(),start_temp,end_temp,Home_required_Entry_UOM.get(),Home_required_Entry_accuracy.get(),Channels_drop.get(),Report_Ammend_no_entry.get(),Report_Ammend_date_entry.get(),Error_master_Entry.get()))
  Test_Report_button.place(x=1000, y=15)

  Correction_Factor_Report_button = customtkinter.CTkButton(master=Report_details_frame, width=60, text="Get Correction Factor Report",corner_radius=6,command=lambda:Correction_Factor_report(Channels_drop.get(),Report_Reference_no_entry.get(),Report_Ammend_no_entry.get(),Report_Ammend_date_entry.get()))
  Correction_Factor_Report_button.place(x=1000, y=50)

  customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green



  # end of - Controls inside the Sensor Value frame *******************************************************************************************************


  # Controls inside the Master Guage frame *****************************************************************************************************************

  def Set_temp_frame_func(val_range,start_temp,step):

    global master_guage_calib_values

    master_guage_calib_values=[]


    Home_master_frame = customtkinter.CTkFrame(master=Home_main_frame, width=980, height=40, corner_radius=0)
    Home_master_frame.place(x=50, y=290)


    X = 50
    Y = 5


    for i in range(0,val_range):
      #entry_name='Home_master_entry'+str(i+1)

      entry_name = customtkinter.CTkEntry(master=Home_master_frame, width=((900/val_range)*(0.7)))
      entry_name.place(x=X, y=Y)
      entry_name.insert(0,start_temp)

      master_guage_calib_values.append(entry_name.get())

      X+=((900/val_range))
      start_temp+=step

  Set_temp_frame_func(range_init,range_start_init,10)

  # end of - Controls inside the Master Guage frame **********************************************************************************************************


  Home_range_frame = customtkinter.CTkFrame(master=Home_main_frame, width=200, height=220, corner_radius=15)
  Home_range_frame.place(x=1045, y=140)

  Home_required_Label1 = customtkinter.CTkLabel(master=Home_range_frame, width=60, text='Range', anchor='w')
  Home_required_Label1.place(x=20, y=15)

  Home_required_Label1 = customtkinter.CTkLabel(master=Home_range_frame, width=60, text='From')
  Home_required_Label1.place(x=20, y=50)

  Home_required_Entry_From = customtkinter.CTkEntry(master=Home_range_frame, width=80)
  Home_required_Entry_From.place(x=80, y=50)
  Home_required_Entry_From.insert(0,start_temp)

  Home_required_Label_To = customtkinter.CTkLabel(master=Home_range_frame, width=60, text='To')
  Home_required_Label_To.place(x=20, y=90)

  Home_required_Entry_To = customtkinter.CTkEntry(master=Home_range_frame, width=80)
  Home_required_Entry_To.place(x=80, y=90)
  Home_required_Entry_To.insert(0,end_temp)

  Home_required_Label_By = customtkinter.CTkLabel(master=Home_range_frame, width=60, text='by')
  Home_required_Label_By.place(x=20, y=130)


  Home_required_Entry_By = customtkinter.CTkEntry(master=Home_range_frame, width=80)
  Home_required_Entry_By.place(x=80, y=130)


  Update_range_button = customtkinter.CTkButton(master=Home_range_frame, width=140, text="Update",corner_radius=6,command=lambda : Range_button(Home_required_Entry_From.get(),Home_required_Entry_To.get(),Home_required_Entry_By.get()))
  Update_range_button.place(x=30, y=180)

  Home_required_frame = customtkinter.CTkFrame(master=Home_main_frame, width=980, height=240, corner_radius=15)
  Home_required_frame.place(x=50, y=335)

  Y=25

  for no_of_channels in range(0,7):
    Home_required_channel_Label = customtkinter.CTkLabel(master=Home_required_frame, width=60, text='Ch'+str(no_of_channels+1), anchor='w')
    Home_required_channel_Label.place(x=20, y=Y)
    Y+=30

  Home_required_plant_Label = customtkinter.CTkLabel(master=Home_required_frame, width=60, text='Plant', anchor='w')
  Home_required_plant_Label.place(x=100, y=2)

  Home_required_Loc_Label = customtkinter.CTkLabel(master=Home_required_frame, width=60, text='Location',anchor='w')
  Home_required_Loc_Label.place(x=350, y=2)

  Home_required_Loc_Label = customtkinter.CTkLabel(master=Home_required_frame, width=60, text='Equipment No', anchor='w')
  Home_required_Loc_Label.place(x=600, y=2)

  Y=25

  global Plant_Loc_Equip_object_list
  Plant_Loc_Equip_object_list=[]


  for channels_no in range(0,7):

    Each_channel_plant_equip_raw=[]
    Home_required_plant_Entry = customtkinter.CTkEntry(master=Home_required_frame, width=200)
    Home_required_plant_Entry.place(x=100, y=Y)
    Home_required_plant_Entry.insert(0, selected_from_location_window[channels_no][0])
    Each_channel_plant_equip_raw.append(Home_required_plant_Entry)

    Home_required_Loc_Entry = customtkinter.CTkEntry(master=Home_required_frame, width=200)
    Home_required_Loc_Entry.place(x=350, y=Y)
    Home_required_Loc_Entry.insert(0, selected_from_location_window[channels_no][1])
    Each_channel_plant_equip_raw.append(Home_required_Loc_Entry)

    Home_required_Equip_no_Entry = customtkinter.CTkEntry(master=Home_required_frame, width=200)
    Home_required_Equip_no_Entry.place(x=600, y=Y)
    Home_required_Equip_no_Entry.insert(0, selected_from_location_window[channels_no][2])
    Each_channel_plant_equip_raw.append(Home_required_Equip_no_Entry)

    Y+=30
    Plant_Loc_Equip_object_list.append(Each_channel_plant_equip_raw)


  Add_button_Loc_1 = customtkinter.CTkButton(master=Home_required_frame, width=70, text="Add Location",corner_radius=6, command=lambda: Location_page(win_Home,1))
  Add_button_Loc_1.place(x=850, y=25)
  Add_button_Loc_2 = customtkinter.CTkButton(master=Home_required_frame, width=70, text="Add Location",corner_radius=6, command=lambda: Location_page(win_Home,2))
  Add_button_Loc_2.place(x=850, y=55)
  Add_button_Loc_3 = customtkinter.CTkButton(master=Home_required_frame, width=70, text="Add Location",corner_radius=6, command=lambda: Location_page(win_Home,3))
  Add_button_Loc_3.place(x=850, y=85)
  Add_button_Loc_4 = customtkinter.CTkButton(master=Home_required_frame, width=70, text="Add Location",corner_radius=6, command=lambda: Location_page(win_Home,4))
  Add_button_Loc_4.place(x=850, y=115)
  Add_button_Loc_5 = customtkinter.CTkButton(master=Home_required_frame, width=70, text="Add Location",corner_radius=6, command=lambda: Location_page(win_Home,5))
  Add_button_Loc_5.place(x=850, y=145)
  Add_button_Loc_6 = customtkinter.CTkButton(master=Home_required_frame, width=70, text="Add Location",corner_radius=6, command=lambda: Location_page(win_Home,6))
  Add_button_Loc_6.place(x=850, y=175)
  Add_button_Loc_7 = customtkinter.CTkButton(master=Home_required_frame, width=70, text="Add Location",corner_radius=6, command=lambda: Location_page(win_Home,7))
  Add_button_Loc_7.place(x=850, y=205)







  Home_uom_frame = customtkinter.CTkFrame(master=Home_main_frame, width=980, height=120, corner_radius=15)
  Home_uom_frame.place(x=50, y=580)

  Home_required_UOM_Label = customtkinter.CTkLabel(master=Home_uom_frame, width=60, text='Unit of Measurement',anchor='w')
  Home_required_UOM_Label.place(x=50, y=10)

  Home_required_Entry_UOM = customtkinter.CTkEntry(master=Home_uom_frame, width=200)
  Home_required_Entry_UOM.place(x=200, y=10)
  Home_required_Entry_UOM.insert(0,'CELCIUS')

  Home_required_Calib_medium_Label = customtkinter.CTkLabel(master=Home_uom_frame, width=60, text='Caliberation Medium',anchor='w')
  Home_required_Calib_medium_Label.place(x=50, y=40)

  Home_required_Entry_Calib_medium = customtkinter.CTkEntry(master=Home_uom_frame, width=200)
  Home_required_Entry_Calib_medium.place(x=200, y=40)
  Home_required_Entry_Calib_medium.insert(0,'THERMAL OIL')

  Home_required_Temp_test_Label = customtkinter.CTkLabel(master=Home_uom_frame, width=60, text='Temperature of Test',anchor='w')
  Home_required_Temp_test_Label.place(x=50, y=70)

  Home_required_Entry_Temp_test = customtkinter.CTkEntry(master=Home_uom_frame, width=200)
  Home_required_Entry_Temp_test.place(x=200, y=70)
  Home_required_Entry_Temp_test.insert(0,'ROOM TEMP')

  Home_required_accuracy_Label = customtkinter.CTkLabel(master=Home_uom_frame, width=60, text='Accuracy',anchor='w')
  Home_required_accuracy_Label.place(x=550, y=10)

  Home_required_Entry_accuracy = customtkinter.CTkEntry(master=Home_uom_frame, width=200)
  Home_required_Entry_accuracy.place(x=700, y=10)
  Home_required_Entry_accuracy.insert(0,selected_from_location_window[0][3])

  Home_required_ser_no_Label = customtkinter.CTkLabel(master=Home_uom_frame, width=60, text='Serial Number',anchor='w')
  Home_required_ser_no_Label.place(x=550, y=40)

  Home_required_Entry_ser_no= customtkinter.CTkEntry(master=Home_uom_frame, width=200)
  Home_required_Entry_ser_no.place(x=700, y=40)
  Home_required_Entry_ser_no.insert(0,'K-TYPE PROBE')

  Home_required_Manufacturer_Label = customtkinter.CTkLabel(master=Home_uom_frame, width=60, text='Manufacturer',anchor='w')
  Home_required_Manufacturer_Label.place(x=550, y=70)

  Home_required_Entry_Manufacturer= customtkinter.CTkEntry(master=Home_uom_frame, width=200)
  Home_required_Entry_Manufacturer.place(x=700, y=70)
  Home_required_Entry_Manufacturer.insert(0,'PYROSALES')

#////////////////////////////////////////////////////////// Master Guage Details ///////////////////////////////////////////////////////////////////////////////////

  Home_Master_detail_frame = customtkinter.CTkFrame(master=Home_main_frame, width=200, height=335, corner_radius=15)
  Home_Master_detail_frame.place(x=1045, y=365)

  Select_master_Label = customtkinter.CTkLabel(master=Home_Master_detail_frame, width=60, text='Master Guage',anchor='w')
  Select_master_Label .place(x=20, y=10)

  Get_master_button = customtkinter.CTkButton(master=Home_Master_detail_frame, width=70, text="Add Master Guage Details",corner_radius=6,command=lambda: Master_Guage_page ())
  Get_master_button.place(x=20, y=40)

  Name_master_Label = customtkinter.CTkLabel(master=Home_Master_detail_frame, width=60, text='Name',anchor='w')
  Name_master_Label .place(x=20, y=80)

  Name_master_Entry= customtkinter.CTkEntry(master=Home_Master_detail_frame, width=150)
  Name_master_Entry.place(x=20, y=110)
  Name_master_Entry.insert(0,Selected_Master_Guage_Details[0])

  Error_master_Label = customtkinter.CTkLabel(master=Home_Master_detail_frame, width=60, text='Error',anchor='w')
  Error_master_Label .place(x=20, y=140)


  Error_master_Entry= customtkinter.CTkEntry(master=Home_Master_detail_frame, width=150)
  Error_master_Entry.place(x=20, y=170)
  Error_master_Entry.insert(0, Selected_Master_Guage_Details[1])

  Trace_master_Label = customtkinter.CTkLabel(master=Home_Master_detail_frame, width=60, text='Tracerbility', anchor='w')
  Trace_master_Label.place(x=20, y=200)

  Trace_master_Entry = customtkinter.CTkEntry(master=Home_Master_detail_frame, width=150)
  Trace_master_Entry.place(x=20, y=230)
  Trace_master_Entry.insert(0, Selected_Master_Guage_Details[2])

  Certificate_master_Label = customtkinter.CTkLabel(master=Home_Master_detail_frame, width=60, text='Certificate No',anchor='w')
  Certificate_master_Label.place(x=20, y=260)

  Certificate_master_Entry = customtkinter.CTkEntry(master=Home_Master_detail_frame, width=150)
  Certificate_master_Entry.place(x=20, y=290)
  Certificate_master_Entry.insert(0, Selected_Master_Guage_Details[3])


#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  def Range_button(start,end,step):
    end=float(end)
    start=float(start)
    step=float(step)

    global range_init
    global start_temp
    global end_temp

    start_temp=start
    end_temp=end
    range_init= int((end-start)/step+1)
    Calib_frame_func(range_init)
    Set_temp_frame_func(range_init,float(Home_required_Entry_From.get()),step)


  # ///////////////////////////////////////////-----------REPORTS---------------/////////////////////////////////////////////////////////////////////////////////////////////////

  #-----------------------------------------------TEST REPORT-------------------------------------------------------------------------------------------------------------

  def Test_report(Ref_No, test_temp, test_med, work_ord_no, ser_no, Manufacturer, range_st,range_end,uom, accuracy,channel_no,ammend_no,ammend_date,master_err):

    global master_guage_calib_values
    global selected_from_location_window
    global Plant_Loc_Equip_object_list


    if channel_no=='Channel 1':
      equip_no= Plant_Loc_Equip_object_list[0][2].get()

      location = Plant_Loc_Equip_object_list[0][1].get()

      plant_name = Plant_Loc_Equip_object_list[0][0].get()
    elif channel_no=='Channel 2':
      equip_no= Plant_Loc_Equip_object_list[1][2].get()
      location = Plant_Loc_Equip_object_list[1][1].get()
      plant_name = Plant_Loc_Equip_object_list[1][0].get()
    elif channel_no=='Channel 3':
      equip_no= Plant_Loc_Equip_object_list[2][2].get()
      location = Plant_Loc_Equip_object_list[2][1].get()
      plant_name = Plant_Loc_Equip_object_list[2][0].get()
    elif channel_no == 'Channel 4':
      equip_no= Plant_Loc_Equip_object_list[3][2].get()
      location = Plant_Loc_Equip_object_list[3][1].get()
      plant_name = Plant_Loc_Equip_object_list[3][0].get()
    elif channel_no=='Channel 5':
      equip_no= Plant_Loc_Equip_object_list[4][2].get()
      location = Plant_Loc_Equip_object_list[4][1].get()
      plant_name = Plant_Loc_Equip_object_list[4][0].get()
    elif channel_no == 'Channel 6':
      equip_no= Plant_Loc_Equip_object_list[5][2].get()
      location = Plant_Loc_Equip_object_list[5][1].get()
      plant_name = Plant_Loc_Equip_object_list[5][0].get()
    elif channel_no=='Channel 7':
      equip_no= Plant_Loc_Equip_object_list[6][2].get()
      location = Plant_Loc_Equip_object_list[6][1].get()
      plant_name = Plant_Loc_Equip_object_list[6][0].get()

    pdf = FPDF(format='A4', unit='in')  # if you wanna take this outside this funcion be careful..fpdf errors will occur

    # ---------Data that should be printed in the report in tables----------------------------------------------------------
    data_sensor_properties = [['Work Order Number', work_ord_no, 'Location', plant_name+"-"+location],
                              ['Equipment Number', equip_no, 'Serial Number', ser_no],
                              ['Manufacture', Manufacturer, '', '']
                              ]

    data_table_one = [['Date of Caliberation', date],
                      ['Next Caliberation Due', next_cal_date],
                      ['Temp of Test', test_temp],
                      ['Medium', test_med]]

    data_table_two = [['Range', range_st, 'To', range_end, 'UOM', uom]]
    data_table_three = [['Span', (range_end - range_st)], ['Accuracy', accuracy]]

    data_sensor_values = [['No', 'Indicated Value', 'Value on Master Guage','Correction On Master Guage','Correction']]

    entry_no = 0

    if channel_no =='Channel 1':
      for entries in Calib_entry_list[1]:
        correction=round(float((Calib_entry_list[0][Calib_entry_list[1].index(entries)]).get())-float(entries.get())+float(master_err),2)
        data_sensor_values.append([entry_no+1, (entries.get()),(Calib_entry_list[0][Calib_entry_list[1].index(entries)]).get() ,master_err,correction])
        entry_no += 1

    elif channel_no =='Channel 2':
      for entries in Calib_entry_list[2]:
        correction= round(float((Calib_entry_list[0][Calib_entry_list[2].index(entries)]).get())-float(entries.get())+float(master_err),2)
        data_sensor_values.append([entry_no+1, (entries.get()), (Calib_entry_list[0][Calib_entry_list[2].index(entries)]).get(),master_err,correction])

        entry_no += 1
    elif channel_no =='Channel 3':
      for entries in Calib_entry_list[3]:
        correction= round(float((Calib_entry_list[0][Calib_entry_list[3].index(entries)]).get())-float(entries.get())+float(master_err),2)
        data_sensor_values.append([entry_no+1, (entries.get()), (Calib_entry_list[0][Calib_entry_list[3].index(entries)]).get(),master_err,correction])

        entry_no += 1
    elif channel_no == 'Channel 4':
      for entries in Calib_entry_list[4]:
        correction= round(float((Calib_entry_list[0][Calib_entry_list[4].index(entries)]).get())-float(entries.get())+float(master_err),2)
        data_sensor_values.append([entry_no+1, (entries.get()), (Calib_entry_list[0][Calib_entry_list[4].index(entries)]).get(),master_err,correction])

        entry_no += 1
    elif channel_no == 'Channel 5':
      for entries in Calib_entry_list[5]:
        correction= round(float((Calib_entry_list[0][Calib_entry_list[5].index(entries)]).get())-float(entries.get())+float(master_err),2)
        data_sensor_values.append([entry_no+1, (entries.get()), (Calib_entry_list[0][Calib_entry_list[5].index(entries)]).get(),master_err,correction])

        entry_no += 1
    elif channel_no == 'Channel 6':
      for entries in Calib_entry_list[6]:
        correction= round(float((Calib_entry_list[0][Calib_entry_list[6].index(entries)]).get())-float(entries.get())+float(master_err),2)
        data_sensor_values.append([entry_no+1, (entries.get()), (Calib_entry_list[0][Calib_entry_list[6].index(entries)]).get(),master_err,correction])

        entry_no += 1
    elif channel_no == 'Channel 7':
      for entries in Calib_entry_list[7]:
        correction= round(float((Calib_entry_list[0][Calib_entry_list[7].index(entries)]).get())-float(entries.get())+float(master_err),2)
        data_sensor_values.append([entry_no + 1, (entries.get()), (Calib_entry_list[0][Calib_entry_list[7].index(entries)]).get(), master_err, correction])
        entry_no += 1

    # ---------end of - Data that should be printed in the report in tables----------------------------------------------------------

    # *******************TEST REPORT PDF FORMAT***************************************************************

    pdf.add_page()

    pdf.set_font('Times', '', 9.0)
    epw = pdf.w - 2 * pdf.l_margin
    th = pdf.font_size

    # --------------TITLE TABLE--------------------
    Title_Table(epw, th, pdf, 'IN HOUSE CALIBERATION TEST REPORT', Ref_No,ammend_no,ammend_date)
    # --------------end 0f TITLE TABLE-------------

    # create data_sensor_properties Table----------------------
    global mean_sensor_error # check this mean error for Correction_Factor_report

    error_Indicated_value_multiple=0
    indicated_value_sum=0

    for error_value in range(1,len(data_sensor_values)):
      error_Indicated_value_multiple += (float(data_sensor_values[error_value][1])*float(data_sensor_values[error_value][4]))
      indicated_value_sum+=float(data_sensor_values[error_value][1])

    mean_sensor_error= round(error_Indicated_value_multiple/(indicated_value_sum),2)


    for row in data_sensor_properties:
      for datum in row:
        pdf.cell(epw / 4, 2 * th, str(datum), border=0)
      pdf.ln(2 * th)

    pdf.ln(0.2)
    # end of - create data_sensor_properties Table--------------

    # create data_table_one Table--------------------------------
    for row in data_table_one:
      for datum in row:
        pdf.cell(epw / 2, 2 * th, str(datum), border=1)
      pdf.ln(2 * th)

    pdf.ln(0.2)
    # end of - create data_table_one Table------------------------

    # create data_table_two Table----------------------------------
    for row in data_table_two:
      for datum in row:
        # Enter data in colums
        pdf.cell(epw / 6, 2 * th, str(datum), border=1)

      pdf.ln(2 * th)

    pdf.ln()
    # end of - create data_table_two Table-------------------------

    # create data_table_three Table
    for row in data_table_three:
      for datum in row:
        pdf.cell(epw / 2, 2 * th, str(datum), border=1)
      pdf.ln(2 * th)

    pdf.ln(0.2)
    # end of - create data_table_three Table------------------------

    # create data_sensor_values Table-------------------------------

    for row in data_sensor_values:
      for datum in row:
        if row.index(datum)==0:
          pdf.cell(epw / 10, 2 * th, str(datum), border=1)
        else:
          pdf.cell((9*epw / 40), 2 * th, str(datum), border=1)

      pdf.ln(2 * th)

    # end of -create data_sensor_values Table---------------------------

    pdf.ln(1)
    pdf.cell(epw / 3, 1 * th, '--------------------', border=0, align='C')
    pdf.cell(epw / 3, 1 * th, '--------------------', border=0, align='C')
    pdf.cell(epw / 3, 1 * th, '--------------------', border=0, align='C')

    pdf.ln()

    pdf.cell(epw / 3, 1 * th, 'Date', border=0, align='C')
    pdf.cell(epw / 3, 1 * th, 'Head of Department', border=0, align='C')
    pdf.cell(epw / 3, 1 * th, 'General Manager - Engineering', border=0, align='C')

    # *******************end of - TEST REPORT PDF FORMAT***************************************************************

    database_file_name = 'Databases/' + plant_name + '.db'
    conn = sqlite3.connect(database_file_name)
    c = conn.cursor()
    c.execute("SELECT *, oid FROM locations")
    sensors_records = c.fetchall()

    for each_sensor in sensors_records:
      if each_sensor[2] == equip_no:
        related_sensor_details = each_sensor
        break

    conn = sqlite3.connect('Databases/' + plant_name + '.db')
    c = conn.cursor()

    c.execute("DELETE from locations where equipment_no = '" + equip_no + "'")
    conn.commit()
    conn.close()

    conn = sqlite3.connect('Databases/' + plant_name + '.db')

    c = conn.cursor()

    c.execute(
      "INSERT INTO locations VALUES (:plant, :place, :equipment_no, :start_val, :end_val, :least_count, :accuracy, :exp_date, :calib_frequency, :purchase_date)",
      {
        'plant': plant_name,
        'place': location,
        'equipment_no': equip_no,
        'start_val': float(range_st),
        'end_val': float(range_end),
        'least_count': related_sensor_details[5],
        'accuracy': accuracy,
        'exp_date': next_cal_date,
        'calib_frequency': related_sensor_details[8],
        'purchase_date': related_sensor_details[9]

      }

    )


    conn.commit()
    conn.close()

    savefolder = filedialog.askdirectory()
    newpath_1 = savefolder+'/'+date
    if not os.path.exists(newpath_1):
      os.makedirs(newpath_1)

    edited_equip_no=equip_no.replace("/","_")
    newpath_2 = newpath_1+'/'+edited_equip_no
    if not os.path.exists(newpath_2):
      os.makedirs(newpath_2)

    file_name = newpath_2 + '/' + 'Test_report.pdf'
    Pdf_print(file_name, pdf)



  # -----------------------------------------------end of - TEST REPORT-------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------Correction Factor REPORT-------------------------------------------------------------------------------------------------------------

  def Correction_Factor_report(channel_no,Ref_No,ammend_no,ammend_date):

    global selected_from_location_window

    if channel_no=='Channel 1':
      equip_no= Plant_Loc_Equip_object_list[0][2].get()
    elif channel_no=='Channel 2':
      equip_no= Plant_Loc_Equip_object_list[1][2].get()
    elif channel_no=='Channel 3':
      equip_no= Plant_Loc_Equip_object_list[2][2].get()
    elif channel_no == 'Channel 4':
      equip_no= Plant_Loc_Equip_object_list[3][2].get()
    elif channel_no=='Channel 5':
      equip_no= Plant_Loc_Equip_object_list[4][2].get()
    elif channel_no == 'Channel 6':
      equip_no= Plant_Loc_Equip_object_list[5][2].get()
    elif channel_no=='Channel 7':
      equip_no= Plant_Loc_Equip_object_list[6][2].get()

    pdf = FPDF(format='A4',
                 unit='in')  # if you wanna take this outside this funcion be careful..fpdf errors will occur

    # ---------Data that should be printed in the report in tables----------------------------------------------------------

    data_actual_values = [['Index', 'Observed Value', 'Actual Value','','','']]

    for list_item in range(0,int(end_temp-start_temp)+1):
      data_actual_values.append([str(list_item+1),str(start_temp+(list_item)),str(start_temp+(list_item)+mean_sensor_error),'','',''])

      # ---------end of - Data that should be printed in the report in tables----------------------------------------------------------

      # *******************TEST REPORT PDF FORMAT***************************************************************

    pdf.add_page()

    pdf.set_font('Times', '', 8.0)
    epw = pdf.w - 2 * pdf.l_margin
    th = pdf.font_size

    # --------------TITLE TABLE--------------------
    Title_Table(epw, th, pdf,'CORRECTION FACTOR REPORT',Ref_No,ammend_no,ammend_date)
    # --------------end 0f TITLE TABLE-------------

    # create data_sensor_properties Table----------------------
    if len(data_actual_values)>45:
      for rows in range(46,len(data_actual_values)):
        data_actual_values[rows-45][3]=data_actual_values[rows][0]
        data_actual_values[rows-45][4]=data_actual_values[rows][1]
        data_actual_values[rows-45][5]=data_actual_values[rows][2]

    data_actual_values=data_actual_values[0:46]
    for row in data_actual_values:
      for datum in row:
        pdf.cell(epw / 6, 2 * th, str(datum), border=0)

      pdf.ln(1.5 * th)


    pdf.ln(0.5)
    # end of - create data_sensor_properties Table--------------

    pdf.cell(epw / 3, 1 * th, '--------------------', border=0, align='C')
    pdf.cell(epw / 3, 1 * th, '--------------------', border=0, align='C')
    pdf.cell(epw / 3, 1 * th, '--------------------', border=0, align='C')

    pdf.ln()

    pdf.cell(epw / 3, 1 * th, 'Date', border=0, align='C')
    pdf.cell(epw / 3, 1 * th, 'Head of Department', border=0, align='C')
    pdf.cell(epw / 3, 1 * th, 'General Manager - Engineering', border=0, align='C')

    # *******************end of - TEST REPORT PDF FORMAT***************************************************************
    savefolder = filedialog.askdirectory()
    newpath_1 = savefolder+'/'+date
    if not os.path.exists(newpath_1):
      os.makedirs(newpath_1)

    edited_equip_no=equip_no.replace("/","_")
    newpath_2 = newpath_1+'/'+edited_equip_no
    if not os.path.exists(newpath_2):
      os.makedirs(newpath_2)

    file_name = newpath_2 + '/' + 'Correction_Factor_Report.pdf'
    Pdf_print(file_name, pdf)

  # -----------------------------------------------end of -Correction Factor REPORT-------------------------------------------------------------------------------------------------------------

  def Pdf_print(name,pdf):
    try:
      pdf.output(name, 'F')# save the pdf file
      Print_Success_Window()
    except:
      Print_Error_Window("Error: Make sure you have closed all the related pdf files",win_Home)

  # --------------TITLE TABLE function------------------------------------------------------------------------

  def Title_Table(w,h,pdf,report_name,ref_no,ammend_no,ammend_date):


    pdf.image('logo-1.png', 0.3, 0.5, 2, 0.5)  # image_dpl

    pdf.cell(w / 4, 2 * h, border=0)  # cell for keeping space for the dpl logo
    pdf.cell(w / 2, 2 * h, 'QUALITY ASSURANCE PROCEDURE FOR', border=0, align='C')  # Title
    pdf.cell(w / 4, 2 * h, 'Reference No:', border=1, align='C')  # reference no:

    pdf.ln()

    pdf.cell(w / 4, 2 * h, border=0)  # cell for keeping space for the dpl logo
    pdf.cell(w / 2, 2 * h, 'CALIBERATION OF EQUIPMENT', border=0, align='C')  # Title
    pdf.cell(w / 4, 2 * h, ref_no, border=1, align='C')  #

    pdf.ln(0.5)

    pdf.set_text_color(255, 255, 255)
    pdf.cell(w, 2 * h, report_name, border=0, align='C', fill=TRUE)  # Title
    pdf.set_text_color(0, 0, 0)

    pdf.ln(0.3)

    pdf.cell(w / 2.5, 2 * h, 'Issue', border=1, align='C')
    pdf.cell(w / 2.5, 2 * h, 'Amendment', border=1, align='C')
    pdf.cell(w / 5, 4 * h, 'DL', border=1, align='C')

    pdf.cell(0, 2 * h, border=0)  # Secret Cell

    pdf.ln()

    pdf.cell(w / 5, 2 * h, 'No: 05', border=1, align='C')
    pdf.cell(w / 5, 2 * h, 'Date: 2014-05-19', border=1, align='C')
    pdf.cell(w / 5, 2 * h, 'No:00', border=1, align='C')
    pdf.cell(w / 5, 2 * h, 'Date:'+str(ammend_date), border=1, align='C')
    pdf.cell(w / 5, 2 * h, border=0)

    pdf.ln(0.5)

  # --------------end of - TITLE TABLE function------------------------------------------------------------------

  # --------------Pdf succesful window function------------------------------------------------------------------------
  def Print_Success_Window():

    win_print_suc = customtkinter.CTk()
    win_print_suc.geometry("450x200")
    win_print_suc.title('Succesfull')

    img_suc = ImageTk.PhotoImage(Image.open("done.png").resize((50, 50), Image.LANCZOS),master=win_print_suc)
    img_l1 = customtkinter.CTkLabel(master=win_print_suc, image=img_suc,text='')
    img_l1.place(x=200, y=40)

    pdf_sucess_l1 = customtkinter.CTkLabel(master=win_print_suc, text="Test Report Successfully Created !",font=('Century Gothic', 12))
    pdf_sucess_l1.place(x=120, y=80)


    OK_button = customtkinter.CTkButton(master=win_print_suc, width=220, text="Got it!",command=lambda: win_print_suc.destroy(), corner_radius=6)
    OK_button.place(x=110, y=120)

    win_print_suc.mainloop()

  # --------------end of - Pdf succesful window function---------------------------------------------------------------------

  # **************************Pdf failed window function**********************************************************************************************************






  # ************************** end of - Pdf failed window function**********************************************************************************************************

  # ///////////////////////////////////////////-----------end of - REPORTS---------------/////////////////////////////////////////////////////////////////////////////////////////////////

  win_Home.mainloop()


#///////////////////////////////////////////////   ------------------------end of -HOME WINDOW------------------------   ///////////////////////////////////////////////////////////////////

def Print_Error_Window(Err_message,master_win):
  win_print_err = Toplevel(master=master_win,bg="black")
  win_print_err.geometry("550x200")
  win_print_err.title('Failed')

  img_err = ImageTk.PhotoImage(Image.open("error.png").resize((50, 50), Image.LANCZOS),master=win_print_err)
  img_l1 = customtkinter.CTkLabel(master=win_print_err, image=img_err,text='')
  img_l1.place(relx=0.5, rely=0.25,anchor= CENTER)

  Login_Failed_l1 = customtkinter.CTkLabel(master=win_print_err, text=Err_message,font=('Century Gothic', 12),anchor='n',text_color=("black","lightgray"))
  Login_Failed_l1.place(relx=0.5, rely=0.5,anchor= CENTER)

  OK_button = customtkinter.CTkButton(master=win_print_err, width=220, text="Got it!",command=lambda: win_print_err.destroy(), corner_radius=6)
  OK_button.place(relx=0.5, rely=0.75,anchor= CENTER)


  win_print_err.grab_set()
  master_win.wait_window(win_print_err)

  win_print_err.mainloop()

#//////////////////////////////////////////////// -------------Location Database WINDOW --------------------------------  ////////////////////////////////////////////////////

Plants=[]
Master_Guages=[]
Master_Guages_tempory_list=[]
Locations=[['Plant K','Oven 1','40.00','80.00']]
locations_list=[]
Selected_Master_Guage_Details=['','','','']

def Location_page (Home_page_name,button_no):

  global Active_Window # active window is not assigned here to the location window..it is kept as the home window
  global Plants
  global Location_button_no

  Location_button_no = button_no
  Plants=[] #otherwise, if the location window was called more than one time pressing Add_location button the items in the list will be duplicated




  customtkinter.set_default_color_theme("green")

  win_Location = customtkinter.CTk()
  win_Location.geometry("1200x750")
  win_Location.title('Locations')



  Locations_main_frame = customtkinter.CTkFrame(master=win_Location, width=1200, height=750, corner_radius=15)
  Locations_main_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

  plant_frame = customtkinter.CTkFrame(master=Locations_main_frame, width=300, height=300, corner_radius=15)
  plant_frame.place(x=20, y=15)


  Select_plant_name = customtkinter.CTkLabel(master=plant_frame, text='Select the plant', font=('Century Gothic', 12),anchor='n')
  Select_plant_name.place(x=20, y=10)

  Plants_drop = customtkinter.CTkOptionMenu(master=plant_frame,values=[''])
  Plants_drop.place(x=20,y=50)

  try:
    conn = sqlite3.connect('Databases/Plants.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM locations")
    Plant_records = c.fetchall()


    for each_record in Plant_records:
      Plants.append(each_record[0])

    Plants_drop.configure(values=Plants)
    Plants_drop.set(Plants[0])

  except:
    pass

  Remove_plant_button = customtkinter.CTkButton(master=plant_frame, width=100, text='Remove Plant', corner_radius=6,command=lambda: Delete_Plant(Plants_drop.get()) )
  Remove_plant_button.place(x=20, y=100)

  Update_plant_button = customtkinter.CTkButton(master=plant_frame, width=100, text='Update Locations', corner_radius=6,command=lambda: show_records(Plants_drop.get()))
  Update_plant_button.place(x=150, y=100)

  Select_plant_name = customtkinter.CTkLabel(master=plant_frame, text='Add a new plant', font=('Century Gothic', 12),anchor='n')
  Select_plant_name = customtkinter.CTkLabel(master=plant_frame, text='Add a new plant', font=('Century Gothic', 12),anchor='n')
  Select_plant_name.place(x=20, y=150)

  Plant_name_Entry= customtkinter.CTkEntry(master=plant_frame, width=200)
  Plant_name_Entry.place(x=20, y=200)

  Add_Plant_button = customtkinter.CTkButton(master=plant_frame, width=100, text='Add Plant', corner_radius=6,command=lambda:Create_DB(Plant_name_Entry.get()) )
  Add_Plant_button.place(x=150, y=250)


  position_frame = customtkinter.CTkFrame(master=Locations_main_frame, width=300, height=420, corner_radius=15)
  position_frame.place(x=20, y=320)

  Place_name_l = customtkinter.CTkLabel(master=position_frame, text='Add a new Position', font=('Century Gothic', 12),anchor='n')
  Place_name_l.place(x=20, y=20)


  Place_name_l = customtkinter.CTkLabel(master=position_frame, text='Place :', font=('Century Gothic', 12), anchor='n')
  Place_name_l .place(x=20, y=50)

  Place_Entry = customtkinter.CTkEntry(master=position_frame, width=200)
  Place_Entry.place(x=80, y=50)

  Equipment_number_l = customtkinter.CTkLabel(master=position_frame, text='Equipment number :', font=('Century Gothic', 12), anchor='n')
  Equipment_number_l .place(x=20, y=90)

  Equipment_number_Entry=customtkinter.CTkEntry(master=position_frame, width=120)
  Equipment_number_Entry.place(x=160, y=90)


  Range_l = customtkinter.CTkLabel(master=position_frame, text='Range :', font=('Century Gothic', 12), anchor='n')
  Range_l.place(x=20, y=130)


  Loc_range_start_Entry = customtkinter.CTkEntry(master=position_frame, width=60)
  Loc_range_start_Entry.place(x=80, y=130)

  Place_name_l = customtkinter.CTkLabel(master=position_frame, text='To', font=('Century Gothic', 12), anchor='n')
  Place_name_l.place(x=160, y=130)

  Loc_range_to_Entry = customtkinter.CTkEntry(master=position_frame, width=60)
  Loc_range_to_Entry.place(x=210, y=130)

  Least_count_l = customtkinter.CTkLabel(master=position_frame, text='Least Count', font=('Century Gothic', 12), anchor='n')
  Least_count_l.place(x=20, y=170)

  Least_count_Entry = customtkinter.CTkEntry(master=position_frame, width=100)
  Least_count_Entry.place(x=160, y=170)

  Accuracy_l = customtkinter.CTkLabel(master=position_frame, text='Accuracy', font=('Century Gothic', 12), anchor='n')
  Accuracy_l.place(x=20, y=210)

  Accuracy_Entry = customtkinter.CTkEntry(master=position_frame, width=100)
  Accuracy_Entry.place(x=160, y=210)

  Expiry_Date_l = customtkinter.CTkLabel(master=position_frame, text='Expiry Date', font=('Century Gothic', 12), anchor='n')
  Expiry_Date_l.place(x=20, y=250)

  Expiry_Date_Entry = customtkinter.CTkEntry(master=position_frame, width=100)
  Expiry_Date_Entry.place(x=160, y=250)

  Calib_Freq_l = customtkinter.CTkLabel(master=position_frame, text='Calibration Frequency', font=('Century Gothic', 12), anchor='n')
  Calib_Freq_l.place(x=20, y=290)

  Calib_Freq_Entry = customtkinter.CTkEntry(master=position_frame, width=100)
  Calib_Freq_Entry.place(x=160, y=290)

  Purchase_Date_l = customtkinter.CTkLabel(master=position_frame, text='Date of Purchase', font=('Century Gothic', 12), anchor='n')
  Purchase_Date_l.place(x=20, y=330)

  Purchase_Date_Entry = customtkinter.CTkEntry(master=position_frame, width=100)
  Purchase_Date_Entry.place(x=160, y=330)

  add_location_button = customtkinter.CTkButton(master=position_frame, width=100, text='Add a Location',corner_radius=6, command=lambda:  database(Plants_drop.get()))
  add_location_button.place(x=150, y=370)


  select_location_button = customtkinter.CTkButton(master=Locations_main_frame, width=100, text='Select Location', corner_radius=6, command=lambda :select_button())
  select_location_button.place(x=720, y=650)

  remove_location_button = customtkinter.CTkButton(master=Locations_main_frame, width=100, text='Remove Location', corner_radius=6,command=lambda:  dlt_table(Plants_drop.get()))
  remove_location_button.place(x=840, y=650)


  def dlt_table(plant_name):
    global authorization_password

    Password_authorization_window('Enter Permission to Remove the Location',win_Location)



    if authorization_password=='user':

      conn = sqlite3.connect('Databases/'+plant_name+'.db')
      c = conn.cursor()
      location_to_delete=(locations_list[radio_var.get()-1])[1]

      c.execute("DELETE from locations where place = '"+location_to_delete+"'")
      conn.commit()
      conn.close()

      authorization_password='Colombo10'

    else:
      Print_Error_Window("Invalid Password or No password entered. Function Terminated !",win_Location)



  def Delete_Plant(plant_name):

    global authorization_password
    Password_authorization_window('Enter Permission to Remove the Plant', win_Location)

    if authorization_password=='user':
      conn = sqlite3.connect('Databases/Plants.db')
      c = conn.cursor()
      c.execute("DELETE from locations where plant = '"+plant_name+"'")
      conn.commit()
      conn.close()

      if os.path.exists('Databases/'+plant_name+'.db'):


        os.remove('Databases/'+plant_name+'.db')

      ################# when a plant is deleted it should be remove from the display in the drop down at the same time########################################

      conn_plant= sqlite3.connect('Databases/Plants.db')
      c_plant=conn_plant.cursor()

      c_plant.execute("SELECT *, oid FROM locations")
      Plant_records = c_plant.fetchall()

      Plants.clear()  # clear the plants list first otherwise already loaded items at the begining of the window will be repeated
      for each_record in Plant_records:
        Plants.append(each_record[0])

      Plants_drop.configure(values=Plants)

      if len(Plants)>0:
        Plants_drop.set(Plants[len(Plants) - 1])  #////////////////////////////////////////////////////////////////////////////////////

      elif len(Plants)==0:
        Plants_drop.set("")

      authorization_password = 'Colombo10'

    else:
      Print_Error_Window("Invalid Password or No password entered. Function Terminated !",win_Location)

  def Create_DB(plant_name):

    global authorization_password
    Password_authorization_window('Enter Permission to Add Plant', win_Location)

    if authorization_password=='user':

      conn_plant= sqlite3.connect('Databases/Plants.db')

      c_plant=conn_plant.cursor()

      c_plant.execute("""CREATE TABLE IF NOT EXISTS locations(
                 plant text)""")

      c_plant.execute("INSERT INTO locations VALUES (:plant)",
                  {
                    'plant': plant_name
                  }

                  )

        ################# when a new plant is added it should be displayed in the drop down at the same time########################################
      c_plant.execute("SELECT *, oid FROM locations")
      Plant_records = c_plant.fetchall()

      Plants.clear() # clear the plants list first otherwise already loaded items at the begining of the window will be repeated
      for each_record in Plant_records:
        Plants.append(each_record[0])

      Plants_drop.configure(values=Plants)
      Plants_drop.set(Plants[len(Plants)-1])#######################################################################################################



      conn_plant.commit()
      conn_plant.close()



      conn_location = sqlite3.connect('Databases/'+plant_name+'.db')
      c_location = conn_location.cursor()

      c_location.execute("""CREATE TABLE IF NOT EXISTS locations(
                 plant text,
                 place text,
                 equipment_no text,
                 start_val real,
                 end_val real,
                 least_count text,
                 accuracy text,
                 exp_date text,
                 calib_frequency text,
                 purchase_date text
                 )""")

      conn_location.commit()
      conn_location.close()

      Plant_name_Entry.delete(0,END)#clear the text insdie the name you enetered as the new plant name
      authorization_password = 'Colombo10'

    else:
      Print_Error_Window("Invalid Password or No password entered. Function Terminated !", win_Location)

  def database(plant_name):

    global authorization_password
    Password_authorization_window('Enter Permission to Add Location',win_Location)

    if authorization_password=='user':

      conn= sqlite3.connect('Databases/'+plant_name+'.db')

      c=conn.cursor()

      c.execute("INSERT INTO locations VALUES (:plant, :place, :equipment_no, :start_val, :end_val, :least_count, :accuracy, :exp_date, :calib_frequency, :purchase_date)",
                {
                  'plant': Plants_drop.get(),
                  'place': Place_Entry.get(),
                  'equipment_no': Equipment_number_Entry.get(),
                  'start_val': float(Loc_range_start_Entry.get()),
                  'end_val' : float(Loc_range_to_Entry.get()),
                  'least_count': Least_count_Entry.get(),
                  'accuracy': Accuracy_Entry.get(),
                  'exp_date': Expiry_Date_Entry.get(),
                  'calib_frequency': Calib_Freq_Entry.get(),
                  'purchase_date': Purchase_Date_Entry.get()


                }

                )
        # plant text
        #place text
        #start_val real
        # end_val real

      conn.commit()
      conn.close()
      authorization_password = 'Colombo10'

    else:
      Print_Error_Window("Invalid Password or No password entered. Function Terminated !", win_Location)

  radio_var = customtkinter.IntVar(value=1)



  def show_records(plant_name):


    database_frame = customtkinter.CTkScrollableFrame(master=Locations_main_frame, width=835, height=550, corner_radius=15)
    database_frame.place(x=325, y=30)



    Select_menu_l = customtkinter.CTkLabel(master=database_frame, text='Select', font=('Century Gothic', 12), anchor='w')

    Select_menu_l.grid(row=0,column=0,padx=5,sticky='w',columnspan=2)
    Equipment_No_menu_l = customtkinter.CTkLabel(master=database_frame, text='Equipment No', font=('Century Gothic', 12), anchor='w')
    Equipment_No_menu_l.grid(row=0, column=2, padx=5, sticky='w')

    Range_start_menu_l = customtkinter.CTkLabel(master=database_frame, text='Range Start', font=('Century Gothic', 12), anchor='w')

    Range_start_menu_l.grid(row=0, column=3, padx=5,sticky='w')
    Range_end_menu_l = customtkinter.CTkLabel(master=database_frame, text='Range End', font=('Century Gothic', 12), anchor='w')

    Range_end_menu_l.grid(row=0, column=4, padx=5,sticky='w')
    Least_count_menu_l = customtkinter.CTkLabel(master=database_frame, text='Least Count', font=('Century Gothic', 12), anchor='w')
    Least_count_menu_l.grid(row=0, column=5, padx=5,sticky='w')
    Accuracy_menu_l = customtkinter.CTkLabel(master=database_frame, text='Accuracy', font=('Century Gothic', 12), anchor='w')
    Accuracy_menu_l.grid(row=0, column=6, padx=5,sticky='w')
    Expiry_date_menu_l = customtkinter.CTkLabel(master=database_frame, text='Expiry Date', font=('Century Gothic', 12), anchor='w')
    Expiry_date_menu_l.grid(row=0, column=7, padx=5,sticky='w')
    Calib_Freq_menu_l = customtkinter.CTkLabel(master=database_frame, text='Calibration Frequency', font=('Century Gothic', 12), anchor='w')
    Calib_Freq_menu_l.grid(row=0, column=8, padx=5,sticky='w')
    Purchase_date_menu_l = customtkinter.CTkLabel(master=database_frame, text='Purchase Date', font=('Century Gothic', 12), anchor='w')
    Purchase_date_menu_l.grid(row=0, column=9, padx=5,sticky='w')

    global locations_list

    try:
      conn= sqlite3.connect('Databases/'+plant_name+'.db')

      c=conn.cursor()

      c.execute("SELECT *, oid FROM locations")
      records=c.fetchall()
      locations_list=records



      Y=60
      row_no=1
      radio_button_value=1

      for position in records:
        radio_button= customtkinter.CTkRadioButton(master=database_frame, text=position[1], value=radio_button_value,variable= radio_var,command=lambda: Select_place())

        radio_button.grid(row=row_no, column=0, padx=5,sticky='w',columnspan=2)

        Equipment_No_db = customtkinter.CTkLabel(master=database_frame, text=position[2],font=('Century Gothic', 14), anchor='w')

        Equipment_No_db.grid(row=row_no, column=2, padx=5,sticky='n')

        Range_start_db = customtkinter.CTkLabel(master=database_frame, text=position[3],font=('Century Gothic', 14), anchor='w')

        Range_start_db.grid(row=row_no, column=3, padx=5,sticky='n')
        Range_end_db = customtkinter.CTkLabel(master=database_frame, text=position[4], font=('Century Gothic', 14),anchor='w')

        Range_end_db.grid(row=row_no, column=4, padx=5,sticky='n')

        Least_count_db = customtkinter.CTkLabel(master=database_frame, text=position[5], font=('Century Gothic', 14),anchor='w')
        Least_count_db.grid(row=row_no, column=5, padx=5, sticky='n')
        Accuracy_db = customtkinter.CTkLabel(master=database_frame, text=position[6], font=('Century Gothic', 14),anchor='w')
        Accuracy_db.grid(row=row_no, column=6, padx=5, sticky='n')
        Expire_Date_db = customtkinter.CTkLabel(master=database_frame, text=position[7], font=('Century Gothic', 14),anchor='w')
        Expire_Date_db.grid(row=row_no, column=7, padx=5, sticky='n')
        Calib_Freq_db = customtkinter.CTkLabel(master=database_frame, text=position[8], font=('Century Gothic', 14),anchor='w')
        Calib_Freq_db.grid(row=row_no, column=8, padx=5, sticky='n')
        Purchase_date_db = customtkinter.CTkLabel(master=database_frame, text=position[9], font=('Century Gothic', 14),anchor='w')
        Purchase_date_db.grid(row=row_no, column=9, padx=5, sticky='n')

        Y+=40
        row_no+=1
        radio_button_value+=1
    except:
      pass

    conn.commit()
    conn.close()


  def Select_place():
    global selected_from_location_window
    global selected_place
    global selected_plant
    global start_temp
    global end_temp
    global range_init
    global selected_accuracy
    global selected_equipment

    start_temp = (locations_list[radio_var.get() - 1])[3]
    end_temp = (locations_list[radio_var.get() - 1])[4]

    if Location_button_no==1:
      selected_from_location_window[0][0]=(locations_list[radio_var.get()-1])[0]
      selected_from_location_window[0][1]= str((locations_list[radio_var.get()-1])[1])
      selected_from_location_window[0][2]=(locations_list[radio_var.get()-1])[2]
      selected_from_location_window[0][3]=(locations_list[radio_var.get()-1])[6]
    elif Location_button_no==2:
      selected_from_location_window[1][0]=(locations_list[radio_var.get()-1])[0]
      selected_from_location_window[1][1]= str((locations_list[radio_var.get()-1])[1])
      selected_from_location_window[1][2]=(locations_list[radio_var.get()-1])[2]
      selected_from_location_window[1][3]=(locations_list[radio_var.get()-1])[6]
    elif Location_button_no==3:
      selected_from_location_window[2][0]=(locations_list[radio_var.get()-1])[0]
      selected_from_location_window[2][1]= str((locations_list[radio_var.get()-1])[1])
      selected_from_location_window[2][2]=(locations_list[radio_var.get()-1])[2]
      selected_from_location_window[2][3]=(locations_list[radio_var.get()-1])[6]
    elif Location_button_no==4:
      selected_from_location_window[3][0]=(locations_list[radio_var.get()-1])[0]
      selected_from_location_window[3][1]= str((locations_list[radio_var.get()-1])[1])
      selected_from_location_window[3][2]=(locations_list[radio_var.get()-1])[2]
      selected_from_location_window[3][3]=(locations_list[radio_var.get()-1])[6]
    elif Location_button_no==5:
      selected_from_location_window[4][0]=(locations_list[radio_var.get()-1])[0]
      selected_from_location_window[4][1]= str((locations_list[radio_var.get()-1])[1])
      selected_from_location_window[4][2]=(locations_list[radio_var.get()-1])[2]
      selected_from_location_window[4][3]=(locations_list[radio_var.get()-1])[6]
    elif Location_button_no==6:
      selected_from_location_window[5][0]=(locations_list[radio_var.get()-1])[0]
      selected_from_location_window[5][1]= str((locations_list[radio_var.get()-1])[1])
      selected_from_location_window[5][2]=(locations_list[radio_var.get()-1])[2]
      selected_from_location_window[5][3]=(locations_list[radio_var.get()-1])[6]
    elif Location_button_no==7:
      selected_from_location_window[6][0]=(locations_list[radio_var.get()-1])[0]
      selected_from_location_window[6][1]= str((locations_list[radio_var.get()-1])[1])
      selected_from_location_window[6][2]=(locations_list[radio_var.get()-1])[2]
      selected_from_location_window[6][3]=(locations_list[radio_var.get()-1])[6]



  def select_button():
    global Active_Window
    Active_Window.destroy() #active window is still Home window and it will be destroyed
    Active_Window=win_Location # since the Active-window is assigned to be closed when Home_page opens, win_Location should be assigned as the Active_window
    Home_page()




  win_Location.mainloop()




#////////////////////////////////////////////---- MASTER GUAGE WINDOW -------/////////////////////////////////////////////////////////////////////////////////

Adding_Master_Guage_List=[]
def Master_Guage_page ():

  global Active_Window # active window is not assigned here to the location window..it is kept as the home window


  customtkinter.set_default_color_theme("green")
  win_Master = customtkinter.CTk()
  win_Master.geometry("1200x800")
  win_Master.title('Master Guages')



  Master_main_frame = customtkinter.CTkFrame(master=win_Master, width=1200, height=800, corner_radius=15)
  Master_main_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

  add_new_master_background_frame = customtkinter.CTkFrame(master=Master_main_frame, width=660, height=770, corner_radius=15)
  add_new_master_background_frame.place(x=20, y=10)
  add_new_master_background_bottom_frame = customtkinter.CTkFrame(master=Master_main_frame, width=500, height=180, corner_radius=0)
  add_new_master_background_bottom_frame.place(x=675, y=600)

  New_master_l = customtkinter.CTkLabel(master=add_new_master_background_frame, text='Add a new Master Guage', font=('Century Gothic', 16), anchor='n')
  New_master_l.place(x=20, y=10)

  Master_From_l = customtkinter.CTkLabel(master=add_new_master_background_frame, text='From', font=('Century Gothic', 12), anchor='n')
  Master_From_l.place(x=20, y=50)

  Master_From_Entry = customtkinter.CTkEntry(master=add_new_master_background_frame, width=60)
  Master_From_Entry.place(x=70, y=50)

  Master_From_l = customtkinter.CTkLabel(master=add_new_master_background_frame, text='To', font=('Century Gothic', 12),anchor='n')
  Master_From_l.place(x=140, y=50)

  Master_To_Entry = customtkinter.CTkEntry(master=add_new_master_background_frame, width=60)
  Master_To_Entry.place(x=160, y=50)

  Master_by_l = customtkinter.CTkLabel(master=add_new_master_background_frame, text='by', font=('Century Gothic', 12),anchor='n')
  Master_by_l.place(x=270, y=50)

  Master_by_Entry = customtkinter.CTkEntry(master=add_new_master_background_frame, width=60)
  Master_by_Entry.place(x=310, y=50)

  add_master_button = customtkinter.CTkButton(master=add_new_master_background_frame, width=100, text='Update Range',corner_radius=6,command=lambda: Set_master_details_table(Master_From_Entry.get(),Master_To_Entry.get(),Master_by_Entry.get()))
  add_master_button.place(x=450, y=50)



  Master_location_l = customtkinter.CTkLabel(master=add_new_master_background_bottom_frame, text='Master Location', font=('Century Gothic', 12),anchor='n')
  Master_location_l.place(x=20, y=30)

  Master_entry_Location = customtkinter.CTkEntry(master=add_new_master_background_bottom_frame, width=120, placeholder_text='GL/DL')
  Master_entry_Location.place(x=140, y=30)

  customtkinter.set_default_color_theme("dark-blue")
  Master_Submit_button = customtkinter.CTkButton(master=add_new_master_background_bottom_frame, width=100, text='Submit New Master Guage',corner_radius=6,command=lambda: Create_DB_MG(Master_entry_Location.get()))
  Master_Submit_button.place(x=290, y=80)
  customtkinter.set_default_color_theme("green")


  Master_Trace_l = customtkinter.CTkLabel(master=add_new_master_background_bottom_frame, text='Tracerbility', font=('Century Gothic', 12),anchor='n')
  Master_Trace_l.place(x=20, y=80)

  Master_entry_Trace = customtkinter.CTkEntry(master=add_new_master_background_bottom_frame, width=120, placeholder_text='GL/DL')
  Master_entry_Trace.place(x=140, y=80)

  Master_Cert_l = customtkinter.CTkLabel(master=add_new_master_background_bottom_frame, text='Certificate No', font=('Century Gothic', 12),anchor='n')
  Master_Cert_l.place(x=20, y=130)

  Master_entry_Cert = customtkinter.CTkEntry(master=add_new_master_background_bottom_frame, width=120, placeholder_text='GL/DL')
  Master_entry_Cert.place(x=140, y=130)




  Update_master_guages_list_button = customtkinter.CTkButton(master=Master_main_frame, width=150, text='Update Master Guages List',corner_radius=6,command=lambda: Update_Master_Scroll_frame())
  Update_master_guages_list_button.place(x=850, y=80)

  Select_master_guages_button = customtkinter.CTkButton(master=Master_main_frame, width=150, text='Select Master Guage',corner_radius=6,command=lambda: Select_master_guage())
  Select_master_guages_button.place(x=865, y=430)
  customtkinter.set_default_color_theme("dark-blue")
  Remove_master_guage_button = customtkinter.CTkButton(master=Master_main_frame, width=150, text='Remove Guage',corner_radius=6,command=lambda : Delete_Master_Guage())
  Remove_master_guage_button.place(x=865, y=480)
  customtkinter.set_default_color_theme("green")



  def Set_master_details_table(start_val, end_val,by_val ):

    global Adding_Master_Guage_List
    Adding_Master_Guage_List=[]

    add_new_master_table_frame = customtkinter.CTkFrame(master=add_new_master_background_frame, width=610, height=650,corner_radius=15)
    add_new_master_table_frame.place(x=20, y=100)

    start_val=float(start_val)
    end_val=float(end_val)
    by_val=float(by_val)

    Table_menu_Set_Temp = customtkinter.CTkLabel(master=add_new_master_table_frame, text='Set_Temp', font=('Century Gothic', 12),anchor='n')
    Table_menu_Set_Temp.place(x=20, y=20)
    Table_menu_Mean_ref_Temp = customtkinter.CTkLabel(master=add_new_master_table_frame, text='Ref_Mean_Temp', font=('Century Gothic', 12),anchor='n')
    Table_menu_Mean_ref_Temp.place(x=130, y=20)
    Table_menu_Mean_uut_Temp = customtkinter.CTkLabel(master=add_new_master_table_frame, text='Mean_UUT_Temp', font=('Century Gothic', 12),anchor='n')
    Table_menu_Mean_uut_Temp.place(x=240, y=20)
    Table_menu_error_Temp = customtkinter.CTkLabel(master=add_new_master_table_frame, text='Error', font=('Century Gothic', 12),anchor='n')
    Table_menu_error_Temp.place(x=350, y=20)
    Table_menu_unceratinity = customtkinter.CTkLabel(master=add_new_master_table_frame, text='Uncertainity (k=2)', font=('Century Gothic', 12),anchor='n')
    Table_menu_unceratinity .place(x=460, y=20)


    no_of_vals=((end_val-start_val)/by_val)+2

    X=20
    Y=70
    vertical_gap=(540-Y)/(no_of_vals-1)



    for i in range(0, int(no_of_vals)):
      Adding_Master_One_Raw = []

      update_master_entry_Set = customtkinter.CTkEntry(master=add_new_master_table_frame, width=80)
      update_master_entry_Set.place(x=X, y=Y)
      update_master_entry_Set.insert(0,start_val)
      Adding_Master_One_Raw.append(update_master_entry_Set)
      update_master_entry_Ref = customtkinter.CTkEntry(master=add_new_master_table_frame, width=80)
      update_master_entry_Ref.place(x=X+120, y=Y)
      Adding_Master_One_Raw.append(update_master_entry_Ref)
      update_master_entry_uut = customtkinter.CTkEntry(master=add_new_master_table_frame, width=80)
      update_master_entry_uut.place(x=X+240, y=Y)
      Adding_Master_One_Raw.append(update_master_entry_uut)
      update_master_entry_error = customtkinter.CTkEntry(master=add_new_master_table_frame, width=80)
      update_master_entry_error.place(x=X+360, y=Y)
      Adding_Master_One_Raw.append(update_master_entry_error)
      update_master_entry_uncertainity = customtkinter.CTkEntry(master=add_new_master_table_frame, width=80)
      update_master_entry_uncertainity.place(x=X+480, y=Y)
      Adding_Master_One_Raw.append(update_master_entry_uncertainity)

      start_val+=by_val
      Y+=vertical_gap
      Adding_Master_Guage_List.append(Adding_Master_One_Raw)

    add_master_error_button = customtkinter.CTkButton(master=Master_main_frame, width=100, text='Calculate error',corner_radius=6,command=lambda:Calculate_error())
    add_master_error_button.place(x=360, y=700)

  def Calculate_error ():
    for raws in Adding_Master_Guage_List:
      try:
        error=float(raws[2].get())-float(raws[1].get())
        raws[3].delete(0, END)
        raws[3].insert(0, error)
      except:
        pass


  radio_var = customtkinter.IntVar(value=1) # this is needed for the radio buttons


  def Create_DB_MG(plant_name):

    global authorization_password

    Password_authorization_window('Enter Permission to Add the Master Guage', win_Master)

    if authorization_password=='user':

      conn_location = sqlite3.connect('Databases/'+'Master_Guages/'+plant_name+'.db')
      c_location = conn_location.cursor()

      c_location.execute("""CREATE TABLE IF NOT EXISTS guage_details(
               Set_temp text,
               Ref_Mean_temp real,
               Mean_uut_temp real,
               error real,
               Uncertainity text
               )""")

      Master_entry_Location.delete(0,END)#clear the text insdie the name you enetered as the new plant name

      sum_error_into_mean_uut=0
      sum_uut=0

      for raws in Adding_Master_Guage_List:

        sum_error_into_mean_uut+=(float(raws[3].get())*float(raws[2].get()))

        sum_uut+=float(raws[2].get())


        c_location.execute("INSERT INTO guage_details VALUES (:Set_temp, :Ref_Mean_temp, :Mean_uut_temp, :error, :Uncertainity)",
                  {
                    'Set_temp': (raws[0].get()),
                    'Ref_Mean_temp': float(raws[1].get()),
                    'Mean_uut_temp' : float(raws[2].get()),
                    'error': float(raws[3].get()),
                    'Uncertainity': (raws[4].get())

                  }

                  )

      conn_location.commit()
      conn_location.close()


      conn_guage= sqlite3.connect('Databases/Master_Guages.db')

      c_guage=conn_guage.cursor()

      c_guage.execute("""CREATE TABLE IF NOT EXISTS guages(guage text,error real,tracerbility text,certificate text)""")



      mean_error=round((sum_error_into_mean_uut/sum_uut),2)

      c_guage.execute("INSERT INTO guages VALUES (:guage,:error,:tracerbility,:certificate)",
                {
                  'guage': plant_name,
                  'error': mean_error,
                  'tracerbility': 'WAGA CALIBRATION (PVT) LTD',
                  'certificate': 'SALTH/00129/22'

                }
                )

      ################# when a new plant is added it should be displayed in the drop down at the same time########################################
      c_guage.execute("SELECT *, oid FROM guages")
      Master_Guage_records = c_guage.fetchall()

      conn_guage.commit()
      conn_guage.close()


      authorization_password='Colombo10'

    else:
      Print_Error_Window("Invalid Password or No password entered. Function Terminated !", win_Master)

  def Update_Master_Scroll_frame():
    global Master_Guages_tempory_list
    master_database_frame = customtkinter.CTkScrollableFrame(master=Master_main_frame, width=450, height=200, corner_radius=15)
    master_database_frame.place(x=700,y=130)

    Select_menu_l = customtkinter.CTkLabel(master=master_database_frame, text='Location', font=('Century Gothic', 12), anchor='w')
    Select_menu_l.grid(row=0,column=0,padx=5,sticky='w',columnspan=2)
    Mean_error_menu_l = customtkinter.CTkLabel(master=master_database_frame, text='Mean Error', font=('Century Gothic', 12), anchor='w')
    Mean_error_menu_l.grid(row=0, column=2, padx=5, sticky='w')
    Trace_menu_l = customtkinter.CTkLabel(master=master_database_frame, text='Tracerbility', font=('Century Gothic', 12), anchor='w')
    Trace_menu_l.grid(row=0, column=3, padx=5, sticky='w',columnspan=3)
    Certificate_menu_l = customtkinter.CTkLabel(master=master_database_frame, text='Certificate No', font=('Century Gothic', 12), anchor='w')
    Certificate_menu_l.grid(row=0, column=6, padx=5, sticky='w')

    conn_fetch = sqlite3.connect('Databases/' + 'Master_Guages' + '.db')
    c_fetch = conn_fetch.cursor()  # this is the place
    c_fetch.execute("SELECT *, oid FROM guages")
    records = c_fetch.fetchall()
    Master_Guages_tempory_list=records


    row_no = 1
    radio_button_value = 1

    for position in records:
      master_radio_button = customtkinter.CTkRadioButton(master=master_database_frame, text=position[0], value=radio_button_value,variable=radio_var)
      master_radio_button.grid(row=row_no, column=0, padx=5, sticky='w', columnspan=2)

      error_scroll = customtkinter.CTkLabel(master=master_database_frame, text=position[1], font=('Century Gothic', 12),anchor='w')
      error_scroll.grid(row=row_no, column=2, padx=5, sticky='n')

      trace_scroll = customtkinter.CTkLabel(master=master_database_frame, text=position[2], font=('Century Gothic', 10),anchor='w')
      trace_scroll.grid(row=row_no, column=3, padx=5, sticky='n',columnspan=3)

      Certificate_no_scroll = customtkinter.CTkLabel(master=master_database_frame, text=position[3], font=('Century Gothic', 10),anchor='w')
      Certificate_no_scroll.grid(row=row_no, column=6, padx=5, sticky='n')

      row_no+=1
      radio_button_value+=1

    conn_fetch.commit()
    conn_fetch.close()

  try:
    Update_Master_Scroll_frame()#To update the scroll window in the begining og the window
  except:
    pass

  def Delete_Master_Guage():

    global authorization_password

    Password_authorization_window('Enter Permission to Remove the Master Guage', win_Master)

    if authorization_password=='user':
      conn = sqlite3.connect('Databases/Master_Guages.db')
      c = conn.cursor()

      location_to_delete=(Master_Guages_tempory_list[radio_var.get()-1])[0]

      c.execute("DELETE from guages where guage = '"+location_to_delete+"'")

      conn.commit()
      conn.close()

      if os.path.exists('Databases/Master_Guages/'+location_to_delete+'.db'):
        os.remove('Databases/Master_Guages/'+location_to_delete+'.db')

      ################# when a plant is deleted it should be remove from the display in the drop down at the same time########################################

      conn_plant= sqlite3.connect('Databases/Master_Guages.db')
      c_plant=conn_plant.cursor()

      c_plant.execute("SELECT *, oid FROM guages")
      Plant_records = c_plant.fetchall()

      Master_Guages.clear()  # clear the plants list first otherwise already loaded items at the begining of the window will be repeated
      for each_record in Plant_records:
        Master_Guages.append(each_record[0])
      authorization_password='Colombo10'
    else:
      Print_Error_Window("Invalid Password or No password entered. Function Terminated !", win_Master)

  def Select_master_guage():
    global Selected_Master_Guage_Details
    global Master_Guages_tempory_list

    Selected_Master_Guage_Details[0] = (Master_Guages_tempory_list[radio_var.get() - 1])[0]
    Selected_Master_Guage_Details[1] = (Master_Guages_tempory_list[radio_var.get() - 1])[1]
    Selected_Master_Guage_Details[2] = (Master_Guages_tempory_list[radio_var.get() - 1])[2]
    Selected_Master_Guage_Details[3] = (Master_Guages_tempory_list[radio_var.get() - 1])[3]

    global Active_Window
    Active_Window.destroy() #active window is still Home window and it will be destroyed
    Active_Window=win_Master
    Home_page()


  win_Master.mainloop()

def Password_authorization_window(text,master_win):
  global authorization_password
  win_password_auth = Toplevel(master=master_win,bg="black")
  win_password_auth.geometry("420x300")
  win_password_auth.title('Permission Required')



  Password_l1 = customtkinter.CTkLabel(master=win_password_auth, text="Enter the Password", font=('Century Gothic', 17),text_color=("black","lightgray"))
  Password_l1.place(relx=0.5, rely=0.25,anchor= CENTER)
  Password_Entry = customtkinter.CTkEntry(master=win_password_auth, font=('Century Gothic', 17))
  Password_Entry.place(relx=0.5, rely=0.5,anchor= CENTER)
  Function_button = customtkinter.CTkButton(master=win_password_auth, width=220, text=text,corner_radius=6,command=lambda:closing_func())
  Function_button.place(relx=0.5, rely=0.75,anchor= CENTER)



  def closing_func():
    global authorization_password

    authorization_password=Password_Entry.get()
    win_password_auth.destroy()

  win_password_auth.grab_set()
  master_win.wait_window(win_password_auth)






app.mainloop()













