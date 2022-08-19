all: clean build

build:
	buildozer -v android debug

clean:
	rm -rf ./Download/
	rm -rf ./modules/__pycache__/


host: 
	buildozer serve

serve: all host

debug: all
	buildozer -v android deploy run

#/home/kali/.buildozer/android/platform/android-sdk/platform-tools/adb devices | tr -d "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm \n"
connect:
	/home/kali/.buildozer/android/platform/android-sdk/platform-tools/adb devices
	@echo "/home/kali/.buildozer/android/platform/android-sdk/platform-tools/adb connect"

disconnect:
	/home/kali/.buildozer/android/platform/android-sdk/platform-tools/adb disconnect

