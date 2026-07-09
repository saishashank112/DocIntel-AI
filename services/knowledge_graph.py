import streamlit as st
import streamlit.components.v1 as components
import json

def render_knowledge_graph(profile: dict, resume_data: dict):
    """Render a premium Vis.js relation graph mapping skills, companies, and projects."""
    st.markdown("### 📊 Interactive Knowledge Graph")
    st.markdown("Zoom, drag, and click nodes in the graph to explore relationships. Detailed connections list is available below.")
    st.markdown("---")
    
    # ── Fetch Theme Variables ──
    theme = st.session_state.get("theme", "light")
    if theme == "dark":
        bg_canvas = "#0f172a"
        border_canvas = "#334155"
        node_bg = "#1e293b"
        node_border = "#cbd5e1"
        node_text = "#ffffff"
        edge_color = "#475569"
    else:
        bg_canvas = "#ffffff"
        border_canvas = "#cbd5e1"
        node_bg = "#f9fafb"
        node_border = "#111827"
        node_text = "#111827"
        edge_color = "#cbd5e1"

    # ── Extract nodes data ──
    candidate_name = (resume_data.get("name", "Unknown") if resume_data else profile.get("title", "Uploaded Document"))
    skills = (resume_data.get("skills", []) if resume_data else profile.get("key_topics", []))
    projects = (resume_data.get("projects", []) if resume_data else profile.get("themes", []))
    entities = profile.get("main_entities", [])
    companies = ([e["company"] for e in resume_data.get("experience", []) if "company" in e] if resume_data else [])

    # Create node list for Vis.js
    nodes = []
    edges = []
    
    # Candidate node (Center)
    nodes.append({
        "id": 1,
        "label": candidate_name,
        "color": {
            "background": node_bg,
            "border": node_border,
            "highlight": {
                "background": node_bg,
                "border": node_border
            }
        },
        "size": 25,
        "font": {"size": 16, "color": node_text, "face": "Outfit", "bold": True}
    })
    
    node_id = 2
    # Add Skills
    for skill in skills[:12]:
        name = skill.get("title") or skill.get("name") if isinstance(skill, dict) else str(skill)
        nodes.append({
            "id": node_id,
            "label": name,
            "color": {
                "background": node_bg,
                "border": node_border,
                "highlight": {
                    "background": node_bg,
                    "border": node_border
                }
            },
            "size": 15
        })
        edges.append({"from": 1, "to": node_id, "length": 120})
        node_id += 1
        
    # Add Projects
    for project in projects[:10]:
        name = project.get("title") or project.get("name") if isinstance(project, dict) else str(project)
        nodes.append({
            "id": node_id,
            "label": name,
            "color": {
                "background": node_bg,
                "border": node_border,
                "highlight": {
                    "background": node_bg,
                    "border": node_border
                }
            },
            "size": 15
        })
        edges.append({"from": 1, "to": node_id, "length": 150})
        node_id += 1
        
    # Add Companies
    for comp in companies[:8]:
        name = comp.get("title") or comp.get("name") if isinstance(comp, dict) else str(comp)
        nodes.append({
            "id": node_id,
            "label": name,
            "color": {
                "background": node_bg,
                "border": node_border,
                "highlight": {
                    "background": node_bg,
                    "border": node_border
                }
            },
            "size": 15
        })
        edges.append({"from": 1, "to": node_id, "length": 130})
        node_id += 1

    # Add Entities
    for ent in entities[:10]:
        nodes.append({
            "id": node_id,
            "label": str(ent),
            "color": {
                "background": node_bg,
                "border": node_border,
                "highlight": {
                    "background": node_bg,
                    "border": node_border
                }
            },
            "size": 12
        })
        edges.append({"from": 1, "to": node_id, "length": 160})
        node_id += 1

    # Vis.js standalone HTML iframe
    vis_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
        <style type="text/css">
            #mynetwork {{
                width: 100%;
                height: 480px;
                background-color: {bg_canvas};
                border: 1px solid {border_canvas};
                border-radius: 12px;
            }}
            body {{
                margin: 0;
                padding: 0;
                overflow: hidden;
                background-color: transparent;
            }}
        </style>
    </head>
    <body>
        <div id="mynetwork"></div>
        <script type="text/javascript">
            var nodes = new vis.DataSet({json.dumps(nodes)});
            var edges = new vis.DataSet({json.dumps(edges)});
            var container = document.getElementById('mynetwork');
            var data = {{
                nodes: nodes,
                edges: edges
            }};
            var options = {{
                nodes: {{
                    shape: 'dot',
                    font: {{
                        size: 11,
                        color: '{node_text}',
                        face: 'system-ui, sans-serif'
                    }},
                    borderWidth: 2,
                    borderColor: '{node_border}',
                    shadow: false
                }},
                edges: {{
                    width: 2,
                    color: '{edge_color}',
                    shadow: false,
                    smooth: {{
                        type: 'continuous'
                    }}
                }},
                physics: {{
                    barnesHut: {{
                        gravitationalConstant: -1800,
                        centralGravity: 0.2,
                        springLength: 90,
                        springConstant: 0.05
                    }},
                    stabilization: {{
                        iterations: 100
                    }}
                }},
                interaction: {{
                    hover: true,
                    tooltipDelay: 200,
                    zoomView: true
                }}
            }};
            var network = new vis.Network(container, data, options);
        </script>
    </body>
    </html>
    """
    
    # Render vis-network canvas in full-width component
    components.html(vis_html, height=500)
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

    # ── Text search inspector below graph ──
    categories = {
        "👤 Candidate / Document": candidate_name,
        "🛠️ Skills & Expertise": skills,
        "🚀 Projects & Research": projects,
        "🏷️ Core Entities": entities,
        "🏢 Companies / Institutions": companies
    }
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("**Graph Nodes** (Click to inspect relationship connections)")
        for category, items in categories.items():
            if items:
                with st.expander(f"{category} ({len(items) if isinstance(items, list) else 1})", expanded=False):
                    if isinstance(items, list):
                        seen = set()
                        for idx, item in enumerate(items):
                            label = item
                            if isinstance(item, dict):
                                label = item.get("title") or item.get("name") or str(item)
                            else:
                                label = str(item)
                                
                            if label in seen:
                                continue
                            seen.add(label)
                                
                            clean_key = label.replace(" ", "_").replace("\"", "").replace("'", "")
                            clean_cat = category.replace(" ", "_").replace("👤", "").replace("🛠️", "").replace("🚀", "").replace("🏷️", "").replace("🏢", "").strip()
                            if st.button(label, key=f"node_{clean_cat}_{clean_key}_{idx}", use_container_width=True):
                                connections = []
                                for c in items:
                                    if c == item:
                                        continue
                                    if isinstance(c, dict):
                                        connections.append(c.get("title") or c.get("name") or str(c))
                                    else:
                                        connections.append(str(c))
                                st.session_state.selected_node = {
                                    "name": label,
                                    "category": category,
                                    "connections": connections
                                }
                    else:
                        label = items
                        if isinstance(items, dict):
                            label = items.get("title") or items.get("name") or str(items)
                        else:
                            label = str(items)
                            
                        clean_key = label.replace(" ", "_").replace("\"", "").replace("'", "")
                        clean_cat = category.replace(" ", "_").replace("👤", "").replace("🛠️", "").replace("🚀", "").replace("🏷️", "").replace("🏢", "").strip()
                        if st.button(label, key=f"node_{clean_cat}_{clean_key}", use_container_width=True):
                            st.session_state.selected_node = {
                                "name": label,
                                "category": category,
                                "connections": [str(skills), str(projects), str(entities), str(companies)]
                            }
                            
    with col2:
        st.markdown("**Node Properties & Relations**")
        if "selected_node" in st.session_state:
            node = st.session_state.selected_node
            st.markdown(f"#### Node: `{node['name']}`")
            st.markdown(f"**Category:** {node['category']}")
            st.markdown("---")
            st.markdown("**Active Connections:**")
            for conn in node['connections']:
                if isinstance(conn, str):
                    st.markdown(f"- related to → `{conn}`")
                elif isinstance(conn, list):
                    for sub_c in conn[:3]:
                        st.markdown(f"- related to → `{sub_c}`")
        else:
            st.info("Select a node on the left to explore its local relationships.")
