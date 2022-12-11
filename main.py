#   Python Projesi - SALON REZERVASYON SİSTEMİ
#   Ammar  Abdurrauf - 170421930

def read_file(file_name):
    dosya = open(file_name, "r")
    text_line = []
    for line in dosya:
        text_line.append(line.strip().split("-"))

    global bilet_fiyatlari
    global max_bilet
    # maximum satin alinabilecek bilet adedi
    max_bilet = int(text_line[0][1])

    # bilet fiyat listesi
    bilet_fiyatlari = text_line[1:5]
    #print(bilet_fiyatlari)

    global indirimler
    indirimler = []
    indirimler.append(list(text_line[5:8]))
    indirimler.append(list(text_line[8:11]))
    indirimler.append(list(text_line[11:14]))
    indirimler.append(list(text_line[14:]))

def koltuk_ayarla():
    kategori01 = [["-"] * 10 for _ in range(10)]
    kategori02 = [[["-"] * 5 for _ in range(10)] for _ in range(2)]
    kategori03 = [["-"] * 10 for _ in range(10)]
    kategori04 = [[["-"] * 5 for _ in range(10)] for _ in range(2)]
    koltuklar = [
        kategori02[0], kategori01, kategori02[1],
        kategori04[0], kategori03, kategori04[1]
    ]
    ciro_seans.append(0)
    return koltuklar

def ciro_goster():
    kategori1 = -1
    kategori2 = -1
    print("1. Toplam Ciro (Seans)\n2. Toplam Ciro (Kategori)")
    while (kategori1 != 1 and kategori1 != 2):
        try:
            kategori1 = int(input("Seçiminiz: "))
        except ValueError:
            print("lütfen rakam dışında giriş yapmayınız")
        else:
            if not (kategori1 == 1 or kategori1 == 2):
                print("lütfen 1-2 aralığın dışında bir değer girmeyiniz")
    if kategori1 == 1:
        print("Seans giriniz: \n(Tüm seansların toplamı için 0 giriniz)")
        seans = -1
        while (seans < 0 or seans > len(ciro_seans)):
            try:
                seans = int(input("Seciminiz: "))
            except ValueError:
                print("lütfen rakam dışında giriş yapmayınız")
            else:
                if (seans < 0 or seans > len(ciro_seans)):
                    print("lütfen 0 -", len(ciro_seans), "aralığın dışında bir değer girmeyiniz")
        if seans == 0:
            print("Tüm seansların toplam kazanç: ", sum(ciro_seans))
        else:
            print(seans, ". Seans icin toplam kazanç: ", ciro_seans[seans-1])
    elif kategori1 == 2:
        while not (kategori2 >= 0 and kategori2 <= 4):
            try:
                kategori2 = int(input("(bütün kategorilerin toplam kazancına bakmak istiyorsaniz 0 giriniz)"
                                     "\nkategori giriniz (1-4): "))
            except ValueError:
                print("lütfen rakam dışında giriş yapmayınız")
            else:
                if kategori2 < 0 or kategori2 > 4:
                    print("lütfen 0-4 aralığın dışında bir değer girmeyiniz")
        if kategori2 == 0:
            print("bütün kategorilerin toplam kazanç: ", sum(ciro_kategori))
        else:
            print(kategori2, ". kategorinin toplam kazanç: ", ciro_kategori[kategori2-1])

def ucret_hesapla(kategori, bilet_adedi):
    kazanc = 0
    indirim_yuzdesi = 0
    toplam_ucret = int(bilet_fiyatlari[kategori-1][1])*bilet_adedi
    print("toplam fiyat: ", toplam_ucret, "TL")
    for indirim in indirimler[kategori-1]:
        if indirim[2] == "M":
            indirim[2] = str(max_bilet)
        if bilet_adedi >= int(indirim[1]) and bilet_adedi <= int(indirim[2]):
            indirim_yuzdesi += int(indirim[3])
            kazanc = kazanc + (toplam_ucret * (indirim_yuzdesi/100))
            toplam_ucret = toplam_ucret - kazanc
            break
    print("indirim: %", indirim_yuzdesi, "\nkazanciniz: ", kazanc,
          "\nindirim uygulandiktan sonra toplam fiyat: ", toplam_ucret, "TL")
    return toplam_ucret

def kategori1ve3(kategori, bilet_adedi, koltuklar):
    satir = -1
    sutun = -1

    bos_koltuk = 0
    dolu_koltuk = 0

    ucret_kategori = 0

    for i in range(10):
        bos_koltuk += koltuklar[kategori][i].count("-")
        dolu_koltuk += koltuklar[kategori][i].count("X")

    if bos_koltuk == 0:
        print("bu kategorideki koltuklar dolmustur, baska kategoriyi seciniz")
    elif bos_koltuk < bilet_adedi:
        print("bu kategorideki kalan bos koltuk: ", bos_koltuk,
        "\nlutfen bu kategoriden daha az bilet aliniz yada baska katgeori seciniz")
    else:
        if kategori == 1:
            ucret_kategori = ucret_hesapla(kategori, bilet_adedi)
        else:
            ucret_kategori = ucret_hesapla(kategori-1, bilet_adedi)
        for i in range(10):
            for j in range(10):
                if koltuklar[kategori][i][j] == "-":
                    satir = i
                    sutun = j
                    break
            if satir != -1:
                break
        doldur = sutun
        for i in range(sutun, sutun + bilet_adedi):
            if koltuklar[kategori][satir].count("-") == 0:
                satir += 1
                doldur = 0
            koltuklar[kategori][satir][doldur] = "X"
            doldur += 1
        print("bos koltuk: ", bos_koltuk - bilet_adedi, "\ndolu koltuk: ", dolu_koltuk + bilet_adedi)
    return koltuklar, ucret_kategori

def kategori2(kategori, bilet_adedi, koltuklar):
    satir = -1
    sutun = -1

    bos_koltuk = 0
    dolu_koltuk = 0

    ucret_kategori = 0

    for i in range(10):
        bos_koltuk = bos_koltuk + koltuklar[0][i].count("-") + koltuklar[2][i].count("-")
        dolu_koltuk = dolu_koltuk + koltuklar[0][i].count("X") + koltuklar[2][i].count("X")

    if bos_koltuk == 0:
        print("bu kategorideki koltuklar dolmustur, baska kategoriyi seciniz")
    elif bos_koltuk < bilet_adedi:
        print("bu kategorideki kategoride kalan bos koltuk: ", bos_koltuk,
        "\nlutfen bu kategoriden daha az bilet aliniz yada baska katgeori seciniz")
    else:
        ucret_kategori = ucret_hesapla(kategori, bilet_adedi)
        for i in range(10): #satir
            for j in range(2): #kategori
                if j == 0:
                    for k in range(4, -1, -1): #k = sutun
                        if koltuklar[j][i][k] == "-":
                            satir = i
                            sutun = k
                            kategori = j
                            break
                elif j == 1:
                    for k in range(5):
                        if koltuklar[j+1][i][k] == "-":
                            satir = i
                            sutun = k
                            kategori = j+1
                            break
                if satir != -1:
                    break
            if satir != -1:
                break
        for i in range(bilet_adedi):
            if i != 0 and koltuklar[kategori][satir].count("-") == 0:
                if kategori == 0:
                    kategori = 2
                    sutun = 0
                elif kategori == 2:
                    kategori = 0
                    satir += 1
                    sutun = 4
            koltuklar[kategori][satir][sutun] = "X"
            if kategori == 0:
                sutun -= 1
            elif kategori == 2:
                sutun += 1
        print("bos koltuk: ", bos_koltuk - bilet_adedi, "\ndolu koltuk: ", dolu_koltuk + bilet_adedi)
    return koltuklar, ucret_kategori

def kategori4(kategori, bilet_adedi, koltuklar):
    satir = -1
    sutun = -1

    bos_koltuk = 0
    dolu_koltuk = 0

    ucret_kategori = 0

    for i in range(10):
        bos_koltuk = bos_koltuk + koltuklar[3][i].count("-") + koltuklar[5][i].count("-")
        dolu_koltuk = dolu_koltuk + koltuklar[3][i].count("X") + koltuklar[5][i].count("X")

    if bos_koltuk == 0:
        print("bu kategorideki koltuklar dolmustur, baska kategoriyi seciniz")
    elif bos_koltuk < bilet_adedi:
        print("bu kategorideki kategoride kalan bos koltuk: ", bos_koltuk,
        "\nlutfen bu kategoriden daha az bilet aliniz yada baska katgeori seciniz")
    else:
        ucret_kategori = ucret_hesapla(kategori, bilet_adedi)
        for i in range(10): #satir
            for j in range(2): #kategori
                if j == 0:
                    for k in range(4, -1, -1): #k = sutun
                        if koltuklar[3][i][k] == "-":
                            satir = i
                            sutun = k
                            kategori = 3
                            # print("bulundu, satir: ", satir, "\nsutun: ", satir)
                            break
                elif j == 1:
                    for k in range(5):
                        if koltuklar[5][i][k] == "-":
                            satir = i
                            sutun = k
                            kategori = 5
                            # print("bulundu, satir: ", satir, "\nsutun: ", satir)
                            break
                if satir != -1:
                    break
            if satir != -1:
                break
        for i in range(bilet_adedi):
            if i != 0 and koltuklar[kategori][satir].count("-") == 0:
                if kategori == 3:
                    kategori = 5
                    sutun = 0
                elif kategori == 5:
                    kategori = 3
                    satir += 1
                    sutun = 4
            koltuklar[kategori][satir][sutun] = "X"
            if kategori == 3:
                sutun -= 1
            elif kategori == 5:
                sutun += 1
        print("bos koltuk: ", bos_koltuk-bilet_adedi, "\ndolu koltuk: ", dolu_koltuk+bilet_adedi)
    return koltuklar, ucret_kategori

def koltuk_ayirt(kategori, bilet_adedi, koltuklar):
    if kategori == 1:
        koltuklar_yeni, ucret_kategori = kategori1ve3(kategori, bilet_adedi, koltuklar)
        ciro_kategori[0] += ucret_kategori
    elif kategori == 3:
        koltuklar_yeni, ucret_kategori = kategori1ve3(kategori+1, bilet_adedi, koltuklar)
        ciro_kategori[2] += ucret_kategori
    elif kategori == 2:
        koltuklar_yeni, ucret_kategori = kategori2(kategori, bilet_adedi, koltuklar)
        ciro_kategori[1] += ucret_kategori
    elif kategori == 4:
        koltuklar_yeni, ucret_kategori = kategori4(kategori, bilet_adedi, koltuklar)
        ciro_kategori[3] += ucret_kategori
    else:
        koltuklar_yeni = koltuklar
        ucret_kategori = 0
    ciro_seans[seans] += ucret_kategori
    return koltuklar_yeni

def rezervasyon(koltuklar):
    print("kategori\tfiyat")
    for i in range(4):
        print(bilet_fiyatlari[i][0].center(8), "\t", bilet_fiyatlari[i][1])
    print("satın alınabilecek maksimum bilet adedi: ", max_bilet)
    kategori = -1
    bilet_adedi = -1
    while (not (kategori >= 1 and kategori <= 4)):
        try:
            kategori = int(input("\nkategori seçiniz (1-4): "))
        except ValueError:
            print("lütfen rakam dışında giriş yapmayınız")
        else:
            if kategori < 1 or kategori > 4:
                print("lütfen 1-4 aralığın dışında bir değer girmeyiniz")

    while (not (bilet_adedi >= 1 and bilet_adedi <= max_bilet)):
        try:
            bilet_adedi = int(input("almak istediğiniz bilet adedi giriniz (maksimum 25): "))
        except ValueError:
            print("lütfen rakam dışında giriş yapmayınız")
        else:
            if bilet_adedi < 1 or bilet_adedi > max_bilet:
                print("en az 1 en fazla 25 tane bilet alabilirsiniz")

    return koltuk_ayirt(kategori, bilet_adedi, koltuklar)

def salonu_yazdir(koltuklar):
    print("koltuklar: ")
    print("   ", end="")

    for i in range(1,21):
        print(str(i).zfill(2)," ", end="")
    print("")
    for i in range(10):
        print(str(i + 1).zfill(2), " ", end="")
        for j in range(0,3):
            for koltuk in koltuklar[j][i]:
                print(koltuk + "   ", end="")
        print("")
    for i in range(10):
        print(i + 11, " ", end="")
        for j in range(3, 6):
            for koltuk in koltuklar[j][i]:
                print(koltuk + "   ", end="")
        print("")

def menuler(secim, koltuklar):
    global seans
    koltuklar_yeni = koltuklar
    if secim == 0:
        print("Çıkış")
        exit()
    elif secim == 1:
        koltuklar_yeni = rezervasyon(koltuklar)
    elif secim == 2:
        salonu_yazdir(koltuklar)
    elif secim == 3:
        koltuklar_yeni = koltuk_ayarla()
        print("Yeni Etkinlik\nTüm rezervasyon silindi")
        for i in range(4):
            ciro_kategori[i] = 0
        print("bu seans için toplam kazanç: ", ciro_seans[seans])
        seans += 1
    elif secim == 4:
        ciro_goster()
    return koltuklar_yeni

def ana_menu_yazdir(koltuklar):
    print("\n")
    print("*"*20)
    print(" ANA MENU ".center(20, "*"))
    print("*" * 20)
    print("1. Rezerfasyon\n2. Salonu Yazdır\n3. Yeni Etkinlik\n4. Toplam Ciro\n0. Çıkış")
    print("*" * 20)
    print("Seçiminiz ? ", end="")

    secim = -1
    while not (secim >= 0 and secim <= 4):
        try:
            secim = int(input())
        except ValueError:
            print("lütfen rakam dışında giriş yapmayınız")
        else:
            if secim < 0 or secim > 4:
                print("lütfen 0-4 aralığın dışında bir değer girmeyiniz")

    return menuler(secim, koltuklar)

if __name__=="__main__":
    ciro_kategori = [0, 0, 0, 0]
    ciro_seans = []
    seans = 0
    read_file("indirim.txt")
    koltuklar = koltuk_ayarla()
    while True:
        koltuklar = ana_menu_yazdir(koltuklar)