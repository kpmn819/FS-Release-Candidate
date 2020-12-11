from pathlib import Path
Path.cwd()
cwd = Path.cwd()
base_path = Path.cwd()
print('first path ',base_path)
base_path /= '1whale1.jpg'
print('second path ',base_path)
file_path = Path(cwd, '1whale1.jpg')
print('file_path ', file_path)
base_path2 = Path(__file__).resolve().parent.parent
print('base_path2 ', base_path2)
template_path = base_path2 / 'Downloads'
print('template_path ', template_path)
whale_path = template_path / '1whale1.jpg'
print('whale_path ', whale_path)