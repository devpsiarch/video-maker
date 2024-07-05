import os
from PIL import Image

def write_id(id):
    with open('ids.txt','a') as f:
        f.write(id)
        f.write("\n")

#return true if the id is in the ides log file and false if there isnt an id match (we can make a video fro that id)
def get_ides():
    # open the data file
    file = open("ids.txt")
    # read the file as a list
    data = file.readlines()
    ides = [i[:-1] for i in data]
    file.close()
    return ides


def assert_png(id):
    directory = 'temp'

    # Define the specific PNG file you are looking for
    specific_file = f'{id}.png'

    # Check if the specific file exists in the directory
    if os.path.exists(os.path.join(directory, specific_file)):
        print(f"{specific_file} exists in the directory.")
        return True
    else:
        return False

def temp_clear():
    directory = "temp"
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')
    print("temp cleared")


def crop_image(path,size):
    print("croping image taken ...")
    image = Image.open(path)
    # Calculate the crop box
    width, height = image.size
    right = width - size # Adjust the right coordinate by 50 pixels
    left = 0
    top = 0
    bottom = height
    # Crop the image and save the cropped screenshot
    cropped_image = image.crop((left, top, right, bottom))
    cropped_image.save(path)
    image.close()



