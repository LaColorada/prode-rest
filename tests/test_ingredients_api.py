from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientsApiTests(TestCase):
    """
    Test ingredients public API 
    """

    def setUp(self):
        self.client = APIClient()
        
    def test_login_requiered(self):
        """
        Tests that login is requiered to obtain tags
        """

        res = self.client.get(INGREDIENTS_URL)
        
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        

class PrivateIngredientsApiTests(TestCase):
    """
    Test ingredients private API 
    """
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@testarudo.com',
            'pass123456',
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)
    
    def test_retrieve_ingredient_list(self):
        """
        Test tag retrieve
        """
        Ingredient.objects.create(user=self.user, name='kale')
        Ingredient.objects.create(user=self.user, name='salt')
        
        res = self.client.get(INGREDIENTS_URL)
        
        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    
    def test_ingredients_limited_to_user(self):
        """
        Test that retrieved tags belong to users
        """
        user2 = get_user_model().objects.create_user(
            'test@test.com',
            'pass123456',
        )
        Ingredient.objects.create(user=user2, name='Raspberry')
        ingredient = Ingredient.objects.create(user=self.user, name='Comfort Food')
        
        res = self.client.get(INGREDIENTS_URL)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)
    
    def test_create_ingredient_successful(self):
        """
        Test create new tag
        """
        
        payload = {'name': 'Simple'}
        self.client.post(INGREDIENTS_URL, payload)
        
        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)
        
    def test_create_ingredient_invalid(self):
        """
        Test create tag with invalid payload
        """
        payload = {'name': ''}
        res = self.client.post(INGREDIENTS_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        