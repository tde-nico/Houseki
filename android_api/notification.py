from re import A
from android import python_act
from android.runnable import run_on_ui_thread
from jnius import autoclass, cast

from android_api import activity, SDK_INT

AndroidString = autoclass('java.lang.String')
Context = autoclass('android.content.Context')
NotificationBuilder = autoclass('android.app.Notification$Builder')
NotificationManager = autoclass('android.app.NotificationManager')
Drawable = autoclass("{}.R$mipmap".format(activity.getPackageName()))
PendingIntent = autoclass('android.app.PendingIntent')
Intent = autoclass('android.content.Intent')
Toast = autoclass('android.widget.Toast')
BitmapFactory = autoclass('android.graphics.BitmapFactory')


class AndroidNotification():

	def __init__(self):
		self._ns = None
		self._channel_id = activity.getPackageName()

	def _get_notification_service(self):
		if not self._ns:
			self._ns = cast(NotificationManager, activity.getSystemService(
				Context.NOTIFICATION_SERVICE
			))
		return self._ns

	def _build_notification_channel(self, name):

		if SDK_INT < 26:
			return
		channel = autoclass('android.app.NotificationChannel')
		app_channel = channel(
			self._channel_id, name, NotificationManager.IMPORTANCE_DEFAULT
		)
		self._get_notification_service().createNotificationChannel(
			app_channel
		)
		return app_channel

	@run_on_ui_thread
	def _toast(self, message):
		Toast.makeText(
			activity,
			cast('java.lang.CharSequence', AndroidString(message)),
			Toast.LENGTH_LONG
		).show()

	@staticmethod
	def _set_icons(notification, icon=None):
		app_icon = Drawable.icon
		notification.setSmallIcon(app_icon)

		bitmap_icon = app_icon
		if icon is not None:
			bitmap_icon = BitmapFactory.decodeFile(icon)
			notification.setLargeIcon(bitmap_icon)
		elif icon == '':
			# we don't want the big icon set,
			# only the small one in the top panel
			pass
		else:
			bitmap_icon = BitmapFactory.decodeResource(
				python_act.getResources(), app_icon
			)
			notification.setLargeIcon(bitmap_icon)

	def _build_notification(self, title):
		if SDK_INT < 26:
			noti = NotificationBuilder(activity)
		else:
			self._channel = self._build_notification_channel(title)
			noti = NotificationBuilder(activity, self._channel_id)
		return noti

	@staticmethod
	def _set_open_behavior(notification):
		app_context = activity.getApplication().getApplicationContext()
		notification_intent = Intent(app_context, python_act)
		notification_intent.setFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP)
		notification_intent.setAction(Intent.ACTION_MAIN)
		notification_intent.addCategory(Intent.CATEGORY_LAUNCHER)

		pending_intent = PendingIntent.getActivity(
			app_context, 0, notification_intent, 0
		)
		notification.setContentIntent(pending_intent)
		notification.setAutoCancel(True)

	def _open_notification(self, notification):
		if SDK_INT >= 16:
			notification = notification.build()
		else:
			notification = notification.getNotification()

		self._get_notification_service().notify(0, notification)

	def _notify(self, **kwargs):
		noti = None
		message = kwargs.get('message').encode('utf-8')
		ticker = kwargs.get('ticker').encode('utf-8')
		title = AndroidString(
			kwargs.get('title', '').encode('utf-8')
		)
		icon = kwargs.get('app_icon')
		if kwargs.get('toast'):
			self._toast(message)
			return
		else:
			noti = self._build_notification(title)

		noti.setContentTitle(title)
		noti.setContentText(AndroidString(message))
		noti.setTicker(AndroidString(ticker))
		self._set_icons(noti, icon=icon)
		self._set_open_behavior(noti)

		self._open_notification(noti)


def instance():
	return AndroidNotification()

def notify(title='', message='', app_icon='', app_name='', timeout=10, ticker='', toast=False):
	my_notification = AndroidNotification()
	my_notification._notify(title=title, message=message,
		app_icon=app_icon, app_name=app_name,
		timeout=timeout, ticker=ticker, toast=toast)