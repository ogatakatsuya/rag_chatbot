import os

import weaviate
from dotenv import load_dotenv
from weaviate.config import AdditionalConfig, ConnectionConfig

load_dotenv()

client = weaviate.connect_to_local(
    #host="localhost",
    host="weaviate",
    port=8080,
    grpc_port=50051,
    headers={"X-OpenAI-Api-Key": os.environ["OPENAI_API_KEY"]},
    additional_config=AdditionalConfig(
        connection=ConnectionConfig(
            session_pool_connections=30,
            session_pool_maxsize=200,
            session_pool_max_retries=3,
        ),
        timeout=(6000, 18000),
    ),
)
