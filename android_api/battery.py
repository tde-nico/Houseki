from jnius import autoclass, cast
from android_api import activity

Intent = autoclass('android.content.Intent')
BatteryManager = autoclass('android.os.BatteryManager')
IntentFilter = autoclass('android.content.IntentFilter')


class AndroidBattery():

	def get_state(self):
		status = {"isCharging": None, "percentage": None}

		ifilter = IntentFilter(Intent.ACTION_BATTERY_CHANGED)

		battery_status = cast(
			'android.content.Intent',
			activity.registerReceiver(None, ifilter)
		)

		query = battery_status.getIntExtra(BatteryManager.EXTRA_STATUS, -1)
		is_charging = query == BatteryManager.BATTERY_STATUS_CHARGING
		is_full = query == BatteryManager.BATTERY_STATUS_FULL

		level = battery_status.getIntExtra(BatteryManager.EXTRA_LEVEL, -1)
		scale = battery_status.getIntExtra(BatteryManager.EXTRA_SCALE, -1)
		percentage = (level / float(scale)) * 100

		status['isCharging'] = is_charging or is_full
		status['percentage'] = percentage

		return status


Battery = AndroidBattery()
