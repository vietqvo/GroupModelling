package edu.monash.cm.android.app.service;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.codehaus.jackson.map.ObjectMapper;

import com.estimote.sdk.Beacon;
import com.estimote.sdk.BeaconManager;
import com.estimote.sdk.Region;
import com.estimote.sdk.Utils;

import edu.monash.cm.android.app.AppController;
import edu.monash.cm.android.app.constant.Constants;
import edu.monash.cm.android.app.restservice.IbeaconAPIHandler;
import edu.monash.cm.android.app.utils.BluetoothCrashResolver;
import edu.monash.cm.android.app.utils.NetworkUtility;
import edu.monash.cm.model.beacon.BeaconDataBundle;
import edu.monash.cm.model.beacon.BeaconDevice;
import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.os.RemoteException;
import android.util.Log;

public class IbeaconPostingService extends Service {
	private static final String TAG = "IbeaconPostingService";

	private BluetoothCrashResolver bluetoothCrashResolver;

	private BeaconManager beaconManager;

	private BeaconDataBundle beaconDataBundle;

	public static boolean isPossibleBeaconDiscoverred;

	@Override
	public IBinder onBind(Intent intent) {
		return null;
	}

	/** Called when the service is being created. */
	@Override
	public void onCreate() {
		LOG("LocationPositingService::onCreate");

		bluetoothCrashResolver = new BluetoothCrashResolver(this);
		bluetoothCrashResolver.disableDebug();

		// set BlueTooth Address for this bundle
		beaconDataBundle = new BeaconDataBundle();
		beaconDataBundle.setBtAddress(NetworkUtility.getBluetoothAddress());

		// construct beacon manager
		beaconManager = new BeaconManager(AppController.getAppContext());
		beaconManager.setForegroundScanPeriod(
				Constants.IBEACON_DEFAULT_SCANNING_TIME,
				Constants.IBEACON_DEFAULT_SLEEPING_TIME);

		// declare action when iBeacons discovered
		beaconManager.setRangingListener(new BeaconManager.RangingListener() {
			@Override
			public void onBeaconsDiscovered(Region region,
					final List<Beacon> beacons) {
				LOG("Ranged beacons : " + beacons);

				List<BeaconDevice> list = new ArrayList<BeaconDevice>();
				if (list.size() != 0) {
					for (Beacon beacon : beacons) {
						list.add(new BeaconDevice(beacon.getMacAddress(), Utils
								.computeAccuracy(beacon), beacon.getRssi()));
					}

					beaconDataBundle.setDetectedBeacons(list);
					IbeaconAPIHandler.postSurroundingDevices(beaconDataBundle);

					isPossibleBeaconDiscoverred = true;
				} else {
					isPossibleBeaconDiscoverred = false;
				}
			}
		});

		// initial the possibility to collect surrounding iBeacons
		isPossibleBeaconDiscoverred = false;
	}

	@Override
	public int onStartCommand(Intent intent, int flags, int startId) {
		LOG("LocationPositingService::onStartCommand");

		// active beacon manager
		beaconManager.connect(new BeaconManager.ServiceReadyCallback() {
			@Override
			public void onServiceReady() {
				try {
					LOG("Start ranging...");
					beaconManager.startRanging(Constants.ALL_ESTIMOTE_BEACONS);
				} catch (RemoteException e) {
					LOG("Cannot start ranging : " + e);
				}
			}
		});
		return super.onStartCommand(intent, flags, startId);
	}

	/** Called when The service is no longer used and is being destroyed */
	@Override
	public void onDestroy() {
		// stop iBeacon service
		try {
			LOG("LocationPositingService::onDestroy");

			bluetoothCrashResolver.stop();
			LOG("Disconnect bluetoothCrashResolver");

			beaconManager.stopRanging(Constants.ALL_ESTIMOTE_BEACONS);
			beaconManager.disconnect();

			LOG("Disconnect beaconManager");

		} catch (Exception e) {
			LOG("Exception : " + e);
			e.printStackTrace();
		}
		super.onDestroy();

	}

	private void LOG(String msg) {
		Log.d(TAG, msg);
		System.out.println(msg);
	}

}
