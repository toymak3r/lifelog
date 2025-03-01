from fastapi import FastAPI
import uvicorn
import logging
from core.config import Config
from core.module_manager import ModuleManager

def create_app(config=None):
    """Create FastAPI app with optional configuration"""
    if config is None:
        config = Config()

    app = FastAPI()
    
    # Initialize and load modules
    module_manager = ModuleManager()
    podcasts = module_manager.load_module('podcasts', config.config)
    if podcasts:
        logging.info("Podcasts module loaded successfully")
        app.include_router(podcasts.get_router())
    else:
        logging.error("Podcasts module not loaded")
        
    return app

app = create_app()

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=5000)
