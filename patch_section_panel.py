import sys
PATH = 'index.html'
s=open(PATH,encoding='utf-8').read()
if '[PATCH] section-panel' in s:
    print('• مُطبّق مسبقاً — تخطّي.'); sys.exit(0)

# 1) ربط البطاقة بقسمها
A='card.position.set(0, ty+0.33, D/2-0.22); card.castShadow=true; card.userData.product=pr;'
if A not in s: print('✗ لم أجد سطر البطاقة'); sys.exit(1)
s=s.replace(A, A+' card.userData.section=sec;',1)

# 2) النقر يفتح القسم بدل منتج واحد
OLD_SEL="""    const hit=raycaster.intersectObjects(interactables, true)[0];
    if(hit) openProduct(hit.object.userData.product);"""
NEW_SEL="""    const hit=raycaster.intersectObjects(interactables, true)[0];
    if(hit && hit.object.userData.section) openSection(hit.object.userData.section);"""
if OLD_SEL not in s: print('✗ لم أجد selectAt'); sys.exit(1)
s=s.replace(OLD_SEL,NEW_SEL,1)

# 3) إضافة openSection بعد openProduct
OLD_OP="""  function openProduct(p){
    pauseWalk(); state.activeProduct=p;
    document.getElementById('pp-index').textContent=`منتج ${String(PRODUCTS.indexOf(p)+1).padStart(2,'0')} / ${PRODUCTS.length}`;
    document.getElementById('pp-name').textContent=p.name;
    document.getElementById('pp-price').innerHTML=`${p.price.toLocaleString('ar')} <small>${CURRENCY}</small>`;
    document.getElementById('pp-desc').textContent=p.description;
    const b=document.getElementById('pp-add'); b.textContent='أضِف إلى السلة'; b.classList.remove('added');
    productPanel.classList.add('open');
  }"""
NEW_OP=OLD_OP + """

  // [PATCH] section-panel: عرض كل منتجات القسم كقائمة في اللوحة اليمنى
  function openSection(sec){
    pauseWalk(); state.activeSection=sec;
    document.getElementById('pp-index').textContent='قسم · ' + sec.products.length + ' منتجات';
    document.getElementById('pp-name').textContent=sec.name;
    document.getElementById('pp-price').style.display='none';
    document.getElementById('pp-add').style.display='none';
    const rows = sec.products.map(pr=>`<div style="display:flex;align-items:center;justify-content:space-between;gap:12px;padding:12px;background:var(--surface-2);border-radius:12px;margin-bottom:10px">
        <div style="flex:1;min-width:0"><b style="display:block;font-size:15px">${pr.name}</b><span style="font-size:13px;color:var(--brass)">${pr.price} ${CURRENCY}</span></div>
        <button class="sec-add" data-id="${pr.id}" style="border:none;background:var(--brass);color:#1a1410;padding:9px 16px;border-radius:10px;font-size:13px;font-weight:700;flex-shrink:0">أضِف</button>
      </div>`).join('');
    const desc=document.getElementById('pp-desc'); desc.innerHTML=rows;
    desc.querySelectorAll('.sec-add').forEach(b=>b.onclick=()=>{
      const pr=sec.products.find(x=>x.id===b.dataset.id);
      addToCart(pr); b.textContent='✓'; setTimeout(()=>b.textContent='أضِف',900);
      toast('أُضيف «' + pr.name + '» إلى السلة');
    });
    productPanel.classList.add('open');
  }"""
if OLD_OP not in s: print('✗ لم أجد openProduct'); sys.exit(1)
s=s.replace(OLD_OP,NEW_OP,1)

# 4) التلميح يعرض اسم القسم
OLD_H="""if(best){ hint.innerHTML=`<b>${best.name}</b> · ${best.price} ${CURRENCY} — انقر للتفاصيل`; hint.classList.add('show'); }"""
NEW_H="""if(best){ hint.innerHTML=`<b>${best.section}</b> — انقر لعرض المنتجات`; hint.classList.add('show'); }"""
if OLD_H in s: s=s.replace(OLD_H,NEW_H,1)
else: print('⚠ لم أجد سطر التلميح (تابعت)')

open(PATH,'w',encoding='utf-8').write(s)
print('✓ تم: اللوحة اليمنى تعرض منتجات القسم مع زر أضِف لكل منتج')
