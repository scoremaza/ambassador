import pytest
from pytest_factoryboy import register
from core.tests.factories import (UserFactory,
                                  ProductFactory,
                                  OrderFactory,
                                  OrderItemFactory,
                                  LinkFactory,
                                  ProfileFactory,
                                  )

register(UserFactory)
register(ProductFactory)
register(OrderFactory)
register(OrderItemFactory)
register(LinkFactory)
register(ProfileFactory)


@pytest.fixture
def base_user(db, user_factory):
    new_user = user_factory.create()
    return new_user

@pytest.fixture
def super_user(db, user_factory):
    new_user = user_factory.create(is_staff=True, is_superuser=True)
    return new_user

@pytest.fixture
def profile(db, profile_factory):
    user_profile = profile_factory.create()
    return user_profile

@pytest.fixture
def product(db, product_factory):
    user_product = product_factory.create()
    return user_product

@pytest.fixture
def order(db, order_factory):
    user_product = order_factory.create()
    return user_product

@pytest.fixture
def orderItem(db, orderItem_factory):
    user_orderItem = orderItem_factory.create()
    return user_orderItem

@pytest.fixture
def link(db, link_factory):
    ambassador_link = link_factory.create()
    return ambassador_link



