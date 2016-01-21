package edu.monash.cm.android.app.map.widget;

import java.util.ArrayList;
import java.util.List;

import org.osmdroid.util.GeoPoint;

import uk.co.senab.bitmapcache.CacheableBitmapDrawable;
import android.content.Context;
import android.graphics.drawable.Drawable;
import android.view.View;

import com.mapbox.mapboxsdk.geometry.LatLng;
import com.mapbox.mapboxsdk.overlay.Marker;
import com.mapbox.mapboxsdk.tileprovider.MapTile;
import com.mapbox.mapboxsdk.tileprovider.modules.MapTileDownloader;
import com.mapbox.mapboxsdk.tileprovider.tilesource.ITileLayer;
import com.mapbox.mapboxsdk.tileprovider.tilesource.WebSourceTileLayer;
import com.mapbox.mapboxsdk.views.MapView;

import edu.monash.cm.android.R;
import edu.monash.cm.android.app.map.controller.AbsMapController;
import edu.monash.cm.android.app.utils.MapUtility;
import edu.monash.cm.model.position.PositionData;

public class MapController extends AbsMapController {

	private List<Marker> markers;
	private MyLocationMarker currentLocationMarker;
	private float posX;
	private float posY;
	private MyIconOverlay itemOverlay = null;

	public MapController(View _view, Context _context) {
		super(_view, _context);
		markers = new ArrayList<Marker>();
		currentLocationMarker = null;
		posX = posY = 0;

		itemOverlay = new MyIconOverlay(getMapView().getContext(),
				new ArrayList<Marker>(), null);
		getMapView().addOverlay(itemOverlay);
	}

	@Override
	public void updateCurrentLocation(PositionData data) {
		if (data == null) {
			return;
		}

		if (posX == 0 && posY == 0) {
			posX = data.getLongitude();
			posY = data.getLatitude();
		}
		if (posX != data.getLongitude() || posY != data.getLatitude()) {
			posX = data.getLongitude();
			posY = data.getLatitude();
		}

		GeoPoint loc = MapUtility.convertToLatLng(data.getLongitude(),
				data.getLatitude());
		LatLng curLocLatLng = new LatLng(loc.getLatitude(), loc.getLongitude());
		//LatLng curLocLatLng = new LatLng(-37.852755,  145.002016);
		if (currentLocationMarker == null) {

			Drawable drawable = null;
			drawable = context.getResources().getDrawable(
					R.drawable.userlocation2);
			currentLocationMarker = new MyLocationMarker(getMapView(), "", "",
					curLocLatLng, drawable);

			//itemOverlay.addItem(currentLocationMarker);
			getMapView().setCenter(curLocLatLng);
			getMapView().invalidate();
		} else {
			currentLocationMarker.setPoint(curLocLatLng);
		}
	}

	@Override
	public void displayMap(PositionData initialData) {
		resetMapController();
		/***
		 * display Map with background is downloaded bitmap
		 */
		getMapView().getTileProvider().setDiskCacheEnabled(false);
		// example: MapConfiguration.getImageMapURL()
		//http://s12.postimg.org/wr0wxok8t/indoormap.png
		ITileLayer aTileSource = new WebSourceTileLayer("gmap",
				"http://s12.postimg.org/wr0wxok8t/indoormap.png") {
			@Override
			public CacheableBitmapDrawable getDrawableFromTile(
					MapTileDownloader arg0, MapTile arg1, boolean arg2) {
				return super.getDrawableFromTile(arg0, arg1, arg2);
			}
		};

		getMapView().setTileSource(aTileSource);
		/***
		 * show user current position
		 */
		updateCurrentLocation(initialData);
	}

	private void resetMapController() {
		if (itemOverlay != null) {
			itemOverlay.removeAllItems();
		}
		clearCurrentLocation();
		getMapView().clear();
		getMapView().getTileProvider().clearTileMemoryCache();
	}

	@Override
	public void clearCurrentLocation() {
		if (currentLocationMarker != null) {
			itemOverlay.removeItem(currentLocationMarker);
			currentLocationMarker = null;

			getMapView().invalidate();
		}
	}

	@Override
	public void setMapViewCenter(PositionData center) {
		GeoPoint geoPoint = MapUtility.convertToLatLng(center.getLongitude(), center.getLatitude());
		getMapView().setCenter(
				new LatLng(geoPoint.getLatitude(), geoPoint.getLongitude()));
	}

	
	public List<Marker> getMarkers() {
		return markers;
	}

	public void setMarkers(List<Marker> markers) {
		this.markers = markers;
	}

	public float getPosX() {
		return posX;
	}

	public void setPosX(float posX) {
		this.posX = posX;
	}

	public float getPosY() {
		return posY;
	}

	public void setPosY(float posY) {
		this.posY = posY;
	}

	public Marker getCurrentLocationMarker() {
		return currentLocationMarker;
	}

	public void setCurrentLocationMarker(MyLocationMarker currentLocationMarker) {
		this.currentLocationMarker = currentLocationMarker;
	}

	public MapView getMapView() {
		return (MapView) mapView;
	}

}
