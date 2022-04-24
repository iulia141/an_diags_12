import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from urllib.request import urlopen
import json
st.title('Калькулятор диаграмм направленности антенн')
an_type = st.radio("Choose your antenna type (выберите тип антенны):", ('Horn', 'Dipole', 'Patch'))
if an_type == 'Horn':
    st.write('Введите ширину антенны "a", высоту антенны "b" и длину волны:')
    width = st.number_input('a', 0, None)
    height = st.number_input('b', 0, None)
    wave_length = st.number_input('l', 0, None)
