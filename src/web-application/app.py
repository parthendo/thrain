import os
import os.path
from flask import Flask, request, redirect, url_for, render_template, session, send_from_directory, send_file
from werkzeug.utils import secure_filename
import DH
import pickle
import random

UPLOAD_FOLDER = './media/text-files/'
UPLOAD_KEY = './media/public-keys/'
ALLOWED_EXTENSIONS = set(['txt'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

'''
-----------------------------------------------------------
					PAGE REDIRECTS
-----------------------------------------------------------
'''
def post_upload_redirect():
	return render_template('post-upload.html')

@app.route('/register')
def call_page_register_user():
	return render_template('register.html')

@app.route('/home')
def back_home():
	return render_template('index.html')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/upload-file')
def call_page_upload():
	return render_template('upload.html')
'''
-----------------------------------------------------------
				DOWNLOAD KEY-FILE
-----------------------------------------------------------
'''
@app.route('/public-key-directory/retrieve/key/<username>')
def download_public_key(username):
	for root,dirs,files in os.walk('./media/public-keys/'):
		for file in files:
			list = file.split('-')
			if list[0] == username:
				filename = UPLOAD_KEY+file
				return send_file(filename, attachment_filename='publicKey.pem',as_attachment=True)

@app.route('/file-directory/retrieve/file/<filename>')
def download_file(filename):
	filepath = UPLOAD_FOLDER+filename
	if(os.path.isfile(filepath)):
		return send_file(filepath, attachment_filename='fileMessage-thrainSecurity.txt',as_attachment=True)
	else:
		return render_template('file-list.html',msg='An issue encountered, our team is working on that')

'''
-----------------------------------------------------------
		BUILD - DISPLAY FILE - KEY DIRECTORY
-----------------------------------------------------------
'''
# Build public key directory
@app.route('/public-key-directory/')
def downloads_pk():
	username = []
	if(os.path.isfile("./media/database/database_1.pickle")):
		pickleObj = open("./media/database/database_1.pickle","rb")
		username = pickle.load(pickleObj)
		pickleObj.close()
	if len(username) == 0:
		return render_template('public-key-list.html',msg='Aww snap! No public key found in the database')
	else:
		return render_template('public-key-list.html',msg='',itr = 0, length = len(username),directory=username)

# Build file directory
@app.route('/file-directory/')
def download_f():
	for root,dirs,files in os.walk(UPLOAD_FOLDER):
		if(len(files) == 0):
			return render_template('file-list.html',msg='Aww snap! No file found in directory')
		else:
			return render_template('file-list.html',msg='',itr=0,length=len(files),list=files)

'''
-----------------------------------------------------------
				UPLOAD ENCRYPTED FILE
-----------------------------------------------------------
'''

@app.route('/data', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		# if user does not select file, browser also
		# submit a empty part without filename
		if file.filename == '':
			flash('No selected file')
			return 'NO FILE SELECTED'
		if file:
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
			return post_upload_redirect()
		return 'Invalid File Format !'

'''
-----------------------------------------------------------
REGISTER UNIQUE USERNAME AND GENERATE PUBLIC KEY WITH FILE
-----------------------------------------------------------
'''
@app.route('/register-new-user', methods = ['GET', 'POST'])
def register_user():
	files = []
	privatekeylist = []
	usernamelist = []
	# Import pickle file to maintain uniqueness of the keys
	if(os.path.isfile("./media/database/database.pickle")):
		pickleObj = open("./media/database/database.pickle","rb")
		privatekeylist = pickle.load(pickleObj)
		pickleObj.close()
	if(os.path.isfile("./media/database/database_1.pickle")):
		pickleObj = open("./media/database/database_1.pickle","rb")
		usernamelist = pickle.load(pickleObj)
		pickleObj.close()
	# Declare a new list which consists all usernames 
	if request.form['username'] in usernamelist:
		return render_template('register.html', name='Username already exists')
	username = request.form['username']
	firstname = request.form['first-name']
	secondname = request.form['last-name']
	pin = int(random.randint(1,128))
	pin = pin % 64
	#Generating a unique private key
	privatekey = DH.generate_private_key(pin)
	while privatekey in privatekeylist:
		privatekey = DH.generate_private_key(pin)
	privatekeylist.append(str(privatekey))
	usernamelist.append(username)
	#Save/update pickle
	pickleObj = open("./media/database/database.pickle","wb")
	pickle.dump(privatekeylist,pickleObj)
	pickleObj.close()
	pickleObj = open("./media/database/database_1.pickle","wb")
	pickle.dump(usernamelist,pickleObj)
	pickleObj.close()
	#Updating a new public key for a new user
	filename = UPLOAD_KEY+username+'-'+secondname.upper()+firstname.lower()+'-PublicKey.pem'
	# Generate public key and save it in the file generated
	publickey = DH.generate_public_key(privatekey)
	fileObject = open(filename,"w")
	fileObject.write(str(publickey))
	return render_template('key-display.html',privatekey=str(privatekey))


	
if __name__ == '__main__':
	#app.run(host="0.0.0.0", port=80)
	app.run()