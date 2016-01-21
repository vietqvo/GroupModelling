package edu.monash.cm.android.app.restservice;

import retrofit.Callback;
import retrofit.http.Body;
import retrofit.http.POST;
import edu.monash.cm.android.app.utils.BaseAPIHandlerUtility;
import edu.monash.cm.model.beacon.BeaconDataBundle;

public class IbeaconAPIHandler {
	
	public static String TAG= "IbeaconAPIHandler";
	
	interface SurroundingIbeaconAPI {
		@POST("/api/nearby/ibeacon")
		void postSurroundingIbeacons(@Body BeaconDataBundle data,
				Callback<String> cb);
	}

	public static SurroundingIbeaconAPI getApiInterface() {

		SurroundingIbeaconAPI nearbyIbeaconAPI = null;
		try {
			nearbyIbeaconAPI = BaseAPIHandlerUtility.getRestAdapter().create(
					SurroundingIbeaconAPI.class);
		} catch (Exception e) {
			e.printStackTrace();
			System.out.println("Message " + e.getMessage());
		}
		return nearbyIbeaconAPI;
	}

	public static void postSurroundingDevices(BeaconDataBundle beaconDataBundle) {
		SurroundingIbeaconAPI surroundingIbeaconAPI = IbeaconAPIHandler
				.getApiInterface();
		if (surroundingIbeaconAPI != null) {
			surroundingIbeaconAPI.postSurroundingIbeacons(beaconDataBundle,
					BaseAPIHandlerUtility.getCallBackFunction(TAG));
		}
	}
}
