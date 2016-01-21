package edu.monash.cm.android.app.restservice;

import retrofit.Callback;
import retrofit.http.Body;
import retrofit.http.POST;
import edu.monash.cm.android.app.utils.BaseAPIHandlerUtility;
import edu.monash.cm.model.surround.SurroundingDeviceDataBundle;

public class SurroundingDeviceAPIHandler {

	public static String TAG = "SurroundingDeviceAPIHandler";

	interface SurroundingDeviceAPI {
		@POST("/api/nearby/device")
		void postSurroundingDevices(@Body SurroundingDeviceDataBundle data,
				Callback<String> cb);
	}

	public static SurroundingDeviceAPI getApiInterface() {

		SurroundingDeviceAPI nearbyDeviceAPI = null;
		try {
			nearbyDeviceAPI = BaseAPIHandlerUtility.getRestAdapter().create(
					SurroundingDeviceAPI.class);
		} catch (Exception e) {
			e.printStackTrace();
			System.out.println("Message " + e.getMessage());
		}
		return nearbyDeviceAPI;
	}

	public static void postSurroundingDevices(
			SurroundingDeviceDataBundle deviceBundle) {
		SurroundingDeviceAPI surroundingDeviceAPI = SurroundingDeviceAPIHandler
				.getApiInterface();
		if (surroundingDeviceAPI != null) {
			surroundingDeviceAPI.postSurroundingDevices(deviceBundle,
					BaseAPIHandlerUtility.getCallBackFunction(TAG));

		}
	}
}
