from django.core.management.base import BaseCommand
from pos.models import MenuCategory, MenuItem, User


class Command(BaseCommand):
    help = 'Populate database with Indian five-star restaurant menu and sample users'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating menu categories and items...')

        # Create categories
        categories_data = [
            {'name': 'Appetizers', 'description': 'Traditional Indian starters', 'order': 1},
            {'name': 'Tandoori Specialties', 'description': 'Clay oven delicacies', 'order': 2},
            {'name': 'Curries & Gravies', 'description': 'Rich and aromatic curries', 'order': 3},
            {'name': 'Biryanis & Rice', 'description': 'Fragrant rice dishes', 'order': 4},
            {'name': 'Breads', 'description': 'Freshly baked Indian breads', 'order': 5},
            {'name': 'Desserts', 'description': 'Traditional Indian sweets', 'order': 6},
            {'name': 'Beverages', 'description': 'Refreshing drinks', 'order': 7},
        ]

        for cat_data in categories_data:
            category, created = MenuCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'order': cat_data['order']
                }
            )
            if created:
                self.stdout.write(f'  Created category: {category.name}')

        # Menu items
        menu_items = [
            # Appetizers
            {
                'category': 'Appetizers',
                'name': 'Paneer Tikka',
                'description': 'Cottage cheese marinated in aromatic spices and grilled to perfection',
                'price': 450,
                'is_vegetarian': True,
                'spice_level': 'medium',
            },
            {
                'category': 'Appetizers',
                'name': 'Tandoori Chicken Wings',
                'description': 'Succulent chicken wings marinated in yogurt and spices',
                'price': 550,
                'is_vegetarian': False,
                'spice_level': 'medium',
            },
            {
                'category': 'Appetizers',
                'name': 'Vegetable Samosa',
                'description': 'Crispy pastry filled with spiced potatoes and peas',
                'price': 350,
                'is_vegetarian': True,
                'is_vegan': True,
                'spice_level': 'mild',
            },
            {
                'category': 'Appetizers',
                'name': 'Gilafi Seekh Kebab',
                'description': 'Minced lamb kebabs wrapped with bell peppers and onions',
                'price': 650,
                'is_vegetarian': False,
                'spice_level': 'hot',
            },
            {
                'category': 'Appetizers',
                'name': 'Crispy Spinach',
                'description': 'Deep-fried crispy spinach with sweet yogurt and tamarind chutney',
                'price': 400,
                'is_vegetarian': True,
                'spice_level': 'mild',
            },
            {
                'category': 'Appetizers',
                'name': 'Amritsari Fish',
                'description': 'Batter-fried fish marinated with carom seeds and spices',
                'price': 750,
                'is_vegetarian': False,
                'spice_level': 'medium',
            },

            # Tandoori Specialties
            {
                'category': 'Tandoori Specialties',
                'name': 'Tandoori Chicken (Half)',
                'description': 'Classic chicken marinated in yogurt and traditional spices',
                'price': 850,
                'is_vegetarian': False,
                'spice_level': 'medium',
            },
            {
                'category': 'Tandoori Specialties',
                'name': 'Tandoori Prawns',
                'description': 'Jumbo prawns marinated in saffron and aromatic spices',
                'price': 1450,
                'is_vegetarian': False,
                'spice_level': 'hot',
            },
            {
                'category': 'Tandoori Specialties',
                'name': 'Malai Chicken Tikka',
                'description': 'Tender chicken pieces marinated in cream, cheese, and mild spices',
                'price': 950,
                'is_vegetarian': False,
                'spice_level': 'mild',
            },
            {
                'category': 'Tandoori Specialties',
                'name': 'Tandoori Mushroom',
                'description': 'Button mushrooms marinated in hung curd and spices',
                'price': 550,
                'is_vegetarian': True,
                'spice_level': 'medium',
            },
            {
                'category': 'Tandoori Specialties',
                'name': 'Lamb Chops',
                'description': 'Succulent lamb chops marinated in royal spices',
                'price': 1650,
                'is_vegetarian': False,
                'spice_level': 'medium',
            },

            # Curries & Gravies
            {
                'category': 'Curries & Gravies',
                'name': 'Butter Chicken',
                'description': 'Tandoori chicken in rich tomato cream sauce',
                'price': 950,
                'is_vegetarian': False,
                'spice_level': 'mild',
            },
            {
                'category': 'Curries & Gravies',
                'name': 'Dal Makhani',
                'description': 'Black lentils simmered overnight with butter and cream',
                'price': 550,
                'is_vegetarian': True,
                'spice_level': 'mild',
            },
            {
                'category': 'Curries & Gravies',
                'name': 'Paneer Lababdar',
                'description': 'Cottage cheese in creamy tomato onion gravy',
                'price': 650,
                'is_vegetarian': True,
                'spice_level': 'medium',
            },
            {
                'category': 'Curries & Gravies',
                'name': 'Rogan Josh',
                'description': 'Kashmiri lamb curry with aromatic spices',
                'price': 1250,
                'is_vegetarian': False,
                'spice_level': 'hot',
            },
            {
                'category': 'Curries & Gravies',
                'name': 'Palak Paneer',
                'description': 'Cottage cheese in spinach gravy with spices',
                'price': 600,
                'is_vegetarian': True,
                'spice_level': 'mild',
            },
            {
                'category': 'Curries & Gravies',
                'name': 'Goan Fish Curry',
                'description': 'Fish cooked in coconut-based curry with Goan spices',
                'price': 1150,
                'is_vegetarian': False,
                'spice_level': 'hot',
            },
            {
                'category': 'Curries & Gravies',
                'name': 'Kadai Paneer',
                'description': 'Cottage cheese with bell peppers in spiced tomato gravy',
                'price': 650,
                'is_vegetarian': True,
                'spice_level': 'medium',
            },
            {
                'category': 'Curries & Gravies',
                'name': 'Chicken Chettinad',
                'description': 'South Indian chicken curry with coconut and curry leaves',
                'price': 950,
                'is_vegetarian': False,
                'spice_level': 'very_hot',
            },

            # Biryanis & Rice
            {
                'category': 'Biryanis & Rice',
                'name': 'Hyderabadi Chicken Biryani',
                'description': 'Fragrant basmati rice layered with marinated chicken',
                'price': 850,
                'is_vegetarian': False,
                'spice_level': 'medium',
            },
            {
                'category': 'Biryanis & Rice',
                'name': 'Lucknowi Lamb Biryani',
                'description': 'Aromatic rice with tender lamb in dum style',
                'price': 1350,
                'is_vegetarian': False,
                'spice_level': 'medium',
            },
            {
                'category': 'Biryanis & Rice',
                'name': 'Vegetable Biryani',
                'description': 'Mixed vegetables and basmati rice with aromatic spices',
                'price': 650,
                'is_vegetarian': True,
                'is_vegan': True,
                'spice_level': 'mild',
            },
            {
                'category': 'Biryanis & Rice',
                'name': 'Prawn Biryani',
                'description': 'Coastal style biryani with succulent prawns',
                'price': 1450,
                'is_vegetarian': False,
                'spice_level': 'hot',
            },
            {
                'category': 'Biryanis & Rice',
                'name': 'Jeera Rice',
                'description': 'Basmati rice tempered with cumin',
                'price': 350,
                'is_vegetarian': True,
                'is_vegan': True,
                'spice_level': 'mild',
            },
            {
                'category': 'Biryanis & Rice',
                'name': 'Saffron Pulao',
                'description': 'Aromatic rice with saffron, dry fruits, and nuts',
                'price': 550,
                'is_vegetarian': True,
                'spice_level': 'mild',
            },

            # Breads
            {
                'category': 'Breads',
                'name': 'Butter Naan',
                'description': 'Soft leavened bread brushed with butter',
                'price': 150,
                'is_vegetarian': True,
                'spice_level': '',
            },
            {
                'category': 'Breads',
                'name': 'Garlic Naan',
                'description': 'Naan topped with fresh garlic and cilantro',
                'price': 180,
                'is_vegetarian': True,
                'spice_level': '',
            },
            {
                'category': 'Breads',
                'name': 'Cheese Naan',
                'description': 'Naan stuffed with mozzarella and cheddar cheese',
                'price': 220,
                'is_vegetarian': True,
                'spice_level': '',
            },
            {
                'category': 'Breads',
                'name': 'Tandoori Roti',
                'description': 'Whole wheat bread baked in tandoor',
                'price': 120,
                'is_vegetarian': True,
                'is_vegan': True,
                'spice_level': '',
            },
            {
                'category': 'Breads',
                'name': 'Laccha Paratha',
                'description': 'Multi-layered whole wheat bread',
                'price': 180,
                'is_vegetarian': True,
                'spice_level': '',
            },
            {
                'category': 'Breads',
                'name': 'Kashmiri Naan',
                'description': 'Sweet naan stuffed with dry fruits and nuts',
                'price': 250,
                'is_vegetarian': True,
                'spice_level': '',
            },

            # Desserts
            {
                'category': 'Desserts',
                'name': 'Gulab Jamun',
                'description': 'Soft milk dumplings soaked in cardamom-flavored syrup',
                'price': 350,
                'is_vegetarian': True,
                'spice_level': '',
            },
            {
                'category': 'Desserts',
                'name': 'Rasmalai',
                'description': 'Cottage cheese dumplings in saffron-flavored milk',
                'price': 400,
                'is_vegetarian': True,
                'spice_level': '',
            },
            {
                'category': 'Desserts',
                'name': 'Kulfi Falooda',
                'description': 'Traditional Indian ice cream with vermicelli and rose syrup',
                'price': 350,
                'is_vegetarian': True,
                'spice_level': '',
            },
            {
                'category': 'Desserts',
                'name': 'Gajar Halwa',
                'description': 'Carrot pudding with khoya, nuts, and cardamom',
                'price': 400,
                'is_vegetarian': True,
                'spice_level': '',
            },
            {
                'category': 'Desserts',
                'name': 'Moong Dal Halwa',
                'description': 'Rich lentil-based dessert with ghee and dry fruits',
                'price': 450,
                'is_vegetarian': True,
                'spice_level': '',
            },

            # Beverages
            {
                'category': 'Beverages',
                'name': 'Masala Chai',
                'description': 'Traditional Indian spiced tea',
                'price': 150,
                'is_vegetarian': True,
                'spice_level': '',
            },
            {
                'category': 'Beverages',
                'name': 'Sweet Lassi',
                'description': 'Traditional yogurt-based drink',
                'price': 200,
                'is_vegetarian': True,
                'spice_level': '',
            },
            {
                'category': 'Beverages',
                'name': 'Mango Lassi',
                'description': 'Yogurt drink blended with fresh mango pulp',
                'price': 250,
                'is_vegetarian': True,
                'spice_level': '',
            },
            {
                'category': 'Beverages',
                'name': 'Fresh Lime Soda',
                'description': 'Freshly squeezed lime with soda water',
                'price': 180,
                'is_vegetarian': True,
                'is_vegan': True,
                'spice_level': '',
            },
            {
                'category': 'Beverages',
                'name': 'Jal Jeera',
                'description': 'Cumin-flavored refreshing drink',
                'price': 150,
                'is_vegetarian': True,
                'is_vegan': True,
                'spice_level': '',
            },
            {
                'category': 'Beverages',
                'name': 'Thandai',
                'description': 'Milk-based drink with almonds, saffron, and spices',
                'price': 250,
                'is_vegetarian': True,
                'spice_level': '',
            },
        ]

        for item_data in menu_items:
            category = MenuCategory.objects.get(name=item_data.pop('category'))
            item, created = MenuItem.objects.get_or_create(
                category=category,
                name=item_data['name'],
                defaults=item_data
            )
            if created:
                self.stdout.write(f'  Created item: {item.name}')

        # Create sample users
        users_data = [
            {'username': 'admin', 'password': 'admin123', 'role': 'waiter', 'is_superuser': True, 'is_staff': True},
            {'username': 'waiter1', 'password': 'waiter123', 'role': 'waiter', 'email': 'waiter1@hotel.com'},
            {'username': 'waiter2', 'password': 'waiter123', 'role': 'waiter', 'email': 'waiter2@hotel.com'},
            {'username': 'reception1', 'password': 'reception123', 'role': 'reception', 'email': 'reception@hotel.com'},
            {'username': 'chef1', 'password': 'chef123', 'role': 'chef', 'email': 'chef@hotel.com'},
        ]

        for user_data in users_data:
            password = user_data.pop('password')
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults=user_data
            )
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f'  Created user: {user.username} (password: {password})'))

        self.stdout.write(self.style.SUCCESS('\nDatabase populated successfully!'))
        self.stdout.write(self.style.SUCCESS('\nSample Login Credentials:'))
        self.stdout.write('  Admin: admin / admin123')
        self.stdout.write('  Waiter: waiter1 / waiter123')
        self.stdout.write('  Reception: reception1 / reception123')
        self.stdout.write('  Chef: chef1 / chef123')
