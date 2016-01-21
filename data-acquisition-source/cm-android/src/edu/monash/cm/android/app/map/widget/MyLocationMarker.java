package edu.monash.cm.android.app.map.widget;

import android.graphics.Bitmap;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;

import com.mapbox.mapboxsdk.geometry.LatLng;
import com.mapbox.mapboxsdk.overlay.Icon;
import com.mapbox.mapboxsdk.overlay.Marker;
import com.mapbox.mapboxsdk.views.MapView;

import edu.monash.cm.android.app.AppController;

public class MyLocationMarker extends Marker {

	private Icon locationIcon;

	public MyLocationMarker(MapView mv, String aTitle, String aDescription,
			LatLng aLatLng, Drawable drawable) {
		super(mv, aTitle, aDescription, aLatLng);
		Bitmap b = ((BitmapDrawable) drawable).getBitmap();
		Bitmap bitmapResized = Bitmap.createScaledBitmap(b, 36, 36, false);
		Drawable resized =  new BitmapDrawable(AppController.getAppContext().getResources(), bitmapResized);
		this.setLocationIcon(new Icon(resized));
	}

	public MyLocationMarker(MapView mv, String aTitle, String aDescription,
			LatLng aLatLng) {
		super(mv, aTitle, aDescription, aLatLng);
	}

	public MyLocationMarker(String title, String description, LatLng latLng) {
		super(title, description, latLng);
	}

	@Override
	public Drawable getImage() {
		return super.getImage();
	}

	@Override
	public Drawable getDrawable() {
		return super.getDrawable();
	}

	public Icon getLocationIcon() {
		return locationIcon;
	}

	public void setLocationIcon(Icon locationIcon) {
		this.locationIcon = locationIcon;
	}

}
