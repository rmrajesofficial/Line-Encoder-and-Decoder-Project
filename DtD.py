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


ani_list = []



def find_consecutive_zeros(arr,zeroes):
    consecutive_zeros_count = 0
    flag=[]
    for i,num in arr:
        if num == 0:
            consecutive_zeros_count += 1
            flag[i]=0
            if consecutive_zeros_count == zeroes:
                print('Found consecutive {zeroes} zeros!')
                flag[i]=1
                consecutive_zeros_count = 0
        else:
            consecutive_zeros_count = 0
    return flag

def polar_nrz_l(inp):
    inp1 = list(inp)
    inp1 = [-1 if i == 0 else 1 for i in inp1]
    return inp1


def polar_nrz_i(inp):
    inp2 = list(inp)
    flag = False
    for i in range(len(inp2)):
        if inp2[i] == 1 and not flag:
            flag = True
            continue
        if flag and inp2[i] == 1:
            if inp2[i-1] == 0:
                inp2[i] = 1
                continue
            else:
                inp2[i] = 0
                continue
        if flag:
            inp2[i] = inp2[i-1]
    inp2 = [-1 if i == 0 else 1 for i in inp2]
    return inp2

def manches(inp):
    inp1 = list(inp)
    manches = []
    for i in inp1:
        if i == 1:
            manches.append(-1)
            manches.append(1)
        else:
            manches.append(1)
            manches.append(-1)
    return manches

def B8ZS(inpt):
    flag = False
    inp = inpt[0:]
    r = []
    prev = 1
    count = 0
    for i in range(len(inp)):
        if inp[i] == 0:
            count = 1
            for j in range(1, 8):
                if i+j < len(inp):
                    if inp[i+j] == 0:
                        count += 1
                    else:
                        break
                else:
                    break
            if count == 8:
                for j in range(1, 8):
                    inp[i+j] = -1
                r.append(0)
                r.append(0)
                r.append(0)
                if flag:
                    prev = prev * -1
                r.append(prev)
                prev = prev * -1
                r.append(prev)
                r.append(0)
                r.append(prev)
                prev = prev * -1
                r.append(prev)
                count = 0
            else:
                r.append(inp[i])
        elif inp[i] == 1 and not flag:
            flag = True
            r.append(inp[i])
            continue
        elif flag and inp[i] == 1:
            inp[i] = -1
            prev = inp[i]
            r.append(inp[i])
            flag = False
        else:
            continue
    return r

def hdb3(inpt):
    flag = False
    inp = inpt[0:]
    r = []
    prev = 1
    count = 0
    parity = 0
    for i in range(len(inp)):
        if inp[i] == 0:
            count = 1
            for j in range(1, 4):
                if i+j < len(inp):
                    if inp[i+j] == 0:
                        count += 1
                    else:
                        break
                else:
                    break
            if count == 4:
                for j in range(1, 4):
                    inp[i+j] = -1
                if parity % 2 == 1:
                    r.append(0)
                    r.append(0)
                    r.append(0)
                    r.append(prev)
                    parity += 1
                else:
                    prev = prev * -1
                    r.append(prev)
                    r.append(0)
                    r.append(0)
                    r.append(prev)
                count = 0
            else:
                r.append(inp[i])
        elif inp[i] == 1 and parity % 2 == 1:
            inp[i] = -1
            parity += 1
            prev = inp[i]
            r.append(inp[i])
        elif inp[i] == 1 and parity % 2 == 0:
            parity += 1
            prev = inp[i]
            r.append(inp[i])
        else:
            continue
    return r


def AMI(inp):
    inp1 = list(inp)
    flag = False
    for i in range(len(inp1)):
        if inp1[i] == 1 and not flag:
            flag = True
            continue
        elif flag and inp1[i] == 1:
            inp1[i] = -1
            flag = False
    return inp1

def Diff_manchester(inp):
    li = []
    if inp[0] == 1:
        li.append(-1)
        li.append(1)
    else:
        li.append(1)
        li.append(-1)
    for i in range(1, len(inp[1:])):
        if li[-1] == 1:
            if(inp[i] == 1):
                li.append(-1)
                li.append(1)
            else:
                li.append(1)
                li.append(-1)
        else:
            if(inp[i] == 1):
                li.append(1)
                li.append(-1)
            else:
                li.append(-1)
                li.append(1)
    return li





def animationCall(signal,bit,type,fig,ax):
    if bit == 2 and type =='original':
        ax.clear()
        line, = ax.step(signal, signal, where='post',color='red', linestyle='-', marker='o', markersize=6)
        ax.set_title('Input')
        ax.set_xlabel('Index')
        ax.set_ylabel('Value')
        def init():
            ax.set_xlim(0, len(signal))
            ax.set_ylim(-1.25, 1.25)
            line.set_data([], [])
            return line,
        def animate(i):
            y = [0] * len(signal)
            
            for j in range(len(signal)):
                if signal[j] == 1:
                    y[j] =i*0.02+0.02# Increase the height gradually
            x = np.arange(len(y))
            line.set_data(x, y)
            return line,
    
    else:
        ax.clear()
        line, = ax.step(signal, signal, where='post',color='blue', linestyle='-', marker='o', markersize=6)
        ax.set_title(type+' Output')
        ax.set_xlabel('Index')
        ax.set_ylabel('Value')
        def init():
            ax.set_xlim(0, len(signal))
            ax.set_ylim(-1.25, 1.25)
            line.set_data([], [])
            return line,
        def animate(i):
            y = [0] * len(signal)
            
            for j in range(len(signal)):
                if signal[j] == 1:
                    y[j] =(i+1)*0.02# Increase the height gradually
                elif signal[j] == -1:
                    y[j] =0-(i+1)*0.02# Increase the height gradually
            x = np.arange(len(y))
            line.set_data(x, y)
            return line,
    ani = animation.FuncAnimation(fig, animate, init_func=init, frames=50, interval=2, repeat=False)
    ani_list.append(ani)



def exit_application(dtd_root):
    dtd_root.destroy()

def DtD():
    global inputdata
    global result
    def submit_form():
        bit=2
        selected_option = option_var.get()
        if selected_option=='Manchester': bit =3
        global inputdata
        global result
        animationCall(inputdata, bit, "original",fig,ax[0])
        animationCall(result, bit, selected_option,fig,ax[1])
        print('method:',selected_option)
        print('Input: ',inputdata)
        print('Output: ',result)
        canvas.draw()
    def on_entry_change(flag=False):
        if flag==True:
            binary_number = ''.join(random.choice('01') for _ in range(15))
            binary_var.set(binary_number)
            binary_entry.config(textvariable=binary_number)
        selected_option = option_var.get()
        entry_content = binary_entry.get()
        global inputdata
        global result
        inputdata=[]
        result=[]
        for x in entry_content:
            inputdata.append(int(x))
        in_var.set(entry_content)
        inp_entry.config(text=in_var.get())
        out_label.config(text=option_var.get()+' Data:')
        if selected_option=='Polar NRZ-L':
            result = polar_nrz_l(inputdata)
        elif selected_option=='Polar NRZ-I':
            result = polar_nrz_i(inputdata)
        elif selected_option=='Manchester':
            result = manches(inputdata)
        elif selected_option=='AMI':
            result = AMI(inputdata)
        elif selected_option=='Differencial Manchester':
            result = Diff_manchester(inputdata)
        elif selected_option=='Scrambling AMI B8ZS':
            result = B8ZS(inputdata)
        elif selected_option=='Scrambling AMI HBD3':
            result = hdb3(inputdata)
        else:
            result=[None]
            out_var.set('Cannot found the Option')
        
        result_string = ','.join(map(str, result))
        out_var.set(result_string)
        out_entry.config(text=out_var.get())

    dtd_root = Tk()
    dtd_root.geometry('1200x1000')
    dtd_root.minsize(1000, 600)
    dtd_root.title('Digital to Digital')

    formFrame = Frame(dtd_root,width=400)
    formFrame.pack(side=LEFT, fill=BOTH)
    inputFrame=Frame(formFrame,bg='teal')
    inputFrame.pack(side=TOP,fill=BOTH,expand=True)

    outputFrame=Frame(formFrame,bg='teal')
    outputFrame.pack(side=BOTTOM,fill=BOTH,expand=True)

    divider=Frame(outputFrame ,bg='white')
    divider.pack(side='top',fill=BOTH,padx=20)

    formFrameWidth = 400
    formFrame.configure(width=formFrameWidth)
    
    formFrameWidth = 300
    formFrame.pack_propagate(False)  # Prevent frame from shrinking to its content
    formFrame.config(width=formFrameWidth)

    diagramFrame = Frame(dtd_root)
    diagramFrame.pack(side=RIGHT, fill=BOTH,expand=True)

    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True

    fig, ax = plt.subplots(2, 1, figsize=(15, 12))

    inputdata = []
    result=[]
    binary_var = StringVar()
    in_var = StringVar()
    in_var.set('000000000000000')
    out_var = StringVar()
    out_var.set('000000000000000')

    # Stylish labels and fonts
    input_label = Label(inputFrame, text="Input:", font=("Arial", 30, "bold"), fg="white", bg='teal')
    input_label.pack(side='top', pady=20)

    binary_label = Label(inputFrame, text="Enter Binary Number:", font=("Arial", 18), fg="white", bg='teal')
    binary_label.pack(pady=10)

    # Use a different entry widget for better appearance
    binary_entry = Entry(inputFrame,width=20, textvariable=binary_var, bg='white', fg='black', font=("Arial", 20), bd=0, relief='flat')
    binary_entry.pack()
    binary_entry.bind("<KeyRelease>", on_entry_change)

    random_button = Button(inputFrame, text="Random", width=8, height=2, command=lambda: on_entry_change(True), fg='white', font=("Comfortaa", 12), border=0)
    random_button.pack(pady=20,)

    options = ['Polar NRZ-L','Polar NRZ-I','Manchester','AMI','Differencial Manchester','Scrambling AMI B8ZS','Scrambling AMI HBD3']
    option_var = StringVar(inputFrame)
    option_var.set(options[0]) 

    option_label = Label(inputFrame, text="Select an Option:",bg='teal',font=("Arial", 18))
    option_label.pack(pady=10)

    
    option_menu = OptionMenu(inputFrame, option_var, *options)
    # option_var.trace("w", on_entry_change(False))
    option_menu.pack(pady=10)

    input_label = Label(outputFrame, text="Output:", font=("Arial", 30, "bold"), fg="white", bg='teal')
    input_label.pack(side=TOP, pady=20)

    inp_label = Label(outputFrame, text="Input Data:",fg="white", bg='teal',font=("Arial", 18))
    inp_label.pack(pady=10)

    inp_entry = Label(outputFrame, text=in_var.get(),bg='white',fg="black",font=("Arial", 20))
    inp_entry.pack(pady=10)

    out_label = Label(outputFrame, text= option_var.get()+" Data:",fg="white", bg='teal',font=("Arial", 18))
    out_label.pack(pady=10)

    out_entry = Label(outputFrame, text=out_var.get(),bg='white',fg="black",font=("Arial", 20))
    out_entry.pack(pady=5)

    submit_button = Button(inputFrame, text="Submit",width=8, height=2, command=lambda: submit_form(),fg='white', font=("Comfortaa", 12), border=0)
    submit_button.pack(pady=20)
    exit_button = Button(outputFrame, text="Exit", command=lambda: exit_application(dtd_root),width=8, height=2, fg='white', font=("Comfortaa", 12), border=0)
    exit_button.pack(pady=20)

    animationCall([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 2, "original",fig,ax[0])
    animationCall([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 2, "Empty",fig,ax[1])

    # Matplotlib animation
    canvas = FigureCanvasTkAgg(fig, master=diagramFrame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=TOP, fill=BOTH, expand=1)
    
    dtd_root.mainloop()

if __name__ == "__main__":
    DtD()
