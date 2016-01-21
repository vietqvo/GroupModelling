package edu.monash.cm.android.app.utils;

import android.annotation.SuppressLint;
import android.app.AlertDialog;
import android.app.Dialog;
import android.bluetooth.BluetoothAdapter;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.net.wifi.WifiInfo;
import android.net.wifi.WifiManager;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.TextView;
import edu.monash.cm.android.R;

public class NetworkUtility {

	/***
	 * Network Utility Management
	 */
	public static boolean checkNetworkConnection(Context mContext) {
		ConnectivityManager connect = (ConnectivityManager) mContext
				.getSystemService(Context.CONNECTIVITY_SERVICE);
		NetworkInfo infoWifi = connect
				.getNetworkInfo(ConnectivityManager.TYPE_WIFI);
		NetworkInfo infoMobile = connect
				.getNetworkInfo(ConnectivityManager.TYPE_MOBILE);

		if (infoWifi.isConnected() || infoMobile.isConnected()) {
			return true;
		} else {
			return false;
		}
	}

	/***
	 * Network management Dialog appearance
	 */
	private static Dialog networkDialog = null;

	@SuppressLint("InflateParams")
	public static void alertNetworkDialog(final Context context) {

		// check whether the dialog has been already displaying
		if (networkDialog != null) {
			return;
		}
		// alert the network dialog
		LayoutInflater inflater = (LayoutInflater) context
				.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
		View layout = inflater.inflate(R.layout.networkdialog, null);
		TextView textView = (TextView) layout
				.findViewById(R.id.networkTextDialog);
		textView.setText(context.getResources().getText(
				R.string.connection_error_message));
		AlertDialog.Builder builder = new AlertDialog.Builder(context);
		builder.setTitle("Network Connection");
		builder.setView(layout);
		builder.setCancelable(false);
		builder.setPositiveButton(android.R.string.yes,
				new DialogInterface.OnClickListener() {

					@Override
					public void onClick(DialogInterface dialog, int which) {
						Intent intent = new Intent(
								android.provider.Settings.ACTION_WIFI_SETTINGS);
						context.startActivity(intent);
						networkDialog.dismiss();
						networkDialog = null;
					}
				});

		builder.setNegativeButton(android.R.string.no,
				new DialogInterface.OnClickListener() {

					@Override
					public void onClick(DialogInterface dialog, int which) {
						networkDialog.dismiss();
						networkDialog = null;
					}
				});

		builder.setIcon(android.R.drawable.ic_dialog_alert);
		try {
			networkDialog = builder.create();
			networkDialog.show();
		} catch (Exception e) {
			System.out.println("Exception " + e.getMessage());
		}
	}

	/***
	 * 
	 * get MAC address by Wifi
	 */
	public static String getMacAddress(Context context) {
		WifiManager wifiManager = (WifiManager) context
				.getSystemService(Context.WIFI_SERVICE);
		String address = null;
		if (wifiManager.isWifiEnabled()) {
			WifiInfo info = wifiManager.getConnectionInfo();
			address = info.getMacAddress();
		} else {
			wifiManager.setWifiEnabled(true);
			WifiInfo info = wifiManager.getConnectionInfo();
			address = info.getMacAddress();
		}
		return address;
	}

	/***
	 * @param Bluetooth
	 *            Utility Management
	 */

	// get Bluetooth Address
	public static String getBluetoothAddress() {
		BluetoothAdapter mBluetoothAdapter = BluetoothAdapter
				.getDefaultAdapter();
		return mBluetoothAdapter.getAddress();
	}

	public static void enableBlueTooth(Context context) {
		Intent enableBtIntent = new Intent(
				BluetoothAdapter.ACTION_REQUEST_ENABLE);
		enableBtIntent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
		context.startActivity(enableBtIntent);
	}

	public static void disableBluetooth() {
		BluetoothAdapter mBluetoothAdapter = BluetoothAdapter
				.getDefaultAdapter();
		if (mBluetoothAdapter.isEnabled()) {
			mBluetoothAdapter.disable();
		}
	}

	public static boolean isBlueToothEnabled() {
		BluetoothAdapter mBluetoothAdapter = BluetoothAdapter
				.getDefaultAdapter();
		return mBluetoothAdapter.isEnabled();
	}

	public static boolean checkBothOfNetworkAndBluetooth(Context mContext) {
		// check BlueTooth is active
		boolean isBluetoothEnabled = NetworkUtility.isBlueToothEnabled();

		boolean isNetworkEnabled = NetworkUtility
				.checkNetworkConnection(mContext);
		if (!isBluetoothEnabled || !isNetworkEnabled) {
			return false;
		}
		return true;
	}
}