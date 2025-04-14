import pytest
from main import Product, Category


@pytest.fixture
def product():
    return Product("Тестовый товар", "Описание", 100.0, 10)


@pytest.fixture
def category(product):
    return Category("Тестовая категория", "Описание", [product])


def test_product_initialization(product):
    assert product.name == "Тестовый товар"
    assert product.description == "Описание"
    assert product.price == 100.0
    assert product.quantity == 10


def test_category_initialization(category):
    assert category.name == "Тестовая категория"
    assert category.description == "Описание"
    assert len(category.products) == 1


def test_product_count():
    Category.category_count = 0
    Category.product_count = 0
    product1 = Product("Товар 1", "Описание 1", 100.0, 10)
    product2 = Product("Товар 2", "Описание 2", 200.0, 20)
    category = Category("Категория", "Описание", [product1, product2])
    assert Category.product_count == 2
    assert category.name == "Категория"


def test_category_count():
    Category.category_count = 0
    Category.product_count = 0
    product = Product("Товар", "Описание", 100.0, 10)
    category1 = Category("Категория 1", "Описание 1", [product])
    category2 = Category("Категория 2", "Описание 2", [product])
    assert Category.category_count == 2
    assert category1.name == "Категория 1"
    assert category2.name == "Категория 2"
