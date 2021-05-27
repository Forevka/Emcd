from aiogram.types.user import User
from third_party.intercom_client.models.search_query import SearchQuery
from third_party.intercom_client.client import IntercomClient
from config import INTERCOM_TOKEN
from third_party.intercom_client.models.contact import Contact

async def get_intercom_contact(user: User):
    async with IntercomClient(INTERCOM_TOKEN) as intercom:
        intercom_users = await intercom.find_contact(
            SearchQuery(
                **{
                    "query": {
                        "field": "external_id",
                        "operator": "=",
                        "value": str(user.id),
                    }
                }
            )
        )

        intercom_user = next((i for i in intercom_users["data"]), None)

        if not intercom_user:
            intercom_user = await intercom.create_contact(
                Contact(
                    **{
                        "role": "user",
                        "external_id": str(user.id),
                        "name": user.full_name,
                        "custom_attributes": {
                            "username": user.username
                        },
                    }
                )
            )
        
        return intercom_user