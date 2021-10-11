import torch
import argparse
import cv2
import os
import json
import requests
import urllib.request
from google_drive_downloader import GoogleDriveDownloader as gdd

MOSAIC_RATIO = 0.05

def check_config(path='./config.json'):
    if os.path.exists(path):
        with open(path) as json_file:
            json_data = json.load(json_file)
        
        if 'matrix' in json_data.keys(): return
    
    json_data = {"matrix": 0}
    with open(path, 'w') as outfile:
        json.dump(json_data, outfile)

def attemp_download_weight():
    if not os.path.exists('./weight'): os.makedirs('./weight')
    
    config_path = './config.json'
    check_config(config_path)
    
    try:
        with open(config_path) as json_file:
            json_data = json.load(json_file)
        
        data = requests.get("http://3.143.240.128:8080/deeplearning/models", timeout=1).json()
        matrix = data['matrix']
        model_url = data['file']
        
        if json_data['matrix'] < matrix or not os.path.exists('weight/yolov5m6.pt'):
            print('download file from django...')
            json_data['matrix'] = matrix
            with open('./config.json', 'w') as json_file: json.dump(json_data, json_file)
            
            
            urllib.request.urlretrieve(model_url, 'weight/yolov5m6.pt') 
            
    except:       
        print('download file from google drive...')
        yolov5m6_id = '1QUaufxw06NVPyn_tIm0qBdOy5ewQ5ffi'
        gdd.download_file_from_google_drive(file_id=yolov5m6_id, dest_path=f'weight/yolov5m6.pt', showsize=True)

    

# def mosaic()

def detect(args):
# Model
    input_image_path = args.input_image_path
    output_image_path = args.output_image_path
    weight_path = args.weight_path
    activeBlur = args.blur
    # strength = args.strength
    output_warning_path = args.output_warning_path
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=weight_path)

    # Inference
    results = model(input_image_path)
    img = cv2.imread(input_image_path)
    CLASS_LIST = ['항공모함', '방탄조끼', '포', '모니터', '군용 차량', '노트북', '군복', '미사일', '모니터', '서류', '부대마크', '리볼버', '소총', '탱크', '군 항공기', '군 표지판']

    if activeBlur == True:
        # TODO : Blur
        print("Not yet!")
    else:
        warn_list = []
        for xmin, ymin, xmax, ymax, conf, class_num in results.xyxy[0]:
            class_num = int(class_num)
            if class_num >= 16: continue
            warn_list.append(CLASS_LIST[class_num])
            if class_num == 6:
                print("Military uniform is detected. Pass mosaic")
                continue


            xmin = int(xmin); xmax = int(xmax); ymin = int(ymin); ymax = int(ymax)
            src = img[ymin: ymax, xmin: xmax]   # 관심영역 지정


            small = cv2.resize(src, None, fx=MOSAIC_RATIO, fy=MOSAIC_RATIO, interpolation=cv2.INTER_NEAREST)
            src = cv2.resize(small, src.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)
            
            img[ymin: ymax, xmin: xmax] = src   # 원본 이미지에 적용
        cv2.imwrite(output_image_path, img)
        warn_list = ','.join(list(set(warn_list)))
        if warn_list:
            # 각 객체의 조합에 따른 시나리오 추가 필요
            warn_text = f'{warn_list}이/가 감지되었습니다. 해당 사진이 보안에 저촉된다면 삭제해주시길 바랍니다.'
        else:
            warn_text = '아무런 객체가 검출되지 않았습니다.'
        with open(output_warning_path, 'w') as f:
            f.write(warn_text)




parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--input_image_path', '-i', help='Input image path')
parser.add_argument('--output_image_path', '-o', help='Output image path')
parser.add_argument('--weight_path', '-w', help='Weight path')
parser.add_argument('--blur', '-b', action="store_true")
# parser.add_argument('--strength', '-s', type='int', default=100, choices=[50, 75, 100]) # test 후 결과에 따라 강도 조정 예정 --> 찬호님이 자동 적응 mosaic 진행중
parser.add_argument('--output_warning_path', '-o2', help='Warning text path')

# TODO: arg로 mosaic 강도를 입력받고, 그 만큼 면적을 줄여서 return
# TODO: output_warning_path를 입력받아 군복, 방탄조끼 class가 포함되어 있을 시 경고문 전달? 해결


args = parser.parse_args()

attemp_download_weight()
detect(args)
