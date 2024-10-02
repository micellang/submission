import pandas as pd
import matplotlib.pyplot as plt
import math
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

#Membuat helper function 
def create_predict_weather(df) :
    weatherPredict = df.groupby(by=['yr', 'weathersit']).agg({
    "cnt": "mean"
    })
    weatherPredict.columns = ["Rata-rata Penyewa"] #Memberi nama variabel yang ditampilkan
    weatherPredict["Tahun"] = weatherPredict.index.get_level_values('yr')
    weatherPredict['Tahun'] = weatherPredict['Tahun'].replace({0: 2011, 1: 2012})
    weatherPredict["Cuaca"] = weatherPredict.index.get_level_values('weathersit')
    return weatherPredict

def create_predict_holiday(df):
    holidayPredict = df.groupby(by=['yr', 'mnth', 'holiday']).agg({
    "instant": "nunique", #Menampilkan jumlah hari libur/tidak libur
    "cnt": "sum" #Menampilkan jumlah penyewa sepeda
    })
    holidayPredict.columns = ["Jumlah Hari", "Jumlah penyewa"] #Memberi nama variabel yang ditampilkan
    holidayPredict["Tahun"] = holidayPredict.index.get_level_values('yr') #Bisa menampilkan year pada kolom berbeda
    holidayPredict['Tahun'] = holidayPredict['Tahun'].replace({0: 2011, 1: 2012})
    holidayPredict["Bulan"] = holidayPredict.index.get_level_values('mnth') #Bisa menampilkan month pada kolom berbeda
    holidayPredict["Libur"] = holidayPredict.index.get_level_values('holiday') #Bisa menampilkan holiday pada kolom berbeda
    holidayPredict["Libur"] = holidayPredict["Libur"].replace({0: "Tidak Libur", 1: "Libur"})
    holidayPredict["average_rents"] = (holidayPredict["Jumlah penyewa"] / holidayPredict["Jumlah Hari"]).apply(math.floor)
    return holidayPredict

def create_predict_season(df):
    df['Musim'] = pd.cut(df['season'], bins=[0, 1, 2, 3, 4], labels=['Spring', 'Summer', 'Fall', 'Winter'])
    season = df.groupby('Musim')['cnt'].agg(['count', 'mean'])
    season.columns = ['Jumlah Hari', 'Rata-rata Penyewaan']
    return season



#Membaca data yang sudah dibersihkan
dfDay = pd.read_csv("dataDay.csv")

#Mengubah data menjadi dateTime
date_column = ["dteday"]
dfDay.sort_values(by="dteday", inplace=True) #Mengurutkan dataframe berdasarkan tanggal (ascending order)
dfDay.reset_index(inplace=True) 
for column in date_column:
    dfDay[column] = pd.to_datetime(dfDay[column])
    
#Menyimpan min dan max date dari dataFrame
minimumDate = dfDay["dteday"].min()
maximumDate = dfDay["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://img.freepik.com/free-vector/bike-sharing-abstract-concept-illustration_335657-3741.jpg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=minimumDate,
        max_value=maximumDate,
        value=[minimumDate, maximumDate]
    )

#Membuat dataframe yang difilter dengan tanggal
main_df = dfDay[(dfDay["dteday"] >= str(start_date)) & 
                (dfDay["dteday"] <= str(end_date))]

#Menyimpan hasil perhitungan function untuk visualisasi berdasarkan tanggal yang dipilih
weather_df = create_predict_weather(main_df)
holiday_df= create_predict_holiday(main_df)
season_df  = create_predict_season(main_df)


#Design DashBoard
st.header('Bike Sharing DashBoard :sparkles:')

st.subheader('Average Bike Sharing based on Weather')
 
sns.set(style="white") 

plt.figure(figsize=(10, 6)) 

palette_col = ["#00B2FF","#94B3C4", "#93E7FB"] 

sns.barplot(x='Tahun', y='Rata-rata Penyewa', hue='Cuaca', data=weather_df, palette=palette_col) 

plt.title('Rata-rata Penyewa Sepeda per Tahun Berdasarkan Cuaca', fontsize=14) 
plt.xlabel('Tahun', fontsize=12) 
plt.ylabel('Rata-rata Penyewa', fontsize=12) 
plt.legend(title='Kondisi Cuaca') 
plt.tight_layout()

# Menampilkan plot di Streamlit
st.pyplot(plt.gcf()) 



st.subheader('Average Bike Sharing based on Holiday')

start_year = start_date.year
end_year = end_date.year

# Menampilkan plot berdasarkan rentang tahun yang dipilih
if start_year == 2011 and end_year == 2011:
    # Hanya tampilkan plot untuk tahun 2011
    sns.set(style="white")
    plt.figure(figsize=(12, 6))
    dataLibur = holiday_df[(holiday_df["Libur"] == "Libur") & (holiday_df["Tahun"] == 2011)]
    dataTidakLibur = holiday_df[(holiday_df["Libur"] == "Tidak Libur") & (holiday_df["Tahun"] == 2011)]
    plt.plot(dataLibur['Bulan'], dataLibur['average_rents'], marker='o', color='blue', label='Libur')
    plt.plot(dataTidakLibur['Bulan'], dataTidakLibur['average_rents'], marker='o', color='red', label='Tidak Libur')
    plt.title('Rata-rata Penyewa Sepeda per Bulan dan Status Libur/Tidak Libur tahun 2011', fontsize=16)
    plt.xlabel('Bulan', fontsize=12)
    plt.ylabel('Rata-rata Penyewa', fontsize=12)
    plt.legend(title='Status Libur')
    plt.tight_layout()
    st.pyplot(plt.gcf())

elif start_year == 2012 and end_year == 2012:
    # Hanya tampilkan plot untuk tahun 2012
    sns.set(style="white")
    plt.figure(figsize=(12, 6))
    dataLibur = holiday_df[(holiday_df["Libur"] == "Libur") & (holiday_df["Tahun"] == 2012)]
    dataTidakLibur = holiday_df[(holiday_df["Libur"] == "Tidak Libur") & (holiday_df["Tahun"] == 2012)]
    plt.plot(dataLibur['Bulan'], dataLibur['average_rents'], marker='o', color='blue', label='Libur')
    plt.plot(dataTidakLibur['Bulan'], dataTidakLibur['average_rents'], marker='o', color='red', label='Tidak Libur')
    plt.title('Rata-rata Penyewa Sepeda per Bulan dan Status Libur/Tidak Libur tahun 2012', fontsize=16)
    plt.xlabel('Bulan', fontsize=12)
    plt.ylabel('Rata-rata Penyewa', fontsize=12)
    plt.legend(title='Status Libur')
    plt.tight_layout()
    st.pyplot(plt.gcf())

elif start_year == 2011 and end_year == 2012:
    # Tampilkan kedua plot
    
    # Plot untuk tahun 2011
    sns.set(style="white")
    plt.figure(figsize=(12, 6))
    dataLibur = holiday_df[(holiday_df["Libur"] == "Libur") & (holiday_df["Tahun"] == 2011)]
    dataTidakLibur = holiday_df[(holiday_df["Libur"] == "Tidak Libur") & (holiday_df["Tahun"] == 2011)]
    plt.plot(dataLibur['Bulan'], dataLibur['average_rents'], marker='o', color='blue', label='Libur')
    plt.plot(dataTidakLibur['Bulan'], dataTidakLibur['average_rents'], marker='o', color='red', label='Tidak Libur')
    plt.title('Rata-rata Penyewa Sepeda per Bulan dan Status Libur/Tidak Libur tahun 2011', fontsize=16)
    plt.xlabel('Bulan', fontsize=12)
    plt.ylabel('Rata-rata Penyewa', fontsize=12)
    plt.legend(title='Status Libur')
    plt.tight_layout()
    st.pyplot(plt.gcf())

    # Plot untuk tahun 2012
    sns.set(style="white")
    plt.figure(figsize=(12, 6))
    dataLibur = holiday_df[(holiday_df["Libur"] == "Libur") & (holiday_df["Tahun"] == 2012)]
    dataTidakLibur = holiday_df[(holiday_df["Libur"] == "Tidak Libur") & (holiday_df["Tahun"] == 2012)]
    plt.plot(dataLibur['Bulan'], dataLibur['average_rents'], marker='o', color='blue', label='Libur')
    plt.plot(dataTidakLibur['Bulan'], dataTidakLibur['average_rents'], marker='o', color='red', label='Tidak Libur')
    plt.title('Rata-rata Penyewa Sepeda per Bulan dan Status Libur/Tidak Libur tahun 2012', fontsize=16)
    plt.xlabel('Bulan', fontsize=12)
    plt.ylabel('Rata-rata Penyewa', fontsize=12)
    plt.legend(title='Status Libur')
    plt.tight_layout()
    st.pyplot(plt.gcf())

st.subheader('Average Bike Sharing based on Seasonal')
plt.figure(figsize=(8, 6)) #Mengatur ukuran plot dari grafik

palette_col = ["#FFFF00","#40E0D0", "#B55119", "#CDB0EE"]
sns.barplot(x=season_df.index, y=season_df['Rata-rata Penyewaan'], hue=season_df.index, palette=palette_col, legend=False)

# Menambahkan judul dan label sumbu
plt.title('Rata-rata Penyewaan Sepeda Berdasarkan Musim', fontsize=16)
plt.xlabel('Kondisi Musim', fontsize=12)
plt.ylabel('Rata-rata Penyewaan Sepeda', fontsize=12)

# Menampilkan visualisasi
plt.tight_layout()
plt.show()
st.pyplot(plt.gcf())
