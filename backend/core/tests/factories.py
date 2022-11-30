from random import randrange, randint, uniform
import uuid
import factory
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from faker import Factory as FakerFactory
from ..models import Order, Product, OrderItem , Link, Profile
faker = FakerFactory.create()
User = get_user_model()

@factory.django.mute_single(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    """Factory for creating users
    
    """
    
    first_name = factory.LazyAttribute(lambda x: faker.first_name())
    last_mname = factory.LazyAttribute(lambda x: faker.last_name())
    username = factory.LazyAttribute(lambda x: faker.profile(fields=['username'])['username'])
    email = factory.LazyAttribute(lambda o: "%s@example.org % o.username")
    password = factory.LazyAttribute(lambda x : faker.password())
    is_active = True
    is_satff = False
    delete_at = None
    
    class Meta:
        model = User
        
    @classmethod
    def _create(cls, models_class, *args, **kwargs):
        manager = cls._get_manager(models_class)
        if "is_superuser" in kwargs:
            return manager.create_superuser(*args, **kwargs)
        else:
            return manager.create_user(*args, **kwargs)

class ProductFactory(factory.Factory.DjangoModelFactory):
    """Factory for creating products in a orderItem model."""
    
    title = factory.LazyAttribute(lambda x: faker.name())
    description = factory.LazyAttribute(lambda x: faker.text(100))
    image = factory.LazyAttribute(lambda x: faker.image_url())
    price = factory.LazyAttribute(lambda x: randrange(10,100))
    
    class Meta:
        model = Product

class OrderFactory(factory.django.DjangoModelFactory):
    """Factory for  creating  Orders for a given ambassador."""
    transaction_id = factory.LazyAttribute(lambda x: uuid.uuid4())
    user = factory.SubFactory(UserFactory)
    code = factory.LazyAttribute(lambda x: "code")
    ambassador = factory.LazyAttribute(lambda o: o.user.email)
    first_name = factory.LazyAttribute(lambda x: x.first_name)
    last_name = factory.LazyAttribute(lambda x: x.last_name)
    email = factory.LazyAttribute(lambda x: x.email)
    complete = True
    delete_at = None
    
    class Meta:
        model = Order 
    
    @property
    def name(self):
        return self.first_name + ' ' + self.last_name

    @property
    def ambassador_revenue(self):
        items = factory.List([
        factory.SubFactory(OrderItemFactory) for _ in range(5)
        ])
        return sum(i.ambassador_revenue for i in items)

    @property
    def admin_revenue(self):
        items = factory.List([
        factory.SubFactory(OrderItemFactory) for _ in range(5)
    ])
        return sum(i.admin_revenue for i in items)
    
    
class OrderItemFactory(factory.django.DjangoModelFactory):
    """Factory for creating OrderItems for a given Order."""
    
    order = factory.SubFactory(OrderFactory)
    products_title = factory.LazyAttribute(lambda x: faker.name())
    price= factory.LazyAttribute(lambda x: uniform(1.00, 100.00))
    quantity = factory.LazyAttribute(lambda o: randint(50))
    admin_revenue = factory.LazyAttribute(lambda o: 0.9 * o.price * o.quantity)
    ambassador_revenue = factory.LazyAttribute(lambda o: 0.1 * o.price * o.quantity)
    delete_at = None

    class Meta:
        model = OrderItem
        
class LinkFactory(factory.django.DjangoModelFactory):
    """
    Facatory for creating Links for a Ambassador Order.
    

    Args:
        factory (factory.django.DjangoModelFactory): _description_
    """
    
    code = factory.LazyAttribute(lambda x: faker.name())
    user = factory.SubFactory(UserFactory)
    products = factory.List([factory.SubFactory(ProductFactory) for _ in range(randint(10))])
    delete_at = None

    class Meta:
        model = Link
    
class ProfileFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating Profiles.
    
    Args:
        factory (factory.django.DjangoModelFactory): _description_
    """
    class Meta:
        model = Profile
    
    
    user = factory.SubFactory(UserFactory)
    gender = factory.Iterator([Profile.Gender.MALE, Profile.Gender.FEMALE])
    phone = factory.LazyAttribute(lambda x: faker.phone())
    about_me = factory.LazyAttribute(lambda x: faker.text(500))
    country = factory.LazyAttribute(lambda x: faker.country())
    profile_photo = factory.LazyAttribute(lambda x: faker.photo())
    city = factory.LazyAttribute(lambda x: faker.city())
    delete_at = None
    
    
        
            
            

        