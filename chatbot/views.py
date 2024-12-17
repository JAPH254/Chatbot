import openai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Set your OpenAI API key
openai.api_key = "your key"

@csrf_exempt
def chatbot_view(request):
    if request.method == 'POST':
        try:
            # Load JSON data sent to the endpoint
            data = json.loads(request.body)
            user_input = data.get('message')

            if not user_input:
                return JsonResponse({"response": "Please provide a message."}, status=400)

            # Call OpenAI ChatCompletion API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # GPT-3.5-turbo or GPT-4
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_input}
                ]
            )

            # Extract the chatbot's response
            bot_reply = response.choices[0].message.content.strip()
            return JsonResponse({"response": bot_reply})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "POST request required"}, status=405)
