#利用包含2部分结构的xyz坐标文件，产生将其中一部分结构沿着特定方向逐步移动的一系列坐标文件（刚性扫描）。
#特定的方向可以为结构中包含的两个坐标的连线方向，或者结构中指定(的多个)坐标确定的平面的法向量方向。
#LiZhiQiang@2501

import numpy as np

def parse_xyz(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()[2:]  # 跳过前两
    atoms = [line.split() for line in lines]
    elements = [atom[0] for atom in atoms]
    coordinates = np.array([[float(x) for x in atom[1:]] for atom in atoms])
    return elements, coordinates

def get_molecule_atoms(input_str):
    indices = []
    for part in input_str.split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            indices.extend(range(start - 1, end))
        else:
            indices.append(int(part) - 1)
    return indices

def normalize_vector(vector):
    return vector / np.linalg.norm(vector)

def two_point_param(all_coordinates):
    print("请指定两个原子序号（空格分隔，分别位于两部分）：")
    atom1_index, atom2_index = map(int, input().split())
    atom1_index -= 1
    atom2_index -= 1

    direction_vector = normalize_vector(all_coordinates[atom2_index] - all_coordinates[atom1_index])
    origianl_distance = np.linalg.norm(all_coordinates[atom2_index] - all_coordinates[atom1_index])
    return direction_vector, origianl_distance

def fit_plane(mol_indices, all_coordinates):
    new_coords = all_coordinates[mol_indices]
    # points is a list of [x, y, z] coordinates
    xs = new_coords[:, 0]
    ys = new_coords[:, 1]
    zs = new_coords[:, 2]

    M = np.column_stack((xs, ys, np.ones_like(xs)))

    # Solve using least squares
    coeffs, residuals, rank, s = np.linalg.lstsq(M, zs, rcond=None)

    return np.append(coeffs, -1)  # Returns A, B, D, C from Ax + By + Cz + D = 0

def point_to_plane_distance(point, plane_coeffs):
    A, B, D, C = plane_coeffs
    x, y, z = point
    return abs(A*x + B*y + C*z + D) / np.sqrt(A**2 + B**2 + C**2)

def point_2_plane_param(all_coordinates):
    input_str3 = input("请输入确定平面的原子序数（数量≥3，尽可能在一个平面，格式如1-5,8,9）：")
    part3_indices = get_molecule_atoms(input_str3)
    print("请输入确定点到面距离的原子的序号(单一正整数)")
    atom3_index = int(input()) - 1

    #最小二乘法求解平面，并给出其法向量
    plane_coeffs = fit_plane(part3_indices, coordinates)
    A, B, D, C = plane_coeffs
    direction_vector = normalize_vector(np.array([A, B, C]))
    
    # Ensure the direction vector points away from the plane to the outside point
    point_on_plane = all_coordinates[part3_indices[0]]
    if np.dot(direction_vector, all_coordinates[atom3_index] - point_on_plane) < 0:
        direction_vector = -direction_vector

    #计算点到面的原始距离
    origianl_distance = point_to_plane_distance(all_coordinates[atom3_index], plane_coeffs)
    return direction_vector, origianl_distance

def move_molecule(mol_indices, all_coordinates, displacement):
    new_coords = all_coordinates.copy()
    new_coords[mol_indices] += displacement
    return new_coords

def write_to_file(filename, elements, coordinates, distance):
    with open(filename, 'a') as f:
        f.write(f"{len(elements)}\n")
        f.write(f"Distance: {distance:.8f}\n")
        for element, coord in zip(elements, coordinates):
            f.write(f"{element:>4} {' '.join(map(lambda x: f'{x:.8f}', coord))}\n")


# 主程序
if __name__ == "__main__":

    xyz_file_path = input("请输入文件路径：")  
    elements, coordinates = parse_xyz(xyz_file_path)

    input_str1 = input("请输入第1部分包含的原子序数（格式如1-5,8,9）：")
    mol1_indices = get_molecule_atoms(input_str1)
    input_str2 = input("请输入第2部分包含的原子序数（格式如1-5,8,9）：")
    mol2_indices = get_molecule_atoms(input_str2)

    choice = input("请选择移动算法类型 (1: 点距离平移, 2: 点到面距离平移): ")
    if choice == '1':
        direction_vector, original_distance = two_point_param(coordinates)
    elif choice == '2':
        direction_vector, original_distance = point_2_plane_param(coordinates)
    else:
        print("无效的选择。")
        exit()

    start_distance = float(input("请输入扫描起始距离(埃)："))
    end_distance = float(input("请输入扫描结束距离(埃)："))
    step_size = float(input("请输入扫描步长(埃)："))

    with open('scan.xyz', 'w') as f:  # 清空文件
        pass

    current_distance = start_distance
    while current_distance <= end_distance + step_size / 2:  # 加上半个步长确保end被包含
        displacement = (current_distance - original_distance) * direction_vector
        new_coordinates = move_molecule(mol2_indices, coordinates, displacement)
        write_to_file('scan.xyz', elements, new_coordinates, current_distance)
        current_distance += step_size


