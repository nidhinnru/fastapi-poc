import json
import random
import secure
import logging
from .config import settings
from .dependencies import PermissionsValidator, validate_token
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, HTTPException, Request, Body, Header
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import operators
from app.api import api
from .db import database, schemas, models, queries

app = FastAPI(
    title="FastAPI with Auth0 RBAC",
    description="This is a demo project",
)

models.Base.metadata.create_all(bind=database.engine)

responses = {
    404: {"description": "Error: Not Found"},
}

csp = secure.ContentSecurityPolicy().default_src("'self'").frame_ancestors("'none'")
hsts = secure.StrictTransportSecurity().max_age(31536000).include_subdomains()
referrer = secure.ReferrerPolicy().no_referrer()
cache_value = secure.CacheControl().no_cache().no_store().max_age(0).must_revalidate()
x_frame_options = secure.XFrameOptions().deny()

secure_headers = secure.Secure(
    csp=csp,
    hsts=hsts,
    referrer=referrer,
    cache=cache_value,
    xfo=x_frame_options,
)

@app.middleware("http")
async def set_secure_headers(request, call_next):
    response = await call_next(request)
    secure_headers.framework.fastapi(response)
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.client_origin_url],
    allow_methods=["GET"],
    allow_headers=["Authorization", "Content-Type"],
    max_age=86400,
)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    message = str(exc.detail)

    return JSONResponse({"message": message}, status_code=exc.status_code)

def timestamp():
    est_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return est_time

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", status_code=200)
def root():
    return {"message": "Fast API with Auth0 RBAC"}

@app.get("/health", status_code=200)
def health_check():
    return {"detail": "ok"}

@app.post("/jumble", dependencies=[Depends(validate_token)], status_code=201)
async def get_body(request: Request, audit_base: schemas.AuditBase = schemas.AuditBase(), db: Session = Depends(get_db)):
    try:
        payload = (await request.body()).decode("utf-8")
        client_host = request.client.host
        audit_base_create = queries.create_audit_base(db, audit_base, timestamp(), client_host, "jumble", payload)
        return api.random_res(await request.body())
    except Exception as e:
        message = "Error getting jumble results."
        logging.error(message, exc_info=e)
        return JSONResponse(status_code=404, content={"message": message})

@app.get("/audit", responses={**responses}, dependencies=[Depends(validate_token)], status_code=200)
async def get_audit(request: Request, audit_base: schemas.AuditBase = schemas.AuditBase(), db: Session = Depends(get_db)):
    try:
        client_host = request.client.host
        audit_res = queries.get_audit_api_response_history2(db, audit_base, timestamp(), client_host, "audit", "Returned last 10 results.")
        return audit_res
    except Exception as e:
        message = "Error getting audit results."
        logging.error(message, exc_info=e)
        return JSONResponse(status_code=404, content={"message": message})
