def create_item(item_type, item_data, trip_id):
    """Adds detaisl related to a particular trip to the database."""

    router_map = {"event": Event,
                  "flight": Flight,
                  "hotel": Hotel,
                  "car-rental": CarRental,
                  "public-transportation": PublicTransportation,
                  "meeting": Meeting}

    if item_type in router_map:
        instance = router_map[item_type]()
 
    for key in item_data:
        if item_data[key]:
            if key == "start-date":
                instance.starts_at = make_start_datetime_obj()
            elif key == "end-date":
                instance.ends_at = make_end_datetime_obj()
            elif key == "start-time" or key == "end-time":
                continue
            else:
                setattr(instance, key, item_data[key]

    instance.trip_id = trip_id

    db.session.add(instance)
    db.session.commit()
