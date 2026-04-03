# 01-01: Set Up Data Pipelines

**Epic:** Data Ingestion & Alerts

## Goal

Fetch weather, satellite, and soil data daily; store in PostgreSQL + cache.

## Acceptance

- Scripts: `fetch_weather.py`, `fetch_sentinel.py`, `fetch_soil.py`
- Database tables: `weather_forecast`, `satellite_ndvi`, `soil_moisture`
- Airflow or automation‑engine schedule to run daily at 6 AM
- Data quality checks (missing values, timestamps)
- Sample data for 3 regions (Nigeria, Kenya, Bangladesh)

## Tasks

1. Get API keys: OpenWeatherMap, Copernicus Sentinel Hub, maybe SoilGrids
2. Write fetchers with `httpx`; store in DB with `asyncpg`
3. Set up PostGIS extension for spatial queries
4. Add logging and alerts on fetch failure
5. Document `.env` variables and setup

## Dependencies

None

## Time

8 hours
