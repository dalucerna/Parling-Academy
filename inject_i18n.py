#!/usr/bin/env python3
"""
inject_i18n.py — Injects a complete i18n translation system into the 7
Parling Academy subpages (ingles.html, espanol.html, frances.html,
aleman.html, italiano.html, portugues.html, chino.html).

For each page:
  1. Removes any existing lang-picker JS block.
  2. Keeps the toggle-panels JS block intact.
  3. Injects a new <script> block (before </body>) with:
       - LANGS object (all common UI strings in 7 languages)
       - PAGE_DATA object (per-page hero content in 7 languages)
       - applyLang() function
       - lang-picker event handlers (open/close + language selection)
       - on-load language application
"""

import os
import re

BASE = "/srv/code/david/workspace/Parling-Academy"

# ---------------------------------------------------------------------------
# Common LANGS object (inline JS, will be embedded verbatim)
# ---------------------------------------------------------------------------

LANGS_JS = r"""  const LANGS = {
    en: {
      nav_home: 'Home',
      nav_live: 'Live Classes',
      nav_1to1: '1 to 1',
      nav_contact: 'Contact',
      nav_comp: 'Para empresas',
      nav_cta: 'Empieza gratis',
      back_link: '\u2190 All languages',
      toggle_group: 'Group',
      toggle_individual: 'Individual 1:1',
      toggle_starter: 'Starter',
      label_monthly: 'Monthly',
      label_annual: 'Annual',
      label_companies: 'Companies',
      note_monthly: 'Month to month \u00b7 no contract',
      note_annual: 'Single annual payment',
      note_companies: 'For teams and organizations',
      per_month: '/mo',
      savings: 'Save $4,044/year',
      inc_live: '4 live classes/mo',
      inc_groups: 'Max 4 students per group',
      inc_material: 'Material included',
      inc_platform: 'Platform access',
      inc_whatsapp: 'WhatsApp support',
      inc_recorded: 'Recorded classes 24hr',
      inc_invoice: 'Business invoice',
      inc_private: 'Private groups',
      btn_enroll: 'Enroll',
      btn_contact: 'Contact',
      specials_title: 'Special rates',
      badge_founder: 'Founder \u221230%',
      badge_friend: 'Refer a friend \u221215%',
      badge_scholarship: 'Scholarship \u221240%',
      chip_founder: 'Founder price',
      chip_referral: 'Referral',
      chip_scholarship: 'Academic scholarship',
      chip_note_founder: 'Limited spots',
      chip_note_referral: 'Per referral',
      chip_note_scholarship: 'Upon request',
      ind_note: 'per 1:1 class \u00b7 4 classes/mo',
      ind_inc_1: '100% personalized class',
      ind_inc_2: 'Flexible schedule',
      ind_inc_3: 'Exclusive teacher attention',
      ind_inc_4: 'Material tailored to your goals',
      ind_inc_5: 'WhatsApp support',
      starter_note: 'entry plan \u00b7 monthly \u00b7 2 classes/mo',
      starter_inc_1: '2 live classes/mo',
      starter_inc_2: 'Max 6 students per group',
      starter_inc_3: 'Basic material included',
      starter_inc_4: 'Platform access',
      starter_inc_5: 'WhatsApp support',
      popular_badge: '\u2605 Most popular',
      features_h2: "What's included in your plan",
      feat1_title: 'Live Classes',
      feat1_desc: 'With certified native teachers',
      feat2_title: 'Learning Material',
      feat2_desc: 'Updated content adapted to your level',
      feat3_title: 'AI 24/7',
      feat3_desc: 'Practice anytime with our AI tutor',
      feat4_title: 'Mobile App',
      feat4_desc: 'Take your lessons anywhere',
      feat5_title: 'Certificate',
      feat5_desc: 'Recognized by companies and universities',
      feat6_title: 'Community',
      feat6_desc: 'Groups by language and level, weekly challenges',
      cta_p: 'Start today with a free trial class.',
      cta_btn: 'Start free',
    },
    es: {
      nav_home: 'Inicio',
      nav_live: 'Clases en vivo',
      nav_1to1: '1 a 1',
      nav_contact: 'Contacto',
      nav_comp: 'Para empresas',
      nav_cta: 'Empieza gratis',
      back_link: '\u2190 Todos los idiomas',
      toggle_group: 'Grupal',
      toggle_individual: 'Individual 1:1',
      toggle_starter: 'Starter',
      label_monthly: 'Mensual',
      label_annual: 'Anual',
      label_companies: 'Empresas',
      note_monthly: 'Mes a mes \u00b7 sin contrato',
      note_annual: 'Pago \u00fanico anual',
      note_companies: 'Para equipos y organizaciones',
      per_month: '/mes',
      savings: 'Ahorr\u00e1s $4,044 al a\u00f1o',
      inc_live: '4 clases en vivo/mes',
      inc_groups: 'Grupos m\u00e1x. 4 alumnos',
      inc_material: 'Material incluido',
      inc_platform: 'Acceso plataforma',
      inc_whatsapp: 'Soporte WhatsApp',
      inc_recorded: 'Clases grabadas 24hr',
      inc_invoice: 'Factura empresarial',
      inc_private: 'Grupos privados',
      btn_enroll: 'Inscribirme',
      btn_contact: 'Contactar',
      specials_title: 'Tarifas especiales',
      badge_founder: 'Fundador \u221230%',
      badge_friend: 'Trae un amigo \u221215%',
      badge_scholarship: 'Beca \u221240%',
      chip_founder: 'Precio fundador',
      chip_referral: 'Referido',
      chip_scholarship: 'Beca acad\u00e9mica',
      chip_note_founder: 'Cupos limitados',
      chip_note_referral: 'Por referido',
      chip_note_scholarship: 'Previa solicitud',
      ind_note: 'por clase 1 a 1 \u00b7 4 clases / mes',
      ind_inc_1: 'Clase 100% personalizada',
      ind_inc_2: 'Horario flexible',
      ind_inc_3: 'Atenci\u00f3n exclusiva del profesor',
      ind_inc_4: 'Material adaptado a tus objetivos',
      ind_inc_5: 'Soporte WhatsApp',
      starter_note: 'plan de entrada \u00b7 mensual \u00b7 2 clases / mes',
      starter_inc_1: '2 clases en vivo/mes',
      starter_inc_2: 'Grupos m\u00e1x. 6 alumnos',
      starter_inc_3: 'Material b\u00e1sico incluido',
      starter_inc_4: 'Acceso a plataforma',
      starter_inc_5: 'Soporte WhatsApp',
      popular_badge: '\u2605 M\u00e1s popular',
      features_h2: 'Qu\u00e9 incluye tu plan',
      feat1_title: 'Clases en vivo',
      feat1_desc: 'Con profesores nativos certificados',
      feat2_title: 'Material did\u00e1ctico',
      feat2_desc: 'Contenido actualizado y adaptado al nivel',
      feat3_title: 'IA 24/7',
      feat3_desc: 'Practica en cualquier momento con nuestro tutor IA',
      feat4_title: 'App m\u00f3vil',
      feat4_desc: 'Lleva tus lecciones a donde vayas',
      feat5_title: 'Certificado',
      feat5_desc: 'Reconocido por empresas y universidades',
      feat6_title: 'Comunidad',
      feat6_desc: 'Grupos por idioma y nivel, retos semanales',
      cta_p: 'Empieza hoy con una clase de prueba gratuita.',
      cta_btn: 'Empieza gratis',
    },
    fr: {
      nav_home: 'Accueil',
      nav_live: 'Cours en direct',
      nav_1to1: '1 pour 1',
      nav_contact: 'Contact',
      nav_comp: 'Pour les entreprises',
      nav_cta: 'Commencer gratuitement',
      back_link: '\u2190 Toutes les langues',
      toggle_group: 'Groupe',
      toggle_individual: 'Individuel 1:1',
      toggle_starter: 'D\u00e9butant',
      label_monthly: 'Mensuel',
      label_annual: 'Annuel',
      label_companies: 'Entreprises',
      note_monthly: 'Mois par mois \u00b7 sans engagement',
      note_annual: 'Paiement annuel unique',
      note_companies: 'Pour les \u00e9quipes et organisations',
      per_month: '/mois',
      savings: '\u00c9conomisez 4\u202f044\u202f$/an',
      inc_live: '4 cours en direct/mois',
      inc_groups: 'Groupes max. 4 \u00e9l\u00e8ves',
      inc_material: 'Mat\u00e9riel inclus',
      inc_platform: 'Acc\u00e8s plateforme',
      inc_whatsapp: 'Support WhatsApp',
      inc_recorded: 'Cours enregistr\u00e9s 24h',
      inc_invoice: 'Facture entreprise',
      inc_private: 'Groupes priv\u00e9s',
      btn_enroll: "M'inscrire",
      btn_contact: 'Contacter',
      specials_title: 'Tarifs sp\u00e9ciaux',
      badge_founder: 'Fondateur \u221230%',
      badge_friend: 'Parrainage \u221215%',
      badge_scholarship: 'Bourse \u221240%',
      chip_founder: 'Prix fondateur',
      chip_referral: 'Parrainage',
      chip_scholarship: 'Bourse acad\u00e9mique',
      chip_note_founder: 'Places limit\u00e9es',
      chip_note_referral: 'Par parrainage',
      chip_note_scholarship: 'Sur demande',
      ind_note: 'par cours 1:1 \u00b7 4 cours/mois',
      ind_inc_1: 'Cours 100% personnalis\u00e9',
      ind_inc_2: 'Horaire flexible',
      ind_inc_3: 'Attention exclusive du professeur',
      ind_inc_4: 'Mat\u00e9riel adapt\u00e9 \u00e0 vos objectifs',
      ind_inc_5: 'Support WhatsApp',
      starter_note: 'plan entr\u00e9e \u00b7 mensuel \u00b7 2 cours/mois',
      starter_inc_1: '2 cours en direct/mois',
      starter_inc_2: 'Groupes max. 6 \u00e9l\u00e8ves',
      starter_inc_3: 'Mat\u00e9riel de base inclus',
      starter_inc_4: 'Acc\u00e8s plateforme',
      starter_inc_5: 'Support WhatsApp',
      popular_badge: '\u2605 Le plus populaire',
      features_h2: 'Ce qui est inclus dans votre plan',
      feat1_title: 'Cours en direct',
      feat1_desc: 'Avec des enseignants natifs certifi\u00e9s',
      feat2_title: 'Mat\u00e9riel p\u00e9dagogique',
      feat2_desc: 'Contenu mis \u00e0 jour et adapt\u00e9 au niveau',
      feat3_title: 'IA 24/7',
      feat3_desc: 'Pratiquez \u00e0 tout moment avec notre tuteur IA',
      feat4_title: 'Application mobile',
      feat4_desc: 'Emportez vos le\u00e7ons partout',
      feat5_title: 'Certificat',
      feat5_desc: 'Reconnu par les entreprises et universit\u00e9s',
      feat6_title: 'Communaut\u00e9',
      feat6_desc: 'Groupes par langue et niveau, d\u00e9fis hebdomadaires',
      cta_p: "Commencez aujourd'hui avec un cours d'essai gratuit.",
      cta_btn: 'Commencer gratuitement',
    },
    de: {
      nav_home: 'Startseite',
      nav_live: 'Live-Kurse',
      nav_1to1: '1 zu 1',
      nav_contact: 'Kontakt',
      nav_comp: 'F\u00fcr Unternehmen',
      nav_cta: 'Kostenlos starten',
      back_link: '\u2190 Alle Sprachen',
      toggle_group: 'Gruppe',
      toggle_individual: 'Einzeln 1:1',
      toggle_starter: 'Starter',
      label_monthly: 'Monatlich',
      label_annual: 'J\u00e4hrlich',
      label_companies: 'Unternehmen',
      note_monthly: 'Monat f\u00fcr Monat \u00b7 kein Vertrag',
      note_annual: 'Einmalige Jahreszahlung',
      note_companies: 'F\u00fcr Teams und Organisationen',
      per_month: '/Monat',
      savings: 'Spare 4.044\u202f$/Jahr',
      inc_live: '4 Live-Kurse/Monat',
      inc_groups: 'Gruppen max. 4 Sch\u00fcler',
      inc_material: 'Material inklusive',
      inc_platform: 'Plattformzugang',
      inc_whatsapp: 'WhatsApp-Support',
      inc_recorded: 'Aufgezeichnete Kurse 24h',
      inc_invoice: 'Unternehmensrechnung',
      inc_private: 'Private Gruppen',
      btn_enroll: 'Anmelden',
      btn_contact: 'Kontakt',
      specials_title: 'Sonderpreise',
      badge_founder: 'Gr\u00fcnder \u221230%',
      badge_friend: 'Freund werben \u221215%',
      badge_scholarship: 'Stipendium \u221240%',
      chip_founder: 'Gr\u00fcnderpreis',
      chip_referral: 'Empfehlung',
      chip_scholarship: 'Akademisches Stipendium',
      chip_note_founder: 'Begrenzte Pl\u00e4tze',
      chip_note_referral: 'Pro Empfehlung',
      chip_note_scholarship: 'Auf Anfrage',
      ind_note: 'pro 1:1-Kurs \u00b7 4 Kurse/Monat',
      ind_inc_1: '100% personalisierter Kurs',
      ind_inc_2: 'Flexibler Stundenplan',
      ind_inc_3: 'Exklusive Lehrerbetreuung',
      ind_inc_4: 'Material auf deine Ziele abgestimmt',
      ind_inc_5: 'WhatsApp-Support',
      starter_note: 'Einsteiger-Plan \u00b7 monatlich \u00b7 2 Kurse/Monat',
      starter_inc_1: '2 Live-Kurse/Monat',
      starter_inc_2: 'Gruppen max. 6 Sch\u00fcler',
      starter_inc_3: 'Grundmaterial inklusive',
      starter_inc_4: 'Plattformzugang',
      starter_inc_5: 'WhatsApp-Support',
      popular_badge: '\u2605 Am beliebtesten',
      features_h2: 'Was dein Plan beinhaltet',
      feat1_title: 'Live-Kurse',
      feat1_desc: 'Mit zertifizierten Muttersprachlern',
      feat2_title: 'Lernmaterial',
      feat2_desc: 'Aktueller niveaugerechter Inhalt',
      feat3_title: 'KI 24/7',
      feat3_desc: '\u00dcbe jederzeit mit unserem KI-Tutor',
      feat4_title: 'Mobile App',
      feat4_desc: 'Nimm deine Lektionen \u00fcberallhin mit',
      feat5_title: 'Zertifikat',
      feat5_desc: 'Von Unternehmen und Universit\u00e4ten anerkannt',
      feat6_title: 'Gemeinschaft',
      feat6_desc: 'Gruppen nach Sprache und Niveau, w\u00f6chentliche Challenges',
      cta_p: 'Starte heute mit einer kostenlosen Probestunde.',
      cta_btn: 'Kostenlos starten',
    },
    it: {
      nav_home: 'Home',
      nav_live: 'Lezioni dal vivo',
      nav_1to1: '1 a 1',
      nav_contact: 'Contatto',
      nav_comp: 'Per le aziende',
      nav_cta: 'Inizia gratis',
      back_link: '\u2190 Tutte le lingue',
      toggle_group: 'Gruppo',
      toggle_individual: 'Individuale 1:1',
      toggle_starter: 'Starter',
      label_monthly: 'Mensile',
      label_annual: 'Annuale',
      label_companies: 'Aziende',
      note_monthly: 'Mese per mese \u00b7 senza contratto',
      note_annual: 'Pagamento annuale unico',
      note_companies: 'Per team e organizzazioni',
      per_month: '/mese',
      savings: 'Risparmia $4.044/anno',
      inc_live: '4 lezioni dal vivo/mese',
      inc_groups: 'Gruppi max. 4 studenti',
      inc_material: 'Materiale incluso',
      inc_platform: 'Accesso piattaforma',
      inc_whatsapp: 'Supporto WhatsApp',
      inc_recorded: 'Lezioni registrate 24h',
      inc_invoice: 'Fattura aziendale',
      inc_private: 'Gruppi privati',
      btn_enroll: 'Iscrivermi',
      btn_contact: 'Contattare',
      specials_title: 'Tariffe speciali',
      badge_founder: 'Fondatore \u221230%',
      badge_friend: 'Porta un amico \u221215%',
      badge_scholarship: 'Borsa \u221240%',
      chip_founder: 'Prezzo fondatore',
      chip_referral: 'Referral',
      chip_scholarship: 'Borsa di studio',
      chip_note_founder: 'Posti limitati',
      chip_note_referral: 'Per referral',
      chip_note_scholarship: 'Previa richiesta',
      ind_note: 'per lezione 1:1 \u00b7 4 lezioni/mese',
      ind_inc_1: 'Lezione 100% personalizzata',
      ind_inc_2: 'Orario flessibile',
      ind_inc_3: 'Attenzione esclusiva del professore',
      ind_inc_4: 'Materiale adattato ai tuoi obiettivi',
      ind_inc_5: 'Supporto WhatsApp',
      starter_note: 'piano di ingresso \u00b7 mensile \u00b7 2 lezioni/mese',
      starter_inc_1: '2 lezioni dal vivo/mese',
      starter_inc_2: 'Gruppi max. 6 studenti',
      starter_inc_3: 'Materiale base incluso',
      starter_inc_4: 'Accesso piattaforma',
      starter_inc_5: 'Supporto WhatsApp',
      popular_badge: '\u2605 Il pi\u00f9 popolare',
      features_h2: 'Cosa include il tuo piano',
      feat1_title: 'Lezioni dal vivo',
      feat1_desc: 'Con insegnanti madrelingua certificati',
      feat2_title: 'Materiale didattico',
      feat2_desc: 'Contenuto aggiornato e adattato al livello',
      feat3_title: 'IA 24/7',
      feat3_desc: 'Pratica in qualsiasi momento con il nostro tutor IA',
      feat4_title: 'App mobile',
      feat4_desc: 'Porta le tue lezioni ovunque tu vada',
      feat5_title: 'Certificato',
      feat5_desc: 'Riconosciuto da aziende e universit\u00e0',
      feat6_title: 'Comunit\u00e0',
      feat6_desc: 'Gruppi per lingua e livello, sfide settimanali',
      cta_p: 'Inizia oggi con una lezione di prova gratuita.',
      cta_btn: 'Inizia gratis',
    },
    pt: {
      nav_home: 'In\u00edcio',
      nav_live: 'Aulas ao vivo',
      nav_1to1: '1 para 1',
      nav_contact: 'Contato',
      nav_comp: 'Para empresas',
      nav_cta: 'Comece gr\u00e1tis',
      back_link: '\u2190 Todos os idiomas',
      toggle_group: 'Grupo',
      toggle_individual: 'Individual 1:1',
      toggle_starter: 'Iniciante',
      label_monthly: 'Mensal',
      label_annual: 'Anual',
      label_companies: 'Empresas',
      note_monthly: 'M\u00eas a m\u00eas \u00b7 sem contrato',
      note_annual: 'Pagamento anual \u00fanico',
      note_companies: 'Para equipes e organiza\u00e7\u00f5es',
      per_month: '/m\u00eas',
      savings: 'Economize $4.044/ano',
      inc_live: '4 aulas ao vivo/m\u00eas',
      inc_groups: 'Grupos m\u00e1x. 4 alunos',
      inc_material: 'Material inclu\u00eddo',
      inc_platform: 'Acesso \u00e0 plataforma',
      inc_whatsapp: 'Suporte WhatsApp',
      inc_recorded: 'Aulas gravadas 24h',
      inc_invoice: 'Nota fiscal empresarial',
      inc_private: 'Grupos privados',
      btn_enroll: 'Inscrever-me',
      btn_contact: 'Contatar',
      specials_title: 'Tarifas especiais',
      badge_founder: 'Fundador \u221230%',
      badge_friend: 'Indique um amigo \u221215%',
      badge_scholarship: 'Bolsa \u221240%',
      chip_founder: 'Pre\u00e7o fundador',
      chip_referral: 'Indica\u00e7\u00e3o',
      chip_scholarship: 'Bolsa acad\u00eamica',
      chip_note_founder: 'Vagas limitadas',
      chip_note_referral: 'Por indica\u00e7\u00e3o',
      chip_note_scholarship: 'Mediante solicita\u00e7\u00e3o',
      ind_note: 'por aula 1:1 \u00b7 4 aulas/m\u00eas',
      ind_inc_1: 'Aula 100% personalizada',
      ind_inc_2: 'Hor\u00e1rio flex\u00edvel',
      ind_inc_3: 'Aten\u00e7\u00e3o exclusiva do professor',
      ind_inc_4: 'Material adaptado aos seus objetivos',
      ind_inc_5: 'Suporte WhatsApp',
      starter_note: 'plano de entrada \u00b7 mensal \u00b7 2 aulas/m\u00eas',
      starter_inc_1: '2 aulas ao vivo/m\u00eas',
      starter_inc_2: 'Grupos m\u00e1x. 6 alunos',
      starter_inc_3: 'Material b\u00e1sico inclu\u00eddo',
      starter_inc_4: 'Acesso \u00e0 plataforma',
      starter_inc_5: 'Suporte WhatsApp',
      popular_badge: '\u2605 Mais popular',
      features_h2: 'O que est\u00e1 inclu\u00eddo no seu plano',
      feat1_title: 'Aulas ao vivo',
      feat1_desc: 'Com professores nativos certificados',
      feat2_title: 'Material did\u00e1tico',
      feat2_desc: 'Conte\u00fado atualizado e adaptado ao n\u00edvel',
      feat3_title: 'IA 24/7',
      feat3_desc: 'Pratique a qualquer momento com nosso tutor IA',
      feat4_title: 'App m\u00f3vel',
      feat4_desc: 'Leve suas li\u00e7\u00f5es para qualquer lugar',
      feat5_title: 'Certificado',
      feat5_desc: 'Reconhecido por empresas e universidades',
      feat6_title: 'Comunidade',
      feat6_desc: 'Grupos por idioma e n\u00edvel, desafios semanais',
      cta_p: 'Comece hoje com uma aula de teste gratuita.',
      cta_btn: 'Comece gr\u00e1tis',
    },
    zh: {
      nav_home: '\u9996\u9875',
      nav_live: '\u76f4\u64ad\u8bfe',
      nav_1to1: '1\u5bf91',
      nav_contact: '\u8054\u7cfb',
      nav_comp: '\u4f01\u4e1a\u670d\u52a1',
      nav_cta: '\u514d\u8d39\u5f00\u59cb',
      back_link: '\u2190 \u6240\u6709\u8bed\u8a00',
      toggle_group: '\u5c0f\u7ec4',
      toggle_individual: '1\u5bf91',
      toggle_starter: '\u5165\u95e8',
      label_monthly: '\u6708\u4ed8',
      label_annual: '\u5e74\u4ed8',
      label_companies: '\u4f01\u4e1a',
      note_monthly: '\u6309\u6708\u4ed8\u00b7\u65e0\u5408\u540c',
      note_annual: '\u4e00\u6b21\u6027\u5e74\u4ed8',
      note_companies: '\u9002\u5408\u56e2\u961f\u548c\u673a\u6784',
      per_month: '/\u6708',
      savings: '\u6bcf\u5e74\u8282\u7701$4,044',
      inc_live: '\u6bcf\u67084\u8282\u76f4\u64ad\u8bfe',
      inc_groups: '\u6bcf\u7ec4\u6700\u591a4\u540d\u5b66\u751f',
      inc_material: '\u542b\u6559\u6750',
      inc_platform: '\u5e73\u53f0\u8bbf\u95ee',
      inc_whatsapp: 'WhatsApp\u652f\u6301',
      inc_recorded: '24h\u5f55\u64ad\u8bfe',
      inc_invoice: '\u4f01\u4e1a\u53d1\u7968',
      inc_private: '\u79c1\u4eba\u5c0f\u7ec4',
      btn_enroll: '\u7acb\u5373\u62a5\u540d',
      btn_contact: '\u8054\u7cfb\u6211\u4eec',
      specials_title: '\u7279\u522b\u4f18\u60e0',
      badge_founder: '\u521b\u59cb\u4eba \u221230%',
      badge_friend: '\u63a8\u8350\u670b\u53cb \u221215%',
      badge_scholarship: '\u5956\u5b66\u91d1 \u221240%',
      chip_founder: '\u521b\u59cb\u4eba\u4ef7\u683c',
      chip_referral: '\u63a8\u8350\u4f18\u60e0',
      chip_scholarship: '\u5b66\u672f\u5956\u5b66\u91d1',
      chip_note_founder: '\u540d\u989d\u6709\u9650',
      chip_note_referral: '\u6bcf\u6b21\u63a8\u8350',
      chip_note_scholarship: '\u7533\u8bf7\u5236',
      ind_note: '\u6bcf\u82031\u5bf91\u8bfe\u00b7\u6bcf\u67084\u8282',
      ind_inc_1: '100%\u4e2a\u6027\u5316\u8bfe\u7a0b',
      ind_inc_2: '\u7075\u6d3b\u65f6\u95f4',
      ind_inc_3: '\u6559\u5e08\u4e13\u5c5e\u6307\u5bfc',
      ind_inc_4: '\u6839\u636e\u76ee\u6807\u5b9a\u5236\u6750\u6599',
      ind_inc_5: 'WhatsApp\u652f\u6301',
      starter_note: '\u5165\u95e8\u8ba1\u5212\u00b7\u6309\u6708\u00b7\u6bcf\u67082\u8282',
      starter_inc_1: '\u6bcf\u67082\u8282\u76f4\u64ad\u8bfe',
      starter_inc_2: '\u6bcf\u7ec4\u6700\u591a6\u540d\u5b66\u751f',
      starter_inc_3: '\u542b\u57fa\u7840\u6559\u6750',
      starter_inc_4: '\u5e73\u53f0\u8bbf\u95ee',
      starter_inc_5: 'WhatsApp\u652f\u6301',
      popular_badge: '\u2605 \u6700\u53d7\u6b22\u8fce',
      features_h2: '\u60a8\u7684\u8ba1\u5212\u5305\u542b\u4ec0\u4e48',
      feat1_title: '\u76f4\u64ad\u8bfe',
      feat1_desc: '\u7531\u8ba4\u8bc1\u6bcd\u8bed\u6559\u5e08\u6388\u8bfe',
      feat2_title: '\u5b66\u4e60\u6750\u6599',
      feat2_desc: '\u66f4\u65b0\u5185\u5bb9\uff0c\u9002\u5e94\u60a8\u7684\u6c34\u5e73',
      feat3_title: 'AI 24/7',
      feat3_desc: '\u968f\u65f6\u4e0e\u6211\u4eec\u7684AI\u5bfc\u5e08\u7ec3\u4e60',
      feat4_title: '\u79fb\u52a8\u5e94\u7528',
      feat4_desc: '\u968f\u65f6\u968f\u5730\u5b66\u4e60',
      feat5_title: '\u8bc1\u4e66',
      feat5_desc: '\u83b7\u4f01\u4e1a\u548c\u5927\u5b66\u8ba4\u53ef',
      feat6_title: '\u793e\u533a',
      feat6_desc: '\u6309\u8bed\u8a00\u548c\u7ea7\u522b\u5206\u7ec4\uff0c\u6bcf\u5468\u6311\u6218',
      cta_p: '\u4eca\u5929\u5c31\u5f00\u59cb\u514d\u8d39\u8bd5\u542c\u8bfe\u3002',
      cta_btn: '\u514d\u8d39\u5f00\u59cb',
    },
  };
"""

# ---------------------------------------------------------------------------
# Per-page PAGE_DATA
# ---------------------------------------------------------------------------

PAGE_DATA = {
    "ingles.html": {
        "en": ("English",
               "The global language of business, technology and culture",
               "Ready to learn English?"),
        "es": ("Ingl\u00e9s",
               "El idioma global de los negocios, la tecnolog\u00eda y la cultura",
               "\u00bfListo para aprender ingl\u00e9s?"),
        "fr": ("Anglais",
               "La langue mondiale des affaires, de la technologie et de la culture",
               "Pr\u00eat \u00e0 apprendre l'anglais?"),
        "de": ("Englisch",
               "Die globale Sprache der Wirtschaft, Technologie und Kultur",
               "Bereit, Englisch zu lernen?"),
        "it": ("Inglese",
               "La lingua globale degli affari, della tecnologia e della cultura",
               "Pronto a imparare l'inglese?"),
        "pt": ("Ingl\u00eas",
               "O idioma global dos neg\u00f3cios, da tecnologia e da cultura",
               "Pronto para aprender ingl\u00eas?"),
        "zh": ("\u82f1\u8bed",
               "\u5546\u4e1a\u3001\u6280\u672f\u548c\u6587\u5316\u7684\u5168\u7403\u8bed\u8a00",
               "\u51c6\u5907\u597d\u5b66\u4e60\u82f1\u8bed\u4e86\u5417\uff1f"),
        "default": "es",
    },
    "espanol.html": {
        "en": ("Spanish",
               "The second most spoken language in the world, key for Latin America and Spain",
               "Ready to learn Spanish?"),
        "es": ("Espa\u00f1ol",
               "La segunda lengua m\u00e1s hablada del mundo, clave para Am\u00e9rica y Espa\u00f1a",
               "\u00bfListo para aprender espa\u00f1ol?"),
        "fr": ("Espagnol",
               "La deuxi\u00e8me langue la plus parl\u00e9e au monde, essentielle pour l'Am\u00e9rique Latine et l'Espagne",
               "Pr\u00eat \u00e0 apprendre l'espagnol?"),
        "de": ("Spanisch",
               "Die zweith\u00e4ufigste Sprache der Welt, wichtig f\u00fcr Lateinamerika und Spanien",
               "Bereit, Spanisch zu lernen?"),
        "it": ("Spagnolo",
               "La seconda lingua pi\u00f9 parlata al mondo, chiave per l'America Latina e la Spagna",
               "Pronto a imparare lo spagnolo?"),
        "pt": ("Espanhol",
               "O segundo idioma mais falado no mundo, essencial para a Am\u00e9rica Latina e a Espanha",
               "Pronto para aprender espanhol?"),
        "zh": ("\u897f\u73ed\u7259\u8bed",
               "\u4e16\u754c\u7b2c\u4e8c\u5927\u8bed\u8a00\uff0c\u5bf9\u62c9\u4e01\u7f8e\u6d32\u548c\u897f\u73ed\u7259\u81f3\u5173\u91cd\u8981",
               "\u51c6\u5907\u597d\u5b66\u4e60\u897f\u73ed\u7259\u8bed\u4e86\u5417\uff1f"),
        "default": "es",
    },
    "frances.html": {
        "en": ("French",
               "The language of culture, diplomacy and romance",
               "Ready to learn French?"),
        "es": ("Franc\u00e9s",
               "El idioma de la cultura, la diplomacia y el romance",
               "\u00bfListo para aprender franc\u00e9s?"),
        "fr": ("Fran\u00e7ais",
               "La langue de la culture, de la diplomatie et du romantisme",
               "Pr\u00eat \u00e0 apprendre le fran\u00e7ais?"),
        "de": ("Franz\u00f6sisch",
               "Die Sprache der Kultur, Diplomatie und Romantik",
               "Bereit, Franz\u00f6sisch zu lernen?"),
        "it": ("Francese",
               "La lingua della cultura, della diplomazia e del romanticismo",
               "Pronto a imparare il francese?"),
        "pt": ("Franc\u00eas",
               "O idioma da cultura, da diplomacia e do romantismo",
               "Pronto para aprender franc\u00eas?"),
        "zh": ("\u6cd5\u8bed",
               "\u6587\u5316\u3001\u5916\u4ea4\u548c\u6d6a\u6f2b\u7684\u8bed\u8a00",
               "\u51c6\u5907\u597d\u5b66\u4e60\u6cd5\u8bed\u4e86\u5417\uff1f"),
        "default": "es",
    },
    "aleman.html": {
        "en": ("German",
               "The language of engineering, philosophy and Europe's largest economy",
               "Ready to learn German?"),
        "es": ("Alem\u00e1n",
               "El idioma de la ingenier\u00eda, la filosof\u00eda y la mayor econom\u00eda de Europa",
               "\u00bfListo para aprender alem\u00e1n?"),
        "fr": ("Allemand",
               "La langue de l'ing\u00e9nierie, de la philosophie et de la plus grande \u00e9conomie d'Europe",
               "Pr\u00eat \u00e0 apprendre l'allemand?"),
        "de": ("Deutsch",
               "Die Sprache der Technik, Philosophie und der gr\u00f6\u00dften Wirtschaft Europas",
               "Bereit, Deutsch zu lernen?"),
        "it": ("Tedesco",
               "La lingua dell'ingegneria, della filosofia e della pi\u00f9 grande economia d'Europa",
               "Pronto a imparare il tedesco?"),
        "pt": ("Alem\u00e3o",
               "O idioma da engenharia, da filosofia e da maior economia da Europa",
               "Pronto para aprender alem\u00e3o?"),
        "zh": ("\u5fb7\u8bed",
               "\u5de5\u7a0b\u3001\u54f2\u5b66\u548c\u6b27\u6d32\u6700\u5927\u7ecf\u6d4e\u4f53\u7684\u8bed\u8a00",
               "\u51c6\u5907\u597d\u5b66\u4e60\u5fb7\u8bed\u4e86\u5417\uff1f"),
        "default": "es",
    },
    "italiano.html": {
        "en": ("Italian",
               "The language of art, gastronomy and la dolce vita",
               "Ready to learn Italian?"),
        "es": ("Italiano",
               "El idioma del arte, la gastronom\u00eda y la dolce vita",
               "\u00bfListo para aprender italiano?"),
        "fr": ("Italien",
               "La langue de l'art, de la gastronomie et de la dolce vita",
               "Pr\u00eat \u00e0 apprendre l'italien?"),
        "de": ("Italienisch",
               "Die Sprache der Kunst, Gastronomie und Dolce Vita",
               "Bereit, Italienisch zu lernen?"),
        "it": ("Italiano",
               "La lingua dell'arte, della gastronomia e della dolce vita",
               "Pronto a imparare l'italiano?"),
        "pt": ("Italiano",
               "O idioma da arte, da gastronomia e da dolce vita",
               "Pronto para aprender italiano?"),
        "zh": ("\u610f\u5927\u5229\u8bed",
               "\u827a\u672f\u3001\u7f8e\u98df\u548c\u751c\u8983\u751f\u6d3b\u7684\u8bed\u8a00",
               "\u51c6\u5907\u597d\u5b66\u4e60\u610f\u5927\u5229\u8bed\u4e86\u5417\uff1f"),
        "default": "es",
    },
    "portugues.html": {
        "en": ("Portuguese",
               "The language of Brazil, Portugal and a growing global community",
               "Ready to learn Portuguese?"),
        "es": ("Portugu\u00e9s",
               "El idioma de Brasil, Portugal y una creciente comunidad global",
               "\u00bfListo para aprender portugu\u00e9s?"),
        "fr": ("Portugais",
               "La langue du Br\u00e9sil, du Portugal et d'une communaut\u00e9 mondiale en pleine croissance",
               "Pr\u00eat \u00e0 apprendre le portugais?"),
        "de": ("Portugiesisch",
               "Die Sprache Brasiliens, Portugals und einer wachsenden globalen Gemeinschaft",
               "Bereit, Portugiesisch zu lernen?"),
        "it": ("Portoghese",
               "La lingua del Brasile, del Portogallo e di una comunit\u00e0 globale in crescita",
               "Pronto a imparare il portoghese?"),
        "pt": ("Portugu\u00eas",
               "O idioma do Brasil, de Portugal e de uma crescente comunidade global",
               "Pronto para aprender portugu\u00eas?"),
        "zh": ("\u8461\u8404\u7259\u8bed",
               "\u5df4\u897f\u3001\u8461\u8404\u7259\u548c\u4e0d\u65ad\u589e\u957f\u7684\u5168\u7403\u793e\u533a\u7684\u8bed\u8a00",
               "\u51c6\u5907\u597d\u5b66\u4e60\u8461\u8404\u7259\u8bed\u4e86\u5417\uff1f"),
        "default": "es",
    },
    "chino.html": {
        "en": ("Chinese",
               "The most spoken language in the world and the key to one of the largest economies",
               "Ready to learn Chinese?"),
        "es": ("Chino",
               "El idioma m\u00e1s hablado del mundo y clave para una de las mayores econom\u00edas",
               "\u00bfListo para aprender chino?"),
        "fr": ("Chinois",
               "La langue la plus parl\u00e9e au monde et la cl\u00e9 de l'une des plus grandes \u00e9conomies",
               "Pr\u00eat \u00e0 apprendre le chinois?"),
        "de": ("Chinesisch",
               "Die meistgesprochene Sprache der Welt und der Schl\u00fcssel zu einer der gr\u00f6\u00dften Volkswirtschaften",
               "Bereit, Chinesisch zu lernen?"),
        "it": ("Cinese",
               "La lingua pi\u00f9 parlata al mondo e la chiave per una delle maggiori economie",
               "Pronto a imparare il cinese?"),
        "pt": ("Chin\u00eas",
               "O idioma mais falado no mundo e chave para uma das maiores economias",
               "Pronto para aprender chin\u00eas?"),
        "zh": ("\u4e2d\u6587",
               "\u4e16\u754c\u4e0a\u4f7f\u7528\u4eba\u6570\u6700\u591a\u7684\u8bed\u8a00\uff0c\u4e5f\u662f\u901a\u5f80\u6700\u5927\u7ecf\u6d4e\u4f53\u4e4b\u4e00\u7684\u9470\u5319",
               "\u51c6\u5907\u597d\u5b66\u4e60\u4e2d\u6587\u4e86\u5417\uff1f"),
        "default": "es",
    },
}

# ---------------------------------------------------------------------------
# Build PAGE_DATA JS for a given page
# ---------------------------------------------------------------------------

def build_page_data_js(page_file):
    data = PAGE_DATA[page_file]
    langs = ["en", "es", "fr", "de", "it", "pt", "zh"]
    lines = ["  const PAGE_DATA = {"]
    for lang in langs:
        h1, p, cta_h2 = data[lang]
        # JSON-encode each string to handle quotes and special chars safely
        import json
        lines.append(f"    {lang}: {{")
        lines.append(f"      h1: {json.dumps(h1)},")
        lines.append(f"      p: {json.dumps(p)},")
        lines.append(f"      cta_h2: {json.dumps(cta_h2)},")
        lines.append("    },")
    lines.append("  };")
    return "\n".join(lines)

# ---------------------------------------------------------------------------
# The applyLang + lang-picker + on-load JS (constant)
# ---------------------------------------------------------------------------

APPLY_LANG_AND_HANDLERS_JS = r"""
  function applyLang(lang) {
    const t = LANGS[lang];
    const p = PAGE_DATA[lang];
    if (!t || !p) return;

    // Nav links (4 links after .nav-lang-menu in .nav-links)
    const navLinks = document.querySelectorAll('.nav-links > a');
    if (navLinks[0]) navLinks[0].textContent = t.nav_home;
    if (navLinks[1]) navLinks[1].textContent = t.nav_live;
    if (navLinks[2]) navLinks[2].textContent = t.nav_1to1;
    if (navLinks[3]) navLinks[3].textContent = t.nav_contact;

    // Nav CTA
    const navCta = document.querySelector('.nav-cta');
    if (navCta) navCta.textContent = t.nav_cta;

    // Back link
    const backLink = document.querySelector('.back-link');
    if (backLink) backLink.textContent = t.back_link;

    // Toggle buttons
    const toggleBtns = document.querySelectorAll('.toggle-btn');
    if (toggleBtns[0]) toggleBtns[0].textContent = t.toggle_group;
    if (toggleBtns[1]) toggleBtns[1].textContent = t.toggle_individual;
    if (toggleBtns[2]) toggleBtns[2].textContent = t.toggle_starter;

    // Hero
    const heroH1 = document.querySelector('.hero h1');
    if (heroH1) heroH1.textContent = p.h1;
    const heroP = document.querySelector('.hero p');
    if (heroP) heroP.textContent = p.p;

    // Card labels
    const labels = document.querySelectorAll('.card-label');
    if (labels[0]) labels[0].textContent = t.label_monthly;
    if (labels[1]) labels[1].textContent = t.label_annual;
    if (labels[2]) labels[2].textContent = t.label_companies;

    // Card notes
    const notes = document.querySelectorAll('.card-note');
    if (notes[0]) notes[0].textContent = t.note_monthly;
    if (notes[1]) notes[1].textContent = t.note_annual;
    if (notes[2]) notes[2].textContent = t.note_companies;

    // Per-month spans inside #group .card-price
    document.querySelectorAll('#group .card-price span').forEach(function(s) {
      s.textContent = t.per_month;
    });

    // Savings
    const savings = document.querySelector('.card-savings');
    if (savings) savings.textContent = t.savings;

    // Popular badge
    const popular = document.querySelector('.badge-popular');
    if (popular) popular.textContent = t.popular_badge;

    // Group cards includes
    const groupCards = document.querySelectorAll('#group .price-card');
    const groupIncludes = [
      [t.inc_live, t.inc_groups, t.inc_material, t.inc_platform, t.inc_whatsapp],
      [t.inc_live, t.inc_groups, t.inc_material, t.inc_platform, t.inc_whatsapp, t.inc_recorded],
      [t.inc_live, t.inc_groups, t.inc_material, t.inc_platform, t.inc_whatsapp, t.inc_invoice, t.inc_private]
    ];
    groupCards.forEach(function(card, ci) {
      const items = card.querySelectorAll('.includes li');
      (groupIncludes[ci] || []).forEach(function(txt, ii) {
        if (items[ii]) items[ii].textContent = txt;
      });
      const btn = card.querySelector('.card-btn');
      if (btn) btn.textContent = ci === 2 ? t.btn_contact : t.btn_enroll;
    });

    // Specials
    const specTitle = document.querySelector('.specials-title');
    if (specTitle) specTitle.textContent = t.specials_title;
    const badges = document.querySelectorAll('.chip-badge');
    if (badges[0]) badges[0].textContent = t.badge_founder;
    if (badges[1]) badges[1].textContent = t.badge_friend;
    if (badges[2]) badges[2].textContent = t.badge_scholarship;
    const chipNames = document.querySelectorAll('.chip-name');
    if (chipNames[0]) chipNames[0].textContent = t.chip_founder;
    if (chipNames[1]) chipNames[1].textContent = t.chip_referral;
    if (chipNames[2]) chipNames[2].textContent = t.chip_scholarship;
    const chipNotes = document.querySelectorAll('.chip-note');
    if (chipNotes[0]) chipNotes[0].textContent = t.chip_note_founder;
    if (chipNotes[1]) chipNotes[1].textContent = t.chip_note_referral;
    if (chipNotes[2]) chipNotes[2].textContent = t.chip_note_scholarship;
    document.querySelectorAll('.chip-price span').forEach(function(s) {
      s.textContent = t.per_month;
    });

    // Individual section
    const indNote = document.querySelector('#individual .ind-note');
    if (indNote) indNote.textContent = t.ind_note;
    const indIncludes = [t.ind_inc_1, t.ind_inc_2, t.ind_inc_3, t.ind_inc_4, t.ind_inc_5];
    const indItems = document.querySelectorAll('#individual .ind-includes li');
    indIncludes.forEach(function(txt, i) { if (indItems[i]) indItems[i].textContent = txt; });
    const indBtn = document.querySelector('#individual .ind-btn');
    if (indBtn) indBtn.textContent = t.btn_enroll;

    // Starter section
    const starterNote = document.querySelector('#starter .ind-note');
    if (starterNote) starterNote.textContent = t.starter_note;
    const starterIncludes = [t.starter_inc_1, t.starter_inc_2, t.starter_inc_3, t.starter_inc_4, t.starter_inc_5];
    const starterItems = document.querySelectorAll('#starter .ind-includes li');
    starterIncludes.forEach(function(txt, i) { if (starterItems[i]) starterItems[i].textContent = txt; });
    const starterBtn = document.querySelector('#starter .ind-btn');
    if (starterBtn) starterBtn.textContent = t.btn_enroll;

    // Features section
    const featH2 = document.querySelector('.features h2');
    if (featH2) featH2.textContent = t.features_h2;
    const featTitles = document.querySelectorAll('.feat-title');
    const featDescs = document.querySelectorAll('.feat-desc');
    const feats = [
      [t.feat1_title, t.feat1_desc], [t.feat2_title, t.feat2_desc],
      [t.feat3_title, t.feat3_desc], [t.feat4_title, t.feat4_desc],
      [t.feat5_title, t.feat5_desc], [t.feat6_title, t.feat6_desc]
    ];
    feats.forEach(function(pair, i) {
      if (featTitles[i]) featTitles[i].textContent = pair[0];
      if (featDescs[i]) featDescs[i].textContent = pair[1];
    });

    // CTA banner
    const ctaH2 = document.querySelector('.cta-banner h2');
    if (ctaH2) ctaH2.textContent = p.cta_h2;
    const ctaP = document.querySelector('.cta-banner p');
    if (ctaP) ctaP.textContent = t.cta_p;
    const ctaBtn = document.querySelector('.cta-banner .btn-white');
    if (ctaBtn) ctaBtn.textContent = t.cta_btn;

    // Update lang picker button display
    const flags = {en:'🇬🇧',es:'🇪🇸',fr:'🇫🇷',de:'🇩🇪',it:'🇮🇹',pt:'🇧🇷',zh:'🇨🇳'};
    const codes = {en:'EN',es:'ES',fr:'FR',de:'DE',it:'IT',pt:'PT',zh:'ZH'};
    const langBtnEl = document.getElementById('langBtn');
    if (langBtnEl) {
      const spans = langBtnEl.querySelectorAll('span');
      if (spans[0]) spans[0].textContent = flags[lang] || '';
      if (spans[1]) spans[1].textContent = codes[lang] || lang.toUpperCase();
    }

    // Mark active lang-option
    const pageForLang = {en:'ingles.html',es:'espanol.html',fr:'frances.html',de:'aleman.html',it:'italiano.html',pt:'portugues.html',zh:'chino.html'};
    document.querySelectorAll('.lang-option').forEach(function(o) {
      o.classList.toggle('active', o.getAttribute('href') === pageForLang[lang]);
    });

    localStorage.setItem('parling_lang', lang);
  }

  // Toggle panels
  const panels = [document.getElementById('group'), document.getElementById('individual'), document.getElementById('starter')];
  const toggleBtnsEl = document.querySelectorAll('.toggle-btn');
  toggleBtnsEl.forEach(function(btn, idx) {
    btn.addEventListener('click', function() {
      panels.forEach(function(p) { p.classList.add('hidden'); });
      toggleBtnsEl.forEach(function(b) { b.classList.remove('active'); });
      panels[idx].classList.remove('hidden');
      btn.classList.add('active');
    });
  });

  // Lang-picker open/close
  document.getElementById('langBtn').addEventListener('click', function(e) {
    e.stopPropagation();
    document.getElementById('langPicker').classList.toggle('open');
  });
  document.addEventListener('click', function() {
    document.getElementById('langPicker').classList.remove('open');
  });

  // Lang-option click handlers — translate in-place instead of navigating
  const langMap = {
    'ingles.html':'en','espanol.html':'es','frances.html':'fr',
    'aleman.html':'de','italiano.html':'it','portugues.html':'pt','chino.html':'zh'
  };
  document.querySelectorAll('.lang-option').forEach(function(opt) {
    opt.addEventListener('click', function(e) {
      e.preventDefault();
      const lang = langMap[this.getAttribute('href')];
      if (lang) {
        applyLang(lang);
        document.getElementById('langPicker').classList.remove('open');
      }
    });
  });

  // On load: apply saved lang or page default
  (function() {
    const saved = localStorage.getItem('parling_lang');
    if (saved && LANGS[saved]) {
      applyLang(saved);
    }
  })();
"""

# ---------------------------------------------------------------------------
# Pattern to strip the old toggle + lang-picker script block(s)
# We'll remove ALL <script> blocks before </body> and re-add only the new one.
# ---------------------------------------------------------------------------

def process_file(filename):
    path = os.path.join(BASE, filename)
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # Remove every <script>…</script> block that appears before </body>
    # (these are the inline scripts added previously; we will add a single new one)
    html_no_scripts = re.sub(
        r'<script>[\s\S]*?</script>',
        '',
        html
    )

    # Build the new combined script block
    page_data_js = build_page_data_js(filename)
    new_script = (
        "<script>\n"
        + LANGS_JS
        + "\n"
        + page_data_js
        + "\n"
        + APPLY_LANG_AND_HANDLERS_JS
        + "</script>"
    )

    # Insert before </body>
    if "</body>" in html_no_scripts:
        html_final = html_no_scripts.replace("</body>", new_script + "\n</body>")
    else:
        html_final = html_no_scripts + "\n" + new_script

    with open(path, "w", encoding="utf-8") as f:
        f.write(html_final)

    print(f"  [OK] {filename}")

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    files = [
        "ingles.html", "espanol.html", "frances.html",
        "aleman.html", "italiano.html", "portugues.html", "chino.html",
    ]
    print("Injecting i18n into Parling Academy subpages...")
    for fname in files:
        process_file(fname)
    print("\nDone. All 7 pages updated.")
