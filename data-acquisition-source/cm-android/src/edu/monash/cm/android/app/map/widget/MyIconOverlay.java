package edu.monash.cm.android.app.map.widget;

import android.content.Context;

import com.mapbox.mapboxsdk.overlay.ItemizedIconOverlay;
import com.mapbox.mapboxsdk.overlay.Marker;
import java.util.List;

public class MyIconOverlay extends ItemizedIconOverlay {

	public MyIconOverlay(Context pContext, List<Marker> pList,
			OnItemGestureListener<Marker> pOnItemGestureListener) {
		super(pContext, pList, pOnItemGestureListener);
	}

	public MyIconOverlay(Context pContext, List<Marker> pList,
			OnItemGestureListener<Marker> pOnItemGestureListener,
			boolean sortList) {
		super(pContext, pList, pOnItemGestureListener, sortList);
	}

	public boolean removeItem(final Marker item) {
		final boolean result = mItemList.remove(item);
		if (getFocus() == item) {
			setFocus(null);
		}
		if (result) {
			item.setParentHolder(null);
		}
		populate();
		return result;
	}
}