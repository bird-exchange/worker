import os
import pathlib
import sys

import torch
import torchvision.transforms as tt
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision.utils import save_image
from tqdm import tqdm

from worker.config import handler_config
from worker.handler.data.dataset import CycleGanDataset
from worker.handler.model.discriminator import Discriminator
from worker.handler.model.generator import Generator
from worker.handler.utils.denormalization import denorm


def test_processing(path_to_test, path_load_model, transform,
                    load_epoch, path_save, type_img, name_img
                    ):

    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

    test_dataset = CycleGanDataset(path_to_test, transform=transform, data_mode='test')

    test_loader = DataLoader(
        test_dataset,
        batch_size=1,
        shuffle=False
    )

    model = {
        "dis_x": Discriminator().to(DEVICE),
        "gen_x": Generator().to(DEVICE),
        "dis_y": Discriminator().to(DEVICE),
        "gen_y": Generator().to(DEVICE)
    }

    path_to_load = os.path.join(path_load_model, f"checkpoint_epoch_{load_epoch}.pth.tar")

    if os.path.isfile(path_to_load):
        checkpoint = torch.load(path_to_load, map_location=DEVICE)
        model["dis_x"].load_state_dict(checkpoint["st_dis_x"])
        model["gen_x"].load_state_dict(checkpoint["st_gen_x"])
        model["dis_y"].load_state_dict(checkpoint["st_dis_y"])
        model["gen_y"].load_state_dict(checkpoint["st_gen_y"])
    else:
        sys.exit("no checkpoint found for {} epoch".format(load_epoch))

    model["dis_x"].eval()
    model["gen_x"].eval()
    model["dis_y"].eval()
    model["gen_y"].eval()

    if type_img == 1:
        for _, real_x in enumerate(tqdm(test_loader, leave=True)):
            real_x = real_x.to(DEVICE)
            with torch.no_grad():
                if handler_config.switch:
                    fake_y = model["gen_y"](real_x)
                else:
                    fake_y = model["gen_x"](real_x)
            save_image(denorm(fake_y), os.path.join(path_save, name_img))
    elif type_img == 2:
        for _, real_y in enumerate(tqdm(test_loader, leave=True)):
            real_y = real_y.to(DEVICE)
            with torch.no_grad():
                if handler_config.switch:
                    fake_x = model["gen_x"](real_y)
                else:
                    fake_x = model["gen_y"](real_y)
            save_image(denorm(fake_x), os.path.join(path_save, name_img))


def general(type_img: int, name_img: str):

    pathlib.Path(f'{handler_config.path_test_results}').mkdir(parents=True, exist_ok=True)

    stats = (0.5, 0.5, 0.5), (0.5, 0.5, 0.5)

    transform = transforms.Compose([transforms.Resize(handler_config.image_size),
                                    transforms.CenterCrop(handler_config.image_size),
                                    transforms.ToTensor(),
                                    tt.Normalize(*stats)])

    test_processing(
        path_to_test=handler_config.path_to_data,
        path_load_model=handler_config.path_load_model,
        transform=transform,
        load_epoch=handler_config.load_epoch,
        path_save=handler_config.path_test_results,
        type_img=type_img,
        name_img=name_img
    )
