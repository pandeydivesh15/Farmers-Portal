# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Crop, Nutrient, Disease, Fertilizer, SoilNutrient, FertiProvide, CropNutrient, CropFarmer

admin.site.register(Crop)
admin.site.register(Nutrient)
admin.site.register(Disease)
admin.site.register(Fertilizer)
admin.site.register(SoilNutrient)
admin.site.register(FertiProvide)
admin.site.register(CropNutrient)
admin.site.register(CropFarmer)