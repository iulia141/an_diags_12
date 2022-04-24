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
    st.write('Введите ширину антенны "a" в метрах, высоту антенны "b" в метрах и длину волны "wl" в метрах:')
    width = st.number_input('a', 0.0, float)
    height = st.number_input('b', 0.0, float)
    wave_length = st.number_input('l', 0.0, float)

if an_type == 'Dipole':
    st.write('Введите длину диполя "l" в метрах и длину волны "wl" в метрах:')
    dipole_length = st.number_input('l', 0.0, float)
    wave_length = st.number_input('wl', 0.0, float)

    theta = np.arange(0.01, 2 * np.pi, 0.01)
    fig, ax = plt.subplots(subplot_kw=dict(projection="polar"))

    def dipole_diagram(wl, l):
        f = 20 * np.log(((np.cos(np.pi * (l / wl) * np.cos(theta)) - np.cos((wl / l) * np.pi)) / (np.sin(theta))) ** 2)
        return f

    ax.plot(theta, dipole_diagram(wave_length, dipole_length))
    ax.set_theta_zero_location('N')
    ax.set_rlabel_position(-90)
    plt.thetagrids(range(0, 360, 30))

    st.pyplot(fig)

if an_type == 'Patch':
    st.write('Введите параметр "w" и длину волны "wl" в метрах:')
    parameter = st.number_input('w', 0.0, float)
    wave_length = st.number_input('wl', 0.0, float)
