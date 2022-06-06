from modules.settings import *

class	Home:
	def __init__(self, app):
		self.app = app
		self.cancel_dialog = None

	def home(self):
		self.app.root.ids['screen_manager'].current = "home"
		self.app.root.ids['nav_drawer'].set_state("close")

	def paste(self):
		self.app.root.ids['url_text'].text = Clipboard.paste()

	def clear(self):
		self.app.root.ids['url_text'].text = ''
		self.app.root.ids['output_label'].text = ''
		self.app.root.ids['playlist_bar'].value = 0
		self.app.root.ids['progress_bar'].value = 0
	
	def resume(self):
		self.app.yd.is_paused = False

	def stop(self):
		self.app.yd.is_paused = True

	def cancel(self):
		if not self.app.yd.is_downloading:
			return
		if self.cancel_dialog == None:
			self.cancel_dialog = MDDialog(
				title="Cancel Download?",
				text="This will cancel the download.",
				buttons=[
					MDFlatButton(
						text="CANCEL",
						theme_text_color="Custom",
						text_color=self.app.theme_cls.primary_color,
						on_press=self._not_cancel,
					),
					MDFlatButton(
						text="OK",
						theme_text_color="Custom",
						text_color=self.app.theme_cls.primary_color,
						on_press=self._cancel,
					),
				],
			)
		self.cancel_dialog.open()
	
	def _not_cancel(self, *args):
		self.cancel_dialog.dismiss()

	def _cancel(self, *args):
		self.cancel_dialog.dismiss()
		self.app.yd.is_cancelled = True
