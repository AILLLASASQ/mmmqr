import sys
PATH = 'index.html'
s=open(PATH,encoding='utf-8').read()
if 'function _editAction' in s:
    print('• مُطبّق مسبقاً — تخطّي.'); sys.exit(0)

BS_OLD = "    const g=new THREE.Group(); g.position.set(x,0,z); g.rotation.y=-side*Math.PI/2;"
BS_NEW = "    const g=new THREE.Group(); g.position.set(x,0,z); g.rotation.y=-side*Math.PI/2 + (sec.rot||0); g.scale.setScalar(sec.scale||1);"
if BS_OLD not in s: print('✗ buildSection g'); sys.exit(1)
s=s.replace(BS_OLD, BS_NEW, 1)

BB_OLD = "  function buildBuildings(){ BUILDINGS.forEach(b=>{ addBuilding(b.x, b.z, b.w, b.d, b.h, b.tint); const g=buildingGroups[buildingGroups.length-1]; if(g) g.userData.editable={type:'building', ref:b, group:g}; }); }"
BB_NEW = "  function buildBuildings(){ BUILDINGS.forEach(b=>{ addBuilding(b.x, b.z, b.w, b.d, b.h, b.tint); const g=buildingGroups[buildingGroups.length-1]; if(g){ g.rotation.y=(b.rot||0); g.scale.setScalar(b.scale||1); g.userData.editable={type:'building', ref:b, group:g}; } }); }"
if BB_OLD not in s: print('✗ buildBuildings'); sys.exit(1)
s=s.replace(BB_OLD, BB_NEW, 1)

RE_OLD = "    h += '<div style=\"color:var(--brass);margin:6px 0 8px\">الأقسام</div>';"
RE_NEW = ("""    if(selectedEdit){
      const tname = selectedEdit.type==='section' ? ('قسم: '+(selectedEdit.ref.name||'')) : 'مبنى';
      h += '<div style="background:var(--brass-soft);border:1px solid var(--brass);border-radius:10px;padding:10px;margin-bottom:12px">'
        + '<div style="color:var(--brass);margin-bottom:8px">المحدّد · '+tname+'</div>'
        + '<div style="display:flex;gap:6px;flex-wrap:wrap">'
        + '<button data-ed="rotL" style="flex:1;border:1px solid var(--line);background:#0000;color:var(--ink);padding:8px;border-radius:8px">↺</button>'
        + '<button data-ed="rotR" style="flex:1;border:1px solid var(--line);background:#0000;color:var(--ink);padding:8px;border-radius:8px">↻</button>'
        + '<button data-ed="sUp" style="flex:1;border:1px solid var(--line);background:#0000;color:var(--ink);padding:8px;border-radius:8px">＋</button>'
        + '<button data-ed="sDn" style="flex:1;border:1px solid var(--line);background:#0000;color:var(--ink);padding:8px;border-radius:8px">－</button>'
        + '<button data-ed="del" style="flex:1;border:1px solid #c0392b;background:#0000;color:#c0392b;padding:8px;border-radius:8px">🗑</button>'
        + '</div></div>';
    }
"""
+ "    h += '<div style=\"color:var(--brass);margin:6px 0 8px\">الأقسام</div>';")
if RE_OLD not in s: print('✗ renderEditor sections header'); sys.exit(1)
s=s.replace(RE_OLD, RE_NEW, 1)

WE_OLD = "    editorEl.querySelectorAll('[data-delprod]').forEach(b=> b.onclick=()=>{ const a=b.dataset.delprod.split(':'); SECTIONS[+a[0]].products.splice(+a[1],1); rebuildScene(); renderEditor(); });"
WE_NEW = (WE_OLD +
  "\n    editorEl.querySelectorAll('[data-ed]').forEach(b=> b.onclick=()=> _editAction(b.dataset.ed));")
if WE_OLD not in s: print('✗ _wireEditor delprod'); sys.exit(1)
s=s.replace(WE_OLD, WE_NEW, 1)

SVS_OLD = """      x: sec._pos ? sec._pos[0] : undefined,
      z: sec._pos ? sec._pos[1] : undefined,
      products: sec.products.map(pr=>({ id: pr.id, name: pr.name, price: pr.price }))"""
SVS_NEW = """      x: sec._pos ? sec._pos[0] : undefined,
      z: sec._pos ? sec._pos[1] : undefined,
      rot: sec.rot || 0, scale: sec.scale || 1,
      products: sec.products.map(pr=>({ id: pr.id, name: pr.name, price: pr.price }))"""
if SVS_OLD not in s: print('✗ saveScene sections'); sys.exit(1)
s=s.replace(SVS_OLD, SVS_NEW, 1)

SVB_OLD = "    const cleanBuildings = BUILDINGS.map(b=>({ x:b.x, z:b.z, w:b.w, d:b.d, h:b.h, tint:b.tint }));"
SVB_NEW = "    const cleanBuildings = BUILDINGS.map(b=>({ x:b.x, z:b.z, w:b.w, d:b.d, h:b.h, tint:b.tint, rot:b.rot||0, scale:b.scale||1 }));"
if SVB_OLD not in s: print('✗ saveScene buildings'); sys.exit(1)
s=s.replace(SVB_OLD, SVB_NEW, 1)

ANCHOR = "  // [المرحلة 1] جلب المشهد من Firestore عبر الخادم (مع رجوع آمن للافتراضي) ثم البناء"
if ANCHOR not in s: print('✗ مرساة loadScene'); sys.exit(1)
ACT = """  // ===== [المرحلة 2-ب-2] تدوير/تكبير/حذف العنصر المحدّد =====
  function _applyTransform(ed){
    const g = ed.group;
    if(ed.type==='section'){
      g.rotation.y = -ed.ref._side*Math.PI/2 + (ed.ref.rot||0);
    } else {
      g.rotation.y = (ed.ref.rot||0);
    }
    g.scale.setScalar(ed.ref.scale||1);
    if(_hl) _hl.setFromObject(g);
  }
  function _editAction(a){
    const ed = selectedEdit; if(!ed) return;
    const r = ed.ref;
    if(a==='rotL'){ r.rot = (r.rot||0) + Math.PI/12; _applyTransform(ed); }
    else if(a==='rotR'){ r.rot = (r.rot||0) - Math.PI/12; _applyTransform(ed); }
    else if(a==='sUp'){ r.scale = Math.min(3, (r.scale||1)*1.1); _applyTransform(ed); }
    else if(a==='sDn'){ r.scale = Math.max(0.3, (r.scale||1)/1.1); _applyTransform(ed); }
    else if(a==='del'){
      if(ed.type==='section'){ const i=SECTIONS.indexOf(r); if(i>=0) SECTIONS.splice(i,1); }
      else { const i=BUILDINGS.indexOf(r); if(i>=0) BUILDINGS.splice(i,1); }
      clearEditSelection(); rebuildScene(); renderEditor(); toast('حُذف'); return;
    }
  }

"""
s=s.replace(ANCHOR, ACT + ANCHOR, 1)

open(PATH,'w',encoding='utf-8').write(s)
print('✓ تم: تدوير + تكبير + حذف + حفظ rot/scale')
