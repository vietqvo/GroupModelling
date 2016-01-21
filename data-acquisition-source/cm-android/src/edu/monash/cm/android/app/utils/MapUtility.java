package edu.monash.cm.android.app.utils;

import org.osmdroid.util.GeoPoint;
import org.osmdroid.util.TileSystem;

import edu.monash.cm.android.app.map.controller.MapConfiguration;
import edu.monash.cm.model.layout.LayoutSize;

public class MapUtility {

	public static GeoPoint convertToLatLng(float x, float y) {

		LayoutSize physicalLayoutSize = MapConfiguration.getPhysicalLayout();
		LayoutSize imageMapSize = MapConfiguration.getImageMapLayout();
		int maxPixcel;

		if (physicalLayoutSize == null || imageMapSize == null) {
			return new GeoPoint(0, 0);
		}
		int maxZoom = 0;
		if (imageMapSize.getWidth() >= imageMapSize.getLength()) {
			maxZoom = (int) (Math.log(imageMapSize.getWidth() / 256) / Math
					.log(2));
			maxPixcel = (int) imageMapSize.getWidth();
		} else {
			maxZoom = (int) (Math.log(imageMapSize.getLength() / 256) / Math
					.log(2));
			maxPixcel = (int) imageMapSize.getLength();
		}

		int convertX = (int) ((x / physicalLayoutSize.getWidth())
				* imageMapSize.getWidth() + (maxPixcel - imageMapSize
				.getWidth()) / 2);
		int convertY = (int) ((y / physicalLayoutSize.getLength())
				* imageMapSize.getLength() + (maxPixcel - imageMapSize
				.getLength()) / 2);

		return TileSystem.PixelXYToLatLong(convertX, convertY, maxZoom, null);
	}
}
