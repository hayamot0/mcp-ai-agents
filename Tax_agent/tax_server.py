from mcp.server.fastmcp import FastMCP

mcp=FastMCP("")

@mcp.resource("resource://tax_config")
def tax_config():
    return {
        "Saudi Arabia":15,
        "KSA":15,
        "Saudi":15,
        "UAE":5,
        "United Arab Emirates":5,
        "Egypt":14,
        "Germany":19,
        "Algeria":19
    }

@mcp.tool(name='calculate_tax')
def calculate_tax(price:float,country:str)->float:
    config=tax_config()
    config_lower={k.lower(): v for k, v in config.items()}
    country_key=country.strip().lower()
    if country_key not in config_lower:
        raise ValueError (f"Country {country} not supported, available: {list(config_lower.keys())}")
    tax_rate=config_lower[country_key]
    tax_amount=price*tax_rate/100
    return round(tax_amount,2)

@mcp.prompt(name='tax_greeting',description="Greet user with VAT info")
def tax_greeting(name:str,country:str):
    config=tax_config
    config_lower={k.lower(): v for k,v in config.items()}
    country_key=country.strip().lower()
    if country_key not in config_lower:
        return f"Hello {name}, Sorry, VAT info for {country} is not available"
    vat=config_lower[country_key]
    return f"Hello {name}, the VAT in {country} is {vat}%"

if __name__=="__main__":
    mcp.run(transport="stdio")





