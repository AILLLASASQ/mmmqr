import sys
PATH='index.html'
s=open(PATH,encoding='utf-8').read()
if 'function loadScene' in s:
    print('• مُطبّق مسبقاً — تخطّي.'); sys.exit(0)

OLD1 = """  // توزيع الأقسام على الجدارين
  const _rightZ=[-10,0,10], _leftZ=[-6,6]; let _ri=0,_li=0;
  SECTIONS.forEach(sec=>{
    if(sec.side==='right'){ sec._pos=[7, _rightZ[_ri++]]; sec._side=1; }
    else { sec._pos=[-7, _leftZ[_li++]]; sec._side=-1; }
  });

  // تسطيح المنتجات (يستخدمه باقي الكود: السلة/التلميح/الوضع 2D)
  const PRODUCTS = [];
  SECTIONS.forEach(sec=> sec.products.forEach(pr=>{
    pr.color=sec.edge; pr.section=sec.name; pr.pos=sec._pos;
    if(!pr.description) pr.description = sec.name + ' — ' + pr.name + '. بطاقة رقمية تُسلَّم فوراً بعد الدفع.';
    PRODUCTS.push(pr);
  }));"""
NEW1 = """  // [المرحلة 1] PRODUCTS تُملأ بعد جلب المشهد (انظر prepareData / loadScene بالأسفل)
  const PRODUCTS = [];
  function prepareData(){
    PRODUCTS.length = 0;
    let ri=0, li=0;
    SECTIONS.forEach(sec=>{
      if(sec.side==='right'){ sec._pos=[7, -10 + ri*8]; sec._side=1; ri++; }
      else { sec._pos=[-7, -6 + li*8]; sec._side=-1; li++; }
      sec.products.forEach(pr=>{
        pr.color = (pr.color!==undefined) ? pr.color : sec.edge;
        pr.section = sec.name; pr.pos = sec._pos;
        if(!pr.description) pr.description = sec.name + ' — ' + pr.name + '. بطاقة رقمية تُسلَّم فوراً بعد الدفع.';
        PRODUCTS.push(pr);
      });
    });
  }"""
if OLD1 not in s: print('✗ لم أجد كتلة التوزيع/التسطيح'); sys.exit(1)
s = s.replace(OLD1, NEW1, 1)

if "  (function buildGrid(){" not in s: print('✗ لم أجد buildGrid'); sys.exit(1)
s = s.replace("  (function buildGrid(){", "  function buildGrid(){", 1)

OLD2_TAIL = """    document.querySelectorAll('[data-add]').forEach(b=>b.onclick=()=>{ addToCart(PRODUCTS.find(p=>p.id===b.dataset.add)); toast('أُضيف إلى السلة'); });
  })();"""
NEW2_TAIL = """    document.querySelectorAll('[data-add]').forEach(b=>b.onclick=()=>{ addToCart(PRODUCTS.find(p=>p.id===b.dataset.add)); toast('أُضيف إلى السلة'); });
  }"""
if OLD2_TAIL not in s: print('✗ لم أجد نهاية buildGrid'); sys.exit(1)
s = s.replace(OLD2_TAIL, NEW2_TAIL, 1)

OLD3 = """  buildSections();
  renderCart();
  animate();"""
NEW3 = """  // [المرحلة 1] جلب المشهد من Firestore عبر الخادم (مع رجوع آمن للافتراضي) ثم البناء
  async function loadScene(){
    try{
      const r = await fetch('/api/scene');
      if(r.ok){
        const data = await r.json();
        if(data && Array.isArray(data.sections) && data.sections.length){
          SECTIONS.length = 0; data.sections.forEach(sec=>SECTIONS.push(sec));
          console.log('[scene] حُمِّل من الخادم:', data.sections.length, 'أقسام');
        }
      }
    }catch(e){ console.warn('[scene] تعذّر الجلب — استخدام الافتراضي', e); }
    prepareData();
    buildSections();
    buildGrid();
    renderCart();
  }
  loadScene();
  animate();"""
if OLD3 not in s: print('✗ لم أجد كتلة الإقلاع'); sys.exit(1)
s = s.replace(OLD3, NEW3, 1)

open(PATH,'w',encoding='utf-8').write(s)
print('✓ تم: الموقع يقرأ /api/scene عند الإقلاع مع رجوع آمن')
