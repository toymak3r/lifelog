import importlib
import logging
from typing import Dict, Optional
from .module import LifeLogModule

class ModuleManager:
    """Manages the loading and lifecycle of LifeLog modules"""
    
    def __init__(self):
        self.modules: Dict[str, LifeLogModule] = {}
        
    def load_module(self, module_name: str, config: dict) -> Optional[LifeLogModule]:
        """Load a module by name if enabled in config"""
        if module_name in self.modules:
            return self.modules[module_name]
            
        try:
            # Check if module is enabled
            if not config.get(f'enable_{module_name}', False):
                return None
                
            # Import module dynamically
            module_path = f'modules.{module_name}.module'
            module = importlib.import_module(module_path)
            
            # Create instance
            module_class = getattr(module, module_name.capitalize())
            instance = module_class()
            
            # Initialize with config
            if instance.initialize(config):
                self.modules[module_name] = instance
                return instance
                
        except (ImportError, AttributeError) as e:
            logging.warning(f"Failed to load module {module_name}: {e}")
            
        return None

    def get_module(self, module_name: str) -> Optional[LifeLogModule]:
        """Get a loaded module by name"""
        return self.modules.get(module_name)