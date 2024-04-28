from django.shortcuts import render

# Create your views here.

def Home(request):
    return render(request, "index.html")

def Account(request):
    return render(request, "account.html")

def Post(request):
    return render(request, "post.html")

def Comment(request):
    return render(request, "comment.html")

def Notification(request):
    return render(request, "notification.html")

def Tag(request):
    return render(request, "tag.html")