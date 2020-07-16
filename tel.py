from telegram.ext import Updater, CommandHandler, MessageHandler,Filters
from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN
from io import BytesIO
import os
import subprocess

def mkdir(d_name):
	try:
		os.mkdir(d_name)
	except:
		pass

def oga_to_wav(file_oga_name):
	new_file_name=file_oga_name.replace('file','audio_message').replace('.oga','.wav').replace('ogaFolder','wavFolder')
	proccess=subprocess.run(['ffmpeg.exe','-i',file_oga_name,'-ar','16000',new_file_name])

def image_handler(update,context ):
	print(type(update))
	print(update.message.photo)
	file = update.message.photo[-1].get_file()
	f =  BytesIO(file.download_as_bytearray())
	#image = Image.open(f).convert("RGBA")
	#print ("file_id: " + str(update.message.photo.file_id))
	name=file['file_path'].split('/photos/')[-1]
	detector = MTCNN()
	pixels = pyplot.imread(f,format='JPG')
	faces = detector.detect_faces(pixels)
	print(len(faces))
	mkdir('photos')
	mkdir('photos/'+str(update.message.from_user.id))
	if len(faces)>0:
		file.download('photos/'+str(update.message.from_user.id)+'/'+name)

def audio_hendler(update,context ):
	print(type(update))
	print(update.message.from_user.id)
	file = update.message.voice.get_file()
	mkdir('voice')
	mkdir('voice/'+str(update.message.from_user.id))
	mkdir('voice/'+str(update.message.from_user.id)+'/ogaFolder')
	mkdir('voice/'+str(update.message.from_user.id)+'/wavFolder')
	name=file['file_path'].split('/voice/')[-1]
	file.download('voice/'+str(update.message.from_user.id)+'/ogaFolder/'+name)
	oga_to_wav('voice/'+str(update.message.from_user.id)+'/ogaFolder/'+name)


updater = Updater('1330025796:AAGCEqc5vQVSw-lCp5wRW4J7M6qVwa1zmIk', use_context=True)

updater.dispatcher.add_handler(MessageHandler(Filters.photo, image_handler))
updater.dispatcher.add_handler(MessageHandler(Filters.voice, audio_hendler))
		
updater.start_polling()
updater.idle()