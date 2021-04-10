from django.forms import forms
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


# Create your views here.
def index(request):
    most_played = []
    #Display recent songs
    if not request.user.is_anonymous :
        recent = list(Recent.objects.filter(user=request.user).values('song_id').order_by('-id'))
        recent_id = [each['song_id'] for each in recent][:5]
        recent_songs_unsorted = Song.objects.filter(id__in=recent_id,recent__user=request.user)
        recent_songs = list()
        for id in recent_id:
            recent_songs.append(recent_songs_unsorted.get(id=id))
        max_played=list(Maxplayed.objects.all())
        # most_played=[]
        if len(recent)!=0:
            m=list(recent[0].values())[0]
            songs = Song.objects.filter(id=m).first()
            if len(max_played)==0:

                m1=Maxplayed.objects.create(user=request.user,song=songs,no_played=1)
                max_played.append(m1)
                print("in 0")
            
            else:
                m2=Maxplayed.objects.filter(user=request.user)
                flag=0
                
                for i in m2:
                    if i.song_id==m:
                        print("in if",i.song_id,m)
                        temp=i.no_played+1
                        Maxplayed.objects.filter(song_id=m).update(no_played=temp)
                        max_played.append(i)
                        flag=1
                        break
                if flag==0:
                    print("in else",m)
                    m1=Maxplayed.objects.create(user=request.user,song=songs,no_played=1)
                    m1.save()
                    max_played.append(m1)
            print(max_played)
            m2=list(Maxplayed.objects.filter(user=request.user))
            m2=sorted(m2,key=lambda x:x.no_played,reverse=True)
            temp_list=[print(i.no_played) for i in m2]
            for i in m2:
                
                songg=i.song
                most_played.append(songg)
            
    else:
        recent = None
        recent_songs = None
        max_played = None

    # Display liked songs
    if not request.user.is_anonymous:
        liked = list(Favourite.objects.filter(user=request.user, is_fav=True).distinct().values('song_id'))
        print('liked', liked)
        liked_id = [each['song_id'] for each in liked][:5]
        liked_songs_unsorted = Song.objects.filter(id__in=liked_id,favourite__user=request.user)
        list_liked_songs = list()
        for id in liked_id:
            list_liked_songs.append(liked_songs_unsorted.get(id=id))
    else:
        liked = None
        list_liked_songs = None


    first_time = False
    #Last played song
    if not request.user.is_anonymous:
        last_played_list = list(Recent.objects.filter(user=request.user).values('song_id').order_by('-id'))
        if last_played_list:
            last_played_id = last_played_list[0]['song_id']
            last_played_song = Song.objects.get(id=last_played_id)
        else:
            first_time = True
            last_played_song = Song.objects.get(id=7)

    else:
        first_time = True
        last_played_song = Song.objects.get(id=7)

    #Display all songs
    songs = Song.objects.all()

    #Display few songs on home page
    songs_all = list(Song.objects.all().values('id').order_by('?'))
    sliced_ids = [each['id'] for each in songs_all][:5]
    indexpage_songs = Song.objects.filter(id__in=sliced_ids)

    # Display Hindi Songs
    songs_hindi = list(Song.objects.filter(language='Hindi').values('id'))
    sliced_ids = [each['id'] for each in songs_hindi][:5]
    indexpage_hindi_songs = Song.objects.filter(id__in=sliced_ids)

    # Display English Songs
    songs_english = list(Song.objects.filter(language='English').values('id'))
    sliced_ids = [each['id'] for each in songs_english][:5]
    indexpage_english_songs = Song.objects.filter(id__in=sliced_ids)

    if len(request.GET) > 0:
        search_query = request.GET.get('q')
        filtered_songs = songs.filter(Q(name__icontains=search_query)).distinct()
        context = {'all_songs': filtered_songs,'last_played':last_played_song,'query_search':True}
        return render(request, 'musicapp/index.html', context)

    context = {
        'all_songs':indexpage_songs,
        'recent_songs': recent_songs,
        'list_liked_songs' : list_liked_songs,
        'max_played':most_played[:min(len(most_played), 5)],
        'hindi_songs':indexpage_hindi_songs,
        'english_songs':indexpage_english_songs,
        'last_played':last_played_song,
        'first_time': first_time,
        'query_search':False,
    }
    return render(request, 'musicapp/index.html', context=context)


def hindi_songs(request):

    hindi_songs1 = Song.objects.filter(language='Hindi')

    #Last played song
    last_played_list = list(Recent.objects.values('song_id').order_by('-id'))
    if last_played_list:
        last_played_id = last_played_list[0]['song_id']
        last_played_song = Song.objects.get(id=last_played_id)
    else:
        last_played_song = Song.objects.get(id=7)

    query = request.GET.get('q')

    if query:
        hindi_songs1 = Song.objects.filter(Q(name__icontains=query)).distinct()
        context = {'hindi_songs': hindi_songs1}
        return render(request, 'musicapp/hindi_songs.html', context)

    context = {'hindi_songs':hindi_songs1, 'last_played':last_played_song}
    return render(request, 'musicapp/hindi_songs.html',context=context)


def english_songs(request):

    english_songs1 = Song.objects.filter(language='English')

    #Last played song
    last_played_list = list(Recent.objects.values('song_id').order_by('-id'))
    if last_played_list:
        last_played_id = last_played_list[0]['song_id']
        last_played_song = Song.objects.get(id=last_played_id)
    else:
        last_played_song = Song.objects.get(id=7)

    query = request.GET.get('q')

    if query:
        english_songs1 = Song.objects.filter(Q(name__icontains=query)).distinct()
        context = {'english_songs': english_songs1}
        return render(request, 'musicapp/english_songs.html', context)

    context = {'english_songs':english_songs1, 'last_played':last_played_song}
    return render(request, 'musicapp/english_songs.html',context=context)

@login_required(login_url='login')
def play_song(request, song_id):
    songs = Song.objects.filter(id=song_id).first()
    # Add data to recent database
    if list(Recent.objects.filter(song=songs,user=request.user).values()):
        data = Recent.objects.filter(song=songs,user=request.user)
        data.delete()
    data = Recent(song=songs,user=request.user)
    data.save()
    return redirect('all_songs')


@login_required(login_url='login')
def play_song_index(request, song_id):
    songs = Song.objects.filter(id=song_id).first()
    # Add data to recent database
    if list(Recent.objects.filter(song=songs,user=request.user).values()):
        data = Recent.objects.filter(song=songs,user=request.user)
        data.delete()
    data = Recent(song=songs,user=request.user)
    data.save()
    return redirect('index')

@login_required(login_url='login')
def play_recent_song(request, song_id):
    songs = Song.objects.filter(id=song_id).first()
    # Add data to recent database
    if list(Recent.objects.filter(song=songs,user=request.user).values()):
        data = Recent.objects.filter(song=songs,user=request.user)
        data.delete()
    data = Recent(song=songs,user=request.user)
    data.save()
    return redirect('recent')


def all_songs(request):
    songs = Song.objects.all()

    first_time = False
    #Last played song
    if not request.user.is_anonymous:
        last_played_list = list(Recent.objects.filter(user=request.user).values('song_id').order_by('-id'))
        if last_played_list:
            last_played_id = last_played_list[0]['song_id']
            last_played_song = Song.objects.get(id=last_played_id)
        else:
            last_played_song = Song.objects.get(id=7)    
    else:
        first_time = True
        last_played_song = Song.objects.get(id=7)

    
    # apply search filters
    qs_singers = Song.objects.values_list('singer').all()
    s_list = [s.split(',') for singer in qs_singers for s in singer]
    all_singers = sorted(list(set([s.strip() for singer in s_list for s in singer])))
    qs_languages = Song.objects.values_list('language').all()
    all_languages = sorted(list(set([l.strip() for lang in qs_languages for l in lang])))
    
    if len(request.GET) > 0:
        search_query = request.GET.get('q')
        search_singer = request.GET.get('singers') or ''
        search_language = request.GET.get('languages') or ''
        filtered_songs = songs.filter(Q(name__icontains=search_query)).filter(Q(language__icontains=search_language)).filter(Q(singer__icontains=search_singer)).distinct()
        context = {
        'songs': filtered_songs,
        'last_played':last_played_song,
        'all_singers': all_singers,
        'all_languages': all_languages,
        'query_search': True,
        }
        return render(request, 'musicapp/all_songs.html', context)

    context = {
        'songs': songs,
        'last_played':last_played_song,
        'first_time':first_time,
        'all_singers': all_singers,
        'all_languages': all_languages,
        'query_search' : False,
        }
    return render(request, 'musicapp/all_songs.html', context=context)


def recent(request):
    
    #Last played song
    last_played_list = list(Recent.objects.values('song_id').order_by('-id'))
    if last_played_list:
        last_played_id = last_played_list[0]['song_id']
        last_played_song = Song.objects.get(id=last_played_id)
    else:
        last_played_song = Song.objects.get(id=7)

    #Display recent songs
    recent = list(Recent.objects.filter(user=request.user).values('song_id').order_by('-id'))
    if recent and not request.user.is_anonymous :
        recent_id = [each['song_id'] for each in recent]
        recent_songs_unsorted = Song.objects.filter(id__in=recent_id,recent__user=request.user)
        recent_songs = list()
        for id in recent_id:
            recent_songs.append(recent_songs_unsorted.get(id=id))
    else:
        recent_songs = None

    if len(request.GET) > 0:
        search_query = request.GET.get('q')
        filtered_songs = recent_songs_unsorted.filter(Q(name__icontains=search_query)).distinct()
        context = {'recent_songs': filtered_songs,'last_played':last_played_song,'query_search':True}
        return render(request, 'musicapp/recent.html', context)

    context = {'recent_songs':recent_songs,'last_played':last_played_song,'query_search':False}
    return render(request, 'musicapp/recent.html', context=context)


@login_required(login_url='login')
def detail(request, song_id):
    songs = Song.objects.filter(id=song_id).first()
    # Add data to recent database
    if list(Recent.objects.filter(song=songs,user=request.user).values()):
        data = Recent.objects.filter(song=songs,user=request.user)
        data.delete()
    data = Recent(song=songs,user=request.user)
    data.save()

    #Last played song
    last_played_list = list(Recent.objects.values('song_id').order_by('-id'))
    if last_played_list:
        last_played_id = last_played_list[0]['song_id']
        last_played_song = Song.objects.get(id=last_played_id)
    else:
        last_played_song = Song.objects.get(id=7)


    playlists = Playlist.objects.filter(user=request.user).values('playlist_name').distinct
    is_favourite = Favourite.objects.filter(user=request.user).filter(song=song_id).values('is_fav')

    if request.method == "POST":
        if 'playlist' in request.POST:
            playlist_name = request.POST["playlist"]
            q = Playlist(user=request.user, song=songs, playlist_name=playlist_name)
            q.save()
            messages.success(request, "Song added to playlist!")
        elif 'add-fav' in request.POST:
            is_fav = True
            song_img = Song.objects.filter(id=song_id)
            print(song_img.first().name)
            query = Favourite(user=request.user, song=songs, is_fav=is_fav, id=song_id)
            print(f'query: {query}')
            query.save()
            messages.success(request, "Added to favorite!")
            return redirect('detail', song_id=song_id)
        elif 'rm-fav' in request.POST:
            is_fav = True
            query = Favourite.objects.filter(user=request.user, song=songs, is_fav=is_fav)
            print(f'user: {request.user}')
            print(f'song: {songs.id} - {songs}')
            print(f'query: {query}')
            query.delete()
            messages.success(request, "Removed from favorite!")
            return redirect('detail', song_id=song_id)
    context = {'songs': songs, 'playlists': playlists, 'is_favourite': is_favourite,'last_played':last_played_song}
    return render(request, 'musicapp/detail.html', context=context)


def mymusic(request):
    return render(request, 'musicapp/mymusic.html')


def playlist(request):
    playlists = Playlist.objects.filter(user=request.user).values('playlist_name').distinct
    context = {'playlists': playlists}
    return render(request, 'musicapp/playlist.html', context=context)


def playlist_songs(request, playlist_name):
    songs = Song.objects.filter(playlist__playlist_name=playlist_name, playlist__user=request.user).distinct()
    # print("playlist nameee: ", playlist_name, request)

    if request.method == "POST":
        print('clicked', list(request.POST.keys()), request.POST.get('New_name'))
        ret_val = list(request.POST.keys())[1]
        try:
            ret_val = int(ret_val)
            song_id = ret_val
            playlist_song = Playlist.objects.filter(playlist_name=playlist_name, song__id=song_id, user=request.user)
            playlist_song.delete()
            messages.success(request, "Song removed from playlist!")
        except:
            selected_playlist = Playlist.objects.filter(playlist_name=playlist_name, user=request.user)
            if list(request.POST.keys())[-1] == 'Delete':
                selected_playlist.delete()
                messages.success(request, "Playlist deleted")
            elif list(request.POST.keys())[-1] == 'Rename':
                rename_playlist = request.POST.get('New_name')
                if rename_playlist =='':
                    messages.success(request, 'Not renamed')
                    context = {'playlist_name': playlist_name, 'songs': songs}
                    return render(request, 'musicapp/playlist_songs.html', context=context)
                Playlist.objects.filter(playlist_name=playlist_name, user=request.user).update(playlist_name = rename_playlist)
                # print(songs.all())
                songs = Song.objects.filter(playlist__playlist_name=rename_playlist, playlist__user=request.user).distinct()
                playlist_name = rename_playlist
                messages.success(request, "Renamed playlist to " + rename_playlist)
                context = {'playlist_name': rename_playlist, 'songs': songs}
                return HttpResponseRedirect("/playlist/"+rename_playlist+"/")

    context = {'playlist_name': playlist_name, 'songs': songs}

    return render(request, 'musicapp/playlist_songs.html', context=context)


def favourite(request):
    songs = Song.objects.filter(favourite__user=request.user, favourite__is_fav=True).distinct()
    print(f'songs: {songs}')
    
    if request.method == "POST":
        song_id = list(request.POST.keys())[1]
        favourite_song = Favourite.objects.filter(user=request.user, song__id=song_id, is_fav=True)
        favourite_song.delete()
        messages.success(request, "Removed from favourite!")
    context = {'songs': songs}
    return render(request, 'musicapp/favourite.html', context=context)


def liked_songs(request):
    # print("negative oneee")
    songs = list(Favourite.objects.filter(user=request.user, is_fav=True).distinct())

    liked_songs_ids = list(Favourite.objects.filter(user=request.user).values('id').order_by('-id'))

    if liked_songs_ids:
        liked_songs_ids_ids = [each['id'] for each in liked_songs_ids]
        liked_songs = list()
        for song_id in liked_songs_ids_ids:
            songg = Song.objects.filter(id=song_id).first()
            liked_songs.append(songg)

    context = {'liked_songs': liked_songs}
    return render(request, 'musicapp/liked_songs.html', context=context)

def max_played_songs(request):

    #Display recent songs
    
    if not request.user.is_anonymous :
        recent = list(Recent.objects.filter(user=request.user).values('song_id').order_by('-id'))
        recent_id = [each['song_id'] for each in recent][:5]
        recent_songs_unsorted = Song.objects.filter(id__in=recent_id,recent__user=request.user)
        recent_songs = list()
        for id in recent_id:
            recent_songs.append(recent_songs_unsorted.get(id=id))
        max_played=list(Maxplayed.objects.all())

        if len(recent)!=0:
            m=list(recent[0].values())[0]
            songs = Song.objects.filter(id=m).first()
            
            if len(max_played)==0:

                m1=Maxplayed.objects.create(user=request.user,song=songs,no_played=1)

                max_played.append(m1)
                
            
            else:
                m2=Maxplayed.objects.filter(user=request.user)
                
                flag=0
                
                for i in m2:
                    if i.song_id==m:
                        print("in if",i.song_id,m)
                        temp=i.no_played+1
                        Maxplayed.objects.filter(song_id=m).update(no_played=temp)
                        max_played.append(i)
                        flag=1
                        break
                if flag==0:
                    
                    m1=Maxplayed.objects.create(user=request.user,song=songs,no_played=1)
                    m1.save()
                    max_played.append(m1)
            #print(max_played)
            m2=list(Maxplayed.objects.filter(user=request.user))
            m2=sorted(m2,key=lambda x:x.no_played,reverse=True)
            #temp_list=[print(i.no_played) for i in m2]
            most_played=[]
            for i in m2:
                
                songg=i.song
                most_played.append(songg)
            
    context = {
        
        'max_played':most_played,
        
    }
    return render(request, 'musicapp/max_played_songs.html', context=context)


