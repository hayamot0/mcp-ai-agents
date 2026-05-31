import asyncio
import json
from mcp import ClientSession
from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params=StdioServerParameters(command="uv",args=["run","converter_server.py"])

    async with stdio_client(server_params) as (reader,writer):
        async with ClientSession(reader,writer) as session:
            await session.initialize()
            while True:
                print("---Menu---")
                print("1. Convert currency")
                print("2. See available currencies")
                print("3. Quit")

                choice=int(input('Select and option: ').strip())

                if choice==3:
                    print(f"Quitting...")
                    break
                elif choice==2:
                    resource_data = await session.read_resource("resource://exchange_rate")
                    resource_text = resource_data.contents[0].text
                    data = json.loads(resource_text)
                    print(f"Available currencies: {data.keys()}")
                elif choice==1:
                    amount=float(input("Input amount: "))
                    from_currency=input("Input original currency: ").strip()
                    to_currency=input("Input target currency: ").strip()
                    response=await session.call_tool("currency_converter",{"amount":amount,
                      "from_currency":from_currency,"to_currency":to_currency})
                    print(f"Converted amount equals: {response.content[0].text.strip()}")
                    


if __name__=="__main__":
    asyncio.run(main())