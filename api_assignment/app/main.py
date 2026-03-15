
# Main entry for Payments API
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from scalar_fastapi import get_scalar_api_reference
from app.routes import customers, payments, refunds

BANNER = r"""
    ____   _ __   __ __  __ _____ _   _ _____ ____      _    ____ ___ 
 |  _ \ / \\ \ / /|  \/  | ____| \ | |_   _/ ___|    / \  |  _ \_ _|
 | |_) / _ \\ V / | |\/| |  _| |  \| | | | \___ \   / _ \ | |_) | | 
 |  __/ ___ \| |  | | |___| |\  | | |  ___) | / ___ \|  __/| | 
 |_| /_/   \_\_|  |_|  |_|_____|_| \_| |_| |____/ /_/   \_\_|  |___|
"""

app = FastAPI(
        title="Payments API",
        version="1.0.0",
        description="Fake payment server for TDD training.",
        docs_url=None,
        redoc_url=None,
)

app.include_router(customers.router)
app.include_router(payments.router)
app.include_router(refunds.router)



@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def home():
    return f"""
    <!DOCTYPE html>
    <html>
        <head>
            <title>Payments API</title>
            <style>
                body {{
                    background-color: #0d1117;
                    color: #58a6ff;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    overflow: hidden;
                    font-family: 'Courier New', Courier, monospace;
                }}
                @keyframes pulse {{
                    0% {{ 
                        text-shadow: 0 0 10px rgba(88, 166, 255, 0.4);
                        transform: scale(1);
                    }}
                    50% {{ 
                        text-shadow: 0 0 30px rgba(88, 166, 255, 0.9), 0 0 50px rgba(88, 166, 255, 0.4);
                        transform: scale(1.02);
                        color: #79c0ff;
                    }}
                    100% {{ 
                        text-shadow: 0 0 10px rgba(88, 166, 255, 0.4);
                        transform: scale(1);
                    }}
                }}
                pre {{
                    font-weight: bold;
                    animation: pulse 3s infinite ease-in-out;
                    user-select: none;
                }}
                .scanline {{
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: linear-gradient(
                        rgba(18, 16, 16, 0) 50%, 
                        rgba(0, 0, 0, 0.1) 50%
                    ), linear-gradient(
                        90deg, 
                        rgba(255, 0, 0, 0.03), 
                        rgba(0, 255, 0, 0.01),
                        rgba(0, 0, 255, 0.03)
                    );
                    background-size: 100% 4px, 3px 100%;
                    pointer-events: none;
                }}
            </style>
        </head>
        <body>
            <div class="scanline"></div>
            <pre>{BANNER}</pre>
        </body>
    </html>
    """




@app.get("/docs", include_in_schema=False)
async def scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Payments API",
    )



@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"error": "Internal server error."})
