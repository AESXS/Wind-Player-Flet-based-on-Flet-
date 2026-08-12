import flet as ft
import flet.canvas as cv
from time import time
from random import randint
from tinytag import TinyTag
from pathlib import Path
from asyncio import sleep
from json import dump,load
from module.manager import scan_files,scan_all,scan_detail,convert,unconvert
import _cffi_backend
from just_playback import Playback

#封面提取
def album_get(path):
    z=Path(path)
    tag=TinyTag.get(z,image=True)
    if tag.images.any:
        return tag.images.any.data
    else:
        return "assets/images/nothing.jpg"

#初始化
setting=[False,False,18,None,0,[],None,True,0,False,0,False,0.5]
set_path=Path("set.json")
if set_path.exists():
    with open("set.json","r",encoding="utf-8") as log:
        setting=load(log)

        
text_group_list=[["播放界面","歌曲列表","艺术家","专辑","设置","采样率&比特率","暂无歌词","动态歌词","B","删除",
                  "歌曲","搜索","简体中文","语言/language","按文件夹排序","按时间升序","按时间降序","按歌曲名升序","按歌曲名降序",
                  "播放此列表","歌词界面是否打开高斯模糊","无色歌词界面","歌词界面更加通透",
                  "载入音乐文件夹","重新扫描文件","歌词文字大小调节","恢复默认字体","重启后生效","设置歌词字体","设置全局字体",
                  "深色模式","配色方案","限制列表长度","极速模式","版本号:1.01","祈祷中!出现错误(QAQ)","液态按钮",
                  "欢迎使用Wind player! 请先完成以下设置","即刻体验","音量调节","40"],
                 ["playing","playlist","artsit","album","setting","Sampling rate&bit rate","not have lyrics","dynamic lyrics",
                  "B","delete","song","search","English","language/语言","order with folder","order with time",
                  "descending order with time","order with name","descending order with name",
                  "play this list","koss blur mode","pure lyrics interface","more transparent interface",
                  "load music folder","rescan files","set lyrics font size","reset font type","restart to use","set lyrics font","set font",
                  "dark mode","color palette","limit list length","fast mode","version:1.01","error","liquid button",
                  "welcome to use Windplayer! Please achive the trailing setting","into play","volume","40"]]

text_group=text_group_list[setting[10]]

color_group_list=[[ft.Colors.INDIGO_50,ft.Colors.INDIGO_100,ft.Colors.BLUE_50,ft.Colors.BLUE_100],
                  [ft.Colors.GREEN_50,ft.Colors.GREEN_100,ft.Colors.CYAN_50,ft.Colors.CYAN_100],
                  [ft.Colors.CYAN_50,ft.Colors.CYAN_100,ft.Colors.BLUE_50,ft.Colors.BLUE_100],
                  [ft.Colors.BLUE_50,ft.Colors.BLUE_100,ft.Colors.INDIGO_50,ft.Colors.INDIGO_100]
                  ,[ft.Colors.PINK_50,ft.Colors.PINK_100,ft.Colors.RED_50,ft.Colors.RED_100],
                  [ft.Colors.ORANGE_50,ft.Colors.ORANGE_100,ft.Colors.RED_50,ft.Colors.RED_100],
                  [ft.Colors.YELLOW_50,ft.Colors.YELLOW_100,ft.Colors.ORANGE_50,ft.Colors.ORANGE_100],]
color_group=color_group_list[setting[8]]   
cursor=0        
set_path=Path("log.json")
if set_path.exists():
    with open("log.json","r",encoding="utf-8") as log:
        file_list=load(log)
        index_list=file_list[0]
        data_list=file_list[1]
        tag_list=file_list[2]
        artist_list=file_list[3]
        album_list=file_list[4]
        time_list=file_list[5]
    music_list=tag_list[0]
    music_place=[i for i in range(0,len(data_list))]
    if setting[4]==1:
        music_place.sort(key=lambda e: time_list[e])
    elif setting[4]==2:
        music_place.sort(key=lambda e: time_list[e])
        music_place.reverse()
    elif setting[4]==3:
        music_place.sort(key=lambda e: music_list[e])
    elif setting[4]==4:
        music_place.sort(key=lambda e: music_list[e])
        music_place.reverse()
    
    music_number=music_place[0]
    exist_music=Path(data_list[music_place[0]])
    begin=True
    while not exist_music.exists():
        if cursor>=len(music_place)-1:
            begin=False
            break
        cursor+=1
        exist_music=Path(data_list[music_place[cursor]])
        music_number=music_place[cursor]
else:
    begin=False

def get_lyrics(num):
    global lyrics_list,lyrics_number
    z=Path(data_list[num])
    lyrics_number=0
    tag=TinyTag.get(z)
    if "lyrics" in tag.other:
        zeta=tag.other["lyrics"][0]
        lyrics_list=zeta.splitlines()
        lyrics_list=list(filter(lambda x:x !="" and x[1]=="0" and x[10:]!="" ,lyrics_list))
    else:
        lyrics_list=["[00:00.00]"+text_group[6]]
        
audio=Playback()
audio.set_volume(setting[12])
full=True
glob_time=0
#主程序
async def main(wind: ft.Page):
    global music_number,begin
    global w,h
    if setting[0]:
        wind.theme_mode=ft.ThemeMode.DARK
        navy.bgcolor=ft.Colors.BLACK
    else:
        wind.theme_mode=ft.ThemeMode.LIGHT
    ft.FletApp.assets_dir="assets/"
    wind.window.icon="assets/icon_windows.ico"
    wind.fonts={"rovin":setting[3],"kanit":setting[6]}
    wind.theme=ft.Theme(font_family="kanit")
    wind.window.title_bar_hidden=True
    w=wind.window.width
    h=wind.window.height
    wind.shadow=False
    wind.window.shadow=None
    wind.spacing=0
     
#初始化
    def renew():        
        global music_number
        canva.shapes=[]
        audio.load_file(data_list[music_number])
        audio.play()
        if not player.selected:
            audio.pause()
        title_update(music_number)
        photo.content=ft.Image(src=album_get(data_list[music_number])
                                     ,cache_width=1000,cache_height=1000,width=h*0.5,height=h*0.5,border_radius=22)
        dynamic_photo.src=album_get(data_list[music_number])
        dynamic_photo.update()
        if setting[0]:
            lyrics_update_dark(music_number)
        else:
            lyrics_update(music_number)
        if setting[1]:
            back.src=album_get(data_list[music_number])
            back.update()
        alltime.value=convert(int(tag_list[4][music_number])*1000)
        timer.max=int(tag_list[4][music_number])*1000
        timer.value=0
        wastetime.value="00:00"
        photo.update()
        lyrics_display.update()
        alltime.update()
        wastetime.update()

    def mini_new():
        global glob_time,music_number
        audio.load_file(data_list[music_number])
        audio.play()
        glob_time=0
        get_lyrics(music_number)
        title_small.value=music_list[music_number]
        title_small.update()

    
#完全初始化
    def allnew():
        global cursor,music_number,file_list,index_list,artist_list,data_list,tag_list,album_list,time_list,music_list,music_place,begin
        set_path=Path("log.json")
        if set_path.exists():
            with open("log.json","r",encoding="utf-8") as log:
                file_list=load(log)
                index_list=file_list[0]
                data_list=file_list[1]
                tag_list=file_list[2]
                artist_list=file_list[3]
                album_list=file_list[4]
                time_list=file_list[5]
            music_list=tag_list[0]
            music_place=[i for i in range(0,len(data_list))]    
            if setting[4]==1:
                music_place.sort(key=lambda e: time_list[e])
            elif setting[4]==2:
               music_place.sort(key=lambda e: time_list[e])
               music_place.reverse()
            elif setting[4]==3:
                music_place.sort(key=lambda e: music_list[e])
            elif setting[4]==4:
                music_place.sort(key=lambda e: music_list[e])
                music_place.reverse()    
            music_number=music_place[0]
            exist_music=Path(data_list[music_place[0]])
            while not exist_music.exists():
                cursor+=1
                exist_music=Path(data_list[music_place[cursor]])
                music_number=music_place[cursor]
            now_update(music_place)
            if setting[7]:
                item_update_fast()
                list_update_fast(music_place)
            else:
                item_update()
                list_update(music_place)
            album_update()
            artist_update()
            renew()
            begin=True
            wind.update()
#播放列表
    def now_update(place):
        global now_list
        now_list=[]
        for i in range(len(place)-1):
            now_list.append([place[i],i-1,i+1])
        now_list.append([place[-1],-2%len(place),0])
        
#导航栏
    async def scroll(e):
        await basis.jump_to_page(e.control.selected_index)
        
    navy=ft.NavigationRail(selected_index=0,height=h-90,width=80,bgcolor=color_group[0],
            destinations=[
        ft.NavigationRailDestination(icon=ft.Icons.MUSIC_NOTE, label=text_group[0]),
        ft.NavigationRailDestination(icon=ft.Icons.REORDER,label=text_group[1]),
        ft.NavigationRailDestination(icon=ft.Icons.PERSON, label=text_group[2]),
        ft.NavigationRailDestination(icon=ft.Icons.ALBUM, label=text_group[3]),
        ft.NavigationRailDestination(icon=ft.Icons.AUTO_AWESOME, label=text_group[7]),
        ft.NavigationRailDestination(icon=ft.Icons.SETTINGS, label=text_group[4]),
        ],                     
    on_change=scroll)
    
#播放页面
    #播放
    async def play(e):
        global music_number
        player.selected=not player.selected
        player.update()
        if player.selected:
            audio.resume() 
            await lyrics_sync()
        else:
            audio.pause()
    #切换
    def flow(orient):
        global music_number,cursor,full
        cursor=now_list[cursor][orient]
        music_number=now_list[cursor][0]
        wind.drawer.selected_index=cursor
        if full:
            renew()
        else:
            mini_new()
        
    #歌词
    def lyrics_update(num):
        lyrics_display.controls=[]
        get_lyrics(num)
        for i in range(0,len(lyrics_list)):
            lyrics_display.controls.append(ft.ListTile(on_click=lyrics_choice,
                                                       text_color=ft.Colors.BLACK,shape=ft.RoundedRectangleBorder(radius=20)
                                                       ,selected_color=ft.Colors.WHITE,selected_tile_color=ft.Colors.GREY,
                                                       title=ft.Text(lyrics_list[i].split("]")[1],
                                                        size=setting[2],color=ft.Colors.BLACK,font_family="rovin"),height=setting[2]*2.5,data=i))
    def lyrics_update_dark(num):
        lyrics_display.controls=[]
        get_lyrics(num)
        for i in range(0,len(lyrics_list)):
            lyrics_display.controls.append(ft.ListTile(text_color=ft.Colors.WHITE,shape=ft.RoundedRectangleBorder(radius=20)
                                                       ,selected_color=ft.Colors.WHITE,selected_tile_color=ft.Colors.GREY,
                on_click=lyrics_choice,title=ft.Text(lyrics_list[i].split("]")[1],
                                                     size=setting[2],color=ft.Colors.WHITE,font_family="rovin"),height=setting[2]*2.5,data=i))
    #歌词选中
    async def lyrics_choice(e):
        global lyrics_number,h
        z=lyrics_list[e.control.data]
        audio.seek(unconvert(z[1:9])*0.001)
        timer.value=unconvert(z[1:9])
        lyrics_display.controls[lyrics_number].selected=False
        lyrics_number=e.control.data
        lyrics_display.controls[lyrics_number].selected=True
        await lyrics_display.scroll_to(offset=max(lyrics_number*(setting[2]*2.5)-0.5*((h*0.7)),0)
                                 ,duration=100)
    #歌词同步
    async def lyrics_sync():
        global lyrics_number,lyrics_list,h,full,glob_time
        last=int(time()*1000)
        while player.selected==True:
            await sleep(0.1)
            if audio.active:
                if full:
                    if timer.value+int(time()*1000)-last<timer.max-100:
                        timer.value=timer.value+int(time()*1000)-last
                        glob_time=timer.value
                        last=int(time()*1000)
                        timer.update()
                        wastetime.update()
                else:
                    glob_time=glob_time+int(time()*1000)-last
                    last=int(time()*1000)           
            else:
                modeking()
            if full:
                if navy.selected_index==0:
                    wastetime.value=convert(int(timer.value))
                    if lyrics_number<len(lyrics_list)-1:
                        if unconvert(lyrics_list[lyrics_number+1][1:9])<timer.value:
                            if not lyrics_photo.selected:         
                                lyrics_display.controls[lyrics_number].selected=False
                                lyrics_number=min(lyrics_number+1,len(lyrics_display.controls)-1)
                                lyrics_display.controls[lyrics_number].selected=True
                                await lyrics_display.scroll_to(
                                    offset=max(lyrics_number*(setting[2]*2.5)-0.5*((h*0.7)),0),duration=300)
                                lyrics_display.update()                   
                elif navy.selected_index==4:
                    if lyrics_number<len(lyrics_list)-1:
                        if unconvert(lyrics_list[lyrics_number+1][1:9])<glob_time:
                            lyrics_display.controls[lyrics_number].selected=False
                            lyrics_number=min(lyrics_number+1,len(lyrics_display.controls)-1)
                            dynamic_update(lyrics_number)
                                              
            else:
                if lyrics_number<len(lyrics_list)-1:
                    if unconvert(lyrics_list[lyrics_number+1][1:9])<glob_time:
                        lyrics_number=min(lyrics_number+1,len(lyrics_display.controls)-1)
                        mini_lyrics.value=lyrics_list[lyrics_number].split("]")[1]
                        mini_lyrics.update()

    def dynamic_update(num):
        canva.shapes.append(cv.Text(value=lyrics_list[num][10:],x=randint(0,int(wind.window.width*0.4)),
                                    y=num%10*(wind.window.height-90)//10,
                                    style=ft.TextStyle(color=color_group[randint(0,3)],
                                                       shadow=ft.BoxShadow(spread_radius=1,blur_radius=5,color=ft.Colors.BLACK,
                                offset=ft.Offset(0, 0),),size=randint(20,int(wind.window.height//12)))))
        if len(canva.shapes)>=10:
            canva.shapes.pop(0)
        canva.update()
        canva_shape.shapes.append(cv.Circle(x=randint(0,int(wind.window.width-120)),
                                                        y=randint(0,int(wind.window.height-90)), radius=randint(0,400),
                                                        paint=ft.Paint(color=color_group[randint(0,3)]
                                                                       ,stroke_width=randint(0,20), style=ft.PaintingStyle.STROKE)))
        if len(canva_shape.shapes)>=5:
            canva_shape.shapes.pop(0)
        canva_shape.update()
      
    #进度条
    async def time_use(e):
        global lyrics_number,lyrics_list,h
        audio.seek(timer.value*0.001)
        wastetime.value=convert(int(timer.value))
        for i in range(len(lyrics_list)):
            if unconvert(lyrics_list[i][1:9])<=timer.value and not lyrics_photo.selected:
                lyrics_display.controls[lyrics_number].selected=False
                lyrics_number=i
                lyrics_display.controls[lyrics_number].selected=True
                await lyrics_display.scroll_to(offset=max(lyrics_number*(setting[2]*2.5)-0.5*((h*0.7)),0)
                                         ,duration=100)
        lyrics_display.update()
        wastetime.update()
    #模式切换
    def modeking():
        global music_number,lyrics_number
        if mode.data==0:
            flow(-1)
        elif mode.data==1:
            audio.play()
            lyrics_number=0
            timer.value=0
        else:
            audio.pause()
            player.selected=False
            timer.value=0
            player.update()
            lyrics_number=0
    def mode_change(e):
        n=[1,2,0]
        p=[ft.Icons.SKIP_NEXT,ft.Icons.REPEAT_ONE,ft.Icons.PAUSE_CIRCLE]
        e.control.data=n[e.control.data]
        e.control.icon=p[e.control.data]
        mode.update()
        
    #标签更新
    def title_update(num):
        title_group.title=ft.Text(music_list[num])
        title_banner.content.controls=[]
        title_banner.content.controls.append(ft.ListTile(leading=ft.Icon(ft.Icons.ALBUM),
                                                            title=ft.Text(tag_list[2][num]),on_click=talbum_choice))
        for i in tag_list[1][num]:
           title_banner.content.controls.append(ft.ListTile(leading=ft.Icon(ft.Icons.PERSON),
                                                               title=ft.Text(i),on_click=tartist_choice))
        title_banner.content.controls.append(ft.ListTile(title=ft.Text(text_group[5]+str([tag_list[3][num]][0]))))
        title_group.update()

    async def tartist_choice(e):
        artist_main.controls=[]  
        for i in artist_list[e.control.title.value]:
            artist_main.controls.append(ft.ListTile(title=ft.Text(music_list[i]),on_click=list_choice,data=i))            
        artist_photo.controls[0].src=album_get(data_list[i])
        artist_photo.controls[1].content.controls[0].value=e.control.title.value
        artist_page.update()
        navy.selected_index=2
        navy.update()
        title_banner.open=False
        title_banner.update()
        await basis.jump_to_page(2)
        await page3.jump_to_page(1)
        
    async def talbum_choice(e):
        album_main.controls=[]  
        for i in album_list[e.control.title.value]:
            album_main.controls.append(ft.ListTile(title=ft.Text(music_list[i]),on_click=list_choice,data=i))
        album_photo.controls[0].src=album_get(data_list[i])
        album_photo.controls[1].content.controls[0].value=e.control.title.value
        album_page.update()
        navy.selected_index=3
        navy.update()
        title_banner.open=False
        title_banner.update()
        await basis.jump_to_page(3)
        await page4.jump_to_page(1)
        
    #随机播放
    def on_shuffle():
        global music_list,now_list,cursor
        if not random_mode.selected:
            for i in range(min(100,len(now_list))):
                now_list[i].insert(0,now_list[randint(0,len(now_list)-1)][0])
        else:
            for i in range(min(100,len(now_list))):
                now_list[i].pop(0)
        if setting[7]:
            item_update_fast()
        else:
            item_update()
        cursor=0
        random_mode.selected=not random_mode.selected
        playitem.update()
        random_mode.update()
        
    #播放列表
    async def exp(e):
        await wind.show_drawer()

    def item_choice(e):
        global music_number,cursor
        cursor=e.control.selected_index
        music_number=now_list[cursor][0]
        renew()
        
    def item_update():
        global now_list
        wind.drawer.controls=[]
        for i in now_list:
           wind.drawer.controls.append(ft.NavigationDrawerDestination(label=music_list[i[0]],icon=ft.Icons.HEADPHONES))
           
    def item_update_fast():
        global now_list
        wind.drawer.controls=[]
        for i in now_list[0:min(len(now_list),100)]:
           wind.drawer.controls.append(ft.NavigationDrawerDestination(label=music_list[i[0]],icon=ft.Icons.HEADPHONES))
    #音量调节
    def volve(e):
        wind.show_dialog(volve_banner)
    def volv(e):
        global setting
        audio.set_volume(e.control.value*0.01)
        setting[12]=e.control.value*0.01
        
    volume=ft.IconButton(ft.Icons.VOLUME_UP,on_click=volve)
                        

    volve_banner=ft.AlertDialog(content=ft.ListTile(title=ft.Text(text_group[39])),actions=[ft.Slider(width=200,max=100,
                                                                   value=setting[12]*100,on_change=volv,divisions=100)])
    wind.add(volve_banner)
        

    #歌词封面转换
    def transation(e):
        e.control.selected=not e.control.selected
        if  e.control.selected:
            if wind.window.width>wind.window.height:
                play_panel.controls[0].controls.pop(-1)
            else:
                play_panel.controls[0].controls.pop(-1)
                play_panel.controls[0].controls.append(ft.Column([control3,photo,control1,control2],
                                                                 spacing=5,width=h*0.5,height=h*0.7,
                                            alignment=ft.MainAxisAlignment.CENTER))
                
        else:
            if wind.window.width>wind.window.height:
                play_panel.controls[0].controls.append(lyrics_display)
                lyrics_display.width=w-210-h*0.5
                lyrics_display.height=h*0.5+140
                lyrics_display.update()
            else:
                play_panel.controls[0].controls.pop(0)  
                play_panel.controls[0].controls.append(ft.Column([control3,lyrics_display,control1,control2]))
                lyrics_display.width=h*0.5
                lyrics_display.height=h*0.5
                lyrics_display.update()
        play_panel.update()
        
    lyrics_photo=ft.IconButton(icon=ft.Icons.COMMENT,on_click=transation,selected_icon=ft.Icons.COMMENTS_DISABLED)
    #信息弹窗
    wind.drawer=ft.NavigationDrawer(controls=[],on_change=item_choice)
    title_banner=ft.BottomSheet(content=ft.ListView())
    wind.add(title_banner)
    playitem=ft.IconButton(icon=ft.Icons.QUEUE_MUSIC,on_click=exp)
    
    
    
    #封装
    timer=ft.Slider(on_change_end=time_use)

    alltime=ft.Text()
    wastetime=ft.Text()
    
    timers=ft.Container(content=timer,width=w-400,height=40)
    
    player=ft.IconButton(on_click=play,icon=ft.Icons.RADIO_BUTTON_UNCHECKED,
                         selected_icon=ft.Icons.CHECK_BOX_OUTLINE_BLANK,selected=False,width=50,height=50)
    
    upper=ft.IconButton(on_click=lambda e: flow(-2),icon=ft.Icons.CHEVRON_LEFT,width=50,height=50)
    
    downer=ft.IconButton(on_click=lambda e: flow(-1),icon=ft.Icons.CHEVRON_RIGHT,width=50,height=50)

    photo=ft.AnimatedSwitcher(content=ft.Image(src=""),transition=ft.AnimatedSwitcherTransition.FADE,
        duration=200,reverse_duration=100)
    
    back=ft.Image(border_radius=22,filter_quality=ft.FilterQuality.LOW,src="")
    

    title_group=ft.ListTile(title=ft.Text(),width=h*0.5,height=40,on_click=lambda e:wind.show_dialog(title_banner))
    
    random_mode=ft.IconButton(icon=ft.Icons.SHUFFLE,selected_icon=ft.Icons.SHUFFLE_ON,on_click=lambda e:on_shuffle())
    mode=ft.IconButton(data=0,icon=ft.Icons.SKIP_NEXT,on_click=mode_change)
    
    lyrics_display=ft.ListView(width=w-210-h*0.5,height=h*0.5+140,scroll=ft.ScrollMode.HIDDEN)

    control1=ft.Container(content=ft.Row([mode,random_mode,playitem,lyrics_photo,volume],
                                         alignment=ft.MainAxisAlignment.CENTER),
                          border_radius=22,width=h*0.5,
                               blend_mode=ft.BlendMode.MODULATE,bgcolor=ft.Colors.GREY_100)
    
    control2=ft.Container(content=ft.Row([upper,player,downer],alignment=ft.MainAxisAlignment.CENTER),
                          border_radius=22,width=h*0.5,
                               blend_mode=ft.BlendMode.MODULATE,bgcolor=ft.Colors.GREY_100)
    
    control3=ft.Container(content=ft.Row([title_group],alignment=ft.MainAxisAlignment.CENTER,width=h*0.5,height=40),
                          border_radius=22)
    
    koss=ft.Container(border_radius=22,blend_mode=ft.BlendMode.MODULATE,
                      bgcolor=color_group[0],height=h-90,width=w-140)

    play_panel=ft.Column([ft.Row([ft.Column([control3,photo,control1,control2],spacing=5,
                            alignment=ft.MainAxisAlignment.CENTER),lyrics_display],alignment=ft.MainAxisAlignment.CENTER),
                          ft.Row([wastetime,timers,alltime],alignment=ft.MainAxisAlignment.CENTER)])
    
    goss=ft.AnimatedSwitcher(content=ft.Stack([koss,play_panel]),height=h-90)
    
    if setting[1]:
        goss.content.controls.insert(0,back)
        koss.blur=ft.Blur(100,100, ft.BlurTileMode.CLAMP)
    if setting[9]:
        koss.bgcolor=ft.Colors.GREY_50
        koss.blur=ft.Blur(200,100, ft.BlurTileMode.REPEATED)
    if setting[11]:
        control1.blend_mode=ft.BlendMode.OVERLAY
        control2.blend_mode=ft.BlendMode.OVERLAY
        
       
#列表页面
    def list_choice(e):
        global music_number,cursor,now_list
        music_number=e.control.data
        renew()
        
    def delete_true(e):
        global music_place,delete_bool
        Path.unlink(Path(delete_banner.content.title.value))
        delete_banner.open=False
        delete_banner.update()
        
    def music_delete(e):
        wind.show_dialog(delete_banner)

    delete_banner=ft.AlertDialog(content=ft.ListTile(title=ft.Text("")),actions=[
                                                      ft.Container(border_radius=22,content=ft.ListTile(title=text_group[9],
                                                                                       on_click=delete_true,bgcolor=ft.Colors.RED_100))])
    wind.add(delete_banner)
        
    def list_update(place):
        playlist.controls=[]
        for i in place:
            playlist.controls.append(ft.ListTile(data=i,width=w-140,height=50,on_click=list_choice,title=ft.Text(music_list[i]),
                                                 trailing=ft.PopupMenuButton(content=ft.Icon(ft.Icons.MENU),items=[
                                                     ft.PopupMenuItem(content=ft.Row([ft.Icon(ft.Icons.DELETE),ft.Text(text_group[9])]),
                                                                 on_click=music_delete,data=i)])))
    def list_update_fast(place):
        playlist.controls=[]
        for i in place[0:min(len(place),100)]:
            playlist.controls.append(ft.ListTile(data=i,width=w-140,height=50,on_click=list_choice,title=ft.Text(music_list[i]),
                                                 trailing=ft.PopupMenuButton(content=ft.Icon(ft.Icons.MENU),items=[
                                                     ft.PopupMenuItem(content=ft.Row([ft.Icon(ft.Icons.DELETE),ft.Text(text_group[9])]),
                                                                      on_click=music_delete,data=i)])))
    #文件夹播放
            
    folder_edge=ft.Container(blend_mode=ft.BlendMode.MODULATE,
                       content=ft.PopupMenuButton(content=ft.Icon(ft.Icons.FOLDER_OPEN),items=[]),
                      bgcolor=color_group[1],border_radius=15,width=54,height=44)
    
    def folder_update():
        folder_edge.content.items=[]
        for i in range(len(index_list)):
            folder_edge.content.items.append(ft.PopupMenuItem(content=ft.Text(index_list[i][0]),on_click=folder_play,data=i))

    def folder_play(e):
        global music_number,now_list,cursor
        now_update([i for i in range(index_list[e.control.data][1],index_list[e.control.data][2])])
        if setting[7]:
            item_update_fast()
        else:
            item_update()
        cursor=0
        music_number=now_list[cursor][0]
        random_mode.selected=False
        renew()

    
        
    #播放全部
    def all_play(e):
        global now_list,cursor,music_number
        now_update(music_place)
        if setting[7]:
            item_update_fast()
        else:
            item_update()
        cursor=0
        music_number=now_list[cursor][0]
        renew()

        
    sword=ft.Container(blend_mode=ft.BlendMode.MODULATE,
                       content=ft.Row([ft.ListTile(title=ft.Icon(icon=ft.Icons.AUDIOTRACK),on_click=all_play,width=60)],
                                      alignment=ft.MainAxisAlignment.CENTER),
                     border_radius=15,width=60,height=44,
                               bgcolor=color_group[2])

    #歌曲搜索
    async def search_choice(e):
        global music_number
        music_number=e.control.data
        await search_button.close_view()
        renew()
        
    async def search(e):
        global music_list
        e.control.controls=[]
        e.control.controls.append(ft.ListTile(title=(ft.Text(text_group[10])),height=40,bgcolor=color_group[1]))
        for i in range(len(data_list)):
            if e.data.lower() in music_list[i].lower():
                e.control.controls.append(ft.ListTile(on_click=search_choice,title=(ft.Text(music_list[i]))
                                                      ,height=40,data=i))
        e.control.controls.append(ft.ListTile(title=(ft.Text(text_group[2])),height=40,bgcolor=color_group[1]))
        for i in artist_list:
            if e.data.lower() in i.lower():
                e.control.controls.append(ft.ListTile(title=(ft.Text(i)),height=30,
                                                   on_click=search_artist_choice))
        e.control.controls.append(ft.ListTile(title=(ft.Text(text_group[3])),height=40,bgcolor=color_group[1]))
        for i in album_list:
            if e.data.lower() in i.lower():
                e.control.controls.append(ft.ListTile(title=(ft.Text(i)),height=30,
                                                   on_click=search_album_choice))
        await e.control.open_view()

    search_button=ft.SearchBar(on_submit=search,height=40,width=300,full_screen=True,bar_hint_text=text_group[11])
    
    #搜索跳转页面
    async def search_artist_choice(e):
        await search_button.close_view()
        artist_main.controls=[]  
        for i in artist_list[e.control.title.value]:
            artist_main.controls.append(ft.ListTile(title=ft.Text(music_list[i]),on_click=list_choice,data=i))
        artist_photo.controls[0].src=album_get(data_list[i])
        artist_photo.controls[1].content.controls[0].value=e.control.title.value
        artist_page.update()
        navy.selected_index=2
        navy.update()
        await basis.jump_to_page(2)
        await page3.jump_to_page(1)
        
    async def search_album_choice(e):
        await search_button.close_view()
        album_main.controls=[]  
        for i in album_list[e.control.title.value]:
            album_main.controls.append(ft.ListTile(title=ft.Text(music_list[i]),on_click=list_choice,data=i))
        album_photo.controls[0].src=album_get(data_list[i])
        album_photo.controls[1].content.controls[0].value=e.control.title.value
        album_page.update()
        navy.selected_index=3
        navy.update()
        await basis.jump_to_page(3)
        await page4.jump_to_page(1)


    #排序方法
    def order(a):
        global music_place,music_list,setting,now_list
        if a==0:
            playlist.controls.sort(key=lambda e: e.data)
        elif a==1:
            playlist.controls.sort(key=lambda e: time_list[e.data])
        elif a==2:
            playlist.controls.sort(key=lambda e: time_list[e.data])
            music_place.sort(key=lambda e: time_list[e])
            playlist.controls.reverse()
            music_place.reverse()
        elif a==3:
            music_place.sort(key=lambda e: music_list[e])
            playlist.controls.sort(key=lambda e: music_list[e.data])
        elif a==4:
            playlist.controls.sort(key=lambda e: music_list[e.data])
            playlist.controls.reverse()
            music_place.sort(key=lambda e: music_list[e])
            music_place.reverse()
        now_update(music_place)
        if setting[7]:
                item_update_fast()
        else:
            item_update()
        setting[4]=a
        
    seque=ft.Container(blend_mode=ft.BlendMode.MODULATE,
                       content=ft.PopupMenuButton(content=ft.Icon(ft.Icons.LIST),items=[
        ft.PopupMenuItem(content=ft.Text(text_group[14]),on_click=lambda e:order(0)),
            ft.PopupMenuItem(content=ft.Text(text_group[15]),on_click=lambda e:order(1)),
            ft.PopupMenuItem(content=ft.Text(text_group[16]),on_click=lambda e:order(2)),
        ft.PopupMenuItem(content=ft.Text(text_group[17]),on_click=lambda e:order(3)),
        ft.PopupMenuItem(content=ft.Text(text_group[18]),on_click=lambda e:order(4))]),
                      bgcolor=color_group[3],border_radius=15,width=54,height=44)
    
        
    playlist=ft.ListView(height=h-144,width=w-120,spacing=5,cache_extent=h-144)
    
    list_panel=ft.Column([ft.Container(blend_mode=ft.BlendMode.MODULATE,
                                       content=ft.Row([search_button,sword,seque,folder_edge]),
                                       width=w-120,bgcolor=color_group[0],height=44
                                       ,border_radius=30)
                          ,ft.Container(blend_mode=ft.BlendMode.MODULATE,
                                        content=playlist,bgcolor=color_group[0],border_radius=22)])

#艺术家&专辑页面
    
    async def artist_choice(e):
        artist_main.controls=[]  
        for i in artist_list[e.control.title.value]:
            artist_main.controls.append(ft.ListTile(title=ft.Text(music_list[i]),on_click=list_choice,data=i))
            
        artist_photo.controls[0].src=album_get(data_list[i])
        artist_photo.controls[1].content.controls[0].value=e.control.title.value
        artist_page.update()
        await page3.jump_to_page(1)
        
    async def album_choice(e):
        album_main.controls=[]  
        for i in album_list[e.control.title.value]:
            album_main.controls.append(ft.ListTile(title=ft.Text(music_list[i]),on_click=list_choice,data=i))
        album_photo.controls[0].src=album_get(data_list[i])
        album_photo.controls[1].content.controls[0].value=e.control.title.value
        album_page.update()
        await page4.jump_to_page(1)

    def artist_play(e):
        global now_list,cursor,music_number
        now_update(artist_list[artist_photo.controls[1].content.controls[0].value])
        if setting[7]:
            item_update_fast()
        else:
            item_update()
        cursor=0
        music_number=now_list[cursor][0]
        renew()

    async def artist_back(e):
        await page3.jump_to_page(0)
        
    def artist_update():
        artist_grid.controls=[]
        for i in artist_list:
            artist_grid.controls.append(ft.ListTile(title=ft.Text(i),on_click=artist_choice))
            
    artist_grid=ft.ListView(width=w-120,height=h-144,spacing=5,cache_extent=h-90)
    
    artist_panel=ft.Column([ft.Container(blend_mode=ft.BlendMode.MODULATE,
                                         content=ft.Row([ft.ListTile(leading=ft.Icon(icon=ft.Icons.PERSON),title=ft.Text(text_group[2]))]),
                                       width=w-120,bgcolor=color_group[1],height=44
                                       ,border_radius=30)
        ,ft.Container(blend_mode=ft.BlendMode.MODULATE,
                      content=artist_grid,bgcolor=color_group[0],border_radius=22,width=w-120)])
    
    def album_update():
        album_grid.controls=[]
        for i in album_list:
            album_grid.controls.append(ft.ListTile(title=ft.Text(i),on_click=album_choice))
            
    album_grid=ft.ListView(width=w-120,height=h-144,spacing=5,cache_extent=h-90)

    album_panel=ft.Column([
        ft.Container(blend_mode=ft.BlendMode.MODULATE,
                     content=ft.Row([ft.ListTile(leading=ft.Icon(icon=ft.Icons.ALBUM),title=ft.Text(text_group[3]))]),
                                       width=w-120,bgcolor=color_group[1],height=44
                                       ,border_radius=30),
                           ft.Container(blend_mode=ft.BlendMode.MODULATE,content=album_grid,
                                        bgcolor=color_group[0],border_radius=22,width=w-120)])
    
    artist_main=ft.ListView(controls=[],height=h-90,width=w-h*0.6-130)
    artist_photo=ft.Column([
        ft.Image(src="",cache_width=1000,cache_height=1000,width=h*0.6,height=h*0.6,border_radius=22),
        ft.Container(blend_mode=ft.BlendMode.MODULATE,content=ft.Row([ft.Text()],alignment=ft.MainAxisAlignment.CENTER),
                     border_radius=22,width=h*0.6,height=50,bgcolor=color_group[1]),
        ft.Container(blend_mode=ft.BlendMode.MODULATE,content=ft.Row([ft.ListTile(height=50,width=h*0.3
                                                                     ,title=ft.Icon(icon=ft.Icons.CHEVRON_LEFT),on_click=artist_back),
        ft.ListTile(height=50,width=h*0.3,title=ft.Text(text_group[19]),on_click=artist_play,bgcolor=color_group[3])],
                                    alignment=ft.MainAxisAlignment.CENTER,spacing=0),border_radius=22,width=h*0.6,height=50,
                               bgcolor=color_group[2]),
        ],alignment=ft.MainAxisAlignment.START)
    
    def album_play(e):
        global now_list,cursor,music_number
        now_update(album_list[album_photo.controls[1].content.controls[0].value])
        if setting[7]:
            item_update_fast()
        else:
            item_update()
        cursor=0
        music_number=now_list[cursor][0]
        renew()

    async def album_back(e):
        await page4.jump_to_page(0)


    album_main=ft.ListView(controls=[],height=h-90,width=w-h*0.6-130)

    album_photo=ft.Column([
        ft.Image(src="",cache_width=1000,cache_height=1000,width=h*0.6,height=h*0.6,border_radius=22),
        
        ft.Container(blend_mode=ft.BlendMode.MODULATE,content=ft.Row([ft.Text()],alignment=ft.MainAxisAlignment.CENTER),
                     border_radius=22,width=h*0.6,height=50,
                               bgcolor=color_group[1]),
        ft.Container(blend_mode=ft.BlendMode.MODULATE,
                     content=ft.Row([ft.ListTile(height=50,width=h*0.3,title=ft.Icon(icon=ft.Icons.CHEVRON_LEFT),
                                                                     on_click=album_back),
                                     ft.ListTile(height=50,width=h*0.3,title=ft.Text(text_group[19]),on_click=album_play,
                                                 bgcolor=color_group[3])],
                                    alignment=ft.MainAxisAlignment.CENTER),border_radius=22,width=h*0.6,height=50,
                               bgcolor=color_group[2])],alignment=ft.MainAxisAlignment.START)

    artist_page=ft.Column([ft.Container(blend_mode=ft.BlendMode.MODULATE,content=ft.Row([artist_photo,artist_main]),
                             bgcolor=color_group[0],border_radius=22,width=w-120,height=h-90)])

    album_page=ft.Column([ft.Container(blend_mode=ft.BlendMode.MODULATE,content=ft.Row([album_photo,album_main]),
                             bgcolor=color_group[0],border_radius=22,width=w-120,height=h-90)])


#设置页面
    #文件夹管理
    warning=ft.BottomSheet(content=ft.ListTile(title=ft.Text(value=text_group[35]),bgcolor=ft.Colors.RED_100))
    wind.add(warning)
    async def load_file(e):
        tar=await ft.FilePicker().get_directory_path()
        scanner.subtitle.value=None
        scanner.update()
        if tar:
            target_list=scan_files(tar)         
            zeta=scan_all(target_list)
            if zeta!=None:
                with open("log.json","w",encoding="utf-8") as file:
                    dump(zeta,file)
                file.close()
                allnew()
                scanner.subtitle.value=1
                scanner.update()
            else:
                wind.show_dialog(warning)
                scanner.subtitle.value=0
                scanner.update()
                
   
    #高斯模糊     
    def gkos(e):
        global setting
        if e.control.value:
            back.src=photo.content.src
            goss.content.controls.insert(0,ft.Row([back]))
            if setting[9]:
                koss.blur=ft.Blur(200,100, ft.BlurTileMode.REPEATED)
            else:
                koss.blur=ft.Blur(100,100, ft.BlurTileMode.CLAMP)
        else:
            if len(goss.content.controls)>=2:
                goss.content.controls.pop(0)
                koss.blur=None
        setting[1]=e.control.value
        goss.update()

    def dkos(e):
        global setting
        if e.control.value:
            koss.bgcolor=ft.Colors.GREY_50
            if setting[1]:
                koss.blur=ft.Blur(200,100, ft.BlurTileMode.REPEATED)
        else:
            koss.bgcolor=color_group[setting[8]]
            if setting[1]:
                koss.blur=ft.Blur(100,100, ft.BlurTileMode.CLAMP)
            
        setting[9]=e.control.value
        koss.update()
        
    
    koss_open=ft.ListTile(leading=ft.Icon(ft.Icons.BLUR_ON)
                          ,title=ft.Text(text_group[20]),trailing=ft.Switch(value=setting[1],on_change=gkos))
    
    koss_deep=ft.ListTile(leading=ft.Icon(ft.Icons.JOIN_LEFT)
                          ,title=ft.Text(text_group[21]),subtitle=ft.Text(text_group[22]),
                          trailing=ft.Switch(value=setting[9],on_change=dkos))
    
    scanner=ft.ListTile(leading=ft.Icon(ft.Icons.FOLDER),
                        title=ft.Text(text_group[23]),on_click=load_file,subtitle=ft.ProgressBar(value=0))
    #液态按钮
    def liquid_on(e):
        global setting
        if e.control.value:
            control1.blend_mode=ft.BlendMode.OVERLAY
            control2.blend_mode=ft.BlendMode.OVERLAY
        else:
            control1.blend_mode=ft.BlendMode.MODULATE
            control2.blend_mode=ft.BlendMode.MODULATE            
        setting[11]=e.control.value

    liquid_open=ft.ListTile(leading=ft.Icon(ft.Icons.MOTION_PHOTOS_ON)
                          ,title=ft.Text(text_group[36]),trailing=ft.Switch(value=setting[11],on_change=liquid_on))
    #文件夹重载
    def rescan(e):
        wind.window.progress_bar=0.5
        wind.update()
        if begin:
            target_list=[Path(i[0]) for i in index_list]
            recheck.subtitle.value=None
            recheck.update()
            zeta=scan_all(target_list)    
            if zeta!=None:
                with open("log.json","w",encoding="utf-8") as file:
                    dump(zeta,file)
                    file.close()
                allnew()
                recheck.subtitle.value=1
                recheck.update()
            else:
                wind.show_dialog(warning)
                scanner.subtitle.value=0
                scanner.update()
        else:
            wind.show_dialog(warning)
        
    recheck=ft.ListTile(leading=ft.Icon(ft.Icons.REFRESH),
                        title=ft.Text(text_group[24]),on_click=rescan,subtitle=ft.ProgressBar(value=0))
    #语言更换
    def language_trans(e):
        global setting,text_group
        if e.control.value=="简体中文":
            setting[10]=0
        elif e.control.value=="English":
            setting[10]=1
        text_group=text_group_list[setting[10]]
        text_update()
        
    language_change=ft.ListTile(leading=ft.Icon(ft.Icons.LANGUAGE),title=ft.Text(text_group[13]),
                trailing=ft.Dropdown(width=150,value=text_group[12],border_radius=22
                                     ,options=[ft.DropdownOption(key="简体中文", text="简体中文"),
             ft.DropdownOption(key="English", text="English")],on_select=language_trans))

    
    
    #字体大小调节
    def font_size(a):
        global setting,music_number,begin
        if a==0:
            setting[2]-=1
        else:
            setting[2]+=1
        fonter.title.controls[2].value=setting[2]
        if begin:
            lyrics_update(music_number)
        fonter.update()
        
    fonter=ft.ListTile(leading=ft.Icon(ft.Icons.FORMAT_SIZE),title=ft.Row([ft.Text(text_group[25])
                                      ,ft.IconButton(icon=ft.Icons.CHEVRON_LEFT,on_click=lambda e: font_size(0)),
                            ft.Text(value=str(setting[2])),ft.IconButton(icon=ft.Icons.CHEVRON_RIGHT,on_click=lambda e: font_size(1))]))
    #字体更换
    def font_trans(e):
        global setting,music_number
        setting[3]=None
        setting[6]=None
        wind.fonts={"kevin":None,"Kanit":None}
        wind.update()
        
    re_font=ft.ListTile(leading=ft.Icon(ft.Icons.FORMAT_CLEAR),
                        title=ft.Text(text_group[26]),on_click=font_trans,subtitle=ft.Text(text_group[27]))
    
    async def font_lyrics(e):
        global setting,music_number
        var=await ft.FilePicker().pick_files(file_type=ft.FilePickerFileType.CUSTOM,allowed_extensions=["ttf","TTF","otf"])
        if var!=[]:
            setting[3]=var[0].path
            wind.fonts={"rovin":setting[3],"Kanit":setting[6]}
            wind.update()
        
    lyrics_font=font_tran=ft.ListTile(title=ft.Text(text_group[28]),leading=ft.Icon(ft.Icons.SUBJECT),
                            on_click=font_lyrics)
    
    async def font_change(e):
        global setting,music_number
        var=await ft.FilePicker().pick_files(file_type=ft.FilePickerFileType.CUSTOM,allowed_extensions=["ttf","TTF","otf"])
        if var!=[]:
            setting[6]=var[0].path
            wind.fonts={"rovin":setting[3],"Kanit":setting[6]}
            wind.theme=ft.Theme(font_family="kanit")
            lyrics_update(music_number)
            wind.update()
        

    font_tran=ft.ListTile(title=ft.Text(text_group[29]),leading=ft.Icon(ft.Icons.FONT_DOWNLOAD),
                            on_click=font_change)
    #黑色模式
    def dark(e):
        global setting,music_number,begin
        if e.control.value:
            wind.theme_mode=ft.ThemeMode.DARK
            navy.bgcolor=ft.Colors.BLACK
            if begin:
                lyrics_update_dark(music_number)
        else:
            wind.theme_mode=ft.ThemeMode.LIGHT
            navy.bgcolor=color_group[0]
            if begin:
                lyrics_update(music_number)
        setting[0]=e.control.value
        wind.update()
        
    darkness=ft.ListTile(leading=ft.Icon(ft.Icons.DARK_MODE),title=ft.Text(text_group[30]),trailing=ft.Switch(value=setting[0],on_change=dark))

    #配色调节
    def color_change(e):
        global setting,color_group
        color_group=color_group_list[e.control.data]
        setting[8]=e.control.data
        color_update()
        
    colorer=ft.ListTile(leading=ft.Icon(ft.Icons.COLOR_LENS),title=ft.Row([ft.Text(text_group[31]),
                                                                           ft.IconButton(data=0,on_click=color_change,
                                                          icon=ft.Icons.COLORIZE,bgcolor=ft.Colors.INDIGO_100),
                                                      ft.IconButton(data=1,on_click=color_change,
                                                          icon=ft.Icons.COLORIZE,bgcolor=ft.Colors.GREEN_100),
                                                      ft.IconButton(data=2,on_click=color_change,
                                                          icon=ft.Icons.COLORIZE,bgcolor=ft.Colors.CYAN_100,),
                                                      ft.IconButton(data=3,on_click=color_change,
                                                          icon=ft.Icons.COLORIZE,bgcolor=ft.Colors.BLUE_100,),
                                                      ft.IconButton(data=4,on_click=color_change,
                                                          icon=ft.Icons.COLORIZE,bgcolor=ft.Colors.PINK_100),
                                                      ft.IconButton(data=5,on_click=color_change,
                                                          icon=ft.Icons.COLORIZE,bgcolor=ft.Colors.ORANGE_100,),
                                                                           ft.IconButton(data=6,on_click=color_change,
                                                          icon=ft.Icons.COLORIZE,bgcolor=ft.Colors.YELLOW_100),]))
    #极速模式
    def faster(e):
        global setting,music_place
        setting[7]=e.control.value
        if begin:
            if setting[7]:
                list_update_fast(music_place)
            else:
                list_update(music_place)
    fast_mode=ft.ListTile(leading=ft.Icon(ft.Icons.BOLT),subtitle=ft.Text(text_group[32]),
                                        title=ft.Text(text_group[33]),trailing=ft.Switch(value=setting[7],on_change=faster))

    
    #版本号
    edition=ft.ListTile(leading=ft.Icon(ft.Icons.LAPTOP),title=ft.Text(text_group[34]))
    

    setting_panel=ft.Column([ft.Container(blend_mode=ft.BlendMode.MODULATE,
                                          content=ft.ListView([ft.ListTile(title=ft.Text("Wind Player"),
                                                                         leading=ft.Image(src="assets/icon_windows.ico",height=30)
                                                                         ),scanner,recheck,language_change,darkness
                                                             ,koss_open,koss_deep,liquid_open,fast_mode,
                                                             fonter,font_tran,lyrics_font,re_font,
                                                               colorer,edition],scroll=ft.ScrollMode.HIDDEN),
                             bgcolor=color_group[0],border_radius=22,width=w-120,height=h-90)])
    #初始化界面
    async def new_load_file(e):
        global begin
        tar=await ft.FilePicker().get_directory_path()
        new_scanner.subtitle.value=None
        new_scanner.update()
        if tar:
            target_list=scan_files(tar)         
            zeta=scan_all(target_list)
            if zeta!=None:
                with open("log.json","w",encoding="utf-8") as file:
                    dump(zeta,file)
                file.close()
                begin=True
                allnew()
                initial_play.content.bgcolor=color_group[1]
                initial_play.update()
                new_scanner.subtitle.value=1
                new_scanner.update()
            else:
                wind.show_dialog(warning)
                new_scanner.subtitle.value=0
                new_scanner.update()
                
    new_scanner=ft.ListTile(leading=ft.Icon(ft.Icons.FOLDER),
                        title=ft.Text(text_group[23]),on_click=new_load_file,subtitle=ft.ProgressBar(value=0))
    
    welcomer=ft.ListTile(title=ft.Text(text_group[37]),leading=ft.Icon(ft.Icons.CELEBRATION),bgcolor=color_group[3])

    language_change_new=ft.ListTile(leading=ft.Icon(ft.Icons.LANGUAGE),title=ft.Text(text_group[13]),
                trailing=ft.Dropdown(width=150,value=text_group[12],border_radius=22
                                     ,options=[ft.DropdownOption(key="简体中文", text="简体中文"),
             ft.DropdownOption(key="English", text="English")],on_select=language_trans))
    
    async def new_play(e):
        global begin
        if begin:
            navy.destinations=[
                       ft.NavigationRailDestination(icon=ft.Icons.MUSIC_NOTE, label=text_group[0]),
                       ft.NavigationRailDestination(icon=ft.Icons.REORDER,label=text_group[1]),
                       ft.NavigationRailDestination(icon=ft.Icons.PERSON, label=text_group[2]),
                       ft.NavigationRailDestination(icon=ft.Icons.ALBUM, label=text_group[3]),
                       ft.NavigationRailDestination(icon=ft.Icons.SETTINGS, label=text_group[4])]
            navy.on_change=scroll
            navy.update()
            await basis.jump_to_page(0)
        else:
            wind.show_dialog(warning)
        

    initial_play=ft.Container(content=ft.ListTile(on_click=new_play,title=ft.Text(text_group[38]),
                                                  leading=ft.Icon(ft.Icons.LOCAL_CAFE)),border_radius=22,bgcolor=color_group[0])
    
    initial_panel=ft.Column([ft.Container(content=ft.ListView([welcomer,new_scanner,language_change_new,initial_play],
                                                              spacing=10),blend_mode=ft.BlendMode.MODULATE,
                                          bgcolor=color_group[0],border_radius=22,width=w-120,height=h-90)])
    
    

#三键导航
    def mini(e):
        wind.window.minimized=True
        wind.update()
        
    def maxc(e):
        e.control.selected=not e.control.selected
        if e.control.selected:
            wind.window.maximized=True 
        else:
            wind.window.maximized=False
        wind.update()
        
    async def close(e): 
        with open("set.json","w",encoding="utf-8") as file:
            dump(setting,file)
        audio.stop()
        await wind.window.close()
        quit()
          
    xiao=ft.IconButton(icon=ft.Icons.RADIO_BUTTON_OFF,on_click=mini)
    qu=ft.IconButton(icon=ft.Icons.CLOSE,on_click=close)
    da=ft.IconButton(icon=ft.Icons.CROP_DIN,selected_icon="CROP_FREE",on_click=maxc)
#快捷键
    async def on_key(e):
        global music_number
        if navy.selected_index==0 or navy.selected_index==4:
            if e.key==" ":
                await play(e)
            elif e.key=="Page Down":
                flow(-1)
            elif e.key=="Page Up":
                flow(-2)
            elif e.key=="Q":
                on_shuffle()
            
    wind.on_keyboard_event=on_key
    
#小窗模式
    def open_window(e):
        global full,setting,glob_time,begin
        if begin:
            glob_time=timer.value
            full=False
            wind.clean()
            wind.window.width=500
            wind.window.height=100
            wind.add(ft.WindowDragArea(ft.ListView([small_line,mini_lyrics]),maximizable=False))
            title_small.value=music_list[music_number]
            title_small.update()
            wind.window.always_on_top=True
            wind.update()
        

    def del_small(e):
        global full,music_number,glob_time
        wind.clean()
        wind.window.width=1280
        wind.window.height=720
        wind.window.always_on_top=False
        wind.add(basic)
        wind.update()
        if not player.selected:
            audio.pause()
        title_update(music_number)
        photo.content=ft.Image(src=album_get(data_list[music_number])
                                     ,cache_width=1000,cache_height=1000,width=h*0.5,height=h*0.5,border_radius=22)
        if setting[0]:
            lyrics_update_dark(music_number)
        else:
            lyrics_update(music_number)
        if setting[1]:
            back.src=album_get(data_list[music_number])
            back.update()
        alltime.value=convert(int(tag_list[4][music_number])*1000)
        timer.max=int(tag_list[4][music_number])*1000
        timer.value=glob_time
        photo.update()
        lyrics_display.update()
        alltime.update()
        full=True
        
        
    small_window=ft.IconButton(icon=ft.Icons.ARROW_DROP_DOWN,on_click=open_window)
    title_small=ft.Text(width=200)
    small_back=ft.IconButton(icon=ft.Icons.ARROW_DROP_UP,on_click=del_small)
    mini_lyrics=ft.Text(value="loading",width=480,size=20)
        
    
#功能栏
    task_line=ft.Container(blend_mode=ft.BlendMode.MODULATE,
                           content=ft.Row([small_window,xiao,da,qu],alignment=ft.MainAxisAlignment.END,height=40,width=w-30),
                           bgcolor=color_group[0],border_radius=22)
    
    area=ft.WindowDragArea(task_line,maximizable=False)

    small_line=ft.Container(content=ft.Row([upper,player,downer,title_small,small_back,qu],
                                           alignment=ft.MainAxisAlignment.END,height=40,width=w-30),)
#动态歌词
    canva=cv.Canvas(width=w-120,height=h-90,shapes=[])
    canva_shape=cv.Canvas(width=w-120,height=h-90,shapes=[])
    canbir=ft.Container(content=canva_shape,width=w-120,height=h-90,border_radius=22,
                        blend_mode=ft.BlendMode.MODULATE,blur=ft.Blur(100,100, ft.BlurTileMode.REPEATED))
    dynamic_photo=ft.Image(filter_quality=ft.FilterQuality.LOW,src="",height=wind.window.height-90)
    
    
#封装
    page1=ft.ListView(controls=[goss])
    page2=ft.ListView(controls=[list_panel])
    page3=ft.PageView([artist_panel,artist_page],selected_index=0,horizontal=False)
    page4=ft.PageView([album_panel,album_page],selected_index=0,horizontal=False)
    page5=ft.ListView(ft.Stack([ft.Row([dynamic_photo],alignment=ft.MainAxisAlignment.CENTER),canbir,canva]))
    page6=ft.ListView(controls=[setting_panel])
    
    
    

    basis=ft.PageView([page1,page2,page3,page4,page5,page6,initial_panel],
                      width=wind.window.width-80,horizontal=True,selected_index=0)
    
    basic=ft.Column([area,ft.Row(controls=[ft.Column([ft.Container(content=navy,border_radius=20)],
                                        alignment=ft.MainAxisAlignment.START),
                              basis],width=wind.window.width,height=wind.window.height)])
    wind.add(basic)

    def must(e):
        with open("set.json","w",encoding="utf-8") as file:
            dump(setting,file)
        audio.stop()
        set_path=Path("log.json")
        if not begin and set_path.exists():
            Path.unlink(set_path)
        quit()
        
    wind.on_close=must

    def color_update():
        navy.bgcolor=color_group[0]
        sword.bgcolor=color_group[2]
        seque.bgcolor=color_group[3]
        list_panel.controls[0].bgcolor=color_group[0]
        list_panel.controls[1].bgcolor=color_group[0]
        artist_panel.controls[0].bgcolor=color_group[1]
        artist_panel.controls[1].bgcolor=color_group[0]
        album_panel.controls[0].bgcolor=color_group[1]
        album_panel.controls[1].bgcolor=color_group[0]
        artist_photo.controls[1].bgcolor=color_group[1]
        artist_photo.controls[2].bgcolor=color_group[2]
        artist_photo.controls[2].content.controls[1].bgcolor=color_group[3]
        album_photo.controls[1].bgcolor=color_group[1]
        album_photo.controls[2].content.controls[1].bgcolor=color_group[3]
        album_photo.controls[2].bgcolor=color_group[3]
        artist_page.controls[0].bgcolor=color_group[0]
        album_page.controls[0].bgcolor=color_group[0]
        setting_panel.controls[0].bgcolor=color_group[0]
        folder_edge.bgcolor=color_group[1]
        task_line.bgcolor=color_group[0]
        if not setting[9]:
            koss.bgcolor=color_group[0]
        wind.update()
        
    def text_update():
        if not begin:
            navy.destinations[0].label=text_group[0]
            navy.destinations[1].label=text_group[1]
            navy.destinations[2].label=text_group[2]
            navy.destinations[3].label=text_group[3]
            navy.destinations[4].label=text_group[7]
            navy.destinations[5].label=text_group[4]
        else:
            welcomer.title.value=text_group[37]
            new_scanner.title.value=text_group[23]
            language_change_new.title.value=text_group[13]
        delete_banner.content.title.value=text_group[9]
        search_button.bar_hint_text=text_group[11]
        seque.content.items[0].content.value=text_group[14]
        seque.content.items[1].content.value=text_group[15]
        seque.content.items[2].content.value=text_group[16]
        seque.content.items[3].content.value=text_group[17]
        seque.content.items[4].content.value=text_group[18]
        artist_photo.controls[2].content.controls[1].title.value=text_group[19]
        album_photo.controls[2].content.controls[1].title.value=text_group[19]
        koss_open.title.value=text_group[20]
        koss_deep.title.value=text_group[21]
        koss_deep.subtitle.value=text_group[22]
        scanner.title.value=text_group[23]
        recheck.title.value=text_group[24]
        language_change.title.value=text_group[13]
        fonter.title.controls[0].value=text_group[25]
        re_font.title.value=text_group[26]
        re_font.subtitle.value=text_group[27]
        lyrics_font.title.value=text_group[28]
        font_tran.title.value=text_group[29]
        darkness.title.value=text_group[30]
        colorer.title.controls[0].value=text_group[31]
        fast_mode.subtitle.value=text_group[32]
        fast_mode.title.value=text_group[33]
        edition.title.value=text_group[34]
        warning.content.title.value=text_group[35]
        liquid_open.title.value=text_group[36]
        initial_play.content.title.value=text_group[38]
        volve_banner.content.title.value=text_group[39]
        wind.update()
    def resize(e):
        global w,h
        w=wind.window.width
        h=wind.window.height  
        basis.width=w-90
        basic.controls[1].width=w
        basic.controls[1].height=h
        task_line.width=w-30
        navy.height=h-90
        timers.width=w-400
        lyrics_display.width=w-210-h*0.5
        lyrics_display.height=h*0.5+140
        photo.content.width=h*0.5
        photo.content.height=h*0.5
        title_group=h*0.5
        control1.width=h*0.5
        control2.width=h*0.5
        control3.width=h*0.5
        koss.width=w-120
        koss.height=h-90
        goss.height=h-90
        list_panel.controls[0].width=w-120
        playlist.width=w-120
        playlist.hight=h-144
        list_panel.controls[1].height=h-144
        artist_grid.width=w-120
        artist_grid.height=h-144
        artist_grid.cache_extent=h-144
        artist_panel.controls[0].width=w-120
        artist_panel.controls[1].width=w-120
        artist_main.width=w-h*0.6-130
        artist_main.height=h-90
        artist_photo.controls[0].width=h*0.6
        artist_photo.controls[0].height=h*0.6
        artist_photo.controls[1].width=h*0.6
        artist_photo.controls[2].content.controls[0].width=h*0.3
        artist_photo.controls[2].content.controls[1].width=h*0.3
        artist_photo.controls[2].width=h*0.6
        artist_page.controls[0].width=w-120
        artist_page.controls[0].height=h-90
        album_grid.width=w-120
        album_grid.height=h-144
        album_grid.cache_extent=h-144
        album_panel.controls[0].width=w-120
        album_panel.controls[1].width=w-120
        album_main.width=w-h*0.6-130
        album_main.height=h-90
        album_photo.controls[0].width=h*0.6
        album_photo.controls[0].height=h*0.6
        album_photo.controls[1].width=h*0.6
        album_photo.controls[2].content.controls[0].width=h*0.3
        album_photo.controls[2].content.controls[1].width=h*0.3
        album_photo.controls[2].width=h*0.6
        album_page.controls[0].width=w-120
        album_page.controls[0].height=h-90
        setting_panel.controls[0].width=w-120
        setting_panel.controls[0].height=h-90
        initial_panel.controls[0].height=h-90
        initial_panel.controls[0].width=w-120
        canva.width=w-120
        canva.height=h-90
        canbir.content.width=w-120
        canbir.content.height=h-90
        canbir.width=w-120
        canbir.height=h-90
        dynamic_photo.height=h-90
        wind.update()
    wind.on_resize=resize

    if begin:
        now_update(music_place)
        album_update()
        artist_update()
        folder_update()
        renew()
        if setting[7]:
            list_update_fast(music_place)
            item_update_fast()
        else:
            list_update(music_place)
            item_update()
    else:
        navy.destinations=[ft.NavigationRailDestination(icon=ft.Icons.CELEBRATION, label="")]
        navy.on_change=None
        await basis.jump_to_page(7)
        navy.selected_index=0
        navy.update()
        
        

    
if __name__ == "__main__":
    ft.run(main)
"""
待维修清单
歌词字体无法单独更改
载入的初始界面"""
