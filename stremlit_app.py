import streamlit as st
import pandas as pd
import numpy as np
#import plotly.express as px
from urllib.request import urlopen
import json
import matplotlib.pyplot as plt
st.title('Antenna radiation pattern calculator (Калькулятор диаграмм направленности антенн)')
ln_type = st.radio("Choose your language (Выберите свой язык):", ('English', 'Русский'))
if ln_type == 'Русский':
    an_type = st.radio("Выберите тип антенны:", ('Horn', 'Dipole', 'Patch'))
    if an_type == 'Horn':
        st.write('Введите ширину антенны "a" в метрах, высоту антенны "b" в метрах и длину волны "wl" в метрах:')
        width = st.number_input('a', 0.0, None)
        height = st.number_input('b', 0.0, None)
        wave_length = st.number_input('l', 0.0, None)

    if an_type == 'Dipole':
        st.write('Введите длину диполя "l" в метрах и длину волны "wl" в метрах:')
        dipole_length = st.number_input('l', 0.0, None)
        wave_length = st.number_input('wl', 0.0, None)

        theta = np.arange(0.001, 2 * np.pi, 0.001)
        fig, ax = plt.subplots(subplot_kw=dict(projection="polar"))

        def dipole_diagram(wl, l):
            f = (np.cos(np.pi * (dipole_length / wave_length) * np.cos(theta)) - np.cos(
                (dipole_length / wave_length) * np.pi)) / (np.sin(theta))
            norm = f.max()
            dipole_diagram = 20 * np.log((f / norm) ** 2)
            return dipole_diagram


        ax.plot(theta, dipole_diagram)
        ax.set_theta_zero_location('N')
        ax.set_rlabel_position(-90)
        plt.thetagrids(range(0, 360, 30))

        st.pyplot(fig)

    if an_type == 'Patch':
        st.write('Введите параметр "w" и длину волны "wl" в метрах:')
        parameter = st.number_input('w', 0.0, None)
        wave_length = st.number_input('wl', 0.0, None)
if ln_type == 'English':
    an_type = st.radio("Choose your antenna type:", ('Horn', 'Dipole', 'Patch'))
    if an_type == 'Horn':
        st.write('Enter antenna width "a" in meters, antenna height "b" in meters and wave length "wl" in meters:')
        width = st.number_input('a', 0.0, None)
        height = st.number_input('b', 0.0, None)
        wave_length = st.number_input('l', 0.0, None)

    if an_type == 'Dipole':
        st.write('Enter dipole length "l" in meters and wave length "wl" in meters:')
        dipole_length = st.number_input('l', 0.0, None)
        wave_length = st.number_input('wl', 0.0, None)

        theta = np.arange(0.001, 2 * np.pi, 0.001)
        fig, ax = plt.subplots(subplot_kw=dict(projection="polar"))


        def dipole_diagram(wl, l):
            f = (np.cos(np.pi * (dipole_length / wave_length) * np.cos(theta)) - np.cos(
                (dipole_length / wave_length) * np.pi)) / (np.sin(theta))
            norm = f.max()
            dipole_diagram = 20 * np.log((f / norm) ** 2)
            return dipole_diagram

        ax.plot(theta, dipole_diagram)
        ax.set_theta_zero_location('N')
        ax.set_rlabel_position(-90)
        plt.thetagrids(range(0, 360, 30))

        st.pyplot(fig)

    if an_type == 'Patch':
        st.write('Enter parameter "w" and wave length "wl" in meters:')
        parameter = st.number_input('w', 0.0, None)
        wave_length = st.number_input('wl', 0.0, None)
