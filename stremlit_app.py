import streamlit as st
import numpy as np

with st.echo(code_location='below'):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(subplot_kw=dict(projection="polar"))
    theta = np.arange(0.01, 2 * np.pi, 0.01)


    def dipole_diagram(p):
        f = 20 * np.log(((np.cos(np.pi * p * np.cos(theta)) - np.cos(p * np.pi)) / (np.sin(theta))) ** 2)
        return f


    length = 1
    while length:
        length = 0.5 #float(input("Введите безразмерный параметр l/lambda: "))
        ax.plot(theta, dipole_diagram(length))
    st.write(fig)


