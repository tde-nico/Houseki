from modules.settings import *
if PLATFORM == 'android':
	import android_api
	from android_api.notification import notify
	from android_api.vibrator import Vibrator
	from android_api.battery import Battery

class	Unit_Test:
	def __init__(self, app):
		self.app = app
		try:
			if PLATFORM == 'android':
				self.battery = Battery
		except Exception as e:
			self.app.root.ids['fix_label'].text += str(e)

	def unit_test(self):
		try:
			if PLATFORM == 'android':
				status = self.battery.get_state()
				self.app.root.ids['battery_charging'].text = str(status['isCharging'])
				self.app.root.ids['battery_percentage'].text = str(status['percentage'])
		except Exception as e:
			self.app.root.ids['fix_label'].text += str(e)
		self.app.root.ids['screen_manager'].current = 'unit_test'
		self.app.root.ids['nav_drawer'].set_state("close")


	def do_vibrate(self):
		if PLATFORM == 'android':
			try:
				if Vibrator.exists():
					Vibrator.vibrate(time=0.1)
			except Exception as e:
				self.app.root.ids['fix_label'].text += str(e)
		else:
			print(" * VIBRATE * for 0.1s")


	def do_notify(self):
		if PLATFORM == 'android':
			notify(title='Unit Test', message='notify', app_icon=ICON_PNG)
		else:
			print("title='Unit Test', message='notify', app_icon='" + ICON_PNG + "'")
		
