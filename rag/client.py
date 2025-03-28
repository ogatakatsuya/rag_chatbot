import weaviate
from weaviate.config import AdditionalConfig, ConnectionConfig

from lib.env import env

client = weaviate.connect_to_local(
    # host="localhost", #vscodeで実行するとき
    host="weaviate",  # streamlitで実行するとき
    port=8080,
    grpc_port=50051,
    headers={"X-OpenAI-Api-Key": env.OPENAI_API_KEY},
    additional_config=AdditionalConfig(
        connection=ConnectionConfig(
            session_pool_connections=30,
            session_pool_maxsize=200,
            session_pool_max_retries=3,
        ),
        timeout=(6000, 18000),
    ),
)
