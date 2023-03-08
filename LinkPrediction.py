
from tkinter import messagebox
from tkinter import *
from tkinter import simpledialog
import tkinter
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np
from tkinter.filedialog import askopenfilename
import networkx as nx
import time

main = tkinter.Tk()
main.title("Link Prediction in Evolving Networks") #designing main screen
main.geometry("1300x1200")

global filename
global graph
unconnected_node1 = []
unconnected_node2 = []
global naive_time, advance_time

def upload(): #function to upload tweeter profile
    global filename
    global graph
    filename = filedialog.askopenfilename(initialdir="dataset")
    pathlabel.config(text=filename)
    graph = nx.read_edgelist(filename,delimiter=' ',create_using=nx.DiGraph(),nodetype=int)
    text.delete('1.0', END)
    text.insert(END,filename+" loaded\n\n");
    text.insert(END,str(nx.info(graph)))

def unconnectedNode():
    unconnected_node1.clear()
    unconnected_node2.clear()
    count = 0
    count1 = 0
    un_connect = graph.edges()
    for a in graph.nodes():
        count1 = 0
        for b in graph.nodes():
            try:
                distance = nx.dijkstra_path(graph,a,b)
                if len(distance) > 0 and count1 < 5 and a != b and (a,b) not in un_connect:
                    unconnected_node1.append(a)
                    unconnected_node2.append(b)
                    count = count + 1
                    count1 = count1 + 1
            except nx.NetworkXNoPath:
                print("no path found")
        if count > 20:
            break
    text.delete('1.0', END)
    text.insert(END,'Unconnected node details\n\n')
    for i in range(len(unconnected_node1)):
        text.insert(END,str(unconnected_node1[i])+' --> '+str(unconnected_node2[i])+"\n")

def influenceSetAlgorithm():
    text.delete('1.0', END)
    pos = nx.spring_layout(graph)    
    influence_node = nx.betweenness_centrality(graph, normalized=True, endpoints=True)
    cis = sorted(influence_node, key=influence_node.get, reverse=True)[:7]
    text.insert(END,'Influence Node with high connection in network\n\n')
    text.insert(END,str(cis))
    node_color = [20000.0 * graph.degree(v) for v in graph]
    node_size =  [v * 10000 for v in influence_node.values()]
    plt.figure(figsize=(20,20))
    nx.draw_networkx(graph, pos=pos, with_labels=True, node_color=node_color, node_size=node_size )
    plt.show()

def naiveCISLinkPrediction(a, b):
    size = 0
    count = 0
    if len(a) > len(b):
        size = len(a)
    else:
        size = len(b)
    dup = []    
    for i in range(len(a)):
        for j in range(len(b)):
            if a[i] == b[j] and a[i] not in dup:
                count = count + 1
        if a[i] not in dup:
            dup.append(a[i])        
    sim_score = 0
    if count > 0:
        sim_score = count/size
    a_set = set(a) 
    b_set = set(b) 
    return a_set & b_set, sim_score    
    
def naiveLinkPrediction():
    global naive_time
    start_time = time.time()
    text.delete('1.0', END)
    text.insert(END,'Naive CIS Link Prediction\n\n')
    for i in range(len(unconnected_node1)):
        e1 = unconnected_node1[i]
        e2 = unconnected_node2[i]
        common1 = sorted(nx.all_neighbors(graph, e1))
        common2 = sorted(nx.all_neighbors(graph, e2))
        predict_link,score = naiveCISLinkPrediction(common1,common2)
        if score > 0.1:
            text.insert(END,'Naive CIS Predicted link : '+str(predict_link)+' for unconnected links : '+str(e1)+' --> '+str(e2)+' with Similarity Score : '+str(score)+"\n")
    end_time = time.time()
    naive_time = end_time - start_time
        


def advanceCISLinkPrediction(a, b):
    count = 0
    size = max(len(a),len(b))
    upperBound = []    
    for i in range(len(a)):
        match = 0
        for j in range(len(b)):
            if a[i] == b[j] and a[i] not in upperBound:
                count = count + 1
                match = 1
        if a[i] not in upperBound and match == 1:
            upperBound.append(a[i])        
    sim_score = 0
    if count > 0:
        sim_score = count/size
    return str(upperBound), sim_score

def advanceUpperBoundLinkPrediction():
    global advance_time
    text.delete('1.0', END)
    text.insert(END,'Advance CIS Link Prediction\n\n')
    start_time = time.time()
    for i in range(len(unconnected_node1)):
        e1 = unconnected_node1[i]
        e2 = unconnected_node2[i]
        common1 = sorted(nx.all_neighbors(graph, e1))
        common2 = sorted(nx.all_neighbors(graph, e2))
        predict_link,score = advanceCISLinkPrediction(common1,common2)
        if score > 0.1:
            text.insert(END,'Advance CIS Predicted link : '+str(predict_link)+' for unconnected links : '+str(e1)+' --> '+str(e2)+' with Similarity Score : '+str(score)+"\n")
    end_time = time.time()
    advance_time = end_time - start_time
    
    
def executionGraph():
    #if advance_time > 
    height = [naive_time,advance_time]
    bars = ('Naive Execution Time', 'Advance Execution Time')
    y_pos = np.arange(len(bars))
    plt.bar(y_pos, height)
    plt.xticks(y_pos, bars)
    plt.show()

def close():
    main.destroy()
    
font = ('times', 16, 'bold')
title = Label(main, text='Link Prediction in Evolving Networks Base on Information Propagation')
title.config(bg='brown', fg='white')  
title.config(font=font)           
title.config(height=3, width=120)       
title.place(x=0,y=5)

font1 = ('times', 14, 'bold')
uploadButton = Button(main, text="Upload Network Dataset", command=upload)
uploadButton.place(x=50,y=100)
uploadButton.config(font=font1)  

pathlabel = Label(main)
pathlabel.config(bg='brown', fg='white')  
pathlabel.config(font=font1)           
pathlabel.place(x=360,y=100)

unconnectButton = Button(main, text="Calculate Unconnected Nodes", command=unconnectedNode)
unconnectButton.place(x=50,y=150)
unconnectButton.config(font=font1) 

ISButton = Button(main, text="Run Influence Set Algorithm", command=influenceSetAlgorithm)
ISButton.place(x=340,y=150)
ISButton.config(font=font1) 

naiveButton = Button(main, text="CIS Link Prediction Using Naive Method", command=naiveLinkPrediction)
naiveButton.place(x=630,y=150)
naiveButton.config(font=font1) 

advanceButton = Button(main, text="Advance Link Prediction using CIS & Upper Bound", command=advanceUpperBoundLinkPrediction)
advanceButton.place(x=50,y=200)
advanceButton.config(font=font1) 

graphButton = Button(main, text="Execution Time Graph", command=executionGraph)
graphButton.place(x=520,y=200)
graphButton.config(font=font1) 

closeButton = Button(main, text="Close Application", command=close)
closeButton.place(x=760,y=200)
closeButton.config(font=font1) 

font1 = ('times', 12, 'bold')
text=Text(main,height=30,width=150)
scroll=Scrollbar(text)
text.configure(yscrollcommand=scroll.set)
text.place(x=10,y=250)
text.config(font=font1)


main.config(bg='brown')
main.mainloop()
