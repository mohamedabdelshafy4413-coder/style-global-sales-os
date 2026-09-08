def build_email(language, persona, company, contact, product):
    company = company or "[Company]"
    contact = contact or "[Name]"
    product = product or "Egyptian marble & granite"
    value = {
        "Importer":"stable container supply, availability and repeatable quality",
        "Distributor":"repeat supply, portfolio fit and dependable replenishment",
        "Fabricator":"consistent material, finish control and workable formats",
        "Contractor":"project quantities, submittals, schedule and packing reliability",
        "Developer":"project specification, value engineering and dependable delivery",
        "Architect":"samples, technical documentation, finishes and specification support",
        "Procurement":"clear commercial terms, documentation, lead time and risk reduction",
    }.get(persona, "reliable export supply")

    if language == "Arabic":
        subject = f"{contact} — توريد حجر مصري مناسب لـ {company}"
        body = f"""أستاذ/ة {contact}،\n\nأتواصل لأن نشاط {company} قريب من نوع المشترين الذين نخدمهم في التوريد الدولي للحجر الطبيعي.\n\nStyle for Marble & Granite تعمل في الرخام والجرانيت المصري، وبالنسبة لاحتياجكم أرى أن نقطة البداية الأقوى هي: {product}.\n\nبدل إرسال كتالوج عام، لو تبعت لي 4 بيانات فقط — الخامة، المقاس/السُمك، الكمية، وميناء الوصول — أقدر أجهز لك عرض موجه للشحنة يركز على {value}.\n\nهل مشترياتكم الحالية للمخزون/التوزيع أم لمشروع محدد؟\n\nتحياتي،\n[Name]\nStyle for Marble & Granite"""
    elif language == "French":
        subject = f"{contact} — option pierre égyptienne pour {company}"
        body = f"""Bonjour {contact},\n\nJe vous contacte car l’activité de {company} correspond au type d’acheteurs que nous ciblons pour l’export de pierre naturelle égyptienne.\n\nPour commencer, je vous proposerais : {product}.\n\nAu lieu d’un catalogue générique, si vous me partagez matériau + dimensions/épaisseur + quantité + port de destination, nous pouvons préparer une proposition centrée sur {value}.\n\nAchetez-vous actuellement pour stock/distribution ou pour un projet précis ?\n\nCordialement,\n[Name]\nStyle for Marble & Granite"""
    else:
        subject = f"{contact} — Egyptian stone supply option for {company}"
        body = f"""Hi {contact},\n\nI’m reaching out because {company} looks relevant to the type of international buyers we support with Egyptian natural stone.\n\nFor your market, I would start with: {product}.\n\nRather than send a generic catalogue, if you share just four details — material, size/thickness, quantity and destination port — we can prepare a shipment-oriented offer focused on {value}.\n\nAre you currently buying for stock/distribution or for a specific project?\n\nBest regards,\n[Name]\nStyle for Marble & Granite"""
    return subject, body
