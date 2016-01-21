package edu.monash.cm.android.app.constant;

import com.estimote.sdk.Region;

public class Constants {
	public static final String ESTIMOTE_PROXIMITY_UUID = "B9407F30-F5F8-466E-AFF9-25556B57FE6D";
	public static final Region ALL_ESTIMOTE_BEACONS = new Region("regionId",
			ESTIMOTE_PROXIMITY_UUID, null, null);

	/***
	 * constants period for Ibeacon working mechanism
	 */
	public static final int IBEACON_DEFAULT_SCANNING_TIME = 1000;// every second
	public static final int IBEACON_DEFAULT_SLEEPING_TIME = 1000;

	/***
	 * constants period for BlueTooth scanning period
	 */
	public static final int BLUETOOTH_DEFAULT_SCANNING_SURROUNDING_DEVICE_TIME = 100000;// 600000;//
																						// 10
																						// minutes

	/***
	 * constants for share preference storage
	 */
	public static final String SETTING_GENERAL = "CrowdModel_Setting";
	public static final String EMPTY_STR = "";
	public static final String DEVICE_INFORMATION_POSTED = "";
	public static final int DEFAULT_REQ_TIMEOUT = 3000;
	public static final String YES_STR = "Yes";
	public static final String NO_STR = "No";

	public static final String INITIAL_POSITION = "initial_position";
}
