import yaml
from pydantic import BaseModel

class AppConfig(BaseModel):
    kafka_bootstrap_servers: str
    kafka_topic: str
    kafka_group_id: str
    kafka_username: str
    kafka_password: str
    
    ecm_auth_url: str
    ecm_search_url: str
    ecm_content_url: str
    ecm_client_credential: str

def load_config(path: str = "data/config.yaml") -> AppConfig:
    """Load configuration from a YAML file and validate it."""
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return AppConfig(**data)
