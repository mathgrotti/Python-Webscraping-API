from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .routes.operadoras import router as operadoras_router

app = FastAPI()

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add exception handler to catch and log errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    error_msg = f"Unhandled error: {str(exc)}"
    print(error_msg)  # Print to console for debugging
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error", "detail": str(exc)}
    )
    
# Rota raiz
@app.get("/")
async def root():
    return {
        "message": "API de Operadoras de Saúde",
        "rotas": {
            "busca_operadoras": "/api/operadoras?termo=valor"
        }
    }

# Inclui as rotas de operadoras
app.include_router(operadoras_router, prefix="/api")

# Debug endpoint
@app.get("/debug")
async def debug():
    return {"message": "Debug endpoint accessible"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)