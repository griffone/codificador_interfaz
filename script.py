import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from tkinter import PhotoImage
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def nrz(bit_sequence):
    return ''.join(['0' if bit == '0' else '1' for bit in bit_sequence])

def nrz_l(bit_sequence):
    return ''.join(['1' if bit == '0' else '0' for bit in bit_sequence])

def nrz_i(bit_sequence):
    current_level = '1'
    encoded_sequence = ''

    for bit in bit_sequence:
        if bit == '1':
            current_level = '1' if current_level == '0' else '0'
        encoded_sequence += current_level

    return encoded_sequence

def manchester(bit_sequence):
    return ''.join(['01' if bit == '0' else '10' for bit in bit_sequence])

def manchester_differential(bit_sequence):
    current_level = '1'
    encoded_sequence = ''

    for bit in bit_sequence:
        if bit == '0':
            current_level = '1' if current_level == '0' else '0'
        encoded_sequence += current_level + ('1' if current_level == '0' else '0')

    return encoded_sequence

def rz(bit_sequence):
    encoded_sequence = ''
    for bit in bit_sequence:
        if bit == '0':
            encoded_sequence += '0N'
        else:
            encoded_sequence += '1N'
    return encoded_sequence

def ami(bit_sequence):
    encoded_sequence = ''
    current_polarity = '1'
    for bit in bit_sequence:
        if bit == '0':
            encoded_sequence += '0'
        else:
            encoded_sequence += current_polarity
            current_polarity = '1' if current_polarity == 'N' else 'N'
    return encoded_sequence

def pseudoternary(bit_sequence):
    encoded_sequence = ''
    current_polarity = '1'
    for bit in bit_sequence:
        if bit == '1':
            encoded_sequence += '0'
        else:
            encoded_sequence += current_polarity
            current_polarity = '1' if current_polarity == 'N' else 'N'
    return encoded_sequence

def hdb3(bit_sequence):
    encoded_sequence = ''
    current_polarity = '1'
    zero_count = 0
    one_count = 0

    for bit in bit_sequence:
        if bit == '1':
            encoded_sequence += current_polarity
            current_polarity = '1' if current_polarity == 'N' else 'N'
            one_count += 1
            zero_count = 0
        else:
            zero_count += 1
            if zero_count == 4:
                if one_count % 2 == 0:
                    encoded_sequence = encoded_sequence[:-3] + current_polarity + '00' + current_polarity
                else:
                    encoded_sequence += current_polarity
                zero_count = 0
                one_count = 0
            else:
                encoded_sequence += '0'

    return encoded_sequence

def b8zs(bit_sequence):
    encoded_sequence = ''
    current_polarity = '1'
    zero_count = 0

    for bit in bit_sequence:
        if bit == '1':
            encoded_sequence += current_polarity
            current_polarity = '1' if current_polarity == 'N' else 'N'
            zero_count = 0
        else:
            zero_count += 1
            if zero_count == 8:
                encoded_sequence = encoded_sequence[:-7] + current_polarity + '0' + ('1' if current_polarity == 'N' else 'N') + '00' + current_polarity + '0' + ('1' if current_polarity == 'N' else 'N')
                zero_count = 0
            else:
                encoded_sequence += '0'

    return encoded_sequence

def plot_signal(signal, title):
    plt.figure()
    plt.step(range(len(signal)), signal, where='post')
    plt.title(title)
    plt.ylim(-0.5, 1.5)
    plt.show()

def generate_graph():
    bit_sequence = input_sequence.get()
    encoding = encoding_combobox.get()

    if encoding == "Sin codificación":
        plot_signal([int(bit) for bit in bit_sequence], "Sin codificación")
    elif encoding == "NRZ":
        plot_signal([int(bit) for bit in nrz(bit_sequence)], "NRZ")
    elif encoding == "NRZ-L":
        plot_signal([int(bit) for bit in nrz_l(bit_sequence)], "NRZ-L")
    elif encoding == "NRZ-I":
        plot_signal([int(bit) for bit in nrz_i(bit_sequence)], "NRZ-I")
    elif encoding == "Manchester":
        plot_signal([int(bit) for bit in manchester(bit_sequence)], "Manchester")
    elif encoding == "Manchester Diferencial":
        plot_signal([int(bit) for bit in manchester_differential(bit_sequence)], "Manchester Diferencial")
    elif encoding == "RZ":
        plot_signal([0 if bit == '0' else (1 if bit == '1' else 0.5) for bit in rz(bit_sequence)], "RZ")
    elif encoding == "AMI":
        plot_signal([0 if bit == '0' else (1 if bit == '1' else 0.5) for bit in ami(bit_sequence)], "AMI")
    elif encoding == "Pseudoternario":
        plot_signal([0 if bit == '0' else (1 if bit == '1' else 0.5) for bit in pseudoternary(bit_sequence)], "Pseudoternario")
    elif encoding == "HDB3":
        plot_signal([0 if bit == '0' else (1 if bit == '1' else 0.5) for bit in hdb3(bit_sequence)], "HDB3")
    elif encoding == "B8ZS":
        plot_signal([0 if bit == '0' else (1 if bit == '1' else 0.5) for bit in b8zs(bit_sequence)], "B8ZS")

root = tk.Tk()
root.title("Gráfico de Secuencia de Bits")
root.geometry("370x270")
root.resizable(False, False)

title_label = ttk.Label(root, text="Codificación de señales", font=("Helvetica", 14, "bold"))
title_label.grid(row=0, column=0, sticky="w", pady=10, padx=10)

input_frame = ttk.Frame(root, padding="10")
input_frame.grid(row=1, column=0, sticky="w")

input_label = ttk.Label(input_frame, text="Introduce la secuencia de bits:")
input_label.pack(side="left")

input_sequence = ttk.Entry(input_frame, width=int(30))
input_sequence.pack(side="left")

encoding_frame = ttk.Frame(root, padding="10")
encoding_frame.grid(row=2, column=0, sticky="w")

encoding_label = ttk.Label(encoding_frame, text="Selecciona el método de codificación:")
encoding_label.pack(side="left")

encoding_combobox = ttk.Combobox(encoding_frame, values=("Sin codificación", "NRZ", "NRZ-L", "NRZ-I", "Manchester", "Manchester Diferencial", "RZ", "AMI", "Pseudoternario", "HDB3", "B8ZS"), state="readonly", width=int(20))
encoding_combobox.current(0)
encoding_combobox.pack(side="left")

generate_button = ttk.Button(root, text="Generar gráfico", command=generate_graph)
generate_button.grid(row=3, column=0, sticky="w", pady=10, padx=10)

logo_image = PhotoImage(file="logo.png")
logo_image = logo_image.subsample(2, 2)
logo_label = ttk.Label(root, image=logo_image)
logo_label.grid(row=4, column=0, sticky="w", pady=10, padx=10)

root.mainloop()
