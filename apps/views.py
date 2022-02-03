from django.shortcuts import render
from . import models
import hashlib

def index(request):
    data = []
    title = ""
    if request.method == "GET" and not request.GET.get('folder') == None:
        folderName = request.GET.get('folder')
        for folder in models.Folders.objects.all():
            hashTitle = hashlib.sha256(folder.name_folder.encode('utf8')).hexdigest()
            if folderName == hashTitle:
                data = models.Apps.objects.filter(folder_id = int(folder.id))
                title = models.Folders.objects.filter(id = int(folder.id)).values('name_folder')[0]['name_folder']
    elif request.method == "POST":
        idList = request.POST.getlist('dataList')
        title = request.POST['titleName']
        for id in idList:
            models.Apps.objects.filter(id=id).delete()
        if title:
            folderId = models.Folders.objects.filter(name_folder = title).values('id')[0]['id']
            data = models.Apps.objects.filter(folder_id = int(folderId))
    return render(request, "index.html", {"data": data, "title": title})