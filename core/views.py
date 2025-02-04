from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .trendcatcher import datafetcher
from .models import UserBlog, Comment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.auth import logout
from datetime import datetime

from . forms import UserCreation, BlogForm, BlogEditForm, CommentForm
# Create your views here.


def homeview(request):
    article_dict = datafetcher()
    # article_dict = {'mains': [{'headline': ' Foundation offers free medical  services to 500 Imo widows, others ', 'link': 'https://punchng.com/foundation-offers-free-medical-services-to-500-imo-widows-others/'}, {'headline': ' Governorship Election Updates ', 'link': 'https://punchng.com/governorship-election-updates/'}, {'headline': ' Five Ogun chiefs bag six months jail for breach of peace ', 'link': 'https://punchng.com/five-ogun-chiefs-bag-six-months-jail-for-breach-of-peace/'}, {'headline': ' Leave Wike alone, 45 Rivers elders tell Odili ', 'link': 'https://punchng.com/leave-wike-alone-45-rivers-elders-tell-odili/'}, {'headline': ' NAPTIP begins rehabilitation of Nigerian rescued from Iraqi traffickers ', 'link': 'https://punchng.com/naptip-begins-rehabilitation-of-nigerian-rescued-from-iraqi-traffickers/'}, {'headline': ' FG set to take over 157 abandoned Almajiri schools ', 'link': 'https://punchng.com/fg-set-to-take-over-157-abandoned-almajiri-schools/'}, {'headline': ' EFCC detains 10 officers in Lagos over alleged theft ', 'link': 'https://punchng.com/efcc-detains-10-officers-in-lagos-over-alleged-theft/'}, {'headline': ' Spanish sports council clears Dani Olmo for Barcelona ', 'link': 'https://punchng.com/spanish-sports-council-clears-dani-olmo-for-barcelona/'}, {'headline': " Ohanaeze Ndigbo election 'll be peaceful, says MASSOB ", 'link': 'https://punchng.com/ohanaeze-ndigbo-election-ll-be-peaceful-says-massob/'}, {'headline': ' Osun donates food items, building materials to disaster victims ', 'link': 'https://punchng.com/osun-donates-food-items-building-materials-to-disaster-victims/'}, {'headline': ' One dead, others injured in Oyo road crash ', 'link': 'https://punchng.com/one-dead-others-injured-in-oyo-road-crash/'}, {'headline': " N'Assembly demands improved capital project funding for 2024 budget ", 'link': 'https://punchng.com/nassembly-demands-improved-capital-project-funding-for-2024-budget/'}, {'headline': ' PICTORIAL: Gombe CAN insists 65 injured in Christmas procession accident ', 'link': 'https://punchng.com/pictorial-gombe-can-insists-65-injured-in-christmas-procession/'}, {'headline': ' Adamawa plans commission to tackle farmer-herder clash ', 'link': 'https://punchng.com/adamawa-plans-commission-to-tackle-farmer-herder-clash/'}, {'headline': ' NOA unveils awareness campaign against HMPV in Akwa Ibom ', 'link': 'https://punchng.com/noa-unveils-awareness-campaign-against-hmpv-in-akwa-ibom/'}, {'headline': ' Kwara CP decorates 96 promoted officers ', 'link': 'https://punchng.com/kwara-cp-decorates-96-promoted-officers/'}, {'headline': ' Five killed, 10 injured in Delta road crash ', 'link': 'https://punchng.com/five-dead-10-injured-in-delta-road-accidents/'}, {'headline': ' Womans breast grows four times larger after covid vaccine jab ', 'link': 'https://punchng.com/womans-breast-grows-four-times-larger-after-covid-vaccine-jab/'}, {'headline': ' Islamic group laments lack of social media regulation ', 'link': 'https://punchng.com/islamic-group-laments-lack-of-social-media-regulation/'}, {'headline': ' Accidental discharge kills Sokoto guard after kidnap rescue ', 'link': 'https://punchng.com/accidental-discharge-kills-sokoto-guard-member-after-kidnap-rescue/'}, {'headline': ' Kano laments N1.5bn monthly spending on water treatment ', 'link': 'https://punchng.com/kano-laments-n1-5bn-monthly-spending-on-water-treatment/'}, {'headline': ' PSC appoints Towuru to represent South-South as Pedro retires ', 'link': 'https://punchng.com/psc-appoints-towuru-to-represent-south-south-as-pedro-retires/'}, {'headline': ' Buy tractors instead of SUVs, Ogun poultry farmerstellgovt ', 'link': 'https://punchng.com/buy-tractors-instead-of-suvs-ogun-poultry-farmers-tell-govt/'}, {'headline': ' Anambra Catholic priest resigns, embraces traditional religion ', 'link': 'https://punchng.com/anambra-catholic-priest-resigns-embraces-traditional-religion/'}, {'headline': ' Women affairs minister celebrates Lagos First Lady at 58 ', 'link': 'https://punchng.com/women-affairs-minister-celebrates-lagos-first-lady-at-58/'}, {'headline': ' UNILAG to graduate 16,409 students, two with perfect 5.0 CGPA ', 'link': 'https://punchng.com/unilag-to-graduate-16409-students-two-with-perfect-5-0-cgpa/'}, {'headline': ' Suspects held as police rescue 59 trafficked Kano children ', 'link': 'https://punchng.com/police-rescue-59-trafficked-kano-children-arrest-suspects/'}, {'headline': ' Kano to distribute N3bn flood relief fund ', 'link': 'https://punchng.com/kano-to-distribute-n3bn-flood-relief-fund/'}, {'headline': ' EPL: Lopetegui sacked by West Ham following Man City defeat ', 'link': 'https://punchng.com/epl-lopetegui-sacked-by-west-ham-following-man-city-defeat/'}, {'headline': ' Court orders temporary forfeiture of funds linked to ex-Abia gov ', 'link': 'https://punchng.com/court-orders-temporary-forfeiture-of-funds-linked-to-ex-abia-gov/'}, {'headline': ' Okupe apologises to Kyari for past criticism ', 'link': 'https://punchng.com/okupe-apologises-to-kyari-for-past-criticism/'}, {'headline': ' Court jails man seven years for stealing phone ', 'link': 'https://punchng.com/court-jails-man-seven-years-for-stealing-phone/'}]}
    return render(request, "trendyblogs.html", {'article_dict': article_dict,})

def signupview(request):
    if request.method == 'POST':
        form = UserCreation(request.POST)
        if form.is_valid():
            user = form.save()
            user_group = Group.objects.get(name= 'slug')
            user.groups.add(user_group)
            user.save()
            return redirect("/login/")
    else:
        form = UserCreation()
    return render(request, "signup.html", {"form": form})


@login_required()
def createblogview(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit= False)
            blog.author = request.user
            blog.save()
            return redirect(f"/blog/{blog.pk}")
    else:
        form = BlogForm()
    return render(request, 'blogcreate.html', {"form": form})

def logoutview(request):
    logout(request)
    return redirect('/')

@login_required()
def editblogview(request, pk):
    blog = get_object_or_404(UserBlog, pk=pk, author= request.user)
    if request.method == 'POST':
        form = BlogEditForm(request.POST, instance= blog)
        if form.is_valid():
            form.save()
            return redirect(f"/blog/{blog.pk}")
    else:
        form = BlogEditForm(initial={'headline': blog.headline, 'body': blog.body})

    return render(request, 'blogedit.html', {"form": form})


@login_required()
def dashboard(request):
    blogs = UserBlog.objects.filter(author= request.user)
    return render(request, "profile.html", {'blogs': blogs})

def profileview(request, pk):
    user = get_object_or_404(User, id=pk)
    blogs = UserBlog.objects.filter(author= user)
    return render(request, "user.html", {'blogs': blogs, 'user': user})

def blogview(request, pk):
    blog = get_object_or_404(UserBlog, id= pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit= False)
            comment.author = request.user
            comment.blog = blog
            comment.save()
    else:
        form = CommentForm()

    return render(request, 'blogpage.html', {'blog': blog, 'form': form})

def allblogsview(request):
    all_blogs = UserBlog.objects.all
    return render(request, "allblogs.html", {'all_blogs': all_blogs})

@login_required()
def deleteview(request, pk):
    blog_data = get_object_or_404(UserBlog, id= pk)
    blog_data.delete()
    return redirect("/all-blogs/")
 
@login_required()
def deletecommentview(request, pk):
    comment = get_object_or_404(Comment, id= pk)
    blog = comment.blog.id
    comment.delete()
    return redirect(f"/blog/{blog}/")