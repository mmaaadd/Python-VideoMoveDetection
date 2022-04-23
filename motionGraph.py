import pandas
from bokeh.plotting import figure
from bokeh.io import output_file,show

from moveDetect import df 

output_file ("motion.html")

f = figure (width=800, height=800, x_axis_type='datetime')
f.sizing_mode = "scale_height"
f.title = "Motion Graph"
f.xaxis.axis_label="Time"
f.xaxis.axis_label_text_font_style="italic"
f.xaxis.axis_label_text_font_size = "24px"
f.xaxis.axis_label_text_font = "helvetica"
f.yaxis.axis_label="Motion size"  
f.yaxis.axis_label_text_font_style="italic"
f.yaxis.axis_label_text_font_size = "24px"
f.yaxis.axis_label_text_font = "helvetica"

f.quad(top=df["MaxFrameSize"], bottom=0, left=df["Start"],
       right=df["End"], color="#B3DE69")

show (f)