import asyncio
from mcp import ClientSession
from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client
import json

async def main():
    server_params = StdioServerParameters(command="uv", args=["run", "tax_server.py"])

    async with stdio_client(server_params) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            await session.initialize()
            print("Connected to MCP Tax Server.\n")

            while True:
                print("=== MENU ===")
                print("1. Calculate Tax (calculate_tax)")
                print("2. Tax Greeting (tax_greeting)")
                print("3. View All VAT Settings")
                print("4. Quit")
                choice = input("Select an option (1/2/3/4): ").strip()

                if choice == "4":
                    print("👋 Exiting.")
                    break

                elif choice == "1":
                    try:
                        price = float(input("Enter price: "))
                    except ValueError:
                        print("Please enter a valid number.")
                        continue

                    country = input("Enter country: ").strip()

                    try:
                        response = await session.call_tool("calculate_tax", {
                            "price": price,
                            "country": country
                        })
                        print(f"Calculated Tax: {response.content[0].text.strip()}")
                    except Exception as e:
                        print(f"Error: {e}")

                elif choice == "2":
                    name = input("Enter your name: ").strip()
                    country = input("Enter country: ").strip()

                    prompt_result = await session.get_prompt("tax_greeting", {
                        "name": name,
                        "country": country
                    })

                    print(f"Message: {prompt_result.messages[0].content.text.strip()}")

                elif choice == "3":
                    resource_data = await session.read_resource("resource://tax_config")
                    resource_text = resource_data.contents[0].text
                    data = json.loads(resource_text)

                    print("\nAvailable VAT Settings:")
                    for country, vat in data.items():
                        print(f"- {country}: {vat}%")

                else:
                    print("Invalid option, please try again.\n")

if __name__ == "__main__":
    asyncio.run(main())