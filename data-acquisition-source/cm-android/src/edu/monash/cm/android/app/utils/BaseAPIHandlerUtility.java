package edu.monash.cm.android.app.utils;

import retrofit.Callback;
import retrofit.RestAdapter;
import retrofit.RetrofitError;
import retrofit.client.Response;
import edu.monash.cm.android.app.AppSetting;

public class BaseAPIHandlerUtility {
	private static RestAdapter restAdapter;

	public static RestAdapter getRestAdapter() {
		if (restAdapter == null) {
			restAdapter = new RestAdapter.Builder().setEndpoint(AppSetting.getServerURL())
					.build();
		}
		return restAdapter;
	}
	
	public static Callback<String> getCallBackFunction(final String callingFunction) {

		Callback<String> mCallback = new Callback<String>() {

			@Override
			public void failure(RetrofitError arg0) {
				System.out.println(">>>" +  callingFunction + " failed : " + arg0);
			}

			@Override
			public void success(String arg0, Response arg1) {
				System.out.println(">>>" +  callingFunction + " successful : " + arg1);
			}

		};
		return mCallback;
	}

}
