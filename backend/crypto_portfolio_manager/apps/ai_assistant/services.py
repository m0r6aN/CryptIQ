from crypto_portfolio_manager.apps.ai_assistant import tools
import openai
import settings

openai.api_key = settings.OPEN_AI_API_KEY

messages = [
    {"role": "system", "content": "You are a helpful customer support assistant. Use the supplied tools to assist the user."},
]

def get_ai_response(messages):
    response = openai.Completion.create(
        engine='gpt-4o',
        messages=messages,
        tools=tools,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

# Choice(
#     finish_reason='tool_calls', 
#     index=0, 
#     logprobs=None, 
#     message=chat.completionsMessage(
#         content=None, 
#         role='assistant', 
#         function_call=None, 
#         tool_calls=[
#             chat.completionsMessageToolCall(
#                 id='call_62136354', 
#                 function=Function(
#                     arguments='{"order_id":"order_12345"}', 
#                     name='get_delivery_date'), 
#                 type='function')
#         ])
# )