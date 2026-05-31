from mcp.server.fastmcp import FastMCP

mcp=FastMCP("")


@mcp.resource("resource://exchange_rate")
def exchange_rate():
    return {
    "USD": 1.0,
    "EUR": 0.858, 
    "GBP": 0.743, 
    "INR": 95.50, 
    "JPY": 159.25,  
    "CAD": 1.39,  
    "AUD": 1.52,
    "CHF": 0.87,
    "CNY": 7.25,
    "AED": 3.67
}

@mcp.tool(name="currency_converter")
def currency_converter(amount: float,from_currency: str,to_currency:str)-> float:
    currencies=exchange_rate()
    currency_symbol={k.lower(): v  for k,v in currencies.items()}
    from_currency = from_currency.strip().lower()
    to_currency = to_currency.strip().lower()

    if from_currency not in currency_symbol :
        raise ValueError (f"{from_currency} is not supported")
    if to_currency not in currency_symbol:
        raise ValueError (f"{to_currency} is not supported")
    
    from_rate=currency_symbol[from_currency]
    to_rate=currency_symbol[to_currency]
    result=(amount/from_rate)*to_rate
    return round(result,2)

@mcp.prompt(name="greet_user")
def greet_user(name:str):
    currencies=exchange_rate()
    return f'Hello {name}, available currencies are:\n {list(currencies.keys())}'



if __name__=="__main__":
    mcp.run(transport="stdio")