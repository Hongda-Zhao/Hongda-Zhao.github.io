(() => {
  const locations = (Array.isArray(window.GALLERY_MAP_PLACES)
    ? window.GALLERY_MAP_PLACES
    : [])
    .map((location) => ({
      admin: typeof location.admin === "string" ? location.admin : "",
      photos: Array.isArray(location.photos) ? location.photos.filter((photo) => typeof photo === "string") : [],
      region: typeof location.region === "string" ? location.region : ""
    }))
    .filter((location) => (
      location.region
      && location.admin
      && location.photos.length > 0
    ));

  const regionSettings = {
    japan: {
      bounds: [[23, 122], [45.5, 146.5]],
      maxBounds: [[19, 117], [49, 151]],
      maxInitialZoom: 5,
      terrain: { bounds: [[0, 60], [70, 180]], url: "assets/map/terrain/asia-natural-earth.jpg" }
    },
    china: {
      bounds: [[34.5, 94], [44.5, 123]],
      maxBounds: [[29, 88], [49, 128]],
      maxInitialZoom: 5,
      terrain: { bounds: [[0, 60], [70, 180]], url: "assets/map/terrain/asia-natural-earth.jpg" }
    },
    australia: {
      bounds: [[-24, 137], [-10, 154]],
      maxBounds: [[-31, 131], [-5, 160]],
      maxInitialZoom: 6,
      terrain: { bounds: [[-60, 90], [10, 180]], url: "assets/map/terrain/oceania-natural-earth.jpg" }
    },
    europe: {
      bounds: [[46.5, 9.5], [49.3, 13.5]],
      maxBounds: [[45.5, 8], [50, 15]],
      maxInitialZoom: 8,
      terrain: { bounds: [[30, -15], [72, 45]], url: "assets/map/terrain/europe-natural-earth.jpg" }
    }
  };

  const primaryAdminLabels = {
    japan: new Set(["JP-01", "JP-13", "JP-20", "JP-26", "JP-34", "JP-47"]),
    china: new Set(["CN-GS", "CN-QH", "CN-NM", "CN-HE"]),
    australia: new Set(["AU-QLD"]),
    europe: new Set(["DE-BY"])
  };

  const adminLabelOffsets = {
    "JP-01": [34, -10],
    "JP-13": [30, 13],
    "JP-20": [20, -28],
    "JP-26": [-51, -26],
    "JP-34": [-60, 38],
    "JP-47": [0, 18],
    "CN-GS": [0, -24],
    "CN-NM": [-38, -18],
    "CN-HE": [0, 20],
    "DE-BY": [-8, -18]
  };

  const copy = {
    en: {
      go: "Go to photograph:",
      cluster: "photographs. Select to reveal individual photograph markers.",
      unavailable: "This regional map could not be drawn. Browse the photographs below."
    },
    zh: {
      go: "前往照片：",
      cluster: "张照片。点击后展开单张照片标记。",
      unavailable: "这幅区域地图暂时无法显示，请在下方浏览照片。"
    }
  };

  const initialiseMaps = () => {
    const mapElements = Array.from(document.querySelectorAll("[data-gallery-region]"));
    if (mapElements.length === 0) return;

    const currentLanguage = () => (
      document.documentElement.dataset.uiLang === "zh" ? "zh" : "en"
    );
    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    const formatPhotoCount = (count) => {
      if (currentLanguage() === "zh") return `${count} 张照片`;
      return `${count} photograph${count === 1 ? "" : "s"}`;
    };

    const adminNameOverrides = {
      zh: {
        "DE-BY": "巴伐利亚州",
        "JP-13": "东京都"
      }
    };

    const getAdminName = (properties) => {
      const override = adminNameOverrides[currentLanguage()]?.[properties.iso_3166_2];
      if (override) return override;
      if (currentLanguage() === "zh") {
        return properties.name_zh || properties.name_en || properties.name || "";
      }
      if (properties.iso_3166_2?.startsWith("JP-")) {
        return properties.name || properties.name_en || "";
      }
      return properties.name_en || properties.name || "";
    };

    const captionAdminNameOverrides = {
      "JP-01": "Hokkaido",
      "JP-13": "Tokyo",
      "JP-18": "Fukui Prefecture",
      "JP-20": "Nagano Prefecture",
      "JP-24": "Mie Prefecture",
      "JP-25": "Shiga Prefecture",
      "JP-26": "Kyoto Prefecture",
      "JP-27": "Osaka Prefecture",
      "JP-28": "Hyogo Prefecture",
      "JP-29": "Nara Prefecture",
      "JP-34": "Hiroshima Prefecture",
      "JP-47": "Okinawa Prefecture"
    };

    const getCaptionAdminName = (properties) => {
      if (currentLanguage() === "zh") return getAdminName(properties);
      return captionAdminNameOverrides[properties.iso_3166_2]
        || properties.name_en
        || properties.name
        || "";
    };

    const countryNames = {
      australia: { en: "Australia", zh: "澳大利亚" },
      china: { en: "China", zh: "中国" },
      europe: { en: "Germany", zh: "德国" },
      japan: { en: "Japan", zh: "日本" }
    };

    const getCountryName = (region) => (
      countryNames[region]?.[currentLanguage()] || region
    );

    const setUnavailable = (mapElement) => {
      mapElement.classList.add("is-unavailable");
      const message = mapElement.querySelector(".gallery-map-loading");
      if (message) message.textContent = copy[currentLanguage()].unavailable;
    };

    const photoTriggers = new Map(
      Array.from(document.querySelectorAll(".gallery-lightbox")).map((trigger) => {
        const filename = decodeURIComponent(trigger.getAttribute("href") || "")
          .split("/")
          .pop()
          .replace(/\.webp$/i, "");
        return [filename, trigger];
      })
    );

    photoTriggers.forEach((trigger, photoId) => {
      const figure = trigger.closest(".gallery-item");
      const caption = figure?.querySelector(".gallery-caption");
      if (!figure) return;
      figure.id = `gallery-photo-${photoId}`;
      if (caption) {
        caption.id = `gallery-caption-${photoId}`;
        trigger.setAttribute("aria-describedby", caption.id);
      }
    });

    const goToPhoto = (photoId, updateHistory = true) => {
      const trigger = photoTriggers.get(photoId);
      const figure = trigger?.closest(".gallery-item");
      if (!trigger || !figure) return;

      document.querySelectorAll(".gallery-item.is-map-target").forEach((item) => {
        item.classList.remove("is-map-target");
      });
      figure.classList.add("is-map-target");

      if (updateHistory) {
        try {
          window.history.replaceState(null, "", `#${figure.id}`);
        } catch (_error) {
          // file:// previews may not allow History API updates.
        }
      }

      const distance = Math.abs(figure.getBoundingClientRect().top);
      const smooth = !reducedMotion && distance < window.innerHeight * 1.5;
      trigger.focus({ preventScroll: true });
      figure.scrollIntoView({
        behavior: smooth ? "smooth" : "auto",
        block: "start"
      });
    };

    const photoIdsByRegion = new Map();
    const regionByPhoto = new Map();
    locations.forEach((location) => {
      if (!photoIdsByRegion.has(location.region)) {
        photoIdsByRegion.set(location.region, new Set());
      }
      location.photos.forEach((photoId) => {
        if (!photoTriggers.has(photoId)) return;
        photoIdsByRegion.get(location.region).add(photoId);
        if (!regionByPhoto.has(photoId)) regionByPhoto.set(photoId, location.region);
      });
    });
    const regionPhotoCounts = new Map(
      Array.from(photoIdsByRegion, ([region, photoIds]) => [region, photoIds.size])
    );
    const firstPhotoIdByRegion = new Map();
    photoTriggers.forEach((_trigger, photoId) => {
      const region = regionByPhoto.get(photoId);
      if (region && !firstPhotoIdByRegion.has(region)) {
        firstPhotoIdByRegion.set(region, photoId);
      }
    });

    const updateRegionShortcuts = () => {
      const language = currentLanguage();
      document.querySelectorAll("[data-gallery-region-count]").forEach((regionCount) => {
        const count = regionPhotoCounts.get(regionCount.dataset.galleryRegionCount) || 0;
        regionCount.textContent = formatPhotoCount(count);
      });
      document.querySelectorAll("[data-gallery-open-region]").forEach((button) => {
        const regionName = button.querySelector(".gallery-region-shortcut-name")?.textContent.trim() || "";
        const count = regionPhotoCounts.get(button.dataset.galleryOpenRegion) || 0;
        button.setAttribute(
          "aria-label",
          language === "zh"
            ? `前往${regionName}的第一张照片（共 ${count} 张）`
            : `Go to the first photograph from ${regionName} (${formatPhotoCount(count)})`
        );
      });
    };

    document.querySelectorAll("[data-gallery-open-region]").forEach((button) => {
      const photoId = firstPhotoIdByRegion.get(button.dataset.galleryOpenRegion);
      if (!photoId) {
        button.disabled = true;
        return;
      }
      button.addEventListener("click", () => goToPhoto(photoId));
    });
    updateRegionShortcuts();
    const shortcutLanguageObserver = new MutationObserver(updateRegionShortcuts);
    shortcutLanguageObserver.observe(document.documentElement, {
      attributeFilter: ["data-ui-lang"],
      attributes: true
    });

    if (!window.GALLERY_ADMIN1) {
      mapElements.forEach(setUnavailable);
      return;
    }

    const adminFeatures = new Map(
      Object.entries(window.GALLERY_ADMIN1).map(([region, collection]) => [
        region,
        new Map((collection.features || []).map((feature) => [feature.properties.iso_3166_2, feature]))
      ])
    );

    const usableLocations = locations
      .map((location) => {
        const adminFeature = adminFeatures.get(location.region)?.get(location.admin);
        const lat = Number(adminFeature?.properties.latitude);
        const lng = Number(adminFeature?.properties.longitude);
        return {
          ...location,
          adminProperties: adminFeature?.properties,
          lat,
          lng,
          photos: location.photos.filter((photoId) => photoTriggers.has(photoId))
        };
      })
      .filter((location) => (
        location.photos.length > 0
        && Number.isFinite(location.lat)
        && Number.isFinite(location.lng)
      ));

    if (usableLocations.length === 0) {
      mapElements.forEach(setUnavailable);
      return;
    }

    const coarsePointer = window.matchMedia("(pointer: coarse)").matches;
    const mapRecords = [];
    const markerRecords = [];

    const getPhotoMeta = (photoId) => {
      const trigger = photoTriggers.get(photoId);
      const figure = trigger?.closest(".gallery-item");
      return {
        date: figure?.querySelector("time")?.textContent.trim() || "",
        place: figure?.querySelector("[data-i18n^='gallery.place.']")?.textContent.trim() || ""
      };
    };

    const getPhotoLabel = (record) => {
      const meta = getPhotoMeta(record.photoId);
      return [
        meta.date,
        getCountryName(record.region),
        getCaptionAdminName(record.adminProperties),
        meta.place
      ].filter(Boolean).join(" · ");
    };

    const photoRecords = usableLocations.flatMap((location) => (
      location.photos.map((photoId) => ({
        adminProperties: location.adminProperties,
        photoId,
        region: location.region
      }))
    ));

    const makeCaptionSeparator = () => {
      const separator = document.createElement("span");
      separator.setAttribute("aria-hidden", "true");
      separator.textContent = "·";
      return separator;
    };

    const updatePhotoCaption = (record) => {
      const trigger = photoTriggers.get(record.photoId);
      const figure = trigger?.closest(".gallery-item");
      const caption = figure?.querySelector(".gallery-caption");
      const time = caption?.querySelector("time");
      const place = caption?.querySelector("[data-i18n^='gallery.place.']");
      if (!figure || !caption || !time || !place) return;

      let country = caption.querySelector(".gallery-caption-country");
      let admin = caption.querySelector(".gallery-caption-admin");
      if (!country || !admin) {
        country = document.createElement("span");
        country.className = "gallery-caption-country";
        admin = document.createElement("span");
        admin.className = "gallery-caption-admin";
        caption.replaceChildren(
          time,
          makeCaptionSeparator(),
          country,
          makeCaptionSeparator(),
          admin,
          makeCaptionSeparator(),
          place
        );
      }

      country.textContent = getCountryName(record.region);
      admin.textContent = getCaptionAdminName(record.adminProperties);
    };

    const updatePhotoCaptions = () => photoRecords.forEach(updatePhotoCaption);
    updatePhotoCaptions();

    if (
      !window.L
      || !window.L.markerClusterGroup
      || !window.GALLERY_WORLD_LAND
      || !window.GALLERY_WORLD_COUNTRIES
    ) {
      mapElements.forEach(setUnavailable);
      return;
    }

    const makeTooltip = (record) => {
      const wrapper = document.createElement("span");
      const label = document.createElement("strong");
      label.textContent = getPhotoLabel(record);
      wrapper.append(label);
      return wrapper;
    };

    const updateMarkerLanguage = (record) => {
      const language = currentLanguage();
      const photoLabel = getPhotoLabel(record);
      const label = `${copy[language].go}${language === "zh" ? "" : " "}${photoLabel}`;
      record.marker.setTooltipContent(makeTooltip(record));
      const element = record.marker.getElement();
      if (element) {
        element.setAttribute("aria-label", label);
        element.setAttribute("role", "button");
        element.setAttribute("title", label);
      }
    };

    const updateClusterLabels = (record) => {
      const language = currentLanguage();
      const regionName = record.mapElement
        .closest(".gallery-region")
        ?.querySelector(".gallery-region-header h2")
        ?.textContent.trim() || "";
      record.mapElement.querySelectorAll(".gallery-map-cluster-shell").forEach((cluster) => {
        const count = cluster.querySelector(".gallery-map-cluster-count")?.textContent.trim() || "";
        const label = `${regionName}${language === "zh" ? "：" : ": "}${count}${language === "zh" ? "" : " "}${copy[language].cluster}`;
        cluster.setAttribute("aria-label", label);
        cluster.setAttribute("role", "button");
        cluster.setAttribute("title", label);
        if (!cluster.dataset.galleryKeyboardReady) {
          cluster.dataset.galleryKeyboardReady = "true";
          cluster.addEventListener("keydown", (event) => {
            if (event.key === " ") {
              event.preventDefault();
              cluster.click();
            }
          });
        }
      });
    };

    const drawRegionalBase = (map, mapElement, settings, bounds) => {
      const mapStyles = window.getComputedStyle(mapElement);
      const landColor = mapStyles.getPropertyValue("--gallery-map-land").trim() || "#eef3f0";
      const lineColor = mapStyles.getPropertyValue("--gallery-map-line").trim() || "#d7dfdb";
      const borderColor = mapStyles.getPropertyValue("--gallery-map-border").trim() || "#bac9c2";

      if (settings.terrain) {
        window.L.imageOverlay(settings.terrain.url, settings.terrain.bounds, {
          alt: "",
          className: "gallery-map-terrain",
          interactive: false,
          opacity: 0.5
        }).addTo(map);
      }

      window.L.geoJSON(window.GALLERY_WORLD_LAND, {
        interactive: false,
        style: {
          color: lineColor,
          fillColor: landColor,
          fillOpacity: settings.terrain ? 0.07 : 1,
          opacity: 1,
          weight: 0.8
        }
      }).addTo(map);

      const south = bounds.getSouth();
      const west = bounds.getWest();
      const north = bounds.getNorth();
      const east = bounds.getEast();
      const latitudeStart = Math.ceil(south / 5) * 5;
      const longitudeStart = Math.ceil(west / 5) * 5;
      for (let latitude = latitudeStart; latitude <= north; latitude += 5) {
        window.L.polyline(
          [[latitude, west], [latitude, east]],
          { color: lineColor, interactive: false, opacity: 0.1, weight: 0.45 }
        ).addTo(map);
      }
      for (let longitude = longitudeStart; longitude <= east; longitude += 5) {
        window.L.polyline(
          [[south, longitude], [north, longitude]],
          { color: lineColor, interactive: false, opacity: 0.1, weight: 0.45 }
        ).addTo(map);
      }

      window.L.geoJSON(window.GALLERY_WORLD_COUNTRIES, {
        interactive: false,
        style: {
          color: borderColor,
          fillOpacity: 0,
          opacity: 0.55,
          weight: 0.7
        }
      }).addTo(map);
    };

    const drawAdministrativeRegions = (map, mapElement, region, regionLocations) => {
      const adminData = window.GALLERY_ADMIN1[region];
      if (!adminData) {
        return { adminLabels: [], adminLayers: new Map(), adminStyle: () => ({}) };
      }

      const mapStyles = window.getComputedStyle(mapElement);
      const adminLine = mapStyles.getPropertyValue("--gallery-map-admin-line").trim() || "#c5d1cb";
      const visitedFill = mapStyles.getPropertyValue("--gallery-map-admin-visited").trim() || "#d9a068";
      const activeColor = mapStyles.getPropertyValue("--gallery-map-admin-active").trim() || "#945638";
      const visitedCodes = new Set(regionLocations.map((location) => location.admin).filter(Boolean));
      const adminLayers = new Map();
      const adminLabels = [];

      map.createPane("galleryAdminLabels");
      const labelPane = map.getPane("galleryAdminLabels");
      labelPane.style.zIndex = "450";
      labelPane.style.pointerEvents = "none";
      labelPane.setAttribute("aria-hidden", "true");

      const adminStyle = (isVisited, isActive = false) => ({
        className: `gallery-map-admin-boundary${isVisited ? " is-visited" : ""}${isActive ? " is-active" : ""}`,
        color: isActive || isVisited ? activeColor : adminLine,
        fillColor: visitedFill,
        fillOpacity: isActive ? 0.5 : isVisited ? 0.3 : 0,
        opacity: isActive ? 0.95 : isVisited ? 0.75 : 0.35,
        weight: isActive ? 1.15 : isVisited ? 0.8 : 0.45
      });

      window.L.geoJSON(adminData, {
        interactive: false,
        style: (feature) => adminStyle(visitedCodes.has(feature.properties.iso_3166_2)),
        onEachFeature: (feature, layer) => {
          const code = feature.properties.iso_3166_2;
          const isVisited = visitedCodes.has(code);
          adminLayers.set(code, { feature, isVisited, layer });
          if (!isVisited) return;

          const latitude = Number(feature.properties.latitude);
          const longitude = Number(feature.properties.longitude);
          if (!Number.isFinite(latitude) || !Number.isFinite(longitude)) return;

          const priority = primaryAdminLabels[region]?.has(code) ? "primary" : "secondary";
          const label = document.createElement("span");
          label.className = "gallery-map-admin-label";
          label.textContent = getAdminName(feature.properties);
          const [offsetX = 0, offsetY = 0] = adminLabelOffsets[code] || [];
          label.style.setProperty("--gallery-admin-label-x", `${offsetX}px`);
          label.style.setProperty("--gallery-admin-label-y", `${offsetY}px`);

          const labelMarker = window.L.marker([latitude, longitude], {
            interactive: false,
            keyboard: false,
            pane: "galleryAdminLabels",
            icon: window.L.divIcon({
              className: `gallery-map-admin-label-shell${priority === "secondary" ? " is-admin-label-hidden" : ""}`,
              html: label,
              iconAnchor: [0, 0],
              iconSize: [0, 0]
            })
          });
          labelMarker.on("add", () => {
            labelMarker.getElement()?.setAttribute("aria-hidden", "true");
          });
          labelMarker.addTo(map);
          adminLabels.push({ code, marker: labelMarker, priority, properties: feature.properties });
        }
      }).addTo(map);

      return { adminLabels, adminLayers, adminStyle };
    };

    const updateAdminLabels = (record) => {
      const showDetailLabels = record.map.getZoom() >= 6;
      record.adminLabels.forEach((labelRecord) => {
        const element = labelRecord.marker.getElement();
        if (!element) return;
        element.classList.toggle(
          "is-admin-label-hidden",
          labelRecord.priority === "secondary" && !showDetailLabels
        );
        const label = element.querySelector(".gallery-map-admin-label");
        if (label) label.textContent = getAdminName(labelRecord.properties);
      });
    };

    const setAdminActive = (record, code, isActive) => {
      const adminRecord = record.adminLayers.get(code);
      if (!adminRecord) return;
      adminRecord.layer.setStyle(record.adminStyle(adminRecord.isVisited, isActive));
      if (isActive) adminRecord.layer.bringToFront();
      const labelRecord = record.adminLabels.find((item) => item.code === code);
      labelRecord?.marker
        .getElement()
        ?.querySelector(".gallery-map-admin-label")
        ?.classList.toggle("is-active", isActive);
    };

    mapElements.forEach((mapElement) => {
      const region = mapElement.dataset.galleryRegion;
      const settings = regionSettings[region];
      const regionLocations = usableLocations.filter((location) => location.region === region);
      if (!settings || regionLocations.length === 0) {
        setUnavailable(mapElement);
        return;
      }

      const displayBounds = window.L.latLngBounds(settings.bounds);
      const navigationBounds = window.L.latLngBounds(settings.maxBounds);
      regionLocations.forEach((location) => {
        const point = window.L.latLng(location.lat, location.lng);
        displayBounds.extend(point);
        navigationBounds.extend(point);
      });
      const paddedNavigationBounds = navigationBounds.pad(0.08);

      const map = window.L.map(mapElement, {
        attributionControl: false,
        doubleClickZoom: true,
        dragging: !coarsePointer,
        keyboard: true,
        maxBounds: paddedNavigationBounds,
        maxBoundsViscosity: 1,
        maxZoom: 10,
        minZoom: 0,
        scrollWheelZoom: false,
        tap: false,
        touchZoom: true,
        zoomControl: true
      });

      map.fitBounds(displayBounds, {
        animate: false,
        maxZoom: settings.maxInitialZoom,
        padding: [18, 18]
      });
      map.setMinZoom(map.getZoom());

      drawRegionalBase(map, mapElement, settings, paddedNavigationBounds);
      const adminRecords = drawAdministrativeRegions(map, mapElement, region, regionLocations);

      const clusterGroup = window.L.markerClusterGroup({
        animate: !reducedMotion,
        animateAddingMarkers: false,
        iconCreateFunction: (cluster) => window.L.divIcon({
          className: "gallery-map-cluster-shell",
          html: `<span class="gallery-map-cluster-count" aria-hidden="true">${cluster.getChildCount()}</span>`,
          iconAnchor: [22, 22],
          iconSize: [44, 44]
        }),
        maxClusterRadius: (zoom) => (zoom < 5 ? 46 : zoom < 7 ? 36 : 26),
        showCoverageOnHover: false,
        spiderLegPolylineOptions: { color: "#547a6d", opacity: 0.55, weight: 1 },
        spiderfyOnMaxZoom: true,
        zoomToBoundsOnClick: true
      });
      const mapRecord = {
        ...adminRecords,
        clusterGroup,
        displayBounds,
        map,
        mapElement,
        region,
        settings
      };
      mapRecords.push(mapRecord);

      regionLocations.forEach((location) => {
        location.photos.forEach((photoId) => {
          const marker = window.L.marker([location.lat, location.lng], {
            autoPanOnFocus: true,
            icon: window.L.divIcon({
              className: "gallery-map-marker-shell",
              html: '<span class="gallery-map-marker-dot" aria-hidden="true"></span>',
              iconAnchor: [22, 22],
              iconSize: [44, 44]
            }),
            keyboard: true,
            riseOnHover: true
          });
          const markerRecord = {
            admin: location.admin,
            adminProperties: location.adminProperties,
            mapRecord,
            marker,
            photoId,
            region: location.region
          };
          marker.bindTooltip(makeTooltip(markerRecord), {
            className: "gallery-map-tooltip",
            direction: "top",
            offset: [0, -14],
            opacity: 1
          });
          marker.on("add", () => {
            updateMarkerLanguage(markerRecord);
            const markerElement = marker.getElement();
            if (markerElement && !markerElement.dataset.galleryKeyboardReady) {
              markerElement.dataset.galleryKeyboardReady = "true";
              markerElement.addEventListener("focus", () => {
                setAdminActive(mapRecord, location.admin, true);
              });
              markerElement.addEventListener("blur", () => {
                setAdminActive(mapRecord, location.admin, false);
              });
              markerElement.addEventListener("keydown", (event) => {
                if (event.key === " " || event.key === "Enter") {
                  event.preventDefault();
                  goToPhoto(photoId);
                }
              });
            }
          });
          marker.on("mouseover", () => setAdminActive(mapRecord, location.admin, true));
          marker.on("mouseout", () => setAdminActive(mapRecord, location.admin, false));
          marker.on("click", () => goToPhoto(photoId));
          markerRecords.push(markerRecord);
          clusterGroup.addLayer(marker);
        });
      });

      clusterGroup.addTo(map);
      map.on("moveend zoomend", () => window.requestAnimationFrame(() => {
        updateAdminLabels(mapRecord);
        updateClusterLabels(mapRecord);
      }));
      clusterGroup.on("animationend spiderfied unspiderfied", () => {
        window.requestAnimationFrame(() => updateClusterLabels(mapRecord));
      });
      mapElement.classList.add("is-ready");
      mapElement.setAttribute("tabindex", "0");
    });

    const resetMap = (record) => {
      record.map.setMinZoom(0);
      record.map.fitBounds(record.displayBounds, {
        animate: false,
        maxZoom: record.settings.maxInitialZoom,
        padding: [18, 18]
      });
      record.map.setMinZoom(record.map.getZoom());
    };

    const constrainMap = (record) => {
      const nextMinimum = Math.min(
        record.map.getBoundsZoom(record.displayBounds, false, window.L.point(18, 18)),
        record.settings.maxInitialZoom
      );
      record.map.setMinZoom(nextMinimum);
      if (record.map.getZoom() < nextMinimum) {
        record.map.setZoom(nextMinimum, { animate: false });
      }
    };

    const updateLanguage = () => {
      const language = currentLanguage();
      updatePhotoCaptions();
      markerRecords.forEach(updateMarkerLanguage);
      mapRecords.forEach((record) => {
        const regionName = record.mapElement
          .closest(".gallery-region")
          ?.querySelector(".gallery-region-header h2")
          ?.textContent.trim() || "";
        const zoomIn = record.mapElement.querySelector(".leaflet-control-zoom-in");
        const zoomOut = record.mapElement.querySelector(".leaflet-control-zoom-out");
        if (zoomIn) {
          const label = language === "zh" ? `放大${regionName}地图` : `Zoom in ${regionName} map`;
          zoomIn.setAttribute("aria-label", label);
          zoomIn.setAttribute("title", label);
        }
        if (zoomOut) {
          const label = language === "zh" ? `缩小${regionName}地图` : `Zoom out ${regionName} map`;
          zoomOut.setAttribute("aria-label", label);
          zoomOut.setAttribute("title", label);
        }
        window.requestAnimationFrame(() => {
          updateAdminLabels(record);
          updateClusterLabels(record);
        });
      });
      mapElements.filter((element) => element.classList.contains("is-unavailable")).forEach((element) => {
        const message = element.querySelector(".gallery-map-loading");
        if (message) message.textContent = copy[language].unavailable;
      });
    };

    const languageObserver = new MutationObserver(updateLanguage);
    languageObserver.observe(document.documentElement, {
      attributeFilter: ["data-ui-lang"],
      attributes: true
    });

    if (window.ResizeObserver) {
      const resizeObserver = new ResizeObserver((entries) => {
        entries.forEach((entry) => {
          const record = mapRecords.find(({ mapElement }) => mapElement === entry.target);
          if (record) {
            record.map.invalidateSize({ animate: false });
            constrainMap(record);
          }
        });
      });
      mapRecords.forEach(({ mapElement }) => resizeObserver.observe(mapElement));
    }

    window.setTimeout(() => {
      mapRecords.forEach((record) => {
        record.map.invalidateSize({ animate: false });
        resetMap(record);
      });
      updateLanguage();
    }, 0);
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialiseMaps, { once: true });
  } else {
    initialiseMaps();
  }
})();
