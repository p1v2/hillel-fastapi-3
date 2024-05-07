import asyncio

from aiohttp import ClientSession


async def get_auth_token():
    login_data = {
        "username": "admin",
        "password": "admin"
    }

    async with ClientSession() as session:
        response = await session.post("http://localhost:8001/token", data=login_data)
        response_json = await response.json()

        return response_json['access_token']


async def get_products(offset: int, token: str):
    limit = 50

    async with ClientSession() as session:
        response = await session.get(f"http://localhost:8001/products?offset={offset}&limit={limit}", headers={
            'Authorization': f"Bearer {token}"
        })

        response_json = await response.json()

        return response_json['results'], response_json['total']


async def create_product(session, product):
    response = await session.post("http://localhost:8001/products", json=product)
    print(response.status)


async def create_many_products():
    async with ClientSession() as session:
        products = [
            {"name": f"Product {i}", "price": i}
            for i in range(1000)
        ]

        # Create all products in once
        # coroutines = [
        #     create_product(product)
        #     for product in products
        # ]
        #
        # await asyncio.gather(*coroutines)

        # Create products per "size"
        size = 100

        products_slices = [
            products[i:i+size]
            for i in range(0,1000,size)
        ]

        for slice in products_slices:
            coroutines = [
                create_product(session, product)
                for product in slice
            ]

            await asyncio.gather(*coroutines)


async def read_all_products():
    # products = 1000
    # max limit = 50
    token = await get_auth_token()

    limit = 50

    products = []

    products_first_page, total = await get_products(0, token)
    products += products_first_page

    # total = 1000
    # limit = 50

    # count_of_request = total // limit + 1
    # 1) 1 .. 50
    # 2) 51 .. 100
    # 20) 950 .. 1000
    # 21) 1001 .. 1050 - empty response

    count_of_requests = total // limit

    coroutines = [
        get_products(50 * i, token)
        for i in range(1, count_of_requests)
    ]

    results = await asyncio.gather(*coroutines)

    for result in results:
        products_page_result, _ = result

        products += products_page_result

    print(len(products))
    print(
        products
    )


if __name__ == "__main__":
    asyncio.run(read_all_products())
