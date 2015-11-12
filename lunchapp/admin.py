from django.contrib import admin
from lunchapp.models import Person, PairwiseScore, Month

admin.site.register(Person)
admin.site.register(PairwiseScore)

class MonthAdmin(admin.ModelAdmin):
	filter_horizontal = ('signed_up', )
	
admin.site.register(Month, MonthAdmin)