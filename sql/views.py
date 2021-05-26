from django.shortcuts import render

# Create your views here.
def test1(request):
    context = {'currentMenu': 123}
    return render(request, 'base.html', context)