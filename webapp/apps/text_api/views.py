from django.http import JsonResponse


def ping(request):
    return JsonResponse({'success': 'pong'}, status=200)
