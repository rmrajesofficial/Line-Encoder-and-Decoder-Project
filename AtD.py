import numpy as np
import matplotlib
from tkinter import ttk
matplotlib.use("TkAgg") 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
ani_list=[]
def exit_application(dtd_root):
    dtd_root.destroy()

def animationCall(fig,ax,type,bitData,x_continuous, y_continuous, sampled_x, sampled_y, quantized_values,quantization_bits,x_binary,binary_output,signal):
    
    if type == 'original':
        ax.clear()
        line, = ax.plot(x_continuous, y_continuous,color='green', label='Continuous Sine Wave')
        
        ax.legend()
        ax.set_title('Step 1: Analog')
        ax.set_xlabel('Time')
        ax.set_ylabel('Amplitude')
        
        def init():
            ax.set_ylim(-1.5, 1.5)
            ax.set_xlim(0,sampled_x[-1]+0.1)
            line.set_data([], [])
            return line,
        def animate(i):
            
            x = x_continuous
            if signal =='cos':
                y = np.cos((i+1)*0.02*x)
            else:
                y = np.sin((i+1)*0.02*x)
            line.set_data(x, y)
            if i==49: ax.scatter(sampled_x, sampled_y, color='red', label='Sampled Points')
            return line,
    elif type == 'quantized':
        ax.clear()
        line,=ax.step(sampled_x, quantized_values, where='post', label='Quantized Levels', color='blue', linestyle='-', marker='o')
        ax.set_title('Step 3: Flat-Top')
        ax.set_xlabel('Time')
        ax.set_ylabel('Quantized Levels')
        cont=0.0015*len(quantized_values)*quantization_bits
        # print('quant value',quantized_values)
        # print('sampled_x',sampled_x)
        def init():
            ax.set_xlim(0, sampled_x[-1]+0.1)
            ax.set_ylim(-1, max(quantized_values)+1)
            return line,
        def animate(i):
            initial=(max(quantized_values)-min(quantized_values))/2
            y = [initial]* len(quantized_values)
            for j in range(len(quantized_values)):
                if quantized_values[j] > initial:
                    k=initial+(i+1)*cont
                    if(k>quantized_values[j]):
                        y[j] =quantized_values[j]
                    else:
                        y[j]=k 
                elif quantized_values[j] < initial:
                    k=initial-(i+1)*cont
                    if(k<quantized_values[j]):
                        y[j] =quantized_values[j]
                    else:
                        y[j]=k 
            x = sampled_x[:len(quantized_values)]
            line.set_data(x, y)
            return line,
    elif type == 'quantized2':
        ax.clear()
        line = ax.stem(sampled_x, np.sin(sampled_x), linefmt='-', markerfmt='o', basefmt=' ')
        def init():
            ax.set_xlim(0, sampled_x[-1]+0.1)
            ax.set_ylim(-1.25, max(quantized_values)+1.25)
            return line,
        def animate(i):
            ax.cla()
            ax.set_title('Step 2: PAM')
            ax.set_xlabel('Time')
            ax.set_ylabel('Quantized Levels')
            ax.set_xlim(0, sampled_x[-1]+0.1)
            if signal =='cos':
                y_values = np.cos(sampled_x*i*0.02)
            else:
                y_values = np.sin(sampled_x*i*0.02)
            ax.axhline(y=0, linestyle='-')
            line = ax.stem(sampled_x, y_values, linefmt='-', markerfmt='o', basefmt=' ')
            return line,
    
    elif type =='binary':
        ax.clear()
        line, = ax.step(x_binary, binary_output, where='post',color='teal', linestyle='-', marker='o', markersize=4)
        ax.set_title('Step 4: Binary')
        ax.set_xlabel('Index')
        ax.set_ylabel('Value')
        def init():
            ax.set_xlim(0, len(bitData))
            ax.set_ylim(-0.5, 1.5)
            line.set_data([], [])
            return line,
        def animate(i):
            y = [0] * len(bitData)
            
            for j in range(len(bitData)):
                if bitData[j] == 1:
                    y[j] =i*0.02+0.02# Increase the height gradually
            x = np.arange(len(y))
            
            line.set_data(x, y)
            return line,
    ani = animation.FuncAnimation(fig, animate, init_func=init, frames=50, interval=2, repeat=False)
    ani_list.append(ani)


def AtD():
    def submit_form():
        print('running')
        signal=signal_var.get()
        signalBit=bit_var.get()
        signalSample=sample_var.get()
        print('signal: ',signal,'\tBit: ',signalBit,'\tsample: ',signalSample)

        x_continuous = np.linspace(0, 4 * np.pi, signalSample)
        sampled_x = np.linspace(0, 4 * np.pi, signalSample) 
        if signal =='cos':
            y_continuous = np.cos(x_continuous)
            sampled_y = np.cos(sampled_x)
        else:
            y_continuous = np.sin(x_continuous)
            sampled_y = np.sin(sampled_x)
        quantized_values = np.round((sampled_y + 1) * ((2**signalBit - 1) / 2)).astype(int)
        x_binary = np.arange(len(quantized_values) * signalBit)
        binary_output = [int(bit) for val in quantized_values for bit in format(val, f'0{signalBit}b')]
        animationCall(fig,ax[0],'original',None,x_continuous, y_continuous, sampled_x, sampled_y, quantized_values,signalBit,x_binary,binary_output, signal)
        animationCall(fig,ax[3],'binary',binary_output,x_continuous, y_continuous, sampled_x, sampled_y, quantized_values,signalBit,x_binary,binary_output, signal)
        animationCall(fig,ax[2],'quantized',binary_output,x_continuous, y_continuous, sampled_x, sampled_y, quantized_values,signalBit,x_binary,binary_output, signal)
        animationCall(fig,ax[1],'quantized2',binary_output,x_continuous, y_continuous, sampled_x, sampled_y, quantized_values,signalBit,x_binary,binary_output, signal)
        result_string = ','.join(map(str, binary_output))
        out_var.set(result_string)
        out_entry.config(text=out_var.get())
        Quantized_string = ','.join(map(str, quantized_values))
        in_var.set(Quantized_string)
        inp_entry.config(text=in_var.get())
        print(binary_output)
        canvas.draw()
        return

    atd_root = Tk()
    atd_root.geometry('1200x1000')
    atd_root.minsize(1000, 600)
    atd_root.title('Analog to Digital')

    formFrame = Frame(atd_root,width=400)
    formFrame.pack(side=LEFT, fill=BOTH)
    inputFrame=Frame(formFrame,bg='teal')
    inputFrame.pack(side=TOP,fill=BOTH,expand=True)
    
    outputFrame=Frame(formFrame,bg='teal')
    outputFrame.pack(side=BOTTOM,fill=BOTH,expand=True)

    formFrameWidth = 400
    formFrame.configure(width=formFrameWidth)
    
    formFrameWidth = 300
    formFrame.pack_propagate(False)  # Prevent frame from shrinking to its content
    formFrame.config(width=formFrameWidth)

    diagramFrame = Frame(atd_root)
    diagramFrame.pack(side=RIGHT, fill=BOTH,expand=True)

    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True

    in_var = StringVar()
    in_var.set('000000000000000')
    out_var = StringVar()
    out_var.set('000000000000000')


    # Stylish labels and fonts
    input_label = Label(inputFrame, text="Input:", font=("Arial", 30, "bold"), fg="white", bg='teal')
    input_label.pack(side='top', pady=20)

    frame1=Frame(inputFrame,bg='teal')
    frame1.pack(fill=BOTH,pady=10,padx=10)

    signal_label = Label(frame1, text="Enter Signal:", font=("Arial", 18), fg="white", bg='teal')
    signal_label.pack(side=LEFT,padx=20)

    signal = ['sin','cos']
    signal_var = StringVar(frame1)
    signal_var.set(signal[0]) 

    signal_menu = OptionMenu(frame1, signal_var, *signal)
    signal_menu.pack(side='right',padx=10)

    frame2=Frame(inputFrame,bg='teal')
    frame2.pack(fill=BOTH,pady=10,padx=20)

    divider=Frame(outputFrame ,bg='white')
    divider.pack(side='top',fill=BOTH,padx=20)


    sample = [10,20,30,40,50,100,200]
    sample_var = IntVar(frame2)
    sample_var.set(sample[1]) 

    sample_label = Label(frame2, text="Enter sampling rate:",bg='teal',font=("Arial", 18))
    sample_label.pack(side='left',padx=10)

    sample_menu = OptionMenu(frame2, sample_var, *sample)
    sample_menu.pack(side='right',padx=10)

    frame3=Frame(inputFrame,bg='teal')
    frame3.pack(fill=BOTH,pady=10,padx=20)

    bit = [2,3,4,5,6,8]
    bit_var = IntVar(frame3)
    bit_var.set(bit[1]) 

    bit_label = Label(frame3, text="Enter Bit rate:",bg='teal',font=("Arial", 18))
    bit_label.pack(side='left',padx=10)

    bit_menu = OptionMenu(frame3, bit_var, *bit)
    bit_menu.pack(side='right',padx=10)


    input_label = Label(outputFrame, text="Output:", font=("Arial", 30, "bold"), fg="white", bg='teal')
    input_label.pack(side=TOP, pady=20)

    inp_label = Label(outputFrame, text="Quantized Value:",fg="white", bg='teal',font=("Arial", 18))
    inp_label.pack(pady=10)

    inp_entry = Label(outputFrame, text=in_var.get(),bg='white',fg="black",font=("Arial", 20))
    inp_entry.pack(pady=10)

    out_label = Label(outputFrame, text= 'Binary Data:',fg="white", bg='teal',font=("Arial", 18))
    out_label.pack(pady=10)

    out_entry = Label(outputFrame, text=out_var.get(),bg='white',fg="black",font=("Arial", 20))
    out_entry.pack(pady=5)

    submit_button = Button(inputFrame, text="Submit",width=8, height=2, command=lambda: submit_form(),fg='white', font=("Comfortaa", 12), border=0)
    submit_button.pack(pady=20)
    exit_button = Button(outputFrame, text="Exit", command=lambda: exit_application(atd_root),width=8, height=2, fg='white', font=("Comfortaa", 12), border=0)
    exit_button.pack(pady=20)

    fig, ax = plt.subplots(4, 1, figsize=(10, 8))

    sampling_rate = 20  # Adjust as needed
    quantization_bits = 3  # Number of bits for quantization

        # Step 1: Sampling
    x_continuous = np.linspace(0, 4 * np.pi, sampling_rate)
    y_continuous = np.sin(x_continuous)

        # Sample the sine wave
    sampled_x = np.linspace(0, 4 * np.pi, sampling_rate)  # Adjust the number of samples
    sampled_y = np.sin(sampled_x)

    quantized_values = np.round((sampled_y + 1) * ((2**quantization_bits - 1) / 2)).astype(int)
    x_binary = np.arange(len(quantized_values) * quantization_bits)
    binary_output = [int(bit) for val in quantized_values for bit in format(val, f'0{quantization_bits}b')]


    animationCall(fig,ax[0],'original',None,x_continuous, y_continuous, sampled_x, sampled_y, quantized_values,quantization_bits,x_binary,binary_output,'sin')
    animationCall(fig,ax[3],'binary',binary_output,x_continuous, y_continuous, sampled_x, sampled_y, quantized_values,quantization_bits,x_binary,binary_output,'sin')
    animationCall(fig,ax[2],'quantized',binary_output,x_continuous, y_continuous, sampled_x, sampled_y, quantized_values,quantization_bits,x_binary,binary_output,'sin')
    animationCall(fig,ax[1],'quantized2',binary_output,x_continuous, y_continuous, sampled_x, sampled_y, quantized_values,quantization_bits,x_binary,binary_output,'sin')
    canvas = FigureCanvasTkAgg(fig, master=diagramFrame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=TOP, fill=BOTH, expand=1)
    

    atd_root.mainloop()

if __name__ == "__main__":
    AtD()