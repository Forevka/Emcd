from asyncio import run
from third_party.intercom_client.models.search_query import SearchQuery
from third_party.intercom_client.models.contact import (
    Contact,
)
from third_party.intercom_client.client import IntercomClient


async def main():
    intercom = IntercomClient(
        "dG9rOjQ3ZjI2NjcyXzQyNjRfNGNmZV9hNTU3XzY3YWNkNTI0YmZhMToxOjA="
    )
    # Create a user
    users = await intercom.get_contacts()
    print(users)

    contact = await intercom.find_contact(
        SearchQuery(
            **{
                "query": {
                    "field": "external_id",
                    "operator": "=",
                    "value": "383492784",
                }
            }
        )
    )

    print(contact)
    #60af94a80f3903f694001ccc

    #conversation = await intercom.create_conversation("60af94a80f3903f694001ccc", "this is a test from tg emcd bot developer")

    #print(conversation)

    conversations = await intercom.find_conversations_for_user("60af94a80f3903f694001ccc")

    print(conversations)
    #1660

    conversation = await intercom.retrieve_conversation("1660")

    print(conversation)


    tg_user = Contact(
        **{
            "role": "user",
            "external_id": 383492784,
            "name": "Developer",
            "custom_attributes": {"username": "@forevka"},
        }
    )
    contact = await intercom.create_contact(contact=tg_user)
    print(contact)


if __name__ == "__main__":
    run(main())
