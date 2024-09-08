def Writer(file,message): # Копируем изображение и добавляем в конец zip файл или текс.
    original = open(file, "rb")
    redacted = open("redacted-"+file, "ab")

    redacted.write(original.read())
    redacted.write(message)
    redacted.close()
    original.close()

def Printer(file): # Находим расширение файла. Если png - считать от [[end] png], если jpg\jpeg считать от [[end] jpg\jpeg]. Все окончания есть в конце программы.
    dot = file.index(".")
    extension = file[dot:]


    original = open(file,"rb")

    b = original.read()
    b = b.hex()

    if extension == ".jpg" or ".jpeg":
        list = []
        o = 0
        for i in range(len(b)):
            if b[i:i+4] == "ffd9":
                list.append(i)
            o += 1
    if extension == ".png":
        list = []
        o = 0
        for i in range(len(b)):
            if b[i:i + 24] == "0000000049454e44ae426082":
                list.append(i)
            o += 1
    else:
        print("Uncorrectly extension!!!")
        exit(0)
    original.close()

    return bytes.fromhex(b[list[-1]+24:])

print("You can write [M]essage or add [Z]ip file.")# Выберем режим.
mod = input("Input mod [M/Z]:   ")
row = input("Input [R]ead or [W]rite "+mod+" [W/R]:    ")
mod = mod.upper()
row = row.upper()

if mod == "Z" and row == "W":
    zfile = input("Input path + ZIP file:   ")
    ifile = input("Input path + IMAGE file:   ")
    z = open(zfile,"rb")
    Writer(ifile,z.read())
    z.close()
if mod == "M" and row == "W":
    ifile = input("Input path + IMAGE file:   ")
    im = input("Input message:   ")
    im = bytes(im, 'utf-8')
    Writer(ifile, im)
if mod == "M" and row == "R":
    redacted = input("Input path + redacted IMAGE:   ")
    print(Printer(redacted))
if mod == "Z" and row == "R":
    hided = input("Input path + redacted IMAGE:   ")

    dot = hided.index(".")
    z = hided[:dot]+"-hided"+".zip"

    hzip = open(z,"wb") # Заменим расширение на zip. Иначе наш зип архив будет иметь расширение png\jpg
    hzip.write(Printer(hided)) # Создадим новый зип файл из выгруженных данных из изображения.
    hzip.close()
else:
    print("Uncorrectly mod!!!")
    exit(0)

#end jpg\jpeg
#ffd9

#begin jpg\jpeg
#ffd8

#end png
#0000000049454e44ae426082

#begin png
#89504e470d0a1a0a0000000d4948445200000
