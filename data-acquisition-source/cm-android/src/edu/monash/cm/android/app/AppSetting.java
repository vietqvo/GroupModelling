package edu.monash.cm.android.app;

import java.util.Properties;

import org.codehaus.jackson.map.ObjectMapper;

import android.content.Context;
import android.content.SharedPreferences;
import android.content.SharedPreferences.Editor;
import edu.monash.cm.android.app.constant.Constants;
import edu.monash.cm.android.app.utils.ConfigReader;
import edu.monash.cm.model.layout.LayoutSize;

public class AppSetting {

	private static final String SERVER_URL = "serverUrl";
	private static final String TIMEOUT_REQ_SERVER = "timeoutRequestServer";
	private static final String CONFIG_FILE = "config.properties";
	private static final String USERNAME = "userName";
	public static final String DEVICE_INFORMATION_POSTED = "devicePosted";
	
	private static final String PHYSICAL_LAYOUT_SIZE = "physicLayout";
	private static final String MAP_LAYOUT_SIZE = "mapLayout";
	private static final String MAP_URL ="mapURL";
	
	private static SharedPreferences getGeneralSetting() {
		return AppController.getAppContext().getSharedPreferences(
				Constants.SETTING_GENERAL, Context.MODE_PRIVATE);
	}

	public static String getServerURL() {
		return getGeneralSetting().getString(AppSetting.SERVER_URL,
				Constants.EMPTY_STR).trim();
	}

	public static void setServerURL(String serverUrl) {
		getGeneralSetting().edit().putString(AppSetting.SERVER_URL, serverUrl)
				.apply();
	}

	public static int getTimeoutReqServer() {
		return getGeneralSetting().getInt(TIMEOUT_REQ_SERVER,
				Constants.DEFAULT_REQ_TIMEOUT);
	}

	public static void setTimeoutReqServer(int timeout) {
		getGeneralSetting().edit()
				.putInt(AppSetting.TIMEOUT_REQ_SERVER, timeout).apply();
	}

	public static void setUserName(String username) {
		getGeneralSetting().edit()
				.putString(AppSetting.USERNAME, username.trim()).apply();
	}

	public static String getUserName() {
		return getGeneralSetting().getString(AppSetting.USERNAME,
				Constants.EMPTY_STR);
	}

	public static void setDeviceInformationPosted(String status) {
		getGeneralSetting().edit()
				.putString(AppSetting.DEVICE_INFORMATION_POSTED, status.trim())
				.apply();
	}

	public static String getDeviceInformationPosted() {
		return getGeneralSetting().getString(
				AppSetting.DEVICE_INFORMATION_POSTED, Constants.EMPTY_STR);
	}

	public static LayoutSize getPhysicalLayoutSize() {
		String jsonLayout = getGeneralSetting().getString(
				AppSetting.PHYSICAL_LAYOUT_SIZE, Constants.EMPTY_STR);
		try {
			LayoutSize physicalLayout = new ObjectMapper().readValue(
					jsonLayout, LayoutSize.class);
			return physicalLayout;
		} catch (Exception e) {
			System.out.println("Exception converting getPhysicalLayoutSize "
					+ e.getMessage());
			return null;
		}
	}

	public static void setPhysicalLayoutSize(LayoutSize layoutsize) {
		getGeneralSetting()
				.edit()
				.putString(AppSetting.PHYSICAL_LAYOUT_SIZE,
						layoutsize.toString()).apply();
	}

	public static LayoutSize getMapLayoutSize() {
		String jsonLayout = getGeneralSetting().getString(
				AppSetting.MAP_LAYOUT_SIZE, Constants.EMPTY_STR);
		try {
			LayoutSize physicalLayout = new ObjectMapper().readValue(
					jsonLayout, LayoutSize.class);
			return physicalLayout;
		} catch (Exception e) {
			System.out.println("Exception converting getMapLayoutSize "
					+ e.getMessage());
			return null;
		}
	}

	public static void setMapLayoutSize(LayoutSize layoutsize) {
		getGeneralSetting().edit()
				.putString(AppSetting.MAP_LAYOUT_SIZE, layoutsize.toString())
				.apply();
	}

	public static void setMapURL(String mapURL){
		getGeneralSetting()
		.edit()
		.putString(AppSetting.MAP_URL,
				mapURL.toString()).apply();
	}
	
	public static String getMapURL(){
		return getGeneralSetting().getString(
				AppSetting.MAP_URL, Constants.EMPTY_STR);
	}
	
	public static void loadSettings(Context context) {

		// read default settings from config file
		ConfigReader reader = new ConfigReader(context);
		Properties properties = reader.readProperties(CONFIG_FILE);

		// general settings
		SharedPreferences generalSetting = getGeneralSetting();

		// check serverURL first to see sharedPreference is null
		String serverURL = getServerURL();
		if (serverURL.compareTo(Constants.EMPTY_STR) == 0) {

			Editor editor = generalSetting.edit();
			editor.putString(AppSetting.SERVER_URL, properties.getProperty(
					AppSetting.SERVER_URL, Constants.EMPTY_STR));
			editor.putInt(AppSetting.TIMEOUT_REQ_SERVER, Integer
					.parseInt(properties.getProperty(TIMEOUT_REQ_SERVER,
							String.valueOf(Constants.DEFAULT_REQ_TIMEOUT))));
			// save settings
			editor.commit();
		}
	}

}
