import os
import shutil
import tarfile
from shutil import copyfile

DATA_DIR = "/opt/dkube/input"
target_dir = '/tmp/dataset'

def extract():
    print(DATA_DIR)
    files = [os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR) if f.endswith('tar.gz')]
    print(files)
    for filename in files:
        print(filename)
        tar = tarfile.open(filename)
        tar.extractall(target_dir)
        tar.close()
    print("Extracted objects and stored. Location: ", target_dir)
    
def partition_train_test(source, dest, ratio, copy_xml):
    source = source.replace('\\', '/')
    dest = dest.replace('\\', '/')
    train_dir = os.path.join(dest, 'train')
    test_dir = os.path.join(dest, 'test')

    if not os.path.exists(train_dir):
        os.makedirs(train_dir)
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    images = [f for f in os.listdir(source)
              if re.search(r'([a-zA-Z0-9\s_\\.\-\(\):])+(.jpg|.jpeg|.png)$', f)]

    num_images = len(images)
    num_test_images = math.ceil(ratio*num_images)

    for i in range(num_test_images):
        idx = random.randint(0, len(images)-1)
        filename = images[idx]
        copyfile(os.path.join(source, filename),
                 os.path.join(test_dir, filename))
        if copy_xml:
            xml_filename = os.path.splitext(filename)[0]+'.xml'
            copyfile(os.path.join(source, xml_filename),
                     os.path.join(test_dir,xml_filename))
        images.remove(images[idx])

    for filename in images:
        copyfile(os.path.join(source, filename),
                 os.path.join(train_dir, filename))
        if copy_xml:
            xml_filename = os.path.splitext(filename)[0]+'.xml'
            copyfile(os.path.join(source, xml_filename),
                     os.path.join(train_dir, xml_filename))

            
def data_cleaning():
    source = target_dir+"/annotations/xmls/"
    destination = target_dir +"/images/"
    for file in os.listdir(source):
        print(file)
        break
        shutil.copy(source+file,destination)
    xml_list=[]
    images_list=[]
    
    for xml_file in os.listdir(source):
        if xml_file.endswith('.xml'):
            xml_list.append(xml_file.strip('.xml'))
    
    for image_file in os.listdir(destination):
        if image_file.endswith('jpg'):
            images_list.append(image_file.strip('.jpg'))
            
    ### generating final images and xmls
    
    final_dataset_list=list(set(xml_list)& set(images_list))
    print("length of final dataset list")
    print(len(final_dataset_list))
    print("len of xml_list")
    print(len(xml_list))
    print("len of images list")
    print(len(images_list))
    os.mkdir(target_dir+"/final_images")
     
    for file in os.listdir(target_dir +"/images/"):
        file=file.strip('.jpg')
        if file in final_dataset_list:
            shutil.copy(source+file+'.jpg',target_dir+"/final_images/")
    
    for file in os.listdir(target_dir+"/annotations/xmls/"):
        file=file.strip('.xml')
        if file in final_dataset_list:
            shutil.copy(source+file+'.xml',target_dir+"/final_images/")
            

if __name__ == '__main__':
    print("Extracting the dataset")
    extract()
    print("Cleaning the dataset")
    data_cleaning()
    print("Splitting the Dataset")
    partition_dataset_train_test('/tmp/dataset/final_images', '/tmp/dataset/images', 0.1,'store_true')
