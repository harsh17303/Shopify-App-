# products/views.py
# added
from django.shortcuts import render
import shopify

from django.shortcuts import redirect
from .forms import ProductForm, VariantForm

def fetch_products(request):
    shop_session = shopify.Session.temp(request.session['https://eadf70-d5.myshopify.com/auth/shopify/callback'], request.session['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'])
    shopify.ShopifyResource.activate_session(shop_session)  # Activate the session for the API call

    products = shopify.Product.find()  # Fetch all products
    return render(request, 'products/products.html', {'products': products})
    


# products/views.py (continued)


def update_product(request, product_id):
    shop_session = shopify.Session.temp(request.session['https://eadf70-d5.myshopify.com/auth/shopify/callback'], request.session['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'])
    shopify.ShopifyResource.activate_session(shop_session)

    product = shopify.Product.find(product_id)  # Fetch the specific product
    
    if request.method == 'POST':
        form = ProductForm(request.POST)
        variant_form = VariantForm(request.POST)

        if form.is_valid() and variant_form.is_valid():
            product.title = form.cleaned_data['title']
            product.body_html = form.cleaned_data['description']
            product.save()

            for variant in product.variants:
                variant.sku = variant_form.cleaned_data['sku']
                variant.price = variant_form.cleaned_data['price']
                variant.save()

            return redirect('fetch_products')
    else:
        form = ProductForm(initial={'title': product.title, 'description': product.body_html})
        variant_form = VariantForm(initial={'sku': product.variants[0].sku, 'price': product.variants[0].price})
    
    return render(request, 'products/update_product.html', {'form': form, 'variant_form': variant_form})
