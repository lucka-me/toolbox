#!/usr/bin/env python3
# coding: utf-8

"""
神奇寶貝百科服飾列表生成器
Author:     Lucka
Version:    0.1.1
Licence:    MIT

"""

# 庫
import time
import urllib.request
from wand.image import Image

def getFullyMatchedSN(target, array):
    """
    獲取列表中完整匹配目标數值的序列號
    參數列表:
        target: int     目標數值
        array:  int     掃描的列表
    返回：
        int     列表中的序列號，如無匹配項則返回-1
    """
    for scanner in range(0, len(array)):
        if target == array[scanner]:
            return scanner
    return -1

def getPartlyMatchedSN(target, array):
    """
    獲取列表中部分匹配目标數值的序列號，倒序扫描
    參數列表:
        target: int     目標數值
        array:  int     掃描的列表
    返回：
        int     列表中的序列號，如無匹配項則返回-1
    """
    for scanner in range(len(array) - 1, -1, -1):
        if array[scanner] in target:
            return scanner
    return -1

def getImg(imgSN, typeSN, colorSN):
    """
    獲取圖片並重命名和裁切
    參數列表:
        imgSN:      int     Serebii.net 上的圖片編號
        typeSN:     int     服裝類型序列號
        colorSN:    int     顏色類型序列號
                            -1: 無顏色類型
    """

    # 生成圖片 URL
    if sex == "男生":
        url = ("https://serebii.net/ultrasunultramoon/clothing/male/{0}.png"
               .format(imgSN))
    else:
        url = ("https://serebii.net/ultrasunultramoon/clothing/female/{0}.png"
               .format(imgSN))

    # 生成圖片文件名
    if colorSN == -1:
        color = ""
    else:
        color = " {0}".format(colorListCH[colorSN])
    fileName = "USUM {0} {1}{2}.png".format(sex, typeListCH[typeSN], color)

    # 獲取圖片
    print("正在下載: {0}".format(url))
    urllib.request.urlretrieve(url, fileName)
    print("下載完成: {0}".format(fileName))

    # 裁切圖片
    # 目前本部分尺寸需要手動設置
    # MARK: - Manual Operation
    # 上衣:   96x96+(x)+50
    # 褲裙:   96x96+(x)+105
    # 襪子:   96x48+(x)+182
    # 鞋子:   96x48+(x)+182
    # 包包:   96x96+(x)+50
    # 帽子:   64x64+(x)+8
    # 眼鏡:   64x64+(x)+8
    # 髮飾:   64x64+(x)+8
    print("正在裁切圖片⋯")
    with Image(filename = fileName) as image:
        sizeX = 96
        sizeY = 96
        x = int((image.width - sizeX) / 2)
        y = 50
        image.crop(x, y, width = sizeX, height = sizeY)
        image.save(filename = fileName)
    print("圖片處理完成。")


def getColumn(typeSN, colorSN,
              price,
              locationSN, location,
              version):
    """
    獲取 Wiki 各式的表格行代碼
    參數列表:
        typeSN:     int     服裝類型序列號
        colorSN:    int     顏色類型序列號
                            -1: 無顏色類型
        price:      int     價格
        locationSN: int     購買城市序列號
                            -1: 無且不生成鏈接
        location:   str     購買商店或地點
        version:    int     版本限定
                            0:  雙版本均有
                            1:  究極之日限定
                            2:  究極之月限定
    返回:
        String      Wiki 各式的表格行代碼
    """

    # 名稱列
    nameRow = ("{0}<br/><small>{1}</small><br/><small>{2}</small>"
               .format(typeListCH[typeSN],
                       typeListJP[typeSN],
                       typeListEN[typeSN]))

    # 圖樣列
    # MARK: - Manual Operation
    # 請確定圖片寬度
    # 上衣、褲裙、襪子、鞋子、包包:   96px
    # 帽子、眼鏡、髮飾:             64px
    if colorSN == -1:
        color = ""
    else:
        color = " {0}".format(colorListCH[colorSN])
    imgRow = ("[[File:USUM {0} {1}{2}.png|96px]]"
              .format(sex, typeListCH[typeSN], color)
    )

    # 顏色列樣式
    if version == 0:
        colorRowStyle = ""
    elif version == 1:
        colorRowStyle = "class = \"bgl-US\" | "
    elif version == 2:
        colorRowStyle = "class = \"bgl-UM\" | "

    # 颜色列
    if colorSN == -1:
        colorRow = "-"
    else:
        colorRow = "{0}".format(colorListCH[colorSN])

    # 價格列
    if price == 0:
        priceRow = "-"
    else:
        priceRow = "{{{{$}}}}{0}".format(price)

    # 購入地點列
    if locationSN == -1:
        locationRow = location
    else:
        locationRow = ("[[{0}]]<br/>[[{0}#{1}|{1}]]"
                       .format(locationListCH[locationSN], location))

    # 生成代碼
    result = ("|-\n| {0}\n| {1}\n| {2}{3}\n| {4}\n| {5}\n\n"
              .format(nameRow,
                      imgRow,
                      colorRowStyle, colorRow,
                      priceRow,
                      locationRow))
    return result

# 主程序
print(__doc__)
print("請在程序代碼中確認下列基本參數:")
print("  * 性別、裁切尺寸、圖片寬度")
print("請搜索 # MARK: - Manual Operation")
answer = input("是否繼續 (Y/N): ")
if answer != "y" and answer != "Y":
    exit()

# 計時器
startTime = time.time()

# 基本信息，需手動設置
# MARK: - Manual Operation
# sex = "女生"
# versionCode = "UM"
sex = "男生"
versionCode = "US"

# 讀取譯名列表
print("正在讀取文本文件⋯")
typeListCH = open('type_ch.txt').read().splitlines()
typeListJP = open('type_jp.txt').read().splitlines()
typeListEN = open('type_en.txt').read().splitlines()
colorListCH = open('color_ch.txt').read().splitlines()
colorListEN = open('color_en.txt').read().splitlines()
locationListCH = open('location_ch.txt').read().splitlines()
locationListEN = open('location_en.txt').read().splitlines()
print("讀取完畢。")

# 處理原文件
print("正在處理 HTML 文件⋯")
sourceFile = open("source.html", "r")
sourceString = sourceFile.read()
sourceFile.close()
sourceString = sourceString.replace("<tr><td class=\"fooinfo\"><a href=\"clothing/male/", "\n")
sourceString = sourceString.replace(".png\" rel=\"lightbox[ranger3]\" title=\"Clothing\"><img src=\"clothing/male/", "\n")
sourceString = sourceString.replace(".jpg\" border=\"0\" /></a></td><td class=\"fooinfo\">", "\n")
sourceString = sourceString.replace("</td><td class=\"fooinfo\">", "\n")
sourceString = sourceString.replace("</td></tr>", "\n")
## 處理原生錯誤
sourceString = sourceString.replace("Grey", "Gray")
sourceString = sourceString.replace("\nNavy\n", "\nNavy Blue\n")
sourceString = sourceString.replace("Hau'oli", "Hau’oli")
sourceString = sourceString.replace(" GI ", " Gi ")

targetFile = open("list.txt", "w")
targetFile.write(sourceString)
targetFile.close()
print("處理完畢，已生成 list.txt 文件。")

# 讀取列表文件並生成 Wiki 代碼
print("正在生成 Wiki 代碼⋯")
listFile = open("list.txt", "r")
wikiFile = open("wiki.txt", "w")
wikiTableHead = """
{{| class = "a-l eplist roundy sortable bgd-{0} b-{0}"
|- class = "bgl-{0}"
! class = "roundytl-6" rowspan = 4 | 名称
! class = "unsortable" rowspan = 4 | 图样
! 颜色／图案
! data-sort-type = "number" rowspan = 4 | 价格
! class = "roundytr-6" rowspan = 4 | 购入地点
|-
! class = "bgwhite" | 太阳／月亮均有
|-
! class = "bgl-US" | 仅太阳
|-
! class = "unsortable bgl-UM" | 仅月亮

""".format(versionCode)
wikiFile.write(wikiTableHead)
# 處理計數
count = 0
# 錯誤列表
errorList = []

while True:
    """
    list.txt 中一件服飾對應十行：

    ImgSN
    ImgSN       重複
    Type        服飾種類如Ｔ恤等
    Color
    Catalog     服飾類型如上衣、褲、裙等
    Price
    Location
    Version

    注意首位各有一空行
    """
    # 第1行若為空則退出循環
    line = listFile.readline()
    if len(line) == 0:
        break

    print("正在處理：")
    print("序號:\t\t{0}".format(count + 1))
    line = listFile.readline()
    imgSN = int(line)
    print("圖片編號:\t{0}".format(imgSN))

    listFile.readline()

    line = listFile.readline()
    clothType = line.replace("\n", "")
    typeSN = getFullyMatchedSN(clothType, typeListEN)
    if typeSN == -1:
        print("警告: 未找到對應服飾，原文: {0}".format(clothType))
    else:
        print("服飾種類:\t{0} -> {1}".format(clothType, typeListCH[typeSN]))

    line = listFile.readline()
    color = line.replace("\n", "")
    if color == "":
        colorSN = -1
        print("顏色:\t\t無")
    else:
        colorSN = getFullyMatchedSN(color, colorListEN)
        print("顏色:\t\t{0} -> {1}".format(color, colorListCH[colorSN]))

    listFile.readline()

    line = listFile.readline()
    if line.replace("\n", "").isdigit():
        price = int(line)
    else:
        price = 0
    print("價格:\t\t{0}".format(price))

    line = listFile.readline()
    location = line.replace("\n", "")
    locationSN = getPartlyMatchedSN(location, locationListEN)
    print("獲得地點:\t{0} -> {1}"
          .format(location, locationListCH[locationSN]))
    if "Apparel Shop" in location:
        location = "时装店"

    line = listFile.readline()
    version = line.replace("\n", "")
    if version == "Both":
        version = 0
    elif version == "Ultra Sun":
        version = 1
    elif version == "Ultra Moon":
        version = 2
    print("版本限定:\t{0}".format(version))

    listFile.readline()

    # 生成 Wiki 各式的表格行並寫入文件
    # 若未成功識別種類則發出警告且不生成代碼
    if typeSN == -1:
        print("警告: 未成功處理第此項目，請檢查。")
        errorList.append(count + 1)
    else:
        print("正在處理圖片…")
        getImg(imgSN, typeSN, colorSN)
        wikiColumn = getColumn(typeSN, colorSN,
                               price,
                               locationSN, location,
                               version)
        # Gracidea -> [[好奥乐市]]<br/>[[购物广场]][[购物广场#葛拉西蒂亞|葛拉西蒂亞]]
        wikiColumn = wikiColumn.replace("Gracidea",
                                        "[[好奥乐市]]<br/>[[购物广场]][[购物广场#葛拉西蒂亞|葛拉西蒂亞]]")
        wikiFile.write(wikiColumn)
    count = count + 1
    print("")

wikiFile.write("|}\n")
wikiFile.close()
print("處理完畢，共處理{0}個服飾，已生成完整 wiki.txt 文件及圖片。".format(count))
if len(errorList) > 0:
    print("未成功處理{0}個服飾，序號如下:".format(len(errorList)))
    for scanner in errorList:
        print("  {0}".format(scanner))
print("運行耗時: {0:.2f}秒。".format(time.time() - startTime))
