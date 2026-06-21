# Abeto Store — متجر 3D بأسلوب الأنمي

واجهة Three.js (Cel-shading + OutlineEffect) تعتمد على نماذج .glb، مع خادم Node خفيف جاهز لـ Render وخطاف Firestore.

## التشغيل محلياً
```
npm install
npm start        # http://localhost:3000
```

## النشر على Render
1. ادفع المشروع إلى مستودع GitHub.
2. على Render: New → Web Service → اربط المستودع.
3. Build: `npm install` — Start: `node server.js` (أو اعتمد render.yaml تلقائياً).

## Firestore (اختياري)
- `npm i firebase-admin`
- أضف متغير البيئة `FIREBASE_SERVICE_ACCOUNT` (محتوى مفتاح الخدمة JSON).
- فعّل الأسطر المعلّقة في `server.js` (تهيئة admin + قراءة/كتابة).

## النماذج
ضع ملفات .glb داخل `models/` (انظر models/README.md). استبدل المسارات الوهمية في index.html.
