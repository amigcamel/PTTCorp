#-*-coding:utf-8-*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import Context, RequestContext

from pttcorp_comments.forms import CommentModelForm
from pttcorp_comments.models import CommentModel
from pttcorp_admin.models import UpdateLogModel
from ipware.ip import get_ip
import json


def chunks(l, n):
    if n < 1:
        n = 1
    return [l[i:i + n] for i in range(0, len(l), n)]


cands_ori = [
    "新聞", "八卦", "就是", "有沒有", "媒體", "報導", "完整", "真的", "日", "來源", "標題", "內文",
    "台北", "還有", "怎麼", "記者", "柯", "其實", "然後", "只是", "國民黨", "一下", "個人", "民眾",
    "連結", "連", "好像", "根本", "朋友", "不要", "為什麼", "總統", "最近", "只有", "買", "文", "阿",
    "連勝", "蘋果", "誰", "萬", "為了", "文哲", "出來", "啦", "到底", "這麼", "感覺", "錢", "鄉民",
    "堆", "事情", "之前", "講", "東西", "支持", "網友", "以前", "民進黨", "警察", "後來", "的話",
    "或是", "網路", "馬英九", "都會", "打", "你們", "高雄", "找", "事件", "香港", "馬", "選舉", "人民",
    "直接", "警方", "請問", "叫", "完全", "女生", "當然", "喜歡", "拿", "相關", "現場", "各位", "手機",
    "哪", "只能", "小弟", "約", "台灣人", "幫", "一點", "大概", "剛剛", "裡面", "玩", "立委", "一起",
    "小時", "去年", "有些", "討論", "以上", "第", "下午", "立法院", "台北市", "不用", "綜合", "那些",
    "就算", "變成", "快", "繼續", "篇", "敢", "台中", "民主", "接受", "幾乎", "長", "不少", "服貿",
    "影片", "多少", "有點", "是不是", "所有", "同學", "相信", "臉書", "部分", "女", "某", "北市",
    "還要", "自由", "處理", "特別", "另外", "遊戲", "文章", "不到", "內容", "調查", "喔", "包括",
    "男子", "老闆", "超過", "突然", "節目", "張", "學運", "有人", "強調", "市場", "整個", "常常",
    "日報", "市長", "年前", "靠", "台", "企業", "兩岸", "寫", "運動", "來說", "情況", "為何", "隻",
    "而已", "甚麼", "原因", "遭", "安全", "電視", "上午", "以為", "以後", "小孩", "提出", "政策",
    "能力", "魯蛇", "電影", "聽到", "抗議", "基本", "網址", "根據", "狀況", "至於", "加上", "想要",
    "看看"
]

#cands = random.sample(cands, 50)
cands = chunks(cands_ori, 50)
cands = [' '.join(i) for i in cands]
cands = json.dumps(cands)


def index(request):
    comments = CommentModel.objects.all()
    comments = reversed(comments)
    update_log = reversed(UpdateLogModel.objects.all())

    if request.method == "POST":
        form = CommentModelForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            message = form.cleaned_data['message']
            ip = get_ip(request)
            if ip is None:
                ip = 'None'
            CommentModel.objects.create(
                username=username, message=message, ip=ip)
            return HttpResponseRedirect(reverse('index'))
    else:
        form = CommentModelForm()
    return render_to_response(
        'index.html', {
            'form': form,
            'comments': comments,
            'update_log': update_log,
            'cands': cands
        },
        context_instance=RequestContext(request))


from django.shortcuts import render_to_response
from django.template import RequestContext


def handler500(request):
    response = render_to_response(
        '500.html', {}, context_instance=RequestContext(request))
    response.status_code = 500
    return response
