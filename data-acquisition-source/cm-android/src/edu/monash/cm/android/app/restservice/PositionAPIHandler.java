package edu.monash.cm.android.app.restservice;

import edu.monash.cm.android.app.utils.BaseAPIHandlerUtility;

public class PositionAPIHandler {
	public static String TAG = "PositionAPIHandler";

	public static PositionAPI getApiInterface() {

		PositionAPI positionAPI = null;
		try {
			positionAPI = BaseAPIHandlerUtility.getRestAdapter().create(
					PositionAPI.class);
		} catch (Exception e) {
			e.printStackTrace();
			System.out.println("Message " + e.getMessage());
		}
		return positionAPI;
	}

}
