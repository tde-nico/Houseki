from modules.settings import *
from modules.youtube import Youtube_Downloader
from modules.settings_menu import Settings
from modules.home import Home
from modules.unit import Unit_Test

#	TEST LINKS

#	https://www.youtube.com/watch?v=_W88oVKhNW0&ab_channel=Geoxor
#	https://www.youtube.com/watch?v=FuaQ1QhJOkc&ab_channel=MusicLab
#	https://www.youtube.com/watch?v=WSeNSzJ2-Jw&list=PL00277C3B32679850&ab_channel=Skrillex
#	https://www.youtube.com/watch?v=JQ1txLdu6qg&t=1476s&ab_channel=AlexMTCH

# some regex error
# var_regex = re.compile(r"^\$*\w+\W")

class Touch(MDScreen):
	#def on_touch_down(self, touch):
	#	print("down")
	#def on_touch_up(self, touch):
	#	print("up")
	def on_touch_move(self, touch):
		if touch.x - touch.ox > 200:
			if self.ids['nav_drawer'].status == 'closed':
				self.ids['nav_drawer'].set_state("open")
		if touch.y - touch.oy > 1000:
			exit()


class main_app(MDApp):
	def build(self):
		self.title = TITLE
		self.theme_cls.theme_style = SETTINGS["theme"]
		self.theme_cls.primary_palette = SETTINGS["palette"]
		self.yd = Youtube_Downloader(self)
		self.settings = Settings(self)
		self.home = Home(self)
		self.unit_test = Unit_Test(self)
		self.info = None
		self.format = None
		self.updating = False

		if kivymd.__version__ == '0.104.2':
			Builder.load_file('main_app_104.kv')
		else:
			Builder.load_file('main_app_new.kv')
		return Touch() #Builder.load_file('main_app.kv')


	def	on_start(self):
		if SETTINGS["update"]:
			self.settings.upgrade()

	'''
	def on_stop(self):
		pass

	def on_pause(self):
		# Here you can save data if needed
		return True

	def on_resume(self):
		# Here you can check if any data needs replacing (usually nothing)
		pass
	'''


	def show_info(self):
		if not self.info:
			app_info =	"App: " + TITLE + "\n" + \
					"Developer: " + DEVELOPER + "\n" + \
					"Git: " + GIT + "\n" + \
					"Version: " + VERSION #+ "\n" + \
			self.info = MDDialog(
				title='Info',
				text=app_info,
				auto_dismiss=True
				)
		self.info.open()


	def exit(self):
		self.get_running_app().stop()
		exit()


main_app().run()
