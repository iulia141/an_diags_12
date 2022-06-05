import math
import streamlit as st
import pandas as pd
import numpy as np
import sympy as sym
import json
import matplotlib.pyplot as plt
c = 299792458

def hornPlot_and_D(a, b, frc):
    frc = frc * 10 ** 6
    c = 299792458
    l = c / frc
    k = 2 * np.pi / l
    theta = np.arange(-np.pi, np.pi, np.pi/36000)
    fig, ax = plt.subplots()
    fE = 20 * np.log10(
        ((1 + np.cos(theta)) / 2) * ((np.sin(b * k / 2 * np.sin(theta))) / (k * b * np.sin(theta) / 2)))

    fH = 20 * np.log10(
        np.pi ** 2 / 8 * (1 + np.cos(theta))
        * np.cos(k * a / 2 * np.sin(theta)) /
        ((np.pi / 2) ** 2 - (k * a / 2 * np.sin(theta)) ** 2))

    plt.axis([-np.pi / 2, np.pi / 2, -80, 10])
    ax.plot(theta, fE, label='%s' % lang_switcher[i][5])
    ax.plot(theta, fH, label='%s' % lang_switcher[i][6])
    ax.set_title('%s' % lang_switcher[i][7], loc='center')
    ax.set_ylabel('Magnitude, dB')
    ax.set_xlabel('Theta, rad')
    ax.legend()

    col2.pyplot(fig)

    De = 32 * a * b1 / np.pi / l / l
    return De

def hornWidthH(frc,a):
    l = c / frc
    return [172*l/a,67*l/a]
def hornWidthE(frc,b):
    l = c / frc
    return [115*l/b,51*l/b]

def dipolPlot(wave_length,dipole_length):
    theta = np.arange(np.pi / 360, 2 * np.pi, np.pi / 360)
    fig = plt.figure()
    ax = fig.add_subplot(projection='polar')

    f = (np.cos(np.pi * (dipole_length / wave_length) * np.cos(theta)) - np.cos(
        (dipole_length / wave_length) * np.pi)) / (np.sin(theta))
    norm = f.max()
    dipole_diagram = 20 * np.log10((f / norm) ** 2)

    ax.plot(theta, dipole_diagram)
    ax.set_theta_zero_location('N')
    ax.set_rlabel_position(-120)
    plt.thetagrids(range(0, 360, 30))
    ax.set_xlabel('Theta, degrees')
    ax.set_title('%s' % lang_switcher[i][11], loc='center')
    col2.pyplot(fig)
    return f


def dipolDirect(f):
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
    return float(D)


def patchPlot(parameter, wave_length):
    fig, ax = plt.subplots(subplot_kw=dict(projection="polar"))
    k = 2 * np.pi / wave_length
    theta = np.arange(0, np.pi, np.pi / 100)
    f = ((np.sin((0.5 * k * parameter) * np.cos(theta)) / np.cos(theta)) ** 2) * ((np.sin(theta)) ** 3)
    norm = f.max()
    patch_diagram = 20 * np.log10(f / norm)
    ax.plot(theta, patch_diagram)
    ax.set_rlabel_position(-45)
    ax.set_title('%s' % lang_switcher[i][13], loc='center')
    col2.pyplot(fig)


def pathcDirect(parameter,wave_length):
    k = 2 * np.pi / wave_length
    X = k * parameter
    x = sym.Symbol('x')
    SiX = sym.integrate(sym.sin(x) / x, (x, 0, X))
    I1 = -2 + sym.cos(X) + X * SiX + sym.sin(X) / X
    return ((2 * np.pi * parameter / wave_length) ** 2) / I1


st.set_page_config(page_title="Antenna radiation pattern calculator", layout="wide",  menu_items={
         'Report a bug': "https://github.com/iulia141/an_diags_12.git",
         'About': " This calculator is made by students Necliudov Egor, Zakharov Ivan & Timankova Iuliia from New Phystech, ITMO, in 2022"
     })
st.title('Antenna radiation pattern calculator')
st.title('(Калькулятор диаграмм направленности антенн)')

ln_type = st.selectbox("Choose your language (Выберите свой язык): ",
                       ['English', 'Русский'])

lang_switcher = [["Выберите тип антенны:",
                  ['Рупорная антенна', 'Дипольная антенна', 'Патч-антенна'],
                  'Введите ширину pупора "a" в метрах, высоту рупора "b" в метрах и частоту волны "frc" в мегагерцах:',
                  'Введите высоту волновода "b1" в метрах:',
                  'Рассчитать диаграмму направленности',
                  'E-плоскость',
                  'H-плоскость',
                  'Диаграмма направленности для рупорной антенны',
                  "Направленность антенны равна ",
                  'Неверно введены данные! Пожалуйста, убедитесь, что введенные величины положительные и постройте диаграмму еще раз.',
                  'Введите длину диполя "l" в метрах и длину волны "wl" в метрах:',
                  'Диаграмма направленности для дипольной антенны',
                  'Введите параметр "w" и длину волны "wl" в метрах:',
                  'Диаграмма направленности для патч-антенны',
                  'Ширина диаграммы направленности нулевого уровня H:   ',
                  'Ширина диаграммы направленности по уровню половинной мощности H:  ',
                  'Ширина диаграммы направленности нулевого уровня F:   ',
                  'Ширина диаграммы направленности по уровню половинной мощности F:   '],
                 ["Choose your antenna type:",
                  ['Horn', 'Dipole', 'Patch'],
                  'Enter antenna width "a" in meters, antenna height "b" in meters and wave frequency "frc" in megahertz:',
                  'Enter antenna waveguide height "b1" in meters:',
                  'Calculate radiation pattern',
                  'E-plane',
                  'H-plane',
                  'Radiation pattern for horn antenna',
                  "Antenna directivity is equal ",
                  'Incorrect data entered! Please, make sure that all the input parameters are positive and restart calculation.',
                  'Enter dipole length "l" in meters and wave length "wl" in meters:',
                  'Radiation pattern for dipole antenna',
                  'Enter parameter "w" and wave length "wl" in meters:',
                  'Radiation pattern for patch antenna',
                  'Zero beamwidth H',
                  'Half power beamwidth H',
                  'Zero beamwidth F',
                  'Half power beamwidth F']]
#ДОПИСАТЬ АНГЛИЙСКИЕ НАЗВАНИЯ ШИРИНЫ ДИАГРАММ 
i = 0
if ln_type == 'Русский':
    i = 0
elif ln_type == 'English':
    i = 1

an_type = st.radio("%s" % lang_switcher[i][0], ('%s' % lang_switcher[i][1][0], '%s' % lang_switcher[i][1][1], '%s' % lang_switcher[i][1][2]))

col1, col2 = st.columns(2)

if an_type == 'Рупорная антенна' or an_type == 'Horn':

    col1.subheader("%s" % lang_switcher[i][2])
    a = col1.number_input('a, m', 0.0, None,1.0)
    b = col1.number_input('b, m', 0.0, None,1.0)
    frc = col1.number_input('frc, MHz', 0.0, None,1000.0)

    from PIL import Image
    image = Image.open("horn_ant.png")

    col1.subheader('%s' % lang_switcher[i][3])
    col1.image(image, width=350)

    b1 = col1.number_input('b1, m', 0.0, None,1.0)


    if col1.button('%s' % lang_switcher[i][4]) and a > 0 and b > 0 and frc > 0:

        De = str(hornPlot_and_D(a, b, frc))
        col2.subheader('%s' % lang_switcher[i][8] + De)
        WH=hornWidthH(frc,a)
        col2.subheader('%s' % lang_switcher[i][14] + str(WH[0]))
        col2.subheader('%s' % lang_switcher[i][15] + str(WH[1]))
        WE = hornWidthE(frc, b)
        col2.subheader('%s' % lang_switcher[i][16] + str(WE[0]))
        col2.subheader('%s' % lang_switcher[i][17] + str(WE[1]))

    else:
        st.warning('%s' % lang_switcher[i][9])


elif an_type == 'Дипольная антенна' or an_type == 'Dipole':

    col1.subheader('%s' % lang_switcher[i][10])
    dipole_length = col1.number_input('l, m', 0.0, None,1.0)
    wave_length = col1.number_input('wl, m', 0.0, None,1.0)

    if col1.button('%s' % lang_switcher[i][4]) and dipole_length > 0 and wave_length > 0:

        f = dipolPlot(wave_length, dipole_length)
        D = str(dipolDirect(f))
        col1.subheader('%s' % lang_switcher[i][8] + D)

    else:
        st.warning('%s' % lang_switcher[i][9])

elif an_type == 'Патч-антенна' or an_type == 'Patch':

    col1.write(lang_switcher[i][11])
    parameter = col1.number_input('w, m', 0.0, None, 1.0)
    wave_length = col1.number_input('wl, m', 0.0, None, 1.0)
    if col1.button('%s' % lang_switcher[i][4]) and wave_length > 0:
        patchPlot(parameter, wave_length)
        D0 = str(pathcDirect(parameter, wave_length))
        col1.subheader('%s' % lang_switcher[i][8] + D0)
    else:
        st.warning('%s' % lang_switcher[i][9])
