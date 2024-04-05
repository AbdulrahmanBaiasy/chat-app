from django.shortcuts import render
from chat.models import Room


def index(request):
    rooms = Room.objects.all()[:8]
    return render(request, "app/index.html", {"rooms": rooms})
