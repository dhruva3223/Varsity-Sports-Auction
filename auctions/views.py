from annoying.functions import get_object_or_None
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
import razorpay
from django.contrib.postgres.search import SearchVector
from .models import *
from django.contrib.postgres.search import TrigramSimilarity
from django.shortcuts import redirect


def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "The password or the username that you've entered is incorrect.",
                "msg_type": "danger"
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        validatepassword = request.POST["validatepassword"]
        if password != validatepassword:
            return render(request, "auctions/register.html", {
                "message": "Passwords does not match.",
                "msg_type": "danger"
            })
        if not username:
            return render(request, "auctions/register.html", {
                "message": "Please enter your username.",
                "msg_type": "danger"
            })
        if not email:
            return render(request, "auctions/register.html", {
                "message": "Please enter your email.",
                "msg_type": "danger"
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already exists.",
                "msg_type": "danger"
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url='/login')
def filter_product(request, fil_product):
    products = Listing.objects.all()
    if fil_product == 'newest':
        products = Listing.objects.order_by('-created_at')
    elif fil_product == 'hightolow':
        products = Listing.objects.order_by('-starting_bid')
    elif fil_product == 'lowtohigh':
        products = Listing.objects.order_by('starting_bid')
    else:
        products = Listing.objects.order_by('-total_bids')

    empty = False
    if len(products) == 0:
        empty = True
    return render(request, "auctions/filtered.html", {
        "products": products,
        "empty": empty
    })


@login_required(login_url='/login')
def dashboard(request):
    winners = Winner.objects.filter(winner=request.user.username)
    watch_list = Watchlist.objects.filter(user=request.user.username)
    present = False
    watch_list_array = []

    if watch_list:
        present = True
        for item in watch_list:
            product = Listing.objects.get(id=item.listingid)
            watch_list_array.append(product)
    print(watch_list_array)
    return render(request, "auctions/dashboard.html", {
        "product_list": watch_list_array,
        "present": present,
        "products": winners
    })


@login_required(login_url='/login')
def activeauction(request):
    products = Listing.objects.all()
    products = Listing.objects.order_by('-total_bids')
    empty = False
    if len(products) == 0:
        empty = True
    return render(request, "auctions/activeauction.html", {
        "products": products,
        "empty": empty
    })


def is_staff(user):
    return user.is_staff


@user_passes_test(is_staff)
@login_required(login_url='/login')
def createauction(request):
    if request.method == "POST":
        item = Listing()
        item.athlete_name = request.POST.get('athlete_name')
        item.seller = request.user.username
        item.title = request.POST.get('title')
        item.description = request.POST.get('description')
        item.category = request.POST.get('category')
        item.starting_bid = request.POST.get('starting_bid')

        if len(request.FILES) != 0:
            item.image_file = request.FILES['image_file']
        else:
            item.image_file = ""
        item.save()
        products = Listing.objects.all()
        empty = False

        if len(products) == 0:
            empty = True
        return render(request, "auctions/activeauction.html", {
            "products": products,
            "empty": empty,
        })
    else:
        category_list = CategoryList.objects.all()
        return render(request, "auctions/createauction.html",
                      {"category_list": category_list,
                       })


@login_required(login_url='/login')
def categories(request):
    category_list = CategoryList.objects.all()
    return render(request, "auctions/categories.html", {
        "category_list": category_list
    })


@login_required(login_url='/login')
def viewauction(request, product_id):
    comments = Comment.objects.filter(listingid=product_id)
    if request.method == "POST":
        item = Listing.objects.get(id=product_id)
        newbid = int(request.POST.get('newbid'))
        if item.starting_bid >= newbid:
            product = Listing.objects.get(id=product_id)
            return render(request, "auctions/viewauction.html", {
                "product": product,
                "message": "Your Bid should be higher than the Current bid.",
                "msg_type": "danger",
                "comments": comments
            })
        else:
            item.starting_bid = newbid
            item.total_bids += 1
            item.save()

            bidobject = Bid.objects.filter(listingid=product_id)
            if bidobject:
                bidobject.delete()

            object = Bid()
            object.email = request.user.email
            object.user = request.user.username
            object.title = item.title
            object.listingid = product_id
            object.bid = newbid

            object.athlete_name = item.athlete_name
            userphone = userProfile.objects.filter(user=request.user.id)
            object.phone_number = userphone[0].phone_number

            object.save()
            product = Listing.objects.get(id=product_id)
            return render(request, "auctions/viewauction.html", {
                "product": product,
                "message": "Your Bid is added.",
                "msg_type": "success",
                "comments": comments
            })
    else:
        product = Listing.objects.get(id=product_id)
        added = Watchlist.objects.filter(
            listingid=product_id, user=request.user.username)
        return render(request, "auctions/viewauction.html", {
            "product": product,
            "added": added,
            "comments": comments
        })


@login_required(login_url='/login')
def addtowatchlist(request, product_id):
    obj = Watchlist.objects.filter(
        listingid=product_id, user=request.user.username)
    if obj:
        obj.delete()
        return redirect("viewauction", product_id)
    else:
        obj = Watchlist()
        obj.user = request.user.username
        obj.listingid = product_id
        obj.save()
        return redirect("viewauction", product_id)


@login_required(login_url='/login')
def additional_info(request, product_id):
    if request.method == "POST":
        addr = request.POST['user_address']
        pho = request.POST['phone_number']
        extend = userProfile(
            phone_number=pho, user_address=addr, user=request.user)
        extend.save()

    comments = Comment.objects.filter(listingid=product_id)
    product = Listing.objects.get(id=product_id)
    added = Watchlist.objects.filter(
        listingid=product_id, user=request.user.username)
    return render(request, "auctions/viewauction.html", {
        "product": product,
        "added": added,
        "comments": comments
    })


@login_required(login_url='/login')
def addcomment(request, product_id):
    obj = Comment()
    obj.comment = request.POST.get("comment")
    obj.user = request.user.username
    obj.listingid = product_id
    obj.save()
    return redirect("viewauction", product_id)


@login_required(login_url='/login')
def category(request, categ):
    categ_products = Listing.objects.filter(category=categ)
    empty = False
    if len(categ_products) == 0:
        empty = True
    return render(request, "auctions/category.html", {
        "categ": categ,
        "empty": empty,
        "products": categ_products
    })

# search product


@login_required(login_url='/login')
def searching(request):
    search_product = ""
    if request.method == "POST":
        search_product = request.POST['query']
        found_products = Listing.objects.annotate(similarity=TrigramSimilarity('title', search_product)).filter(similarity__gt=0.1).order_by('-similarity') | Listing.objects.annotate(similarity=TrigramSimilarity('athlete_name', search_product)).filter(similarity__gt=0.1).order_by('-similarity')
    empty = False
    if len(found_products) == 0:
        empty = True
    return render(request, "auctions/searching.html", {
        "search_product": search_product,
        "empty": empty,
        "found_products": found_products
    })


@login_required(login_url='/login')
def closebid(request, product_id):
    winobject = Winner()
    listobj = Listing.objects.get(id=product_id)
    obj = get_object_or_None(Bid, listingid=product_id)
    if not obj:
        message = "Deleting Bid"
        msg_type = "danger"
    else:
        bidobject = Bid.objects.get(listingid=product_id)

        # payment
        key_id = 'YOUR ID'
        key_secret = 'YOUR SECRET KEY'
        client = razorpay.Client(auth=(key_id, key_secret))
        createpayment = client.payment_link.create({
            "amount": int(bidobject.bid)*100,
            "currency": "INR",
            "description": bidobject.title,
            "customer": {
                "name": bidobject.user,
                "email": bidobject.email,
                "contact": bidobject.phone_number,
            },
            "notify": {
                "sms": "true",
                "email": "true",
            },
            "reminder_enable": "true",
            "notes": {
                "policy_name": "Project"
            },
        })
        print(createpayment)

        # winner object
        winobject.owner = request.user.username
        winobject.winner = bidobject.user
        winobject.listingid = product_id
        winobject.winprice = bidobject.bid
        winobject.title = bidobject.title
        winobject.athlete_name = bidobject.athlete_name
        winobject.save()
        message = "Bid Closed"
        msg_type = "success"
        bidobject.delete()
    if Watchlist.objects.filter(listingid=product_id):
        watchobj = Watchlist.objects.filter(listingid=product_id)
        watchobj.delete()
    if Comment.objects.filter(listingid=product_id):
        commentobj = Comment.objects.filter(listingid=product_id)
        commentobj.delete()
    listobj.delete()
    winners = Winner.objects.all()
    empty = False
    if len(winners) == 0:
        empty = True
    return render(request, "auctions/closedauction.html", {
        "products": winners,
        "empty": empty,
        "message": message,
        "msg_type": msg_type
    })


@login_required(login_url='/login')
def closedauction(request):
    winners = Winner.objects.all().order_by('-listingid')
    empty = False
    if len(winners) == 0:
        empty = True
    return render(request, "auctions/closedauction.html", {
        "products": winners,
        "empty": empty
    })
