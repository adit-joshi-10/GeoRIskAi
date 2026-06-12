import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


def render_global_tab(filtered_df, PLOTLY_LAYOUT):

    screen = st.session_state.get("screen_width", 1200)
    is_mobile = screen < 768

    # ── LAYOUT ──────────────────────────────────────
    if is_mobile:
        col_map    = st.container()
        col_alerts = st.container()
    else:
        col_map, col_alerts = st.columns([2, 1])

    # ── MAP ─────────────────────────────────────────
    with col_map:

        st.markdown(
            '<div class="section-label">Threat Assessment</div>'
            '<div class="section-title">Global Risk Map</div>',
            unsafe_allow_html=True,
        )

        country_coords = {
            "United States": [37.09,  -95.71],
            "Russia":        [61.52,  105.31],
            "China":         [35.86,  104.19],
            "India":         [20.59,   78.96],
            "Iran":          [32.42,   53.68],
            "Israel":        [31.04,   34.85],
            "Ukraine":       [48.37,   31.16],
            "Pakistan":      [30.37,   69.34],
            "North Korea":   [40.33,  127.51],
            "South Korea":   [35.90,  127.76],
            "Afghanistan":   [33.93,   67.71],
            "Syria":         [34.80,   38.99],
            "Venezuela":     [ 6.42,  -66.58],
            "Taiwan":        [23.69,  120.96],
        }

        filtered_df = filtered_df.copy()
        filtered_df["Latitude"]  = filtered_df["Country"].map(lambda x: country_coords.get(x, [0, 0])[0])
        filtered_df["Longitude"] = filtered_df["Country"].map(lambda x: country_coords.get(x, [0, 0])[1])

        # On mobile use flat map instead of globe
        if is_mobile:
            map_fig = go.Figure()
            map_fig.add_trace(go.Scattergeo(
                lon=filtered_df["Longitude"],
                lat=filtered_df["Latitude"],
                text=filtered_df["Country"],
                customdata=filtered_df[["Country","Dynamic_Risk_Level","Conflict_Probability","News_Risk_Score"]].values,
                hovertemplate=(
                    "<b>%{customdata[0]}</b><br>"
                    "GeoRisk: <b>%{marker.color:.3f}</b><br>"
                    "Level: <b>%{customdata[1]}</b><br>"
                    "<extra></extra>"
                ),
                mode="markers+text",
                textposition="top center",
                textfont=dict(size=8, color="#c8dde8"),
                marker=dict(
                    size=filtered_df["GeoRisk_Live_Score"] * 20 + 6,
                    color=filtered_df["GeoRisk_Live_Score"],
                    colorscale=[
                        [0.00, "#00e5ff"],
                        [0.40, "#00ffaa"],
                        [0.65, "#ffaa00"],
                        [0.85, "#ff5c00"],
                        [1.00, "#ff1a3c"],
                    ],
                    opacity=0.9,
                    line=dict(width=1, color="#ffffff"),
                    colorbar=dict(
                        title="Risk",
                        thickness=8,
                        len=0.5,
                        titlefont=dict(size=9, color="#7a9db0"),
                        tickfont=dict(size=8, color="#7a9db0"),
                    ),
                ),
            ))
            map_fig.update_layout(
                height=320,
                margin=dict(l=0, r=0, t=0, b=0),
                paper_bgcolor="#020609",
                geo=dict(
                    projection_type="natural earth",
                    bgcolor="#020609",
                    showocean=True,    oceancolor="#020d18",
                    showland=True,     landcolor="#071420",
                    showlakes=True,    lakecolor="#020d18",
                    showcountries=True, countrycolor="#16354d",
                    showcoastlines=True, coastlinecolor="#16354d",
                    showframe=False,
                    lataxis=dict(showgrid=False),
                    lonaxis=dict(showgrid=False),
                    # Center on Middle East / conflict zone
                    center=dict(lon=50, lat=25),
                    projection_scale=1.2,
                ),
            )

        else:
            # Desktop — keep the globe
            map_fig = go.Figure()
            map_fig.add_trace(go.Scattergeo(
                lon=filtered_df["Longitude"],
                lat=filtered_df["Latitude"],
                text=filtered_df["Country"],
                customdata=filtered_df[["Country","Dynamic_Risk_Level","Conflict_Probability","News_Risk_Score"]].values,
                hovertemplate=(
                    "<b>%{customdata[0]}</b><br>"
                    "GeoRisk: <b style='color:#00e5ff'>%{marker.color:.4f}</b><br>"
                    "Level: <b>%{customdata[1]}</b><br>"
                    "Conflict Prob: <b style='color:#ff9500'>%{customdata[2]:.4f}</b><br>"
                    "News Risk: <b style='color:#ff3b5c'>%{customdata[3]:.4f}</b><br>"
                    "<extra></extra>"
                ),
                mode="markers",
                marker=dict(
                    size=filtered_df["GeoRisk_Live_Score"] * 35,
                    color=filtered_df["GeoRisk_Live_Score"],
                    colorscale=[
                        [0.00, "#00e5ff"],
                        [0.35, "#00ffaa"],
                        [0.60, "#ffaa00"],
                        [0.80, "#ff5c00"],
                        [1.00, "#ff1a3c"],
                    ],
                    opacity=0.95,
                    line=dict(width=1.2, color="#ffffff"),
                ),
            ))
            map_fig.update_layout(
                height=580,
                margin=dict(l=0, r=0, t=0, b=0),
                paper_bgcolor="#020609",
                geo=dict(
                    projection_type="orthographic",
                    bgcolor="#020609",
                    showocean=True,    oceancolor="#020d18",
                    showland=True,     landcolor="#071420",
                    showlakes=True,    lakecolor="#020d18",
                    showcountries=True, countrycolor="#16354d",
                    showcoastlines=True, coastlinecolor="#16354d",
                    showframe=False,
                    lataxis=dict(showgrid=False),
                    lonaxis=dict(showgrid=False),
                    projection_rotation=dict(lon=40, lat=20, roll=0),
                ),
            )

        st.plotly_chart(map_fig, use_container_width=True)

        # ── TOP THREATS BAR CHART ────────────────────
        st.markdown(
            '<div class="section-label">Top Threats</div>'
            '<div class="section-title">Highest Risk Countries</div>',
            unsafe_allow_html=True,
        )

        top_n  = 7 if is_mobile else 10
        top10  = filtered_df.nlargest(top_n, "GeoRisk_Live_Score")

        if is_mobile:
            # Horizontal bar on mobile — much more readable
            bar_fig = px.bar(
                top10.sort_values("GeoRisk_Live_Score"),
                x="GeoRisk_Live_Score",
                y="Country",
                orientation="h",
                color="Dynamic_Risk_Level",
                color_discrete_map={
                    "Critical": "#ff3b5c",
                    "High":     "#ff9500",
                    "Medium":   "#ffe600",
                    "Low":      "#00ff88",
                },
                text="GeoRisk_Live_Score",
            )
            bar_fig.update_traces(
                texttemplate="%{x:.2f}",
                textposition="outside",
                textfont=dict(size=9, color="#c8dde8"),
            )
            bar_fig.update_layout(
                **PLOTLY_LAYOUT,
                height=280,
                margin=dict(l=0, r=40, t=20, b=0),
                showlegend=False,
                xaxis=dict(showticklabels=False, title=""),
                yaxis=dict(
                    title="",
                    tickfont=dict(size=10, color="#c8dde8"),
                ),
            )
        else:
            bar_fig = px.bar(
                top10,
                x="Country",
                y="GeoRisk_Live_Score",
                color="Dynamic_Risk_Level",
                color_discrete_map={
                    "Critical": "#ff3b5c",
                    "High":     "#ff9500",
                    "Medium":   "#ffe600",
                    "Low":      "#00ff88",
                },
                text="GeoRisk_Live_Score",
            )
            bar_fig.update_traces(
                texttemplate="%{y:.3f}",
                textposition="outside",
                textfont=dict(size=9),
            )
            bar_fig.update_layout(
                **PLOTLY_LAYOUT,
                height=320,
                bargap=0.35,
            )

        st.plotly_chart(bar_fig, use_container_width=True)

    # ── ALERTS PANEL ────────────────────────────────
    with col_alerts:

        st.markdown(
            '<div class="section-label">Intelligence Feed</div>'
            '<div class="section-title">Strategic Alerts</div>',
            unsafe_allow_html=True,
        )

        top_n_alerts = 4 if is_mobile else 6
        top_alerts   = filtered_df.nlargest(top_n_alerts, "GeoRisk_Live_Score")

        for _, row in top_alerts.iterrows():
            country = row["Country"]
            score   = row["GeoRisk_Live_Score"]
            risk    = row["Dynamic_Risk_Level"]
            news    = row["News_Risk_Score"]

            if risk == "Critical":
                color, icon = "#ff3b5c", "🔴"
            elif risk == "High":
                color, icon = "#ff9500", "🟠"
            elif risk == "Medium":
                color, icon = "#ffe600", "🟡"
            else:
                color, icon = "#00ff88", "🟢"

            st.markdown(f"""
<div style="
background:rgba(5,15,25,0.95);
border:1px solid {color};
border-radius:12px;
padding:12px 14px;
margin-bottom:10px;
">
<div style="font-size:0.7rem;color:{color};
font-family:'Share Tech Mono',monospace;
letter-spacing:0.08em;margin-bottom:5px;">
{icon} {risk.upper()} ALERT
</div>
<div style="font-size:0.95rem;font-weight:700;
color:white;margin-bottom:7px;">
{country}
</div>
<div style="display:flex;justify-content:space-between;
font-size:0.75rem;color:#9db4c0;">
<span>GeoRisk: <b>{score:.2f}</b></span>
<span>News: <b>{news:.2f}</b></span>
</div>
</div>""", unsafe_allow_html=True)

        st.markdown("---")
        st.caption("Live geopolitical intelligence monitoring active.")