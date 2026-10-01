import logging
from datetime import datetime, timezone
from geoalchemy2.elements import WKTElement
from app.db.session import SessionLocal
from app.models.domain_models import (
    User,
    Worker,
    Train,
    WorkZone,
    BlockSection,
    Device,
    NearMiss,
    Team,
    RailwayNetwork,
    RailwayNode,
    TrackSegment,
    Station,
    SafeRefugeLocation,
    SafetyZone,
)

logger = logging.getLogger("dost_guardian.seed")


def utc_now():
    return datetime.now(timezone.utc)


def init_seed_data(db=None):
    close_on_done = False
    if db is None:
        db = SessionLocal()
        close_on_done = True
    try:
        logger.info("Seeding synthetic operational railway geospatial data...")

        # 1. Users
        if not db.query(User).filter_by(id="usr-dev-control-room").first():
            db.add(User(
                id="usr-dev-control-room",
                username="control_room_operator",
                email="operator@dostguardian.railway",
                full_name="Control Room Operator (Dev)",
                role="CONTROL_ROOM",
            ))

        if not db.query(User).filter_by(id="usr-dev-worker").first():
            db.add(User(
                id="usr-dev-worker",
                username="ramesh_kumar",
                email="ramesh@dostguardian.railway",
                full_name="Ramesh Kumar",
                role="WORKER",
            ))
        db.commit()

        # 2. Teams
        if not db.query(Team).filter_by(id="team-01").first():
            db.add(Team(
                id="team-01",
                code="TM-ALPHA-120",
                name="Chennai Central Gang Maintainer Unit 4",
                assigned_section="MAS-AJJ-DOWN-120",
            ))
            db.commit()

        # 3. Railway Network
        network = db.query(RailwayNetwork).filter_by(code="MAS-AJJ-NET").first()
        if not network:
            network = RailwayNetwork(
                id="net-mas-ajj",
                code="MAS-AJJ-NET",
                name="Chennai Central - Arakkonam Corridor",
                description="Synthetic WGS84 railway corridor for DOST Guardian 2.0 demonstration",
                srid=4326,
                is_active=True,
            )
            db.add(network)
            db.commit()

        # 4. Railway Nodes (Junctions & Signals)
        if not db.query(RailwayNode).filter_by(id="node-mas-01").first():
            db.add(RailwayNode(
                id="node-mas-01",
                network_id="net-mas-ajj",
                code="NODE-MAS-01",
                name="Chennai Central Junction Node 1",
                node_type="JUNCTION",
                position_x=30.0,
                position_y=140.0,
                geom=WKTElement("POINT(80.2700 13.0820)", srid=4326),
            ))

        if not db.query(RailwayNode).filter_by(id="node-mas-02").first():
            db.add(RailwayNode(
                id="node-mas-02",
                network_id="net-mas-ajj",
                code="NODE-MAS-02",
                name="Perambur Signal Node 2",
                node_type="SIGNAL",
                position_x=500.0,
                position_y=140.0,
                geom=WKTElement("POINT(80.2800 13.0825)", srid=4326),
            ))

        if not db.query(RailwayNode).filter_by(id="node-ajj-01").first():
            db.add(RailwayNode(
                id="node-ajj-01",
                network_id="net-mas-ajj",
                code="NODE-AJJ-01",
                name="Arakkonam Terminus Node 3",
                node_type="TERMINUS",
                position_x=970.0,
                position_y=140.0,
                geom=WKTElement("POINT(80.2900 13.0830)", srid=4326),
            ))
        db.commit()

        # 5. Stations
        if not db.query(Station).filter_by(id="stn-mas").first():
            db.add(Station(
                id="stn-mas",
                network_id="net-mas-ajj",
                code="MAS",
                name="Chennai Central Railway Station",
                station_type="PASSENGER",
                position_x=50.0,
                position_y=120.0,
                geom=WKTElement("POINT(80.2710 13.0822)", srid=4326),
                boundary_geom=WKTElement("POLYGON((80.2705 13.0820, 80.2715 13.0820, 80.2715 13.0825, 80.2705 13.0825, 80.2705 13.0820))", srid=4326),
            ))

        if not db.query(Station).filter_by(id="stn-ajj").first():
            db.add(Station(
                id="stn-ajj",
                network_id="net-mas-ajj",
                code="AJJ",
                name="Arakkonam Junction Railway Station",
                station_type="JUNCTION",
                position_x=950.0,
                position_y=290.0,
                geom=WKTElement("POINT(80.2890 13.0828)", srid=4326),
                boundary_geom=WKTElement("POLYGON((80.2885 13.0826, 80.2895 13.0826, 80.2895 13.0831, 80.2885 13.0831, 80.2885 13.0826))", srid=4326),
            ))
        db.commit()

        # 6. Block Sections
        bs_down = db.query(BlockSection).filter_by(code="MAS-AJJ-DOWN-120").first()
        if not bs_down:
            bs_down = BlockSection(
                id="bs-120",
                network_id="net-mas-ajj",
                code="MAS-AJJ-DOWN-120",
                name="Chennai-Arakkonam Down Line KM 12.0 - 13.5",
                line_type="DOWN",
                start_km=12.0,
                end_km=13.5,
                speed_limit_kmh=110,
                status="ACTIVE",
                is_active=True,
                geom=WKTElement("LINESTRING(80.2700 13.0820, 80.2800 13.0825)", srid=4326),
                corridor_geom=WKTElement("POLYGON((80.2698 13.0818, 80.2802 13.0823, 80.2802 13.0827, 80.2698 13.0822, 80.2698 13.0818))", srid=4326),
            )
            db.add(bs_down)
        else:
            bs_down.network_id = "net-mas-ajj"
            bs_down.geom = WKTElement("LINESTRING(80.2700 13.0820, 80.2800 13.0825)", srid=4326)
            bs_down.corridor_geom = WKTElement("POLYGON((80.2698 13.0818, 80.2802 13.0823, 80.2802 13.0827, 80.2698 13.0822, 80.2698 13.0818))", srid=4326)

        bs_up = db.query(BlockSection).filter_by(code="MAS-AJJ-UP-122").first()
        if not bs_up:
            bs_up = BlockSection(
                id="bs-122",
                network_id="net-mas-ajj",
                code="MAS-AJJ-UP-122",
                name="Chennai-Arakkonam Up Line KM 12.0 - 13.5",
                line_type="UP",
                start_km=12.0,
                end_km=13.5,
                speed_limit_kmh=110,
                status="ACTIVE",
                is_active=True,
                geom=WKTElement("LINESTRING(80.2800 13.0825, 80.2900 13.0830)", srid=4326),
                corridor_geom=WKTElement("POLYGON((80.2798 13.0823, 80.2902 13.0828, 80.2902 13.0832, 80.2798 13.0827, 80.2798 13.0823))", srid=4326),
            )
            db.add(bs_up)
        db.commit()

        # 7. Track Segments
        if not db.query(TrackSegment).filter_by(id="ts-down-1").first():
            db.add(TrackSegment(
                id="ts-down-1",
                network_id="net-mas-ajj",
                code="TS-MAS-AJJ-D1",
                name="MAS-AJJ Down Line Segment 1",
                start_node_id="node-mas-01",
                end_node_id="node-mas-02",
                track_code="DOWN_MAIN",
                direction="DOWN",
                chainage_start_km=12.0,
                chainage_end_km=13.5,
                length_meters=1500.0,
                speed_limit_kmh=110,
                block_section_id="bs-120",
                status="ACTIVE",
                geom=WKTElement("LINESTRING(80.2700 13.0820, 80.2800 13.0825)", srid=4326),
            ))

        if not db.query(TrackSegment).filter_by(id="ts-up-1").first():
            db.add(TrackSegment(
                id="ts-up-1",
                network_id="net-mas-ajj",
                code="TS-MAS-AJJ-U1",
                name="MAS-AJJ Up Line Segment 1",
                start_node_id="node-mas-02",
                end_node_id="node-ajj-01",
                track_code="UP_MAIN",
                direction="UP",
                chainage_start_km=12.0,
                chainage_end_km=13.5,
                length_meters=1500.0,
                speed_limit_kmh=110,
                block_section_id="bs-122",
                status="ACTIVE",
                geom=WKTElement("LINESTRING(80.2800 13.0825, 80.2900 13.0830)", srid=4326),
            ))
        db.commit()

        # 8. Workers
        workers_data = [
            ("WRK-101", "Ramesh Kumar", "Gang Maintainer", 450.0, 140.0, "80.2750 13.0823", "usr-dev-worker"),
            ("WRK-102", "Suresh Patel", "Track Mate", 470.0, 142.0, "80.2754 13.0823", None),
            ("WRK-103", "Priya Sharma", "Keyman Inspector", 420.0, 138.0, "80.2744 13.0822", None),
        ]

        for wid, wname, wrole, px, py, pt_wkt, uid in workers_data:
            w = db.query(Worker).filter_by(id=wid).first()
            if not w:
                w = Worker(
                    id=wid,
                    user_id=uid,
                    name=wname,
                    role=wrole,
                    team_id="team-01",
                    current_block_section="MAS-AJJ-DOWN-120",
                    status="SAFE",
                    network_state="ONLINE",
                    battery_level=94,
                    gps_accuracy_meters=2.5,
                    position_x=px,
                    position_y=py,
                    current_geom=WKTElement(f"POINT({pt_wkt})", srid=4326),
                    last_location_at=utc_now(),
                    envelope_data={
                        "radiusMeters": 500,
                        "gpsUncertaintyBufferMeters": 2.5,
                        "trackGeometryBufferMeters": 50,
                        "isExpandedDueToGps": False,
                    },
                )
                db.add(w)
            else:
                w.current_geom = WKTElement(f"POINT({pt_wkt})", srid=4326)
                w.last_location_at = utc_now()
        db.commit()

        # 9. Work Zone
        wz = db.query(WorkZone).filter_by(id="WZ-402").first()
        if not wz:
            wz = WorkZone(
                id="WZ-402",
                name="MAS-AJJ Down Line Track Maintenance",
                description="Synthetic maintenance work zone for gang maintainer team Alpha-120",
                block_section_code="MAS-AJJ-DOWN-120",
                block_section_id="bs-120",
                start_x=400.0,
                end_x=500.0,
                buffer_zone_meters=500.0,
                safety_zone_meters=200.0,
                assigned_team_code="TM-ALPHA-120",
                status="ACTIVE",
                is_active=True,
                geom=WKTElement("POLYGON((80.2740 13.0821, 80.2760 13.0821, 80.2760 13.0826, 80.2740 13.0826, 80.2740 13.0821))", srid=4326),
            )
            db.add(wz)
        else:
            wz.block_section_id = "bs-120"
            wz.geom = WKTElement("POLYGON((80.2740 13.0821, 80.2760 13.0821, 80.2760 13.0826, 80.2740 13.0826, 80.2740 13.0821))", srid=4326)
        db.commit()

        # 10. Safety Refuge Locations
        refuge1 = db.query(SafeRefugeLocation).filter_by(id="refuge-101").first()
        if not refuge1:
            refuge1 = SafeRefugeLocation(
                id="refuge-101",
                work_zone_id="WZ-402",
                code="REFUGE-MAS-101",
                name="Down Line Refuge Niche KM 12.4",
                refuge_type="NICHE",
                capacity_persons=10,
                position_x=440.0,
                position_y=75.0,
                geom=WKTElement("POINT(80.2748 13.0828)", srid=4326),
                is_active=True,
            )
            db.add(refuge1)

        refuge2 = db.query(SafeRefugeLocation).filter_by(id="refuge-102").first()
        if not refuge2:
            refuge2 = SafeRefugeLocation(
                id="refuge-102",
                work_zone_id="WZ-402",
                code="REFUGE-MAS-102",
                name="Up Line Platform Clearance Niche KM 13.1",
                refuge_type="PLATFORM",
                capacity_persons=15,
                position_x=810.0,
                position_y=305.0,
                geom=WKTElement("POINT(80.2850 13.0822)", srid=4326),
                is_active=True,
            )
            db.add(refuge2)
        db.commit()

        # 11. Trains
        t1 = db.query(Train).filter_by(id="TRN-204").first()
        if not t1:
            t1 = Train(
                id="TRN-204",
                number="12626",
                name="MAS-SBC Express",
                line="DOWN",
                current_block_section="MAS-AJJ-DOWN-120",
                position_x=0.0,
                speed_kmh=110.0,
                heading=90.0,
                direction="EASTBOUND",
                status="APPROACHING",
                current_geom=WKTElement("POINT(80.2700 13.0820)", srid=4326),
                last_position_at=utc_now(),
            )
            db.add(t1)
        else:
            t1.current_geom = WKTElement("POINT(80.2700 13.0820)", srid=4326)
            t1.heading = 90.0
            t1.last_position_at = utc_now()
        db.commit()

        # 12. Devices
        dev1 = db.query(Device).filter_by(id="DEV-801").first()
        if not dev1:
            dev1 = Device(
                id="DEV-801",
                worker_id="WRK-101",
                device_type="HANDHELD_SAFETY_UNIT",
                firmware_version="2.1.0-prod",
                battery_percentage=94,
                network_signal_dbm=-72,
                status="HEALTHY",
                current_geom=WKTElement("POINT(80.2750 13.0823)", srid=4326),
            )
            db.add(dev1)
        else:
            dev1.current_geom = WKTElement("POINT(80.2750 13.0823)", srid=4326)
        db.commit()

        # 13. Near Misses
        nm = db.query(NearMiss).filter_by(id="NM-9012").first()
        if not nm:
            nm = NearMiss(
                id="NM-9012",
                occurred_at=utc_now(),
                train_id="EXP-12626",
                train_speed_kmh=112.0,
                worker_id="WRK-101",
                worker_name="Ramesh Kumar",
                block_section_code="MAS-AJJ-DOWN-120",
                min_spatial_clearance_meters=1.8,
                ttd_at_ack_seconds=12,
                severity="MODERATE",
                contributing_factors=["Track Curve Blind Spot", "Late Audio Notice (8s)", "Wind Noise"],
                location_coords={"x": 450.0, "y": 140.0},
                geom=WKTElement("POINT(80.2750 13.0823)", srid=4326),
            )
            db.add(nm)
        else:
            nm.geom = WKTElement("POINT(80.2750 13.0823)", srid=4326)
        db.commit()

        logger.info("Spatial seed data creation completed successfully.")
    except Exception as e:
        logger.error(f"Error seeding spatial database: {e}")
        db.rollback()
    finally:
        if close_on_done:
            db.close()
