# PIL module is used to extract pixels of image and modify them
# To encode a file, use the PNG format, JPEG will result in a bad decoding due to it compressing the image
import argparse
from PIL import Image

# Convert encoding data into 8-bit binary from using ASCII value of characters
def genData(data):
    """
    genData Function

    Args:
        data (string): Data to insert into the file

    Returns:
        newData: Data in binary format
    """

    # list of binary codes from the given data
    newData = []

    # Formatting into 8 bit binary
    for i in data:
        newData.append(format(ord(i), '08b'))
    # Return data in binary format
    return newData


# Pixels are modified according to the 8-bit binary data and finally returned
def modifyPixels(pixels, data):
    """
    modifyPixels Function
    Args:
        pixels (data): Passed data from new Image
        data (str): data to insert into the image

    """

    dataList = genData(data)

    # Getting the length of the list returned from genData
    dataLen = len(dataList)
    imdata = iter(pixels)

    for i in range(dataLen):

        # Extracting 3 pixels at a time
        pixels = [value for value in imdata.__next__()[:3] +
                                imdata.__next__()[:3] +
                                imdata.__next__()[:3]]

        # Pixel value should be made odd for 1 and even for 0
        for j in range(0, 8):
            if (dataList[i][j] == '0' and pixels[j]% 2 != 0):
                pixels[j] -= 1

            elif (dataList[i][j] == '1' and pixels[j] % 2 == 0):
                if(pixels[j] != 0):
                    pixels[j] -= 1
                else:
                    pixels[j] += 1

        # Eighth pixel of every set tells whether to stop or read further. 0 means keep reading; 1 means the message is over.
        if (i == dataLen - 1):
            if (pixels[-1] % 2 == 0):
                if(pixels[-1] != 0):
                    pixels[-1] -= 1
                else:
                    pixels[-1] += 1
        else:
            if (pixels[-1] % 2 != 0):
                pixels[-1] -= 1

        pixels = tuple(pixels)

        # Yield does the same thing as return, except it returns a generator instead of a function
        yield pixels[0:3]
        yield pixels[3:6]
        yield pixels[6:9]


def encode_enc(newImage, data):
    """
    encode_enc Function

    Args:
        newImage (file): Newly created image file
        data (str): data to add into the encoding
    """
    # Getting the size of the image
    width = newImage.size[0]

    # Assigning x & y to hold 0 and 0
    (x, y) = (0, 0)

    for pixel in modifyPixels(newImage.getdata(), data):

        # Putting modified pixels in the new image
        newImage.putpixel((x, y), pixel)
        if (x == width - 1):
            x = 0
            y += 1
        else:
            x += 1


# Encode data into image
def encode(img, newImageName, data):
    """
    encode Function
    Args:
        img (file): Original file to copy.
        newImageName (str): New name to save the file as.
        data (str): Data to hide in the file.

    Raises:
        ValueError: If data is empty
    
    Returns:
        Success: If file was succesfully encoded it will create a new file using whatever name was specified.
    """
    # Opens the image as read-only
    image = Image.open(img, 'r')

    # Throws an error if data is None or empty
    if (len(data) == 0):
        raise ValueError('Data is empty')

    # Copying the image and starting the encoding process
    newImage = image.copy()
    encode_enc(newImage, data)

    # Saving the newly generated file with the message hidden
    newImage.save(newImageName, str(newImageName.split(".")[1].upper()))


# Decode the data in the image
def decode(img):
    """
    decode Function
    Args:
        img (file): File to decode message from.

    Returns:
        String: Returns the decoded message from the image file.
    """
    # Opens the image as read-only
    image = Image.open(img, 'r')

    data = ''
    imgdata = iter(image.getdata())

    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                                imgdata.__next__()[:3] +
                                imgdata.__next__()[:3]]

        # string of binary data
        binstr = ''

        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        # Creating the characters from binary input
        data += chr(int(binstr, 2))

        # Breaks out of the while loop if this condition is met, meaning there is no more to decode.
        if (pixels[-1] % 2 != 0):
            return data


# Main Function
def main():
    # Defining the argument parser for specifying arguments
    parser = argparse.ArgumentParser('Steganography Tool')

    # Allows users to decode files (Defaults to True)
    parser.add_argument("-d", '--decode', type=bool, default=True,
                        help='Decode a file containing Steganography.')

    # Allows users to encode files (Defaults to False)
    parser.add_argument("-e", '--encode', type=bool, default=False,
                        help='Encode a file with Steganography.')

    # Allows users to specify a file to encode or decode (Required)
    parser.add_argument("-f", '--file', type=str, required=True,
                        help='File to decode or encode.')
    
    # Allows users to specify a message to encode into the file (Required for -e)
    parser.add_argument("-i", '--insert', type=str, 
                        help='Data to insert into the file.')

    # Allows users to specify an output file for the newly created image (Required for -e)
    parser.add_argument("-o", '--outfile', type=str,
                        help='File to output the generated Steganography file to. (EX: test.png)')
    
    # Args variable holds all the arguments passed to the script
    args = parser.parse_args()

    # If encode is True, check the length of insert to verify that data is not empty
    if args.encode == True:
        if len(str(args.insert)) != 0:
            # Check the length of the output file to make sure it is defined
            if args.outfile != "":
                if args.insert != "":
                    # If all conditions are met, we're positive the user wants to encode a file
                    encode(args.file, args.outfile, args.insert)
                    print('Succesfully encoded the file.')
                else:
                    print('Error.')
            else:
                print('Error')
    
    # Otherwise, if decode is True, decode the file.
    else:
        print(f'Decoded: {decode(args.file)}')
                        

# Main run code
if __name__ == '__main__' :
    # Calling the main function to start the script
    main()