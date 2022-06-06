# remove telnetlib
import kivy
import kivymd
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.button import MDFlatButton
from kivymd.uix.snackbar import Snackbar
from kivy.core.clipboard import Clipboard

import os, threading, json, time, requests

TITLE = "Houseki"
DEVELOPER = "tde-nico"
GIT = "https://github.com/tde-nico"
VERSION = "1.3.4"
ICON = "modules/gem.ico"
ICON_PNG = "modules/gem.png"
PLATFORM = kivy.utils.platform
SETTINGS = dict()

if PLATFORM == 'android':
	import android_api
	from android_api.notification import notify

def	dump():
	with open('settings.json', 'w') as s:
		json.dump(SETTINGS, s)


# ssl permisson
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

if PLATFORM == 'android':
	# request permissions for android
	from android.permissions import request_permissions, Permission
	request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
	# storage permissions
	from android.storage import primary_external_storage_path
	common_dir = primary_external_storage_path()
	# default download folder
else:
	kivy.core.window.Window.size = (450, 700)
	common_dir = os.getcwd()
	common_dir = common_dir.replace("\\", "/")
	if not os.path.exists(common_dir + "/Download"):
		os.mkdir(common_dir + "/Download")

#import requests

def reset_settings():
	#global SETTINGS
	'''
	SETTINGS = {
		"theme":		"Dark",
		"palette":		"Purple",
		"resolution":	1,
		"limit":		1,
		"download":		(os.path.join(common_dir, 'Download') + '/')
	}
	'''
	SETTINGS['theme'] = 'Dark'
	SETTINGS['palette'] = 'Purple'
	SETTINGS['resolution'] = 1
	SETTINGS['limit'] = 1
	SETTINGS['update'] = 0
	SETTINGS['download'] = common_dir + '/Download'
	dump()

try:
	with open('settings.json', 'r') as s:
		SETTINGS = json.load(s)
except:
	reset_settings()

class	Debug:
	def __init__(self, app):
		self.app = app

	def unit_test(self):
		print('unit test')

def debug(error):
	with open(SETTINGS['download'] + '/log.txt', 'w') as d:
		d.write(error)
