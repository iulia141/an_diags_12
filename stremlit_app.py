import streamlit as st
import pandas as pd
import numpy as np
#import plotly.express as px
from urllib.request import urlopen
import json
import matplotlib.pyplot as plt
st.title('Калькулятор диаграмм направленности антенн')
an_type = st.radio("Choose your antenna type (выберите тип антенны):", ('Horn', 'Dipole', 'Patch'))
if an_type == 'Horn':
    st.write('Введите ширину антенны "a", высоту антенны "b" и длину волны "wl":')
    width = st.number_input('a', 0, None)
    height = st.number_input('b', 0, None)
    wave_length = st.number_input('l', 0, None)
if an_type == 'Dipole':
    st.write('Введите длину диполя "l" и длину волны "wl":')
    dipole_length = st.number_input('l', 0, None)
    wave_length = st.number_input('wl', 0, None)
if an_type == 'Patch':
    st.write('Введите параметр "w" и длину волны "wl":')
    parameter = st.number_input('w', 0, None)
    wave_length = st.number_input('wl', 0, None)
theta = np.arange(0.01, 2 * np.pi, 0.01)
fig, ax = plt.subplots(subplot_kw=dict(projection="polar"))

def dipole_diagram(wl, l):
    f = 20 * np.log(((np.cos(np.pi * (wl/l) * np.cos(theta)) - np.cos((wl/l) * np.pi)) / (np.sin(theta))) ** 2)
    return f

length = 1
while length:
    length = float(input("Введите безразмерный параметр l/lambda: "))
    ax.plot(theta, dipole_diagram(length))
    ax.set_theta_zero_location('N')
    ax.set_rlabel_position(-90)
    plt.thetagrids(range(0, 360, 30))

st.pyplot(fig)