package edu.monash.cm.android.app.service;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Timer;
import java.util.TimerTask;

import org.codehaus.jackson.map.ObjectMapper;

import android.app.Activity;
import android.app.Service;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.IBinder;
import android.util.Log;
import edu.monash.cm.android.app.AppController;
import edu.monash.cm.android.app.constant.Constants;
import edu.monash.cm.android.app.restservice.SurroundingDeviceAPIHandler;
import edu.monash.cm.android.app.utils.NetworkUtility;
import edu.monash.cm.model.surround.SurroundingDevice;
import edu.monash.cm.model.surround.SurroundingDeviceDataBundle;

public class BluetoothScanningService extends Service {
	private static final String TAG = "BluetoothScanningService";

	// keep the context of the activity registering BlueTooth Scanning Service
	private Activity registeredActivity = null;

	private BluetoothAdapter mBluetoothAdapter;

	public List<SurroundingDevice> mNewDevicesArrayAdapter;

	public static SurroundingDeviceDataBundle deviceBundle;

	// timer handling
	private Timer mTimer = null;

	@Override
	public IBinder onBind(Intent intent) {
		return null;
	}

	/** Called when the service is being created. */
	@Override
	public void onCreate() {

		LOG("BluetoothScanningService::onCreate");

		registeredActivity = AppController.getCurrentActivity();

		mBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
		mNewDevicesArrayAdapter = new ArrayList<SurroundingDevice>();
		// set bluetoothAddress of this device for the bundle
		deviceBundle = new SurroundingDeviceDataBundle();
		deviceBundle.setBtAddress(NetworkUtility.getBluetoothAddress());

		if (mTimer != null) {
			mTimer.cancel();
		} else {
			mTimer = new Timer();
		}
	}

	/** Called when The service is no longer used and is being destroyed */
	@Override
	public void onDestroy() {

		LOG("BluetoothScanningService::onDestroy");
		if (registeredActivity != null) {
			registeredActivity.unregisterReceiver(deviceBroadcastReceiver);
			registeredActivity.unregisterReceiver(adapterBroadcastReceiver);
		}
		// stop timer
		if (mTimer != null) {
			mTimer.cancel();
			mTimer.purge();
			mTimer = null;
		}
		LOG("Disconnect BluetoothScanningService");
		super.onDestroy();

	}

	@Override
	public int onStartCommand(Intent intent, int flags, int startId) {
		LOG("BluetoothScanningService::onStartCommand");

		mTimer.scheduleAtFixedRate(new ScanningTimerTask(), 0,
				Constants.BLUETOOTH_DEFAULT_SCANNING_SURROUNDING_DEVICE_TIME);

		return super.onStartCommand(intent, flags, startId);
	}

	class ScanningTimerTask extends TimerTask {
		public void run() {
			fetchSurroundingDevices();
		}
	}

	public void fetchSurroundingDevices() {
		// reset the list of detected Device first
		mNewDevicesArrayAdapter.clear();

		if (registeredActivity != null) {
			if (mBluetoothAdapter.isDiscovering()) {
				mBluetoothAdapter.cancelDiscovery();
			}
			mBluetoothAdapter.startDiscovery();

			// Register for broadcasts when a device is discovered
			IntentFilter filter = new IntentFilter(BluetoothDevice.ACTION_FOUND);
			registeredActivity
					.registerReceiver(deviceBroadcastReceiver, filter);

			// Register for broadcasts when discovery has finished
			IntentFilter intentFilter = new IntentFilter(
					BluetoothAdapter.ACTION_DISCOVERY_FINISHED);
			registeredActivity.registerReceiver(adapterBroadcastReceiver,
					intentFilter);
		}
	}

	private final BroadcastReceiver deviceBroadcastReceiver = new BroadcastReceiver() {
		@Override
		public void onReceive(Context context, Intent intent) {
			String action = intent.getAction();

			if (BluetoothDevice.ACTION_FOUND.equals(action)) {

				mBluetoothAdapter.cancelDiscovery();

				// get the BluetoothDevice object from the Intent
				BluetoothDevice device = intent
						.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE);
				short rssi = intent.getShortExtra(BluetoothDevice.EXTRA_RSSI,
						Short.MIN_VALUE);

				SurroundingDevice newDetectedDevice = new SurroundingDevice(
						device.getAddress(), Short.toString(rssi));
				// check whether the device is already inside the list
				if (!mNewDevicesArrayAdapter.contains(newDetectedDevice)) {

					// TODO: make sure this list doesn't contain iBeacon devices
					mNewDevicesArrayAdapter.add(newDetectedDevice);
				}
				mBluetoothAdapter.startDiscovery();
			}
		}
	};

	private final BroadcastReceiver adapterBroadcastReceiver = new BroadcastReceiver() {
		@Override
		public void onReceive(Context context, Intent intent) {
			String action = intent.getAction();

			if (BluetoothAdapter.ACTION_DISCOVERY_FINISHED.equals(action)) {
				// we check the list first and then use Retrofit service to send
				// data into server
				if (mNewDevicesArrayAdapter.size() > 0) {
					// only work if the application detect surrounding ibeacons
					if (IbeaconPostingService.isPossibleBeaconDiscoverred) {
						// update the detectedDevices
						deviceBundle
								.setDetectedDevices(mNewDevicesArrayAdapter);

						ObjectMapper mapper = new ObjectMapper(); // for testing
																	// purpose
						try {
							System.out.println(mapper
									.writeValueAsString(deviceBundle));
						} catch (IOException e) {
							e.printStackTrace();
						}
						SurroundingDeviceAPIHandler
								.postSurroundingDevices(deviceBundle);
					}
				}
			}
		}
	};

	private void LOG(String msg) {
		Log.d(TAG, msg);
		System.out.println(msg);
	}
}
