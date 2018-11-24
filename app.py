####################################
# Flask App demo to upload an image
#
# to do
#   trigger machine learning model to split image by pattern
# 
# to run
#   python app.py 
####################################

from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename
from flask import send_from_directory
import os
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16MB max
#app.config['MAX_CONTENT_LENGTH'] = 1024 # 1KB max test only

@app.route('/')
def home():
    return render_template('input.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def uploaded_file():
   if request.method == 'POST':
      file = request.files['file']
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

      return redirect(url_for('output'))

# later will reuse this for machine learning on one single image
#def uploaded_file_single_fixed_file():
#   if request.method == 'POST':
#      file = request.files['file']
#      filename = secure_filename('data.jpg')
#      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#
#      return render_template('output.html')
  
@app.route('/output', methods = ['GET', 'POST'])
def output():
#    return '<img src="uploads/data.jpg" />'

    directory = os.fsencode(app.config['UPLOAD_FOLDER'])
    
    html_buffer = ('<html>'
                    +'<head>'
                    +'<style>'
                    +'img.resize {width:300px; height:auto}'
                    +'</style>'
                    +'</head>'
                    +'<body>')
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".jpg") or filename.endswith(".png"):
            html_buffer += '<img class="resize" src="uploads/'+filename+'" />'

    html_buffer += '</body>'
    html_buffer += '</html>'

    return html_buffer
    
@app.route('/uploads/<filename>')
def map_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
		
# aws ec2 run on these lines, local also works
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

# local run this is fine
#app.run(port=5000)
