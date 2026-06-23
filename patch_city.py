import sys
PATH = 'index.html'
s=open(PATH,encoding='utf-8').read()
if 'CITY_FILE' in s:
    print('• مُطبّق مسبقاً — تخطّي.'); sys.exit(0)

BB_OLD = "  function buildBuildings(){ BUILDINGS.forEach(b=>{ addBuilding(b.x, b.z, b.w, b.d, b.h, b.tint); const g=buildingGroups[buildingGroups.length-1]; if(g){ g.rotation.y=(b.rot||0); g.scale.setScalar(b.scale||1); g.userData.editable={type:'building', ref:b, group:g}; } }); }"
BB_NEW = """  // [city] البيوت المرسومة مخفية (المدينة الخارجية توفّر المباني). غيّر SHOW_CODE_BUILDINGS=true لإظهارها.
  const SHOW_CODE_BUILDINGS = false;
  function buildBuildings(){ if(!SHOW_CODE_BUILDINGS) return; BUILDINGS.forEach(b=>{ addBuilding(b.x, b.z, b.w, b.d, b.h, b.tint); const g=buildingGroups[buildingGroups.length-1]; if(g){ g.rotation.y=(b.rot||0); g.scale.setScalar(b.scale||1); g.userData.editable={type:'building', ref:b, group:g}; } }); }"""
if BB_OLD not in s: print('✗ buildBuildings'); sys.exit(1)
s=s.replace(BB_OLD, BB_NEW, 1)

ST_OLD = "  const STREET = { halfX:6.3, halfZ:24 };"
ST_NEW = "  const STREET = { halfX:40, halfZ:40 };   // [city] حدود أوسع للتجوّل داخل المدينة"
if ST_OLD not in s: print('✗ STREET'); sys.exit(1)
s=s.replace(ST_OLD, ST_NEW, 1)

FOG_OLD = "  scene.fog = new THREE.Fog(0x9fb0bd, 22, 70);"
FOG_NEW = "  scene.fog = new THREE.Fog(0x9fb0bd, 60, 220);   // [city] ضباب أبعد"
if FOG_OLD not in s: print('✗ fog'); sys.exit(1)
s=s.replace(FOG_OLD, FOG_NEW, 1)

ANCHOR = "  // [المرحلة 1] جلب المشهد من Firestore عبر الخادم (مع رجوع آمن للافتراضي) ثم البناء"
if ANCHOR not in s: print('✗ مرساة loadScene'); sys.exit(1)
CITY = """  // ===== [city] تحميل مدينة CCity Building Set 1 (الكاتب: Neberkenezer — رخصة CC-BY) =====
  console.log('City model: "CCity Building Set 1" by Neberkenezer (Sketchfab) — CC-BY.');
  const CITY_FILE  = 'models/city.glb';
  const CITY_SCALE = 0.05;   // ← اضبط هذا حتى يصير حجم المدينة مناسباً (جرّب 0.02 ، 0.1 ، 0.5 ، 1 ...)
  const CITY_X = 0, CITY_Y = 0, CITY_Z = 0;   // إزاحة المدينة
  const CITY_ROT = 0;        // تدوير المدينة (راديان، مثلاً Math.PI/2)
  let cityGroup = null;
  function loadCity(){
    loader.load(CITY_FILE, (gltf)=>{
      const m = gltf.scene;
      const box = new THREE.Box3().setFromObject(m); const size = new THREE.Vector3(); box.getSize(size);
      console.log('[city] الحجم الأصلي ≈ X:'+size.x.toFixed(1)+' Y:'+size.y.toFixed(1)+' Z:'+size.z.toFixed(1)
        + ' | إن كان ضخماً جرّب CITY_SCALE أصغر، وإن كان صغيراً جرّبه أكبر.');
      m.traverse(o=>{ if(o.isMesh){ o.castShadow=true; o.receiveShadow=true; o.frustumCulled=false; } });
      m.scale.setScalar(CITY_SCALE);
      m.rotation.y = CITY_ROT;
      m.position.set(CITY_X, CITY_Y, CITY_Z);
      scene.add(m); cityGroup = m;
      console.log('[city] حُمِّلت المدينة. اضبط CITY_SCALE/CITY_Y حتى تقف الشخصية على الشارع.');
    }, undefined, e=> console.warn('[city] تعذّر تحميل', CITY_FILE, e));
  }
  loadCity();

"""
s=s.replace(ANCHOR, CITY + ANCHOR, 1)

open(PATH,'w',encoding='utf-8').write(s)
print('✓ تم: تحميل المدينة + إخفاء البيوت + حدود أوسع + ضباب أبعد')
