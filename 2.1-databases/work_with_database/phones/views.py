from django.shortcuts import render, redirect, get_object_or_404

from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    sort_by = request.GET.get('sort')
    phones = Phone.objects.all()
    if sort_by:
        if sort_by == 'name':
            phones = Phone.objects.order_by('name')
        elif sort_by == 'min_price':
            phones = Phone.objects.order_by('price')
        elif sort_by == 'max_price':
            phones = Phone.objects.order_by('-price')
    context = {
        'phones': phones,
    }
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone = get_object_or_404(Phone, slug=slug)
    context = {
        'phone': phone,
    }
    return render(request, template, context)
