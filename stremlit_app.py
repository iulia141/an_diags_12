import math
import streamlit as st
import pandas as pd
import numpy as np
import sympy as sym
#import plotly.express as px
#from urllib.request import urlopen
import json
import matplotlib.pyplot as plt
st.title('Antenna radiation pattern calculator (Калькулятор диаграмм направленности антенн)')
ln_type = st.radio("Choose your language (Выберите свой язык):", ('English', 'Русский'))

if ln_type == 'Русский':
    an_type = st.radio("Выберите тип антенны:", ('Рупорная антенна', 'Дипольная антенна', 'Патч-антенна'))

    if an_type == 'Рупорная антенна':
        st.write('Введите ширину антенны "a" в метрах, высоту антенны "b" в метрах и частоту волны "frc" в мегагерцах:')
        a = st.number_input('a', 0.0, None)
        b = st.number_input('b', 0.0, None)
        frc = st.number_input('frc', 0.0, None)
        frc = frc * 1000000
        if a > 0 and b > 0 and frc > 0:

            c = 299792458
            l = c / frc
            k = 2 * np.pi / l
            st.write('Диаграмма направленности для рупорной антенны')

            theta = np.arange(-np.pi / 2, np.pi / 2, 0.0005)
            fig, ax = plt.subplots()
            fE = 20 * np.log(
                ((1 + np.cos(theta)) / 2) * ((np.sin(b * k * np.sin(theta))) / (k * b * np.sin(theta) / 2)))
            fH = 20*np.log(np.pi**2/8*(1+np.cos(theta))*
                           (np.cos(k*a/2*np.sin(theta)))/(np.pi**2/4-(k*a/2*np.sin(theta))**2))

            plt.axis([-np.pi / 2, np.pi / 2, -80, 10])
            ax.plot(theta, fE)
            ax.plot(theta, fH)
            st.pyplot(fig)

            st.write('Введите высоту рупора антенны "b1" в метрах:')
            b1 = st.number_input('b1', 0.0, None)
            De = 32 * a * b1 / np.pi / l / l
            st.write("Направленность антенны равна " + De)

        else:
            st.write('Неверно введены данные')

    if an_type == 'Дипольная антенна':
        st.write('Введите длину диполя "l" в метрах и длину волны "wl" в метрах:')
        dipole_length = st.number_input('l', 0.0, None)
        wave_length = st.number_input('wl', 0.0, None)
        if dipole_length > 0 and wave_length > 0:
            theta = np.arange(0.001, 2 * np.pi, 0.001)
            fig, ax = plt.subplots(subplot_kw=dict(projection="polar"))

            st.write('Диаграмма направленности для дипольной антенны')

            f = (np.cos(np.pi * (dipole_length / wave_length) * np.cos(theta)) - np.cos(
                (dipole_length / wave_length) * np.pi)) / (np.sin(theta))
            norm = f.max()
            dipole_diagram = 20 * np.log((f / norm) ** 2)

            ax.plot(theta, dipole_diagram)
            ax.set_theta_zero_location('N')
            ax.set_rlabel_position(-90)
            plt.thetagrids(range(0, 360, 30))

            st.pyplot(fig)

            x = sym.Symbol('x')
            C = 0.5772
            Cikl = sym.integrate(sym.cos(x)/x, (x, 0, 2*np.pi*dipole_length/wave_length))
            Ci2kl = sym.integrate(sym.cos(x)/x, (x, 0, 4*np.pi*dipole_length/wave_length))
            Sikl = sym.integrate(sym.sin(x)/x, (x, 0, 2*np.pi*dipole_length/wave_length))
            Si2kl = sym.integrate(sym.sin(x)/x, (x, 0, 4*np.pi*dipole_length/wave_length))
            Q = (C + np.log(2 * np.pi * dipole_length / wave_length) - Cikl + 0.5 *
                 np.sin(2 * np.pi * dipole_length / wave_length) *
                 (Si2kl - 2 * Sikl) + 0.5 * np.cos(2 * np.pi * dipole_length / wave_length) *
                 (C + np.log(np.pi * dipole_length / wave_length) + Ci2kl - 2 * Cikl))
            D = 2 * norm / Q
            D = float(D)
            D = str(D)
            st.write("Направленность антенны равна " + D)
        else:
            st.write('Неверно введены данные')

    if an_type == 'Патч-антенна':
        st.write('Введите параметр "w" и длину волны "wl" в метрах:')
        parameter = st.number_input('w', 0.0, None)
        wave_length = st.number_input('wl', 0.0, None)
        if wave_length > 0:
            pass
        else:
            st.write('Неверно введены данные')

if ln_type == 'English':
    an_type = st.radio("Choose your antenna type:", ('Horn', 'Dipole', 'Patch'))

    if an_type == 'Horn':
        st.write('Enter antenna width "a" in meters, antenna height "b" in meters '
                 'and wave frequency "frc" in megahertz:')

        a = st.number_input('a', 0.0, None)
        b = st.number_input('b', 0.0, None)
        frc = st.number_input('frc', 0.0, None)
        frc = frc * 1000000
        if a > 0 and b > 0 and frc > 0:

            c = 299792458
            l = c / frc
            k = 2 * np.pi / l
            st.write('Radiation pattern for horn antenna')

            theta = np.arange(-np.pi / 2, np.pi / 2, 0.0005)
            fig, ax = plt.subplots()
            fE = 20 * np.log(
                ((1 + np.cos(theta)) / 2) * ((np.sin(b * k * np.sin(theta))) / (k * b * np.sin(theta) / 2)))
            fH = 20 * np.log(np.pi ** 2 / 8 * (1 + np.cos(theta)) *
                             (np.cos(k * a / 2 * np.sin(theta))) / (np.pi ** 2 / 4 - (k * a / 2 * np.sin(theta)) ** 2))

            plt.axis([-np.pi / 2, np.pi / 2, -80, 10])
            ax.plot(theta, fE)
            ax.plot(theta, fH)
            st.pyplot(fig)

            st.write('Enter antenna horn height "b1" in meters:')
            b1 = st.number_input('b1', 0.0, None)
            De = 32*a*b1/np.pi/l/l
            st.write("Antenna directivity is equal " + De)

        else:
            st.write('Incorrect data entered')

    if an_type == 'Dipole':
        st.write('Enter dipole length "l" in meters and wave length "wl" in meters:')
        dipole_length = st.number_input('l', 0.0, None)
        wave_length = st.number_input('wl', 0.0, None)
        if dipole_length > 0 and wave_length > 0:
            theta = np.arange(0.001, 2 * np.pi, 0.001)
            fig, ax = plt.subplots(subplot_kw=dict(projection="polar"))

            st.write('Radiation pattern for dipole antenna')

            f = (np.cos(np.pi * (dipole_length / wave_length) * np.cos(theta)) - np.cos(
                (dipole_length / wave_length) * np.pi)) / (np.sin(theta))
            norm = f.max()
            dipole_diagram = 20 * np.log((f / norm) ** 2)

            ax.plot(theta, dipole_diagram)
            ax.set_theta_zero_location('N')
            ax.set_rlabel_position(-90)
            plt.thetagrids(range(0, 360, 30))

            st.pyplot(fig)

            x = sym.Symbol('x')
            C = 0.5772
            Cikl = sym.integrate(sym.cos(x) / x, (x, 0, 2 * np.pi * dipole_length / wave_length))
            Ci2kl = sym.integrate(sym.cos(x) / x, (x, 0, 4 * np.pi * dipole_length / wave_length))
            Sikl = sym.integrate(sym.sin(x) / x, (x, 0, 2 * np.pi * dipole_length / wave_length))
            Si2kl = sym.integrate(sym.sin(x) / x, (x, 0, 4 * np.pi * dipole_length / wave_length))
            Q = (C + np.log(2 * np.pi * dipole_length / wave_length) - Cikl + 0.5 *
                 np.sin(2 * np.pi * dipole_length / wave_length) *
                 (Si2kl - 2 * Sikl) + 0.5 * np.cos(2 * np.pi * dipole_length / wave_length) *
                 (C + np.log(np.pi * dipole_length / wave_length) + Ci2kl - 2 * Cikl))
            D = 2 * f.max() / Q
            D = float(D)
            D = str(D)
            st.write("Antenna directivity is equal " + D)
        else:
            st.write('Incorrect data entered')

    if an_type == 'Patch':
        st.write('Enter parameter "w" and wave length "wl" in meters:')
        parameter = st.number_input('w', 0.0, None)
        wave_length = st.number_input('wl', 0.0, None)
        if wave_length > 0:
            pass
        else:
            st.write('Incorrect data entered')
