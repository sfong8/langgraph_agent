from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain.messages import SystemMessage
# Initialize Groq LLM
model = ChatGroq(
    model_name="qwen/qwen3-32b",
    temperature=0.1
)

# addition tool
@tool    # This identifies the following function as a tool to LangGraph
# in the following statement the function name, the attributes their types and the output type are defined
def addition(x:int, y:int) -> int :
    # The following docstring describes what the function can do and is used by the LLM to determine whethere this
    # is the tool to be called, and what are its inputs and outputs
    """
    This addition function adds two numbers and returns their sum.
    It takes two integers as its inputs and the output is an integer.
    """
    return x + y

# subtraction tool
@tool
def subtraction(x:int, y:int) -> int :
    """
    This subtraction function subtracts a number from another and returns the difference.
    It takes two integers as its inputs and the output is an integer.
    """
    return x - y
# multiplication tool
@tool
def multiplication(x:int, y:int) -> int :
    """
    This multiplication function multiplies two numbers returns the product.
    It takes two integers as its inputs and the output is an integer.
    """
    return x * y
# division tool
@tool
def division(x:int, y:int) -> int :
    """
    This division function divides one number by another and returns the quotient.
    It takes two integers as its inputs and the output is an integer.
    """
    return x / y



# Initialize Groq LLM
model = ChatGroq(
    model_name="qwen/qwen3-32b",
    temperature=0.1
)
arithmeticagent_system_prompt = SystemMessage(
    """You are a mathematics agent that can solve simple mathematics problems like addition, subtraction, multiplication and division. 
    Solve the mathematics problems provided by the user using only the available tools and not by yourself. Provide the answer given by the tool.  
    Provide the answer given by the tool.
    """
)

arithmeticagent_tools = [addition, subtraction, multiplication, division]
agent = create_agent(model, system_prompt = arithmeticagent_system_prompt, tools=arithmeticagent_tools)


while True :
    prompt_query = input("Enter a simple mathematics question or a question about employees (or exit to stop): ")
    if prompt_query == "exit" :
        print("Exiting")
        break
    else:
        inputs = {"messages":[("user", prompt_query)]}
        result = agent.invoke(inputs)
        print(f"Agent response : {result['messages'][-1].content} \n")
        detailed_yn = input("Do you want a detailed explanation? (y/n) :")
        if detailed_yn == "y" :
            print("Detailed execution flow : ")
            for message in result['messages']:
                print(message.pretty_repr())