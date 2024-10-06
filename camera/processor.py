import numpy as np
import supervision as sv
from inference.models.yolo_world.yolo_world import YOLOWorld
from segment_anything import sam_model_registry, SamPredictor
import matplotlib.pyplot as plt
from .camera import RGBDCamera
from .utils import rgbd2cloud, get_largest_cluster


class Processor:
    def __init__(self, sam_checkpoint, model_type, device):
        sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
        sam.to(device=device)
        self.predictor = SamPredictor(sam)
        self.yolo = YOLOWorld(model_id="yolo_world/l")
        self.camera = RGBDCamera()

    def get_pcd(self, target, debug=False):
        color, depth = self.camera.get_frame()
        self.yolo.set_classes([target])
        results = self.yolo.infer(color, confidence=0.01)
        detections = sv.Detections.from_inference(results)

        def get_mask(rgb, input_box):
            self.predictor.set_image(rgb)
            masks, _, _ = self.predictor.predict(
                point_coords=None,
                point_labels=None,
                box=input_box[None, :],
                multimask_output=False,
            )
            return masks[0]

        mask = get_mask(color, detections.xyxy[0])
        masked_depth_image = np.where(mask > 0, depth, 0)
        depth_image = masked_depth_image
        pcd = rgbd2cloud(depth_image, color)
        if debug:
            plt.figure(figsize=(6, 6))
            plt.imshow(color)
            plt.imshow(mask, cmap='Reds', alpha=0.5)  # 使用 'Reds' 颜色映射来显示掩码
            plt.axis('off')  # 隐藏坐标轴
            plt.show()
            plt.imshow(depth)
            plt.imshow(mask, cmap='Reds', alpha=0.5)  # 使用 'Reds' 颜色映射来显示掩码
            plt.axis('off')  # 隐藏坐标轴
            plt.show()
        pcd = get_largest_cluster(pcd)[0]
        return pcd
