from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routes.payments import router as payment_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Razorpay Payment Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # fine for local demo; tighten this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(payment_router)

@app.get("/")
def health_check():
    return {"message": "Payment service is running"}