# Gói duyệt biên tập: "How Does a Bridge Carry Its Load?" (M6, narration `m6-r1`)

> **Agent không tự duyệt.** 14 claim (CLM_601–CLM_614) đều ở trạng thái `SOURCE_VERIFIED`: câu trích đã được đối chiếu nguyên văn, nhưng chưa được duyệt biên tập. Gate G1 và G6 chặn cho tới khi một người có tên duyệt (mục 5).

- Ngày soạn: 2026-10-29. Người soạn: agent. Người duyệt: _(chưa có)_.
- Phạm vi: câu chữ lời dẫn (`script/narration.json`), chữ trên màn hình (nhãn, callout, chú giải, thẻ 'Conceptual load path — not to scale') và cách thể hiện bằng hình (mũi tên tải, phản lực, đường truyền tải).
- Không có con số nào về nội lực, sức chịu tải, hệ số an toàn, ứng suất hay độ võng. Độ dài mũi tên là cố định, không biểu diễn độ lớn.

## 1. Nguồn

- **SRC_ODOT_MBI**: Manual of Bridge Inspection (Part 2 Ratings; Glossary). Ohio Department of Transportation (working group incl. FHWA), Published 1973, revised 2010. https://www.dot.state.oh.us/Divisions/Engineering/Structures/News%20Document/Manual%20of%20Bridge%20Inspection_2010.pdf (truy cập 2026-10-28). PDF downloaded 2026-10-28, text extracted with pdftotext; every excerpt matched verbatim; page = PDF page.
- **SRC_FHWA_CBM**: Covered Bridge Manual (FHWA-HRT-04-098), Chapter 2. Covered Bridges: Form, Use, and Terminology. Federal Highway Administration, April 2005. https://www.fhwa.dot.gov/publications/research/infrastructure/structures/04098/02.cfm (truy cập 2026-10-28). Page HTML fetched 2026-10-28; excerpts matched verbatim in the page text.
- **SRC_FHWA_PBES_GLOSSARY**: Connection Details for Prefabricated Bridge Elements and Systems (FHWA-IF-09-010), Appendix E: Glossary. Federal Highway Administration. https://www.fhwa.dot.gov/bridge/prefab/if09010/appe.cfm (truy cập 2026-10-28). Page HTML fetched 2026-10-28; excerpts matched verbatim.
- **SRC_FHWA_PBES_CH2**: Connection Details for Prefabricated Bridge Elements and Systems (FHWA-IF-09-010), Chapter 2: Superstructure Connections. Federal Highway Administration. https://www.fhwa.dot.gov/bridge/prefab/if09010/02.cfm (truy cập 2026-10-28). Read with a web-fetch tool 2026-10-28 (introduction, AASHTO definition quoted).
- **SRC_SCI_TRUSSES**: Trusses: types, design and applications in buildings. steelconstruction.info (Steel Construction Institute resource). https://www.steelconstruction.info/Trusses (truy cập 2026-10-28). Page HTML fetched 2026-10-28; excerpts matched verbatim.
- **SRC_YALE_PHYSICS**: The Physics of Bridges (curriculum unit 01.05.08), Theresa Matthews. Yale-New Haven Teachers Institute (Yale University), 2001, Volume V. https://teachersinstitute.yale.edu/curriculum/units/2001/5/01.05.08/6 (truy cập 2026-10-28). Page HTML fetched 2026-10-28; excerpts matched verbatim.

## 2. Bảng claim

Ký hiệu: ✅ = nguồn nói gần như nguyên văn; ◐ = được hỗ trợ nhưng có diễn giải, giả định hoặc lệch nhỏ.

### CLM_601
| | |
|---|---|
| Câu chữ claim | Loads on a bridge include live loads such as traffic and the dead load of the structure's own weight. |
| Dùng trong beat | B1 |
| Nguồn (nguyên văn) | SRC_ODOT_MBI Glossary p.365 'live load': "live load - a temporary dynamic load such as vehicular traffic that is applied to a structure" · SRC_ODOT_MBI Glossary p.350 'dead load': "dead load - a static load due to the weight of the structure itself" |
| Giả định | Generic definition of load types; no magnitudes. |
| Áp dụng cho | all; bộ phận: deck_planks, deck |
| Hình (chú thích) | B1_load (LOAD_ARROW "Load"); B3_load (LOAD_ARROW "Load") |
| Hỗ trợ trực tiếp? | ◐ |
| Ghi chú cho người duyệt | Nguồn định nghĩa live load là 'vehicular traffic'. Lời dẫn thêm 'people'; điều này được CLM_602 hỗ trợ (deck đỡ 'vehicular and pedestrian traffic'). Lời dẫn không nói tới tải gió, tuyết hay động đất. Đây là cách giản lược có chủ ý. |
| **Đề xuất** | **DUYỆT** |

### CLM_602
| | |
|---|---|
| Câu chữ claim | The deck directly supports traffic and is itself supported by the superstructure. |
| Dùng trong beat | B1, B2 |
| Nguồn (nguyên văn) | SRC_ODOT_MBI Glossary p.350 'deck': "deck - that portion of a bridge which provides direct support for vehicular and pedestrian traffic, supported by a superstructure" |
| Giả định | Definition. |
| Áp dụng cho | all; bộ phận: deck_planks, deck |
| Hình (chú thích) | — |
| Hỗ trợ trực tiếp? | ✅ |
| Ghi chú cho người duyệt | Định nghĩa thuật ngữ, không có chỗ mơ hồ. |
| **Đề xuất** | **DUYỆT** |

### CLM_603
| | |
|---|---|
| Câu chữ claim | The superstructure is the part of a bridge that provides the horizontal span; it typically includes beams, girders, trusses and the deck. |
| Dùng trong beat | B2 |
| Nguồn (nguyên văn) | SRC_FHWA_PBES_CH2 Chapter 2 introduction (AASHTO definition): "Structural parts of the bridge that provide the horizontal span." · SRC_FHWA_PBES_GLOSSARY Appendix E 'superstructure': "It typically includes beams, girders, trusses, and the bridge deck." |
| Giả định | Definition; the cap beams of a timber bent belong to the substructure (pier cap). |
| Áp dụng cho | all; bộ phận: superstructure |
| Hình (chú thích) | B2_super (HIGHLIGHT_REGION "Superstructure") |
| Hỗ trợ trực tiếp? | ✅ |
| Ghi chú cho người duyệt | Định nghĩa AASHTO, trích qua FHWA. Lời dẫn: 'the part of the bridge that spans the gap'. Khung HIGHLIGHT_REGION bao cả giàn và mặt cầu, đúng với nguồn ('beams, girders, trusses, and the bridge deck'). |
| **Đề xuất** | **DUYỆT** |

### CLM_604
| | |
|---|---|
| Câu chữ claim | The substructure - abutments at the ends and piers in between - supports the superstructure, and abutments transfer loads from the superstructure to the foundation. |
| Dùng trong beat | B2 |
| Nguồn (nguyên văn) | SRC_ODOT_MBI Glossary p.383 'substructure': "substructure - the abutments and piers built to support the span of a bridge superstructure" · SRC_ODOT_MBI Glossary p.338 'abutment': "abutment - part of bridge substructure at either end of bridge which transfers loads from superstructure to foundation" · SRC_ODOT_MBI Glossary p.370 'pier': "pier - a substructure unit that supports the spans of a multi-span superstructure at an intermediate location between its abutments" |
| Giả định | Definitions; in the timber model the trestle bents play the role of piers and the banks of the site the role of abutments (illustrative). |
| Áp dụng cho | all; bộ phận: substructure, ground |
| Hình (chú thích) | B2_path (CONCEPTUAL_LOAD_PATH); B2_abut (COMPONENT_LABEL "Abutment"); B2_pier (COMPONENT_LABEL "Pier"); B2_found (COMPONENT_LABEL "Foundation") |
| Hỗ trợ trực tiếp? | ✅ |
| Ghi chú cho người duyệt | 'sometimes piers in between' khớp với định nghĩa pier là trụ ở vị trí trung gian của kết cấu nhiều nhịp. Mô hình giàn minh họa có 2 nhịp và 1 trụ. Nhãn 'Foundation' chỉ vào chân mố; mô hình không có hình học móng riêng, nên đây là chỉ vị trí, không phải mô tả cấu tạo móng. |
| **Đề xuất** | **DUYỆT, lưu ý nhãn Foundation** |

### CLM_605
| | |
|---|---|
| Câu chữ claim | A beam spans from one support to another and supports vertical loads. |
| Dùng trong beat | B3 |
| Nguồn (nguyên văn) | SRC_ODOT_MBI Glossary p.341 'beam': "beam - a linear structural member designed to span from one support to another and support vertical loads" |
| Giả định | Definition. |
| Áp dụng cho | beam; bộ phận: stringer |
| Hình (chú thích) | B3_beams (COMPONENT_LABEL "Beams") |
| Hỗ trợ trực tiếp? | ✅ |
| Ghi chú cho người duyệt | Định nghĩa beam. Trong mô hình cầu gỗ, dầm là các stringer (vocabulary: stringer = primary beams). |
| **Đề xuất** | **DUYỆT** |

### CLM_606
| | |
|---|---|
| Câu chữ claim | A beam carries load through its resistance to bending. |
| Dùng trong beat | B3, B7 |
| Nguồn (nguyên văn) | SRC_FHWA_CBM Chapter 2, 'Component Terminology': "As a beam has strength from its bending resistance" · SRC_ODOT_MBI Glossary p.358 'girder': "girder - a horizontal flexural member that is the main or primary support for a structure" |
| Giả định | Qualitative; no stresses, deflections or capacities. The procedural model has not been analysed. |
| Áp dụng cho | beam; bộ phận: stringer |
| Hình (chú thích) | B3_bend (CALLOUT "Resists bending"); B7_beam (CALLOUT "Bending") |
| Hỗ trợ trực tiếp? | ◐ |
| Ghi chú cho người duyệt | Câu FHWA CBM ('As a beam has strength from its bending resistance') nằm trong đoạn nói về giàn, nhưng là phát biểu chung về dầm. ODOT định nghĩa girder là 'horizontal flexural member'. Hình không vẽ độ võng (không bịa biến dạng). |
| **Đề xuất** | **DUYỆT** |

### CLM_607
| | |
|---|---|
| Câu chữ claim | A cap at the top of a bent distributes the loads onto its columns, and columns are vertical members resisting compression. |
| Dùng trong beat | B3 |
| Nguồn (nguyên văn) | SRC_ODOT_MBI Glossary p.344 'cap': "cap - the topmost portion of a pier or a pile bent serving to distribute the loads upon the columns or piles" · SRC_ODOT_MBI Glossary p.341 'bent': "bent - a substructure unit made up of two or more column or column-like members connected at their top-most ends by a cap" · SRC_ODOT_MBI Glossary p.346 'column': "column - a general term applying to a vertical member resisting compressive stresses" |
| Giả định | Definitions; the posts of the illustrative trestle bents are treated as columns. |
| Áp dụng cho | beam; bộ phận: cap_beam, trestle_bent |
| Hình (chú thích) | B3_path (CONCEPTUAL_LOAD_PATH); B3_cap (COMPONENT_LABEL "Cap beam"); B3_posts (CALLOUT "Posts: compression") |
| Hỗ trợ trực tiếp? | ◐ |
| Ghi chú cho người duyệt | Nguồn nói về cap của pier/pile bent và column chịu nén. Mô hình gọi các cột là 'posts' của trestle bent. Lời dẫn 'posts carry it down in compression' là áp dụng định nghĩa column cho post. Người duyệt xác nhận cách gọi này. |
| **Đề xuất** | **DUYỆT, hoặc đổi 'posts' thành 'columns'** |

### CLM_608
| | |
|---|---|
| Câu chữ claim | A stone arch ring is made of wedge-shaped stones called voussoirs; the keystone is the wedge-like stone at the crown. |
| Dùng trong beat | B4 |
| Nguồn (nguyên văn) | SRC_ODOT_MBI Glossary p.388 'voussoir': "Voussoir - one of the truncated wedge-shaped stones composing a ring course in a stone arch" · SRC_ODOT_MBI Glossary p.363 'keystone': "keystone - the symmetrically shaped, wedge-like stone located in a head ring course at the crown of an arch" |
| Giả định | Definitions. |
| Áp dụng cho | arch; bộ phận: voussoir, keystone |
| Hình (chú thích) | B4_vous (COMPONENT_LABEL "Voussoirs"); B4_key (COMPONENT_LABEL "Keystone") |
| Hỗ trợ trực tiếp? | ✅ |
| Ghi chú cho người duyệt | Định nghĩa voussoir và keystone. |
| **Đề xuất** | **DUYỆT** |

### CLM_609
| | |
|---|---|
| Câu chữ claim | The curve of an arch converts vertical loads into horizontal and vertical thrusts at its ends, so the forces within the arch are generally compression. |
| Dùng trong beat | B5, B7 |
| Nguồn (nguyên văn) | SRC_ODOT_MBI Part 2 Ratings, Item 25 Arch, p.144 (manual p.2-56): "The curve converts vertical (gravity) loads within the span to horizontal and vertical thrusts at the spring lines. As a result, the forces within the arch are generally compression" · SRC_ODOT_MBI Glossary p.339 'arch': "arch - a curved structure element primarily in compression that transfers vertical loads through inclined reactions to its end supports" · SRC_YALE_PHYSICS 'Arch Bridges' section: "Arch bridges rely primarily on compression" |
| Giả định | General principle for masonry arches under gravity load; no thrust line, magnitudes or stability assessment of the illustrative model. |
| Áp dụng cho | arch; bộ phận: arch_ring |
| Hình (chú thích) | B5_load (LOAD_ARROW "Load"); B5_thrust (CONCEPTUAL_LOAD_PATH); B5_comp (CALLOUT "Mainly compression"); B7_arch (CALLOUT "Compression") |
| Hỗ trợ trực tiếp? | ✅ |
| Ghi chú cho người duyệt | ODOT: 'generally compression'. Lời dẫn: 'mainly in compression'. Mức độ tương đương. Đường lực nén là khái niệm (có nhãn 'not to scale'). |
| **Đề xuất** | **DUYỆT** |

### CLM_610
| | |
|---|---|
| Câu chữ claim | An arch transfers vertical loads through inclined reactions to its end supports, and the abutments push inward on the arch. |
| Dùng trong beat | B5 |
| Nguồn (nguyên văn) | SRC_ODOT_MBI Glossary p.339 'arch': "transfers vertical loads through inclined reactions to its end supports" · SRC_YALE_PHYSICS 'Arch Bridges' section: "creating two equal and opposite horizontal forces that push inward on the arch" |
| Giả định | Direction only (inclined, upward and inward on the arch); no magnitudes; the arrow is a support REACTION, distinct from the applied load. |
| Áp dụng cho | arch; bộ phận: abutment, pier |
| Hình (chú thích) | B5_react (REACTION_ARROW "Supports push back") |
| Hỗ trợ trực tiếp? | ◐ |
| Ghi chú cho người duyệt | Nguồn nói 'inclined reactions to its end supports' và 'abutments push inward on the arch'. Lời dẫn nói 'supports'. Mũi tên phản lực đặt ở hai chân vòm giữa, nơi gối lên trụ, không phải mố. Với cầu nhiều nhịp, lực xô ngang tại trụ còn được các nhịp kề cân bằng, và lời dẫn không giải thích điểm này. Hướng mũi tên (lên và vào trong) chỉ là khái niệm. |
| **Đề xuất** | **DUYỆT, hoặc chuyển mũi tên sang vòm biên (gối lên mố)** |

### CLM_611
| | |
|---|---|
| Câu chữ claim | A truss is a jointed structure of members arranged in triangles, primarily carrying axial loads. |
| Dùng trong beat | B6 |
| Nguồn (nguyên văn) | SRC_ODOT_MBI Glossary p.386 'truss': "truss - a jointed structure made up of individual members primarily carrying axial loads arranged and connected in triangular panels" · SRC_SCI_TRUSSES Introduction: "A truss is essentially a triangulated system of (usually) straight interconnected structural elements" |
| Giả định | Definition. |
| Áp dụng cho | truss; bộ phận: truss_members, truss_joint |
| Hình (chú thích) | B6_joints (COMPONENT_LABEL "Joints") |
| Hỗ trợ trực tiếp? | ✅ |
| Ghi chú cho người duyệt | Định nghĩa truss. |
| **Đề xuất** | **DUYỆT** |

### CLM_612
| | |
|---|---|
| Câu chữ claim | The principal force in each truss member is axial tension or compression. |
| Dùng trong beat | B6, B7 |
| Nguồn (nguyên văn) | SRC_SCI_TRUSSES Introduction: "The principal force in each element in a truss is axial tension or compression." · SRC_FHWA_CBM Chapter 2, 'Component Terminology': "These axial forces are either compression or tension." |
| Giả định | Idealisation (pinned joints); the source notes real joints are not perfectly pinned. No member-by-member forces are shown. |
| Áp dụng cho | truss; bộ phận: truss_members |
| Hình (chú thích) | B6_legend (TENSION_COMPRESSION_LEGEND); B7_truss (CALLOUT "Tension and compression") |
| Hỗ trợ trực tiếp? | ✅ |
| Ghi chú cho người duyệt | 'mainly pulled or pushed along its length' là diễn giải 'principal force ... axial tension or compression'. |
| **Đề xuất** | **DUYỆT** |

### CLM_613
| | |
|---|---|
| Câu chữ claim | In a simple-span truss under downward loads, the top chord is in compression and the bottom chord is in tension. |
| Dùng trong beat | B6 |
| Nguồn (nguyên văn) | SRC_FHWA_CBM Chapter 2, 'Component Terminology': "The upper, or top, chords are in compression. The bottom, or lower, chords are in tension." · SRC_SCI_TRUSSES 'Types of trusses': "Under gravity loads, the top and bottom chords of the truss provide the compression and tension resistance to overall bending" |
| Giả định | ASSUMPTION: each truss span of the illustrative model is treated as a simple span (separate truss on its own bearings) carrying a downward load. The FHWA source calls this a simplified characterization for the common single-span bridge; continuous spans behave differently. Qualitative only. |
| Áp dụng cho | truss; bộ phận: truss_chord |
| Hình (chú thích) | B6_top (CALLOUT "Top chord: compression"); B6_bottom (CALLOUT "Bottom chord: tension") |
| Hỗ trợ trực tiếp? | ◐ |
| Ghi chú cho người duyệt | GIẢ ĐỊNH: mỗi nhịp giàn trong mô hình là nhịp giản đơn, có gối riêng. Mô hình có 2 nhịp tách rời. FHWA CBM gọi đây là mô tả đơn giản hóa cho cầu một nhịp; giàn liên tục làm việc khác. Lời dẫn nêu rõ 'Each span here is a simple span'. Chỉ gọi tên biên trên và biên dưới, không tô màu thanh nào. |
| **Đề xuất** | **DUYỆT nếu chấp nhận giả định nhịp giản đơn** |

### CLM_614
| | |
|---|---|
| Câu chữ claim | In a truss, some web members are in compression and others in tension. |
| Dùng trong beat | B6 |
| Nguồn (nguyên văn) | SRC_FHWA_CBM Chapter 2, 'Component Terminology': "Some of these web members will usually be in compression; others will consistently be in tension." |
| Giả định | General statement; which web member carries which force is NOT shown (no load case analysed). |
| Áp dụng cho | truss; bộ phận: truss_web |
| Hình (chú thích) | B6_web (COMPONENT_LABEL "Web members") |
| Hỗ trợ trực tiếp? | ✅ |
| Ghi chú cho người duyệt | 'Some ... others ...' giữ đúng mức chung của nguồn. Không chỉ định thanh bụng nào chịu kéo hay nén, và không tô màu. |
| **Đề xuất** | **DUYỆT** |

## 3. Lời dẫn theo beat

**B1** (fact; claim CLM_601, CLM_602)
- s0: What happens when weight is placed on a bridge?
- s1: Traffic, people and the bridge's own weight all press down on its deck.
- s2: To stay standing, the bridge has to carry that load down into the ground.

**B2** (fact; claim CLM_602, CLM_603, CLM_604)
- s0: The load follows a path down through the structure.
- s1: The deck is carried by the superstructure, the part of the bridge that spans the gap.
- s2: That rests on the substructure: abutments at the ends, and sometimes piers in between.
- s3: The abutments pass the load on to the foundations.

**B3** (fact; claim CLM_605, CLM_606, CLM_607)
- s0: Now take a beam bridge.
- s1: Its deck rests on long beams that span from one support to the next.
- s2: Each beam carries the load by resisting bending.
- s3: A cap beam spreads the load onto the posts, and the posts carry it down in compression.

**B4** (fact; claim CLM_608)
- s0: A masonry arch works differently.
- s1: It is built from wedge-shaped stones called voussoirs, with a keystone at the crown.

**B5** (fact; claim CLM_609, CLM_610)
- s0: The curve turns the downward load into thrust along the arch, pressing the stones together.
- s1: So the arch works mainly in compression.
- s2: At each end it pushes outward and down on its supports, and the supports push back.

**B6** (fact; claim CLM_611, CLM_612, CLM_613, CLM_614)
- s0: The truss we started with takes another approach: straight members joined into triangles.
- s1: Each member is mainly pulled or pushed along its length, in tension or in compression.
- s2: Each span here is a simple span, so under a downward load its top chord is squeezed and its bottom chord is stretched.
- s3: Inside, some web members are in compression and others are in tension.

**B7** (interpretation; claim CLM_606, CLM_609, CLM_612)
- s0: Let's compare them one at a time.
- s1: The beam bridge carries its load by bending.
- s2: The arch carries it mainly in compression, pushing against its supports.
- s3: In the truss, the load is shared between members in tension and in compression.

**B8** (framing; claim —)
- s0: Three arrangements of parts, one job: carrying the load across the gap and down into the ground.
- s1: These models are illustrations, not engineering designs, and the arrows show ideas, not calculated forces.

## 4. Cần nghe lại (phát âm và độ rõ)

ASR (Whisper large-v3-turbo) nhận đúng cả 26 câu (WER ≤ 0.087). Sai khác đều nằm ở chính tả, không phải ở nghĩa: 'veussoirs' cho *voussoirs* (B4.s1) và 'cord' cho *chord* (B6.s2, từ đồng âm). Ở bản đầu, câu B7.s3 "The truss shares it…" bị nghe thành "The trust shares it…", nên agent đã viết lại thành "In the truss, the load is shared…" (WER 0). Người nghe cần xác nhận:
- *voussoirs* /ˈvuːswɑːz/ (misaki: vˈuːswɑːz), *keystone*, *abutments*, *superstructure*, *substructure*, *truss*, *chord*.
- Giọng `bf_emma` là mặc định kỹ thuật tạm thời, **chưa được người dùng duyệt** (xem `review/voice_audition/AUDITION.md`).

## 5. Cách ghi quyết định (chỉ người duyệt)

Với mỗi claim được duyệt, trong `research/sources.json`: đặt `review_status` thành `EDITORIALLY_APPROVED` và thêm `editorial_approval: {approved_by, approved_on, narration_revision: "m6-r1"}`. Claim bị bác: đặt `REJECTED`; planner sẽ chặn mọi beat và chú thích dùng nó. Sửa câu chữ: sửa `script/narration.json` và `script/visual_beats.json` (hai file phải khớp nhau), rồi chạy `narrate → asr-check → align → lock-audio → plan-visuals → build-shots`. Khi mọi claim đã duyệt, đặt `factual_review: "verified"` trong `project.json`.
