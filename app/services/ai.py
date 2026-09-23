from app.config import GROQ_API_KEY
import requests
from app.database import get_messages, save_message
import json
from app.services.tools import tool_functions, tools
SYSTEM_PROMPT = {
    "role": "system",
    "content": "You are a friendly business assistant. Help users manage customers and orders. Respond clearly, naturally, and briefly. When a tool is needed, use it. After receiving a tool result, use that result directly to answer the user. Do not explain the tool call, show JSON, or teach programming unless the user specifically asks. If no results are found, clearly say so. Do not invent information.  When displaying orders, use a simple bullet list unless a table can be formatted correctly. Before deleting a customer, always ask for confirmation. Do not call the delete_customer tool until the user clearly confirms the deletion,Only use a tool when it directly matches the user's request. If the requested information or capability is not available through the provided tools, say so clearly. Do not substitute unrelated data or tools,After successfully updating an order, use check_order to verify that the requested change was actually applied before giving the final response."
}





def ask_ai(message: str, conversation_id: int):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    messages = [SYSTEM_PROMPT]

    history = get_messages(conversation_id)
    messages.extend(history)

    messages.append({
        "role": "user",
        "content": message
    })

    data = {
        "model": "openai/gpt-oss-20b",
        "messages": messages,
        "tools": tools,
        "tool_choice": "auto",
        "temperature": 0
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=30
        )

        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        print("AI REQUEST ERROR:", e)

        if e.response is not None:
            print("GROQ ERROR:", e.response.text)

        return "Sorry, I'm having trouble connecting to the AI service, please try again in few"

    result = response.json()

    tool_rounds = 0

    executed_tool_calls = set()

    while True:
        tool_rounds += 1

        if tool_rounds > 3:
            reply = "I wasn't able to complete that request."
            break

        assistant_message = result["choices"][0]["message"]

        tool_calls = assistant_message.get("tool_calls")

        if not tool_calls:
            reply = assistant_message.get("content", "")
            break

        messages.append(assistant_message)
        for tool_call in tool_calls:
            function_name = tool_call["function"]["name"]

            try:
                arguments = json.loads(
                    tool_call["function"]["arguments"]
                )

            except json.JSONDecodeError:
                tool_result = f"The arguments provided for the {function_name} tool were invalid."

            else:
                call_key = f"{function_name}:{json.dumps(arguments, sort_keys=True)}"


                if call_key in executed_tool_calls:
                    tool_result = "This tool call was already executed. Do not call it again. Use the previous tool result to answer the user."
                else:
                    executed_tool_calls.add(call_key)

                    tool_function = tool_functions.get(function_name)

                    if tool_function:
                        try:
                            tool_result = tool_function(**arguments)
                        except Exception as e:
                            print("TOOL RESULT:", e)
                            tool_result = f"The {function_name} tool failed while processing the request."
                    else:
                        tool_result = f"Unknown tool: {function_name}"
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "content": str(tool_result)
            })


        data["messages"] = messages

        try:
            response = requests.post(
                url,
                headers=headers,
                json=data,
                timeout=30
            )

          
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print("FOLLOW-UP AI REQUEST ERROR:", e)
            if e.response is not None:
                print("GROQ ERROR:", e.response.text)
            reply = "Sorry, i couldn't complete that request, please try again later"
            break

        result = response.json()
    save_message(conversation_id, "user", message)
    save_message(conversation_id, "assistant", reply)

    return reply