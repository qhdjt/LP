import os
import shutil
from PIL import Image


def convert_tiff_to_bmp(input_folder: str, output_folder: str):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for root, dirs, files in os.walk(input_folder):
        relative_path = os.path.relpath(root, input_folder)
        output_subfolder = os.path.join(output_folder, relative_path)
        if not os.path.exists(output_subfolder):
            os.makedirs(output_subfolder)
        for file in files:
            input_path = os.path.join(root, file)
            output_path = os.path.join(output_subfolder, file)
            if file.endswith('.tiff') or file.endswith('.tif'):
                output_path = os.path.join(output_subfolder, os.path.splitext(file)[0] + '.bmp')
                with Image.open(input_path) as img:
                    if img.is_animated:
                        pages = []
                        for i in range(img.n_frames):
                            if i == 3:
                                continue
                            img.seek(i)
                            pages.append(img.copy())
                        if len(pages) >= 3:
                            bmp = Image.merge('RGB',
                                              (pages[0].convert('L'), pages[1].convert('L'), pages[2].convert('L'))
                                              )
                            bmp.save(output_path, 'BMP')
                            print(f"Converted {input_path} to {output_path}")
                        else:
                            print("TIFF文件中的页面数量不足，无法创建RGB BMP文件。将复制")
                            shutil.copy2(input_path, output_path)
                            print(f"Copied {input_path} to {output_path}")
            else:
                shutil.copy2(input_path, output_path)
                print(f"Copied {input_path} to {output_path}")


if __name__ == '__main__':
    # 等待用户输入
    input_folder = input("转换此路径下的TIFF文件:")
    output_folder = input("保存转换后的BMP文件到此路径:")
    # 校验路径
    if not os.path.exists(input_folder):
        print("输入路径不存在。")
        exit(1)
    print("正在转换TIFF文件...")
    convert_tiff_to_bmp(input_folder, output_folder)
    print("转换完成。")
