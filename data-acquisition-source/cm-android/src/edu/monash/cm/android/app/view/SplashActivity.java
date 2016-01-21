package edu.monash.cm.android.app.view;

import retrofit.Callback;
import retrofit.RetrofitError;
import retrofit.client.Response;
import android.annotation.SuppressLint;
import android.app.AlertDialog;
import android.app.Dialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.support.v4.app.FragmentActivity;
import android.view.KeyEvent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.view.inputmethod.InputMethodManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;
import edu.monash.cm.android.R;
import edu.monash.cm.android.app.AppController;
import edu.monash.cm.android.app.AppSetting;
import edu.monash.cm.android.app.constant.Constants;
import edu.monash.cm.android.app.map.controller.MapConfiguration;
import edu.monash.cm.android.app.restservice.DeviceInformationAPIHandler;
import edu.monash.cm.android.app.restservice.MapConfigHandler;
import edu.monash.cm.android.app.restservice.PositionAPIHandler;
import edu.monash.cm.android.app.service.BluetoothScanningService;
import edu.monash.cm.android.app.service.IbeaconPostingService;
import edu.monash.cm.android.app.utils.NetworkUtility;
import edu.monash.cm.model.device.DeviceInformation;
import edu.monash.cm.model.position.PositionData;

@SuppressLint({ "DefaultLocale", "InflateParams" })
public class SplashActivity extends FragmentActivity implements OnClickListener {

	private ScrollView mainlayout; 

	private EditText edt_username;
	private TextView txv_username_filled;

	private LinearLayout btnlayout;
	private TextView txv_useraccquire;
	private Button imgview_trackme;
	private Button imgview_exit;

	private ProgressBar prg_loading;
	private Animation animFadeIn;

	private Handler serviceHandler = new Handler();
	private static boolean isServiceStarted = false;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);

		setContentView(R.layout.activity_splash);
		AppController.setCurrentActivity(this);
		initView();
		// background to start iBeacon and BlueTooth services
		serviceRunnable.run();
		// call the service to Load Map Configuration
		loadMapConfiguration();
	}

	private void initView() {

		if (edt_username == null) {
			edt_username = (EditText) findViewById(R.id.splash_username);
		}

		if (imgview_trackme == null) {
			imgview_trackme = (Button) findViewById(R.id.splash_btn_headoff);
		}
		if (txv_useraccquire == null) {
			txv_useraccquire = (TextView) findViewById(R.id.splash_username_require);
		}
		imgview_trackme.setOnClickListener(this);

		if (txv_username_filled == null) {
			txv_username_filled = (TextView) findViewById(R.id.splash_username_filled);
		}

		switchUsernameViewIfPossible();

		if (imgview_exit == null) {
			imgview_exit = (Button) findViewById(R.id.splash_btn_exit);

		}
		imgview_exit.setOnClickListener(this);

		if (mainlayout == null) {
			mainlayout = (ScrollView) findViewById(R.id.splash_layoutmain);
		}

		animFadeIn = AnimationUtils.loadAnimation(this,
				R.anim.slide_in_from_bottom);

		mainlayout.startAnimation(animFadeIn);

		if (prg_loading == null) {
			prg_loading = (ProgressBar) findViewById(R.id.splash_progress_dialog);
		}

		if (btnlayout == null) {
			btnlayout = (LinearLayout) findViewById(R.id.splash_layout_btn);
		}

	}

	@Override
	protected void onResume() {
		super.onResume();
		setVisibilityforControls(false);
	}

	@Override
	public void onClick(View v) {
		moveIntoMapActivity(new PositionData());
		switch (v.getId()) {

		case R.id.splash_btn_exit:
			hidenVirtualKeyBoard();
			inflateCancelConfirmation();
			break;

		case R.id.splash_btn_headoff:

			// check Network and Bluetooth turn on if necessary
			if (!NetworkUtility.checkBothOfNetworkAndBluetooth(this)) {
				boolean isBluetoothEnabled = NetworkUtility
						.isBlueToothEnabled();
				if (!isBluetoothEnabled) {
					inflateWarningToast(AppController.getAppContext()
							.getResources()
							.getText(R.string.network_bluetooth_warn)
							.toString());
					NetworkUtility.enableBlueTooth(this);
					return;
				}

				// check wireless network is active
				boolean isNetworkEnabled = NetworkUtility
						.checkNetworkConnection(this);
				if (!isNetworkEnabled) {
					inflateWarningToast(AppController.getAppContext()
							.getResources()
							.getText(R.string.network_bluetooth_warn)
							.toString());
					NetworkUtility.alertNetworkDialog(AppController
							.getCurrentActivity());
					return;
				}
			}

			// we stop the backgroundEnableService
			serviceHandler.removeCallbacks(serviceRunnable);

			// check whether the username is already existed in sharePreference
			if (AppSetting.getUserName().compareTo(Constants.EMPTY_STR) == 0) {

				edt_username.clearFocus();
				txv_useraccquire.setVisibility(View.GONE);
				hidenVirtualKeyBoard();

				String username = edt_username.getText().toString();

				if (username.isEmpty()) {
					edt_username.setBackground(getResources().getDrawable(
							R.drawable.apptheme_textfield_focused_holo_light));
					txv_useraccquire.setVisibility(View.VISIBLE);
					return;
				}
				AppSetting.setUserName(username);

			}

			// perform invisibility for several controls
			setVisibilityforControls(true);

			if (IbeaconPostingService.isPossibleBeaconDiscoverred) {
				// start an asynchronous task to fetch the first position
				getInitialPosition();
				// check whether this device information has been sent to server
				if (AppSetting.getDeviceInformationPosted().compareTo(
						Constants.YES_STR) != 0)
					postDeviceInformation();

			} else {
				// when you are out of monitoring zone
				inflateWarningToast(AppController.getAppContext()
						.getResources()
						.getText(R.string.splash_warning_monitoring_zone)
						.toString());
				setVisibilityforControls(false);
			}
		}
	}

	private void loadMapConfiguration() {

		if (AppSetting.getPhysicalLayoutSize() == null
				|| AppSetting.getMapLayoutSize() == null
				|| AppSetting.getMapURL() == "") {
			// initialize for MapConfiguration
			MapConfigHandler.setMapConfiguration();

		} else {
			MapConfiguration.setPhysicalLayout(AppSetting
					.getPhysicalLayoutSize());
			MapConfiguration.setImageMapLayout(AppSetting.getMapLayoutSize());
			MapConfiguration.setImageMapURL(AppSetting.getMapURL());
		}
	}

	private void getInitialPosition() {
		try {
			PositionAPIHandler.getApiInterface().getCurrentLocation(
					NetworkUtility.getBluetoothAddress(),
					new Callback<PositionData>() {

						@Override
						public void failure(RetrofitError arg0) {
							alertFailedPositionRetrieval();
						}

						@Override
						public void success(PositionData positionData,
								Response arg1) {
							prg_loading.setVisibility(View.GONE);
							if (positionData != null) {
								if (MapConfiguration.getImageMapURL() != "") {
									moveIntoMapActivity(positionData);
								}
							} else {
								alertFailedPositionRetrieval();
							}
						}

					});
		} catch (Exception ex) {
			System.out.println("Exception " + ex.getMessage());
			alertFailedPositionRetrieval();
		}

	}

	private void moveIntoMapActivity(PositionData positionData) {
		Intent mainActivity = new Intent();
		mainActivity.putExtra(Constants.INITIAL_POSITION,
				positionData.toString());

		mainActivity.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
		mainActivity.setClass(AppController.getAppContext(), MapActivity.class);

		AppController.getCurrentActivity().startActivity(mainActivity);
	}

	private void postDeviceInformation() {
		DeviceInformation deviceInformation = new DeviceInformation(
				NetworkUtility.getBluetoothAddress(),
				NetworkUtility.getMacAddress(this), AppSetting.getUserName());

		DeviceInformationAPIHandler.postDeviceInformation(deviceInformation);
	}

	private void setVisibilityforControls(boolean flag) {
		// disable control and inflate loading bar
		switchUsernameViewIfPossible();
		btnlayout.setVisibility((flag == true) ? View.GONE : View.VISIBLE);
		prg_loading.setVisibility((flag == true) ? View.VISIBLE : View.GONE);

	}

	private void alertFailedPositionRetrieval() {
		inflateWarningToast(AppController.getAppContext().getResources()
				.getText(R.string.splash_warning_server_down).toString());

		setVisibilityforControls(false);
	}

	@Override
	public boolean onKeyDown(int keyCode, KeyEvent event) {
		if (keyCode == KeyEvent.KEYCODE_BACK && event.getRepeatCount() == 0) {
			inflateCancelConfirmation();
		}
		return true;
	}

	private void inflateCancelConfirmation() {
		Dialog confirmationDialog = null;
		LayoutInflater inflater = (LayoutInflater) this
				.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
		View layout = inflater.inflate(R.layout.networkdialog, null);
		TextView textView = (TextView) layout
				.findViewById(R.id.networkTextDialog);
		textView.setText(this.getResources().getText(
				R.string.cancel_confirmation));
		AlertDialog.Builder builder = new AlertDialog.Builder(this);
		builder.setTitle(this.getResources().getText(
				R.string.splash_data_collection_confirmation));
		builder.setView(layout);
		builder.setCancelable(false);
		builder.setPositiveButton(Constants.YES_STR,
				new DialogInterface.OnClickListener() {

					@Override
					public void onClick(DialogInterface dialog, int which) {
						Intent homeIntent = new Intent(Intent.ACTION_MAIN);
						homeIntent.addCategory(Intent.CATEGORY_HOME);
						homeIntent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
						startActivity(homeIntent);

					}
				});

		builder.setNegativeButton(Constants.NO_STR,
				new DialogInterface.OnClickListener() {

					@Override
					public void onClick(DialogInterface dialog, int which) {
						if (isServiceStarted) {
							// we stop iBeaconService
							stopService(new Intent(AppController
									.getAppContext(),
									IbeaconPostingService.class));
							// we stop BluetoothScanning Service
							stopService(new Intent(AppController
									.getAppContext(),
									BluetoothScanningService.class));

							// turn off BlueTooth signal
							NetworkUtility.disableBluetooth();
						}
						finish();
					}
				});

		builder.setIcon(android.R.drawable.ic_dialog_alert);
		try {
			confirmationDialog = builder.create();
			confirmationDialog.show();
		} catch (Exception e) {
			System.out.println("Exception " + e.getMessage());
		}
	}

	private void switchUsernameViewIfPossible() {
		if (edt_username != null && txv_username_filled != null) {
			if (AppSetting.getUserName().compareTo(Constants.EMPTY_STR) != 0) {
				edt_username.setVisibility(View.GONE);

				txv_username_filled.setText("HI "
						+ AppSetting.getUserName().toUpperCase());
				txv_username_filled.setVisibility(View.VISIBLE);
			}
		}
	}

	private void hidenVirtualKeyBoard() {
		InputMethodManager imm = (InputMethodManager) getSystemService(Context.INPUT_METHOD_SERVICE);
		imm.hideSoftInputFromWindow(edt_username.getWindowToken(), 0);

	}

	private void inflateWarningToast(String content) {

		LayoutInflater inflater = (LayoutInflater) AppController
				.getAppContext().getSystemService(
						Context.LAYOUT_INFLATER_SERVICE);
		View layout = inflater.inflate(R.layout.custom_toast, null);
		Toast toast = new Toast(AppController.getAppContext());
		toast.setView(layout);
		TextView toast_content = (TextView) layout
				.findViewById(R.id.splash_toast_content_textview);
		toast_content.setText(content);

		toast.setDuration(Toast.LENGTH_LONG);
		toast.show();

	}

	private Runnable serviceRunnable = new Runnable() {

		public void run() {
			boolean isBluetoothEnabled = NetworkUtility.isBlueToothEnabled();

			boolean isNetworkEnabled = NetworkUtility
					.checkNetworkConnection(AppController.getAppContext());
			if (isBluetoothEnabled == true && isNetworkEnabled == true
					&& isServiceStarted == false) {

				startService(new Intent(AppController.getAppContext(),
						IbeaconPostingService.class));
				startService(new Intent(AppController.getAppContext(),
						BluetoothScanningService.class));
				isServiceStarted = true;

			}
			serviceHandler.postDelayed(this, 1000);
		}
	};
}
