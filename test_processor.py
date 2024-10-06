from camera import Processor
from camera.utils import *
sam_checkpoint = "/data/E/D/file/share/sam_vit_b_01ec64.pth"
model_type = "vit_b"
device = "cpu"
processor = Processor(sam_checkpoint, model_type, device, )
pcd = processor.get_pcd('cup', debug=True)
visualize_pcd(pcd)