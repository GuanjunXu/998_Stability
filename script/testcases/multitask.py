#! /usr/bin/env python
# -*- coding: utf-8 -*-  
import unittest
from uiautomatorplug.android import device as d
import commands
import util as u

APP_TEL_LIST = ['com.smartisanos.appstore/.AppStoreActivity','com.android.mms/.ui.ConversationList','com.smartisanos.music/.activities.MusicMain','com.android.browser/.BrowserActivity']
APP_BROWSER_LIST = ['com.smartisanos.appstore/.AppStoreActivity','com.android.mms/.ui.ConversationList','com.smartisanos.music/.activities.MusicMain','com.android.contacts/.activities.DialtactsActivity']
MULTIPLE_APP_LIST = {'com.smartisanos.appstore/.ui.AppStoreActivity':'com.smartisanos.appstore',
	'com.smartisanos.clock/.activity.ClockActivity':'com.smartisanos.clock',
	'com.android.camera2/com.android.camera.CameraLauncher':'com.android.camera2',
	'com.android.calendar/.AllInOneActivity':'com.android.calendar',
	'com.smartisanos.notes/.NotesActivity':'com.smartisanos.notes',
	'com.android.settings/.Settings': 'com.android.settings',
	'com.android.email/.activity.Welcome':'com.android.email',
	'com.android.gallery3d/.app.Gallery':'com.android.gallery3d',
	'com.smartisanos.calculator/.Calculator':'com.smartisanos.calculator',
	'com.smartisanos.recorder/.activity.EmptyActivity':'com.smartisanos.recorder',
	'com.smartisanos.weather/.CityWeather':'com.smartisanos.weather',
	'com.smartisanos.cloudsync/.AccountsActivityLauncher':'com.smartisanos.cloudsync',
	'com.android.contacts/.activities.DialtactsActivity':'com.android.contacts',
	'com.android.mms/.ui.ConversationList':'com.android.mms',
	'com.android.browser/.BrowserActivity':'com.android.browser'}

class MultiTaskTest(unittest.TestCase):
	def setUp(self):
		u.setUp()

	def tearDown(self):
		u.tearDown()

	def testMultiTaskTelephony(self):
		# make a phone call
		commands.getoutput('adb shell am start -n com.android.contacts/.activities.DialtactsActivity')
		d(text = '拨号').click.wait()
		d(resourceId = 'com.android.contacts:id/digits').set_text(u.getNumber())
		d(resourceId = 'com.android.contacts:id/call_classic').click.wait()
		d.sleep(1)
		d.press('home')
		# launch app
		for i in APP_TEL_LIST:
			commands.getoutput('adb shell am start -n %s'%i)
			d.sleep(5)
			d.press('home')
			d.sleep(1)
		d.press('home')
		d.swipe(540,1,540,500,10)
		d.sleep(1)
		if d(text = '当前通话').exists:
			d(text = '当前通话').click.wait()
			d(text = '结束').click.wait()
		d.press('home')
		assert d(packageName = 'com.smartisanos.launcher').exists,'Launcher is not show on the screen!'

	def testMultiTaskBrowser(self):
		# browse webpage
		commands.getoutput('adb shell am start -n com.android.browser/.BrowserActivity')
		# close all webpage
		d(resourceId = 'com.android.browser:id/switch_btn').click.wait()
		d(resourceId = 'com.android.browser:id/clearall').click.wait()
		d(text = '关闭').click.wait()
		d(resourceId = 'com.android.browser:id/url', text = '输入网址').set_text('wap.sohu.com')
		d.press('enter')
		d.sleep(1)
		d.press('home')
		for i in APP_BROWSER_LIST:
			commands.getoutput('adb shell am start -n %s'%i)
			d.sleep(5)
			d.press('home')
			d.sleep(1)
		d.press('home')
		assert d(packageName = 'com.smartisanos.launcher').exists,'Launcher is not show on the screen!'

	def testLaunchMultipleApp(self):
		# Launch an
		for app in MULTIPLE_APP_LIST:
			d.start_activity(component= app)
			assert d(packageName = MULTIPLE_APP_LIST[app]).wait.exists(timeout = 5000),'Launch %s failed in 5s'%app
			d.sleep(5)
			d.press('home')
			d.sleep(1)