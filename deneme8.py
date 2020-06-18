import requests
import json
from tkinter import *
from tkinter import messagebox as tkMessageBox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure


window = Tk() #pencere açtık
window.title("Trakya Üniversitesi Bilgisayar Mühendisliği 1191602801 Berkay Cihan PDG Final Ödevi Covid-19 Grafik Çizici")
window.iconbitmap('215px-Trakya_Üniversitesi_logosu.ico')  #programa ikon ekledim
window.geometry('1250x720')
window.configure(background='white')  #arkaplanı beyaz yaptım


class CustomListbox(Listbox):        #listboxa atarken integer değer str ye dönüştürülemiyo hatası verdi netten bunu buldum çalıştı
    def __contains__(self, str):
        return str in self.get(0, "end")


lb3=CustomListbox(window,bg="black",exportselection=False,fg="white",activestyle="dotbox",font="Helvetica",height=20)
lbl = Label(window,
            text="Toplam Teyit Edilen Vaka: ..............",height=5,fg="red",bg="white")
lbl1 = Label(window,
             text="Dünya Genelinde Toplam Ölüm: ...............",height=5,fg="red",bg="white")
lb2=Label(window,
           text="(Kullanılan bilgisayara göre biraz uzun sürebilir json dosyası 134mb)")
lb0=CustomListbox(window,
        bg = "black", fg = "white",exportselection=False,activestyle = "dotbox", font = "Helvetica", height = 20)


lbl.grid(column=0, row=1)
lbl1.grid(column=0, row=2)
lb2.grid(column=0,row=4)
lb0.grid(column=1,row=0)
lb3.grid(column=0,row=0)


def clicked():

    #internet varsa api'den çeker yoksa aynı dizindeki json dosyasından çeksin(dünya geneli kısmı için)
    try:
        url = "https://api.covid19api.com/summary"
        page = requests.get(url)
        veri = json.loads(page.text)
    except:
        with open("summary.json") as f:
            veri = json.load(f)

    lbl.configure(text=" Toplam Teyit Edilen Vaka: "
                       + str(veri["Global"]["TotalConfirmed"]))

    lbl1.configure(text="Dünya Genelinde Toplam Ölüm: "
                       + str(veri["Global"]["TotalDeaths"]))
    #try:
    #    url = "https://api.covid19api.com/all"
    #    page = requests.get(url)
    #    data = json.loads(page.text)
    #except:
    with open("all.json") as f:  #offline olarak yüklediğimiz aynı dizindeki json dosyasını çekiyor
        data = json.load(f)

    for deger in data:    #bu döngü apiden tüm ülkeleri lb3 listboxına unique çekiyor.
        for i, j in deger.items():
            if (i == "Country"):
                if (j in lb3):
                    continue
                else:
                    lb3.insert(END, j)
    liste = ["Confirmed", "Deaths", "Recovered", "Active", ]  #bu değerleri çekeceğiz lb0'a
    for deger in liste:
        if(deger in lb0):
            continue
        else:
            lb0.insert(END, deger)



    lb2.configure(text="Yenilendi")

def clicked2():
    selected_text2 = lb0.get("active")    #listboxlardan işaretli veriyi alıyoruz
    selected_text = lb3.get("active")
    tkMessageBox.showinfo("Bilgi",
                           selected_text+" "+selected_text2+" "+ "Grafiği çiziliyor...")

    #türkçeye çeviriyoruz
    if (selected_text2=="Confirmed"):
        selected_text5="Vaka"
    elif(selected_text2=="Deaths"):
        selected_text5="Ölüm"
    elif(selected_text2=="Recovered"):
        selected_text5="İyileşen"
    elif(selected_text2=="Active"):
        selected_text5="Hasta"

    isim = {"title":selected_text, "xlabel":"Date (Ocak 22,2020 tarihinden günümüze) " , "ylabel":selected_text5}

    ulke_floatlar=[]    #grafiğini çizmek için x ve y koordinatında kullanılacak listeler
    ulke_tarihler=[]

    with open("all.json") as f:
        data = json.load(f)

    for deger in data:                  #json üzerinde işimize yarayan değerlere ulaşıyoruz
        for c,v in deger.items():
            if(v==selected_text):
                for i,j in deger.items():
                    if(i==selected_text2):
                        ulke_floatlar.append(float(j))
    for deger in data:
        for i,j in deger.items():
            if(j==selected_text):
                for c,v in deger.items():
                    if(c=="Date"):

                        ulke_tarihler.append(str(v))

    fig = plt.figure()      #grafiği tkinter arayüzüne çizdiriyoruz bu kod bloğunda
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(ulke_tarihler, ulke_floatlar, linestyle="--", color="red")
    ax.set(**isim)

    # tarih kısmı üst üste bindiği ve okunmadığı için kaldırdım bu kodla
    plt.xticks([ulke_tarihler[i] for i in range(len(ulke_tarihler)) if i % 1 == 1], rotation='vertical')


    canvas = FigureCanvasTkAgg(fig, master=window)
    plot_widget = canvas.get_tk_widget()
    fig.canvas.draw_idle()
    plot_widget.grid(row=0, column=3)



btn = Button(window, text="Verileri Çek",relief=RAISED,bg="green",fg="white", command=clicked,width=25)
btn.grid(column=0, row=3)

btn2 = Button(window, text="Grafik çiz",relief=SUNKEN,bg="blue",fg="white", command=clicked2,width=25)
btn2.grid(column=1, row=1)

window.mainloop()