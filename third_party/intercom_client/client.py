from third_party.intercom_client.models.message import Message
from third_party.intercom_client.models.conversation import Conversation, conversation_from_dict
from third_party.intercom_client.models.search_query import SearchQuery
from types import TracebackType
from typing import Optional, Type

import aiohttp
import ujson as json
from third_party.intercom_client.models.contact import Contact
from yarl import URL


class IntercomClient:
    def __init__(self, token: str, base_url: URL = URL('https://api.intercom.io/')) -> None:
        self._base_url = base_url
        self._client = aiohttp.ClientSession(raise_for_status=True, headers={
            'Authorization': f'Bearer {token}',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        })

        self.token = token

    async def close(self) -> None:
        return await self._client.close()

    async def __aenter__(self) -> "IntercomClient":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> Optional[bool]:
        await self.close()
        return None

    def _make_url(self, path: str) -> URL:
        return self._base_url / path

    async def get_contacts(self,):
        """
            List all contacts
        """
        async with self._client.get(self._make_url("contacts"), raise_for_status=False) as resp:
            if (resp.status == 200):
                ret = await resp.json()
                return ret
            return None

    async def find_contact(self, query: SearchQuery):
        async with self._client.post(self._make_url("contacts/search"), raise_for_status=False, data=json.dumps(query.dict())) as resp:
            return await resp.json()

    async def create_contact(self, contact: Contact):
        """
            Creates contact
        """
        async with self._client.post(self._make_url("contacts"), raise_for_status=False, data=json.dumps(contact.dict())) as resp:
            return await resp.json()

    async def create_conversation(self, intercom_user_id: str, text: str) -> Message:
        """
            Creates conversation
        """
        async with self._client.post(self._make_url("conversations"), raise_for_status=False, data=json.dumps({
                "from": {
                    "type": "user",
                    "id": intercom_user_id,
                },
                "body": text,
            })) as resp:
            return await resp.json()

    async def retrieve_conversation(self, conversation_id: str) -> Conversation:
        """
            Get concrete conversation
        """
        async with self._client.get(self._make_url(f"conversations/{conversation_id}"), raise_for_status=False, params={
            'display_as': 'plaintext',
        }) as resp:
            return await resp.json()

    async def find_conversations_for_user(self, intercom_user_id: str):
        """
            Find all conversations initiated by user
        """
        async with self._client.post(self._make_url(f"conversations/search"), raise_for_status=False, data=json.dumps({
                "query": {
                    "field": "contact_ids",
                    "operator": "IN",
                    "value": [intercom_user_id],
                }
            })) as resp:
            return await resp.json()
