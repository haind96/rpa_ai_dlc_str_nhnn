import sys
from pathlib import Path
from loguru import logger
from typing import Dict, Any

# Ensure project root is in sys.path when running script directly
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.config import load_config
from src.api_client import ECMClient
from src.kafka_consumer import consume_messages

def process_customer_message(data: Dict[str, Any], ecm_client: ECMClient) -> bool:
    """Process a single Kafka message representing a customer. Returns True on success."""
    logger.info(f"Processing message: {data}")
    
    # In a real scenario, the business code and customer code are extracted from the message.
    # Assuming 'customer_code' is present in the JSON payload
    customer_code = data.get("customer_code")
    # You might want to get this from the message or loop over `config.ecm_business_codes` if it was loaded
    business_code = data.get("business_code", "mb_smart_channel")
    
    if not customer_code:
        logger.warning("Message missing 'customer_code', skipping...")
        return False
        
    try:
        # Step 1: Search for files
        files = ecm_client.search_files(business_code, customer_code)
        logger.info(f"Found {len(files)} files for customer {customer_code} under business {business_code}")
        
        # Define directory to save downloaded files
        download_dir = Path("data/downloads")
        download_dir.mkdir(parents=True, exist_ok=True)
        
        # Step 2: Download each file
        for file_info in files:
            file_id = file_info.get("fileId")
            file_name = file_info.get("fileName", f"{file_id}.pdf")
            
            if file_id:
                logger.info(f"Downloading file ID: {file_id}")
                content = ecm_client.download_file(file_id)
                logger.info(f"Successfully downloaded file {file_id}, size: {len(content)} bytes")
                
                # Save file to disk
                file_path = download_dir / file_name
                with open(file_path, "wb") as f:
                    f.write(content)
                logger.info(f"Saved file to {file_path}")
                
        logger.info(f"✅ Successfully finished processing message for customer: {customer_code}.")
        return True
                
    except Exception as e:
        logger.error(f"❌ Failed to process customer {customer_code}: {e}")
        return False

def main() -> None:
    """Main entrypoint for the service."""
    # Setup logger
    logger.remove()
    logger.add(sys.stderr, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", level="INFO")
    
    logger.info("Loading configuration...")
    try:
        config = load_config("data/config.yaml")
    except Exception as e:
        logger.critical(f"Failed to load configuration: {e}")
        sys.exit(1)
        
    # Initialize API client
    ecm_client = ECMClient(config)
    
    # Define a closure or partial function to pass to the consumer
    def message_handler(data: Dict[str, Any]) -> bool:
        return process_customer_message(data, ecm_client)

    logger.info("Starting Kafka consumer...")
    try:
        consume_messages(config, message_handler)
    finally:
        ecm_client.close()
        logger.info("Service shutting down.")

if __name__ == "__main__":
    main()
