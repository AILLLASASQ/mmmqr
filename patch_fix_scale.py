import sys
PATH='index.html'
s=open(PATH,encoding='utf-8').read()

if '[PATCH] robust-fit' in s:
    print('• مُطبّق مسبقاً — تخطّي.'); sys.exit(0)

OLD = """    const sz = new THREE.Vector3(); new THREE.Box3().setFromObject(model).getSize(sz);
    if (sz.y > 0) model.scale.setScalar(TARGET_HEIGHT / sz.y);
    const b = new THREE.Box3().setFromObject(model);
    model.position.y -= b.min.y;

    model.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; o.frustumCulled = false; } });
    player.add(model);"""

NEW = """    // [PATCH] robust-fit: نضيف ثم نحدّث المصفوفات ثم نقيس ونصغّر فعلياً
    model.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; o.frustumCulled = false; } });
    player.add(model);
    player.updateWorldMatrix(true, true);
    let bb = new THREE.Box3().setFromObject(model);
    const size = new THREE.Vector3(); bb.getSize(size);
    const h = size.y || 1;
    model.scale.multiplyScalar(TARGET_HEIGHT / h);          // تطبيع الارتفاع إلى TARGET_HEIGHT
    player.updateWorldMatrix(true, true);
    bb = new THREE.Box3().setFromObject(model);
    model.position.y -= bb.min.y;                           // القدمان عند الأرض
    console.log('[scale] ارتفاع أصلي=' + h.toFixed(2) + ' → مضبوط=' + TARGET_HEIGHT);"""

if OLD not in s:
    print('✗ لم أجد كتلة القياس المتوقعة — أوقفت التعديل (ربما عدّلتها يدوياً).'); sys.exit(1)

s=s.replace(OLD, NEW, 1)
open(PATH,'w',encoding='utf-8').write(s)
print('✓ تم إصلاح منطق الحجم (تطبيع الارتفاع فعلياً)')
