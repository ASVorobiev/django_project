from django.shortcuts import render


def main(request):
    return render(request, 'about/index.html', {'pass': 'pass'})