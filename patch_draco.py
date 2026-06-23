import sys
PATH = 'index.html'
s=open(PATH,encoding='utf-8').read()
if 'DRACOLoader' in s:
    print('• مُطبّق مسبقاً — تخطّي.'); sys.exit(0)

IMP_OLD = "  import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';"
IMP_NEW = ("  import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';\n"
           "  import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';")
if IMP_OLD not in s: print('✗ import GLTFLoader'); sys.exit(1)
s=s.replace(IMP_OLD, IMP_NEW, 1)

LD_OLD = "  const loader = new GLTFLoader();"
LD_NEW = ("""  const loader = new GLTFLoader();
  // [draco] فاكّ ضغط الهندسة (مطلوب للملفات المضغوطة بـDraco)
  const dracoLoader = new DRACOLoader();
  dracoLoader.setDecoderPath('https://cdn.jsdelivr.net/npm/three@0.161.0/examples/jsm/libs/draco/');
  loader.setDRACOLoader(dracoLoader);""")
if LD_OLD not in s: print('✗ const loader'); sys.exit(1)
s=s.replace(LD_OLD, LD_NEW, 1)

open(PATH,'w',encoding='utf-8').write(s)
print('✓ تم: إضافة DRACOLoader لقراءة الملفات المضغوطة')
