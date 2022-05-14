from pytube import YouTube
from pytube import Playlist
from pytube import request

from modules.settings import *

class	Youtube_Downloader:
	def __init__(self, app):
		self.title = ''
		self.file_format = ''
		self.is_cancelled = False
		self.is_paused = False
		self.is_downloading = False
		self.download_dialog = None
		self.snackbar = None
		self.app = app

	def reder_format_menu(self):
		self.app.format = MDDropdownMenu(
			caller=self.app.root.ids.drop_item,
			items = [{
				"text": "mp4",
				'viewclass': 'OneLineListItem',
				'on_release': lambda x='': self.app.resolution_menu.open()
				},{
				"text": "mp3",
				'viewclass': 'OneLineListItem',
				'on_release': lambda x='mp3': self.select_format(x)
				}],
			width_mult=1.2,
			position="bottom",
			)
		self.app.resolution_menu = MDListBottomSheet(radius_from=('top'))
		# '144','240','360','480','720','1080','1440','2160'
		self.app.resolution_menu.add_item('144',lambda x: self.select_format('mp4', '144p'))
		self.app.resolution_menu.add_item('240',lambda x: self.select_format('mp4', '240p'))
		self.app.resolution_menu.add_item('360',lambda x: self.select_format('mp4', '360p'))
		self.app.resolution_menu.add_item('480',lambda x: self.select_format('mp4', '480p'))
		self.app.resolution_menu.add_item('720',lambda x: self.select_format('mp4', '720p'))
		self.app.resolution_menu.add_item('1080',lambda x: self.select_format('mp4', '1080p'))
		self.app.resolution_menu.add_item('1440',lambda x: self.select_format('mp4', '1440p'))
		self.app.resolution_menu.add_item('2160',lambda x: self.select_format('mp4', '2160p'))


	def pause(self):
		self.app.root.ids['output_label'].text += '\n\nDownload Paused\n'
		while self.is_paused:
			time.sleep(0.1)
		self.app.root.ids['output_label'].text += '\nDownload Resumed\n\n'


	def select_format(self, form, resolution=''):
		self.file_format = form
		self.resolution = resolution
		if resolution:
			resolution = '  '+resolution
		self.app.root.ids.drop_item.set_item(form + resolution)
		self.app.format.dismiss()


	def format_selection_menu(self):
		self.reder_format_menu()
		self.app.format.open()


	def youtube_download(self, link):
		while self.is_downloading:
			time.sleep(0.1)
		if link == '':
			return
		self.is_downloading = True
		self.is_cancelled = self.is_paused = False
		try:
			playlist = Playlist(link)
			videos = playlist.videos
			lenght = len(videos)
			#folder = SETTINGS["download"] + '/' + # name of the playlist #
		except KeyError:
			try:
				videos = [YouTube(link)]
				lenght = 1
			except Exception as e:
				self.app.root.ids['output_label'].text = str(e)
				self.is_downloading = False
				return
		count, error = 0, 0
		self.app.root.ids['playlist_bar'].value = 0
		self.app.root.ids['output_label'].text = ''
		for video_link in videos:
			if self.is_cancelled:
				break
			if self.is_paused:
				self.pause()
			error = self.video_download(video_link)
			count += 1
			self.app.root.ids['playlist_bar'].value = count*100/lenght
		else:
			if PLATFORM == 'android' and not error:
				notify(title="Download Completed", message=self.title, app_icon=ICON_PNG)
		if self.is_cancelled:
			self.app.root.ids['output_label'].text += '\n\nDownload Cancellated\n\n'
		self.is_downloading = False
			

	def video_download(self, video_link):
		try:
			self.app.root.ids['progress_bar'].value = 0
			self.app.root.ids['output_label'].text += 'Acquiring File'
			self.title = video_link.title
			if self.file_format == 'mp4':
				if SETTINGS['limit']:
					video = video_link.streams.get_by_resolution(self.resolution)
				else:
					video = video_link.streams.get_by_resolution_limitless(self.resolution)
				if not video:
					self.app.root.ids['output_label'].text += '\nResolution not found, getting default resolution'
					if SETTINGS["resolution"]:
						video = video_link.streams.get_highest_resolution()
					elif SETTINGS['limit']:
						video = video_link.streams.get_lowest_resolution()
					else:
						video = video_link.streams.get_lowest_resolution_limitless()
			elif self.file_format == 'mp3':
				video = video_link.streams.filter(only_audio=True).first()
			self.app.root.ids['output_label'].text += '\nDownload Started\n' + self.title
			for char in ".\\/:*?\"\'<>|":
				self.title = self.title.replace(char, '')
			self.downloading(video)
			if self.is_cancelled:
				return
			if self.file_format == 'mp3':
				os.rename(SETTINGS["download"] + '/' + self.title + '.mp4', SETTINGS["download"] + '/' + self.title + '.mp3')
			self.app.root.ids['output_label'].text += '\nDownload Completed\n\n'
		except Exception as error:
			self.app.root.ids['output_label'].text += '\n\n'+str(error)+'\n\n'
			if PLATFORM == 'android':
				notify(title="Error", message=str(error), app_icon=ICON_PNG)
			return 1


	def downloading(self, video):
		filesize = video.filesize
		if self.is_cancelled:
			return
		if self.is_paused:
			self.pause()
		with open(SETTINGS["download"] + '/' + self.title + ".mp4", 'wb') as f:
			#self.is_paused = self.is_cancelled = False
			video = request.stream(video.url)
			downloaded = 0
			while True:
				if self.is_cancelled:
					break
				if self.is_paused:
					self.pause()
				chunk = next(video, None)
				if chunk:
					f.write(chunk)
					downloaded += len(chunk)
					self.app.root.ids['progress_bar'].value = (downloaded / filesize) * 100
				else:
					break	
		
	def download(self):
		if self.app.updating:
			return
		if self.file_format:
			if self.is_downloading:
				if self.download_dialog == None:
					self.download_dialog = MDDialog(
						title="Start Download?",
						text="This will cancel the previous download by starting another.",
						buttons=[
							MDFlatButton(
								text="CANCEL",
								theme_text_color="Custom",
								text_color=self.app.theme_cls.primary_color,
								on_press=self._not_download,
							),
							MDFlatButton(
								text="DOWNLOAD",
								theme_text_color="Custom",
								text_color=self.app.theme_cls.primary_color,
								on_press=self._download,
							),
						],
					)
				self.download_dialog.open()
			else:
				self._download()
		else:
			if self.snackbar == None:
				self.snackbar = Snackbar(
					text="Select Output Format!",
					duration=1,
					snackbar_x="10dp",
					snackbar_y="10dp",
				)
				self.snackbar.size_hint_x = (
					Window.width - (self.snackbar.snackbar_x * 2)
				) / Window.width
			self.snackbar.open()

	def _not_download(self, *args):
		self.download_dialog.dismiss()

	def _download(self, *args):
		if self.download_dialog != None:
			self.download_dialog.dismiss()
		self.is_cancelled = True
		self.thread = threading.Thread(target=self.youtube_download, args=(self.app.root.ids['url_text'].text,))
		self.thread.start()

