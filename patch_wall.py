import sys
PATH = 'index.html'
s = open(PATH, encoding='utf-8').read()
if '[PATCH] wall-shelves' in s:
    print('• مُطبّق مسبقاً — تخطّي.'); sys.exit(0)

# 1) مواضع المنتجات إلى الجدران (x=±7) مع إبقاء z
pos_map = {'pos:[-3,-12]':'pos:[-7,-12]','pos:[ 3,-6 ]':'pos:[ 7,-6 ]','pos:[-3, 0 ]':'pos:[-7, 0 ]','pos:[ 3, 6 ]':'pos:[ 7, 6 ]','pos:[-3, 12]':'pos:[-7, 12]'}
for a,b in pos_map.items():
    if a not in s: print('✗ لم أجد', a); sys.exit(1)
    s = s.replace(a,b,1)

OLD_STAND = """  function addStand(p){
    const [x,z]=p.pos;
    const base=new THREE.Mesh(new THREE.CylinderGeometry(.85,.95,.4,32),
      new THREE.MeshStandardMaterial({color:0x231f1b, roughness:.8}));
    base.position.set(x,.2,z); base.receiveShadow=true; scene.add(base);
    const ring=new THREE.Mesh(new THREE.RingGeometry(.95,1.15,32),
      new THREE.MeshBasicMaterial({color:p.color, transparent:true, opacity:.5, side:THREE.DoubleSide}));
    ring.rotation.x=-Math.PI/2; ring.position.set(x,.42,z); scene.add(ring); p._ring=ring;

    const put=(mesh)=>{
      mesh.position.set(x,1.25,z); mesh.userData.product=p;
      mesh.traverse(o=>{ if(o.isMesh) o.userData.product=p; });
      scene.add(mesh); interactables.push(mesh); productMeshes[p.id]=mesh;
    };
    if(p.model){
      loader.load(p.model, gltf=>{ gltf.scene.traverse(o=>{if(o.isMesh){o.castShadow=true;o.userData.product=p;}}); put(gltf.scene); },
        undefined, ()=>put(placeholder(p)));
    } else put(placeholder(p));
  }"""

NEW_STAND = """  // [PATCH] wall-shelves: رفوف مرتفعة على الجدران (يسار/يمين)
  function addStand(p){
    const [x,z]=p.pos;
    const side = x < 0 ? -1 : 1;     // -1 جدار يسار، +1 جدار يمين
    const SHELF_Y = 1.7;             // ارتفاع الرف

    // لوح الرف + ساندة سفلية
    const shelf=new THREE.Mesh(new THREE.BoxGeometry(1.4,0.12,1.0),
      new THREE.MeshStandardMaterial({color:0x3a2f25, roughness:.85}));
    shelf.position.set(x, SHELF_Y, z); shelf.castShadow=true; shelf.receiveShadow=true; scene.add(shelf);
    const bracket=new THREE.Mesh(new THREE.BoxGeometry(0.1,0.4,0.7),
      new THREE.MeshStandardMaterial({color:0x2a2018, roughness:.9}));
    bracket.position.set(x + side*0.6, SHELF_Y-0.28, z); scene.add(bracket);

    // حلقة مضيئة عمودية تواجه الشارع
    const ring=new THREE.Mesh(new THREE.RingGeometry(.5,.62,32),
      new THREE.MeshBasicMaterial({color:p.color, transparent:true, opacity:.5, side:THREE.DoubleSide}));
    ring.rotation.y = side<0 ? -Math.PI/2 : Math.PI/2; ring.position.set(x - side*0.1, SHELF_Y+0.5, z);
    scene.add(ring); p._ring=ring;

    const put=(mesh)=>{
      mesh.position.set(x, SHELF_Y+0.1, z); mesh.userData.product=p;   // يجلس فوق الرف
      mesh.traverse(o=>{ if(o.isMesh) o.userData.product=p; });
      scene.add(mesh); interactables.push(mesh); productMeshes[p.id]=mesh;
    };
    if(p.model){
      loader.load(p.model, gltf=>{ gltf.scene.traverse(o=>{if(o.isMesh){o.castShadow=true;o.userData.product=p;}}); put(gltf.scene); },
        undefined, ()=>put(placeholder(p)));
    } else put(placeholder(p));
  }"""

if OLD_STAND not in s: print('✗ لم أجد دالة addStand المتوقعة'); sys.exit(1)
s = s.replace(OLD_STAND, NEW_STAND, 1)

OLD_COL = """    for(const p of PRODUCTS){
      const dx=pos.x-p.pos[0], dz=pos.z-p.pos[1], min=1.1+PLAYER.radius, dist=Math.hypot(dx,dz);
      if(dist<min && dist>1e-4){ const f=min/dist; pos.x=p.pos[0]+dx*f; pos.z=p.pos[1]+dz*f; }
    }"""
NEW_COL = """    // [wall-shelves] المنتجات مرتفعة على الجدران — لا تصادم أرضي معها"""
if OLD_COL in s: s = s.replace(OLD_COL, NEW_COL, 1)
else: print('⚠ لم أجد كتلة تصادم المنتجات (تابعت بدونها)')

open(PATH,'w',encoding='utf-8').write(s)
print('✓ تم: رفوف جدارية + مواضع جديدة + إلغاء تصادم المنتجات')
