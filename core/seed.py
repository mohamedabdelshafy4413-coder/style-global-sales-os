from .database import query_df, execute

MARKETS = [
("السعودية","Saudi Arabia","GCC",82,78,88,88,92,96,90,90,88,72,86,"Arabic / English","Large importer / project contractor","Project procurement + importer","Galala / Sunny / project cut-to-size","Relationship-led; trust, speed and project timing matter.","Verify HS code, VAT, conformity and project-specific rules.","Project delays, approval chains, price pressure.","Sun–Thu, 09:00–11:00 local","DEMO"),
("الإمارات","United Arab Emirates","GCC",85,78,90,90,90,92,92,94,95,74,90,"English / Arabic","Importer-distributor / stone yard","Distributor + re-export hub","Premium slabs / tiles / project supply","Direct, fast and comparison-driven.","Verify UAE customs/VAT and emirate-specific rules.","Intense competition and established supplier networks.","Mon–Thu, 09:00–11:00 local","DEMO"),
("المغرب","Morocco","North Africa",80,75,87,82,82,80,86,90,88,76,92,"French","Importer / distributor","Established importer","Egyptian marble value range","Relationship + value + French localization.","Verify duty/VAT and documentation for exact HS/origin.","French communication and local relationship depth matter.","Tue–Thu, 09:00–11:00 local","DEMO"),
("المملكة المتحدة","United Kingdom","Europe",86,68,83,86,88,79,88,78,84,70,78,"English","Importer / fabricator","Importer-fabricator","Slabs / cut-to-size / project stone","Evidence-led, specification-led, reliability sensitive.","Verify UK Trade Tariff, VAT, origin and standards.","Longer qualification and stronger proof threshold.","Tue–Thu, 09:00–11:00 local","DEMO"),
("الولايات المتحدة","United States","North America",98,70,82,92,98,88,95,54,62,64,58,"English","Large importer / distributor","High-volume importer-distributor","Slabs / tiles / distributor assortment","Scale-oriented and evidence-driven.","Verify current HTS/tariff measures before quote.","Freight, tariffs and long-distance service expectations.","Tue–Thu, 09:00–11:00 recipient local","DEMO"),
("فرنسا","France","Europe",88,65,85,84,86,75,86,75,80,68,76,"French","Importer / fabricator","Importer / specialist distributor","Light marble / design-led stone","Formal, design and quality sensitive.","Verify TARIC/Access2Markets and VAT.","Strong European competition and localization needs.","Tue–Thu, 09:00–11:00 local","DEMO"),
("ألمانيا","Germany","Europe",82,62,82,86,88,82,90,72,76,66,68,"German / English","Importer / fabricator","Technical importer-fabricator","Technical/project stone","Precise, technical and documentation-heavy.","Verify EU tariff, VAT, standards and packaging.","High proof threshold and slower onboarding.","Tue–Thu, 08:30–10:30 local","DEMO"),
("إيطاليا","Italy","Europe",92,58,72,84,90,70,86,72,75,48,60,"Italian / English","Stone trader / fabricator","Specialist stone trader","Selective Egyptian stones","Highly knowledgeable and comparative.","Verify EU tariff/VAT/standards.","World-class local stone industry.","Tue–Thu, 09:00–11:00 local","DEMO"),
("إسبانيا","Spain","Europe",80,63,80,80,82,74,82,76,80,60,70,"Spanish / English","Importer / distributor","Importer / stone distributor","Tiles / slabs","Relationship plus value and availability.","Verify EU customs/VAT.","Strong local/European supply.","Tue–Thu, 09:00–11:00 local","DEMO"),
("كندا","Canada","North America",76,66,82,82,84,78,84,60,68,68,62,"English / French","Importer / distributor","Regional importer","Slabs / tiles","Reliable supply and documentation valued.","Verify CBSA tariff, taxes and wood packaging.","Freight distance and fragmented geography.","Tue–Thu, 09:00–11:00 local","DEMO"),
]

ACCOUNTS = [
("DEMO Gulf Stone Importer","السعودية","Importer","https://example.com","Ahmed Demo","Procurement Director","demo1@example.com","",92,94,88,95,85,80,90,92,180000,"Qualified","2026-09-06","Send current availability + ask RFQ","2026-09-08","DEMO"),
("DEMO Dubai Stone Hub","الإمارات","Distributor","https://example.com","M. Demo","Managing Director","demo2@example.com","",88,92,90,94,76,85,86,84,150000,"Contacted","2026-09-07","Follow up with 3 hero materials","2026-09-08","DEMO"),
("DEMO Morocco Import","المغرب","Importer","https://example.com","Jean Demo","Import Manager","demo3@example.com","",90,82,91,88,80,76,82,90,110000,"Target","","French outreach + availability","2026-09-08","DEMO"),
("DEMO UK Fabricator","المملكة المتحدة","Fabricator","https://example.com","Chris Demo","Purchasing Manager","demo4@example.com","",76,88,86,90,72,70,88,70,90000,"Target","","Send technical/spec pack","2026-09-09","DEMO"),
("DEMO US Distributor","الولايات المتحدة","Distributor","https://example.com","Taylor Demo","Sourcing Director","demo5@example.com","",94,98,82,96,70,58,92,66,320000,"Target","","Validate freight/tariff before outreach","2026-09-10","DEMO"),
]

def seed_demo():
    if query_df("SELECT COUNT(*) n FROM markets").iloc[0]["n"] == 0:
        for r in MARKETS:
            execute("""INSERT INTO markets
            (country_ar,country_en,region,import_demand,import_growth,product_fit,buyer_quality,deal_potential,
             construction,repeat_potential,logistics,market_access,competition_advantage,fast_response,
             language,best_buyer,entry_point,product_focus,business_mindset,customs_note,risk_note,send_window,evidence_status)
             VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", r)
    if query_df("SELECT COUNT(*) n FROM accounts").iloc[0]["n"] == 0:
        for r in ACCOUNTS:
            execute("""INSERT INTO accounts
            (company,country,account_type,website,decision_maker,title,email,linkedin,
             import_activity,purchasing_power,product_fit,repeat_potential,project_activity,
             decision_access,financial_strength,buying_signal,potential_usd,stage,last_contact,next_action,next_date,data_status)
             VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", r)
