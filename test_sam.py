import cv2
import supervision as sv
from inference.models.yolo_world.yolo_world import YOLOWorld
from segment_anything import sam_model_registry, SamPredictor
import matplotlib.pyplot as plt

target = "plate"
img_path = "/home/ykx/下载/菜.jpg"

sam_checkpoint = "/data/E/D/file/share/sam_vit_b_01ec64.pth"
model_type = "vit_b"
device = "cpu"
sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
sam.to(device=device)
predictor = SamPredictor(sam)
yolo = YOLOWorld(model_id="yolo_world/l")
yolo.set_classes([target])

color = cv2.imread(img_path, cv2.IMREAD_COLOR)
color = cv2.cvtColor(color, cv2.COLOR_BGR2RGB)
results = yolo.infer(color, confidence=0.01)
detections = sv.Detections.from_inference(results)


def get_mask(rgb, input_box):
    predictor.set_image(rgb)
    masks, _, _ = predictor.predict(
        point_coords=None,
        point_labels=None,
        box=input_box[None, :],
        multimask_output=False,
    )
    return masks[0]


def show_box(box):
    print(box)
    mask = get_mask(color, box)
    plt.figure(figsize=(6, 6))
    plt.imshow(color)
    plt.imshow(mask, cmap='Reds', alpha=0.5)  # 使用 'Reds' 颜色映射来显示掩码
    plt.axis('off')  # 隐藏坐标轴
    plt.show()


for box in detections.xyxy:
    show_box(box)
