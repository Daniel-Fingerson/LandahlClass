#RAMP STATE, EX AND ACTUAL VALUES NEED TO BE REMOVED ASS ACTUAL VARIABLES AND RATHER MADE TO BE THE DATA VARIABLES FORMAT                
#two tasks for this app:
#1: figure out how to get rid of the dropdowns
#2: figure out what the best way to display the ramps (or simply have a seperate graph)
#3: figure out how to make this run AND actually run the oven at the same time (could run both at once, then have it read a shared file?
#a loop could occur in either of the update functions, will have to experiment; will also need to update interval value
#will need to have a new system for when it turns on and off so that it doesnt disrupt the graph updating (although I could try saving the sleep function and seeing what happens)
#rather have a counter variable that updates itself each time the function is called which via modulo the app can keep track of
#BEST OPTION: output the text within the dash page itself (will need to figure out how to do so)
#test if I can use either of the "update" functions to turn on and off the oven (have modulo so that it alternates between on and off)
#run AND have website: https://stackoverflow.com/questions/32045300/running-a-continous-while-loop-in-python-along-with-flask-app
#above suggests either having chrom execute script and then recieve it back as data OR use threading
#threading seems much better
#https://stackoverflow.com/questions/28800614/run-while-loop-concurrently-with-flask-server
#https://stackoverflow.com/questions/25639221/how-to-run-recurring-task-in-the-python-flask-framework
#BEST SOLUTION AS OF YET: https://forum.arduino.cc/index.php?topic=474104.0
#the above uses threading; may need to have an outside file that tells the app what the GPIO output value is (need to check if there are built-in functions that can check the state)
#ALSO need to write a way so that it takes all of the measuremnts but lets me manually turn it on and off/the ramp time
#could probably easilly do this via a threading "check input" method


#sample on and off function: 
import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import time
from collections import deque
import plotly.graph_objs as go
import random
import spidev
import RPi.GPIO as GPIO
import time
import _thread
from time import sleep
from readloop import read
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21,GPIO.OUT)
GPIO.output(21,1)
#populate the list with expected temperature per second of the reflow profile
ramp=[]
#25-90 degrees in 90 seconds
for i in range(91):
    ramp.append(25+(i*.722))
#for i in range(90):
time_pass=0
def background_ramp():
    global ramp_flag
    global time_pass
    while True:
        time.sleep(1)
        time_pass+=1
ramp_flag=1
app = dash.Dash(__name__)
max_length = 90
times = deque(maxlen=max_length)
ex_val = deque(maxlen=max_length)
actual_val = deque(maxlen=max_length)
ramp_state = deque(maxlen=max_length)



data_dict = {"Expected Value":ex_val,
"Actual Measured Value": actual_val,
"Ramp State": ramp_state}


#THIS NEEDS TO HAVE A FUNCTION THAT APPENDS THE EXPECTED VALUES LIST TO A NEW LIST EVERY SECOND (or however amount of time we want to elapse in between data points)
def update_obd_values(times, ex_val, actual_val, ramp_state):
    #print("yeet")
    #may update the "time" paramater to be something more...preferable (honestly dont know if this will be a problem or not)
    #times.append(time.time()) old time code
    times.append(time_pass)
    ex_val.append(read())
    #actual_val.append(interpolation function)
    actual_val.append(random.randrange(95,115)) #place holder
    ramp_state.append(ramp_flag)
    return times, ex_val, actual_val, ramp_state

times, ex_val, actual_val, ramp_state = update_obd_values(times, ex_val, actual_val, ramp_state)

app.layout = html.Div([
    html.Div([
        html.H2('Instrumentation Amplifier w/ Bridge Live Readout',
                style={'float': 'left',
                       }),
        ]),
    
    
    html.Div(children=html.Div(id='graphs'), className='row'),
    dcc.Interval(
        id='graph-update',
        interval=1000,  #in milliseconds
        n_intervals=0),
    ], className="container",style={'width':'98%','margin-left':10,'margin-right':10,'max-width':50000})

#callback is where the graph is calling functions and what not
@app.callback(
    dash.dependencies.Output('graphs','children'),
    [dash.dependencies.Input('graph-update', 'n_intervals')])
#need to figure out how to handle getting rid of data_names   
def update_graph_scatter(n):
    graphs = []
    update_obd_values(times, ex_val, actual_val, ramp_state)

    #get rid of this loop to get rid of dropdown
    #for data_name in data_names:

    data = go.Scatter(
        x=list(times),
        y=list(ex_val),
        name='Scatter',
        fill="tozeroy",
        fillcolor="#6897bb"
        )
        #new code for multiple lines:
    '''
    data2=go.Scatter(
        x=list(times),
        y=list(ex_val),
        name='Expected value',
        fill="tozeroy",
        fillcolor="#6897bb"
        )
    '''
        #put data for other lines in the below variable "figure[data] brackets
    graphs.append(html.Div(dcc.Graph(
        id="Expected Value",
        animate=True,
        figure={'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(times),max(times)],title="Time (Seconds)"),
                                                    yaxis=dict(range=[min(ex_val),max(ex_val)]),
                                                    #margin={'l':50,'r':1,'t':45,'b':1}, if I want to predefine graph
                                                    title='{}'.format("ADC Voltage"))}
        ), '''className=class_choice'''))

    return graphs
if __name__=='__main__':
    _thread.start_new_thread(background_ramp, ())
    app.run_server(debug=True)

