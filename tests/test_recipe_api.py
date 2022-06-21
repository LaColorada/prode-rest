from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Tag, Ingredient
import recipe

from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

import tempfile
import os

from PIL import Image


RECIPES_URL = reverse('recipe:recipe-list')


def image_upload_url(recipe_id):
    """
    Uploaded image URL
    """
    return reverse('recipe:recipe-upload-image', args=[recipe_id])


def sample_tag(user, name='Main course'):
    """
    Create and return tag
    """
    
    return Tag.objects.create(user=user, name=name)


def sample_ingredient(user, name='Cinnamon'):
    """
    Create and return recipe
    """
    
    return Ingredient.objects.create(user=user, name=name)


def detail_url(recipe_id):
    """
    Returns recipe detail url
    """
    return reverse('recipe:recipe-detail', args=[recipe_id])


def sample_recipe(user, **params):
    """
    Create and return recipe
    """
    defaults = {
        'title': 'Sample recipe',
        'time_minutes': 10,
        'price': 5.00,
    }
    defaults.update(params)
    
    return Recipe.objects.create(user=user, **defaults)


class PublicRecipeApiTests(TestCase):
    """
    Test recipes public API
    """
    
    def setUp(self):
        self.client = APIClient()
        
    def test_required_auth(self):
        """
        Test required authentication
        """
        res = self.client.get(RECIPES_URL)
        
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """
    Test recipes private API
    """
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@testarudo.com',
            'pass123456',
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        
    def test_retrieve_recipes(self):
        """
        Test recipe retrieve
        """
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)
        
        res = self.client.get(RECIPES_URL)
        
        recipes = Recipe.objects.all().order_by('id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """
        Test that retrieved tags belong to users
        """
        user2 = get_user_model().objects.create_user(
            'test@test.com',
            'pass123456',
        )
        sample_recipe(user=user2)
        sample_recipe(user=self.user)
        
        res = self.client.get(RECIPES_URL)
        
        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)
        
    
    def test_view_recipe_detail(self):
        """
        Test view recipe details
        """
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingredients.add(sample_ingredient(user=self.user))
        
        url = detail_url(recipe.id)
        res = self.client.get(url)
        
        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)
        
    def test_create_basic_recipe(self):
        """
        Test create new recipe
        """
        
        payload = {
        'title': 'Test recipe',
        'time_minutes': 30,
        'price': 10.00,
        }
        
        res = self.client.post(RECIPES_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))

    def test_create_recipe_with_tags(self):
        """
        Test create new recipe with tags
        """
        tag1 = sample_tag(user=self.user, name='Tag 1')
        tag2 = sample_tag(user=self.user, name='Tag 2')
        payload = {
        'title': 'Test recipe with two tags',
        'tags': [tag1.id, tag2.id],
        'time_minutes': 30,
        'price': 10.00,
        }
        
        res = self.client.post(RECIPES_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        tags = recipe.tags.all()
        self.assertEqual(tags.count(), 2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)
        
    def test_create_recipe_with_ingredients(self):
        """
        Test create new recipe with ingredients
        """
        ingredient1 = sample_ingredient(user=self.user, name='Ingredient 1')
        ingredient2 = sample_ingredient(user=self.user, name='Ingredient 2')
        payload = {
        'title': 'Test recipe with ingredients',
        'ingredients': [ingredient1.id, ingredient2.id],
        'time_minutes': 45,
        'price': 15.00,
        }
        
        res = self.client.post(RECIPES_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        ingredients = recipe.ingredients.all()
        self.assertEqual(ingredients.count(), 2)
        self.assertIn(ingredient1, ingredients)
        self.assertIn(ingredient2, ingredients)
    

class RecipeImageUploadTest(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user('user', 'testpass')
        self.client.force_authenticate(self.user)
        self.recipe = sample_recipe(user=self.user)
        
    def tearDown(self):
        self.recipe.image.delete()
        
    def test_upload_image_to_recipe(self):
        """
        Test upload image to recipe
        """
        url = image_upload_url(self.recipe.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB', (10,10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            res = self.client.post(url, {'image': ntf}, format='multipart')

        self.recipe.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.recipe.image.path))
        
    def test_upload_image_bad_request(self):
        """
        Test fail upload image
        """
        url = image_upload_url(self.recipe.id)
        res = self.client.post(url, {'image': 'notimage'}, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_filter_recipes_by_tags(self):
        """
        Test filter recipes by tags
        """
        recipe1 = sample_recipe(user=self.user, title='Thai vegetable curry')
        recipe2 = sample_recipe(user=self.user, title='Aubergine with tahini')
        tag1 = sample_tag(user=self.user, name='Vegan')
        tag2 = sample_tag(user=self.user, name='Vegetarian')
        recipe1.tags.add(tag1)
        recipe2.tags.add(tag2)
        recipe3 = sample_recipe(user=self.user, title='Fish and chips')
        
        res = self.client.get(
            RECIPES_URL,
            {'tags': '{},{}'.format(tag1.id, tag2.id)}
        )
        
        serializer1 = RecipeSerializer(recipe1)
        serializer2 = RecipeSerializer(recipe2)
        serializer3 = RecipeSerializer(recipe3)
        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)
    
    def test_filter_recipes_by_ingredients(self):
        """
        Test filter recipes by tags
        """
        recipe1 = sample_recipe(user=self.user, title='Thai vegetable curry')
        recipe2 = sample_recipe(user=self.user, title='Aubergine with tahini')
        ingredient1 = sample_ingredient(user=self.user, name='Vegan')
        ingredient2 = sample_ingredient(user=self.user, name='Vegetarian')
        recipe1.ingredients.add(ingredient1)
        recipe2.ingredients.add(ingredient2)
        recipe3 = sample_recipe(user=self.user, title='Fish and chips')
        
        res = self.client.get(
            RECIPES_URL,
            {'ingredients': '{},{}'.format(ingredient1.id, ingredient2.id)}
        )
        
        serializer1 = RecipeSerializer(recipe1)
        serializer2 = RecipeSerializer(recipe2)
        serializer3 = RecipeSerializer(recipe3)
        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)