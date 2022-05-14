from jnius import autoclass, cast
from android_api import activity
from android_api import SDK_INT

Context = autoclass("android.content.Context")
vibrator_service = activity.getSystemService(Context.VIBRATOR_SERVICE)
vibrator = cast("android.os.Vibrator", vibrator_service)
if SDK_INT >= 26:
	VibrationEffect = autoclass("android.os.VibrationEffect")


class AndroidVibrator():

	def vibrate(self, time=None, **kwargs):
		if vibrator:
			if SDK_INT >= 26:
				vibrator.vibrate(
					VibrationEffect.createOneShot(
						int(1000 * time), VibrationEffect.DEFAULT_AMPLITUDE
					)
				)
			else:
				vibrator.vibrate(int(1000 * time))

	def pattern(self, pattern=None, repeat=None, **kwargs):
		pattern = [int(1000 * time) for time in pattern]

		if vibrator:
			if SDK_INT >= 26:
				vibrator.vibrate(
					VibrationEffect.createWaveform(pattern, repeat)
				)
			else:
				vibrator.vibrate(pattern, repeat)

	def exists(self, **kwargs):
		if SDK_INT >= 11:
			return vibrator.hasVibrator()
		elif vibrator_service is None:
			raise NotImplementedError()
		return True

	def cancel(self, **kwargs):
		vibrator.cancel()


Vibrator = AndroidVibrator()
