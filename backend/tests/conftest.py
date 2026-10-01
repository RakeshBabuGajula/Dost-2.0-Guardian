import os
import sys

# 1. Force default test database URL to postgres container
# 1. Force default test database URL to postgres container if available, or sqlite for local test runner
TEST_DB_URL = os.getenv("TEST_DATABASE_URL", os.getenv("DATABASE_URL", "sqlite:///./test.db"))
os.environ["DATABASE_URL"] = TEST_DB_URL
os.environ["REDIS_URL"] = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# 2. Ensure backend root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

# 3. Initialize test engine
test_engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False} if "sqlite" in TEST_DB_URL else {})

@event.listens_for(test_engine, "connect")
def _add_sqlite_spatial_funcs(dbapi_connection, connection_record):
    if type(dbapi_connection).__module__.startswith("sqlite3"):
        dummy_funcs = [
            ("RecoverGeometryColumn", -1, lambda *a: 1),
            ("InitSpatialMetaData", -1, lambda *a: 1),
            ("CreateSpatialIndex", -1, lambda *a: 1),
            ("AddGeometryColumn", -1, lambda *a: 1),
            ("DisableSpatialIndex", -1, lambda *a: 1),
            ("DiscardGeometryColumn", -1, lambda *a: 1),
            ("GeomFromEWKT", -1, lambda *a: a[0] if a else None),
            ("GeomFromEWKB", -1, lambda *a: a[0] if a else None),
            ("AsEWKB", -1, lambda *a: b"\x01\x01\x00\x00\x00"),
            ("AsGeoJSON", -1, lambda *a: '{"type":"Point","coordinates":[80.275,13.0823]}'),
            ("ST_AsBinary", -1, lambda *a: b"\x01\x01\x00\x00\x00"),
            ("AsBinary", -1, lambda *a: b"\x01\x01\x00\x00\x00"),
            ("ST_AsGeoJSON", -1, lambda *a: '{"type":"Point","coordinates":[80.275,13.0823]}'),
            ("ST_Within", -1, lambda *a: 1),
            ("ST_DWithin", -1, lambda *a: 1),
            ("ST_Intersects", -1, lambda *a: 1),
            ("ST_Distance", -1, lambda *a: 10.0),
            ("ST_MakeEnvelope", -1, lambda *a: "ENVELOPE"),
            ("ST_Buffer", -1, lambda *a: "BUFFER"),
            ("ST_Centroid", -1, lambda *a: "CENTROID"),
            ("ST_SetSRID", -1, lambda *a: a[0] if a else None),
            ("ST_Transform", -1, lambda *a: a[0] if a else None),
            ("ST_Contains", -1, lambda *a: 1),
            ("ST_X", -1, lambda *a: 80.275),
            ("ST_Y", -1, lambda *a: 13.0823),
        ]
        for name, nargs, func in dummy_funcs:
            try:
                dbapi_connection.create_function(name, nargs, func)
            except Exception:
                pass

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# 4. Patch app.db.session before importing app modules
import app.db.session
app.db.session.engine = test_engine
app.db.session.SessionLocal = TestingSessionLocal

import pytest
from fastapi.testclient import TestClient
from app.db.session import get_db, Base
from app.models.domain_models import *  # Ensure all models are registered in metadata
from app.db.init_db import init_seed_data
from app.main import app

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    Base.metadata.create_all(bind=test_engine)
    session = TestingSessionLocal()
    try:
        init_seed_data(session)
    finally:
        session.close()
    yield

@pytest.fixture
def db_session():
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db_session):
    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
