import random
import numpy as np
import cv2
from .ACT_utils import iou2d

def random_brightness(imglist, evtlist, evtlist2, evtlist3, brightness_prob, brightness_delta):

    if random.random() < brightness_prob:
        brig = random.uniform(-brightness_delta, brightness_delta)
        for i in range(len(imglist)):
            imglist[i] += brig
            evtlist[i] += brig

            evtlist2[i] += brig
            evtlist3[i] += brig

    return imglist, evtlist, evtlist2, evtlist3


def random_contrast(imglist, evtlist, evtlist2, evtlist3, contrast_prob, contrast_lower, contrast_upper):

    if random.random() < contrast_prob:
        cont = random.uniform(contrast_lower, contrast_upper)
        for i in range(len(imglist)):
            imglist[i] *= cont
            evtlist[i] *= cont

            evtlist2[i] *= cont
            evtlist3[i] *= cont

    return imglist, evtlist, evtlist2, evtlist3


def random_saturation(imglist, evtlist, evtlist2, evtlist3, saturation_prob, saturation_lower, saturation_upper):

    if random.random() < saturation_prob:
        satu = random.uniform(saturation_lower, saturation_upper)
        for i in range(len(imglist)):
            hsv = cv2.cvtColor(imglist[i], cv2.COLOR_BGR2HSV)
            hsv[:, :, 1] *= satu
            imglist[i] = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
            hsv2 = cv2.cvtColor(evtlist[i], cv2.COLOR_BGR2HSV)
            hsv2[:, :, 1] *= satu
            evtlist[i] = cv2.cvtColor(hsv2, cv2.COLOR_HSV2BGR)

            hsv2_2 = cv2.cvtColor(evtlist2[i], cv2.COLOR_BGR2HSV)
            hsv2_2[:, :, 1] *= satu
            evtlist2[i] = cv2.cvtColor(hsv2_2, cv2.COLOR_HSV2BGR)
            hsv2_3 = cv2.cvtColor(evtlist3[i], cv2.COLOR_BGR2HSV)
            hsv2_3[:, :, 1] *= satu
            evtlist3[i] = cv2.cvtColor(hsv2_3, cv2.COLOR_HSV2BGR)

    return imglist, evtlist, evtlist2, evtlist3


def random_hue(imglist, evtlist, evtlist2, evtlist3, hue_prob, hue_delta):

    if random.random() < hue_prob:
        hue = random.uniform(-hue_delta, hue_delta)
        for i in range(len(imglist)):
            hsv = cv2.cvtColor(imglist[i], cv2.COLOR_BGR2HSV)
            hsv[:, :, 0] += hue
            imglist[i] = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
            hsv2 = cv2.cvtColor(evtlist[i], cv2.COLOR_BGR2HSV)
            hsv2[:, :, 0] += hue
            evtlist[i] = cv2.cvtColor(hsv2, cv2.COLOR_HSV2BGR)

            hsv2_2 = cv2.cvtColor(evtlist2[i], cv2.COLOR_BGR2HSV)
            hsv2_2[:, :, 0] += hue
            evtlist2[i] = cv2.cvtColor(hsv2_2, cv2.COLOR_HSV2BGR)
            hsv2_3 = cv2.cvtColor(evtlist3[i], cv2.COLOR_BGR2HSV)
            hsv2_3[:, :, 0] += hue
            evtlist3[i] = cv2.cvtColor(hsv2_3, cv2.COLOR_HSV2BGR)

    return imglist, evtlist, evtlist2, evtlist3


def apply_distort(imglist, evtlist, evtlist2, evtlist3, distort_param):

    out_imglist = imglist
    out_evtlist = evtlist

    out_evtlist2 = evtlist2
    out_evtlist3 = evtlist3

    if distort_param['random_order_prob'] != 0:
        raise NotImplementedError

    if random.random() > 0.5:
        out_imglist, out_evtlist, out_evtlist2, out_evtlist3 = random_brightness(out_imglist, out_evtlist, out_evtlist2, out_evtlist3, distort_param['brightness_prob'], distort_param['brightness_delta'])
        out_imglist, out_evtlist, out_evtlist2, out_evtlist3 = random_contrast(out_imglist, out_evtlist, out_evtlist2, out_evtlist3, distort_param['contrast_prob'], distort_param['contrast_lower'], distort_param['contrast_upper'])
        out_imglist, out_evtlist, out_evtlist2, out_evtlist3 = random_saturation(out_imglist, out_evtlist, out_evtlist2, out_evtlist3, distort_param['saturation_prob'], distort_param['saturation_lower'], distort_param['saturation_upper'])
        out_imglist, out_evtlist, out_evtlist2, out_evtlist3 = random_hue(out_imglist, out_evtlist, out_evtlist2, out_evtlist3, distort_param['hue_prob'], distort_param['hue_delta'])
    else:
        out_imglist, out_evtlist, out_evtlist2, out_evtlist3 = random_brightness(out_imglist, out_evtlist, out_evtlist2, out_evtlist3, distort_param['brightness_prob'], distort_param['brightness_delta'])
        out_imglist, out_evtlist, out_evtlist2, out_evtlist3 = random_saturation(out_imglist, out_evtlist, out_evtlist2, out_evtlist3, distort_param['saturation_prob'], distort_param['saturation_lower'], distort_param['saturation_upper'])
        out_imglist, out_evtlist, out_evtlist2, out_evtlist3 = random_hue(out_imglist, out_evtlist, out_evtlist2, out_evtlist3, distort_param['hue_prob'], distort_param['hue_delta'])
        out_imglist, out_evtlist, out_evtlist2, out_evtlist3 = random_contrast(out_imglist, out_evtlist, out_evtlist2, out_evtlist3, distort_param['contrast_prob'], distort_param['contrast_lower'], distort_param['contrast_upper'])

    return out_imglist, out_evtlist, out_evtlist2, out_evtlist3


def apply_expand(imglist, evtlist, evtlist2, evtlist3, tubes, expand_param, mean_values=None):

    # Tubes: dict of label -> list of tubes with tubes being <x1> <y1> <x2> <y2>
    out_imglist = imglist
    out_evtlist = evtlist

    out_evtlist2 = evtlist2
    out_evtlist3 = evtlist3

    out_tubes = tubes

    if random.random() < expand_param['expand_prob']:
        expand_ratio = random.uniform(1, expand_param['max_expand_ratio'])
        oh, ow = imglist[0].shape[:2]
        h = int(oh * expand_ratio)
        w = int(ow * expand_ratio)
        out_imglist = [np.zeros((h, w, 3), dtype=np.float32) for i in range(len(imglist))]
        out_evtlist = [np.zeros((h, w, 3), dtype=np.float32) for i in range(len(evtlist))]

        out_evtlist2 = [np.zeros((h, w, 3), dtype=np.float32) for i in range(len(evtlist2))]
        out_evtlist3 = [np.zeros((h, w, 3), dtype=np.float32) for i in range(len(evtlist3))]

        h_off = int(np.floor(h - oh))
        w_off = int(np.floor(w - ow))
        if mean_values is not None:
            for i in range(len(imglist)):
                out_imglist[i] += np.array(mean_values).reshape(1, 1, 3)
        for i in range(len(imglist)):
            out_imglist[i][h_off:h_off + oh, w_off:w_off + ow, :] = imglist[i]
            out_evtlist[i][h_off:h_off + oh, w_off:w_off + ow, :] = evtlist[i]

            out_evtlist2[i][h_off:h_off + oh, w_off:w_off + ow, :] = evtlist2[i]
            out_evtlist3[i][h_off:h_off + oh, w_off:w_off + ow, :] = evtlist3[i]

        # project boxes
        for ilabel in tubes:
            for itube in range(len(tubes[ilabel])):
                out_tubes[ilabel][itube] += np.array([[w_off, h_off, w_off, h_off]], dtype=np.float32)

    return out_imglist, out_evtlist, out_evtlist2, out_evtlist3, out_tubes


def sample_cuboids(tubes, batch_samplers, imheight, imwidth):
    sampled_cuboids = []
    for batch_sampler in batch_samplers:
        max_trials = batch_sampler['max_trials']
        max_sample = batch_sampler['max_sample']
        itrial = 0
        isample = 0
        sampler = batch_sampler['sampler']

        min_scale = sampler['min_scale'] if 'min_scale' in sampler else 1
        max_scale = sampler['max_scale'] if 'max_scale' in sampler else 1
        min_aspect = sampler['min_aspect_ratio'] if 'min_aspect_ratio' in sampler else 1
        max_aspect = sampler['max_aspect_ratio'] if 'max_aspect_ratio' in sampler else 1

        while itrial < max_trials and isample < max_sample:
            # sample a normalized box
            scale = random.uniform(min_scale, max_scale)
            aspect = random.uniform(min_aspect, max_aspect)
            width = scale * np.sqrt(aspect)
            height = scale / np.sqrt(aspect)
            if width > 1 or height > 1:
                continue
            x = random.uniform(0, 1 - width)
            y = random.uniform(0, 1 - height)

            # rescale the box
            sampled_cuboid = np.array([x * imwidth, y * imheight, (x + width) * imwidth, (y + height) * imheight], dtype=np.float32)
            # check constraint
            itrial += 1
            if not 'sample_constraint' in batch_sampler:
                sampled_cuboids.append(sampled_cuboid)
                isample += 1
                continue

            constraints = batch_sampler['sample_constraint']
            ious = np.array([np.mean(iou2d(t, sampled_cuboid)) for t in sum(tubes.values(), [])])
            if ious.size == 0:  # empty gt
                isample += 1
                continue

            if 'min_jaccard_overlap' in constraints and ious.max() >= constraints['min_jaccard_overlap']:
                sampled_cuboids.append(sampled_cuboid)
                isample += 1
                continue

            if 'max_jaccard_overlap' in constraints and ious.min() >= constraints['max_jaccard_overlap']:
                sampled_cuboids.append(sampled_cuboid)
                isample += 1
                continue

    return sampled_cuboids


def crop_image(imglist, evtlist, evtlist2, evtlist3, tubes, batch_samplers):

    candidate_cuboids = sample_cuboids(tubes, batch_samplers, imglist[0].shape[0], imglist[0].shape[1])

    if not candidate_cuboids:
        return imglist, evtlist, evtlist2, evtlist3, tubes

    h = imglist[0].shape[0]
    w = imglist[0].shape[1]
    crop_cuboid = random.choice(candidate_cuboids)
    x1, y1, x2, y2 = map(int, crop_cuboid.tolist())

    for i in range(len(imglist)):
        imglist[i] = imglist[i][y1:y2 + 1, x1:x2 + 1, :]
        evtlist[i] = evtlist[i][y1:y2 + 1, x1:x2 + 1, :]

        evtlist2[i] = evtlist2[i][y1:y2 + 1, x1:x2 + 1, :]
        evtlist3[i] = evtlist3[i][y1:y2 + 1, x1:x2 + 1, :]

    out_tubes = {}
    wi = x2 - x1
    hi = y2 - y1
    # if x1<0 or x2>w or y1<0 or y2>h:
    #    print('error:')
    #    print(x1,y1,x2,y2)
    #    print(imglist[0].shape)

    for ilabel in tubes:
        for itube in range(len(tubes[ilabel])):
            t = tubes[ilabel][itube]
            t -= np.array([[x1, y1, x1, y1]], dtype=np.float32)

            # check if valid
            cx = 0.5 * (t[:, 0] + t[:, 2])
            cy = 0.5 * (t[:, 1] + t[:, 3])

            if np.any(cx < 0) or np.any(cy < 0) or np.any(cx > wi) or np.any(cy > hi):
                continue

            if not ilabel in out_tubes:
                out_tubes[ilabel] = []

            # clip box
            t[:, 0] = np.maximum(0, t[:, 0])
            t[:, 1] = np.maximum(0, t[:, 1])
            t[:, 2] = np.minimum(wi, t[:, 2])
            t[:, 3] = np.minimum(hi, t[:, 3])

            out_tubes[ilabel].append(t)

    return imglist, evtlist, evtlist2, evtlist3, out_tubes
