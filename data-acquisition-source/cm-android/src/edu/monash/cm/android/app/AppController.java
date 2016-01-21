package edu.monash.cm.android.app;

import android.app.Activity;
import android.app.Application;
import android.content.Context;

public class AppController extends Application {

	public static final String TAG = AppController.class.getSimpleName();
	private static Context context;
	private static AppController mInstance;
	private static Activity mCurrentActivity = null;

	private Thread.UncaughtExceptionHandler androidDefaultUEH;
	private Thread.UncaughtExceptionHandler handler = new Thread.UncaughtExceptionHandler() {
		public void uncaughtException(Thread thread, Throwable ex) {
			// Stop all services of iBeacon and Bluetooth
			// Utils.stopServiceIBeacon();
			// Utils.stopBluetooth();

			androidDefaultUEH.uncaughtException(thread, ex);
			android.os.Process.killProcess(android.os.Process.myPid());
		}
	};

	@Override
	public void onCreate() {
		super.onCreate();

		mInstance = this;
		AppController.context = getApplicationContext();

		androidDefaultUEH = Thread.getDefaultUncaughtExceptionHandler();
		Thread.setDefaultUncaughtExceptionHandler(handler);

		AppSetting.loadSettings(this);
	}

	public static Context getAppContext() {
		return AppController.context;
	}


	public static Activity getCurrentActivity() {
		return mCurrentActivity;
	}

	public static void setCurrentActivity(Activity currentActivity) {
		mCurrentActivity = currentActivity;
	}

	public static synchronized AppController getInstance() {
		return mInstance;
	}
}
