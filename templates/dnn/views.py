import logging
logger = logging.getLogger(__name__)
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render
from post_management.models import category,sub_category,NewsPost,VideoNews
from Ad_management.models import ad_category
from Ad_management.models import ad
from Seo_management.models import seo_optimization
from service.models import jobApplication,CareerApplication,SubscribeUser,BrandPartner,RegForm

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
#from store.models import Product
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, Http404
from datetime import date, datetime
import re


# home-pahe---------
def home(request):
    seo=seo_optimization.objects.get(pageslug='https://www.dxbnewsnetwork.com/')
    current_datetime = datetime.now()
    blogdata=NewsPost.objects.filter(schedule_date__lt=current_datetime,is_active=1,status='active').order_by('-id') [:10]
    mainnews=NewsPost.objects.filter(schedule_date__lt=current_datetime,status='active').order_by('order')[:4]
    events=NewsPost.objects.filter(schedule_date__lt=current_datetime,Event=1,status='active').order_by('-id') [:10]
    bp=BrandPartner.objects.filter(is_active=1).order_by('-id') [:20]
    articales=NewsPost.objects.filter(schedule_date__lt=current_datetime,articles=1,status='active').order_by('-id') [:3]
    headline=NewsPost.objects.filter(schedule_date__lt=current_datetime,Head_Lines=1,status='active').order_by('-id') [:4]
    trending=NewsPost.objects.filter(schedule_date__lt=current_datetime,trending=1,status='active').order_by('-id') [:2]
    brknews=NewsPost.objects.filter(BreakingNews=1,status='active').order_by('-id') [:4]
    Category=category.objects.filter(cat_status='active').order_by('order') [:11]
    
    truet=VideoNews.objects.filter(is_active='active',video_type='reel',News_Category=75).order_by('-id')[:8]
    recipe=VideoNews.objects.filter(is_active='active',video_type='reel',News_Category=76).order_by('-id')[:8]
# --------------video-post-manage--------------
    podcast=VideoNews.objects.filter(is_active='active',video_type='video',Head_Lines=1).order_by('order')[:2]
    mainvid=VideoNews.objects.filter(is_active='active',video_type='video',order__range=[3, 6]).order_by('order')[:4]
    catvid=VideoNews.objects.filter(is_active='active',video_type='video',order__gte=3).order_by('-id')[:8]
    reel=VideoNews.objects.filter(is_active='active',video_type='reel').order_by('-id')[:16]
    vidarticales=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('order')[:3]
# --------------ad-manage-meny--------------
    lfsid=ad_category.objects.get(ads_cat_slug='left-fest-square')
    leftsquqre=ad.objects.filter(ads_cat_id=lfsid.id, is_active=1).order_by('-id') [:4]
    
    adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')
    adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]
    
    adtrid=ad_category.objects.get(ads_cat_slug='topright-600x80')
    adtopright=ad.objects.filter(ads_cat_id=adtrid.id, is_active=1).order_by('-id') [:1]
    
    adtopid=ad_category.objects.get(ads_cat_slug='leaderboard')
    adtop=ad.objects.filter(ads_cat_id=adtopid.id, is_active=1).order_by('-id') [:1]
    
    adleftid=ad_category.objects.get(ads_cat_slug='skyscraper')
    adleft=ad.objects.filter(ads_cat_id=adleftid.id, is_active=1).order_by('-id') [:1]
    
    adrcol=ad_category.objects.get(ads_cat_slug='mrec')
    adright=ad.objects.filter(ads_cat_id=adrcol.id, is_active=1).order_by('-id') [:1]
    
    festbg=ad_category.objects.get(ads_cat_slug='festivebg')
    festive=ad.objects.filter(ads_cat_id=festbg.id, is_active=1).order_by('-id') [:1]
    # header--to--ad---
    topad=ad_category.objects.get(ads_cat_slug='topad')
    tophead=ad.objects.filter(ads_cat_id=topad.id, is_active=1).order_by('-id') [:1]
    
    popup=ad_category.objects.get(ads_cat_slug='popup')
    popupad=ad.objects.filter(ads_cat_id=popup.id, is_active=1).order_by('-id') [:1]
# -------------end-ad-manage-meny--------------    
    # slider=NewsPost.objects.filter(id=1).order_by('id')[:5] use for filter value
    
    slider=NewsPost.objects.filter().order_by('-id')[:5]
    latestnews=NewsPost.objects.all().order_by('-id')[:5]
    data={
            'indseo':seo,
            'BlogData':blogdata,
            'mainnews':mainnews,
            'event':events,
            'bplogo':bp,
            'Slider':slider,
            'Blogcat':Category,
            'latnews':latestnews,
            'adtop':adtop,
            'adleft':adleft,
            'adright':adright,
            'adtl':adtopleft,
            'adtr':adtopright,
            'bgad':festive,
            'headtopad':tophead,
            'popup':popupad,
            'lfs':leftsquqre,
            'Articale':articales,
            'vidart':vidarticales,
            'headline':headline,
            'trendpost':trending,
            'bnews':brknews,
            'vidnews':podcast,
            'MainV':mainvid,
            'CatV':catvid,
            'Reels':reel,
            'recipe':recipe,
            'tt':truet,
        }
   
    return render(request,'index.html',data)
# News-details-page----------

def newsdetails(request,slug):
    counter=NewsPost.objects.get(slug=slug)
    counter.viewcounter=counter.viewcounter + 1
    counter.save()
    seo='ndetail'
    blogdetails=NewsPost.objects.get(slug=slug)
    blogdata=NewsPost.objects.filter(is_active=1,status='active').order_by('-id') [:20]
    mainnews=NewsPost.objects.filter(is_active=1,status='active').order_by('-id') [:2]
    articales=NewsPost.objects.filter(articles=1,status='active').order_by('-id') [:3]
    headline=NewsPost.objects.filter(Head_Lines=1,status='active').order_by('-id') [:14]
    trending=NewsPost.objects.filter(trending=1,status='active').order_by('-id') [:7]
    brknews=NewsPost.objects.filter(BreakingNews=1,status='active').order_by('-id') [:8]
    podcast=VideoNews.objects.filter(is_active='active').order_by('-id') [:1]
    vidarticales=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('order')[:2]
    # --------------ad-manage-meny--------------
    lfsid=ad_category.objects.get(ads_cat_slug='left-fest-square')
    leftsquqre=ad.objects.filter(ads_cat_id=lfsid.id, is_active=1).order_by('-id') [:4]
    
    adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')
    adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]
    
    adtrid=ad_category.objects.get(ads_cat_slug='topright-600x80')
    adtopright=ad.objects.filter(ads_cat_id=adtrid.id, is_active=1).order_by('-id') [:1]
    
    adtopid=ad_category.objects.get(ads_cat_slug='leaderboard')
    adtop=ad.objects.filter(ads_cat_id=adtopid.id, is_active=1).order_by('-id') [:1]
    
    adleftid=ad_category.objects.get(ads_cat_slug='skyscraper')
    adleft=ad.objects.filter(ads_cat_id=adleftid.id, is_active=1).order_by('-id') [:1]
    
    adrcol=ad_category.objects.get(ads_cat_slug='mrec')
    adright=ad.objects.filter(ads_cat_id=adrcol.id, is_active=1).order_by('-id') [:1]
    
    festbg=ad_category.objects.get(ads_cat_slug='festivebg')
    festive=ad.objects.filter(ads_cat_id=festbg.id, is_active=1).order_by('-id') [:1]
    # festivetop
    # festiveleft
    # festiveright
# -------------end-ad-manage-meny--------------    
    # slider=NewsPost.objects.filter(id=1).order_by('id')[:5] use for filter value
    Category=category.objects.filter(cat_status='active').order_by('order') [:11]
    slider=NewsPost.objects.filter().order_by('-id')[:5]
    latestnews=NewsPost.objects.all().order_by('-id')[:5]
    data={
            'indseo':seo,
            'Blogdetails':blogdetails,
            'BlogData':blogdata,
            'mainnews':mainnews,
            'Slider':slider,
            'Blogcat':Category,
            'latnews':latestnews,
            'adtop':adtop,
            'adleft':adleft,
            'adright':adright,
            'adtl':adtopleft,
            'adtr':adtopright,
            'bgad':festive,
            'lfs':leftsquqre,
            'Articale':articales,
            'vidart':vidarticales,
            'headline':headline,
            'trendpost':trending,
            'bnews':brknews,
            'vidnews':podcast,
        }
    return render(request,'news-details.html',data)
    #return render(request, 'index.html')
# News-details-page--end--------
# News-pdf--------
def GetNewsPdf(request):
    current_datetime = datetime.now()
    blogdata=NewsPost.objects.filter(schedule_date__lt=current_datetime,is_active=1,status='active').order_by('-id') [:10]
    mainnews=NewsPost.objects.filter(schedule_date__lt=current_datetime,status='active').order_by('order')[:4]
    articales=NewsPost.objects.filter(schedule_date__lt=current_datetime,articles=1,status='active').order_by('-id') [:3]
    headline=NewsPost.objects.filter(schedule_date__lt=current_datetime,Head_Lines=1,status='active').order_by('-id') [:4]
    vidarticales=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('order')[:3]
    data={
            # 'indseo':seo,
            'BlogData':blogdata,
            'mainnews':mainnews,
            'Articale':articales,
            'vidart':vidarticales,
            'headline':headline,
            
        }
    return render(request,'epaper.html',data)

# News-pdf--------
# News-News-search--------
def find_post_by_title(request):
    seo='allnews'
    current_datetime = datetime.now()
    events=NewsPost.objects.filter(Event=1,status='active').order_by('-id') [:10]
    bp=BrandPartner.objects.filter(is_active=1).order_by('-id') [:20]
    articales=NewsPost.objects.filter(schedule_date__lt=current_datetime,articles=1,status='active').order_by('-id') [:3]
    vidarticales=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('order')[:2]
    headline=NewsPost.objects.filter(schedule_date__lt=current_datetime,Head_Lines=1,status='active').order_by('-id') [:14]
    trending=NewsPost.objects.filter(schedule_date__lt=current_datetime,trending=1,status='active').order_by('-id') [:7]
    brknews=NewsPost.objects.filter(BreakingNews=1,status='active').order_by('-id') [:8]
    podcast=VideoNews.objects.filter(is_active='active').order_by('-id') [:2]
    Category=category.objects.filter(cat_status='active').order_by('order') [:11]
    
    # --------------ad-manage-meny--------------
    adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')
    adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]
    
    adtrid=ad_category.objects.get(ads_cat_slug='topright-600x80')
    adtopright=ad.objects.filter(ads_cat_id=adtrid.id, is_active=1).order_by('-id') [:1]
    
    adtopid=ad_category.objects.get(ads_cat_slug='leaderboard')
    adtop=ad.objects.filter(ads_cat_id=adtopid.id, is_active=1).order_by('-id') [:1]
    
    adleftid=ad_category.objects.get(ads_cat_slug='skyscraper')
    adleft=ad.objects.filter(ads_cat_id=adleftid.id, is_active=1).order_by('-id') [:1]
    
    adrcol=ad_category.objects.get(ads_cat_slug='mrec')
    adright=ad.objects.filter(ads_cat_id=adrcol.id, is_active=1).order_by('-id') [:1]
    
    festbg=ad_category.objects.get(ads_cat_slug='festivebg')
    festive=ad.objects.filter(ads_cat_id=festbg.id, is_active=1).order_by('-id') [:1]
    
    topad=ad_category.objects.get(ads_cat_slug='topad')
    tophead=ad.objects.filter(ads_cat_id=topad.id, is_active=1).order_by('-id') [:1]
    popup=ad_category.objects.get(ads_cat_slug='popup')
    popupad=ad.objects.filter(ads_cat_id=popup.id, is_active=1).order_by('-id') [:1]
# -------------end-ad-manage-meny--------------    

    title = request.GET.get('title')
    if title:
        blogdata = NewsPost.objects.filter(post_title__contains=title,is_active=1,status='active')
        if blogdata.exists():
            #return redirect(newsdetails,title)
            data={
                'BlogData':blogdata,
                'indseo':seo,
                'BlogData':blogdata,
                'event':events,
                'bplogo':bp,
                'Blogcat':Category,
                'adtop':adtop,
                'adleft':adleft,
                'adright':adright,
                'adtl':adtopleft,
                'adtr':adtopright,
                'bgad':festive,
                'headtopad':tophead,
                'popup':popupad,
                'Articale':articales,
                'vidart':vidarticales,
                'headline':headline,
                'bnews':brknews,
                'vidnews':podcast,
                }
            return render(request, 'all-news.html', data)
        else:
           
            data={
                'messages':'No Data Found!',
                }
            return render(request, 'error.html', data)
    else:
        #return JsonResponse({'error_message': 'Title not provided'})
        data={
            'messages':'No Data Found!',
            }
        return render(request, 'error.html', data)
# News-News-search-end-------

# error-page-------
def ErrorPage(request):
    data={
        'messages':'No Data Found!',
        }
    return render(request, 'thanks.html', data)
# error-page-------
# All-News-----------
def AllNews(request,slug):
    alnslug='/all-news/'+ slug
    seo=seo_optimization.objects.get(pageslug=alnslug)
    current_datetime = datetime.now()
    page_number = request.GET.get('page', 1)  
    # Get the page number from the request, default to 1 if not provided
    if slug == 'articles':
        blogdata=NewsPost.objects.filter(schedule_date__lt=current_datetime,articles=1,status='active').order_by('-schedule_date')
        podcast=VideoNews.objects.filter(is_active='active',articles=1).order_by('-schedule_date')
    elif slug == 'breaking':
        blogdata=NewsPost.objects.filter(BreakingNews=1,status='active').order_by('-schedule_date') [:100]
        podcast=VideoNews.objects.filter(is_active='active',BreakingNews=1).order_by('-schedule_date')
    elif slug == 'head-lines':
        blogdata=NewsPost.objects.filter(schedule_date__lt=current_datetime,Head_Lines=1,status='active').order_by('-schedule_date') [:100]
        podcast=VideoNews.objects.filter(is_active='active',Head_Lines=1).order_by('-schedule_date')
    elif slug == 'trending':
        blogdata=NewsPost.objects.filter(schedule_date__lt=current_datetime,trending=1,status='active').order_by('-schedule_date') [:100]
        podcast=VideoNews.objects.filter(is_active='active',trending=1).order_by('-schedule_date')
    elif slug == 'latest':
        blogdata=NewsPost.objects.filter(schedule_date__lt=current_datetime,is_active=1,status='active').order_by('-schedule_date') [:1000]
        podcast=VideoNews.objects.filter(is_active='active',).order_by('-schedule_date')
    else:
        blogdata=NewsPost.objects.filter(schedule_date__lt=current_datetime,is_active=1,status='active').order_by('-schedule_date') [:200]
        podcast=VideoNews.objects.filter(is_active='active').order_by('-schedule_date')
    
    paginator = Paginator(blogdata, 12)   

    try:
        blogdata = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        blogdata = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        blogdata = paginator.page(paginator.num_pages) 
        
    mainnews=NewsPost.objects.filter(schedule_date__lt=current_datetime,status='active').order_by('order')[:4]
    events=NewsPost.objects.filter(Event=1,status='active').order_by('-id') [:10]
    bp=BrandPartner.objects.filter(is_active=1).order_by('-id') [:20]
    articales=NewsPost.objects.filter(schedule_date__lt=current_datetime,articles=1,status='active').order_by('-schedule_date') [:3]
    vidarticales=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('order')[:2]
    headline=NewsPost.objects.filter(schedule_date__lt=current_datetime,Head_Lines=1,status='active').order_by('-schedule_date') [:14]
    trending=NewsPost.objects.filter(schedule_date__lt=current_datetime,trending=1,status='active').order_by('-schedule_date') [:7]
    brknews=NewsPost.objects.filter(BreakingNews=1,status='active').order_by('-schedule_date') [:8]
    Category=category.objects.filter(cat_status='active').order_by('order') [:11]
# --------------ad-manage-meny--------------
    adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')
    adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]
    
    adtrid=ad_category.objects.get(ads_cat_slug='topright-600x80')
    adtopright=ad.objects.filter(ads_cat_id=adtrid.id, is_active=1).order_by('-id') [:1]
    
    adtopid=ad_category.objects.get(ads_cat_slug='leaderboard')
    adtop=ad.objects.filter(ads_cat_id=adtopid.id, is_active=1).order_by('-id') [:1]
    
    adleftid=ad_category.objects.get(ads_cat_slug='skyscraper')
    adleft=ad.objects.filter(ads_cat_id=adleftid.id, is_active=1).order_by('-id') [:1]
    
    adrcol=ad_category.objects.get(ads_cat_slug='mrec')
    adright=ad.objects.filter(ads_cat_id=adrcol.id, is_active=1).order_by('-id') [:1]
    
    festbg=ad_category.objects.get(ads_cat_slug='festivebg')
    festive=ad.objects.filter(ads_cat_id=festbg.id, is_active=1).order_by('-id') [:1]
    
    topad=ad_category.objects.get(ads_cat_slug='topad')
    tophead=ad.objects.filter(ads_cat_id=topad.id, is_active=1).order_by('-id') [:1]
    popup=ad_category.objects.get(ads_cat_slug='popup')
    popupad=ad.objects.filter(ads_cat_id=popup.id, is_active=1).order_by('-id') [:1]
# -------------end-ad-manage-meny--------------    
    # slider=NewsPost.objects.filter(id=1).order_by('id')[:5] use for filter value
    
    slider=NewsPost.objects.filter().order_by('-id')[:5]
    latestnews=NewsPost.objects.all().order_by('-id')[:5]
    data={
            'indseo':seo,
            'BlogData':blogdata,
            'mainnews':mainnews,
            'event':events,
            'bplogo':bp,
            'Slider':slider,
            'Blogcat':Category,
            'latnews':latestnews,
            'adtop':adtop,
            'adleft':adleft,
            'adright':adright,
            'adtl':adtopleft,
            'adtr':adtopright,
            'bgad':festive,
            'headtopad':tophead,
            'popup':popupad,
            'Articale':articales,
            'vidart':vidarticales,
            'headline':headline,
            'trendpost':trending,
            'bnews':brknews,
            'vidnews':podcast,
        }
   
    return render(request,'all-news.html',data)
    #return render(request, 'index.html')
# News-details-page--end--------


# Video-all-News-details-----------
def AllvideoNews(request,slug):
    alnslug='/all-video-news/'+ slug
    seo=seo_optimization.objects.get(pageslug=alnslug)
    
    if slug == 'articles':
        blogdata=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('-id')
    elif slug == 'breaking':
        blogdata=VideoNews.objects.filter(BreakingNews=1,is_active='active',video_type='video').order_by('-id') [:100]
    elif slug == 'head-lines':
        blogdata=VideoNews.objects.filter(Head_Lines=1,is_active='active',video_type='video').order_by('-id') [:100]
    elif slug == 'trending':
        blogdata=VideoNews.objects.filter(trending=1,is_active='active',video_type='video').order_by('-id') [:100]
    elif slug == 'stories':
        blogdata=VideoNews.objects.filter(is_active='active',video_type='reel').order_by('-id')
    else:
        blogdata=VideoNews.objects.filter(is_active='active',video_type='video').order_by('-id')
        
    mainnews=NewsPost.objects.filter(status='active').order_by('order')[:4]
    events=NewsPost.objects.filter(Event=1,status='active').order_by('-id') [:10]
    bp=BrandPartner.objects.filter(is_active=1).order_by('-id') [:20]
    articales=NewsPost.objects.filter(articles=1,status='active').order_by('-id') [:3]
    vidarticales=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('order')[:2]
    headline=NewsPost.objects.filter(Head_Lines=1,status='active').order_by('-id') [:14]
    trending=NewsPost.objects.filter(trending=1,status='active').order_by('-id') [:7]
    brknews=NewsPost.objects.filter(BreakingNews=1,status='active').order_by('-id') [:8]
    podcast=VideoNews.objects.filter(is_active='active').order_by('-id') [:2]
    Category=category.objects.filter(cat_status='active').order_by('order') [:11]
# --------------ad-manage-meny--------------
    adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')
    adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]
    
    adtrid=ad_category.objects.get(ads_cat_slug='topright-600x80')
    adtopright=ad.objects.filter(ads_cat_id=adtrid.id, is_active=1).order_by('-id') [:1]
    
    adtopid=ad_category.objects.get(ads_cat_slug='leaderboard')
    adtop=ad.objects.filter(ads_cat_id=adtopid.id, is_active=1).order_by('-id') [:1]
    
    adleftid=ad_category.objects.get(ads_cat_slug='skyscraper')
    adleft=ad.objects.filter(ads_cat_id=adleftid.id, is_active=1).order_by('-id') [:1]
    
    adrcol=ad_category.objects.get(ads_cat_slug='mrec')
    adright=ad.objects.filter(ads_cat_id=adrcol.id, is_active=1).order_by('-id') [:1]
    
    festbg=ad_category.objects.get(ads_cat_slug='festivebg')
    festive=ad.objects.filter(ads_cat_id=festbg.id, is_active=1).order_by('-id') [:1]
    
    topad=ad_category.objects.get(ads_cat_slug='topad')
    tophead=ad.objects.filter(ads_cat_id=topad.id, is_active=1).order_by('-id') [:1]
    popup=ad_category.objects.get(ads_cat_slug='popup')
    popupad=ad.objects.filter(ads_cat_id=popup.id, is_active=1).order_by('-id') [:1]
# -------------end-ad-manage-meny--------------    
    # slider=NewsPost.objects.filter(id=1).order_by('id')[:5] use for filter value
    
    slider=NewsPost.objects.filter().order_by('-id')[:5]
    latestnews=NewsPost.objects.all().order_by('-id')[:5]
    data={
            'indseo':seo,
            'BlogData':blogdata,
            'mainnews':mainnews,
            'event':events,
            'bplogo':bp,
            'Slider':slider,
            'Blogcat':Category,
            'latnews':latestnews,
            'adtop':adtop,
            'adleft':adleft,
            'adright':adright,
            'adtl':adtopleft,
            'adtr':adtopright,
            'bgad':festive,
            'headtopad':tophead,
            'popup':popupad,
            'Articale':articales,
            'vidart':vidarticales,
            'headline':headline,
            'trendpost':trending,
            'bnews':brknews,
            'vidnews':podcast,
        }
   
    return render(request,'all-video-news.html',data)
    #return render(request, 'index.html')
# Video-all-News-details-page--end--------


# Events-page----------
def UcEvents(request):
    seo='Event'
    eventdata=NewsPost.objects.filter(Event=1,status='active').order_by('-id') [:100]
    articales=NewsPost.objects.filter(articles=1,status='active').order_by('-id') [:3]
    vidarticales=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('order')[:2]
    headline=NewsPost.objects.filter(Head_Lines=1,status='active').order_by('-id') [:14]
    trending=NewsPost.objects.filter(trending=1,status='active').order_by('-id') [:7]
    brknews=NewsPost.objects.filter(BreakingNews=1,status='active').order_by('-id') [:8]
    podcast=VideoNews.objects.filter(is_active='active').order_by('-id') [:2]
    Category=category.objects.filter(cat_status='active').order_by('order') [:11]
# --------------ad-manage-meny--------------
    adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')
    adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]
    
    adtrid=ad_category.objects.get(ads_cat_slug='topright-600x80')
    adtopright=ad.objects.filter(ads_cat_id=adtrid.id, is_active=1).order_by('-id') [:1]
    
    adtopid=ad_category.objects.get(ads_cat_slug='leaderboard')
    adtop=ad.objects.filter(ads_cat_id=adtopid.id, is_active=1).order_by('-id') [:1]
    
    adleftid=ad_category.objects.get(ads_cat_slug='skyscraper')
    adleft=ad.objects.filter(ads_cat_id=adleftid.id, is_active=1).order_by('-id') [:1]
    
    adrcol=ad_category.objects.get(ads_cat_slug='mrec')
    adright=ad.objects.filter(ads_cat_id=adrcol.id, is_active=1).order_by('-id') [:1]
    
    festbg=ad_category.objects.get(ads_cat_slug='festivebg')
    festive=ad.objects.filter(ads_cat_id=festbg.id, is_active=1).order_by('-id') [:1]
    
    topad=ad_category.objects.get(ads_cat_slug='topad')
    tophead=ad.objects.filter(ads_cat_id=topad.id, is_active=1).order_by('-id') [:1]
    popup=ad_category.objects.get(ads_cat_slug='popup')
    popupad=ad.objects.filter(ads_cat_id=popup.id, is_active=1).order_by('-id') [:1]
# -------------end-ad-manage-meny--------------    
    # slider=NewsPost.objects.filter(id=1).order_by('id')[:5] use for filter value
    
    slider=NewsPost.objects.filter().order_by('-id')[:5]
    latestnews=NewsPost.objects.all().order_by('-id')[:5]
    data={
            'indseo':seo,
            'EventData':eventdata,
            'Slider':slider,
            'Blogcat':Category,
            'latnews':latestnews,
            'adtop':adtop,
            'adleft':adleft,
            'adright':adright,
            'adtl':adtopleft,
            'adtr':adtopright,
            'bgad':festive,
            'headtopad':tophead,
            'popup':popupad,
            'Articale':articales,
            'vidart':vidarticales,
            'headline':headline,
            'trendpost':trending,
            'bnews':brknews,
            'vidnews':podcast,
        }
   
    return render(request,'upcoming-events.html',data)
    #return render(request, 'index.html')
# Events-page--end--------
def eventdetails(request,slug):
    seo='eventdetails'
    subcatid=sub_category.objects.get(subcat_slug=slug)
    #print(subcatid.subcat_tag)
    
    catvid=VideoNews.objects.filter(News_Category=subcatid.id,is_active='active',video_type='video').order_by('order')[:50]
    if not catvid:
        catvid="no data"
    #using regex post_tag__regex for search  match....
    databytag=NewsPost.objects.filter(status='active').filter(post_tag__regex = rf'^(\D+){subcatid.subcat_tag}(\D+)').order_by('-id') [:400]
    
    blogdata=NewsPost.objects.filter(is_active=1,status='active',post_cat=subcatid.id).order_by('-id') [:20]
    eventdata=NewsPost.objects.filter(Event=1,status='active').order_by('-id') [:100]
    
    adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')
    adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]
        
    mainnews=NewsPost.objects.filter(status='active').order_by('order')[:4]
    events=NewsPost.objects.filter(Event=1,status='active').order_by('-id') [:10]
    bp=BrandPartner.objects.filter(is_active=1).order_by('-id') [:20]
    articales=NewsPost.objects.filter(articles=1,status='active').order_by('-id') [:3]
    vidarticales=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('order')[:2]
    headline=NewsPost.objects.filter(Head_Lines=1,status='active').order_by('-id') [:14]
    trending=NewsPost.objects.filter(trending=1,status='active').order_by('-id') [:7]
    brknews=NewsPost.objects.filter(BreakingNews=1,status='active').order_by('-id') [:8]
    podcast=VideoNews.objects.filter(is_active='active').order_by('-id') [:2]
    Category=category.objects.filter(cat_status='active').order_by('order') [:11]
# --------------ad-manage-meny--------------
    adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')
    adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]
    
    adtrid=ad_category.objects.get(ads_cat_slug='topright-600x80')
    adtopright=ad.objects.filter(ads_cat_id=adtrid.id, is_active=1).order_by('-id') [:1]
    
    adtopid=ad_category.objects.get(ads_cat_slug='leaderboard')
    adtop=ad.objects.filter(ads_cat_id=adtopid.id, is_active=1).order_by('-id') [:1]
    
    adleftid=ad_category.objects.get(ads_cat_slug='skyscraper')
    adleft=ad.objects.filter(ads_cat_id=adleftid.id, is_active=1).order_by('-id') [:1]
    
    adrcol=ad_category.objects.get(ads_cat_slug='mrec')
    adright=ad.objects.filter(ads_cat_id=adrcol.id, is_active=1).order_by('-id') [:1]
    
    festbg=ad_category.objects.get(ads_cat_slug='festivebg')
    festive=ad.objects.filter(ads_cat_id=festbg.id, is_active=1).order_by('-id') [:1]
    
    topad=ad_category.objects.get(ads_cat_slug='topad')
    tophead=ad.objects.filter(ads_cat_id=topad.id, is_active=1).order_by('-id') [:1]
    popup=ad_category.objects.get(ads_cat_slug='popup')
    popupad=ad.objects.filter(ads_cat_id=popup.id, is_active=1).order_by('-id') [:1]
# -------------end-ad-manage-meny--------------    
    # slider=NewsPost.objects.filter(id=1).order_by('id')[:5] use for filter value
    
    slider=NewsPost.objects.filter().order_by('-id')[:5]
    latestnews=NewsPost.objects.all().order_by('-id')[:5]
    data={
            'indseo':seo,
            'BlogData':blogdata,
            'mainnews':mainnews,
            'event':events,
            'bplogo':bp,
            'Slider':slider,
            'Blogcat':Category,
            'latnews':latestnews,
            'adtop':adtop,
            'adleft':adleft,
            'adright':adright,
            'adtl':adtopleft,
            'adtr':adtopright,
            'bgad':festive,
            'headtopad':tophead,
            'popup':popupad,
            'Articale':articales,
            'vidart':vidarticales,
            'headline':headline,
            'trendpost':trending,
            'bnews':brknews,
            'vidnews':podcast,
            'CatV':catvid,
            'subcat':subcatid,
            'evedata':eventdata,
            'bytag':databytag
        }
    return render(request,'eventdetails.html',data)

# News-details-page----------
def videonewsdetails(request,slug):
    counter=VideoNews.objects.get(slug=slug)
    counter.viewcounter=counter.viewcounter + 1
    counter.save()
    seo='video'
    current_datetime = datetime.now()
    viddetails=VideoNews.objects.get(slug=slug)
    blogdata=NewsPost.objects.filter(schedule_date__lt=current_datetime,is_active=1,status='active').order_by('-id') [:20]
    mainnews=NewsPost.objects.filter(status='active').order_by('order')[:4]
    articales=NewsPost.objects.filter(schedule_date__lt=current_datetime,articles=1,status='active').order_by('-id') [:3]
    
    vidarticales=VideoNews.objects.filter(schedule_date__lt=current_datetime,articles=1,is_active='active',video_type='video').order_by('order')[:2]
    headline=NewsPost.objects.filter(schedule_date__lt=current_datetime,Head_Lines=1,status='active').order_by('-id') [:14]
    trending=NewsPost.objects.filter(schedule_date__lt=current_datetime,trending=1,status='active').order_by('-id') [:3]
    brknews=NewsPost.objects.filter(schedule_date__lt=current_datetime,BreakingNews=1,status='active').order_by('-id') [:8]
    podcast=VideoNews.objects.filter(schedule_date__lt=current_datetime,is_active='active').order_by('-id') [:1]
    # --------------ad-manage-meny--------------
    adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')
    adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]
    
    adtrid=ad_category.objects.get(ads_cat_slug='topright-600x80')
    adtopright=ad.objects.filter(ads_cat_id=adtrid.id, is_active=1).order_by('-id') [:1]
    
    adtopid=ad_category.objects.get(ads_cat_slug='leaderboard')
    adtop=ad.objects.filter(ads_cat_id=adtopid.id, is_active=1).order_by('-id') [:1]
    
    adleftid=ad_category.objects.get(ads_cat_slug='skyscraper')
    adleft=ad.objects.filter(ads_cat_id=adleftid.id, is_active=1).order_by('-id') [:1]
    
    adrcol=ad_category.objects.get(ads_cat_slug='mrec')
    adright=ad.objects.filter(ads_cat_id=adrcol.id, is_active=1).order_by('-id') [:1]
    
    festbg=ad_category.objects.get(ads_cat_slug='festivebg')
    festive=ad.objects.filter(ads_cat_id=festbg.id, is_active=1).order_by('-id') [:1]
    
    # festivetop
    # festiveleft
    # festiveright
# -------------end-ad-manage-meny--------------    
    # slider=NewsPost.objects.filter(id=1).order_by('id')[:5] use for filter value
    Category=category.objects.filter(cat_status='active').order_by('order') [:11]
    slider=NewsPost.objects.filter().order_by('-id')[:5]
    latestnews=NewsPost.objects.all().order_by('-id')[:5]
    data={
            'indseo':seo,
            'Vnews':viddetails,
            'BlogData':blogdata,
            'mainnews':mainnews,
            'Slider':slider,
            'Blogcat':Category,
            'latnews':latestnews,
            'adtop':adtop,
            'adleft':adleft,
            'adright':adright,
            'adtl':adtopleft,
            'adtr':adtopright,
            'bgad':festive,
            'Articale':articales,
            'vidart':vidarticales,
            'headline':headline,
            'trendpost':trending,
            'bnews':brknews,
            'vidnews':podcast,
        }
   
    return render(request,'video-news-details.html',data)
    #return render(request, 'index.html')
# News-details-page--end--------
# cat-details-page---------
def catdetails(request,catlink,slug):
    #blogdetails=NewsPost.objects.get(slug=slug)
    seourl='/'+catlink+'/'+slug
    seoslug = seourl.replace("-", " ").upper()
   
    try:
        seo = seo_optimization.objects.get(pageslug=seourl)
    except seo_optimization.DoesNotExist:
        seo=seo_optimization.objects.get(pageslug='https://www.dxbnewsnetwork.com/')
        #raise Http404("No MyModel matches the given query.")
    
    current_datetime = datetime.now()
    subcatid=sub_category.objects.get(subcat_slug=slug)
    blogdata=NewsPost.objects.filter(post_cat=subcatid.id, schedule_date__lt=current_datetime, status='active').order_by('-id') [:100]
    
    
    mainnews=NewsPost.objects.filter(schedule_date__lt=current_datetime,status='active').order_by('order')[:4]
    # articales=NewsPost.objects.filter(post_cat=subcatid.id, articles=1 ,status='active').order_by('-id') [:2]
    articales=NewsPost.objects.filter(schedule_date__lt=current_datetime,articles=1,status='active').order_by('-id') [:3]

    vidarticales=VideoNews.objects.filter(schedule_date__lt=current_datetime,articles=1,is_active='active',video_type='video').order_by('order')[:2]
    headline=NewsPost.objects.filter(post_cat=subcatid.id, Head_Lines=1,schedule_date__lt=current_datetime,status='active').order_by('-id') [:10]
    trending=NewsPost.objects.filter(post_cat=subcatid.id, trending=1 ,schedule_date__lt=current_datetime,status='active').order_by('-id') [:7]
    brknews=NewsPost.objects.filter(schedule_date__lt=current_datetime,BreakingNews=1,status='active').order_by('-id') [:8]
    podcast=VideoNews.objects.filter(News_Category=subcatid.id,schedule_date__lt=current_datetime,is_active='active').order_by('-id') [:6]
    bp=BrandPartner.objects.filter(is_active=1).order_by('-id') [:20]
    
    # --------------ad-manage-meny--------------
    adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')
    adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]
    
    adtrid=ad_category.objects.get(ads_cat_slug='topright-600x80')
    adtopright=ad.objects.filter(ads_cat_id=adtrid.id, is_active=1).order_by('-id') [:1]
    
    adtopid=ad_category.objects.get(ads_cat_slug='leaderboard')
    adtop=ad.objects.filter(ads_cat_id=adtopid.id, is_active=1).order_by('-id') [:1]
    
    adleftid=ad_category.objects.get(ads_cat_slug='skyscraper')
    adleft=ad.objects.filter(ads_cat_id=adleftid.id, is_active=1).order_by('-id') [:1]
    
    adrcol=ad_category.objects.get(ads_cat_slug='mrec')
    adright=ad.objects.filter(ads_cat_id=adrcol.id, is_active=1).order_by('-id') [:1]
    festbg=ad_category.objects.get(ads_cat_slug='festivebg')
    festive=ad.objects.filter(ads_cat_id=festbg.id, is_active=1).order_by('-id') [:1]
    
    # festivetop
    # festiveleft
    # festiveright
# -------------end-ad-manage-meny--------------   
    # slider=NewsPost.objects.filter(id=1).order_by('id')[:5] use for filter value
    Category=category.objects.filter(cat_status='active').order_by('order') [:11]
    slider=NewsPost.objects.filter().order_by('-id')[:5]
    latestnews=NewsPost.objects.all().order_by('-id')[:5]
    data={ 
            'indseo':seo,
            'sslug':seoslug,
            'slugurl':catlink+'/'+slug,
            'BlogData':blogdata,
            'mainnews':mainnews,
            'Slider':slider,
            'Blogcat':Category,
            'latnews':latestnews,
            'adtop':adtop,
            'adleft':adleft,
            'adright':adright,
            'adtl':adtopleft,
            'adtr':adtopright,
            'bgad':festive,
            'bplogo':bp,
            'Articale':articales,
            'vidart':vidarticales,
            'headline':headline,
            'trendpost':trending,
            'bnews':brknews,
            'vidnews':podcast,
        }
    return render(request,'all-news.html',data)
# cat-details-page--end--------
# cat-contact-page---------
def Contactus(request):
    blogdata=NewsPost.objects.filter(is_active=1,status='active').order_by('-id') [:20]
    mainnews=NewsPost.objects.filter(status='active').order_by('order')[:4]
    articales=NewsPost.objects.filter(articles=1,status='active').order_by('-id') [:3]
    vidarticales=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('order')[:2]
    headline=NewsPost.objects.filter(Head_Lines=1,status='active').order_by('-id') [:14]
    trending=NewsPost.objects.filter(trending=1,status='active').order_by('-id') [:7]
    brknews=NewsPost.objects.filter(BreakingNews=1,status='active').order_by('-id') [:8]
    podcast=VideoNews.objects.filter(is_active='active').order_by('-id') [:1]
    Category=category.objects.filter(cat_status='active').order_by('order') [:11]
    
    # --------------ad-manage-meny--------------
    adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')
    adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]
    
    adtrid=ad_category.objects.get(ads_cat_slug='topright-600x80')
    adtopright=ad.objects.filter(ads_cat_id=adtrid.id, is_active=1).order_by('-id') [:1]
    
    adtopid=ad_category.objects.get(ads_cat_slug='leaderboard')
    adtop=ad.objects.filter(ads_cat_id=adtopid.id, is_active=1).order_by('-id') [:1]
    
    adleftid=ad_category.objects.get(ads_cat_slug='skyscraper')
    adleft=ad.objects.filter(ads_cat_id=adleftid.id, is_active=1).order_by('-id') [:1]
    
    adrcol=ad_category.objects.get(ads_cat_slug='mrec')
    adright=ad.objects.filter(ads_cat_id=adrcol.id, is_active=1).order_by('-id') [:1]
    festbg=ad_category.objects.get(ads_cat_slug='festivebg')
    festive=ad.objects.filter(ads_cat_id=festbg.id, is_active=1).order_by('-id') [:1]
# -------------end-ad-manage-meny--------------   
    # slider=NewsPost.objects.filter(id=1).order_by('id')[:5] use for filter value
    
    slider=NewsPost.objects.filter().order_by('-id')[:5]
    latestnews=NewsPost.objects.all().order_by('-id')[:5]
    data={
            'BlogData':blogdata,
            'mainnews':mainnews,
            'Slider':slider,
            'Blogcat':Category,
            'latnews':latestnews,
            'adtop':adtop,
            'adleft':adleft,
            'adright':adright,
            'adtl':adtopleft,
            'adtr':adtopright,
            'bgad':festive,
            'Articale':articales,
            'vidart':vidarticales,
            'headline':headline,
            'trendpost':trending,
            'bnews':brknews,
            'vidnews':podcast,
        }
    return render(request,'contact.html',data)
# cat-contact-page--end--------

# cat-registration-page---------
def Userregistration(request):
    blogdata=NewsPost.objects.filter(is_active=1,status='active').order_by('-id') [:20]
    mainnews=NewsPost.objects.filter(status='active').order_by('order')[:4]
    articales=NewsPost.objects.filter(articles=1,status='active').order_by('-id') [:3]
    vidarticales=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('order')[:2]
    headline=NewsPost.objects.filter(Head_Lines=1,status='active').order_by('-id') [:14]
    trending=NewsPost.objects.filter(trending=1,status='active').order_by('-id') [:7]
    brknews=NewsPost.objects.filter(BreakingNews=1,status='active').order_by('-id') [:8]
    podcast=VideoNews.objects.filter(is_active='active').order_by('-id') [:1]
    Category=category.objects.filter(cat_status='active').order_by('order') [:11]
    
    # --------------ad-manage-meny--------------
    adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')
    adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]
    
    adtrid=ad_category.objects.get(ads_cat_slug='topright-600x80')
    adtopright=ad.objects.filter(ads_cat_id=adtrid.id, is_active=1).order_by('-id') [:1]
    
    adtopid=ad_category.objects.get(ads_cat_slug='leaderboard')
    adtop=ad.objects.filter(ads_cat_id=adtopid.id, is_active=1).order_by('-id') [:1]
    
    adleftid=ad_category.objects.get(ads_cat_slug='skyscraper')
    adleft=ad.objects.filter(ads_cat_id=adleftid.id, is_active=1).order_by('-id') [:1]
    
    adrcol=ad_category.objects.get(ads_cat_slug='mrec')
    adright=ad.objects.filter(ads_cat_id=adrcol.id, is_active=1).order_by('-id') [:1]
    festbg=ad_category.objects.get(ads_cat_slug='festivebg')
    festive=ad.objects.filter(ads_cat_id=festbg.id, is_active=1).order_by('-id') [:1]
    # festivetop
    # festiveleft
    # festiveright
# -------------end-ad-manage-meny--------------   
    # slider=NewsPost.objects.filter(id=1).order_by('id')[:5] use for filter value
    
    slider=NewsPost.objects.filter().order_by('-id')[:5]
    latestnews=NewsPost.objects.all().order_by('-id')[:5]
    data={
            'BlogData':blogdata,
            'mainnews':mainnews,
            'Slider':slider,
            'Blogcat':Category,
            'latnews':latestnews,
            'adtop':adtop,
            'adleft':adleft,
            'adright':adright,
            'adtl':adtopleft,
            'adtr':adtopright,
            'bgad':festive,
            'Articale':articales,
            'vidart':vidarticales,
            'headline':headline,
            'trendpost':trending,
            'bnews':brknews,
            'vidnews':podcast,
        }
    return render(request,'registration.html',data)

def Registeration(request):
    if request.method == "POST":
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        username=request.POST.get('username')
        email=request.POST.get('email')
        #contact=request.POST.get('contact')
        if request.POST.get('password1')==request.POST.get('password2'):
            password=request.POST.get('password1')
            user=User(
                first_name=fname,
                last_name=lname,
                username = username,
                email = email,
                )
            user.set_password(password)
            user.save()
            if user is not None:
                messages.success(request, 'You Are Registered successfully!')
                return redirect(Userlogin)
            else:
                messages.success(request, 'You Are Not Registered !')
        else:
            messages.success(request, 'The password dose not match !')
    return render(request,'registration.html')
        #messages.success(request, 'Your message was successfully sent!')
    
# cat-registration-page--end--------

# start-subscriber-page-----------
def SubscribeView(request):
    if request.method == "POST":
            fname=request.POST.get('fname')
            email=request.POST.get('email')
            message = f"Subject: Welcome to DXB News Network - Your Source for Insightful News!\n\n" \
                      f"Dear {fname},\n\n" \
                      f"Greetings from DXB News Network!\n\n" \
                      f"We are thrilled to welcome you to our community of informed readers. " \
                      f"As a valued subscriber, you have taken a significant step towards staying updated with the latest news, " \
                      f"in-depth analyses, and diverse perspectives that shape the UAE and the world beyond.\n\n" \
                      f"Here's what you can look forward to as a part of the DXB News Network:\n\n" \
                      f"- Exclusive Updates: Regular newsletters delivering the most important news stories directly to your inbox.\n" \
                      f"- In-Depth Analysis: Insightful articles and features that delve deeper into key issues, offering clarity and context.\n" \
                      f"- Diverse Perspectives: A platform that celebrates diverse voices and viewpoints, enriching your understanding of the world.\n" \
                      f"- Collaboration Opportunities: Engage with us! Share your news, stories, and viewpoints. As a subscriber, " \
                      f"you are more than a reader; you're a potential contributor to our growing network.\n\n" \
                      f"We encourage you to explore our site, participate in discussions, and contribute your insights. " \
                      f"Your active engagement will make our news platform a richer and more vibrant space.\n\n" \
                      f"If you have any queries, suggestions, or contributions, please feel free to reach out to us at contact@dxbnewsnetwork.com. " \
                      f"We are always here to listen and improve.\n\n" \
                      f"Once again, welcome to DXB News Network, where news meets perspective. Together, let's stay informed and connected.\n\n" \
                      f"Warm regards,\n\n" \
                      f"Daniel.\n" \
                      f"Community Engagement Manager\n" \
                      f"DXB News Network\n" \
                      f"dxbnewsnetwork.com\n\n" \
                      f"P.S. Don't forget to follow us on our social media platforms for instant news updates and more interactive content!"
            ip = request.META.get('REMOTE_ADDR', '')  # Retrieve IP address
            country = request.META.get('GEOIP_COUNTRY_NAME', '')  # Retrieve country (using GeoIP)
            city = request.META.get('GEOIP_CITY', '')  # Retrieve city (using GeoIP)

            # Print the retrieved details for confirmation
            # print("Name:", fname)
            # print("Email:", email)
            # print("IP Address:", ip)
            # print("Country:", country)
            # print("City:", city)
            
            SubUser=SubscribeUser(
                name=fname,
                email=email,
                ip=ip,
                country=country,
                city=city,
                )
            SubUser.save()
            if SubUser is not None:
                send_mail(
                    "Welcome to DXB News Network",
                    message,
                    "no-reply@dxbnewsnetwork.com",
                    [email],
                    fail_silently=False,
                )
                messages.success(request, 'You Are Registered successfully!')
                return redirect(thanks)
            else:
                messages.success(request, 'You Are Not Registered !')
        
    return render(request,'index.html')
        #messages.success(request, 'Your message was successfully sent!')
    
# subscribe-page--end--------

def Reg_Form(request):
    if request.method == "POST":
            pname=request.POST.get('person_name')
            cname=request.POST.get('company_name')
            cadd=request.POST.get('company_address')
            phone=request.POST.get('phone')
            email=request.POST.get('email')
            city=request.POST.get('city')
            country=request.POST.get('country')
            dgn=request.POST.get('designation')
            et=request.POST.get('enquiry_type')
            staff=request.POST.get('executive_names')
            sf=request.POST.get('source_from')
            win=request.POST.get('walk_in')
            ip=request.META['REMOTE_ADDR']
            
            RegUser=RegForm(
                person_name=pname,
                company_name=cname,
                company_address= cadd,
                phone=phone,
                email=email,
                city= city,
                country=country,
                diesgantion=dgn,
                enquiry_type=et,
                executive_names=staff,
                source_from=sf,
                walk_in=win,
                ip=ip
                )
            RegUser.save()
            if RegUser is not None:
                messages.success(request, 'You Are Registered successfully!')
                return redirect(thanks)
            else:
                messages.success(request, 'You Are Not Registered !')
        
    return render(request,'thanks.html')
        #messages.success(request, 'Your message was successfully sent!')
    
# cat-subscribe-page--end--------

# cat-Userlogin-page---------
def Userlogin(request):
    seo=seo_optimization.objects.get(pageslug='login')
    if request.method == "POST":
        uname=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(username=uname, password=password)
        if user is not None:
            login(request,user)
            return redirect(Userdashboard)
        else:
            messages.success(request, 'User and Password Wrong!')
            
        return render(request,'login.html')
      
    else:    
        blogdata=NewsPost.objects.filter(is_active=1,status='active').order_by('-id') [:20]
        mainnews=NewsPost.objects.filter(status='active').order_by('order')[:4]
        articales=NewsPost.objects.filter(articles=1,status='active').order_by('-id') [:3]
        vidarticales=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('order')[:2]
        headline=NewsPost.objects.filter(Head_Lines=1,status='active').order_by('-id') [:14]
        trending=NewsPost.objects.filter(trending=1,status='active').order_by('-id') [:7]
        brknews=NewsPost.objects.filter(BreakingNews=1,status='active').order_by('-id') [:8]
        podcast=VideoNews.objects.filter(is_active='active').order_by('-id') [:1]
        Category=category.objects.filter(cat_status='active').order_by('order') [:11]

        # --------------ad-manage-meny--------------
        adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')
        adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]
        
        adtrid=ad_category.objects.get(ads_cat_slug='topright-600x80')
        adtopright=ad.objects.filter(ads_cat_id=adtrid.id, is_active=1).order_by('-id') [:1]
        
        adtopid=ad_category.objects.get(ads_cat_slug='leaderboard')
        adtop=ad.objects.filter(ads_cat_id=adtopid.id, is_active=1).order_by('-id') [:1]
        
        adleftid=ad_category.objects.get(ads_cat_slug='skyscraper')
        adleft=ad.objects.filter(ads_cat_id=adleftid.id, is_active=1).order_by('-id') [:1]
        
        adrcol=ad_category.objects.get(ads_cat_slug='mrec')
        adright=ad.objects.filter(ads_cat_id=adrcol.id, is_active=1).order_by('-id') [:1]
        festbg=ad_category.objects.get(ads_cat_slug='festivebg')
        festive=ad.objects.filter(ads_cat_id=festbg.id, is_active=1).order_by('-id') [:1]
    # festivetop
    # festiveleft
    # festiveright
    # -------------end-ad-manage-meny--------------  
    # slider=NewsPost.objects.filter(id=1).order_by('id')[:5] use for filter value

        slider=NewsPost.objects.filter().order_by('-id')[:5]
        latestnews=NewsPost.objects.all().order_by('-id')[:5]
        data={
                'indseo':seo,
                'BlogData':blogdata,
                'mainnews':mainnews,
                'Slider':slider,
                'Blogcat':Category,
                'latnews':latestnews,
                'adtop':adtop,
                'adleft':adleft,
                'adright':adright,
                'adtl':adtopleft,
                'adtr':adtopright,
                'bgad':festive,
                'Articale':articales,
                'vidart':vidarticales,
                'headline':headline,
                'trendpost':trending,
                'bnews':brknews,
                'vidnews':podcast,
            }
    return render(request,'login.html',data)

# def Logincheck(request):
#     if request.method == "POST":
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user=form.get_user()
#             login(request,user)
#             return redirect(Userdashboard)
#     else:
#         initial_data={'username':'','password':''}
#         form =AuthenticationForm(initial=initial_data)
#         #return redirect('Userlogin')
#     return render(request,'login.html',{'form':form})
# cat-Userlogin-page--end--------

# cat-Userdashboard-page---------
@login_required(login_url="/login")
def Userdashboard(request):
    
    blogdata=NewsPost.objects.filter(is_active=1,status='active', author=request.user.id).order_by('-id') [:20]
    data={
            'BlogData':blogdata,
        }
    return render(request,'user-dashboard.html',data)
# cat-Userdashboard-page--end--------

# cat-ManagePost-page---------
@login_required(login_url="/login")
def ManagePost(request):
    
    blogdata=NewsPost.objects.filter(is_active=1,status='active', author=request.user.id).order_by('-id') [:20]
    data={
            'BlogData':blogdata,
        }
    return render(request,'managepost.html',data)
# cat-ManagePost-page--end--------

# cat-logout-page---------
def Logout(request):
    logout(request)
    return redirect('login')
# cat-career-page---------
@login_required(login_url="/login")
def Career(request):
    if request.method == "POST":    
        name=request.POST.get('name')
        mobnumber=request.POST.get('mobnumber')
        email=request.POST.get('email')
        location=request.POST.get('location')
        nationality=request.POST.get('nationality')
        language=request.POST.get('language')
        address=request.POST.get('address')
        highestedu=request.POST.get('highestedu')
        fos=request.POST.get('fos')
        occupation=request.POST.get('occupation')
        journalexp=request.POST.get('journalexp')
        lastwork=request.POST.get('lastwork')
        portfolio=request.POST.get('portfolio')
        category1=request.POST.get('category')
        equipment=request.POST.get('equipment')
        softwareskill=request.POST.get('softwareskill')
        availability=request.POST.get('availability')
        resume=request.FILES.get('resume')
        whyjoin=request.POST.get('whyjoin')
        anysegment=request.POST.get('anysegment')
        career=CareerApplication(
                name=name,
                mobnumber=mobnumber,
                email=email,
                location=location,
                nationality=nationality,
                language=language,
                address=address,
                highestedu=highestedu,
                fos=fos,
                occupation=occupation,
                journalexp=journalexp,
                lastwork=lastwork,
                portfolio=portfolio,
                category=category1,
                equipment=equipment,
                softwareskill=softwareskill,
                availability=availability,
                resume=resume,
                whyjoin=whyjoin,
                anysegment=anysegment,
                )
        career.save()
        if career is not None:
            messages.success(request, 'You Are Registered successfully!')
            return redirect('career')
        else:
            messages.success(request, 'You Are Not Registered !')
            return redirect('career')
    else:
            blogdata=NewsPost.objects.filter(is_active=1,status='active').order_by('-id') [:20]
            mainnews=NewsPost.objects.filter(status='active').order_by('order')[:4]
            articales=NewsPost.objects.filter(articles=1,status='active').order_by('-id') [:3]
            vidarticales=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('order')[:2]
            headline=NewsPost.objects.filter(Head_Lines=1,status='active').order_by('-id') [:14]
            trending=NewsPost.objects.filter(trending=1,status='active').order_by('-id') [:7]
            brknews=NewsPost.objects.filter(BreakingNews=1,status='active').order_by('-id') [:8]
            podcast=VideoNews.objects.filter(is_active='active').order_by('-id') [:1]
            Category=category.objects.filter(cat_status='active').order_by('order') [:11]
            # --------------ad-manage-meny--------------
            adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')
            adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]

            adtrid=ad_category.objects.get(ads_cat_slug='topright-600x80')
            adtopright=ad.objects.filter(ads_cat_id=adtrid.id, is_active=1).order_by('-id') [:1]

            adtopid=ad_category.objects.get(ads_cat_slug='leaderboard')
            adtop=ad.objects.filter(ads_cat_id=adtopid.id, is_active=1).order_by('-id') [:1]

            adleftid=ad_category.objects.get(ads_cat_slug='skyscraper')
            adleft=ad.objects.filter(ads_cat_id=adleftid.id, is_active=1).order_by('-id') [:1]

            adrcol=ad_category.objects.get(ads_cat_slug='mrec')
            adright=ad.objects.filter(ads_cat_id=adrcol.id, is_active=1).order_by('-id') [:1]

            # festivetop
            # festiveleft
            # festiveright
            # -------------end-ad-manage-meny--------------  
            # slider=NewsPost.objects.filter(id=1).order_by('id')[:5] use for filter value
            
            slider=NewsPost.objects.filter().order_by('-id')[:5]
            latestnews=NewsPost.objects.all().order_by('-id')[:5]
            data={
                    'BlogData':blogdata,
                    'mainnews':mainnews,
                    'Slider':slider,
                    'Blogcat':Category,
                    'latnews':latestnews,
                    'adtop':adtop,
                    'adleft':adleft,
                    'adright':adright,
                    'adtl':adtopleft,
                    'adtr':adtopright,
                    'Articale':articales,
                    'vidart':vidarticales,
                    'headline':headline,
                    'trendpost':trending,
                    'bnews':brknews,
                    'vidnews':podcast,
                }
    return render(request,'career.html',data)
# cat-career-page--end--------
   
# cat-Guestnewspost-page---------
@login_required(login_url="/login")
def Guestpost(request):
    if request.method == "POST":
        if 'upcoming_events' in request.POST:
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
        else:
            start_date = date.today()
            end_date = date.today()
            
        post_image = None
        if 'post_image' in request.FILES:
            post_image = request.FILES['post_image']
        
    # if request.method == "POST":
    #     if 'upcoming_events' in request.POST:
    #         upcoming_events = True
    #         start_date = request.POST.get('start_date')
    #         end_date = request.POST.get('end_date')
    #     else:
    #         upcoming_events = False
    #     if 'post_image' in request.FILES:
    #         post_image = request.FILES['post_image']
    #     else:
    #         post_image = None    
        # form = AuthenticationForm(request, data=request.POST)
        # if form.is_valid(): 
        postcat = request.POST.get('post_cat')
        post_title = request.POST.get('post_title')
        post_short_des = request.POST.get('post_short_des')
        post_des = request.POST.get('post_des')
        post_tag = request.POST.get('post_tag')
        is_active = request.POST.get('is_active')
        Head_Lines = request.POST.get('Head_Lines')
        articles = request.POST.get('articles')
        trending = request.POST.get('trending')
        brknews = request.POST.get('BreakingNews')
        newsch = request.POST.get('scheduled_datetime')
        order = request.POST.get('order')
        counter = request.POST.get('counter')
        status = request.POST.get('status')
        upcoming_events=request.POST.get('upcoming_events')
        
        
        # Instantiate NewsPost with corrected fields
        newsdata = NewsPost(
            post_cat_id=postcat,
            post_title=post_title,
            post_short_des=post_short_des,
            post_des=post_des,
            post_image=post_image,
            post_tag=post_tag,
            is_active=is_active,
            Head_Lines=Head_Lines,
            articles=articles,
            trending=trending,
            BreakingNews=brknews,
            schedule_date=newsch,
            order=order,
            status=status,
            post_status=counter,
            Event=upcoming_events,
            Event_date=start_date,
            Eventend_date=end_date,
            author_id = request.user.id
                )
        newsdata.save()
        if newsdata is not None:
            messages.success(request, 'Your news post successfully!')
            return redirect('guest-news-post')
        else:
            messages.success(request, 'You Are Not Registered !')
            return redirect('guest-news-post')
    else:
            blogdata=NewsPost.objects.filter(is_active=1,status='active').order_by('-id') [:20]
            mainnews=NewsPost.objects.filter(status='active').order_by('order')[:4]
            articales=NewsPost.objects.filter(articles=1,status='active').order_by('-id') [:3]
            vidarticales=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('order')[:2]
            headline=NewsPost.objects.filter(Head_Lines=1,status='active').order_by('-id') [:14]
            trending=NewsPost.objects.filter(trending=1,status='active').order_by('-id') [:3]
            brknews=NewsPost.objects.filter(BreakingNews=1,status='active').order_by('-id') [:8]
            podcast=VideoNews.objects.filter(is_active='active').order_by('-id') [:1]
            Category=category.objects.filter(cat_status='active').order_by('order') [:11]
            Categories=category.objects.filter(cat_status='active').order_by('order') [:11]
            # --------------ad-manage-meny--------------
            adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')
            adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]

            adtrid=ad_category.objects.get(ads_cat_slug='topright-600x80')
            adtopright=ad.objects.filter(ads_cat_id=adtrid.id, is_active=1).order_by('-id') [:1]

            adtopid=ad_category.objects.get(ads_cat_slug='leaderboard')
            adtop=ad.objects.filter(ads_cat_id=adtopid.id, is_active=1).order_by('-id') [:1]

            adleftid=ad_category.objects.get(ads_cat_slug='skyscraper')
            adleft=ad.objects.filter(ads_cat_id=adleftid.id, is_active=1).order_by('-id') [:1]

            adrcol=ad_category.objects.get(ads_cat_slug='mrec')
            adright=ad.objects.filter(ads_cat_id=adrcol.id, is_active=1).order_by('-id') [:1]

            slider=NewsPost.objects.filter().order_by('-id')[:5]
            latestnews=NewsPost.objects.all().order_by('-id')[:5]
            data={
                    'BlogData':blogdata,
                    'mainnews':mainnews,
                    'Slider':slider,
                    'Blogcat':Category,
                    'latnews':latestnews,
                    'adtop':adtop,
                    'adleft':adleft,
                    'adright':adright,
                    'adtl':adtopleft,
                    'adtr':adtopright,
                    'Articale':articales,
                    'vidart':vidarticales,
                    'headline':headline,
                    'trendpost':trending,
                    'bnews':brknews,
                    'vidnews':podcast,
                    'categories':Categories
                }
    return render(request,'guestnewspost.html',data)
# cat-guestnewspost-page--end--------
# cat-EditNewsPost-page--start--------
@login_required(login_url="/login")
def EditNewsPost(request,post_id):
    blogdata=NewsPost.objects.get(id=post_id)
    Category=category.objects.filter(cat_status='active').order_by('order') [:11]
    Categories=category.objects.filter(cat_status='active').order_by('order') [:11]
    trending=NewsPost.objects.filter(trending=1,status='active').order_by('-id') [:3]
    data={
            'ed':blogdata,
            'categories':Categories,
            'Blogcat':Category,
            'trendpost':trending,
            
                
            }
    return render(request,'edit-news-post.html',data)
# cat-updateNewsPost-page--start--------
@login_required(login_url="/login")
def UpdateNewsPost(request):
    if request.method == "POST":
        if 'upcoming_events' in request.POST:
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
        else:
            start_date = date.today()
            end_date = date.today()
            
        
        if 'post_image' in request.FILES:
            post_image = request.FILES['post_image']
        else:
            post_image =request.POST.get('post_image')
            
        post_id = request.POST.get('postId')
        postcat = request.POST.get('post_cat')
        post_title = request.POST.get('post_title')
        post_short_des = request.POST.get('post_short_des')
        post_des = request.POST.get('post_des')
        post_tag = request.POST.get('post_tag')
        is_active = request.POST.get('is_active')
        Head_Lines = request.POST.get('Head_Lines')
        articles = request.POST.get('articles')
        trending = request.POST.get('trending')
        brknews = request.POST.get('BreakingNews')
        newsch = request.POST.get('scheduled_datetime')
        order = request.POST.get('order')
        counter = request.POST.get('counter')
        status = request.POST.get('status')
        upcoming_events=request.POST.get('upcoming_events')
        
        
        # Instantiate NewsPost with corrected fields
        newsdata = NewsPost(
            id=post_id,
            post_cat_id=postcat,
            post_title=post_title,
            post_short_des=post_short_des,
            post_des=post_des,
            post_image=post_image,
            post_tag=post_tag,
            is_active=is_active,
            Head_Lines=Head_Lines,
            articles=articles,
            trending=trending,
            BreakingNews=brknews,
            schedule_date=newsch,
            order=order,
            status=status,
            post_status=counter,
            Event=upcoming_events,
            Event_date=start_date,
            Eventend_date=end_date,
            author_id = request.user.id,
            post_date=date.today()
                )
        newsdata.save()
        if newsdata is not None:
            messages.success(request, 'Your news post Update successfully!')
            return redirect('managepost')
        else:
            messages.success(request, 'Not Update Somthing Went Wrong !')
            return redirect('managepost')
    
# about-us-page---------
def Aboutus(request):
    blogdata=NewsPost.objects.all().order_by('-id') [:4]
    articales=NewsPost.objects.filter(articles=1, status='active').order_by('-id') [:3]
    vidarticales=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('order')[:2]
    headline=NewsPost.objects.filter(Head_Lines=1, status='active').order_by('-id') [:14]
    trending=NewsPost.objects.filter(trending=1, status='active').order_by('-id') [:3]
    brknews=NewsPost.objects.filter(BreakingNews=1,status='active').order_by('-id') [:8]
    
    # --------------ad-manage-meny--------------
    adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')
    adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]
    
    adtrid=ad_category.objects.get(ads_cat_slug='topright-600x80')
    adtopright=ad.objects.filter(ads_cat_id=adtrid.id, is_active=1).order_by('-id') [:1]
    
    adtopid=ad_category.objects.get(ads_cat_slug='leaderboard')
    adtop=ad.objects.filter(ads_cat_id=adtopid.id, is_active=1).order_by('-id') [:1]
    
    adleftid=ad_category.objects.get(ads_cat_slug='skyscraper')
    adleft=ad.objects.filter(ads_cat_id=adleftid.id, is_active=1).order_by('-id') [:1]
    
    adrcol=ad_category.objects.get(ads_cat_slug='mrec')
    adright=ad.objects.filter(ads_cat_id=adrcol.id, is_active=1).order_by('-id') [:1]
    
    # festivetop
    # festiveleft
    # festiveright
# -------------end-ad-manage-meny--------------  
    # slider=NewsPost.objects.filter(id=1).order_by('id')[:5] use for filter value
    Category=category.objects.filter(cat_status='active').order_by('order') [:11]
    slider=NewsPost.objects.filter().order_by('-id')[:5]
    latestnews=NewsPost.objects.all().order_by('-id')[:5]
    data={
            'BlogData':blogdata,
            'Slider':slider,
            'Blogcat':Category,
            'latnews':latestnews,
            'adtop':adtop,
            'adleft':adleft,
            'adright':adright,
            'adtl':adtopleft,
            'adtr':adtopright,
            'Articale':articales,
            'vidart':vidarticales,
            'headline':headline,
            'trendpost':trending,
            'bnews':brknews,
        }
   
    return render(request,'aboutus.html',data)
# sitemap-us-page---------
# thanks-page---------
def thanks(request):
    blogdata=NewsPost.objects.all().order_by('-id') [:4]
    articales=NewsPost.objects.filter(articles=1, status='active').order_by('-id') [:3]
    vidarticales=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('order')[:2]
    headline=NewsPost.objects.filter(Head_Lines=1, status='active').order_by('-id') [:14]
    trending=NewsPost.objects.filter(trending=1, status='active').order_by('-id') [:7]
    brknews=NewsPost.objects.filter(BreakingNews=1,status='active').order_by('-id') [:8]
    
    # --------------ad-manage-meny--------------
    adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')
    adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]
    
    adtrid=ad_category.objects.get(ads_cat_slug='topright-600x80')
    adtopright=ad.objects.filter(ads_cat_id=adtrid.id, is_active=1).order_by('-id') [:1]
    
    adtopid=ad_category.objects.get(ads_cat_slug='leaderboard')
    adtop=ad.objects.filter(ads_cat_id=adtopid.id, is_active=1).order_by('-id') [:1]
    
    adleftid=ad_category.objects.get(ads_cat_slug='skyscraper')
    adleft=ad.objects.filter(ads_cat_id=adleftid.id, is_active=1).order_by('-id') [:1]
    
    adrcol=ad_category.objects.get(ads_cat_slug='mrec')
    adright=ad.objects.filter(ads_cat_id=adrcol.id, is_active=1).order_by('-id') [:1]
    
    # festivetop
    # festiveleft
    # festiveright
# -------------end-ad-manage-meny--------------  
    # slider=NewsPost.objects.filter(id=1).order_by('id')[:5] use for filter value
    Category=category.objects.filter(cat_status='active').order_by('order') [:11]
    slider=NewsPost.objects.filter().order_by('-id')[:5]
    latestnews=NewsPost.objects.all().order_by('-id')[:5]
    data={
            'BlogData':blogdata,
            'Slider':slider,
            'Blogcat':Category,
            'latnews':latestnews,
            'adtop':adtop,
            'adleft':adleft,
            'adright':adright,
            'adtl':adtopleft,
            'adtr':adtopright,
            'Articale':articales,
            'vidart':vidarticales,
            'headline':headline,
            'trendpost':trending,
            'bnews':brknews,
        }
   
    return render(request,'thanks.html',data)
# thanks-us-page---------
def PrivacyPolicy (request):
    blogdata=NewsPost.objects.all().order_by('-id') [:4]
    articales=NewsPost.objects.filter(articles=1, status='active').order_by('-id') [:3]
    vidarticales=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('order')[:2]
    headline=NewsPost.objects.filter(Head_Lines=1, status='active').order_by('-id') [:14]
    trending=NewsPost.objects.filter(trending=1, status='active').order_by('-id') [:3]
    brknews=NewsPost.objects.filter(BreakingNews=1,status='active').order_by('-id') [:8]
    
    # --------------ad-manage-meny--------------
    adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')
    adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]
    
    adtrid=ad_category.objects.get(ads_cat_slug='topright-600x80')
    adtopright=ad.objects.filter(ads_cat_id=adtrid.id, is_active=1).order_by('-id') [:1]
    
    adtopid=ad_category.objects.get(ads_cat_slug='leaderboard')
    adtop=ad.objects.filter(ads_cat_id=adtopid.id, is_active=1).order_by('-id') [:1]
    
    adleftid=ad_category.objects.get(ads_cat_slug='skyscraper')
    adleft=ad.objects.filter(ads_cat_id=adleftid.id, is_active=1).order_by('-id') [:1]
    
    adrcol=ad_category.objects.get(ads_cat_slug='mrec')
    adright=ad.objects.filter(ads_cat_id=adrcol.id, is_active=1).order_by('-id') [:1]
    
    # festivetop
    # festiveleft
    # festiveright
# -------------end-ad-manage-meny--------------  
    # slider=NewsPost.objects.filter(id=1).order_by('id')[:5] use for filter value
    Category=category.objects.filter(cat_status='active').order_by('order') [:11]
    slider=NewsPost.objects.filter().order_by('-id')[:5]
    latestnews=NewsPost.objects.all().order_by('-id')[:5]
    data={
            'BlogData':blogdata,
            'Slider':slider,
            'Blogcat':Category,
            'latnews':latestnews,
            'adtop':adtop,
            'adleft':adleft,
            'adright':adright,
            'adtl':adtopleft,
            'adtr':adtopright,
            'Articale':articales,
            'vidart':vidarticales,
            'headline':headline,
            'trendpost':trending,
            'bnews':brknews,
        }
    return render(request,'privacypolicy.html',data)

def TandC(request):
    blogdata=NewsPost.objects.all().order_by('-id') [:4]
    articales=NewsPost.objects.filter(articles=1, status='active').order_by('-id') [:3]
    vidarticales=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('order')[:2]
    headline=NewsPost.objects.filter(Head_Lines=1, status='active').order_by('-id') [:14]
    trending=NewsPost.objects.filter(trending=1, status='active').order_by('-id') [:3]
    brknews=NewsPost.objects.filter(BreakingNews=1,status='active').order_by('-id') [:8]
    
    # --------------ad-manage-meny--------------
    adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')
    adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]
    
    adtrid=ad_category.objects.get(ads_cat_slug='topright-600x80')
    adtopright=ad.objects.filter(ads_cat_id=adtrid.id, is_active=1).order_by('-id') [:1]
    
    adtopid=ad_category.objects.get(ads_cat_slug='leaderboard')
    adtop=ad.objects.filter(ads_cat_id=adtopid.id, is_active=1).order_by('-id') [:1]
    
    adleftid=ad_category.objects.get(ads_cat_slug='skyscraper')
    adleft=ad.objects.filter(ads_cat_id=adleftid.id, is_active=1).order_by('-id') [:1]
    
    adrcol=ad_category.objects.get(ads_cat_slug='mrec')
    adright=ad.objects.filter(ads_cat_id=adrcol.id, is_active=1).order_by('-id') [:1]
    
    # festivetop
    # festiveleft
    # festiveright
# -------------end-ad-manage-meny--------------  
    # slider=NewsPost.objects.filter(id=1).order_by('id')[:5] use for filter value
    Category=category.objects.filter(cat_status='active').order_by('order') [:11]
    slider=NewsPost.objects.filter().order_by('-id')[:5]
    latestnews=NewsPost.objects.all().order_by('-id')[:5]
    data={
            'BlogData':blogdata,
            'Slider':slider,
            'Blogcat':Category,
            'latnews':latestnews,
            'adtop':adtop,
            'adleft':adleft,
            'adright':adright,
            'adtl':adtopleft,
            'adtr':adtopright,
            'Articale':articales,
            'vidart':vidarticales,
            'headline':headline,
            'trendpost':trending,
            'bnews':brknews,
        }
    return render(request,'t&c.html',data)

def Disclaimer(request):
    blogdata=NewsPost.objects.all().order_by('-id') [:4]
    articales=NewsPost.objects.filter(articles=1, status='active').order_by('-id') [:3]
    vidarticales=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('order')[:2]
    headline=NewsPost.objects.filter(Head_Lines=1, status='active').order_by('-id') [:14]
    trending=NewsPost.objects.filter(trending=1, status='active').order_by('-id') [:3]
    brknews=NewsPost.objects.filter(BreakingNews=1,status='active').order_by('-id') [:8]
    
    # --------------ad-manage-meny--------------
    adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')
    adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]
    
    adtrid=ad_category.objects.get(ads_cat_slug='topright-600x80')
    adtopright=ad.objects.filter(ads_cat_id=adtrid.id, is_active=1).order_by('-id') [:1]
    
    adtopid=ad_category.objects.get(ads_cat_slug='leaderboard')
    adtop=ad.objects.filter(ads_cat_id=adtopid.id, is_active=1).order_by('-id') [:1]
    
    adleftid=ad_category.objects.get(ads_cat_slug='skyscraper')
    adleft=ad.objects.filter(ads_cat_id=adleftid.id, is_active=1).order_by('-id') [:1]
    
    adrcol=ad_category.objects.get(ads_cat_slug='mrec')
    adright=ad.objects.filter(ads_cat_id=adrcol.id, is_active=1).order_by('-id') [:1]
    
    # festivetop
    # festiveleft
    # festiveright
# -------------end-ad-manage-meny--------------  
    # slider=NewsPost.objects.filter(id=1).order_by('id')[:5] use for filter value
    Category=category.objects.filter(cat_status='active').order_by('order') [:11]
    slider=NewsPost.objects.filter().order_by('-id')[:5]
    latestnews=NewsPost.objects.all().order_by('-id')[:5]
    data={
            'BlogData':blogdata,
            'Slider':slider,
            'Blogcat':Category,
            'latnews':latestnews,
            'adtop':adtop,
            'adleft':adleft,
            'adright':adright,
            'adtl':adtopleft,
            'adtr':adtopright,
            'Articale':articales,
            'vidart':vidarticales,
            'headline':headline,
            'trendpost':trending,
            'bnews':brknews,
        }
    return render(request,'disclaimer.html',data)

def SiteMap(request):
    blogdata=NewsPost.objects.all().order_by('-id') [:4]
    articales=NewsPost.objects.filter(articles=1, status='active').order_by('-id') [:3]
    vidarticales=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('order')[:2]
    headline=NewsPost.objects.filter(Head_Lines=1, status='active').order_by('-id') [:14]
    trending=NewsPost.objects.filter(trending=1, status='active').order_by('-id') [:3]
    brknews=NewsPost.objects.filter(BreakingNews=1,status='active').order_by('-id') [:8]
    
    # --------------ad-manage-meny--------------
    adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')
    adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]
    
    adtrid=ad_category.objects.get(ads_cat_slug='topright-600x80')
    adtopright=ad.objects.filter(ads_cat_id=adtrid.id, is_active=1).order_by('-id') [:1]
    
    adtopid=ad_category.objects.get(ads_cat_slug='leaderboard')
    adtop=ad.objects.filter(ads_cat_id=adtopid.id, is_active=1).order_by('-id') [:1]
    
    adleftid=ad_category.objects.get(ads_cat_slug='skyscraper')
    adleft=ad.objects.filter(ads_cat_id=adleftid.id, is_active=1).order_by('-id') [:1]
    
    adrcol=ad_category.objects.get(ads_cat_slug='mrec')
    adright=ad.objects.filter(ads_cat_id=adrcol.id, is_active=1).order_by('-id') [:1]
    
    # festivetop
    # festiveleft
    # festiveright
# -------------end-ad-manage-meny--------------  
    # slider=NewsPost.objects.filter(id=1).order_by('id')[:5] use for filter value
    Category=category.objects.filter(cat_status='active').order_by('order') [:11]
    slider=NewsPost.objects.filter().order_by('-id')[:5]
    latestnews=NewsPost.objects.all().order_by('-id')[:5]
    data={
            'BlogData':blogdata,
            'Slider':slider,
            'Blogcat':Category,
            'latnews':latestnews,
            'adtop':adtop,
            'adleft':adleft,
            'adright':adright,
            'adtl':adtopleft,
            'adtr':adtopright,
            'Articale':articales,
            'vidart':vidarticales,
            'headline':headline,
            'trendpost':trending,
            'bnews':brknews,
            'sitemapcat':Category,
        }
    return render(request,'sitemap.html',data)

# advertise-with-us-page---------
def advertise(request):
    blogdata=NewsPost.objects.all().order_by('-id') [:4]
    articales=NewsPost.objects.filter(articles=1, status='active').order_by('-id') [:3]
    vidarticales=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('order')[:2]
    headline=NewsPost.objects.filter(Head_Lines=1, status='active').order_by('-id') [:14]
    trending=NewsPost.objects.filter(trending=1, status='active').order_by('-id') [:7]
    brknews=NewsPost.objects.filter(BreakingNews=1,status='active').order_by('-id') [:8]
    
    # --------------ad-manage-meny--------------
    adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')
    adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]
    
    adtrid=ad_category.objects.get(ads_cat_slug='topright-600x80')
    adtopright=ad.objects.filter(ads_cat_id=adtrid.id, is_active=1).order_by('-id') [:1]
    
    adtopid=ad_category.objects.get(ads_cat_slug='leaderboard')
    adtop=ad.objects.filter(ads_cat_id=adtopid.id, is_active=1).order_by('-id') [:1]
    
    adleftid=ad_category.objects.get(ads_cat_slug='skyscraper')
    adleft=ad.objects.filter(ads_cat_id=adleftid.id, is_active=1).order_by('-id') [:1]
    
    adrcol=ad_category.objects.get(ads_cat_slug='mrec')
    adright=ad.objects.filter(ads_cat_id=adrcol.id, is_active=1).order_by('-id') [:1]
    
    # festivetop
    # festiveleft
    # festiveright
# -------------end-ad-manage-meny--------------  
    # slider=NewsPost.objects.filter(id=1).order_by('id')[:5] use for filter value
    Category=category.objects.filter(cat_status='active').order_by('order') [:11]
    slider=NewsPost.objects.filter().order_by('-id')[:5]
    latestnews=NewsPost.objects.all().order_by('-id')[:5]
    data={
            'BlogData':blogdata,
            'Slider':slider,
            'Blogcat':Category,
            'latnews':latestnews,
            'adtop':adtop,
            'adleft':adleft,
            'adright':adright,
            'adtl':adtopleft,
            'adtr':adtopright,
            'Articale':articales,
            'vidart':vidarticales,
            'headline':headline,
            'trendpost':trending,
            'bnews':brknews,
        }
   
    return render(request,'advertise-with-us.html',data)
