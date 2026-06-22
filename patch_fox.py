import re, sys
PATH = 'index.html'
s = open(PATH, encoding='utf-8').read()

if '[PATCH] fox-single-file' in s:
    print('• مُطبّق مسبقاً — تخطّي.'); sys.exit(0)

A = 'const loader = new GLTFLoader();'
B = 'const interactables = ['
if A not in s or B not in s:
    print('✗ لم أجد المرساة المتوقعة — أوقفت التعديل.'); sys.exit(1)

start, end = s.index(A), s.index(B)

NEW = """const loader = new GLTFLoader();
  let mixer = null, walkAction = null;

  // [PATCH] fox-single-file: الميش + المشي من نفس الملف (الثعلب) مع مقياس تلقائي
  const CHARACTER     = 'models/walk_animation2.glb';   // يحوي الميش + الأنميشن
  const TARGET_HEIGHT = 1.6;                             // ارتفاع تقريبي — غيّره حسب رغبتك

  loader.load(CHARACTER, (gltf) => {
    const model = gltf.scene;

    let meshes = 0; model.traverse(o => { if (o.isMesh) meshes++; });
    console.log('[fox] ميش=' + meshes, '| أنميشن=', gltf.animations.map(a => a.name));

    // الثعلب مُصدّر بمقياس ضخم → نضبطه تلقائياً + ننزل قدميه للأرض
    const sz = new THREE.Vector3(); new THREE.Box3().setFromObject(model).getSize(sz);
    if (sz.y > 0) model.scale.setScalar(TARGET_HEIGHT / sz.y);
    const b = new THREE.Box3().setFromObject(model);
    model.position.y -= b.min.y;

    model.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; o.frustumCulled = false; } });
    player.add(model);

    // اختيار أنميشن المشي بالاسم (Survey/Walk/Run)، وإلا الأطول/الأول كبديل
    mixer = new THREE.AnimationMixer(model);
    const clips = gltf.animations || [];
    const walk = clips.find(c => /walk/i.test(c.name)) || clips[1] || clips[0];
    if (walk) { walkAction = mixer.clipAction(walk); walkAction.play(); }
    else console.warn('⚠ لا يوجد أي clip في', CHARACTER);
  }, undefined, e => console.warn('تعذّر تحميل', CHARACTER, e));"""

open(PATH, 'w', encoding='utf-8').write(s[:start] + NEW + "\n\n  " + s[end:])
print('✓ تم تعديل index.html لتحميل الثعلب (ميش + مشي) بمقياس صحيح')
