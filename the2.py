import random
from math import sqrt
from evaluator import *


# random.seed(111)

DATA = get_data()
 

global m,n,d,k,h,u     # Sabitleri çektik. Assign ettik. 

m,n,d,k,h,u = DATA[0], DATA[1], DATA[2], DATA[3], DATA[4], DATA[5]

dataF = DATA[6]   # dataF dediğimiz universal_state oldu 

global koordinatlar
koordinatlar = [ [0 for i in range(n+1)] for i in range(m+1)] # Koordinat düzlemi, ilerlenilecek alanda başka birinin olup olmadığını kontrol etmek için matris ile (iç içe listelerle) oluşturduk.

for item in dataF:
    x,y= item[0]          # Başlangıç konumlarını 0 dan 1 e çevirdik ki dolu olduğu belli olsun...
    koordinatlar[y][x] = 1

def hareket(kisi):
    
    koordinat = kisi[0]
    durum  = kisi[1]
    
    x1,y1 = koordinat
    x,y = koordinat


    #print("x1:{} y1:{}".format(x,y))  
    if durum == 0: listMove = [["Forward",0,1,0],["Forward Right",-1,1,1],["Right",-1,0,2],["Backward Right",-1,-1,3],["Backward",0,-1,4],["Backward Left",1,-1,5],["Left",1,0,6],["Forward Left",1,1,7]]
         
    elif durum == 4: listMove = [["Forward",0,-1,4],["Forward Right",1,-1,5],["Right",1,0,2],["Backward Right",1,1,7],["Backward",0,1,0],["Backward Left",-1,1,3],["Left",-1,0,6],["Forward Left",-1,-1,7]]
        
    elif durum == 6: listMove = [["Forward",1,0,6],["Forward Right",1,1,7],["Right",0,1,0],["Backward Right",-1,1,3],["Backward",-1,0,2],["Backward Left",-1,-1,3],["Left",0,-1,4],["Forward Left",1,-1,5]]
        
    elif durum == 2: listMove = [["Forward",-1,0,0],["Forward Right",-1,-1,3],["Right",0,-1,4],["Backward Right",1,-1,5],["Backward",1,0,6],["Backward Left",1,1,7],["Left",0,1,0],["Forward Left",-1,1,1]]
            
    
    elif durum == 7: listMove = [["Forward",1,1,7],["Forward Right",0,1,0],["Right",-1,1,1],["Backward Right",-1,0,2],["Backward",-1,-1,3],["Backward Left",0,-1,4],["Left",1,-1,5],["Forward Left",1,0,6]]           
       
    elif durum == 3: listMove = [["Forward",-1,-1,3],["Forward Right",0,-1,4],["Right",1,-1,5],["Backward Right",1,0,6],["Backward",1,1,7],["Backward Left",0,1,0],["Left",-1,1,1],["Forward Left",-1,0,2]]           
        
    elif durum == 1: listMove = [["Forward",-1,1,1],["Forward Right",-1,0,2],["Right",-1,-1,3],["Backward Right",0,-1,4],["Backward",1,-1,5],["Backward Left",1,0,6],["Left",1,1,7],["Forward Left",0,1,0]]           
        
    elif durum == 5: listMove = [["Forward",1,-1,5],["Forward Right",1,0,6],["Right",1,1,7],["Backward Right",0,1,0],["Backward",-1,1,1],["Backward Left",-1,0,2],["Left",-1,-1,3],["Forward Left",0,-1,4]]           
       
        #Forward, Forward Right, Right, Backward Right, Backward, Backward Left, Left, Forward Left

    olasılık = random.choices(listMove, weights=[(1/2)*u , (1/8)*u , (1/2)*(1-u-(u**2)) , (2/5)*(u**2) , (1/5)*(u**2) , (2/5)*(u**2) , (1/2)*(1-u-(u**2)) , (1/8)*u],k=1)   # Hareket seçimi yaptık. 
    
    #print("olasılık:",olasılık)
    #print("Geldiği Yön: " , durum)
    #print("Hareket Yönü: " , olasılık[0][0])
    #print("Hareket Miktarı: " , olasılık[0][1:3])
    
    x += olasılık[0][1]             # Hareket seçimimize göre kordinatları güncelledik.
    y += olasılık[0][2]
    
    #print("x2:{} y2:{}".format(x,y))
    #print("-"*20)  
    
    if x < n or y < m:      # Örneğin 10'a 10'luk bir arenada maksimum 9'a 9'olabiliyoruz --> Discussion Forumdaki bilgi       
        if koordinatlar[y][x] == 0:     # Gitmek istediğimiz yer boş mu diye kontrol ettik...
            koordinatlar[y][x] = 1      # gittiysek yeni yer(kordinatlar) doldu 0 dı --> 1 oldu
            koordinatlar[y1][x1] = 0    # önceki yer boşaldı 1 di --> 0 oldu 
            return (x,y) , olasılık[0][3]
        else:
            return (x1,y1) , durum      # hareket edemedik. 
        
    else:
      
        return (x1,y1) , durum      # hareket edemedik.


def euclideanDist(a1,a2):
    x1,y1 = a1
    x2,y2 = a2
    return sqrt((x1-x2)**2 + (y1-y2)**2)

def prob(dist):
    
    if dist<=d:
        return min(1,k/(dist**2))    
    else:
        return 0        
    
def infected(kisi1,kisi2):
    
    koor1,koor2 = kisi1[0],kisi2[0]    # kişilerin kordinatları 
    mask1,mask2 = kisi1[2],kisi2[2]
    infec1,infec2 = kisi1[3],kisi2[3]  # kişilerin hastalık durumları 
    
    if infec1 == "notinfected" and infec2 == "infected":
        distance = euclideanDist(koor1,koor2)
        #print("Distance: ",distance)
    
        probb = prob(distance)
        #print("Olasılık: ",probb)
        #print("-"*20) 

        if probb == 0:              # Eğer bulaş riski yoksa mesafeden ötürü fazladan random.choices çağırmamak için...
            return 0,0              # neden 0 return ettiğimizi alt satırlara gelince fark edebiliriz.

        if probb != 0:     

            plist = ["infected","notinfected"]
            
            if mask1 == "masked" and mask2 == "masked": secim = random.choices(plist,weights = [(1/((h**2)))*probb, 1 - (1/((h**2)))*probb], k=1)
            elif mask1 != mask2: secim = random.choices(plist, weights = [(1/h)*probb,1-((1/h)*probb)], k=1)
            elif mask1 == "notmasked" and mask1 == "notmasked": secim = random.choices(plist, weights = [probb,1-probb], k=1)

            return secim[0] , 1    # neden 1 return ettiğimizi alt satırlarda fark edebiliriz. 
    
    elif infec1 == "infected" and infec2 == "notinfected":
        distance = euclideanDist(koor1,koor2)
        #print("Distance: ",distance)
    
        probb = prob(distance)
        #print("Olasılık: ",probb)
        #print("-"*20)  
        
        if probb == 0:                 # Eğer bulaş riski yoksa mesafeden ötürü fazladan random.choices çağırmamak için...
            return 0,0

        if probb != 0:

            plist = ["infected","notinfected"]
            
            if mask1 == "masked" and mask2 == "masked": secim = random.choices(plist,weights = [(1/((h**2)))*probb, 1 - (1/((h**2)))*probb], k=1)
            elif mask1 != mask2: secim = random.choices(plist, weights = [(1/h)*probb,1-((1/h)*probb)], k=1)
            elif mask1 == "notmasked" and mask1 == "notmasked": secim = random.choices(plist, weights = [probb,1-probb], k=1)
            
            return secim[0] , 2   # neden 2 return ettiğimizi alt satırlarda fark edebiliriz. 
    
    else:
        return 0, 0    # neden 0,0 return ettiğimizi alt satırlarda fark edebiliriz. 

def new_move():
    #print("-"*20)
    
    dataCopy = dataF.copy()    # dataF = universal_state idi kopyaladık 
    
    for kisi in dataF:
        #print("Çıktı: ", hareket(kisi),"Type: ",type( hareket(kisi)))   
        
        yeniKoordinat,moveType = hareket(kisi)
        
        #print("Koor: ",yeniKoordinat)
        #print("Type: ",moveType)
        
        kisi[0] = yeniKoordinat
        kisi[1] = moveType           # insanları HAREKET ETTİRDİK VE YENİ last_move ( hareket biçimi ) koyduk kişilere

    for idx1 in range(len(dataCopy)-1):
        infectedDurum = infected(dataCopy[idx1],dataCopy[idx1+1])    # kendisinden sonra gelen bireylerle ilişkisini incelemek için infected() fonksiyonuna soktuk kişileri. 
        infecDurum , kisisayi, = infectedDurum   # infected() fonksiyonunun döndüğü 0, 2, 1 gibi değerler burada anlam kazanıyor 
  
        if infecDurum == 0:      # Burası şunun için, örneğin elimizde 4 kişi olsun --> kodumuz 1-2, 1-3, 1-4 incelemesi yapacağından mesla 1-2 ilişkisinden hastalık kapan 1. bireyin, diğer "for loop" dan meslea 1-3 den hastalık kapmadığı durum için, "hastalık kaptı"" halini "hasta değil" haline geri döndürmeyi engellemek için. bir diğer deyişle, anlamsız bir overwrite yapmamak adına    
            pass
        else:
            if kisisayi == 1 and dataF[idx1][3] != "infected": dataF[idx1][3] = infecDurum  # Hala hasta değilse overwrite(güncelleme) yapabilirsin. Ama arada bir yerde hasta olduysan artık "infected" halini güncelleme ! ... 
            elif kisisayi == 2 and dataF[idx1+1][3] != "infected": dataF[idx1+1][3] = infecDurum
    
    #print("data: ",data)
    
    return dataF  #yeni universal_state'i döndük. 



#for i in range(10):
    #data = new_move()
    #print(data)
    #print("-"*30)