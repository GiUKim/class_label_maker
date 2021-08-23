from glob import glob
import cv2
import numpy as np
import os
import sys

def checkListEqual(list1, list2):
    if len(list1) != len(list2):
        return False
    else:
        for idx in range(0, len(list1)):
            if list1[idx] != list2[idx]:
                return False
    return True

def put_text_classes(category_list, toolbox, checkbox):
    font = cv2.FONT_HERSHEY_SIMPLEX
    bold = [1, 2]
    bold_list = []
    for cls in category_list:
        if cls.find(search_key) >= 0 and search_key is not "":
            bold_list.append(1)
        else:
            bold_list.append(0)

    if len(globals()[category + '_list']) < 18:
        for idx in range(0, len(category_list)):
            if checkbox[idx] == 1:
                cv2.putText(toolbox, category_list[idx], (10, 40 + 27 + 40 * idx), font, 0.8, (0, 0, 0), bold[bold_list[idx]], cv2.LINE_AA)
            elif checkbox[idx] == -1:
                cv2.putText(toolbox, category_list[idx], (10, 40 + 27 + 40 * idx), font, 0.8, (0, 255, 0), bold[bold_list[idx]], cv2.LINE_AA)

    elif len(globals()[category + '_list']) < 36:
        for idx in range(0, 18):
            if checkbox[idx] == 1:
                cv2.putText(toolbox, category_list[idx], (10, 27 + 40 * idx), font, 0.8, (0, 0, 0), bold[bold_list[idx]], cv2.LINE_AA)
            elif checkbox[idx] == -1:
                cv2.putText(toolbox, category_list[idx], (10, 27 + 40 * idx), font, 0.8, (0, 255, 0), bold[bold_list[idx]], cv2.LINE_AA)
        for idx in range(18, len(category_list)):
            if checkbox[idx] == 1:
                cv2.putText(toolbox, category_list[idx], (320 + 10, 27 + 40 * (idx % 18)), font, 0.8, (0, 0, 0), bold[bold_list[idx]], cv2.LINE_AA)
            elif checkbox[idx] == -1:
                cv2.putText(toolbox, category_list[idx], (320 + 10, 27 + 40 * (idx % 18)), font, 0.8, (0, 255, 0), bold[bold_list[idx]], cv2.LINE_AA)
    else:
        for idx in range(0, 18):
            if checkbox[idx] == 1:
                cv2.putText(toolbox, category_list[idx], (10, 40 + 27 + 40 * idx), font, 0.8, (0, 0, 0), bold[bold_list[idx]], cv2.LINE_AA)
            elif checkbox[idx] == -1:
                cv2.putText(toolbox, category_list[idx], (10, 40 + 27 + 40 * idx), font, 0.8, (0, 255, 0), bold[bold_list[idx]], cv2.LINE_AA)
        for idx in range(18, 36):
            if checkbox[idx] == 1:
                cv2.putText(toolbox, category_list[idx], (320 + 10, 40 + 27 + 40 * (idx % 18)), font, 0.8, (0, 0, 0), bold[bold_list[idx]], cv2.LINE_AA)
            elif checkbox[idx] == -1:
                cv2.putText(toolbox, category_list[idx], (320 + 10, 40 + 27 + 40 * (idx % 18)), font, 0.8, (0, 255, 0), bold[bold_list[idx]], cv2.LINE_AA)
        for idx in range(36, len(category_list)):
            if checkbox[idx] == 1:
                cv2.putText(toolbox, category_list[idx], (640 + 10, 40 + 27 + 40 * (idx % 18)), font, 0.8, (0, 0, 0), bold[bold_list[idx]], cv2.LINE_AA)
            elif checkbox[idx] == -1:
                cv2.putText(toolbox, category_list[idx], (640 + 10, 40 + 27 + 40 * (idx % 18)), font, 0.8, (0, 255, 0), bold[bold_list[idx]], cv2.LINE_AA)
    return toolbox

def draw_Toolbox_Realtime(toolbox, checkbox):
    count = 0
    for i in toolbox:
        if (count + 1) % 40 == 0:
            for pixel in i:
                pixel[0] = 0
                pixel[1] = 0
                pixel[2] = 0
        count += 1
        if count == 720:
            break

    if len(globals()[category + '_list']) > 18 and len(globals()[category + '_list']) <= 36:
        for i in range(0, 720):
            toolbox[i][319] = 0
    elif len(globals()[category + '_list']) <= 54:
        for i in range(0, 720):
            toolbox[i][319] = 0
            toolbox[i][639] = 0


    toolbox = put_text_classes(globals()[category+'_list'], toolbox, checkbox)
    return toolbox

def mouse_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN and x > 960:
        if len(globals()[category + '_list']) <= 18:
            checkbox[cur_idx][y // 40 -1] *= -1
            toolbox = 255 * np.ones((720, 320, 3), np.uint8)
        elif len(globals()[category + '_list']) <= 36:
            if x < 1280:
                checkbox[cur_idx][y // 40- 1 ] *= -1
            else:
                checkbox[cur_idx][18 + y // 40 - 1] *= -1
            toolbox = 255 * np.ones((720, 640, 3), np.uint8)
        elif len(globals()[category + '_list']) <= 54:
            if x < 1280:
                checkbox[cur_idx][y // 40] *= -1
            elif x < 1600:
                checkbox[cur_idx][18 + y // 40] *= -1
            elif x < 1920:
                checkbox[cur_idx][36 + y // 40] *= -1
            toolbox = 255 * np.ones((720, 960, 3), np.uint8)
        toolbox = draw_Toolbox_Realtime(toolbox, checkbox[cur_idx])
        img_array = np.fromfile(data[cur_idx], np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        img = padding_Resize(img, (720, 960))
        img = np.hstack((img, toolbox))
        search_box = 255 * np.ones((40, img.shape[1], 3), np.uint8)

        for line in search_box:
            line[959] = 1
        img = np.vstack((search_box, img))
        cv2.putText(img, 'filename: '+data[cur_idx].split('\\')[-1], (10, 27), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1, cv2.LINE_AA)
        if search_key is not "":
            cv2.putText(img, search_key, (960 + 10, 27), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
        else:
            cv2.putText(img, "search:", (960 + 10, 27), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
        line = np.zeros((1600, 3), np.uint8)
        img[39] = np.copy(line)
        cv2.imshow('label', img)

def padding_Resize(img, max_size):
    if img.shape == max_size:
        return img
    else:
        if img.shape[0] > max_size[0] or img.shape[1] > max_size[1]:
            shrink_start = 1.0
            shrink_step = 0.05
            height = img.shape[0]
            width = img.shape[1]
            while True:
                if width < 960 and height < 720:
                    break
                shrink_start = shrink_start - shrink_step
                height = img.shape[0] * shrink_start
                width = img.shape[1] * shrink_start
            img = cv2.resize(img, None, None, fx=shrink_start, fy=shrink_start)

        else:
            zoom_start = 1.0
            zoom_step = 0.05
            height = img.shape[0]
            width = img.shape[1]
            while True:
                if height > 720 or width > 960:
                    break
                zoom_start = zoom_start + zoom_step
                height = img.shape[0] * zoom_start
                width = img.shape[1] * zoom_start
            zoom_start = zoom_start - zoom_step
            img = cv2.resize(img, None, None, fx=zoom_start, fy=zoom_start)

        bh = int((720 - img.shape[0]) / 2)
        th = (720 - img.shape[0]) - bh
        lw = int((960 - img.shape[1]) / 2)
        rw = (960 - img.shape[1]) - lw

        # horizontal padding
        horizontal_padding_box_left = np.ones((img.shape[0], lw, 3), dtype=np.uint8)
        horizontal_padding_box_right = np.ones((img.shape[0], rw, 3), dtype=np.uint8)
        img = np.hstack((np.hstack((horizontal_padding_box_left, img)), horizontal_padding_box_right))

        # vertical padding
        vertical_padding_box_top = np.ones((th, img.shape[1], 3), dtype=np.uint8)
        vertical_padding_box_bottom = np.ones((bh, img.shape[1], 3), dtype=np.uint8)
        img = np.vstack((np.vstack((vertical_padding_box_top, img)), vertical_padding_box_bottom))
        return img

def save_label(filename, checkbox):
    f = open(filename.split('\\')[-1].split('.')[0]+'.txt', 'w+')
    for label in checkbox:
        if label == -1:
            f.write('1\n')
        elif label == 1:
            f.write('0\n')

head_list = ['longhair', 'longhair_cap', 'longhair_glass', 'longhair_glass_mask', 'longhair_hat',
             'longhair_helmet', 'longhair_mask', 'longhair_siga', 'shorthair', 'shorthair_cap',
             'shorthair_glass', 'shorthair_glass_mask', 'shorthair_hat', 'shorthair_helmet',
             'shorthair_mask', 'shorthair_siga', 'umbrella', 'longhair_mask', 'longhair_siga', 'shorthair', 'shorthair_cap',
             'shorthair_glass', 'shorthair_glass_mask']
top_list = ['longshirt', 'longshirt_backpack', 'longshirt_crossbag', 'longshirt_handbag',
            'shortshirt', 'shortshirt_backpack', 'shortshirt_crossbag', 'shortshirt_handbag']
bottom_list = ['longpants', 'longpants_shoes', 'longpants_slipper', 'shortpants', 'shortpants_shoes',
               'shortpants_slipper', 'skirt', 'skirt_shoes', 'skirt_slipper']
umbrella_list = ['umbrella']
handbag_list = ['handbag', 'not_handbag', 'umbrella']
foot_list = ['shoose', 'slipper']

category = sys.argv[1]
data = glob(os.getcwd() + '/*.jpg')

# create checkbox of all images
checkbox = []
search_key = ""
for num in range(0, len(data)):
    if os.path.isfile(data[num].split('\\')[-1].split('.')[0]+'.txt'):
        f = open(data[num].split('\\')[-1].split('.')[0]+'.txt', 'r')
        lines = f.readlines()
        sub_check = []
        for l in lines:
            if l.split('\n')[0] == '0':
                sub_check.append(1)
            else:
                sub_check.append(-1)
        checkbox.append(sub_check)

    else:
        checkbox.append(np.ones(len(globals()[category+'_list'])))

cur_idx = 0
while True:
    img = data[cur_idx]
    if len(globals()[category + '_list']) <= 18:
        toolbox = 255 * np.ones((720, 320, 3), np.uint8)
    elif len(globals()[category + '_list']) <= 36:
        toolbox = 255 * np.ones((720, 640, 3), np.uint8)
    elif len(globals()[category + '_list']) <= 54:
        toolbox = 255 * np.ones((720, 960, 3), np.uint8)
    toolbox = draw_Toolbox_Realtime(toolbox, checkbox[cur_idx])
    org_checkbox = checkbox[cur_idx].copy()
    img_array = np.fromfile(img, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    img = padding_Resize(img, (720, 960))
    img = np.hstack((img, toolbox))

    search_box = 255 * np.ones((40, img.shape[1], 3), np.uint8)

    for line in search_box:
        line[959] = 1
    img = np.vstack((search_box, img))
    if search_key is not "":
        cv2.putText(img, search_key, (960 + 10, 27), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
    else:
        cv2.putText(img, "search:", (960 + 10, 27), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1, cv2.LINE_AA)

    cv2.putText(img, 'filename: '+data[cur_idx].split('\\')[-1], (10, 27), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1, cv2.LINE_AA)
    line = np.zeros((1600, 3), np.uint8)
    img[39] = np.copy(line)

    cv2.imshow('label', img)
    cv2.setMouseCallback('label', mouse_event, img)
    key = cv2.waitKey()
    if key == ord(','):
        if cur_idx > 0:
            if not checkListEqual(org_checkbox, checkbox[cur_idx]) or len(globals()[category+'_list']) == 1:
                save_label(data[cur_idx], checkbox[cur_idx])
                print('save file:', data[cur_idx].split('\\')[-1].split('.')[0]+'.txt')
            cur_idx -= 1
    elif key == ord('.'):
        if cur_idx < len(data) - 1:
            if not checkListEqual(org_checkbox, checkbox[cur_idx]) or len(globals()[category+'_list']) == 1:
                save_label(data[cur_idx], checkbox[cur_idx])
                print('save file:', data[cur_idx].split('\\')[-1].split('.')[0] + '.txt')
            cur_idx += 1
        elif cur_idx == len(data) - 1:
            if not checkListEqual(org_checkbox, checkbox[cur_idx]) or len(globals()[category+'_list']) == 1:
                save_label(data[cur_idx], checkbox[cur_idx])
                print('save file:', data[cur_idx].split('\\')[-1].split('.')[0] + '.txt')
            cur_idx = 0
    elif key == 27:
        break
    elif key == 8:
        search_key = search_key[:-1]
    else:
        search_key += chr(key)