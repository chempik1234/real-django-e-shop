from rest_framework import serializers
from .models import *
PRODUCT_FIELDS = ("title", "image", "description", "price")
SEED_FIELDS = ("category", "ripening_period", "ripe_color", "ripe_form", "ripe_weight_grams", "yield_kg_div_m2")


##########
class SeedsCategoriesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SeedsCategories
        fields = ['name']
        lookup_field = 'name'
        model_field = "name"


class RipeningPeriodsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RipeningPeriods
        fields = ['name']
        lookup_field = 'name'


class TomatoTypeOfPlantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TomatoTypeOfPlant
        fields = ['name']
        lookup_field = 'name'


class GroundGrowingConditionsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TomatoTypeOfPlant
        fields = ['name']
        lookup_field = 'name'


non_seed_classes = [SeedsCategoriesSerializer, RipeningPeriodsSerializer, TomatoTypeOfPlantSerializer, GroundGrowingConditionsSerializer]
###############


class TomatoSeedsSerializer(serializers.HyperlinkedModelSerializer):
    category = SeedsCategoriesSerializer()
    ripening_period = RipeningPeriodsSerializer()
    type_of_plant = TomatoTypeOfPlantSerializer()
    ground_growing_conditions = GroundGrowingConditionsSerializer()

    class Meta:
        model = TomatoSeeds
        fields = PRODUCT_FIELDS + SEED_FIELDS + ('type_of_plant', 'ground_growing_conditions')


class CucumberSeedsSerializer(serializers.HyperlinkedModelSerializer):
    category = SeedsCategoriesSerializer()
    ripening_period = RipeningPeriodsSerializer()
    ground_growing_conditions = GroundGrowingConditionsSerializer()

    class Meta:
        model = CucumberSeeds
        fields = PRODUCT_FIELDS + SEED_FIELDS + ('ground_growing_conditions',)