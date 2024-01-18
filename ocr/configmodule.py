class BaseConfig:
    DEBUG = False
    SECRET_KEY = 'amyl140200'
    
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    
class ProductionConfig(BaseConfig):
    DEBUG = False
    