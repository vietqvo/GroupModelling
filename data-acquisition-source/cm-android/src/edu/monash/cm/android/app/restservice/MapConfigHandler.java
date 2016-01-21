package edu.monash.cm.android.app.restservice;

import retrofit.Callback;
import retrofit.RetrofitError;
import retrofit.client.Response;
import retrofit.http.GET;
import edu.monash.cm.android.app.AppSetting;
import edu.monash.cm.android.app.map.controller.MapConfiguration;
import edu.monash.cm.android.app.utils.BaseAPIHandlerUtility;
import edu.monash.cm.model.layout.MapModel;

public class MapConfigHandler {
	public static String TAG = "MapConfigHandler";

	interface MapConfigAPI {
		@GET("/api/map/model")
		void getMapConfiguration(Callback<MapModel> callback);
	}
	
	public static void setMapConfiguration() {

		MapConfigAPI mapAPI = null;
		try {
			mapAPI = BaseAPIHandlerUtility.getRestAdapter().create(
					MapConfigAPI.class);
			
			mapAPI.getMapConfiguration(getMapConfigCallBackFunction());
		} catch (Exception e) {
			e.printStackTrace();
			System.out.println("Message " + e.getMessage());
		}
	}
	
	public static Callback<MapModel> getMapConfigCallBackFunction() {

		Callback<MapModel> mCallback = new Callback<MapModel>() {

			@Override
			public void failure(RetrofitError arg0) {
				System.out.println(">>>" +  "getMapConfigCallBackFunction" + " failed : " + arg0);
			}

			@Override
			public void success(MapModel mapModel, Response arg1) {
				if(mapModel.getPhysicalLayout()!= null && mapModel.getImageMapLayout() !=null && mapModel.getImageMapURL()!=""){
					MapConfiguration.setPhysicalLayout(mapModel.getPhysicalLayout());
					MapConfiguration.setImageMapLayout(mapModel.getImageMapLayout());
					MapConfiguration.setImageMapURL(mapModel.getImageMapURL());
					
					//set SharePreference
					AppSetting.setPhysicalLayoutSize(mapModel.getPhysicalLayout());
					AppSetting.setMapLayoutSize(mapModel.getImageMapLayout());
					AppSetting.setMapURL(mapModel.getImageMapURL());
					
					System.out.println(">>>" +  "getMapConfigCallBackFunction"  + " successful : " + arg1);
				}						
			}

		};
		return mCallback;
	}
}
