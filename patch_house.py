import sys
PATH='index.html'
s=open(PATH,encoding='utf-8').read()
if '[PATCH] house-shape' in s:
    print('• مُطبّق مسبقاً — تخطّي.'); sys.exit(0)

OLD = """  function addBuilding(x,z,w,d,h,tint){
    const tex=facadeTexture(tint); tex.repeat.set(Math.max(1,Math.round(w/3)), Math.max(1,Math.round(h/3)));
    const wall=new THREE.MeshStandardMaterial({map:tex, roughness:.95});
    const roof=new THREE.MeshStandardMaterial({color:0x1b1a20, roughness:1});
    const b=new THREE.Mesh(new THREE.BoxGeometry(w,h,d), [wall,wall,roof,roof,wall,wall]);
    b.position.set(x,h/2,z); b.castShadow=true; b.receiveShadow=true; scene.add(b);
    buildingBoxes.push({minX:x-w/2,maxX:x+w/2,minZ:z-d/2,maxZ:z+d/2});
  }"""

NEW = """  // [PATCH] house-shape: بيت بالكود (جسم بنوافذ + سقف هرمي + باب)
  function addBuilding(x,z,w,d,h,tint){
    const g=new THREE.Group(); g.position.set(x,0,z);

    // جسم البيت بجدران ونوافذ
    const tex=facadeTexture(tint); tex.repeat.set(Math.max(1,Math.round(w/3)), Math.max(1,Math.round(h/3)));
    const wall=new THREE.MeshStandardMaterial({map:tex, roughness:.95});
    const body=new THREE.Mesh(new THREE.BoxGeometry(w,h,d), wall);
    body.position.y=h/2; body.castShadow=true; body.receiveShadow=true; g.add(body);

    // سقف هرمي (جملون)
    const roofH=1.6+Math.random()*0.8;
    const roof=new THREE.Mesh(new THREE.ConeGeometry(Math.hypot(w,d)/2, roofH, 4),
      new THREE.MeshStandardMaterial({color:0x7a4a3a, roughness:.9}));
    roof.rotation.y=Math.PI/4; roof.position.y=h+roofH/2; roof.castShadow=true; g.add(roof);

    // باب على الواجهة المطلّة على الشارع
    const side=x<0?1:-1;
    const door=new THREE.Mesh(new THREE.BoxGeometry(0.9,1.8,0.1),
      new THREE.MeshStandardMaterial({color:0x2a1d14, roughness:.8}));
    door.position.set(side*(w/2+0.02), 0.9, 0); door.rotation.y=Math.PI/2; g.add(door);

    scene.add(g);
    buildingBoxes.push({minX:x-w/2,maxX:x+w/2,minZ:z-d/2,maxZ:z+d/2});
  }"""

if OLD not in s:
    print('✗ لم أجد دالة addBuilding المتوقعة — أوقفت التعديل.'); sys.exit(1)
open(PATH,'w',encoding='utf-8').write(s.replace(OLD,NEW,1))
print('✓ تم: المباني صارت بيوتاً بسقف هرمي وباب')
