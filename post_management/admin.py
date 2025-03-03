from django.contrib import admin
from post_management.models import category, sub_category, NewsPost, VideoNews, CMS, slider
from django.contrib.auth.models import User

class Post_cat(admin.ModelAdmin):
    list_display=('cat_name','cat_slug','cat_status','order')
    list_editable=('cat_status','order',)
admin.site.register(category,Post_cat)

class Post_subcat(admin.ModelAdmin):
    list_display=('subcat_name','subcat_slug','subcat_status','order','subcat_tag')
    list_editable=('subcat_status','order',)
admin.site.register(sub_category,Post_subcat)

class Post_Admin(admin.ModelAdmin):
    search_fields=('post_title','slug','post_tag','post_date')
    list_filter=('post_date','order','Head_Lines',
    'articles',
    'trending',
    'BreakingNews',
    'Event')
    list_display=(
        'post_title',
        'post_date',
        'slug',
        'post_status',
        'viewcounter',
        'order',
        'is_active',
        'status',
        'post_cat',
        'post_image',
        'Head_Lines',
        'articles',
        'trending',
        'BreakingNews',
        'Event',
        'Event_date',
        'Eventend_date',
        'schedule_date',
        'post_date',
        'updated_at',
        #'user',
        )
    list_editable=('status','is_active','order')
    cropping_fields = {'image_crop': ('post_image',)}
    #crop_fields = ['post_image'] #tapple

admin.site.register(NewsPost,Post_Admin)

class VideoPost(admin.ModelAdmin):
    search_fields=('video_title','slug')
    list_filter=('video_date','order')
    readonly_fields = ('viewcounter',)
    list_display=(
        'News_Category',
        'video_title',
        'slug',
        'video_url',
        'viewcounter',
        'counter',
        'video_tag',
        'video_date',
        'order',
        'is_active',
        'Head_Lines',
        'articles',
        'trending',
        'BreakingNews',
        'schedule_date',
        )
    list_editable=('is_active','order',)

admin.site.register(VideoNews,VideoPost)

class cmsadmin(admin.ModelAdmin):
    search_fields=('pagename','slug')
    list_filter=('post_date','order')
    readonly_fields = ('viewcounter',)
    
    list_display=(
        'pagename',
        'Content',
        'pageimage',
        'slug',
        'post_date',
        'updated_at',
        'viewcounter',
        'post_status',
        'order'
        )
    list_editable=('post_status','order',)
    cropping_fields = {'image_crop': ('pageimage',)}
admin.site.register(CMS,cmsadmin)

class slideradmin(admin.ModelAdmin):
    search_fields=('title','slug')
    list_filter=('post_date','order')
    
    list_display=(
    'slidercat',
    'title',
    'des',
    'sliderimage',
    'slug',
    'post_date',
    'updated_at',
    'order',
    'status',
        )
    list_editable=('status','order',)
    cropping_fields = {'image_crop': ('sliderimage',)}
admin.site.register(slider,slideradmin)