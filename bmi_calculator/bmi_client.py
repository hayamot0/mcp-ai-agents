import json
import asyncio
from mcp import ClientSession
from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params=StdioServerParameters(command="uv",args=["run","bmi_server.py"])

    async with stdio_client(server_params) as (reader,writer):

        async with ClientSession(reader,writer) as session:

            await session.initialize()

            while True:
                print("---BMI Calculator menu---")
                print("1. Calculate BMI")
                print("2. View categories")
                print("3. Quit")

                choice=int(input("Input your selection: ").strip())

                if choice==3:
                    break

                elif choice==2:
                    source_categories=await session.read_resource("resource://bmi_category")
                    categories=source_categories.contents[0].text
                    clean_format=json.loads(categories)
                    print("---BMI categories")
                    print({k: v for k,v in clean_format.items()})

                elif choice==1:
                    weight=float(input("Input your weight (KG): ").strip())
                    height=float(input("Input your height (M): ").strip())
                    response=await session.call_tool("bmi_calculator",{"weight":weight,"height":height})
                    print(response.content[0].text)

                else: 
                    print(f"Error, unavailable selection")

if __name__=="__main__":
    asyncio.run(main())


