import struct


def main_work_two(x,wid,r,g,b):
    darkness_scale = [' ', '.', '-', ',', '~', ':', ';', '=', '!', '*', '#', '%'
                      , 'i', 'j', 'L', '8', '&', 'Q', 'M', 'W', 'B', 'O', 'X','D','N', '@']
    mix = (( r + g + b ) / 3)/10 
    mix = round( mix )
    file_ascii = open("img_but_in_ascii_form.txt",'a')
    if(x!=wid-1):
        file_ascii.write(darkness_scale[mix])
    else:
        file_ascii.write(f"{darkness_scale[mix]}\n")
    file_ascii.close()


def invers_and_fix():
    file_ascii = open("img_but_in_ascii_form.txt",'r')
    file_asciiw = open("img_but_in_ascii_form2.txt",'w')
    ch=file_ascii.read()
    while ch!="":
        file_asciiw.write(ch[::-1])
        ch=file_ascii.read()
    file_asciiw.close()
    file_ascii.close()
    file_ascii = open("img_but_in_ascii_form2.txt",'r')
    file_asciiw = open("img_but_in_ascii_form.txt",'w')
    ch=file_ascii.read()
    while ch!="":
        file_asciiw.write(ch)
        ch=file_ascii.read()
    file_asciiw.close()
    file_ascii.close()
    
def img(path):
    file_ascii = open("img_but_in_ascii_form.txt",'w')
    file_ascii.close()
    # Suppose we have a byte sequence: 0x01 0x00 0x02 0x00 0x0A 0x00 0x00 0x00
    # It represents two 16-bit (2-byte) unsigned integers and one 32-bit (4-byte) unsigned integer

    binary_data = b'\x01\x00\x02\x00\x0A\x00\x00\x00'

    # Use struct.unpack to extract the integers
    # 'H' represents 2-byte unsigned integers, 'I' represents a 4-byte unsigned integer
    values = struct.unpack('HHI', binary_data)

    print(values)  # Output: (1, 2, 10)


    # reading the photo ? : my idea is using reding as binary and read every character
    img_file = open(path,"rb") 


    #read 14 bit file header and then read 40 bit info header
    file_header = img_file.read(14)
    file_info = img_file.read(40)


    print(file_header) # output: b'BM\x8a{\x0c\x00\x00\x00\x00\x00\x8a\x00'


    file_type = struct.unpack("H",file_header[0:2])[0]
    file_size = struct.unpack("I",file_header[2:6])[0]
    offset_data = struct.unpack("I",file_header[10:14])[0]


    print(file_info) # output: <_io.BufferedReader name='sample_640 426.bmp'>


    width = struct.unpack("I",file_info[4:8])[0]
    height = struct.unpack("I",file_info[8:12])[0]
    bit_count=struct.unpack("H",file_info[14:16])[0]
    
    # Ensure it's a valid BMP file

    if(file_type != 0x4D42):
        print("Error: Not a valid BMP file.")
        return


    # Ensure it is a 24-bit BMP file
    if bit_count != 24:
        print("Error: Only 24-bit BMP files are supported.")
        return


    print(f"file_size: {file_size}")
    print(f"file_type: {file_type}")
    print(f"file_offset: {offset_data}")
    print(f"Image dimensions: {width}x{height}")
    print(f"Bit depth: {bit_count}-bit")

    # Seek to the beginning of pixel data
    img_file.seek(offset_data)

    # Calculate row padding (each row must be aligned to a multiple of 4 bytes)
    row_padding = ( 4 - ( width * 3 ) % 4 ) % 4

    # pixel loop

    for y in range(height):
        row = img_file.read(width*3)
        for x in range(width):
            blue=row[x*3]
            green=row[x*3+1]
            red=row[x*3+2]
#            print(f"Pixel ({x},{y}) : Red : {red} Green : {green} Blue : {blue}")
            main_work_two(x,width,red,green,blue)
        img_file.read(row_padding)
        print(f"The file is in part: {round((y*100)/height)} %")
    img_file.close()

    invers_and_fix()

if(__name__=="__main__"):
    img("images.bmp")