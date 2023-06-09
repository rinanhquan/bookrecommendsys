from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from .models import *
from django.http import JsonResponse
import random
from django.views.decorators.csrf import csrf_exempt
from .serializers import GetProduct
from django.core import serializers
import json
from django.forms.models import model_to_dict
from requests import request
from django.contrib.auth import authenticate,login,logout,decorators
from django.core.paginator import Paginator
from .forms import CreateUserForm
from .colab_filltering import get_item_cf_for_user,process_data,get_author_cf_for_user
from .content_based import get_item_cb_for_user
import json
import numpy as np
from django.db.models import Q
from numpy import random
from datetime import datetime, timezone
import random
from django.db.models import Avg 
@csrf_exempt
def recommend(request):
	json_data = json.loads(request.body) 
	user_id= json_data['user_id']
	arrProductRatingCb =[]
	arrProductRatingCf =[]
	arrProductRatingAuthor =[]
	
	try:
		exituser = Rating.objects.filter(user_id=user_id)
	except:
		exituser=False
	
	
	if exituser:
		rating = Rating.objects.all()
		category = Category.objects.all()
		product = Product.objects.all()

		data = { "code":"001","Rating" :list(rating.values("rating_id", "product_id","user_id","rating")),"Category":list(category.values("category_id", "category_name")),"Product":list(product.values("product_id", "category_id", "prodcut_num", "product_intro", "product_name", "product_picture","product_price","product_title","author_id"))
			}
		try:
			listProductcf = get_item_cf_for_user(data,user_id)
		except:
			listProductcf = random.sample(range(1, 30), 4)
	      

		for i in listProductcf:
			product = model_to_dict(Product.objects.get(product_id=i))
			rating_numbercf = 0
			try:
				if Rating_Star.objects.filter(product_id=i):
					rating_numbercf = round(Rating_Star.objects.filter(product_id=i).aggregate(Avg('rating'))['rating__avg'],1)
				else:
					rating_numbercf = 0
			except:
				rating_numbercf = 0
			product['rating'] = rating_numbercf

			arrProductRatingCf.append(product)
		try:
			listProductcb = get_item_cb_for_user(data,data,data,user_id)
		except :
			listProductcb = random.sample(range(1, 30), 4)

		for i in listProductcb:
			product = model_to_dict(Product.objects.get(product_id=i))
			rating_numbercb = 0
			try:
				if Rating_Star.objects.filter(product_id=i):
					rating_numbercb = round(Rating_Star.objects.filter(product_id=i).aggregate(Avg('rating'))['rating__avg'],1)
					# rating_numbercb = productRating.rating
				else:
					rating_numbercb = 0
			except:
				rating_numbercb = 0
			product['rating'] = rating_numbercb
			arrProductRatingCb.append(product)
       
	else:
		obj = Product.objects.all().order_by('product_id')[:4] 
		ListProduct = list(obj.values("product_id", "category_id", "prodcut_num", "product_intro", "product_name", "product_picture","product_price","product_title","author_id"))
		for product in ListProduct:
			arrProductRatingCf.append(product)
		obj2 = Product.objects.all().order_by('product_id')[:4] 
		ListProduct2 = list(obj2.values("product_id", "category_id", "prodcut_num", "product_intro", "product_name", "product_picture","product_price","product_title","author_id"))
		for product2 in ListProduct2:
			arrProductRatingCb.append(product2)
	try:
		exituser_author = Rating_Author.objects.filter(user_id=user_id)
	except:
		exituser_author=False
	if exituser_author:
		print('exits')
		rating_author = Rating_Author.objects.all()
		
		author = Author.objects.all()
		product = Product.objects.all()
		rating = Rating.objects.all()
		total = len(rating)
		category = Category.objects.all()

		data = { "code":"001","Rating" :list(rating.values("rating_id", "product_id","user_id","rating")),"Rating_author":list(rating_author.values("rating_id", "author_id","user_id","rating")),"category":list(category.values("category_id", "category_name")),"Product":list(product.values("product_id", "category_id", "prodcut_num", "product_intro", "product_name", "product_picture","product_price","product_title","author_id"))
			}
		try:
			listProductauthor = get_author_cf_for_user(data,user_id)[:4]
		except:
			listProductauthor =random.sample(range(1, 30), 4)
		for i in listProductauthor:
			product = model_to_dict(Product.objects.get(product_id=i))
			rating_numberauthor = 0
			try:
				if Rating_Star.objects.filter(product_id=i):
					# productRating = Rating_Star.objects.get(product_id=i)
					# rating_numberauthor = productRating.rating
					rating_numberauthor = round(Rating_Star.objects.filter(product_id=i).aggregate(Avg('rating'))['rating__avg'],1)
				else:
					rating_numberauthor = 0
			except:
				rating_numberauthor = 0
			product['rating'] = rating_numberauthor
			arrProductRatingAuthor.append(product)
	else:
		print('none')
		obj = Product.objects.all().order_by('product_id')[:4] 
		total = len(obj)
		ListProduct = list(obj.values("product_id", "category_id", "prodcut_num", "product_intro", "product_name", "product_picture","product_price","product_title","author_id"))
		for product in ListProduct:
			rating_numberauthor = 0
			try:
				if Rating_Star.objects.filter(product_id=product.product_id):
					# productRating = Rating_Star.objects.get(product_id=i)
					# rating_numberauthor = productRating.rating
					rating_numberauthor = round(Rating_Star.objects.filter(product_id=product.product_id).aggregate(Avg('rating'))['rating__avg'],1)
				else:
					rating_numberauthor = 0
			except:
				rating_numberauthor = 0
			product['rating'] = rating_numberauthor
			arrProductRatingAuthor.append(product)


	return JsonResponse({"code":"001","ProductRatingCb":arrProductRatingCb,"ProductRatingCf":arrProductRatingCf,"ProductRatingAuthor":arrProductRatingAuthor})

@csrf_exempt
def getPromoProduct(request):
	arrproduct1 = []
	top_ratings = Rating_Star.objects.order_by('-rating')[:12]
	print(top_ratings)
	for rate in top_ratings:
		obj = Product.objects.get(product_id=rate.product_id)
		dictProduct = model_to_dict(obj)
		dictProduct['rating'] = rate.rating
		arrproduct1.append(dictProduct)
	if len(arrproduct1) <12:
		number = 12-int(len(arrproduct1))
		obj = Product.objects.all().order_by('product_id')[:number]
		for product in obj:
			dictProduct = model_to_dict(product)
			dictProduct['rating'] = 0
			arrproduct1.append(dictProduct)
	data = { "code":"001","ProductRatingAuthor" :arrproduct1[4:8],"ProductRatingCb" :arrproduct1[8:12],"ProductRatingCf" :arrproduct1[:4]
		}
	
	return JsonResponse(data)
@csrf_exempt        
def getCategory(request):
	obj = Category.objects.all()
	total = len(obj)
	data = { "category" :list(obj.values("category_id", "category_name"))
		}
	
	return JsonResponse(data)
@csrf_exempt        
def getProductByCategory(request):
	json_data = json.loads(request.body) 
	categoryID = int(json_data['categoryID'][0])
	currentPage = int(json_data['currentPage'])
	pageSize = int(json_data['pageSize'])
	listProduct = Product.objects.filter(category_id=categoryID)
	p = Paginator(listProduct, pageSize)   
	listProductPage = p.get_page(currentPage).object_list
	arrproduct = []
	for product in listProductPage:
		rating_numberauthor = 0
		try:
			if Rating_Star.objects.filter(product_id=product.product_id):
				# productRating = Rating_Star.objects.get(product_id=product.product_id)
				# rating_numberauthor = productRating.rating
				rating_numberauthor = round(Rating_Star.objects.filter(product_id=product.product_id).aggregate(Avg('rating'))['rating__avg'],1)
		except:
			rating_numberauthor = 0
		dictProduct = model_to_dict(product)
		dictProduct['rating'] = rating_numberauthor
		arrproduct.append(dictProduct)
	data = { "Product" :arrproduct,"total":len(arrproduct)
		}
	return JsonResponse(data)
@csrf_exempt        
def getShoppingCart(request):

	user_id = request.GET.get('user_id')
	b = ShoppingCart.objects.filter(user_id=user_id)
	arrProduct = []
	for p in b.values():

		product = Product.objects.get(product_id=p['product_id'])
		shoppingCartDataTemp = {
			"id": p['shoppingCart_id'],
			"productID": product.product_id,
			"productName": product.product_name,
			"productImg": product.product_picture,
			"price": product.product_price,
			"num": p['num'],
			"maxNum": product.prodcut_num,
			"check": False  ,
			'author_id' : product.author_id
		}
		arrProduct.append(shoppingCartDataTemp)
	data = { "code":"001","shoppingCartData" :arrProduct}
	      
	return JsonResponse(data)


@csrf_exempt        
def addOrder(request):
	json_data = json.loads(request.body) 
	user_id = json_data['user_id']
	products = json_data['products']
	nowTime = datetime.now(tz=timezone.utc)
	for product in products:
		
		try:
			lastOrder = Order.objects.last()
			Order_idobj = int(lastOrder.order_id) + 1
		except:
			Order_idobj = 0
		
		try : 
			if Rating.objects.get(user_id=user_id,product_id=product['productID']):
				objRating = Rating.objects.get(user_id=user_id,product_id=product['productID'])
				objRating.rating =  objRating.rating + 5
				
				objRating.save()
			else :
				if len(Rating.objects.all()) ==0:
					rating_idobj = 0
				else:
					lastRating = Rating.objects.last()
					rating_idobj = int(lastRating.rating_id) + 1
				NewobjRating = Rating(rating_id=rating_idobj,user_id=user_id,product_id=product['productID'],rating=5)
				NewobjRating.save()

		except:
			lastRating = Rating.objects.last()
			rating_idobj = int(lastRating.rating_id) + 1
			objRating = Rating(rating_id=rating_idobj,user_id=user_id,product_id=product['productID'],rating=5)
			objRating.save()
		
		try : 
			if Rating_Author.objects.get(user_id=user_id,author_id=product['author_id']):
				objRating = Rating_Author.objects.get(user_id=user_id,author_id=product['author_id'])
				objRating.rating =  objRating.rating + 5
				objRating.save()
				msg="Plus Rating OK"
			else :
				if len(Rating_Author.objects.all()) ==0:
					rating_idobj = 0
				else:
					lastRating = Rating_Author.objects.last()
					rating_idobj = int(lastRating.rating_id) + 5
				NewobjRating = Rating_Author(rating_id=rating_idobj,user_id=user_id,author_id=product['author_id'],rating=1)
				NewobjRating.save()

		except:
			lastRating1 = Rating_Author.objects.last()
			rating_idobj1 = int(lastRating1.rating_id) + 1
			objRating1 = Rating_Author(rating_id=rating_idobj1,user_id=user_id,author_id=product['author_id'],rating=5)
			objRating1.save()
		orderObj = Order(order_id=Order_idobj,user_id=user_id,product_id=product['productID'],product_num=product['num'],product_price=product['price'],order_time=nowTime)
		orderObj.save()
		
	try:
		shoppingCartObj = ShoppingCart.objects.filter(user_id=user_id)
		shoppingCartObj.delete()
	except:
		msgCard = "ShoppongCart Delete OK"
	data = { "code":"001","msg" :"Add Order OK"}
	      
	return JsonResponse(data)


@csrf_exempt
def getAllProduct(request):
	json_data = json.loads(request.body)
	currentPage = int(json_data['currentPage'])
	pageSize = int(json_data['pageSize'])
	listProduct = Product.objects.filter()
	total = len(listProduct)
	p = Paginator(listProduct, pageSize)   
	obj = p.get_page(currentPage).object_list
	arrproduct = []
	for product in obj:
		try:
			print(Rating_Star.objects.filter(product_id=product.product_id))
			if Rating_Star.objects.filter(product_id=product.product_id):
				rating_numberauthor = round(Rating_Star.objects.filter(product_id=product.product_id).aggregate(Avg('rating'))['rating__avg'],1)
		except:
			rating_numberauthor = 0
		dictProduct = model_to_dict(product)
		dictProduct['rating'] = rating_numberauthor
		arrproduct.append(dictProduct)
	data = { "code":"001","total":total,"Product" :arrproduct
		}

	return JsonResponse(data)

@csrf_exempt
def getProductBySearch(request):

	json_data = json.loads(request.body) 
	key = json_data['search']
	currentPage = int(json_data['currentPage'])
	pageSize = int(json_data['pageSize'])
	listProduct = Product.objects.filter(Q(product_intro__contains=str(key)) | Q(product_name__contains=str(key)))
	p = Paginator(listProduct, pageSize)   
	listProductPage = p.get_page(currentPage).object_list
	arrproduct = []
	for product in listProductPage:
		rating_numberauthor = 0
		try:
			if Rating_Star.objects.filter(product_id=product.product_id):
				rating_numberauthor = round(Rating_Star.objects.filter(product_id=product.product_id).aggregate(Avg('rating'))['rating__avg'],1)
				
				# productRating = Rating_Star.objects.get(product_id=product.product_id)
				# rating_numberauthor = productRating.rating
		except:
			rating_numberauthor = 0
		dictProduct = model_to_dict(product)
		dictProduct['rating'] = rating_numberauthor
		arrproduct.append(dictProduct)
	data = { "Product" :arrproduct,"total":len(arrproduct)
		}
	return JsonResponse(data)
	

@csrf_exempt
def getDetails(request):
	
	id = request.GET.get('productID')
	obj = Product.objects.get(product_id=int(id))
	
	user_id= request.GET.get('user_id')
	rating = 0
	try:
		if Rating_Star.objects.filter(product_id=int(id)):
			rating = round(Rating_Star.objects.filter(product_id=int(id)).aggregate(Avg('rating'))['rating__avg'],1)
		else:
			rating = 0
	except:
		rating = 0
	if  user_id:
		try : 
			if Rating.objects.get(user_id=user_id,product_id=id):
				objRating = Rating.objects.get(user_id=user_id,product_id=id)
				objRating.rating =  objRating.rating + 1
				
				objRating.save()
			else :
				if len(Rating.objects.all()) ==0:
					rating_idobj = 0
				else:
					lastRating = Rating.objects.last()
					rating_idobj = int(lastRating.rating_id) + 1
				NewobjRating = Rating(rating_id=rating_idobj,user_id=user_id,product_id=id,rating=2)
				NewobjRating.save()
			
		except:
			lastRating = Rating.objects.last()
			rating_idobj = int(lastRating.rating_id) + 1
			objRating = Rating(rating_id=rating_idobj,user_id=user_id,product_id=id,rating=1)
			objRating.save()
			
		try : 
			if Rating_Author.objects.get(user_id=user_id,author_id=obj.author_id):
				objRating = Rating_Author.objects.get(user_id=user_id,author_id=obj.author_id)
				objRating.rating =  objRating.rating + 1
				objRating.save()
				msg="Plus Rating OK"
			else :
				if len(Rating_Author.objects.all()) ==0:
					rating_idobj = 0
				else:
					lastRating = Rating_Author.objects.last()
					rating_idobj = int(lastRating.rating_id) + 1
				NewobjRating = Rating_Author(rating_id=rating_idobj,user_id=user_id,author_id=obj.author_id,rating=1)
				NewobjRating.save()
			
		except:
			lastRating = Rating_Author.objects.last()
			rating_idobj = int(lastRating.rating_id) + 1
			objRating = Rating_Author(rating_id=rating_idobj,user_id=user_id,author_id=obj.author_id,rating=1)
			objRating.save()
		

	data = { "code":"001","Product" :model_to_dict(obj),'Rating':rating
		}
	return JsonResponse(data)

@csrf_exempt
def addShoppingCart(request):
	json_data = json.loads(request.body) 
	user_id = json_data['user_id']
	product_id = json_data['product_id']
	try :
		lastShoppingCart = ShoppingCart.objects.last()
		idShoppingCartCreate = int(lastShoppingCart.shoppingCart_id) + 1
	except:
		idShoppingCartCreate = 0

	b = ShoppingCart(shoppingCart_id=idShoppingCartCreate,user_id=user_id, product_id=product_id,num=1)
	b.save()
	product = Product.objects.get(product_id=int(product_id))
	shoppingCartDataTemp = {
		"id": b.shoppingCart_id,
		"productID": product.product_id,
		"productName": product.product_name,
		"productImg": product.product_picture,
		"price": product.product_price,
		"num": b.num,
		"maxNum": product.prodcut_num,
		"check": False,
		"author_id":product.author_id
	}
	
	try : 
		if Rating.objects.get(user_id=user_id,product_id=product_id):
			objRating = Rating.objects.get(user_id=user_id,product_id=product_id)
			objRating.rating =  objRating.rating + 2
			objRating.save()
			msg="Plus Rating OK"
		else :
			if len(Rating.objects.all()) ==0:
				rating_idobj = 0
			else:
				lastRating = Rating.objects.last()
				rating_idobj = int(lastRating.rating_id) + 1
			NewobjRating = Rating(rating_id=rating_idobj,user_id=user_id,product_id=product_id,rating=2)
			NewobjRating.save()

	except:
		lastRating = Rating.objects.last()
		rating_idobj = int(lastRating.rating_id) + 1
		objRating = Rating(rating_id=rating_idobj,user_id=user_id,product_id=product_id,rating=2)
		objRating.save()
		msg ="Create Rating OK"
	
	try : 
		if Rating_Author.objects.get(user_id=user_id,author_id=product.author_id):
			objRating = Rating_Author.objects.get(user_id=user_id,author_id=product.author_id)
			objRating.rating =  objRating.rating + 2
			objRating.save()
			msg="Plus Rating OK"
		else :
			if len(Rating_Author.objects.all()) ==0:
				rating_idobj = 0
			else:
				lastRating = Rating_Author.objects.last()
				rating_idobj = int(lastRating.rating_id) + 1
			NewobjRating = Rating_Author(rating_id=rating_idobj,user_id=user_id,product_id=id,rating=2)
			NewobjRating.save()
	except:
		lastRating = Rating_Author.objects.last()
		rating_idobj = int(lastRating.rating_id) + 1
		objRating = Rating_Author(rating_id=rating_idobj,user_id=user_id,author_id=product.author_id,rating=2)
		objRating.save()
		msg ="Create Rating OK"
	
	data = { "code":"001","shoppingCartData" :[shoppingCartDataTemp],"msgRate":msg
		}
	
	return JsonResponse(data)
	
@csrf_exempt
def voteStar(request):
	json_data = json.loads(request.body) 
	user_id = json_data['user_id']
	product_id = json_data['product_id']
	star = int(json_data['star'])
	data = { "code":"001","msg":"Vote Star Ok"
		}
	try : 
		if Rating.objects.get(user_id=user_id,product_id=product_id):
			objRating = Rating.objects.get(user_id=user_id,product_id=product_id)
			if star == 1:
				if objRating.rating >1:
					objRating.rating =  objRating.rating -1
				else :
					objRating.rating =  0
			elif star == 2:
				if objRating.rating >2:
					objRating.rating =  objRating.rating -2
				else :
					objRating.rating =  0
			elif star == 3:   
				objRating.rating =  objRating.rating
			elif star == 4:
				objRating.rating =  objRating.rating +1
			else :
				objRating.rating =  objRating.rating + 2
			objRating.save()
		else :
			if len(Rating.objects.all()) ==0:
				rating_idobj = 0
			else:
				lastRating = Rating.objects.last()
				rating_idobj = int(lastRating.rating_id) + 1
			objRating = Rating(rating_id=rating_idobj,user_id=user_id,product_id=product_id,rating=star)
			objRating.save()
	except :
		if len(Rating.objects.all()) ==0:
				rating_idobj = 0
		else:
			lastRating = Rating.objects.last()
			rating_idobj = int(lastRating.rating_id) + 1
		objRating = Rating(rating_id=rating_idobj,user_id=user_id,product_id=product_id,rating=star)
		objRating.save()
	try:
		print('try')
		if Rating_Star.objects.get(user_id=user_id,product_id=product_id):
			objRating_Star = Rating_Star.objects.get(user_id=user_id,product_id=product_id)
			print(objRating_Star)
			print(objRating_Star.rating)
			objRating_Star.rating =  round((objRating_Star.rating +star)/2, 1)
			print(objRating_Star.rating)
			objRating_Star.save()
		else :  
			if len(Rating_Star.objects.all()) ==0:
				rating_idobj = 0
			else:
				lastRating = Rating_Star.objects.last()
				rating_idobj = int(lastRating.rating_id) + 1
			
			objRating_Star = Rating_Star(rating_id=rating_idobj,user_id=user_id,product_id=product_id,rating=star)
			objRating_Star.save()
	
	except:
		print('except')
		if len(Rating_Star.objects.all()) ==0:
				rating_idobj = 0
		else:
			lastRating = Rating_Star.objects.last()
			rating_idobj = int(lastRating.rating_id) + 1
		
		objRating_Star = Rating_Star(rating_id=rating_idobj,user_id=user_id,product_id=product_id,rating=star)
		print(objRating_Star)
		objRating_Star.save()
		
	
	return JsonResponse(data)
		


@csrf_exempt
def updateShoppingCart(request):
	json_data = json.loads(request.body) 
	user_id = json_data['user_id']
	product_id = json_data['product_id']
	num = json_data['num']
	tmpshoppingCart = ShoppingCart.objects.get(user_id=user_id,product_id=product_id)
	tmpshoppingCart.num = num
	tmpshoppingCart.save()
	data = { "code":"001"}
	
	return JsonResponse(data)
@csrf_exempt
def deleteShoppingCart(request):
	json_data = json.loads(request.body) 
	user_id = json_data['user_id']
	product_id = json_data['product_id']
	tmpshoppingCart = ShoppingCart.objects.get(user_id=user_id,product_id=product_id)
	tmpshoppingCart.delete()
	data = { "code":"001"}
	
	return JsonResponse(data)



@csrf_exempt
def findUserName(request):
	json_data = json.loads(request.body) 
	username = json_data['userName']
	if User.objects.filter(userName=username).exists():
		
		context = {"code":"002","message":"Existed UserName"}
	else: 
		context = {"code":"001","message":"NOT Existed UserName"}
	return JsonResponse(context)

@csrf_exempt
def register(request):
	json_data = json.loads(request.body) 
	username = json_data['userName']
	password = json_data['password']
	if User.objects.filter(userName=username,password=password).exists():
		context = {"code":"002","message":"Existed User"}
	else:
		lastUser = User.objects.last()
		idUserCreate = int(lastUser.user_id) + 1
		b = User(user_id=idUserCreate, userName=username, password=password)
		b.save()
		context = {"code":"001","message":"Create OK"}
	return JsonResponse(context)

@csrf_exempt
def login(request):     
	json_data = json.loads(request.body) 
	username = json_data['userName']
	password = json_data['password']
	try :
		user =User.objects.filter(userName=username,password=password)
	except:
		user = False
	if user:
		context = {"code":"001","msg":"login successfully","user":list(user.values())[0]}
	else:        
		context = {"code":"002","message":"Username OR password is incorrect"} 
	return JsonResponse(context)
