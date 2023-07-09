from django.db import models
from register.models import User

Catagory = (
    ("Air Max", "Air Max"),
    ("Air Force", "Air Force"),
    ("Air Vapormax", "Air Vapormax"),
    ("Air Jordan", "Air Jordan"),
    ("Kyrie", "Kyrie"),
    ("Lebron", "Lebron"),
)


Season = (
    ("Summer", "Summer"),
    ("Spring", "Spring"),
    ("Autumn", "Autumn"),

)

Color = (

    ("White", "White"),
("Yellow", "Yellow"),
("Red", "Red"),
("Green", "Green"),
("Violet", "Violet"),
("Dark", "Dark"),
("Blue", "Blue"),
("Brown", "Brown"),
("Pink", "Pink"),

)




class Shoes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True)
    name = models.CharField(max_length=200)

    categaory = models.CharField(max_length=200, choices=Catagory, default='Catagory')
    season = models.CharField(max_length=200, choices=Season, default='season')
    color = models.CharField(max_length=200, choices=Color, default='color')
    size = models.IntegerField()

    description = models.CharField(max_length=200)
    price = models.FloatField(null=True,blank=True)
    main_image_url = models.URLField(max_length=2000)

    front_image = models.CharField(max_length=2000)
    back_image = models.CharField(max_length=2000)
    side_image = models.CharField(max_length=2000)

    shoe_available = models.BooleanField()
    is_delete = models.BooleanField()

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Shoes, on_delete=models.CASCADE)
    image_url = models.CharField(max_length = 2083, default=False)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.product



