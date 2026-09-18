from pathlib import Path

import yaml


CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"

class ConfigLoader:
    """Load configuration files from config/ directory"""
    
    @staticmethod
    def load_competencies():
        """Load competencies configuration"""
        config_path = CONFIG_DIR / "competencies.yaml"
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    
    @staticmethod
    def load_grading():
        """Load grading scale configuration"""
        config_path = CONFIG_DIR / "grading.yaml"
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    
    @staticmethod
    def load_taxonomy():
        """Load safety taxonomy configuration"""
        config_path = CONFIG_DIR / "taxonomy.yaml"
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    
    @staticmethod
    def get_competency_codes():
        """Get list of all competency codes"""
        comp = ConfigLoader.load_competencies()
        return list(comp.get('competencies', {}).keys())
    
    @staticmethod
    def get_competency_info(code):
        """Get info for specific competency code"""
        comp = ConfigLoader.load_competencies()
        return comp.get('competencies', {}).get(code, None)
    
    @staticmethod
    def get_observable_behaviors(competency_code):
        """Get observable behaviors for competency"""
        info = ConfigLoader.get_competency_info(competency_code)
        if info:
            return info.get('observable_behaviors', [])
        return []
