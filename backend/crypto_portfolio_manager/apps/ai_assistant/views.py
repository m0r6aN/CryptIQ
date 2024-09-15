from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import get_ai_response

class AIChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        prompt = request.data.get('prompt', '')
        if not prompt:
            return Response({'error': 'Prompt is required.'}, status=400)
        response_text = get_ai_response(prompt)
        return Response({'response': response_text})
