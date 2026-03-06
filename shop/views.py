from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from .models import Category, Product, Brand
from .forms import InquiryForm


def home(request):
    categories = Category.objects.all()
    return render(request, "home.html", {"categories": categories})


def products(request):
    all_products = Product.objects.select_related('category', 'brand').all()
    categories = Category.objects.all()
    brands = Brand.objects.all()

    category_id = request.GET.get('category')
    brand_id = request.GET.get('brand')
    search = request.GET.get('search', '').strip()

    if category_id:
        all_products = all_products.filter(category__id=category_id)
    if brand_id:
        all_products = all_products.filter(brand__id=brand_id)
    if search:
        all_products = all_products.filter(name__icontains=search)

    return render(request, 'products.html', {
        'products': all_products,
        'categories': categories,
        'brands': brands,
        'selected_category': category_id,
        'selected_brand': brand_id,
        'search': search,
    })


def category_detail(request, id):
    category = get_object_or_404(Category, id=id)
    products = Product.objects.filter(category=category).select_related('brand')
    return render(request, 'category.html', {
        'category': category,
        'products': products,
    })


def contact(request):
    if request.method == 'POST':
        name    = request.POST.get('name', '').strip()
        phone   = request.POST.get('phone', '').strip()
        email   = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        # Send email notification
        try:
            send_mail(
                subject=f'New Contact Message from {name}',
                message=(
                    f'Name:    {name}\n'
                    f'Phone:   {phone}\n'
                    f'Email:   {email}\n\n'
                    f'Message:\n{message}'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.NOTIFY_EMAIL],
                fail_silently=False,
            )
        except Exception:
            pass  # Don't block the user if email fails

        return render(request, 'success.html')
    return render(request, 'contact.html')


def request_quote(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save()

            # Send email notification
            try:
                send_mail(
                    subject=f'New Quote Request from {inquiry.name}',
                    message=(
                        f'Name:    {inquiry.name}\n'
                        f'Phone:   {inquiry.phone}\n'
                        f'Product: {inquiry.product.name} '
                        f'({inquiry.product.category.name})\n\n'
                        f'Message:\n{inquiry.message}'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.NOTIFY_EMAIL],
                    fail_silently=False,
                )
            except Exception:
                pass  # Don't block the user if email fails

            return render(request, 'success.html')
    else:
        form = InquiryForm()
    return render(request, 'request_quote.html', {'form': form})