package edu.monash.cm.android.app.utils;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

import android.content.Context;
import android.content.res.AssetManager;
import android.util.Log;

public class ConfigReader {
	private Context context;
	private Properties properties;

	public ConfigReader(Context context) {
		this.context = context;
		/**
		 * Constructs a new Properties object.
		 */
		properties = new Properties();
	}

	public Properties readProperties(String fileName) {

		try {
			/**
			 * getAssets() Return an AssetManager instance for your
			 * application's package. AssetManager Provides access to an
			 * application's raw asset files;
			 */
			AssetManager assetManager = context.getAssets();
			/**
			 * Open an asset using ACCESS_STREAMING mode. This
			 */
			InputStream inputStream = assetManager.open(fileName);
			/**
			 * Loads properties from the specified InputStream,
			 */
			properties.load(inputStream);

		} catch (IOException e) {
			Log.e("PropertyReader", e.toString());
		}
		return properties;
	}
}
