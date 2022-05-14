from modules.settings import *
from pytube import __version__

class	Settings:
	def __init__(self, app):
		self.app = app
		self.manager_open = False
		self.file_manager = MDFileManager(
			exit_manager=self.exit_manager,
			select_path=self.select_path,
		)
		self.dialog = None

	def settings(self):
		if self.app.theme_cls.theme_style == 'Dark':
			self.app.root.ids['theme'].active = True
		self.app.root.ids['palette'].text = SETTINGS['palette']

		colors = ('Red','Pink','Purple','DeepPurple','Indigo','Blue','LightBlue','Cyan','Teal','Green',
			'LightGreen', 'Lime','Yellow','Amber','Orange','DeepOrange','Brown','Gray','BlueGray')
		self.palette_menu = MDDropdownMenu(
			caller=self.app.root.ids.palette,
			items = [{
				"text": color,
				'viewclass': 'OneLineListItem',
				'on_release': lambda x=color: self.change_palette(x)
				} for color in colors],
			width_mult=2,
			max_height=700,
			position="bottom",
			)

		if SETTINGS["resolution"]:
			self.app.root.ids['resolution'].active = True
		if SETTINGS["limit"]:
			self.app.root.ids['limit'].active = True
		if SETTINGS["update"]:
			self.app.root.ids['update'].active = True
		self.app.root.ids['download_folder'].text = SETTINGS['download'].split('/')[-1]
		self.app.root.ids['screen_manager'].current = 'settings'
		self.app.root.ids['nav_drawer'].set_state("close")


	def change_theme(self):
		if self.app.root.ids['theme'].active:
			self.app.theme_cls.theme_style = "Dark"
			SETTINGS["theme"] = 'Dark'
		else:
			self.app.theme_cls.theme_style ="Light"
			SETTINGS["theme"] = 'Light'
		dump()


	def change_palette(self, palette):
		self.palette_menu.dismiss()
		self.app.theme_cls.primary_palette = palette
		self.app.root.ids['palette'].text = palette
		SETTINGS["palette"] = palette
		dump()


	def set_default_resolution(self):
		if self.app.root.ids['resolution'].active:
			SETTINGS["resolution"] = 1
		else:
			SETTINGS["resolution"] = 0
		dump()


	def set_limit(self):
		if self.app.root.ids['limit'].active:
			SETTINGS["limit"] = 1
		else:
			SETTINGS["limit"] = 0
		dump()


	def set_update(self):
		if self.app.root.ids['update'].active:
			SETTINGS["update"] = 1
		else:
			SETTINGS["update"] = 0
		dump()


	def file_manager_open(self):
		self.file_manager.show(SETTINGS['download'])
		self.manager_open = True

	def select_path(self, path):
		self.exit_manager()
		path = path.replace("\\", "/")
		SETTINGS['download'] = path
		self.app.root.ids['download_folder'].text = path.split('/')[-1]
		dump()

	def exit_manager(self, *args):
		self.manager_open = False
		self.file_manager.close()


	def reset(self):
		if self.app.updating:
			return
		if self.dialog == None:
			self.dialog = MDDialog(
				title="Reset settings?",
				text="This will reset your device to its default factory settings.",
				buttons=[
					MDFlatButton(
						text="CANCEL",
						theme_text_color="Custom",
						text_color=self.app.theme_cls.primary_color,
						on_press=self._not_reset,
					),
					MDFlatButton(
						text="CONTINUE",
						theme_text_color="Custom",
						text_color=self.app.theme_cls.primary_color,
						on_press=self._reset,
					),
				],
			)
		self.dialog.open()

	def _not_reset(self, *args):
		self.dialog.dismiss()

	def _reset(self, *args):
		self.dialog.dismiss()
		reset_settings()
		self.app.theme_cls.primary_palette = SETTINGS['palette']
		self.app.root.ids['palette'].text = SETTINGS['palette']
		self.app.theme_cls.theme_style = SETTINGS['theme']
		self.app.root.ids['theme'].active = True
		self.app.root.ids['resolution'].active = True
		self.app.root.ids['limit'].active = True
		self.app.root.ids['download_folder'].text = SETTINGS['download'].split('/')[-1]


	def	upgrade(self):
		try:
			self.app.updating = True
			self.update_snackbar = Snackbar(
				text="Up to Date",
				snackbar_x="10dp",
				snackbar_y="10dp",
				size_hint_x=.5
			)
			self.update_snackbar.size_hint_x = (
				Window.width - (self.update_snackbar.snackbar_x * 2)
			) / Window.width

			version_url = "https://raw.githubusercontent.com/pytube/pytube/master/pytube/version.py"
			version_req = requests.get(version_url)
			version_code = version_req.content.decode()
			new_version = version_code.split()[2].replace("\"", "")
			if new_version == __version__:
				self.update_snackbar.open()
				self.app.updating = False
				return

			cipher_url = "https://raw.githubusercontent.com/pytube/pytube/master/pytube/cipher.py"
			cipher_req = requests.get(cipher_url)
			cipher_code = cipher_req.content.decode()
			with open("pytube/cipher.py", "w") as f:
				f.write(cipher_code)
			with open("pytube/version.py", "w") as f:
				f.write(version_code)

			self.update_snackbar.text = "Restart the app to update"
			self.update_snackbar.buttons = [
				MDFlatButton(
					text="CLOSE",
					text_color=(1, 1, 1, 1),
					on_release=self._finish_update,
				),
				MDFlatButton(
					text="CANCEL",
					text_color=(1, 1, 1, 1),
					on_release=self.update_snackbar.dismiss,
				),
			]
			self.update_snackbar.open()
		except Exception as error:
			self.app.updating = False
			if PLATFORM == 'android':
				notify(title='Error', message=str(error), app_icon=ICON_PNG)
			else:
				print(error)
	
	def	_finish_update(self, *args):
		self.update_snackbar.dismiss()
		self.app.updating = False
		self.app.exit()

