/*
 * Gallery map locations
 * ---------------------
 * Add a Gallery location by copying one object and changing three values:
 *
 *   {
 *     region: "japan",                 // japan | china | australia | europe
 *     admin: "JP-13",                  // ISO 3166-2 code
 *     photos: ["2026-08-14-example"]   // image filename without .webp
 *   }
 *
 * On the China and Japan maps, the marker is placed automatically at the
 * administrative area's label centre. Australia and Germany use the same
 * records to count photos and open their shortcut buttons. The matching
 * photograph must also exist as a Gallery card in gallery.qmd. Multiple
 * photographs from the same administrative area can share one object.
 */
window.GALLERY_MAP_PLACES = [
  // China: ISO 3166-2 administrative order.
  { region: "china", admin: "CN-CQ", photos: ["2024-04-30-chongqing-yangtze-river"] },
  { region: "china", admin: "CN-GD", photos: ["2025-06-08-canton-tower", "2025-06-05-shantou"] },
  { region: "china", admin: "CN-GS", photos: ["2026-07-08-gansu"] },
  { region: "china", admin: "CN-HE", photos: ["2023-08-08-qinhuangdao"] },
  { region: "china", admin: "CN-JS", photos: ["2026-02-26-nanjing-museum"] },
  { region: "china", admin: "CN-NM", photos: ["2023-08-15-chifeng"] },
  { region: "china", admin: "CN-QH", photos: ["2026-07-06-qinghai"] },
  { region: "china", admin: "CN-SD", photos: ["2026-07-10-jinan-pearl-spring"] },
  { region: "china", admin: "CN-SH", photos: ["2025-02-22-shanghai-jiao-tong-minhang"] },
  { region: "china", admin: "CN-SX", photos: ["2025-03-01-taiyuan-ancient-county-town"] },
  { region: "china", admin: "CN-TJ", photos: ["2025-03-15-tianjin-century-clock"] },
  { region: "china", admin: "CN-ZJ", photos: ["2025-02-24-hangzhou-west-lake"] },

  // Japan: prefecture code, then place name; dates only break ties.
  { region: "japan", admin: "JP-01", photos: ["2026-02-02-otaru", "2023-01-06-noboribetsu", "2024-01-29-shiretoko"] },
  { region: "japan", admin: "JP-13", photos: ["2024-01-27-tokyo"] },
  { region: "japan", admin: "JP-18", photos: ["2025-09-15-wakasa"] },
  { region: "japan", admin: "JP-20", photos: ["2023-11-02-lake-tateshina", "2026-01-07-tateishi-park", "2023-11-02-tateishi-park"] },
  { region: "japan", admin: "JP-24", photos: ["2026-06-07-shima"] },
  { region: "japan", admin: "JP-25", photos: ["2024-07-27-otsu"] },
  { region: "japan", admin: "JP-26", photos: ["2024-06-08-amanohashidate", "2022-10-25-kyoto-university-uji-campus", "2022-11-05-nanzenji"] },
  { region: "japan", admin: "JP-27", photos: ["2025-11-16-kawachinagano"] },
  { region: "japan", admin: "JP-28", photos: ["2024-10-24-kobe"] },
  { region: "japan", admin: "JP-29", photos: ["2022-10-23-odaigahara"] },
  { region: "japan", admin: "JP-34", photos: ["2022-08-25-hiroshima", "2022-08-23-miyajima"] },
  { region: "japan", admin: "JP-47", photos: ["2025-08-12-ishigaki-blue-cave", "2025-08-08-ishigaki"] },

  // Regions represented by shortcut buttons below the two maps.
  { region: "australia", admin: "AU-QLD", photos: ["2023-07-16-cairns", "2024-07-20-fitzroy-island"] },
  { region: "europe", admin: "DE-BY", photos: ["2025-12-14-munich", "2025-12-18-kreuth"] }
];
