import sys, os


def init():
    global subjectID
    filename = str(subjectID) + "-bisbas.txt"
    f = open(filename, 'w')
    output = 'subjectID,question,answer\n'
    f.write(output)
    f.close()

    global items
    items = ["Familie is het belangrijkste in iemands leven",
             "Ik voel zelden angst of zenuwen, zelfs als me iets vervelends staat te wachten",
             "Ik zal over mijn grenzen heen gaan om de dingen te krijgen die ik wil",
             "Als ik iets goed doe, wil ik er graag mee doorgaan",
             "Ik ben altijd bereid iets nieuws te proberen als ik denk dat het leuk zal zijn",
             "Kleren zijn belangrijk voor me",
             "Als ik krijg wat ik wil, voel ik me me opgewonden en energiek",
             "Kritiek of uitbranders raken mij behoorlijk",
             "Als ik iets wil, zal ik er gewoonlijk alles aan doen om dit te krijgen",
             "Vaak doe ik dingen alleen voor de lol",
             "Ik heb vaak weinig tijd om dingen te doen",
             "Als ik de kans zie iets te krijgen wat ik wil, zal ik die kans meteen grijpen",
             "Ik voel me bezorgd of overstuur als ik denk of weet dat iemand boos op mij is",
             "Als ik ergens een buitenkansje zie dan word ik meteen enthousiast",
             "Ik doe vaak dingen in een vlaag van opwelling",
             "Ik raak enigszins gestrest als ik denk dat er iets vervelends staat te gebeuren",
             "Ik vraag me vaak af waarom mensen doen zoals ze doen",
             "Als ik iets leuks meemaak heeft dat duidelijk invloed op me",
             "Ik voel me bezorgd als ik denk dat ik slecht heb gepresteerd",
             "Ik verlang naar spanning en sensatie",
             "Als ik iets van plan ben dan laat ik mij door niets weerhouden",
             "Ik ervaar weinig angsten vergeleken met mijn vrienden",
             "Als ik een wedstrijd zou winnen, zou ik erg enthousiast zijn",
             "Ik pieker wel eens over het maken van fouten"]


def present_intro():
    print ("\n" * 100)
    print "In de komende schermen ziet u een aantal stellingen staan waar u het mee eens of oneens kan zijn. "
    print "Geef voor elke stelling aan in welke mate u het ermee eens of oneens bent."
    print "Beantwoord alle stellingen, sla er geen over. Per stelling is slechts 1 antwoord mogelijk."
    print "Probeer zo eerlijk mogelijk antwoord te geven, er zijn geen goede of foute antwoorden. "
    print "Beantwoord elke stelling alsof het de enige stelling zou zijn. "
    print "Met andere woorden, u hoeft geen rekening te houden met uw vorige antwoorden.\n\n"
    print "Druk op ENTER om te beginnen..."


def present_item(itemNum):
    global items
    global subjectID
    print ("\n" * 100)
    print items[itemNum]
    print "\n"
    print("1 = Helemaal mee oneens")
    print("2 = Beetje mee oneens")
    print("3 = Beetje mee eens")
    print("4 = Helemaal mee eens")
    answer = raw_input("In hoeverre bent u het met deze stelling eens? ")

    filename = str(subjectID) + "-bisbas.txt"
    f = open(filename, 'a')
    output = str(subjectID) + "," + str(itemNum+1) + "," + str(answer) + "\n"
    f.write(output)
    f.close()


if __name__ == "__main__":
    global subjectID
    subjectID = str(sys.argv[1])
    init()
    present_intro()

    for i in range(24):
        present_item(i)