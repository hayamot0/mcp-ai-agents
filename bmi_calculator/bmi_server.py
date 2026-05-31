from mcp.server.fastmcp import FastMCP

mcp = FastMCP()

@mcp.resource("resource://bmi_category")
def bmi_category():
    return {
    "Underweight": "below 18.5",
    "Normal": "18.5 to 24.9",
    "Overweight": "25 to 29.9",
    "Obese": "30 and above",
}


@mcp.tool(name="bmi_calculator")
def bmi_calculator(weight:float,height:float)->str:
    result= round(weight / height **2,2)
    if result<18.5:
        return f"Your BMI is {result}: Underweight"
    elif result<25:
        return f"Your BMI is {result}: Normal"
    elif result<30:
        return f"Your BMI is {result}: Overwheight"
    else:
        return f"Your BMI is {result}: Obese"

@mcp.prompt(name="greeting_prompt")
def greet_user(name):
    return f"Hello! {name}, welcome to BMI calculator"


if __name__=="__main__":
    mcp.run(transport="stdio")

