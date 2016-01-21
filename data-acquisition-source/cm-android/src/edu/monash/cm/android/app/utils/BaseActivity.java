package edu.monash.cm.android.app.utils;

import edu.monash.cm.android.app.AppController;
import android.app.Activity;
import android.os.Bundle;
import android.support.v4.app.FragmentActivity;

public class BaseActivity extends FragmentActivity {

	protected AppController mMyApp;

	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		mMyApp = (AppController) this.getApplicationContext();
		AppController.setCurrentActivity(this);
	}

	protected void onResume() {
		super.onResume();
		AppController.setCurrentActivity(this);
	}

	protected void onPause() {
		clearReferences();
		super.onPause();
	}

	protected void onDestroy() {
		clearReferences();
		super.onDestroy();
	}

	private void clearReferences() {
		Activity currActivity = AppController.getCurrentActivity();
		if (currActivity != null && currActivity.equals(this))
			AppController.setCurrentActivity(null);
	}
}
