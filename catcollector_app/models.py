from django.db import models
from django.urls import reverse

# choices for cat's feeding schedule
MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)

class Toy(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('toys_detail', kwargs={'pk': self.id})


# Create your models here.
class Cat(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'cat_id': self.id})
    

class Feeding(models.Model):
    date = models.DateField('feeding Date')
    meal = models.CharField(
        max_length=1,
        choices=MEALS,
        default=MEALS[0][0]
    )
    # on delete they will remove all Feeding instances related to the deleted cat
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

    def __str__(self):
        # get_Field_display() returns a human readable value for the field
        return f"{self.get_meal_display()} on {self.date}"
    
class Meta:
    ordering = ['-date']
