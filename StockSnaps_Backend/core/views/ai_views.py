from django.http import JsonResponse

def ai_customer_service(request):
    if request.method == 'POST':
        user_input = request.POST['query']
        response = {"message": f"AI 응답: {user_input}에 대한 도움입니다."}
        return JsonResponse(response)
    return render(request, 'ai_customer_service.html')
