from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from API.routes.scan import router as scan_router


app = FastAPI(title="URLShield API")
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_methods=["POST"],
	allow_headers=["Content-Type"],
)
app.include_router(scan_router)
