package edu.monash.cm.android.app.restservice;

import retrofit.Callback;
import retrofit.RetrofitError;
import retrofit.client.Response;
import retrofit.http.Body;
import retrofit.http.POST;
import edu.monash.cm.android.app.AppSetting;
import edu.monash.cm.android.app.constant.Constants;
import edu.monash.cm.android.app.utils.BaseAPIHandlerUtility;
import edu.monash.cm.model.device.DeviceInformation;

public class DeviceInformationAPIHandler {
	public static String TAG = "DeviceInformationAPIHandler";

	interface DeviceInformationAPI {
		@POST("/api/info/device")
		void postDeviceInformation(@Body DeviceInformation data,
				Callback<String> cb);
	}

	public static DeviceInformationAPI getApiInterface() {

		DeviceInformationAPI deviceInformationAPI = null;
		try {
			deviceInformationAPI = BaseAPIHandlerUtility.getRestAdapter().create(
					DeviceInformationAPI.class);
		} catch (Exception e) {
			e.printStackTrace();
			System.out.println("Message " + e.getMessage());
		}
		return deviceInformationAPI;
	}

	public static void postDeviceInformation(DeviceInformation deviceInformation) {
		DeviceInformationAPI deviceInformationAPI = DeviceInformationAPIHandler
				.getApiInterface();
		if (deviceInformation != null) {
			deviceInformationAPI.postDeviceInformation(deviceInformation,
					getCallBackFunction());
		}
	}

	private static Callback<String> getCallBackFunction() {

		Callback<String> mCallback = new Callback<String>() {

			@Override
			public void failure(RetrofitError arg0) {
				System.out.println(">>>" + TAG + " failed : " + arg0);
				AppSetting.setDeviceInformationPosted(Constants.NO_STR);
			}

			@Override
			public void success(String arg0, Response arg1) {
				System.out.println(">>>" + TAG + " successful : " + arg1);
				AppSetting.setDeviceInformationPosted(Constants.YES_STR);
			}

		};
		return mCallback;
	}

}
