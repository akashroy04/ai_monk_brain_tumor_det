from src.core.infer import get_pred


def format_output(img):
    pred_dict= get_pred(img)

    return pred_dict