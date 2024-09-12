from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import os

__pk_path = os.path.dirname(os.path.realpath(__file__))
scene = [sc for sc in os.listdir(__pk_path) if sc.endswith('.ttt')]
assert len(scene) == 1
scene = scene[0]
scene_path = os.path.join(__pk_path, scene)

client = RemoteAPIClient()
sim = client.require('sim')
sim.loadScene(scene_path)
SceneObjectSubTypes = ['light_omnidirectional_subtype',
                         'light_spot_subtype',
                         'light_directional_subtype',
                         'joint_revolute_subtype',
                         'joint_prismatic_subtype',
                         'joint_spherical_subtype',
                         'shape_simpleshape_subtype',
                         'shape_multishape_subtype',
                         'proximitysensor_ray_subtype',
                         'proximitysensor_pyramid_subtype',
                         'proximitysensor_cylinder_subtype',
                         'proximitysensor_disc_subtype',
                         'proximitysensor_cone_subtype']
SceneObjectSubTypes = {getattr(sim, attr): attr for attr in SceneObjectSubTypes}
