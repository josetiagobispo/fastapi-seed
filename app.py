from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from injector import Injector
from loguru import logger

from modules.lead.module import LeadModule
from settings import Settings
from src.core.container import AppContainer
from src.core.registry import ModuleRegistry

ModuleRegistry.register_modules([
    LeadModule,
])


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Aplicação iniciada")
    yield
    logger.info("Aplicação encerrada")


def create_app() -> FastAPI:
    settings = Settings()
    enable_docs = settings.should_enable_swagger()

    fastapi_app = FastAPI(
        title=settings.APP_NAME,
        description="API para gerenciamento de Leads",
        version="1.0.0",
        docs_url="/docs" if enable_docs else None,
        redoc_url="/redoc" if enable_docs else None,
        lifespan=lifespan,
        openapi_tags=[
            {"name": "leads", "description": "Operações de Leads"},
        ],
    )

    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    modules = [AppContainer()]
    for module_class in ModuleRegistry.get_modules():
        module = module_class()
        modules.append(module)
        fastapi_app.include_router(module.router)
        logger.info(f"Módulo {module_class.__name__} registrado")

    fastapi_app.state.injector = Injector(modules)

    @fastapi_app.get("/health", tags=["health"])
    async def health_check():
        return {"status": "healthy", "message": "API está funcionando"}

    return fastapi_app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
