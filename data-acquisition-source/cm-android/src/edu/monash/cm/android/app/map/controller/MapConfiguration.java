package edu.monash.cm.android.app.map.controller;

import edu.monash.cm.model.layout.LayoutSize;

public class MapConfiguration {
	private static LayoutSize physicalLayout;
	private static LayoutSize imageMapLayout;
	private static String imageMapURL;

	public MapConfiguration() {
		physicalLayout = null;
		imageMapLayout = null;
		imageMapURL = "";
	}

	public static LayoutSize getPhysicalLayout() {
		return physicalLayout;
	}

	public static void setPhysicalLayout(LayoutSize physicalLayout) {
		MapConfiguration.physicalLayout = physicalLayout;
	}

	public static LayoutSize getImageMapLayout() {
		return imageMapLayout;
	}

	public static void setImageMapLayout(LayoutSize imageMapLayout) {
		MapConfiguration.imageMapLayout = imageMapLayout;
	}

	public static String getImageMapURL() {
		return imageMapURL;
	}

	public static void setImageMapURL(String imageMapURL) {
		MapConfiguration.imageMapURL = imageMapURL;
	}
}
