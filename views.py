from django.shortcuts import render,redirect,get_object_or_404

from AdminApp.models import Category,Product,UserInfo,PaymentMaster
from UserApp.models import MyCart,OrderMaster,Checkout,Review
from django.contrib import messages
# Create your views here.
def homepage(request):
    #Fetch all records from Category table
    cats = Category.objects.all()
    cakes = Product.objects.all()
    return render(request,"homepage.html",{"cats":cats,"cakes":cakes})

def login(request):
    if(request.method == "GET"):
        return render(request,"login.html",{})
    else:
        uname = request.POST["uname"]
        password = request.POST["password"]
        try:
            user = UserInfo.objects.get(uname=uname,password=password)
        except:
            messages.success(request,'Invalid Username and Password')
            return redirect(login)
        else:
            #Create the session
            request.session["uname"]=uname
            return redirect(homepage)

def signup(request):
    if(request.method == "GET"):
        return render(request,"signup.html",{})
    else:
        uname = request.POST["uname"]
        password = request.POST["password"]
        email = request.POST["email"]
        user = UserInfo(uname,password,email)
        user.save()
        messages.success(request,'Register Succesfully')
        return redirect(homepage)

def Showpizza(request,id):
    #get method returns single object
    id = Category.objects.get(id=id) 
    #filter method returns multiple objects   
    pizza = Product.objects.filter(cat=id)
    cats = Category.objects.all()    
    return render(request,"homepage.html",{"cats":cats,"cakes":pizza})

def Viewdetails(request,id):
    pizza=Product.objects.get(id=id)
    return render(request,"Viewdetails.html",{"cake":pizza})

def signout(request):
    request.session.clear()
    return redirect(homepage)

def addtocart(request):
    if(request.method == "POST"):
        if("uname" in request.session):
            #Add to cart
            #User and Product
            cakeid = request.POST["cakeid"]
            user = request.session["uname"]
            qty = request.POST["qty"]
            cake = Product.objects.get(id=cakeid)
            user = UserInfo.objects.get(uname = user)
            try:
                cart = MyCart.objects.get(cake=cake,user=user)
            except:
                cart=MyCart()
                cart.user = user
                cart.cake = cake
                cart.qty = qty
                cart.save()
            else:
                pass
            return redirect(homepage)
        else:
            return redirect(login)

def ShowAllCartItems(request):
    uname = request.session["uname"]
    user = UserInfo.objects.get(uname = uname)
    if(request.method == "GET"):       
        cartitems = MyCart.objects.filter(user=user)
        total = 0
        for item in cartitems:
            total+= item.qty*item.cake.price
        request.session["total"] = total
        return render(request,"ShowAllCartItems.html",{"items":cartitems})
    else:
        id = request.POST["cakeid"]
        cake = Product.objects.get(id=id)
        item = MyCart.objects.get(user=user,cake=cake)           
        qty = request.POST["qty"]
        item.qty = qty
        item.save() #Update
        return redirect(ShowAllCartItems)
        
def removeItem(request):
    uname = request.session["uname"]
    user = UserInfo.objects.get(uname = uname)
    id = request.POST["cakeid"]
    cake = Product.objects.get(id=id)
    item = MyCart.objects.get(user=user,cake=cake)   
    item.delete()
    return redirect(ShowAllCartItems)
    
def MakePayment(request):
    if(request.method == "GET"):
        return render(request,"MakePayment.html",{})
    else:
        cardno = request.POST["cardno"]
        cvv = request.POST["cvv"]
        expiry = request.POST["expiry"]
        try:
            buyer = PaymentMaster.objects.get(cardno=cardno,cvv=cvv,expiry=expiry)
        except:
            return redirect(MakePayment)
        else:
            #Its a match
            owner = PaymentMaster.objects.get(cardno='111',cvv='111',expiry='12/2025')
            owner.balance += request.session["total"]
            buyer.balance -=request.session["total"]
            owner.save()
            buyer.save()
            #Delete all items from cart
            uname = request.session["uname"]
            user = UserInfo.objects.get(uname = uname)
            
            order = OrderMaster()
            order.user = user
            order.amount = request.session["total"]
            #order.dateOfOrder = datetime.now
            #Fetch all cart items for that user
            details = ""
            items = MyCart.objects.filter(user=user)
            for item in items:
                details += (item.cake.pname)+","
                item.delete()            
            order.details = details
            order.save()
            return render(request,"PaymentSuccess.html",{})

def Orderdetails(request):
    if(request.method == "GET"):
        return render(request,"Orderdetails.html",{})
    else: 
        name = request.POST['name']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        zip_code = request.POST['zip_code']
        phone = request.POST['phone']

        try:
            phone = int(phone)

        except ValueError:
            messages.error(request, "Invalid Mobile Number")
            return redirect('Orderdetails')

        try:
            zip_code= int(zip_code)

        except ValueError:
            messages.error(request, "Invalid Zip Code")
            return redirect('Orderdetails')

        
        checkout_order = Checkout(name=name, address=address,city=city, state=state, zip_code=zip_code, phone=phone)
        checkout_order.save()
        return redirect(MakePayment)


def reviewsave(request):       
    if(request.method == "POST"):
        uname = request.session["uname"]
        user = UserInfo.objects.get(uname = uname)
            
        rating_star = request.POST['ratings']
        feedback = request.POST['feedback']
        rating = 0
        if rating_star == "star1":
            rating = 5

        elif rating_star == "star2":
            rating = 4

        elif rating_star == "star3":
            rating = 3

        elif rating_star == "star4":
            rating = 2

        elif rating_star == "star5":
            rating = 1

        try:
            feedback = Review( user=uname,ratings=rating, feedback=feedback)
            feedback.save()
           
            return redirect(homepage)

        except Exception as e:
                print(e)
                return redirect(reviewsave)
    else:
        return render(request,"reviews.html",{})


def review(request):
    review_list = Review.objects.all()
    review_count = len(review_list)

    contextlib = {
        'reviews': review_list,
        'review_count': review_count,

    }
    return render(request, 'reviews.html', context=contextlib)



