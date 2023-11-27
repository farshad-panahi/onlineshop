from django.db import models


class Category(models.Model):

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255,blank=True)
    top_product = models.ForeignKey('Product', on_delete=models.SET_NULL,null=True, related_name='+')



class Discount(models.Model):

    discount = models.FloatField()
    description = models.CharField(max_length=255)


class Product(models.Model):

    discount = models.ManyToManyField(Discount,blank=True,related_name='products')
    Category = models.ForeignKey(Category,on_delete=models.PROTECT,related_name='products')
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    price = models.DecimalField(max_digits=6,decimal_places=2) 
    inventory = models.IntegerField(default=0,) 
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)


class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)


class Order(models.Model):
    
    ORDER_STATUS_PAID = 'p'
    ORDER_STATUS_UNPAID = 'u'
    ORDER_STATUS_CANCELED = 'c'

    ORDER_STATUS =(
        (ORDER_STATUS_PAID,'Paid'),
        (ORDER_STATUS_UNPAID,'Unpaid'),
        (ORDER_STATUS_CANCELED,'Canceled'),
    )
    customer = models.ForeignKey(Customer,on_delete=models.PROTECT,related_name='orders')
    datetime_crated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1,choices=ORDER_STATUS,default=ORDER_STATUS_UNPAID)


class Comment(models.Model):

    COMMENT_STATUS_WAITING = 'w'
    COMMENT_STATUS_APROVED = 'a'
    COMMENT_STATUS_NOT_APPROVED = 'na'
    
    COMMENT_STATUS = (
        ( COMMENT_STATUS_WAITING , 'Waiting'),
        ( COMMENT_STATUS_APROVED , 'Approved'),
        ( COMMENT_STATUS_NOT_APPROVED , 'Not Approved'),
    )

    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2,choices=COMMENT_STATUS,default=COMMENT_STATUS_WAITING)


class Address(models.Model):

    customer = models.OneToOneField(
        Customer,
        on_delete=models.CASCADE,
        primary_key=True
    ) 
    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)


class OrderItem(models.Model):

    order = models.ForeignKey(Order,on_delete=models.PROTECT,related_name='items')
    product = models.ForeignKey(Product,on_delete=models.PROTECT,related_name='oreder_items')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6,decimal_places=2)

    class Meta:
        unique_together = [[
            'order',
            'product'
        ]]


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='cart_items')
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together =[[
            'cart',
            'product',
        ]]