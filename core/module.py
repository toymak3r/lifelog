from abc import ABC, abstractmethod
from fastapi import FastAPI, APIRouter

class LifeLogModule(ABC):
    """Base interface for all LifeLog modules"""
    
    def __init__(self, app: FastAPI):
        self.app = app

    @abstractmethod
    def initialize(self, config: dict) -> bool:
        """Initialize the module with given configuration"""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Return the module name"""
        pass

    @abstractmethod
    def get_router(self) -> APIRouter:
        """Return the module's API router"""
        pass