import numpy as np
import torch
from torch import optim

from os.path import join
import matplotlib.pyplot as plt
from PIL import Image

from model.mammogram_densenet import MammogramDenseNet
from model import helper
from util.image import normalize_between
from util.checkpoint import load_model

def get_activation(model, layer, image, device = torch.device('cuda'), dtype = torch.float32):
    model.eval()
    
    # Forward pass on the convolutions
    conv_output = []
    conv_layer_list = []
    x = torch.from_numpy(image).unsqueeze(0).unsqueeze(0)
    x = x.to(device=device, dtype=dtype)
    
    for module_pos, module in model.features._modules.items():
        print (module_pos)
        if "conv" in module_pos:
            x = module(x)
            conv_output.append(x)
            conv_layer_list.append(module_pos)
        elif "transition" in module_pos:
            for module_pos_1, module_1 in module._modules.items():
                print ("\t", module_pos_1)
                x = module_1(x)
                if "conv" in module_pos_1:
                    conv_output.append(x)
                    conv_layer_list.append(module_pos+", "+module_pos_1)
        else:
            x = module(x)
    
    print (conv_layer_list)
    print (len(conv_output))
    for layer_name, output in zip(conv_layer_list, conv_output):
        print (output.shape)
        activation = output.cpu().data.numpy()[0]
        #resize to 1024x1024?
        activation = np.maximum(activation, 0)
        activation = (activation - np.min(activation)) / (np.max(activation) - np.min(activation))  # Normalize between 0-1
        activation = np.uint8(activation * 255)  # Scale between 0-255 to visualize
        print (layer_name)
        print (activation)
        return activation
    