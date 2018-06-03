from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import  render_to_response


# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from app.models import Category, Product, Productimage, Propertyvalue, Property, User, Cart
def app(request):
    name = request.COOKIES.get('name', '')
    categorylist = Category.objects.all()[:4]
    clist=[]
    for i in categorylist:
        cid=i.id
        products=Product.objects.filter(cid_id=cid)
        ps=[]
        for j in products:
            pid=j.id
            try:
                l=Productimage.objects.filter(typ='type_single',pid_id=pid)
                id=l.first().id
                img="/static/img/productSingle/%s.jpg"%id
            except:
                img='/static/img/site/tmallbuy.png'
            product={'id':j.id,'name':j.name,'price':j.promotePrice,'img':img}
            ps.append(product)
        category={'id':i.id,'name':i.name,'products':ps}
        clist.append(category)
    return render_to_response('index.html' ,{'name':name,'clist':clist})
def product(request):
    name = request.COOKIES.get('name', '')
    pid=request.GET['pid']
    product=Product.objects.get(id=pid)
    cid=product.cid_id
    headimg="/static/img/category/%s.jpg"%cid
    images=Productimage.objects.filter(pid_id=pid,typ='type_single')
    image=[]
    for i in images:
        id=i.id
        img="/static/img/productSingle/%s.jpg"%id
        image.append(img)
    detailImages=Productimage.objects.filter(pid_id=pid,typ='type_detail')
    detailImage = []
    for i in detailImages:
        id = i.id
        img = "/static/img/productDetail/%s.jpg" % id
        detailImage.append(img)
    propertys=Property.objects.filter(cid_id=cid)
    propertyValues=[]
    for i in propertys:
        ptid=i.id
        try:
            value=Propertyvalue.objects.get(ptid_id=ptid,pid_id=pid).value
        except:
            value=''
        propertyvalue={'property':i.name,'value':value}
        propertyValues.append(propertyvalue)
    return render_to_response('product.html', {'name': name,'product':product,'headimg':headimg,'image':image,'defaultimg':image[0],'detailImage':detailImage,
                                               'propertyValues': propertyValues})
def forecategory(request):
    name = request.COOKIES.get('name', '')
    cid=request.GET['cid']
    headimg="/static/img/category/%s.jpg"%cid
    productlist = Product.objects.filter(cid_id=cid)
    products=[]
    for i in productlist:
        pid=i.id
        imgs = Productimage.objects.filter(pid_id=pid, typ='type_single')
        imgid=imgs.first().id
        img="/static/img/productSingle/%s.jpg"%imgid
        product={'id':i.id,'promotePrice':i.promotePrice,'name':i.name,'img':img}
        products.append(product)
    return render_to_response('forecategory.html', {'name': name,'headimg':headimg,'products':products})
@csrf_exempt
def addcart(request):
    if request.method == 'POST':
        pid=request.POST['pid']
        price=request.POST['add_price']
        amount=request.POST['amount']
        name=request.COOKIES.get('name', '')
        uid=User.objects.get(name=name).id
        if name !='':
            Cart.objects.create(uid=uid,pid=pid,price=price,amount=amount)
            return JsonResponse({"status": 'ok'})
        else:
            return JsonResponse({"status": 'no'})
def cart(request):
    if request.method == 'GET':
        try:
            name = request.COOKIES.get('name', '')
            uid = User.objects.get(name=name).id
            cartlist=Cart.objects.filter(uid=uid)
            carts=[]
            for cart in cartlist:
                price=cart.price
                amount=cart.amount
                pro=Product.objects.get(id=cart.pid)
                product = {'id':pro.id,'subTitle':pro.subTitle,'orignalPrice':pro.orignalPrice,
                         'promotePrice':pro.promotePrice,'stock':pro.stock}
                img = Productimage.objects.filter(typ="type_single", pid_id=cart.pid)
                id = img.first().id
                product['img'] = '/static/img/productSingle/%s.jpg' % id
                c={'id':cart.id,'price':price,'amount':amount,'product':product}
                carts.append(c)
            return render_to_response('cart.html', {'carts':carts})
        except:
            response = HttpResponseRedirect('/login/')
            return  response