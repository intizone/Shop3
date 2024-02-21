from django.core.paginator import (Paginator, EmptyPage, PageNotAnInteger)


# filter
def search_with_fields(request):
    result = {}
    for key, value in request.GET.items():
        if value:
            if key == 'name':
                key = 'product__name__icontains'
            elif key == 'quantity':
                key = 'quantity'
            elif key == 'created_at_start':
                key = 'created_at__gte'
            elif key == 'created_at_end':
                key = 'created_at__lte'
            elif key == 'page':
                continue
            if key in ['product__name__icontains', 'quantity', 'created_at__gte', 'created_at__lte']:
                result[key] = value
    return result

# pagenator
def pagenator_page(list, num, request):
    paginator = Paginator(list, num)
    pages = request.GET.get('page')
    try:
        list = paginator.page(pages)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)
    return list