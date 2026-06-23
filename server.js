const express = require('express');
const path = require('path');
const { initializeApp, cert, getApps } = require('firebase-admin/app');
const { getFirestore, FieldValue } = require('firebase-admin/firestore');

const app = express();
const PORT = process.env.PORT || 3000;
let db = null;

try {
    if (process.env.FIREBASE_SERVICE_ACCOUNT) {
        const serviceAccount = JSON.parse(process.env.FIREBASE_SERVICE_ACCOUNT);
        if (!getApps().length) {
            initializeApp({
                credential: cert(serviceAccount)
            });
        }
        db = getFirestore();
        console.log("✅ تم الاتصال بـ Firebase بنجاح");
    } else {
        console.warn("⚠️ تحذير: متغير FIREBASE_SERVICE_ACCOUNT غير موجود في إعدادات Render.");
    }
} catch (error) {
    console.error("❌ خطأ في تهيئة Firebase:", error);
}

const PRODUCTS = [
  { id:'p1', name:'كرسي أوريون', price:1290, model:'models/products/chair.glb',  description:'كرسي بهيكل خشب الجوز ووسائد جلدية.' },
  { id:'p2', name:'مزهرية لُمى',  price:340,  model:'models/products/vase.glb',   description:'مزهرية خزفية بطلاء لامع.' },
  { id:'p3', name:'مصباح سُهى',   price:560,  model:'models/products/lamp.glb',   description:'مصباح أرضي بإضاءة دافئة.' },
  { id:'p4', name:'طاولة نجمة',   price:980,  model:'models/products/table.glb',  description:'طاولة جانبية بسطح رخامي.' },
  { id:'p5', name:'تمثال فلَك',   price:1750, model:'models/products/statue.glb', description:'قطعة نحتية محدودة الإصدار.' },
];

app.use(express.json());
app.use(express.static(path.join(__dirname)));

app.get('/api/products', async (req, res) => {
    if (!db) return res.json(PRODUCTS);
    try {
        const snapshot = await db.collection('products').get();
        if (snapshot.empty) return res.json(PRODUCTS);
        const products = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
        res.json(products);
    } catch (e) {
        res.status(500).json({ error: 'فشل جلب المنتجات من Firestore' });
    }
});

app.post('/api/orders', async (req, res) => {
    if (!db) return res.status(500).json({ error: 'قاعدة البيانات غير متصلة' });
    try {
        await db.collection('orders').add({
            items: req.body.items,
            total: req.body.total,
            createdAt: FieldValue.serverTimestamp()
        });
        res.json({ success: true, message: 'تم حفظ الطلب بنجاح' });
    } catch (e) {
        res.status(500).json({ error: 'فشل حفظ الطلب' });
    }
});

// ===== [المرحلة 1] تخطيط المشهد (Scene Layout) =====
app.get('/api/scene', async (req, res) => {
    if (!db) return res.json(null);
    try {
        const doc = await db.collection('scene').doc('layout').get();
        res.json(doc.exists ? doc.data() : null);
    } catch (e) {
        res.status(500).json({ error: 'فشل جلب المشهد' });
    }
});

function requireAdmin(req, res, next) {
    const token = req.get('x-admin-token');
    if (!process.env.ADMIN_TOKEN) return res.status(500).json({ error: 'ADMIN_TOKEN غير مضبوط على الخادم' });
    if (token !== process.env.ADMIN_TOKEN) return res.status(401).json({ error: 'غير مصرّح' });
    next();
}

app.post('/api/admin/check', requireAdmin, (req, res) => res.json({ ok: true }));

app.post('/api/admin/save', requireAdmin, async (req, res) => {
    if (!db) return res.status(500).json({ error: 'قاعدة البيانات غير متصلة' });
    try {
        const layout = req.body && req.body.layout;
        if (!layout || typeof layout !== 'object') return res.status(400).json({ error: 'تخطيط غير صالح' });
        await db.collection('scene').doc('layout').set({
            ...layout,
            updatedAt: FieldValue.serverTimestamp()
        });
        res.json({ success: true });
    } catch (e) {
        res.status(500).json({ error: 'فشل حفظ المشهد' });
    }
});

app.get('*', (req, res) => res.sendFile(path.join(__dirname, 'index.html')));

app.listen(PORT, () => console.log(`🚀 الخادم يعمل على المنفذ ${PORT}`));
