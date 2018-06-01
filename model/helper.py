from model.mammogram_densenet import MammogramDenseNet, Swish
from torchvision.models.densenet import _DenseBlock, _Transition


def get_tiny_densenet(swish=False, **kwargs):
    model = MammogramDenseNet(block_config=(6,), **kwargs)
    return replace_relu_with_swish(model)

def get_small_densenet(swish=False, **kwargs):
    model = MammogramDenseNet(block_config=(10, 6), **kwargs)
    return replace_relu_with_swish(model)

def get_medium_densenet(swish=False, **kwargs):
    model = MammogramDenseNet(block_config=(8, 12, 8), **kwargs)
    return replace_relu_with_swish(model)

def get_large_densenet(swish=False, **kwargs):
    model = MammogramDenseNet(block_config = (6,12,18,12), **kwargs) # Default block config
    return replace_relu_with_swish(model)


def replace_relu_with_swish(model):
    """ Change places with relu activation in MammogramDenseNet to swish
        denseblock_positions: 
            a list of ints, indicating which indices in features have dense blocks
    """
    denseblock_positions = [i for i, m in enumerate(model.features) if type(m) is _DenseBlock]
    transition_positions = [i for i, m in enumerate(model.features) if type(m) is _Transition]
    
    # The first relu
    model.features[2] = Swish()
    
    for i in denseblock_positions:
        nb_dense_layers = len(model.features[i])
        for _ in range(nb_dense_layers):
            model.features[i][_][1] = Swish()
            model.features[i][_][4] = Swish()
    
    for i in transition_positions:
        model.features[i][1] = Swish()

    return model
