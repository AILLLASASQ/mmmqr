import sys
PATH = 'index.html'
s = open(PATH, encoding='utf-8').read()
if '[PATCH] sections' in s:
    print('• مُطبّق مسبقاً — تخطّي.'); sys.exit(0)

OLD1 = """  const PRODUCTS = [
    { id:'p1', name:'كرسي أوريون', price:1290, color:0xC9A24B, shape:'chair', pos:[-7,-12], model:null,
      description:'كرسي بهيكل من خشب الجوز ووسائد جلدية، يجمع الدفء والخطوط الاسكندنافية النظيفة.' },
    { id:'p2', name:'مزهرية لُمى',  price:340,  color:0x8FB6C9, shape:'vase',  pos:[ 7,-6 ], model:null,
      description:'مزهرية خزفية مصنوعة يدوياً بطلاء لامع، لمسة هادئة لأي مساحة.' },
    { id:'p3', name:'مصباح سُهى',   price:560,  color:0xE0C56B, shape:'lamp',  pos:[-7, 0 ], model:null,
      description:'مصباح أرضي بإضاءة دافئة قابلة للتعتيم، يمنح الركن أجواء مسائية.' },
    { id:'p4', name:'طاولة نجمة',   price:980,  color:0xB07A4A, shape:'table', pos:[ 7, 6 ], model:null,
      description:'طاولة جانبية بسطح رخامي وقاعدة معدنية، متينة وأنيقة.' },
    { id:'p5', name:'تمثال فلَك',   price:1750, color:0xC9C2B8, shape:'art',   pos:[-7, 12], model:null,
      description:'قطعة نحتية محدودة الإصدار تتبدّل ألوانها مع زوايا الإضاءة.' },
  ];"""

NEW1 = """  // [PATCH] sections — أقسام نموذجية (غيّر الأسماء/الأسعار/المنتجات كما تشاء)
  const SECTIONS = [
    { id:'pubg', name:'شدات ببجي', side:'right', edge:0x2d6cdf, products:[
      { id:'pubg60',   name:'ببجي 60 شدة',   price:5  },
      { id:'pubg325',  name:'ببجي 325 شدة',  price:25 },
      { id:'pubg660',  name:'ببجي 660 شدة',  price:50 },
      { id:'pubg1800', name:'ببجي 1800 شدة', price:120 },
    ]},
    { id:'fn', name:'فورت نايت', side:'right', edge:0x8e44ad, products:[
      { id:'fn1000', name:'1000 V-Bucks', price:40  },
      { id:'fn2800', name:'2800 V-Bucks', price:100 },
      { id:'fn5000', name:'5000 V-Bucks', price:170 },
    ]},
    { id:'ludo', name:'لودو', side:'right', edge:0xe67e22, products:[
      { id:'ludo_s', name:'لودو ذهب صغير', price:10 },
      { id:'ludo_m', name:'لودو ذهب وسط',  price:30 },
      { id:'ludo_l', name:'لودو ذهب كبير',  price:60 },
    ]},
    { id:'hay', name:'هاي داي', side:'left', edge:0x27ae60, products:[
      { id:'hay1', name:'هاي داي ألماس صغير', price:15 },
      { id:'hay2', name:'هاي داي ألماس وسط',  price:45 },
      { id:'hay3', name:'هاي داي ألماس كبير',  price:90 },
    ]},
    { id:'shaab', name:'شعبيات', side:'left', edge:0xc0392b, products:[
      { id:'sh1', name:'بطاقة شعبية 10', price:10 },
      { id:'sh2', name:'بطاقة شعبية 25', price:25 },
      { id:'sh3', name:'بطاقة شعبية 50', price:50 },
    ]},
  ];

  // توزيع الأقسام على الجدارين
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

if OLD1 not in s: print('✗ لم أجد مصفوفة PRODUCTS'); sys.exit(1)
s = s.replace(OLD1, NEW1, 1)

OLD2 = """  // [PATCH] wall-shelves: رفوف مرتفعة على الجدران (يسار/يمين)
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

NEW2 = """  // [PATCH] sections: وحدة رفوف (جندولة) لكل قسم + لافتة + بطاقات منتجاته
  const shelfBoxes = [];
  function labelTexture(text, color){
    const c=document.createElement('canvas'); c.width=512; c.height=128; const x=c.getContext('2d');
    x.fillStyle='#'+color.toString(16).padStart(6,'0'); x.fillRect(0,0,512,128);
    x.fillStyle='#ffffff'; x.font='bold 60px system-ui, sans-serif'; x.textAlign='center'; x.textBaseline='middle'; x.direction='rtl';
    x.fillText(text, 256, 70);
    const t=new THREE.CanvasTexture(c); t.colorSpace=THREE.SRGBColorSpace; return t;
  }
  function cardTexture(pr, color){
    const c=document.createElement('canvas'); c.width=256; c.height=320; const x=c.getContext('2d');
    x.fillStyle='#'+color.toString(16).padStart(6,'0'); x.fillRect(0,0,256,320);
    x.fillStyle='rgba(0,0,0,.25)'; x.fillRect(0,232,256,88);
    x.fillStyle='#ffffff'; x.textAlign='center'; x.direction='rtl';
    x.font='bold 28px system-ui, sans-serif'; x.fillText(pr.name, 128, 150);
    x.font='bold 40px system-ui, sans-serif'; x.fillText(pr.price + ' ' + CURRENCY, 128, 282);
    const t=new THREE.CanvasTexture(c); t.colorSpace=THREE.SRGBColorSpace; return t;
  }
  function buildSection(sec){
    const [x,z]=sec._pos, side=sec._side;
    const g=new THREE.Group(); g.position.set(x,0,z); g.rotation.y=-side*Math.PI/2;
    const W=2.4, D=1.0, n=sec.products.length, tier=0.7, baseH=0.35, top=0.55;
    const H=baseH + n*tier + top;
    const metal=new THREE.MeshStandardMaterial({color:0xe9e9ec, roughness:.55, metalness:.15});
    const edgeMat=new THREE.MeshStandardMaterial({color:sec.edge, roughness:.5});

    const back=new THREE.Mesh(new THREE.BoxGeometry(W,H,0.08), metal); back.position.set(0,H/2,-D/2); back.receiveShadow=true; g.add(back);
    const base=new THREE.Mesh(new THREE.BoxGeometry(W,baseH,D), metal); base.position.set(0,baseH/2,0); base.castShadow=true; base.receiveShadow=true; g.add(base);
    for(const sx of [-W/2+0.05, W/2-0.05]){
      const post=new THREE.Mesh(new THREE.BoxGeometry(0.07,H,0.07), metal); post.position.set(sx,H/2,-D/2+0.04); g.add(post);
    }
    sec.products.forEach((pr,i)=>{
      const ty=baseH + (i+0.5)*tier;
      const shelf=new THREE.Mesh(new THREE.BoxGeometry(W-0.12,0.05,D-0.12), metal); shelf.position.set(0,ty,0); shelf.castShadow=true; shelf.receiveShadow=true; g.add(shelf);
      const edge=new THREE.Mesh(new THREE.BoxGeometry(W-0.12,0.06,0.05), edgeMat); edge.position.set(0,ty,(D-0.12)/2); g.add(edge);
      const front=new THREE.MeshStandardMaterial({map:cardTexture(pr,sec.edge), roughness:.4});
      const plain=new THREE.MeshStandardMaterial({color:sec.edge, roughness:.5});
      const card=new THREE.Mesh(new THREE.BoxGeometry(0.5,0.6,0.06), [plain,plain,plain,plain,front,plain]);
      card.position.set(0, ty+0.33, D/2-0.22); card.castShadow=true; card.userData.product=pr;
      g.add(card); interactables.push(card); productMeshes[pr.id]=card;
    });
    const sign=new THREE.Mesh(new THREE.PlaneGeometry(W+0.2,0.7), new THREE.MeshBasicMaterial({map:labelTexture(sec.name,sec.edge)}));
    sign.position.set(0, H+0.45, D/2-0.02); g.add(sign);

    scene.add(g);
    g.updateWorldMatrix(true,true);
    const bb=new THREE.Box3().setFromObject(g);
    shelfBoxes.push({minX:bb.min.x,maxX:bb.max.x,minZ:bb.min.z,maxZ:bb.max.z});
  }
  function buildSections(){ SECTIONS.forEach(buildSection); }"""

if OLD2 not in s: print('✗ لم أجد دالة addStand'); sys.exit(1)
s = s.replace(OLD2, NEW2, 1)

if '  PRODUCTS.forEach(addStand);' not in s: print('✗ لم أجد نداء addStand'); sys.exit(1)
s = s.replace('  PRODUCTS.forEach(addStand);', '  buildSections();', 1)

if '    for(const b of buildingBoxes){' not in s: print('✗ لم أجد حلقة التصادم'); sys.exit(1)
s = s.replace('    for(const b of buildingBoxes){', '    for(const b of buildingBoxes.concat(shelfBoxes)){', 1)

open(PATH,'w',encoding='utf-8').write(s)
print('✓ تم: نظام الأقسام (جندولة) + توزيع + تصادم')
