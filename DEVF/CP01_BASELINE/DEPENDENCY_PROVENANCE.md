# Dependencias efectivas del baseline Windows

Datos recibidos del artefacto del run38256856294. Los hashes son de los paquetes descargados; no se incluyen los paquetes ni su contenido.

| Origen | Archivo | Bytes | SHA256 observado |
|---|---|---:|---|
| _deps | 20240722.0.tar.gz | 2242861 | `f50e5ac311a81382da7fa75b97310e4b9006474f9560ac46f54a9967f07d4ae3` |
| _deps | v3.3.1.tar.gz | 161557 | `3bfc70542c521d4b55a46429d808178916a579b28d048bd8c727ee76c39e2072` |
| _deps | dawn-windows-amd64.tar.gz | 14209713 | `42a7a295c87b2e8a36312e2f84a5823aac63325e8e1d271bc7ced6f83bfb075f` |
| _deps | 12.1.0.tar.gz | 711419 | `ea7de4299689e12b6dddd392f9896f08fb0777ac7168897a244a6d6085043fea` |
| _deps | v1.17.0.tar.gz | 885595 | `65fab701d9829d38cb77c14acdc431d2108bfdbf8979e40eb8ae567edf10b27c` |
| _deps | v1.91.9b-docking.tar.gz | 2006500 | `466fdef9b18de15f0bb6e288e3d00ffa3d82200ec458ce5e4f724a161d9528a5` |
| _deps | twilit-v1.zip | 3890843 | `aa65e6e3446363d03842134182db28e6206e08d366b8efb8f66d26f96a3314be` |
| _deps | 0.734.tar.gz | 3112286 | `cb55a891226d8c70284e22eb9281cc2b4496c709a4050f52aaa18a355fe7b1a3` |
| _deps | miniz-3.0.2.zip | 99268 | `ada38db0b703a56d3dd6d57bf84a9c5d664921d870d8fea4db153979fb5332c5` |
| _deps | json.tar.xz | 114576 | `42f6e95cad6ec532fd372391373363b62a14af6d771056dbfc86160e6dfff7aa` |
| _deps | libnod-windows-x86_64.tar.gz | 6408338 | `c9dfecf8e52066a5222f3cb1cad18d0740c958ce65bf60cb84e780a3856ed881` |
| _deps | v1.0.1.tar.gz | 7767 | `9983136544234e573fe07cc1a22fdf978ad7979043e7be2e9082f6d4991ff8a8` |
| _deps | f00a0fee38391b2f927114e11bea18dc0a7dba1e.tar.gz | 4033883 | `6d9fd1164b7873c9dfba72d724753bda9e3db8280c9af802eed8e2a12035f152` |
| _deps | SDL3-windows-amd64.tar.gz | 1948117 | `5a641c2355b4cf3e710662f1b29d1255448ca55d9f34f1c62cd29668eaa3aabb` |
| _deps | sqlite-amalgamation-3510300.zip | 2876305 | `acb1e6f5d832484bf6d32b681e858c38add8b2acdfd42ac5df24b8afb46552b4` |
| _deps | v0.14.1.zip | 6387264 | `908f3a2917fa86a247abfcf85dcf04bad1db6986a4d40f94b70512f3e9e98d5b` |
| _deps | v0.8.3.tar.gz | 1147630 | `aae608dfe8213dfd05d909a57718ef82f30722c392344583d3f39050c7f29a80` |
| downloads | bzip2-1.0.8.tar.gz | 810029 | `ab5a03176ee106d3f0fa90e381da478ddae405918153cca248e682cd0c4a2269` |
| downloads | facebook-zstd-v1.5.7.tar.gz | 2451884 | `37d7284556b20954e56e1ca85b80226768902e2edabd3b649e9e72c0c9012ee3` |
| downloads | freetype-freetype-VER-2-14-3.tar.gz | 2515533 | `dc49de6b01a266eef4876a4dd34d9842c475d3e28ff2eff63bd2fb760ab56261` |
| downloads | google-brotli-v1.2.0.tar.gz | 646315 | `816c96e8e8f193b40151dad7e8ff37b1221d019dbcb9c35cd3fadbfe6477dfec` |
| downloads | madler-zlib-v1.3.2.tar.gz | 1566911 | `b99a0b86c0ba9360ec7e78c4f1e43b1cbdf1e6936c8fa0f6835c0cd694a495a1` |
| downloads | pnggroup-libpng-v1.6.58.tar.gz | 1592190 | `a9d4df463d36a6e5f9c29bd6f4967312d17e996c1854f3511f833924eb1993cf` |

Los otros 20 ZIP observados son fixtures incluidas en el árbol descargado (battery-embed/crashpad-zlib), no descargas independientes ni archivos recibidos del juego. No se extraen ni publican.

Repositorios Git efectivos, incluidos submódulos registrados por FetchContent:

| Path relativo | Commit exacto |
|---|---|
| base64pp-src | `736345896182b50babfe6eaa10b211b90d6abb0b` |
| battery-embed-src | `408567ae3eb296f3aa8d00e1c57d0b7d28ce992b` |
| funchook-src | `88388db3c69e16c1560fee65c6857d75f5ce6fd5` |
| sentry_native-src | `93c4e3221d3a2c91a9797a1195cb5280eff55d5a` |
| yaml-cpp-src | `56e3bb550c91fd7005566f19c079cb7a503223cf` |
| base64pp-src/doxygen-awesome-css | `245c7c94c20eac22730ef89035967f78b77bf405` |
| funchook-src/distorm | `ab59d6e193948cfa5d1482fb6c7e64870e9e93b9` |
| sentry_native-src/external/benchmark | `48f5cc21bac647a8a64e9787cb84f349e334b7ac` |
| sentry_native-src/external/breakpad | `25b6b727af49fa383161e7dba4a82ab0661b69b8` |
| sentry_native-src/external/crashpad | `e5040b878718f5c004d0ecfe1747642c72ddcd39` |
| sentry_native-src/external/libunwindstack-ndk | `284202fb1e42dbeba6598e26ced2e1ec404eecd1` |
| sentry_native-src/external/crashpad/third_party/lss/lss | `9719c1e1e676814c456b55f5f070eabad6709d31` |
| sentry_native-src/external/crashpad/third_party/mini_chromium/mini_chromium | `5d060033dbe1595f612a2f506b7988c8d513d32e` |
| sentry_native-src/external/crashpad/third_party/zlib/zlib | `fef58692c1d7bec94c4ed3d030a45a1832a9615d` |
| sentry_native-src/external/third_party/lss | `ed31caa60f20a4f6569883b2d752ef7522de51e0` |

El CMake original clona automáticamente también submódulos de documentación/tests u otras plataformas (doxygen-awesome-css, benchmark, libunwindstack, LSS), aunque no todos se compilen en Windows. No se añadieron roots ni clones opcionales manualmente. Se conservó este comportamiento original; no se afirma una minimización absoluta de bytes descargados. Los targets randomizer_generator_tests se compilaron por el default del proyecto, pero no se ejecutaron.

Dawn v20260807.225922, SDL3 3.4.10 y nod v2.0.0-alpha.12 usan provider package/shared según auto original. No se reconstruyeron esas bibliotecas desde HEAD. Abseil20240722.0 y miniz3.0.2, junto a paquetes prebuilt, carecen de URL_HASH en sus declaraciones: sus hashes observados se registran aquí; no atribuir al source una verificación que no hace.

symgen1.3.6 Windows x86_64 es una herramienta binaria descargada por CMake, con SHA256 esperado171995a33bfd5a5271b5bb78d3f2c1d4aec58721bf3a894aaad5607ff648e2a4 según el archivo oficial. No forma parte de la lista de archivos comprimidos; su descarga la valida el CMake original.
