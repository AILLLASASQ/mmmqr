import sys
PATH = 'index.html'
s=open(PATH,encoding='utf-8').read()
if 'function groundPlayer' in s:
    print('• مُطبّق مسبقاً — تخطّي.'); sys.exit(0)

GROUND_OLD = """  const ground = new THREE.Mesh(new THREE.PlaneGeometry(120,120),
    new THREE.MeshStandardMaterial({color:0x2b2723, roughness:1}));
  ground.rotation.x=-Math.PI/2; ground.receiveShadow=true; scene.add(ground);
  const sidewalkMat=new THREE.MeshStandardMaterial({color:0x3b362f, roughness:1});
  [-7.5,7.5].forEach(x=>{ const s=new THREE.Mesh(new THREE.BoxGeometry(2.4,0.2,STREET.halfZ*2+8),sidewalkMat);
    s.position.set(x,0.1,0); s.receiveShadow=true; scene.add(s); });"""
GROUND_NEW = """  // [city] أُزيلت الأرض والأرصفة الافتراضية — المدينة هي البيئة الحقيقية.
  // أرض أمان غير مرئية: مرجع احتياطي لو فشل إسقاط الشخصية على سطح المدينة.
  const SAFETY_Y = 0;
  const safetyFloor = new THREE.Mesh(new THREE.PlaneGeometry(400,400),
    new THREE.MeshBasicMaterial({visible:false}));
  safetyFloor.rotation.x=-Math.PI/2; safetyFloor.position.y=SAFETY_Y; scene.add(safetyFloor);"""
if GROUND_OLD not in s: print('✗ ground/sidewalk'); sys.exit(1)
s=s.replace(GROUND_OLD, GROUND_NEW, 1)

LIGHTS_OLD = """  buildLights();

  const player = new THREE.Group();"""
LIGHTS_NEW = """  // [city] أعمدة الإنارة الافتراضية مُعطّلة — المدينة توفّر إنارتها. // buildLights();

  const player = new THREE.Group();"""
if LIGHTS_OLD not in s: print('✗ buildLights call'); sys.exit(1)
s=s.replace(LIGHTS_OLD, LIGHTS_NEW, 1)

START_OLD = "  player.position.set(0,0,18); player.rotation.y = Math.PI;"
START_NEW = "  player.position.set(0,0,0); player.rotation.y = Math.PI;   // [city] البداية وسط المدينة"
if START_OLD not in s: print('✗ player start'); sys.exit(1)
s=s.replace(START_OLD, START_NEW, 1)

ANIM_ANCHOR = "  function animate(){"
if ANIM_ANCHOR not in s: print('✗ animate'); sys.exit(1)
GROUNDFN = """  // ===== [city] إسقاط الشخصية على سطح المدينة (raycast لأسفل) =====
  const _downRay = new THREE.Raycaster();
  const _downOrigin = new THREE.Vector3();
  const _downDir = new THREE.Vector3(0,-1,0);
  const CITY_PROBE_UP = 50;   // ارتفاع بدء الشعاع فوق الشخصية
  function groundPlayer(){
    if(!cityGroup){ player.position.y = SAFETY_Y; return; }
    _downOrigin.set(player.position.x, player.position.y + CITY_PROBE_UP, player.position.z);
    _downRay.set(_downOrigin, _downDir);
    _downRay.far = CITY_PROBE_UP + 200;
    const hits = _downRay.intersectObject(cityGroup, true);
    player.position.y = hits.length ? hits[0].point.y : SAFETY_Y;
  }

"""
s=s.replace(ANIM_ANCHOR, GROUNDFN + ANIM_ANCHOR, 1)

CALL_OLD = """      if(mixer) mixer.update(dt);

      let best=null, bd=3.2;"""
CALL_NEW = """      if(mixer) mixer.update(dt);

      groundPlayer();

      let best=null, bd=3.2;"""
if CALL_OLD not in s: print('✗ animate mixer/best'); sys.exit(1)
s=s.replace(CALL_OLD, CALL_NEW, 1)

open(PATH,'w',encoding='utf-8').write(s)
print('✓ تم: حذف الأرض/الأرصفة/الأعمدة + أرض أمان + المشي على سطح المدينة + بداية وسط المدينة')
