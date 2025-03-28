import open3d as o3d
import numpy as np
import cv2
import datetime

filename = input("Enter file name: ")

mesh = o3d.io.read_triangle_mesh(filename)
texture_filename = input("Enter texture file name: ")
texture_image = o3d.io.read_image(texture_filename)

texture_np = np.asarray(texture_image)

flipped_texture = cv2.flip(texture_np, 0)

texture_image = o3d.geometry.Image(flipped_texture)
mesh.textures = [texture_image]


if not mesh.has_vertex_normals():
    mesh.compute_vertex_normals()

def capture_snapshot(vis):
    image = vis.capture_screen_float_buffer(True)
    image_np = (np.asarray(image) * 255).astype(np.uint8)
    image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
    
    x=datetime.datetime.now()
    cur_time=x.strftime("%Y%m%d_%H%M%S")
    snapshot_path = f"D:/BDAS/snapshots/snapshot_{cur_time}.png"
    cv2.imwrite(snapshot_path, image_np)
    print(f"Snapshot saved at: {snapshot_path}")

    depth_image = vis.capture_depth_float_buffer(True)
    depth_np = (np.asarray(depth_image)).astype(np.uint8)
    depth_np = cv2.cvtColor(depth_np, cv2.COLOR_BGR2RGB)

    depth_snapshot_path = f"D:/BDAS/snapshots/depth_{cur_time}.png"
    cv2.imwrite(depth_snapshot_path, depth_np)
    print(f"Depth buffer saved at: {depth_snapshot_path}")

o3d.visualization.draw_geometries_with_key_callbacks([mesh], {ord("Q"): capture_snapshot})