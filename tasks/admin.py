from django.contrib import admin
from tasks.models import Task

class TaskAdmin(admin.ModelAdmin):
	fieldsets = [	(None, {'fields' : ['title', 'author', 'category']}),
					('Date Information', {'fields' : ['publication_date', 'deadline_date']}),
					('Content', {'fields' : ['description', 'slug']})]
	list_display = ('title', 'publication_date', 'deadline_date', 'author')
	list_filter = ['category', 'publication_date', 'deadline_date']
	search_fields = ['title', 'description']
	prepopulated_fields = {'slug' : ('title',)}

admin.site.register(Task, TaskAdmin)