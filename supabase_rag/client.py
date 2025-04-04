from abc import ABCMeta, abstractmethod

from supabase import AsyncClient, create_async_client

from lib.env import env


class DBAsyncClient(metaclass=ABCMeta):
    """
    Attributes:
        client: DBクライアント
    """

    @abstractmethod
    async def get_client(self) -> AsyncClient:
        """
        DBクライアントを取得するメソッド
        """
        raise NotImplementedError()


class SupabaseClient(DBAsyncClient):
    """SupabaseのDBクライアント"""

    def __init__(self):
        self._client = None

    async def get_client(self) -> AsyncClient:
        if self._client is None:
            self._client = await create_async_client(
                supabase_url=env.SUPABASE_URL,
                supabase_key=env.SUPABASE_KEY,
            )
        return self._client
