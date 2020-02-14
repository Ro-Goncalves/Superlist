from django.shortcuts import render, redirect

from lists.models import Item, List

# Create your views here.
def home_page(request):        
    return render(request, 'home.html')

def view_list(request): 
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})

def new_list(request):
    list_ = List()
    list_.pk = 1
    Item.objects.create(text=request.POST['item_text']
                        ,list=list_)
    return redirect('/lists/the-only-list-in-the-world/')